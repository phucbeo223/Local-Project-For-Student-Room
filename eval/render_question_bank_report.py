"""Render the saved question-bank run into a compact, reproducible Markdown report."""
from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path

LABELS = {
    "find_listing": "Tìm và lọc phòng", "housing_contract": "Hợp đồng",
    "electricity": "Điện", "water_cantho": "Nước Cần Thơ",
    "residence": "Cư trú", "fire_safety": "PCCC",
    "student_housing": "Nhà ở sinh viên", "real_estate_brokerage": "Môi giới",
    "ecommerce_platform": "Nền tảng đăng tin", "privacy_data": "Dữ liệu cá nhân",
    "criminal_law": "Dấu hiệu lừa đảo",
}


def display(value: object) -> str:
    return "N/A" if value is None else str(value)


def metric_mean(cases: list[dict], name: str) -> str:
    values = [case.get("ragas", {}).get(name) for case in cases]
    valid = [value for value in values if isinstance(value, (int, float)) and math.isfinite(value)]
    return f"{statistics.mean(valid):.3f} ({len(valid)})" if valid else "N/A (0)"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    audit = json.loads(args.audit.read_text(encoding="utf-8")) if args.audit else None
    summary = data["summary"]
    cases = data["cases"]
    lines = [
        f"# Kết quả kiểm thử bộ {summary['questions']} câu hỏi bằng Ragas",
        "",
        f"- Bắt đầu (UTC): {data['started_at_utc']}",
        f"- Cập nhật (UTC): {data.get('updated_at_utc', 'đang chạy')}",
        f"- SHA-256 bộ câu hỏi: `{data['question_bank_sha256']}`",
        f"- Trình chấm: Ragas {data.get('judge', {}).get('version', 'chưa chạy')}; "
        f"mô hình theo chỉ số: {', '.join(f'{name}={model}' for name, model in data.get('judge', {}).get('models_by_metric', {}).items()) or data.get('judge', {}).get('model', 'chưa chạy')}",
        f"- Mô hình embedding: {data.get('judge', {}).get('embedding_model', 'intfloat/multilingual-e5-small')}",
        "",
        "## Chỉ số hệ thống",
        "",
        "| Chỉ số | Kết quả |",
        "|---|---:|",
        f"| Câu đã kiểm thử | {summary['completed']}/{summary['questions']} |",
        f"| Có ngữ cảnh truy xuất | {summary['with_contexts']}/{summary['completed']} |",
        f"| Truy xuất vector | {summary['vector_retrieval']}/{summary['completed']} |",
        f"| Có ít nhất một nguồn cùng nhãn chủ đề dự kiến | {summary['category_source_match']}/{summary['category_source_evaluated']} |",
        f"| Không đủ căn cứ / không có kết quả | {summary['no_answer']} |",
        f"| Có câu trả lời tổng hợp (chưa kiểm định độc lập) | {summary['completed'] - summary['no_answer']} |",
        f"| Câu trả lời một phần bằng trích đoạn nguồn | {summary.get('partial_answer', 0)} |",
        f"| Chế độ suy giảm | {summary['degraded']} |",
        f"| Lỗi chạy câu hỏi | {summary['errors']} |",
        f"| Đúng định dạng trích dẫn, trung bình | {display(summary['citation_format_accuracy_mean'])} |",
        f"| Độ trễ p50 / p95 | {display(summary['latency_p50_ms'])} / {display(summary['latency_p95_ms'])} ms |",
        "",
        "## Chỉ số Ragas",
        "",
        "| Chỉ số | Trung bình | Số câu được chấm |",
        "|---|---:|---:|",
    ]
    for name, label in (("faithfulness", "Bám sát ngữ cảnh"),
                        ("answer_relevancy", "Liên quan câu hỏi"),
                        ("context_utilization", "Hữu dụng của ngữ cảnh")):
        item = summary["ragas"][name]
        lines.append(f"| {label} | {display(item['mean'])} | {item['scored']} |")
    lines += [
        "| Context recall | N/A | 0 |",
        "| Answer correctness | N/A | 0 |",
        "",
        "Hai chỉ số cuối cần đáp án hoặc ngữ cảnh chuẩn được gán nhãn độc lập. Bộ câu hỏi hiện chưa có đáp án độc lập, nên không lấy câu trả lời của hệ thống làm đáp án chuẩn.",
        "",
        "## Theo nhóm câu hỏi",
        "",
        "| Nhóm | Đã kiểm thử / tổng | Có nguồn | Chưa tổng hợp được kết luận | Bám nguồn (n) | Liên quan (n) | Hữu dụng ngữ cảnh (n) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for category, counts in data["by_category"].items():
        group = [case for case in cases if case["category"] == category and "answer" in case]
        lines.append(
            f"| {LABELS.get(category, category)} | {counts['completed']}/{counts['questions']} | "
            f"{counts['with_contexts']} | {counts['no_answer']} | "
            f"{metric_mean(group, 'faithfulness')} | {metric_mean(group, 'answer_relevancy')} | "
            f"{metric_mean(group, 'context_utilization')} |"
        )
    if audit:
        stale_paths = set(audit["indexed_but_missing_from_data"])
        stale_cases = [case["id"] for case in cases if any(
            source.get("source_path") in stale_paths for source in case.get("sources", [])
        )]
        lines += [
            "", "## Trạng thái kho dữ liệu", "",
            f"Có {audit['data_files']} tệp trong `Data`, {audit['indexed_documents']} tài liệu trong DB. "
            f"Thiếu trong chỉ mục: {len(audit['missing_from_index'])}; "
            f"còn trong chỉ mục nhưng không còn tệp nguồn: {len(audit['indexed_but_missing_from_data'])}.",
            f"Embedding: {audit.get('current_document_vectors', 'N/A')}/"
            f"{audit.get('current_document_chunks', 'N/A')} đoạn của {audit['data_files']} tệp hiện hành; "
            f"{audit.get('listing_vectors', 'N/A')}/{audit.get('listing_records', 'N/A')} tin phòng đủ điều kiện.",
            f"Có {len(stale_cases)}/{summary['completed']} câu đã truy xuất ít nhất một tệp không còn trong `Data` "
            f"(câu: {', '.join(map(str, stale_cases)) if stale_cases else 'không có'}).",
            "",
            "Nguồn không còn trong kho đã được ngừng truy xuất và giữ nội dung để khôi phục." if not stale_paths else "Còn đường dẫn vắng trong kho cần xử lý; không diễn giải điểm như chất lượng riêng của tập hiện hành.",
        ]
    issues = [case for case in cases if case.get("error") or case.get("ragas_errors") or
              case.get("category_source_match") is False or case.get("degraded") or case.get("no_answer")]
    lines += ["", "## Các câu cần xem lại", ""]
    if issues:
        for case in issues[:30]:
            reasons = []
            if case.get("error"):
                reasons.append("lỗi chạy")
            if case.get("ragas_errors"):
                reasons.append("lỗi Ragas: " + ", ".join(case["ragas_errors"]))
            if case.get("category_source_match") is False:
                reasons.append("chưa có nguồn mang nhãn chủ đề dự kiến")
            if case.get("degraded"):
                reasons.append("chế độ suy giảm")
            if case.get("partial_answer"):
                reasons.append("trả lời một phần bằng trích đoạn, chưa kết luận áp dụng")
            elif case.get("no_answer"):
                reasons.append("chưa đủ căn cứ trả lời")
            lines.append(f"- Câu {case['id']}: {'; '.join(reasons)}.")
        if len(issues) > 30:
            lines.append(f"- Còn {len(issues) - 30} câu cần xem lại trong JSON chi tiết.")
    else:
        lines.append("Chưa ghi nhận lỗi hoặc câu trả lời cần xem lại theo các quy tắc tự động.")
    lines += [
        "", "## Giới hạn", "",
        "- Faithfulness đo mức nhất quán với các đoạn đã lấy, không chứng minh văn bản đúng hoặc còn hiệu lực.",
        "- Context utilization so với câu trả lời của chính hệ thống; đây không phải context precision so với đáp án độc lập.",
        f"- Giới hạn ngữ cảnh Ragas: {data.get('judge', {}).get('context_limit')} đoạn, giới hạn ký tự mỗi đoạn {display(data.get('judge', {}).get('context_char_limit'))}; Answer Relevancy strictness=1. Cửa sổ token của mô hình vẫn có giới hạn.",
        "- Mô hình sinh và chấm thuộc cùng họ Qwen local; điểm có thể thiên lệch. Cần người đánh giá độc lập cho kết luận pháp lý.",
        "- Câu không có ngữ cảnh không bị gán điểm 0. Câu từ chối tổng hợp có nguồn được chấm nếu bật score_abstentions; điểm được tính thật, không giả lập.",
        "- Tỷ lệ cùng nhãn chủ đề chỉ kiểm tra source.category với một nhãn dự kiến của câu hỏi. Nguồn khác nhóm có thể liên quan; đây là cảnh báo định tuyến/truy xuất, không phải tỷ lệ câu trả lời đúng hoặc trích dẫn được nguồn hỗ trợ.",
        "- JSON chi tiết lưu từng câu, nguồn, ngữ cảnh, loại truy xuất, mô hình, độ trễ và lỗi chấm để kiểm tra lại.",
        "",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
