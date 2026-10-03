"""Preserve an archived baseline and compare answers under one judge method."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

METRICS = ("faithfulness", "answer_relevancy", "context_utilization")
METHOD_FIELDS = ("library", "version", "model", "provider", "embedding_model",
                 "answer_relevancy_strictness", "context_char_limit", "score_abstentions",
                 "max_output_tokens", "temperature", "context_policy", "score_workers", "judge_request_timeout_seconds")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clone(source, target):
    if target.exists():
        raise ValueError("Baseline clone already exists; resume scoring it without overwriting")
    data = read(source)
    data["archived_baseline"] = {
        "path": source.as_posix(), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "original_judge": data.pop("judge", {}), "original_summary": read(source)["summary"],
        "cloned_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    for case in data["cases"]:
        for name in ("ragas", "ragas_errors", "ragas_usage", "ragas_retry_history", "ragas_judgements"):
            if name in case:
                case.setdefault("archived_evaluation", {})[name] = case.pop(name)
    for metric in data["summary"]["ragas"].values():
        metric.update(mean=None, scored=0)
    data["method"] = "Archived unchanged answers and contexts; rescored by a common judge"
    write(target, data)
    print(f"Preserved {len(data['cases'])} archived answers in {target}")


def valid(value):
    return isinstance(value, (int, float)) and math.isfinite(value)


def status(case):
    if "error" in case:
        return "lỗi chạy"
    if "answer" not in case:
        return "chưa hoàn tất"
    if case.get("partial_answer"):
        return "một phần"
    if case.get("no_answer"):
        return "chưa đủ căn cứ"
    return "tổng hợp"


def render(before_path, after_path, audit_path, output):
    before, after, audit = read(before_path), read(after_path), read(audit_path)
    if before["question_bank_sha256"] != after["question_bank_sha256"]:
        raise ValueError("Different question banks cannot be compared")
    old = {case["id"]: case for case in before["cases"]}
    pairs = [(old[case["id"]], case) for case in after["cases"]]
    if any(a["question"] != b["question"] for a, b in pairs):
        raise ValueError("Question text mismatch")
    common = all(before.get("judge", {}).get(k) == after.get("judge", {}).get(k)
                 for k in METHOD_FIELDS) and bool(before.get("judge")) and bool(after.get("judge"))
    lines = ["# Nâng cấp model và kiểm thử 36 câu pháp lý", "",
        "Phạm vi: hợp đồng, cư trú, PCCC, điện, nước, môi giới, dữ liệu cá nhân, nền tảng và hình sự. Các câu giá phòng, khoảng cách và dữ liệu phòng cũ được loại khỏi lượt đánh giá.", "",
        "## Máy và model", "",
        "- Ryzen 5 7535HS; RAM khoảng 15,2 GiB; RTX 4050 Laptop 6.141 MiB VRAM.",
        "- Cài Qwen 3.5 9B Q4_K_M (khoảng 6,6 GB); xóa Qwen 3.5 4B và Qwen 2.5 1.5B sau khi thử model mới thành công.",
        "- Thử local ở cửa sổ 8.192 token: khoảng 25,44 giây, 7,52 token/giây. Ngữ cảnh lớn hơn có thể phải dùng thêm RAM.",
        "- Cấu hình cuối: Gemini 3.5 Flash Lite ưu tiên, Qwen 9B dự phòng. Đọc đầy đủ các khóa đánh số, ưu tiên slot 3 đã gọi thành công; slot 2 bị Google từ chối quyền dự án (HTTP 403), slot 1 gặp quá tải khi thử Gemini 3.8 (HTTP 503). Không ghi khóa vào báo cáo.",
        "- Lượt thử Gemini 3.8 chạm hạn mức ngày 20 lượt (HTTP 429), phải chuyển sang local và chậm. Giữ checkpoint ban đầu và lượt local riêng, rồi chạy đủ 36 câu mới bằng cấu hình cuối. Bộ chấm Gemini 3.5 chạm 500 lượt/ngày; lưu riêng lượt chấm đó, rồi chấm lại cả hai bộ bằng Gemini 3.1 Flash Lite với cùng tham số.", "",
        "## Sửa hệ thống", "",
        "- Sửa cấu hình Compose từng ghi đè provider/model; giữ khóa trong .env.",
        "- Phân biệt lỗi quyền với quá tải; tạm ngừng gọi model khi 503/429. Không đổi khóa để vượt hạn mức 429.",
        "- Truy xuất đúng hơn cho công khai dữ liệu cá nhân và phòng tránh lừa đảo; giảm các điều khoản định danh, thông báo sự cố hoặc thẩm quyền tố tụng lệch câu hỏi.",
        "- Phân biệt ‘tài liệu này không nêu’ với ‘pháp luật không quy định’; cho sửa câu trả lời một lần theo lỗi kiểm tra nguồn, rồi kiểm tra lại.",
        "- Bước kiểm tra local chỉ gửi mỗi nguồn một lần, giữ toàn bộ nội dung/ngoại lệ và ánh xạ trích dẫn; giới hạn giải thích lỗi ngắn. Không sinh lại khi bộ kiểm tra không khả dụng; vẫn chuyển về trích đoạn/từ chối khi chưa xác nhận được.",
        "- Chặn kết luận xử phạt/bồi thường/hoàn trả thiếu trích dẫn hoặc thiếu căn cứ trực tiếp; sau khi rà đủ 36 câu, chỉ câu 23 bị phát hiện lỗi mới và được chạy lại. 35 câu còn lại giữ nguyên. Hạn mức ngày dùng thời gian chờ Google cung cấp.",
        "- 89 kiểm tra hồi quy đạt. Kiểm thử câu hỏi dùng ChatService và cơ sở dữ liệu thật; tắt ghi sự kiện chat trong runner.",
        f"- Kho đã nạp: {audit['data_files']} tài liệu, {audit['current_document_vectors']}/{audit['current_document_chunks']} đoạn có embedding; {len(audit['missing_from_index'])} nguồn chưa nạp, {len(audit['indexed_but_missing_from_data'])} nguồn ready vắng trong Data.", "",
        "## Kết quả vận hành", "",
        "| Chỉ số | Trước | Sau |", "|---|---:|---:|"]
    def full(data):
        return sum(status(c) == "tổng hợp" for c in data["cases"])
    for label, a, b in [
        ("Câu đã chạy", before["summary"]["completed"], after["summary"]["completed"]),
        ("Phản hồi gán trạng thái tổng hợp", full(before), full(after)),
        ("Câu trả lời một phần", before["summary"]["partial_answer"], after["summary"]["partial_answer"]),
        ("Chưa đủ căn cứ tổng hợp", sum(status(c) == "chưa đủ căn cứ" for c in before["cases"]), sum(status(c) == "chưa đủ căn cứ" for c in after["cases"])),
        ("Lỗi chạy", before["summary"]["errors"], after["summary"]["errors"]),
        ("Độ trễ p50 (giây)", round(before["summary"]["latency_p50_ms"] / 1000, 2), round(after["summary"]["latency_p50_ms"] / 1000, 2)),
        ("Độ trễ p95 (giây)", round(before["summary"]["latency_p95_ms"] / 1000, 2), round(after["summary"]["latency_p95_ms"] / 1000, 2)),
    ]:
        lines.append(f"| {label} | {a} | {b} |")
    providers = Counter(f"{c.get('generation_provider')}/{c.get('generation_model') or '-'}" for c in after["cases"] if "answer" in c)
    calls = [call for case in after["cases"] for call in case.get("provider_calls", [])]
    attempts = Counter(f"{c['provider']}/{c['model']}/{c['method']}" for c in calls)
    failures = Counter(f"{c['provider']}/{c.get('error_type', '-')}/{c.get('http_status', '-')}" for c in calls if not c.get("success"))
    lines += ["", f"Provider của phản hồi cuối: {dict(providers)}.",
        f"Các lần gọi model, bao gồm thử trước khi chuyển về trích đoạn: {dict(attempts)}.",
        f"Lỗi gọi model: {dict(failures)}. JSON lưu thời gian từng lần gọi.", "",
        "## Ragas: chấm lại bằng cùng phương pháp", "",
        f"Phương pháp khớp: {'có' if common else 'không; không kết luận mức tăng điểm'}. Mô hình: {after.get('judge', {}).get('model')}; Ragas {after.get('judge', {}).get('version')}; dùng toàn bộ nguồn đã đưa vào sinh câu trả lời, chấm cả câu từ chối, Answer Relevancy strictness=1, E5 đa ngôn ngữ.", "",
        "Các trung bình dưới đây chỉ lấy những câu có điểm ở **cả hai lượt**. Mỗi metric có số cặp riêng; lỗi chấm được giữ trong JSON.", "",
        "| Metric | Trước | Sau | Chênh lệch | Số cặp |", "|---|---:|---:|---:|---:|"]
    for name in METRICS:
        values = [(a.get("ragas", {}).get(name), b.get("ragas", {}).get(name)) for a, b in pairs]
        values = [(a, b) for a, b in values if valid(a) and valid(b)]
        a = statistics.mean(x for x, _ in values) if values else None
        b = statistics.mean(x for _, x in values) if values else None
        fmt = lambda v: f"{v:.4f}" if v is not None else "N/A"
        delta = f"{b-a:+.4f}" if common and a is not None else "N/A"
        lines.append(f"| {name} | {fmt(a)} | {fmt(b)} | {delta} | {len(values)} |")
    lines += ["", "### Đọc kết quả", "",
        "Không xem số câu tổng hợp tăng là bằng chứng độ đúng tăng. Đối chiếu cả ba metric và từng phán định nguồn; giữ nguyên điểm native Ragas, không loại câu hoặc sửa prompt chấm để nâng điểm.",
        "Độ trễ p50 đo câu điển hình; p95 phản ánh các lượt chuyển về local khi Gemini hết quota. Model 9B đã chạy được trên máy, nhưng không đáp ứng cùng tốc độ với Gemini cho kiểm tra pháp lý dài.", "",
        "### Phân tích các điểm bám nguồn thấp", "",
        "Các ví dụ dưới đây là phán định tự động, chưa phải kết luận của chuyên gia luật:", ""]
    noncommittal = [c for c in after['cases'] if any(j.get('output', {}).get('noncommittal')
        for j in c.get('ragas_judgements', {}).get('answer_relevancy', []))]
    flagged_as_full = [c['id'] for c in noncommittal if status(c) == 'tổng hợp']
    lines.append(f"- Judge ghi noncommittal ở {len(noncommittal)} câu: {[c['id'] for c in noncommittal]}. Trong đó {flagged_as_full} vẫn được hệ thống gán trạng thái tổng hợp dù nội dung nói chưa tìm thấy căn cứ cho yêu cầu chính. Vì vậy số 30 không phải số câu đã giải quyết đúng; cần rà cách đánh dấu mức hoàn thành và bổ sung nguồn đúng câu hỏi.")
    for case_id in (2, 13, 17, 19, 22):
        case = next((c for c in after['cases'] if c['id'] == case_id), None)
        if not case:
            continue
        rejected = []
        for judgement in case.get('ragas_judgements', {}).get('faithfulness', []):
            if judgement.get('schema') == 'NLIStatementOutput':
                rejected.extend(s for s in judgement.get('output', {}).get('statements', []) if s.get('verdict') == 0)
        if rejected:
            lines.append(f"- Câu {case_id}: {len(rejected)} phát biểu bị chấm không được nguồn hỗ trợ; chi tiết ở JSON.")
            for statement in rejected[:2]:
                claim = statement.get('statement', '').replace(chr(10), ' ')
                reason = statement.get('reason', '').replace(chr(10), ' ')
                lines.append(f"  - Phát biểu: {claim} Lý do judge: {reason}")
    lines += ["",
        "Lời giới thiệu và lời nhắc tham khảo cũng bị native Faithfulness tính thành phát biểu thiếu nguồn. Đây là giới hạn của phép đo; không bỏ chúng khỏi điểm công bố. Ở câu 13, judge dường như nhầm phần ‘Lược khỏi bản trích’ về các trường hợp đặc thù không liên quan với phần hồ sơ Điều 28 vẫn được giữ trước đó; đây là lỗi chấm cần con người kiểm tra, không đủ để kết luận câu trả lời sai. Câu 17 cần tách lời khuyên kiểm tra với nghĩa vụ được điều luật quy định. Nguồn và lý do chấm lưu nguyên vẹn để rà soát.",
        "Câu 4 có Khoản 2 Điều 328 bị kết thúc ở ‘trừ trườ’ ngay trong DOCX Data/housing_contract/Bộ-luật-91-2015-QH13-trích-tuyển.docx; nguồn được truy xuất cũng kết thúc như vậy. Đây là lỗi tài liệu đầu vào, không phải cắt prompt. Cần bổ sung từ bản gốc chính thức, nạp lại và kiểm thử câu bị ảnh hưởng; không tự điền ngoại lệ từ trí nhớ model."]
    legacy = before.get("archived_baseline", {}).get("original_summary", {}).get("ragas", {})
    lines += ["", f"Điểm Qwen chấm cũ, chỉ để lưu lịch sử và không dùng tính mức tăng: {legacy}.", "",
        "### Điểm lượt sau theo mức trả lời", "",
        "| Nhóm | Số câu | Faithfulness | Answer relevancy | Context utilization |",
        "|---|---:|---:|---:|---:|"]
    for group in ("tổng hợp", "một phần", "chưa đủ căn cứ"):
        members = [c for c in after["cases"] if status(c) == group]
        cells = []
        for name in METRICS:
            scores = [c.get("ragas", {}).get(name) for c in members]
            scores = [s for s in scores if valid(s)]
            cells.append(f"{statistics.mean(scores):.4f} (n={len(scores)})" if scores else "N/A")
        lines.append(f"| {group} | {len(members)} | " + " | ".join(cells) + " |")
    lines += ["",
        "### Các lỗi chưa được giải quyết đầy đủ", "",
        "Lý do dưới đây do bước kiểm tra tự động ghi nhận, cần đọc lại nguồn để phân biệt lỗi thật với từ chối quá mức. Từ chối hoặc trích đoạn không được tính là đã giải quyết câu hỏi.", ""]
    unresolved = [c for c in after["cases"] if status(c) != "tổng hợp"]
    for case in unresolved:
        reasons = [r for r in case.get("degraded_reasons", []) if "Câu trả lời dùng mẫu" not in r]
        explanation = " ".join(reasons[:2]) or case.get("error") or "Chưa đủ căn cứ tổng hợp theo nguồn được truy xuất."
        lines.append(f"- Câu {case['id']} ({case['category']}): {explanation.replace(chr(10), ' ')}")
    lines += ["",
        "### Giới hạn của kết quả", "",
        "- Chưa có đáp án và nhãn điều khoản độc lập: answer_correctness và context_recall chưa đo được. Faithfulness cao có thể do trả lời ngắn hoặc từ chối; phải đọc cùng mức trả lời đầy đủ.",
        "- Bộ chấm bằng mô hình vẫn có thiên lệch; nếu Gemini cũng sinh câu trả lời thì có thêm nguy cơ thiên lệch cùng họ model. Điểm không xác nhận độ đúng pháp lý hay hiệu lực văn bản.",
        "- Lượt sau thay cả model, truy xuất và bước kiểm tra/sửa câu trả lời; không quy toàn bộ chênh lệch cho riêng model 9B hoặc Gemini.",
        "- Cùng nhãn chủ đề và trích dẫn đúng định dạng không chứng minh điều khoản đúng hoặc bao phủ đầy đủ tình huống. Quá tải Google ảnh hưởng độ trễ và việc chuyển sang local.", "",
        "## Chi tiết từng câu", "",
        "F/R/C lần lượt là Faithfulness / Answer Relevancy / Context Utilization; dấu — là chưa có điểm hợp lệ.", "",
        "| Câu | Chủ đề | Trước | Sau | F/R/C trước | F/R/C sau | Provider/model sau | Lỗi chấm trước / sau |", "|---|---|---|---|---|---|---|---|"]
    for a, b in pairs:
        errors = f"{','.join(a.get('ragas_errors', {})) or '-'} / {','.join(b.get('ragas_errors', {})) or '-'}"
        metric_cells = lambda c: ' / '.join(f"{c.get('ragas', {}).get(m):.3f}" if valid(c.get('ragas', {}).get(m)) else '—' for m in METRICS)
        lines.append(f"| {b['id']} | {b['category']} | {status(a)} | {status(b)} | {metric_cells(a)} | {metric_cells(b)} | {b.get('generation_provider', '-')}/{b.get('generation_model') or '-'} | {errors} |")
    lines += ["", "JSON giữ nguyên câu hỏi, câu trả lời, nguồn, ngữ cảnh, thời gian và lý do chặn kết luận để kiểm tra từng lỗi.", "",
        "## Tài liệu kỹ thuật", "",
        "- [Qwen 3.5 9B trên Ollama](https://ollama.com/library/qwen3.5:9b).",
        "- [Gemini JSON Schema](https://ai.google.dev/gemini-api/docs/structured-output).",
        "- [Định nghĩa Faithfulness của Ragas](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/).", ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--clone", action="store_true")
    args = parser.parse_args()
    if args.clone:
        clone(args.before, args.after)
    else:
        if not args.audit or not args.output:
            parser.error("Rendering requires --audit and --output")
        render(args.before, args.after, args.audit, args.output)


if __name__ == "__main__":
    main()
