"""Legal vocabulary, transparent reranking and conservative evidence checks.

These rules improve recall; they never supply a legal answer or a tariff.
"""
from __future__ import annotations

import re

from .providers import normalize_text
from ..legal_knowledge.quality import usable_legal_text

LEGAL_STOP_WORDS = {"toi", "minh", "giup", "xin", "hoi", "the", "nao", "sao", "la",
                    "va", "cua", "theo", "quy", "dinh", "duoc", "co", "khong", "ve"}


def legal_tokens(value: str) -> list[str]:
    return [word for word in re.findall(r"[a-z0-9]+", normalize_text(value))
            if len(word) > 1 and word not in LEGAL_STOP_WORDS]


def electricity_question(query: str) -> bool:
    value = normalize_text(query)
    return any(term in value for term in ("tien dien", "gia dien", "thu dien", "tinh dien", "kwh", "dinh muc dien"))


def rental_electricity_question(query: str) -> bool:
    value = normalize_text(query)
    return electricity_question(query) and not any(term in value for term in ("trom cap", "hanh lang", "duong day"))


def expand_legal_query(query: str) -> str:
    value = normalize_text(query)
    additions: list[str] = []
    if any(term in value for term in ("chu tro", "chu nha")):
        additions.append("người cho thuê nhà")
    if any(term in value for term in ("o ghep", "o chung", "sinh vien")):
        additions.append("người thuê nhà định mức số người sử dụng điện" if electricity_question(query)
                         else "người thuê nhà")
    if rental_electricity_question(query):
        additions.append("thu tiền điện người thuê nhà giá bán lẻ điện sinh hoạt hóa đơn")
    if any(term in value for term in ("phat", "xu ly", "thu thua", "hoan tra")):
        additions.append("xử phạt vi phạm hoàn trả số tiền thu thừa khắc phục hậu quả")
    return query + (". " + ". ".join(additions) if additions else "")


def rental_evidence(content: str) -> bool:
    value = normalize_text(content)
    return any(term in value for term in ("tien dien", "gia dien", "gia ban le dien", "su dung dien", "mua dien")) and any(term in value for term in
                                   ("thue nha", "nha cho thue", "chu nha", "sinh vien"))


def rerank_legal(query: str, rows: list[dict], limit: int = 30) -> list[dict]:
    rental = rental_electricity_question(query)
    question = normalize_text(query)
    penalty = any(word in question for word in ("phat", "xu ly", "thu thua", "hoan tra"))
    for row in rows:
        value = normalize_text(row["content"])
        base = float(row.get("similarity_score", 0))
        if rental:
            if not rental_evidence(str(row.get("heading") or "") + " " + row["content"]):
                row["similarity_score"] = 0.0
                continue
            phrases = ("thu tien dien", "tien dien", "nguoi thue nha", "dinh muc", "hoa don")
            coverage = sum(phrase in value for phrase in phrases) / len(phrases)
            base = 0.45 * base + 0.35 + 0.2 * coverage
            if penalty and any(term in value for term in ("phat tien", "hoan tra", "thu thua")):
                base += 0.15
            elif not penalty and "vi pham" in normalize_text(str(row.get("heading") or "")):
                base -= 0.2
        row["similarity_score"] = round(min(1.0, base), 6)
    return sorted((row for row in rows if row["similarity_score"] > 0
                   and usable_legal_text(row["content"])),
                  key=lambda row: (-row["similarity_score"], row["chunk_id"]))[:limit]


def evidence_issues(answer: str, chunks: list[dict], query: str) -> list[str]:
    """Deterministic guard, not a claim of full semantic entailment verification."""
    issues = []
    normalized = normalize_text(answer)
    if any(term in normalized for term in (
        "phap luat khong co quy dinh", "khong co quy dinh cu the", "khong co quy dinh ve",
        "khong co van ban nao", "luat khong quy dinh",
    )):
        issues.append("Không thể kết luận pháp luật không có quy định từ các đoạn truy xuất.")
    if rental_electricity_question(query) and not any(rental_evidence(row["content"]) for row in chunks):
        issues.append("Chưa tìm thấy nguồn trực tiếp về tiền điện của người thuê nhà.")
    evidence_text = normalize_text(" ".join(row["content"] for row in chunks))
    if rental_electricity_question(query):
        if any(term in normalized for term in ("phai bang", "phai dung bang")) and "khong duoc vuot qua" in evidence_text:
            issues.append("Giữ đúng giới hạn 'không được vượt quá'; không đổi thành 'phải bằng'.")
        if "lai suat" in normalized and "thoa thuan" not in normalized and "thoa thuan" in evidence_text:
            issues.append("Lãi suất hoàn trả phải giữ điều kiện do hai bên thỏa thuận trong hợp đồng.")
        if "khong ke khai hoac" in normalized or "khong ke khai du hoac" in normalized:
            issues.append("Không đổi điều kiện đồng thời 'dưới 12 tháng và không kê khai đủ người' thành 'hoặc'.")
        if (any(term in normalized for term in ("bac 2", "3 4", "04 nguoi", "4 nguoi", "bon nguoi"))
                and "ke tu ngay thuc hien" in evidence_text
                and not any(term in normalized for term in ("dieu chinh", "chuyen tiep", "thoi diem ap dung"))):
            issues.append("Phải nêu điều kiện hiệu lực gắn với lần điều chỉnh giá điện; chưa xác minh mốc thì không khẳng định đang áp dụng.")
    sources = {int(row["rank"]): normalize_text(row["content"] + " " + str(row.get("heading") or ""))
               for row in chunks}
    # Each cited sentence must share meaningful vocabulary with its own sources.
    for segment in re.split(r"\n+|(?<=[.!?])\s+", answer):
        refs = [int(ref) for ref in re.findall(r"\[(\d+)\]", segment)]
        if not refs:
            continue
        evidence = " ".join(sources.get(ref, "") for ref in refs)
        if not evidence:
            issues.append("Trích dẫn không có nguồn tương ứng.")
            continue
        terms = set(legal_tokens(re.sub(r"\[\d+\]", "", segment)))
        if terms and len(terms & set(legal_tokens(evidence))) / len(terms) < 0.18:
            issues.append("Nội dung câu trả lời không khớp từ vựng của nguồn trích dẫn.")
        amounts = re.findall(r"\b\d{1,3}(?:[.,]\d{3}){2,}\b", segment)
        for match in re.finditer(r"(\d+(?:[.,]\d+)?)\s*(?:[-–]|đến)?\s*(\d+(?:[.,]\d+)?)?\s*triệu", segment, re.I):
            amounts.extend(str(round(float(value.replace(",", ".")) * 1_000_000))
                           for value in match.groups() if value)
        for amount in amounts:
            digits = re.sub(r"\D", "", amount)
            source_numbers = {re.sub(r"\D", "", n) for n in re.findall(r"\d[\d.,]*", evidence)}
            if digits not in source_numbers:
                issues.append("Số tiền nêu trong câu trả lời chưa được nguồn trích dẫn xác nhận.")
    return list(dict.fromkeys(issues))


def append_commencement_evidence(answer: str, chunks: list[dict], query: str) -> str:
    """Retain an essential commencement condition verbatim, never invent a date.

    Only supplements an otherwise generated answer when its retrieved source has
    an explicit delayed-commencement phrase and the answer omitted that condition.
    """
    issues = evidence_issues(answer, chunks, query)
    if not any(issue.startswith("Phải nêu điều kiện hiệu lực") for issue in issues):
        return answer
    for row in chunks:
        match = re.search(r"có hiệu lực(?: thi hành)? k[ểê] từ ngày thực hiện[^.\n]{20,700}(?:\.|$)", row["content"], re.I)
        if match:
            return answer + f"\n\nĐiều kiện hiệu lực trong nguồn: “{match[0].rstrip('.')}” [{row['rank']}]."
    return answer
