"""Compare preserved Gemini and Gemini/Qwen runs on the same question bank."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import random
import statistics

METRICS = ("faithfulness", "answer_relevancy", "context_utilization")
METHOD_FIELDS = ("library", "version", "model", "provider", "endpoint", "embedding_model",
                 "answer_relevancy_strictness", "context_limit", "context_char_limit", "score_abstentions",
                 "max_output_tokens", "temperature", "context_policy", "score_workers", "judge_request_timeout_seconds")
CORPUS_FIELDS = ("data_files", "indexed_documents", "missing_from_index", "indexed_but_missing_from_data",
                 "current_document_chunks", "current_document_vectors")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid(value):
    return isinstance(value, (int, float)) and math.isfinite(value)


def state(case):
    if case.get("error"):
        return "lỗi"
    if case.get("partial_answer"):
        return "một phần"
    return "chưa đủ căn cứ" if case.get("no_answer") else "đủ theo hệ thống"


def cell(value):
    return f"{value:.4f}" if valid(value) else "N/A"


def paired_interval(values):
    if not values:
        return None
    rng = random.Random(20261004)
    samples = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(5000))
    return [round(samples[124], 4), round(samples[4874], 4)]


def main():
    parser = argparse.ArgumentParser()
    for name in ("gemini", "hybrid", "baseline-manifest", "audit-baseline", "audit-before", "audit-after", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--recommendation", type=Path)
    args = parser.parse_args()
    first, second = read(args.gemini), read(args.hybrid)
    baseline_manifest = read(args.baseline_manifest)
    if digest(args.gemini) != baseline_manifest["run_sha256"]:
        raise ValueError("Preserved Gemini baseline changed")
    if first["question_bank_sha256"] != second["question_bank_sha256"]:
        raise ValueError("Different question banks")
    left = {c["id"]: c for c in first["cases"]}
    right = {c["id"]: c for c in second["cases"]}
    if set(left) != set(right) or len(left) != 36:
        raise ValueError("Expected 36 matching cases")
    pairs = [(left[i], right[i]) for i in sorted(left)]
    if any(a["question"] != b["question"] for a, b in pairs):
        raise ValueError("Question text changed")
    common_judge = all(first.get("judge", {}).get(k) == second.get("judge", {}).get(k) for k in METHOD_FIELDS)
    if not common_judge:
        raise ValueError("Judging methods differ; cannot compare aggregate scores")
    audits = [read(p) for p in (args.audit_baseline, args.audit_before, args.audit_after)]
    same_corpus_inventory = all(all(a.get(k) == audits[0].get(k) for k in CORPUS_FIELDS) for a in audits[1:])
    pipeline_checks = {p: digest(Path(p)) == sha for p, sha in baseline_manifest["source_sha256"].items()
                       if p.startswith("/workspace/apps/api/app/") and Path(p).exists()}
    same_pipeline_files = bool(pipeline_checks) and all(pipeline_checks.values())
    summary_a, summary_b = first["summary"], second["summary"]
    stages = [step for c in second["cases"] for step in c.get("agent_trace", [])]
    analysis_success = sum(s.get("agent") == "question_analysis" and s.get("provider") == "gemini"
                           and s.get("status") == "completed" for s in stages)
    analysis_fallback = sum(s.get("agent") == "question_analysis" and s.get("status") == "fallback" for s in stages)
    exact_checks = sum(s.get("agent") == "source_verification" and s.get("provider") == "exact_source_match"
                       and s.get("status") == "accepted" for s in stages)
    model_checks = sum(s.get("agent") == "source_verification" and s.get("provider") == "gemini" for s in stages)
    qwen_calls = [p for c in second["cases"] for p in c.get("provider_calls", [])
                  if p.get("provider") == "qwen-local" and p.get("method") == "generate"]
    metrics = {}
    lines = ["# So sánh Gemini và Gemini + Qwen trên 36 câu", "",
             "## Thiết lập so sánh", "",
             "- Phương án A: định tuyến bằng quy tắc, truy xuất nguồn; Gemini 3.8 Flash High tổng hợp và kiểm tra nguồn, "
             "có đáp án trích xuất trực tiếp hoặc dự phòng theo quy tắc.",
             "- Phương án B: Gemini 3.8 Flash High phân tích câu hỏi, truy xuất theo kế hoạch; "
             "Qwen 3.5 9B chọn ID đoạn nguồn ở chế độ `source_select`, hệ thống ghép trích nguyên văn. "
             "Đoạn nguyên văn được kiểm tra exact-source; bước Gemini kiểm tra ý nghĩa được bỏ qua trong nhánh này.",
             "- Cả hai dùng kho `public`, bộ 36 câu và E5 hiện hành. API chính không được đổi sang B khi chạy test.",
             f"- Bộ chấm chung: Ragas {first['judge']['version']}, {first['judge']['provider']}/{first['judge']['model']}; "
             "4 worker, 8.192 token đầu ra, chấm cả phản hồi một phần có nguồn; cùng endpoint proxy và toàn bộ ngữ cảnh.",
             f"- SHA bộ câu hỏi: `{first['question_bank_sha256']}`.",
             f"- Baseline Gemini giữ nguyên SHA: `{digest(args.gemini)}`.",
             f"- Cùng các tệp pipeline: {same_pipeline_files}; cùng kiểm kê corpus trước/sau và baseline: {same_corpus_inventory}.",
             "- Các thống kê kiểm kê không phải fingerprint đầy đủ của DB ở thời điểm lượt A; không sửa/nạp corpus trong hai lượt.",
             "", "## Kết quả vận hành", "", "| Chỉ số | A: Gemini | B: Gemini + Qwen |", "|---|---:|---:|"]
    for label, key in (("Hoàn thành", "completed"), ("Lỗi thực thi", "errors"), ("Có ngữ cảnh", "with_contexts"),
                       ("Trả lời một phần", "partial_answer"), ("Chưa đủ căn cứ (gồm một phần)", "no_answer"),
                       ("Suy giảm", "degraded"), ("Định dạng trích dẫn trung bình", "citation_format_accuracy_mean")):
        lines.append(f"| {label} | {summary_a[key]} | {summary_b[key]} |")
    lines.append(f"| Đủ theo kiểm tra hệ thống | {summary_a['completed'] - summary_a['no_answer']} | {summary_b['completed'] - summary_b['no_answer']} |")
    for label, key in (("Độ trễ p50 (giây)", "latency_p50_ms"), ("Độ trễ p95 (giây)", "latency_p95_ms")):
        lines.append(f"| {label} | {summary_a[key]/1000:.2f} | {summary_b[key]/1000:.2f} |")
    lengths = [statistics.median(len(c.get("answer", "")) for c in run["cases"] if "answer" in c)
               for run in (first, second)]
    lines.append(f"| Độ dài phản hồi trung vị (ký tự) | {lengths[0]:.0f} | {lengths[1]:.0f} |")
    lines += ["", "## Ragas cùng phương pháp", "", "| Chỉ số | A: Gemini (n) | B: Kết hợp (n) | Δ B−A trên các cặp | Khoảng bootstrap 95% | B cao / bằng / thấp |", "|---|---:|---:|---:|---|---|"]
    for name in METRICS:
        selected = [(a["ragas"][name], b["ragas"][name]) for a, b in pairs
                    if valid(a.get("ragas", {}).get(name)) and valid(b.get("ragas", {}).get(name))]
        differences = [b-a for a, b in selected]
        interval = paired_interval(differences)
        metrics[name] = {"paired_cases": len(selected), "mean_a": statistics.mean(a for a, _ in selected) if selected else None,
                         "mean_b": statistics.mean(b for _, b in selected) if selected else None,
                         "mean_delta": statistics.mean(differences) if differences else None,
                         "bootstrap_95": interval, "wins_b": sum(d > 1e-8 for d in differences),
                         "ties": sum(abs(d) <= 1e-8 for d in differences), "losses_b": sum(d < -1e-8 for d in differences)}
        m = metrics[name]
        lines.append(f"| {name} | {cell(m['mean_a'])} ({len(selected)}) | {cell(m['mean_b'])} ({len(selected)}) | "
                     f"{cell(m['mean_delta'])} | {interval} | {m['wins_b']} / {m['ties']} / {m['losses_b']} |")
    lines += ["", "Bootstrap chỉ thể hiện biến thiên giữa 36 câu đã chọn (5.000 mẫu, seed 20261004); "
              "không đo nhiễu của bộ chấm qua nhiều lần chạy. Điểm Ragas không phải tỷ lệ đúng luật. "
              "Cùng proxy cung cấp model sinh/chấm; tên alias chưa xác minh model nền. Qwen trích nguyên văn có thể tăng "
              "Faithfulness nhưng vẫn chọn sai phạm vi hoặc thiếu cách áp dụng.", "",
              "## Xác nhận vai trò và nguồn lực", "",
              f"- Gemini phân tích thành công {analysis_success}/36; fallback phân tích: {analysis_fallback}.",
              f"- Lượt gọi Qwen generate: {len(qwen_calls)}; thành công: {sum(p.get('success') is True for p in qwen_calls)}.",
              f"- Kiểm tra trích nguyên văn được chấp nhận: {exact_checks}; lượt Gemini kiểm tra ý nghĩa trong trace: {model_checks}.",
              f"- Provider cuối A: {dict(Counter(c.get('generation_provider') for c in first['cases']))}.",
              f"- Provider cuối B: {dict(Counter(c.get('generation_provider') for c in second['cases']))}.",
              "- Không có bảng giá thực của proxy; không suy ra chi phí tiền. B dùng thêm tài nguyên Ollama trên máy và vẫn gọi Gemini để phân tích/chấm.",
              f"- Corpus có {audits[0]['indexed_documents']} tài liệu, {audits[0]['current_document_vectors']} vector; "
              f"{len(audits[0]['missing_from_index'])} tệp mới chưa nạp ở cả hai phương án.",
              "", "## Từng câu", "", "| Câu | Chủ đề | Trạng thái A → B | Độ trễ A / B (s) | F A / B | AR A / B | CU A / B |", "|---|---|---|---|---|---|---|"]
    for a, b in pairs:
        scores = [f"{cell(a.get('ragas', {}).get(m))} / {cell(b.get('ragas', {}).get(m))}" for m in METRICS]
        lines.append(f"| {a['id']} | {a['category']} | {state(a)} → {state(b)} | "
                     f"{a.get('latency_ms', 0)/1000:.2f} / {b.get('latency_ms', 0)/1000:.2f} | {' | '.join(scores)} |")
    gained = [b["id"] for a, b in pairs if a.get("no_answer") and not b.get("no_answer") and not b.get("error")]
    lost = [b["id"] for a, b in pairs if not a.get("no_answer") and b.get("no_answer")]
    lines += ["", f"B chuyển từ chưa đủ sang đủ theo hệ thống: {gained}.", f"B chuyển từ đủ sang chưa đủ: {lost}.", ""]
    errors = {label: [(c["id"], list(c.get("ragas_errors", {}))) for c in report["cases"] if c.get("ragas_errors")]
              for label, report in (("A", first), ("B", second))}
    lines += [f"Metric còn lỗi: {errors}.", ""]
    observed_f = [c.get("ragas", {}).get("faithfulness") for c in second["cases"]]
    observed_f = [v for v in observed_f if valid(v)]
    missing_f = len(second["cases"]) - len(observed_f)
    faithfulness_bounds = [(sum(observed_f) + missing_f * value) / len(second["cases"]) for value in (0, 1)]
    if missing_f:
        lines += [f"Faithfulness của B còn thiếu {missing_f} điểm. Nếu các điểm này nhận bất kỳ giá trị nào trong [0,1], "
                  f"trung bình toàn bộ 36 câu sẽ nằm trong [{faithfulness_bounds[0]:.4f}, {faithfulness_bounds[1]:.4f}]. "
                  f"Đây là biên toán học, không phải điểm được chấm; các điểm lỗi vẫn giữ N/A. "
                  f"Trung bình A trên 36 câu là {summary_a['ragas']['faithfulness']['mean']}.", ""]
    if args.recommendation:
        lines += ["## Khuyến nghị chọn phương án", "", args.recommendation.read_text(encoding="utf-8"), ""]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    details = ["# Toàn bộ phản hồi của hai phương án", "", "Phản hồi đã lưu, chưa được kiểm định pháp lý độc lập.", ""]
    for a, b in pairs:
        details += [f"## Câu {a['id']}: {a['question']}", ""]
        for label, case in (("A — Gemini", a), ("B — Gemini + Qwen", b)):
            details += [f"### {label}", "", f"Trạng thái: {state(case)}; độ trễ {case.get('latency_ms', 0)/1000:.2f} giây.", "",
                        case.get("answer", case.get("error", "Chưa có phản hồi")), "", "Nguồn:", ""]
            details += [f"- [{s.get('rank')}] {s.get('title')}; `{s.get('source_path')}`; {s.get('heading') or ''}"
                        for s in case.get("sources", [])]
            details += ["", "Lý do: " + "; ".join(case.get("degraded_reasons", [])), ""]
    details_path = args.output.with_name(args.output.stem + "_answers.md")
    details_path.write_text("\n".join(details) + "\n", encoding="utf-8")
    manifest = {"baseline_sha256": digest(args.gemini), "hybrid_sha256": digest(args.hybrid),
                "same_question_bank": True, "same_judge_method": common_judge, "same_pipeline_files": same_pipeline_files,
                "pipeline_checks": pipeline_checks, "same_corpus_inventory": same_corpus_inventory,
                "baseline_summary": summary_a, "hybrid_summary": summary_b, "paired_metrics": metrics,
                "analysis_success": analysis_success, "analysis_fallback": analysis_fallback,
                "qwen_generate_calls": len(qwen_calls), "exact_source_checks": exact_checks,
                "hybrid_faithfulness_missing": missing_f, "hybrid_faithfulness_all_case_bounds": faithfulness_bounds,
                "metric_errors": errors, "gained_completion_ids": gained, "lost_completion_ids": lost}
    args.output.with_suffix(".json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(args.output)
    print(details_path)


if __name__ == "__main__":
    main()
