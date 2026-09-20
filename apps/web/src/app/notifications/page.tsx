import { redirect } from "next/navigation";
import SiteHeader from "../SiteHeader";
import { getNotifications } from "@/lib/api";
import { getAccessToken } from "@/lib/session";
import NotificationsClient from "./NotificationsClient";

export const dynamic = "force-dynamic";

export default async function NotificationsPage() {
  const token = getAccessToken();
  if (!token) redirect("/login?next=/notifications");
  const notifications = await getNotifications(token);
  return <div className="min-h-screen bg-paper"><SiteHeader /><main className="mx-auto max-w-[900px] px-5 py-10 sm:px-10"><h1 className="text-3xl font-extrabold text-ink">Thông báo phòng mới</h1><p className="mt-2 text-sm text-ink-muted">Đối chiếu các tin mới với những bộ lọc bạn đã lưu.</p><NotificationsClient initial={notifications} /></main></div>;
}
