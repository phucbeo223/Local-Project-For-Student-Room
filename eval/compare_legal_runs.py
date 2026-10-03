"""Compare the same legal questions; keep judge-method differences explicit."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    before = json.loads(args.before.read_text(encoding="utf-8"))
    after = json.loads(args.after.read_text(encoding="utf-8"))
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    original = {case["question"]: case for case in before["cases"]}
    pairs = [(original[case["question"]], case) for case in after["cases"]]
    stale_paths = set(json.loads((args.before.parent / "question_bank_corpus_audit_2026-10-01.json").read_text(encoding="utf-8"))["indexed_but_missing_from_data"])
    def count(field, value, side):
        return sum(pair[side].get(field) == value for pair in pairs)
    def stale(side):
        return sum(any(source.get("source_path") in stale_paths for source in pair[side].get("sources", [])) for pair in pairs)
    lines = ["# Kết quả sửa và kiểm thử phần pháp lý, điện và nước", "",
        "Phạm vi: 36 câu pháp lý tương ứng câu 19–38 và 43–58 của bộ cũ. Tạm bỏ câu giá thuê, khoảng cách, tin phòng và KTX theo yêu cầu; không dùng dữ liệu phòng cũ để kết luận chất lượng tìm phòng.", "",
        "## Các sửa đổi đã thực hiện", "",
        "| Nhóm | Thay đổi |", "|---|---|",
        "| Định tuyến | Khớp cụm từ có ranh giới; bổ sung chủ đề điện, nước, cư trú, PCCC, môi giới, dữ liệu cá nhân, nền tảng và hình sự. |",
        "| Truy xuất | Lọc chủ đề chính và nguồn hỗ trợ liên chủ đề; ưu tiên điều khoản hợp đồng/hồ sơ cư trú, giảm nguồn xử phạt khi hỏi thủ tục; bỏ đoạn giới thiệu biên tập làm nguồn kết luận. |",
        "| Vòng đời nguồn | Ngừng dùng 24 đường dẫn vắng trong Data; giữ đoạn/vectors cũ và lưu metadata trước thay đổi. Không coi vắng tệp là hết hiệu lực pháp luật. |",
        "| Tách đoạn/tài liệu | Nhận tiêu đề Điều dạng dấu gạch và Markdown. Sửa tham chiếu ‘và Phụ lục’ làm mất tiêu đề hiệu lực. Thêm tóm tắt phạm vi nước, giữ nguyên DOCX đầu vào. |",
        "| Kiểm tra kết luận | Kiểm tra kết luận chưa trích dẫn, số tiền không có trong nguồn, khẳng định sai về thiếu quy định; đối chiếu từng câu với chính nguồn được trích. Nếu không xác nhận được, chỉ trích nguyên đoạn phù hợp và đánh dấu câu trả lời một phần. |",
        "| Đánh giá | Chỉ đánh giá 36 câu pháp lý; nạp embedding trước; lưu từng câu, nguồn, ngữ cảnh, độ trễ, lỗi và ba chỉ số Ragas. Giá thuê/khoảng cách/hội thoại chọn phòng chờ Data mới. |", "",
        "## Đối chiếu cùng 36 câu", "",
        "| Chỉ số vận hành | Trước | Sau |", "|---|---:|---:|",
        f"| Đi vào kho pháp lý | {count('intent', 'legal_question', 0)}/36 | {count('intent', 'legal_question', 1)}/36 |",
        f"| Có ít nhất một nguồn cùng nhãn câu hỏi | {count('category_source_match', True, 0)}/36 | {count('category_source_match', True, 1)}/36 |",
        f"| Truy xuất đường dẫn không còn trong Data | {stale(0)}/36 | {stale(1)}/36 |",
        f"| Không đủ căn cứ tổng hợp / không có kết quả | {count('no_answer', True, 0)} | {count('no_answer', True, 1)} |", "",
        f"Trong các câu chưa tổng hợp được kết luận, lượt sau có {count('partial_answer', True, 1)} câu đưa được trích đoạn liên quan, gắn cờ `partial_answer`. Chúng không được coi là câu trả lời hoàn chỉnh.", "",
        "Cùng nhãn chỉ phản ánh chọn nhóm nguồn, không phải tỷ lệ trả lời đúng. Nguồn liên chủ đề cần xem nội dung. Từ chối tổng hợp có thể do thiếu nguồn, sai kết luận hoặc bước kiểm tra bằng mô hình không xác nhận được; không đồng nghĩa luật không có quy định.", "",
        "## Nạp dữ liệu và kiểm tra", "",
        f"- Nguồn đang truy xuất: {audit['data_files']} tài liệu; {audit['current_document_vectors']}/{audit['current_document_chunks']} đoạn có vector.",
        f"- Nguồn chưa nạp: {len(audit['missing_from_index'])}; nguồn ready vắng trong Data: {len(audit['indexed_but_missing_from_data'])}.",
        "- Hồi quy: 72 kiểm tra qua. Kiểm thử câu hỏi chạy bằng ChatService thực, DB thật, embedding E5 và Qwen local; tắt ghi sự kiện chat trong runner.", "",
        "## Metrics Ragas của lượt sau", "",
        "| Metric | Trung bình | Số câu có điểm |", "|---|---:|---:|"]
    for name, values in after["summary"]["ragas"].items():
        lines.append(f"| {name} | {values['mean'] if values['mean'] is not None else 'N/A'} | {values['scored']} |")
    lines += ["| context_recall | N/A: chưa có đáp án độc lập | 0 |",
              "| answer_correctness | N/A: chưa có đáp án độc lập | 0 |", "",
              f"Mô hình chấm: {after.get('judge', {}).get('models_by_metric', {})}. Lượt sau dùng toàn bộ ngữ cảnh; lượt cũ chỉ dùng 2 đoạn × 1.200 ký tự và mô hình khác cho hai metric. Không suy ra mức cải thiện Ragas trực tiếp giữa hai phương pháp.", "",
              "Ragas và bước kiểm tra kết luận đều dùng mô hình local; điểm không chứng minh văn bản còn hiệu lực hoặc câu trả lời đúng pháp lý. Cần gán nhãn độc lập để đo mức đúng và đầy đủ. Câu không đủ căn cứ được báo riêng, không giả lập đáp án chuẩn từ chính câu trả lời.", "",
              "## Hạn chế còn phải khắc phục", "",
              "Lượt này hoàn tất nạp dữ liệu, sửa luồng truy xuất và đo lại. Chất lượng trả lời pháp lý chưa đạt mức nghiệm thu: phần lớn phản hồi chỉ trích đoạn và chưa giải thích cách áp dụng cho câu hỏi.", "",
              "- Bước kiểm tra bằng Qwen có cả dấu hiệu bỏ sót lẫn từ chối quá mức: một số lý do đánh đồng lời khuyên ‘nên kiểm tra’ với nghĩa vụ bắt buộc, hoặc không nhận đủ thông tin trong tiêu đề nguồn. Lý do tự động không phải kết luận của người kiểm định.",
              "- Một số câu tổng hợp đã bị chặn vì bổ sung điều kiện, quyền hoặc thủ tục không xuất hiện trong nguồn được trích; bản trả lời sau cùng chuyển sang trích nguyên văn thay vì giữ kết luận này.",
              "- Một nguồn đúng nhãn chưa bảo đảm đủ điều khoản để trả lời toàn bộ tình huống. Câu 29 lấy nguồn cư trú nhưng thiếu nguồn cùng nhãn dữ liệu cá nhân; phải kiểm tra mức bao phủ hai phần của câu hỏi.",
              "- Cần đáp án tham chiếu và nhãn điều khoản độc lập cho từng câu, rồi đối chiếu cả truy xuất, kết luận và độ đầy đủ. Hiện chưa đo được answer correctness/context recall; không tính câu trích đoạn là đã giải quyết xong yêu cầu tư vấn.", "",
              "## Chi tiết từng câu", "",
              "| Câu mới / cũ | Chủ đề | Trạng thái |", "|---|---|---|"]
    for old, case in pairs:
        status = "lỗi chạy" if case.get("error") else "chưa hoàn tất" if "answer" not in case else "một phần: trích đoạn, chưa kết luận áp dụng" if case.get("partial_answer") else "chưa đủ căn cứ tổng hợp" if case.get("no_answer") else "có câu trả lời tổng hợp, chưa kiểm định độc lập"
        metric_errors = ", ".join(case.get("ragas_errors", {}))
        lines.append(f"| {case['id']} / {old['id']} | {case['category']} | {status}" + (f"; lỗi chấm {metric_errors}" if metric_errors else "") + " |")
    lines += ["", "JSON chi tiết giữ nguyên câu trả lời, nguồn, ngữ cảnh, lý do từ chối và lỗi chấm để kiểm tra lại.", ""]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
