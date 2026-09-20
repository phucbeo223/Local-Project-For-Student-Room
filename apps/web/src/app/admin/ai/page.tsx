import { redirect } from "next/navigation";
import { getAIDashboard } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export const dynamic = "force-dynamic";

function percent(value: number | null) {
  return value == null ? "Chưa có" : `${Math.round(value * 100)}%`;
}

export default async function AIAdminPage() {
  const token = getAccessToken();
  if (!token) redirect("/login?next=/admin/ai");
  const data = await getAIDashboard(token);
  const cards = [
    ["Yêu cầu chatbot", data.chatbot_requests],
    ["Không có câu trả lời", percent(data.no_answer_rate)],
    ["Fallback/degraded", percent(data.degraded_rate)],
    ["P95 latency", `${data.p95_latency_ms} ms`],
    ["Phản hồi tích cực", percent(data.positive_feedback_rate)],
    ["Tương tác người dùng", data.interaction_count],
  ];
  return <div><p className="text-sm font-bold uppercase tracking-[.14em] text-emerald-600">AI observability</p><h1 className="mt-1 text-3xl font-extrabold text-slate-950">Chất lượng Chatbot & Risk</h1><p className="mt-2 text-sm text-slate-500">Metric tổng hợp {data.period_days} ngày; không lưu nội dung hội thoại.</p><section className="mt-7 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{cards.map(([label, value]) => <article key={String(label)} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><p className="text-sm font-semibold text-slate-500">{label}</p><p className="mt-3 text-3xl font-black text-slate-950">{value}</p></article>)}</section><section className="mt-6 grid gap-5 md:grid-cols-2"><article className="rounded-2xl border border-slate-200 bg-white p-6"><h2 className="font-extrabold">Phân bố Risk</h2><div className="mt-4 space-y-2 text-sm"><p>Chưa đánh giá: <strong>{data.risk_not_evaluated}</strong></p><p>An toàn: <strong>{data.risk_safe}</strong></p><p>Cần chú ý: <strong>{data.risk_caution}</strong></p><p>Đáng ngờ: <strong>{data.risk_suspicious}</strong></p><p>Admin override: <strong>{data.risk_override_count}</strong></p></div></article><article className="rounded-2xl border border-slate-200 bg-white p-6"><h2 className="font-extrabold">Tín hiệu sản phẩm</h2><div className="mt-4 space-y-2 text-sm"><p>Yêu thích: <strong>{data.favorite_count}</strong></p><p>Tìm kiếm đã lưu: <strong>{data.saved_search_count}</strong></p><p>Feedback chatbot: <strong>{data.feedback_count}</strong></p><p>Confidence trung bình: <strong>{percent(data.average_confidence)}</strong></p></div></article></section><section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6"><h2 className="font-extrabold">Lần đánh giá nghiên cứu gần nhất</h2><pre className="mt-3 overflow-x-auto rounded-xl bg-slate-950 p-4 text-xs text-slate-100">{JSON.stringify(data.latest_evaluation || { status: "Chưa nạp kết quả RAGAS" }, null, 2)}</pre></section></div>;
}
