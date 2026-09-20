import { redirect } from "next/navigation";
import ListingCard from "../ListingCard";
import SiteHeader from "../SiteHeader";
import { getFavorites } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export const dynamic = "force-dynamic";

export default async function FavoritesPage() {
  const token = getAccessToken();
  if (!token) redirect("/login?next=/favorites");
  const favorites = await getFavorites(token);
  return (
    <div className="min-h-screen bg-paper">
      <SiteHeader />
      <main className="mx-auto max-w-[1160px] px-5 py-10 sm:px-10">
        <h1 className="text-3xl font-extrabold text-ink">Phòng yêu thích</h1>
        <p className="mt-2 text-sm text-ink-muted">Danh sách được dùng làm tín hiệu mạnh cho gợi ý cá nhân hóa.</p>
        {favorites.length ? (
          <div className="mt-7 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {favorites.map((item) => <ListingCard key={item.listing.id} listing={item.listing} />)}
          </div>
        ) : <p className="mt-8 rounded-2xl border border-line bg-white p-8 text-center text-ink-muted">Bạn chưa lưu phòng nào.</p>}
      </main>
    </div>
  );
}
