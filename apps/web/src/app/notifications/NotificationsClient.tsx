"use client";

import Link from "next/link";
import { useState } from "react";
import type { NotificationOut } from "@/lib/api";

export default function NotificationsClient({ initial }: { initial: NotificationOut[] }) {
  const [items, setItems] = useState(initial);
  const [message, setMessage] = useState<string | null>(null);
  async function refresh() {
    const response = await fetch("/api/notifications", { method: "POST" });
    const body = await response.json();
    if (response.ok) { setItems(body.items); setMessage(`Tìm thấy ${body.created} thông báo mới.`); }
    else setMessage(body.detail || "Không thể kiểm tra thông báo");
  }
  async function markRead(id: number) {
    const response = await fetch(`/api/notifications/${id}`, { method: "PATCH" });
    if (response.ok) {
      const updated = await response.json() as NotificationOut;
      setItems((current) => current.map((item) => item.id === id ? updated : item));
    }
  }
  return <div className="mt-7"><button onClick={() => void refresh()} className="rounded-xl bg-primary px-4 py-2.5 font-bold text-white">Kiểm tra phòng mới</button>{message && <p className="mt-2 text-sm text-ink-muted">{message}</p>}<div className="mt-5 space-y-3">{items.map((item) => <article key={item.id} className={`rounded-2xl border p-5 shadow-sm ${item.read_at ? "border-line bg-white" : "border-blue-200 bg-blue-50"}`}><p className="font-semibold text-ink">{item.message}</p><div className="mt-2 flex flex-wrap items-center justify-between gap-3"><time className="text-xs text-ink-muted">{new Date(item.created_at).toLocaleString("vi-VN")}</time><div className="flex items-center gap-3">{!item.read_at && <button onClick={() => void markRead(item.id)} className="text-sm font-semibold text-slate-600">Đánh dấu đã đọc</button>}{item.listing_id && <Link href={`/listings/${item.listing_id}`} className="text-sm font-bold text-primary">Xem phòng →</Link>}</div></div></article>)}{!items.length && <p className="rounded-2xl border border-line bg-white p-8 text-center text-ink-muted">Chưa có thông báo.</p>}</div></div>;
}
