"""Report a saved proxy run without treating operational success as legal accuracy."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def ids(cases, predicate):
    return ", ".join(str(c["id"]) for c in cases if predicate(c)) or "không có"


def status(case):
    if case.get("error"):
        return "lỗi thực thi"
    if case.get("partial_answer"):
        return "trả lời một phần"
    if case.get("no_answer"):
        return "chưa đủ căn cứ"
    return "đủ theo kiểm tra hệ thống"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--revision", default="unknown")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    cases, summary = data["cases"], data["summary"]
    completed = [c for c in cases if "answer" in c]
    providers = Counter(c.get("generation_provider") for c in completed)
    called = sum(any(p.get("provider") == "gemini" and p.get("method") == "generate"
                     for p in c.get("provider_calls", [])) for c in completed)
    judge = data.get("judge", {})
    lines = ["# Kiểm thử lại 36 câu qua Gemini proxy", "",
             "Lượt chạy dùng pipeline và DB thật của API chính, kho `public`, agent riêng tắt; "
             "runner gọi dịch vụ nội bộ để lưu đầy đủ ngữ cảnh, tắt telemetry. "
             "Không dùng bộ đáp án ngoài làm chuẩn đúng/sai.", "",
             f"- Bắt đầu UTC: {data['started_at_utc']}; kết thúc UTC: {data.get('updated_at_utc')}.",
             "- Model trả lời được cấu hình: `gemini-3.8-flash-high` qua proxy local.",
             f"- Bộ chấm: Ragas {judge.get('version')}, {judge.get('provider')}/{judge.get('model')}; "
             f"{judge.get('score_workers')} worker; chấm cả phản hồi một phần có nguồn.",
             f"- JSON đầy đủ: `{args.input.name}`; SHA-256 bộ câu hỏi: `{data['question_bank_sha256']}`.",
             "", "## Kết quả thực thi", "", "| Chỉ số | Kết quả |", "|---|---:|",
             f"| Hoàn thành | {summary['completed']}/{summary['questions']} |",
             f"| Lỗi thực thi | {summary['errors']} |",
             f"| Có ngữ cảnh / truy xuất vector | {summary['with_contexts']} / {summary['vector_retrieval']} |",
             f"| Có nguồn cùng nhóm câu hỏi | {summary['category_source_match']}/{summary['category_source_evaluated']} |",
             f"| Đủ theo kiểm tra hệ thống | {summary['completed'] - summary['no_answer']} |",
             f"| Chưa đủ căn cứ, gồm phản hồi một phần | {summary['no_answer']} |",
             f"| Trả lời một phần | {summary['partial_answer']} |",
             f"| Chế độ suy giảm | {summary['degraded']} |",
             f"| Định dạng trích dẫn trung bình | {summary['citation_format_accuracy_mean']} |",
             f"| Độ trễ p50 / p95 | {summary['latency_p50_ms']} / {summary['latency_p95_ms']} ms |", "",
             f"Gemini được gọi sinh câu trả lời ở {called}/{len(completed)} câu. "
             "Một số câu được trả lời trực tiếp bằng nguồn; câu bị kiểm tra bác bỏ có thể chuyển dự phòng. "
             f"Provider cuối cùng: {dict(providers)}.", "",
             "## Điểm Ragas", "", "| Chỉ số | Trung bình | Số điểm hợp lệ |", "|---|---:|---:|"]
    for metric, values in summary["ragas"].items():
        lines.append(f"| {metric} | {values['mean'] if values['mean'] is not None else 'N/A'} | {values['scored']}/{len(cases)} |")
    lines += ["", "Các điểm đo mức bám ngữ cảnh và liên quan câu hỏi. Chưa có đáp án chuẩn độc lập, "
              "nên không báo tỷ lệ đúng pháp luật, Answer Correctness hay Context Recall. "
              "Model sinh và model chấm đều do cùng proxy cung cấp, thuộc họ Gemini theo tên alias; "
              "có thể có thiên lệch và chưa xác minh model nền thực tế.", "",
              "## Phạm vi dữ liệu và sửa lỗi", "",
              f"Kho chính có {audit['indexed_documents']} tài liệu, {audit['current_document_chunks']} đoạn, "
              f"{audit['current_document_vectors']} vector. Trong {audit['data_files']} tệp Data, "
              f"{len(audit['missing_from_index'])} tệp chưa được nạp; "
              f"{len(audit['indexed_but_missing_from_data'])} đường dẫn chỉ mục vắng tệp nguồn.", "",
              "Các tệp chưa nạp:", ""]
    lines.extend(f"- `{name}`" for name in audit["missing_from_index"])
    lines += ["", "Lượt trước sửa lỗi dừng sau 6 phản hồi và được giữ riêng. Proxy bọc JSON trong Markdown; "
              "đã sửa để chỉ bỏ lớp bọc hoàn chỉnh, vẫn giữ kiểm tra JSON/schema và lỗi cắt token. "
              "Runner chấm được sửa truyền đúng endpoint proxy. 37 kiểm tra hồi quy đã đạt; "
              "API chính đã build lại và kiểm tra JSON proxy thành công.", "",
              "## Từng câu", "", "| Câu | Chủ đề | Trạng thái | Provider / model cuối | F | AR | CU |", "|---|---|---|---|---:|---:|---:|"]
    for case in cases:
        scores = [case.get("ragas", {}).get(name) for name in ("faithfulness", "answer_relevancy", "context_utilization")]
        cells = [str(v) if v is not None else "N/A" for v in scores]
        lines.append(f"| {case['id']} | {case['category']} | {status(case)} | "
                     f"{case.get('generation_provider')} / {case.get('generation_model') or '—'} | {' | '.join(cells)} |")
    lines += ["", f"Câu chưa đủ căn cứ: {ids(cases, lambda c: c.get('no_answer'))}.",
              f"Câu trả lời một phần: {ids(cases, lambda c: c.get('partial_answer'))}.", "",
              "Trạng thái đủ là kết quả kiểm tra của hệ thống, không phải chứng nhận độc lập về đúng luật."]
    low_faithfulness = [(c["id"], c["ragas"]["faithfulness"]) for c in cases
                        if isinstance(c.get("ragas", {}).get("faithfulness"), (int, float))
                        and c["ragas"]["faithfulness"] < .5]
    lines += ["", f"Ưu tiên rà thủ công các câu có Faithfulness dưới 0,5: {low_faithfulness}. "
              "Đặc biệt câu 17 đã được kiểm tra của hệ thống chấp nhận nhưng bộ chấm báo bám nguồn thấp."]
    scoring_errors = [(c["id"], metric) for c in cases for metric in c.get("ragas_errors", {})]
    retries = sum(len(c.get("ragas_retry_history", [])) for c in cases)
    lines += ["", f"Số metric đã thử lại có lưu lỗi trước đó: {retries}. "
              f"Các metric vẫn lỗi: {scoring_errors or 'không có'}."]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    answers = ["# Toàn bộ phản hồi của lượt test Gemini proxy", "",
               "Đây là phản hồi hệ thống đã lưu, chưa được xác minh pháp lý độc lập.", ""]
    for case in cases:
        answers += [f"## Câu {case['id']}: {case['question']}", "", f"Trạng thái: {status(case)}.", "",
                    case.get("answer", case.get("error", "Chưa có phản hồi")), "", "Nguồn truy xuất:", ""]
        for source in case.get("sources", []):
            title = source.get("title", "Nguồn")
            link = f"[{title}]({source['source_url']})" if source.get("source_url") else title
            answers.append(f"- [{source.get('rank')}] {link}; `{source.get('source_path')}`; {source.get('heading') or ''}")
        if case.get("degraded_reasons"):
            answers += ["", "Lý do hệ thống ghi nhận: " + "; ".join(case["degraded_reasons"])]
        if case.get("ragas_errors"):
            answers += ["", "Lỗi chấm: " + json.dumps(case["ragas_errors"], ensure_ascii=False)]
        answers.append("")
    answers_path = args.output.with_name(args.output.stem + "_answers.md")
    answers_path.write_text("\n".join(answers) + "\n", encoding="utf-8")
    root = Path("/workspace")
    sources = [*sorted((root / "apps/api/app/room_service/chatbot").glob("*.py")),
               root / "apps/api/app/config.py", Path(__file__), Path(__file__).with_name("question_bank_ragas.py")]
    manifest = {"created_at_utc": datetime.now(timezone.utc).isoformat(), "git_revision_before_test_fixes": args.revision,
                "run": str(args.input), "run_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
                "corpus_audit_sha256": hashlib.sha256(args.audit.read_bytes()).hexdigest(),
                "source_sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources if p.is_file()},
                "answer_model": "gemini-3.8-flash-high", "judge": judge, "legal_schema": "public",
                "judge_min_request_interval_seconds": 0,
                "agents_enabled": False, "regression_tests_passed": 37,
                "summary": summary, "final_providers": dict(providers)}
    evidence = [{k: c.get(k) for k in ("id", "question", "answer", "sources", "contexts")} for c in cases]
    manifest["evidence_sha256"] = hashlib.sha256(json.dumps(evidence, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    manifest_path = args.input.with_name(args.output.stem + "_manifest.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    print(answers_path)
    print(manifest_path)


if __name__ == "__main__":
    main()
