"""Readable answers, source excerpts and RAGAS scores from real checkpoints."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html import escape
import json
import math
from pathlib import Path
from urllib.parse import urlparse

METRICS = ("faithfulness", "answer_relevancy", "context_utilization", "context_recall", "context_precision")
LABELS = {"housing_contract": "Hợp đồng", "electricity": "Điện", "water_cantho": "Nước",
          "residence": "Cư trú", "fire_safety": "PCCC", "student_housing": "Ký túc xá",
          "real_estate_brokerage": "Môi giới", "ecommerce_platform": "Nền tảng đăng tin",
          "privacy_data": "Dữ liệu cá nhân", "criminal_law": "Dấu hiệu lừa đảo"}


def state(case):
    if case.get("error"):
        return "Lỗi chạy"
    if "answer" not in case:
        return "Chưa chạy"
    if case.get("partial_answer"):
        return "Trả lời một phần"
    if case.get("no_answer"):
        return "Chưa đủ căn cứ"
    return "Đã trả lời · cần rà nguồn"


def score_text(value):
    return "Chưa có điểm" if value is None else str(value)


def case_score_text(case, metric):
    if metric in case.get("ragas_unavailable", {}):
        return "N/A (" + str(case["ragas_unavailable"][metric]) + ")"
    return score_text(case.get("ragas", {}).get(metric))


def link(source):
    title = escape(source.get("title") or "Nguồn")
    url = source.get("source_url") or ""
    if urlparse(url).scheme in {"http", "https"}:
        return '<a target="_blank" rel="noreferrer" href="' + escape(url, quote=True) + '">' + title + ' ↗</a>'
    return title


def render(data, output):
    output.parent.mkdir(parents=True, exist_ok=True)
    cases = data["cases"]
    summary = data.get("summary", {})
    comparison = data.get("comparison_with_20261013", {})
    generated = sum("answer" in case for case in cases)
    identity = data.get("generation_identity", {})
    judge = data.get("judge", {})
    configuration = data.get("run_configuration", {})
    now = data.get("updated_at_utc") or datetime.now(timezone.utc).isoformat()
    if identity.get("agents_enabled"):
        model_label = "Pipeline pháp lý: " + " → ".join(str(model or "—") for model in (
            configuration.get("question_analysis_model"), configuration.get("answer_model"),
            configuration.get("answer_synthesis_model")))
    else:
        model_label = "Model trả lời: " + str(identity.get("answer_model", "—"))
    selected = ", ".join(str(case["id"]) for case in cases)
    notes = [
        f"Lượt này có {len(cases)} câu từ ngân hàng {data.get('bank_size', len(cases))} câu. Các mã đã chọn: {selected}.",
        "Câu trả lời và nguồn được lấy từ hệ thống thật, không dùng đáp án sinh ra làm đáp án chuẩn.",
        f"Schema pháp lý: {identity.get('legal_schema', '—')}; schema tin trọ: {identity.get('listing_schema', '—')}. "
        f"Tác nhân {'bật' if identity.get('agents_enabled') else 'tắt'}; Graph RAG {'bật' if identity.get('graph_enabled') else 'tắt'}.",
        "Đo trực tiếp tầng service với database thật; tắt ghi sự kiện tổng hợp trong lượt đánh giá. Độ trễ không bao gồm trình duyệt và HTTP.",
        "Nhánh tra cứu danh mục KTX có thể trả lời bằng dữ liệu có cấu trúc; provider thực tế được ghi ở từng câu.",
        "Faithfulness đo mức câu trả lời được các đoạn truy xuất hỗ trợ; Answer Relevancy đo liên quan câu hỏi; Context Utilization đo mức ngữ cảnh hữu dụng cho phản hồi.",
        "Context Recall và Context Precision ở lượt này là RAGAS IDBasedContextRecall/IDBasedContextPrecision: so khớp tập tài liệu/nguồn được truy xuất với ID nguồn liên quan gán theo từng câu. Đây là độ bao phủ ở cấp tài liệu, không phải tỷ lệ bao phủ từng mệnh đề trong đáp án.",
        "Các ID nguồn chuẩn được gán từ corpus và tài liệu KTX được nêu trong câu hỏi, không lấy từ câu trả lời của chatbot. Nhãn hiện do một lượt rà soát tạo; cần rà soát độc lập trước khi dùng như chuẩn vàng đã xác nhận.",
        "Chưa có đáp án chuẩn dạng nội dung do chuyên gia xác nhận: không báo Answer Correctness hay LLM Context Recall. Điểm ID-based không xác nhận độ đúng pháp lý.",
        "Nếu không truy xuất nguồn, IDBasedContextRecall là 0 khi bộ nguồn chuẩn không rỗng; IDBasedContextPrecision là N/A vì không có nguồn được xếp hạng. Faithfulness và Context Utilization là N/A; Answer Relevancy vẫn có thể được chấm.",
        "Điểm RAGAS không chứng minh luật còn hiệu lực hoặc câu trả lời đúng pháp lý. Câu lỗi/chưa chấm không được gán điểm 0.",
        "Nếu model sinh và chấm cùng họ Gemini thì có thể có thiên lệch. Tên model được ghi theo cấu hình endpoint; alias proxy chưa xác minh mô hình nền.",
        "Phí, kỳ tính giá, GPS và chỗ trống KTX cần đọc cùng giới hạn nguồn được nêu trong từng phản hồi.",
    ]
    if comparison:
        comparison_metrics = comparison.get("faithfulness", {})
        notes.append(
            f"Faithfulness so với lượt 13/10: {comparison_metrics.get('baseline')} → "
            f"{comparison_metrics.get('current')} trên cùng 48 mã câu. Đây là so sánh chỉ báo, "
            "không hoàn toàn đồng điều kiện vì lượt mới siết hướng dẫn tổng hợp và đưa metadata phạm vi nguồn vào ngữ cảnh judge."
        )
    markdown = ["# Câu trả lời, nguồn và điểm RAGAS · Pháp lý & KTX", "",
                f"Cập nhật báo cáo: {now}. Đã lưu {generated}/{len(cases)} câu trả lời.", "",
                f"{model_label}; model chấm: {judge.get('model', 'chưa chấm')}; RAGAS {judge.get('version', 'chưa chấm')}.", "",
                "## Phạm vi và cách đọc", "", *["- " + note for note in notes], "",
                "## Điểm tổng hợp", "", "| Chỉ số | Trung bình | Số điểm hợp lệ |", "|---|---:|---:|"]
    for metric in METRICS:
        metric_summary = summary.get("ragas", {}).get(metric, {})
        markdown.append(f"| {metric} | {score_text(metric_summary.get('mean'))} | {metric_summary.get('scored', 0)}/{len(cases)} |")
    ktx_ids = set(range(39, 43)) | set(range(59, 67))
    groups = {
        "Pháp lý": [case for case in cases if int(case["id"]) not in ktx_ids],
        "KTX": [case for case in cases if int(case["id"]) in ktx_ids],
    }
    markdown.extend(["", "## Điểm theo nhóm câu hỏi", "", "| Nhóm | Chỉ số | Trung bình | Số điểm hợp lệ |", "|---|---|---:|---:|"])
    group_rows = []
    for group_name, group_cases in groups.items():
        for metric in METRICS:
            values = [float(case["ragas"][metric]) for case in group_cases
                      if isinstance(case.get("ragas", {}).get(metric), (int, float))
                      and math.isfinite(case["ragas"][metric])]
            mean = round(sum(values) / len(values), 4) if values else None
            markdown.append(f"| {group_name} | {metric} | {score_text(mean)} | {len(values)}/{len(group_cases)} |")
            group_rows.append((group_name, metric, mean, len(values), len(group_cases)))
    if comparison:
        comparison_metrics = comparison.get("faithfulness", {})
        markdown.extend(["", "## So sánh Faithfulness với lượt 13/10", "",
                         "| Lượt | Điểm | Số câu có điểm |", "|---|---:|---:|",
                         f"| 13/10/2026 | {score_text(comparison_metrics.get('baseline'))} | {comparison_metrics.get('baseline_scored', 0)}/48 |",
                         f"| 14/10/2026 | {score_text(comparison_metrics.get('current'))} | {comparison_metrics.get('current_scored', 0)}/48 |",
                         "", comparison.get("comparability_note", ""), ""])
    cards = []
    for case in cases:
        status = state(case)
        scores = case.get("ragas", {})
        warnings = []
        if case.get("degraded"):
            warnings.append("Hệ thống ghi nhận chế độ hạn chế")
        if case.get("ragas_errors"):
            warnings.append("Có lỗi chấm RAGAS")
        if case.get("ragas_unavailable"):
            warnings.append("Có chỉ số N/A do không có ngữ cảnh nguồn")
        if any(isinstance(scores.get(metric), (int, float)) and scores[metric] < .7 for metric in METRICS):
            warnings.append("Có điểm dưới 0,7: ưu tiên đọc lại")
        if case.get("partial_answer") or case.get("no_answer") or case.get("error"):
            warnings.append(status)
        group = LABELS.get(case["category"], case["category"])
        answer = case.get("answer", case.get("error", "Chưa có câu trả lời trong checkpoint."))
        markdown.extend(["", f"## Câu {case['id']} · {group}", "", case["question"], "",
                         f"Trạng thái: {status}. Provider: {case.get('generation_provider', '—')}; model: {case.get('generation_model') or '—'}.", "",
                         " | ".join(metric + ": " + case_score_text(case, metric) for metric in METRICS), "",
                         "ID nguồn chuẩn: " + ", ".join(case.get("reference_context_ids", [])), "",
                         "ID nguồn đã truy xuất: " + ", ".join(case.get("retrieved_context_ids", [])), "",
                         answer, "", "### Nguồn và ngữ cảnh", ""])
        source_html = []
        for index, source in enumerate(case.get("sources", [])):
            title = source.get("title", "Nguồn")
            url = source.get("source_url")
            heading = source.get("heading") or ""
            pages = str(source.get("page_from") or "")
            if source.get("page_to") and source.get("page_to") != source.get("page_from"):
                pages += "–" + str(source["page_to"])
            page_label = "Trang bản trích" if source.get("page_kind") == "logical_document" else "Trang PDF" if source.get("page_kind") == "physical_pdf" else "Trang"
            context = case.get("contexts", [])[index] if index < len(case.get("contexts", [])) else source.get("excerpt", "")
            markdown.extend([f"**[{source.get('rank')}] " + (f"[{title}]({url})" if url else title) + "**", "",
                             heading + (" · " + page_label + " " + pages if pages else ""), "",
                             "Đường dẫn nguồn: " + (source.get("source_path") or "Danh mục KTX dùng chung"), "",
                             "```text", context or "Không có trích đoạn", "```", ""])
            source_html.append('<details class="source"><summary>[' + str(source.get("rank")) + '] ' + link(source)
                               + '</summary><p>' + escape(heading) + (" · " + page_label + " " + pages if pages else "")
                               + '</p><pre>' + escape(context or "Không có trích đoạn") + '</pre></details>')
        errors = {"collect": case.get("error"), "ragas": case.get("ragas_errors"),
                  "unavailable": case.get("ragas_unavailable"), "degraded": case.get("degraded_reasons")}
        if any(errors.values()):
            markdown.extend(["### Lỗi và giới hạn đã ghi nhận", "", "```json", json.dumps(errors, ensure_ascii=False, indent=2), "```", ""])
        details = '<details class="errors"><summary>Lỗi/giới hạn đã ghi nhận</summary><pre>' + escape(json.dumps(errors, ensure_ascii=False, indent=2)) + '</pre></details>' if any(errors.values()) else ''
        score_html = ''.join('<span><b>' + metric + '</b> ' + case_score_text(case, metric) + '</span>' for metric in METRICS)
        gold_ids = '<details class="source"><summary>ID nguồn chuẩn và đã truy xuất</summary><pre>Chuẩn: ' + escape(', '.join(case.get("reference_context_ids", [])) + '\nĐã truy xuất: ' + ', '.join(case.get("retrieved_context_ids", []))) + '</pre></details>'
        cards.append('<article class="case" data-group="' + escape(case["category"]) + '" data-review="' + str(bool(warnings)).lower() + '">'
                     + '<p class="eyebrow">Câu ' + str(case["id"]) + ' · ' + escape(group) + '</p><h2>' + escape(case["question"])
                     + '</h2><p class="status">' + escape(status) + ' · ' + escape(case.get("generation_provider") or '—') + '</p>'
                     + '<div class="scores">' + score_html + '</div>'
                     + ('<p class="warning">' + escape(' · '.join(warnings)) + '</p>' if warnings else '')
                     + '<h3>Câu trả lời đã lưu</h3><pre class="answer">' + escape(answer) + '</pre><h3>Nguồn · bấm để mở trích đoạn</h3>'
                     + ''.join(source_html) + gold_ids + details + '</article>')
    markdown.append("\nBáo cáo JSON gốc lưu toàn bộ provider calls, quyết định chấm, lỗi, hash dữ liệu và cấu hình không chứa khóa API.\n")
    output.with_suffix(".md").write_text("\n".join(markdown), encoding="utf-8")
    options = '<option value="">Tất cả chủ đề</option>' + ''.join('<option value="' + key + '">' + label + '</option>' for key, label in LABELS.items())
    html = '''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RAGAS · Pháp lý & KTX CTU</title>
<style>*{box-sizing:border-box}body{margin:0;background:#f2f6fa;color:#16314a;font:15px/1.65 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:28px 20px 60px}header{background:#06305c;color:white;padding:30px;border-radius:22px}h1{font-size:30px;margin:0}h2{font-size:20px;line-height:1.5}h3{font-size:14px}a{color:#0766ad}header a{color:#cfeeff}.toolbar{position:sticky;top:0;z-index:2;display:flex;gap:12px;flex-wrap:wrap;background:#f2f6faf5;padding:18px 0}input,select{font:inherit;min-height:44px;border:1px solid #c5d5e3;border-radius:10px;padding:8px 12px;background:white}input{flex:1;min-width:200px}.case{background:white;border:1px solid #dbe5ef;border-radius:18px;padding:24px;margin:18px 0}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:#087684;font-weight:700}.scores{display:flex;gap:10px;flex-wrap:wrap}.scores span{padding:6px 10px;background:#eaf3fc;border-radius:8px;font-size:12px}.status{font-size:13px;color:#62788d}.warning{background:#fff1cf;color:#684606;padding:8px 12px;border-radius:8px}pre{font:14px/1.75 system-ui,sans-serif;white-space:pre-wrap;overflow-wrap:anywhere;margin:10px 0}.answer{border-left:3px solid #2186c4;padding-left:16px}.source,.errors{border:1px solid #dbe5ef;border-radius:10px;padding:12px;margin:10px 0}.source pre{background:#f7fafc;padding:14px}.source p{font-size:12px;color:#63788d}summary{cursor:pointer}.note{font-size:13px;color:#546b80}.notes{background:white;border-radius:14px;padding:18px;margin-top:18px}label{display:flex;align-items:center;gap:6px}label input{min-height:0;min-width:0;flex:0}small{color:#cee7ff}@media(max-width:600px){main{padding:16px 12px}header{padding:22px}h1{font-size:24px}.case{padding:18px}}@media print{.toolbar{display:none}body{background:white}.case{break-inside:avoid}details>*{display:block!important}}</style><main>'''
    html += '<header><h1>Pháp lý & KTX CTU · RAGAS</h1><p>' + str(generated) + '/' + str(len(cases)) + ' câu đã có phản hồi · Ngân hàng ' + str(data.get("bank_size", 66)) + ' câu</p><small>' + escape(model_label) + ' · Judge: ' + escape(str(judge.get("model", "chưa chấm"))) + ' · Cập nhật UTC: ' + now + '</small></header>'
    html += '<section class="notes"><h2>Điểm RAGAS trung bình</h2><div class="scores">' + ''.join(
        '<span><b>' + label + '</b> ' + score_text(summary.get("ragas", {}).get(metric, {}).get("mean"))
        + ' · ' + str(summary.get("ragas", {}).get(metric, {}).get("scored", 0)) + '/' + str(len(cases)) + ' câu</span>'
        for metric, label in zip(METRICS, ("Bám nguồn", "Liên quan câu hỏi", "Hữu dụng ngữ cảnh", "Recall nguồn chuẩn", "Precision nguồn chuẩn"))) + '</div></section>'
    html += '<section class="notes"><h2>Điểm theo nhóm câu hỏi</h2><table><thead><tr><th>Nhóm</th><th>Chỉ số</th><th>Trung bình</th><th>Số điểm hợp lệ</th></tr></thead><tbody>' + ''.join(
        '<tr><td>' + escape(group_name) + '</td><td>' + escape(metric) + '</td><td>' + score_text(mean) + '</td><td>' + str(scored) + '/' + str(total) + '</td></tr>'
        for group_name, metric, mean, scored, total in group_rows) + '</tbody></table></section>'
    if comparison:
        comparison_metrics = comparison.get("faithfulness", {})
        html += '<section class="notes"><h2>So sánh Faithfulness với lượt 13/10</h2><table><thead><tr><th>Lượt</th><th>Điểm</th><th>Số câu có điểm</th></tr></thead><tbody>'
        html += '<tr><td>13/10/2026</td><td>' + score_text(comparison_metrics.get("baseline")) + '</td><td>' + str(comparison_metrics.get("baseline_scored", 0)) + '/48</td></tr>'
        html += '<tr><td>14/10/2026</td><td>' + score_text(comparison_metrics.get("current")) + '</td><td>' + str(comparison_metrics.get("current_scored", 0)) + '/48</td></tr>'
        html += '</tbody></table><p class="note">' + escape(comparison.get("comparability_note", "")) + '</p></section>'
    html += '<details class="notes"><summary>Phạm vi, cách đọc và giới hạn đánh giá</summary><ul>' + ''.join('<li>' + escape(note) + '</li>' for note in notes) + '</ul></details>'
    html += '<div class="toolbar"><input id="search" aria-label="Tìm câu hỏi, câu trả lời hoặc nguồn" placeholder="Tìm câu hỏi, câu trả lời, nguồn…"><select id="group" aria-label="Chủ đề">' + options + '</select><label><input id="review" type="checkbox">Ưu tiên xem lại</label><span id="count"></span></div>'
    html += ''.join(cards) + '''<script>const norm=v=>v.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d');const cards=[...document.querySelectorAll('.case')];function filter(){const q=norm(document.getElementById('search').value),group=document.getElementById('group').value,review=document.getElementById('review').checked;let n=0;for(const card of cards){const show=(!q||norm(card.textContent).includes(q))&&(!group||card.dataset.group===group)&&(!review||card.dataset.review==='true');card.hidden=!show;if(show)n++;}document.getElementById('count').textContent=n+' câu';}['search','group','review'].forEach(id=>document.getElementById(id).addEventListener('input',filter));filter();</script></main></html>'''
    output.with_suffix(".html").write_text(html, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    render(json.loads(args.input.read_text(encoding="utf-8")), args.output)
    print(str(args.output.with_suffix(".html")))


if __name__ == "__main__":
    main()
