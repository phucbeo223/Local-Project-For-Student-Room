import Link from "next/link";
import { redirect } from "next/navigation";
import ListingCard from "../ListingCard";
import SiteHeader from "../SiteHeader";
import { getRecommendations } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export const dynamic = "force-dynamic";

export default async function RecommendationsPage() {
  const token = getAccessToken();
  if (!token) redirect("/login?next=/recommendations");
  const result = await getRecommendations(token);
  return (
    <div className="min-h-screen bg-paper">
      <SiteHeader />
      <main className="mx-auto max-w-[1160px] px-5 py-10 sm:px-10">
        <h1 className="text-3xl font-extrabold text-ink">Dành cho bạn</h1>
        <p className="mt-2 text-sm text-ink-muted">
          {result.cold_start
            ? "Đang dùng tin mới và chất lượng tốt. Hãy xem hoặc lưu vài phòng để cá nhân hóa."
            : `Xếp hạng từ ${result.profile_evidence} tín hiệu tương tác gần đây.`}
        </p>
        {result.items.length ? (
          <div className="mt-7 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {result.items.map((item) => (
              <div key={item.listing.id}>
                <ListingCard listing={item.listing} />
                <div className="mt-2 rounded-xl bg-blue-50 px-3 py-2 text-xs text-blue-800">
                  <strong>{Math.round(item.score * 100)}% phù hợp</strong> · {item.reasons.join(" · ")}
                </div>
              </div>
            ))}
          </div>
        ) : <div className="mt-8 rounded-2xl border border-line bg-white p-8 text-center"><p>Chưa có tin phù hợp.</p><Link className="mt-3 inline-block font-bold text-primary" href="/">Tìm phòng ngay</Link></div>}
      </main>
    </div>
  );
}
