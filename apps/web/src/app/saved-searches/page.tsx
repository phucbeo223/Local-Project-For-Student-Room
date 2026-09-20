import { redirect } from "next/navigation";
import SiteHeader from "../SiteHeader";
import { getSavedSearches } from "@/lib/api";
import { getAccessToken } from "@/lib/session";
import SavedSearchClient from "./SavedSearchClient";

export const dynamic = "force-dynamic";

export default async function SavedSearchesPage() {
  const token = getAccessToken();
  if (!token) redirect("/login?next=/saved-searches");
  const searches = await getSavedSearches(token);
  return <div className="min-h-screen bg-paper"><SiteHeader /><main className="mx-auto max-w-[1160px] px-5 py-10 sm:px-10"><h1 className="text-3xl font-extrabold text-ink">Tìm kiếm đã lưu</h1><p className="mt-2 text-sm text-ink-muted">Lưu nhu cầu để dùng lại và làm nền cho thông báo phòng mới.</p><SavedSearchClient initial={searches} /></main></div>;
}
