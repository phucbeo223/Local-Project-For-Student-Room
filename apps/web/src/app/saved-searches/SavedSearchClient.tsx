"use client";

import { FormEvent, useState } from "react";
import type { SavedSearchOut } from "@/lib/api";

export default function SavedSearchClient({ initial }: { initial: SavedSearchOut[] }) {
  const [items, setItems] = useState(initial);
  const [name, setName] = useState("");
  const [district, setDistrict] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function submit(event: FormEvent) {
    event.preventDefault();
    const response = await fetch("/api/saved-searches", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        criteria: { district: district || null, max_price: maxPrice ? Number(maxPrice) : null },
        notify_enabled: true,
      }),
    });
    const body = await response.json();
    if (!response.ok) return setError(body.detail || "Không thể lưu tìm kiếm");
    setItems((current) => [body as SavedSearchOut, ...current]);
    setName(""); setDistrict(""); setMaxPrice(""); setError(null);
  }

  async function remove(id: number) {
    const response = await fetch(`/api/saved-searches/${id}`, { method: "DELETE" });
    if (response.ok) setItems((current) => current.filter((item) => item.id !== id));
  }

  return (
    <div className="mt-7 grid gap-6 lg:grid-cols-[360px_1fr]">
      <form onSubmit={submit} className="rounded-2xl border border-line bg-white p-5 shadow-sm">
        <h2 className="font-extrabold text-ink">Tạo bộ lọc thông báo</h2>
        <input required value={name} onChange={(e) => setName(e.target.value)} placeholder="Tên bộ lọc" className="mt-4 w-full rounded-lg border border-line px-3 py-2" />
        <input value={district} onChange={(e) => setDistrict(e.target.value)} placeholder="Quận/huyện" className="mt-3 w-full rounded-lg border border-line px-3 py-2" />
        <input type="number" min="0" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} placeholder="Giá tối đa" className="mt-3 w-full rounded-lg border border-line px-3 py-2" />
        <button className="mt-4 w-full rounded-lg bg-primary px-4 py-2 font-bold text-white">Lưu tìm kiếm</button>
        {error && <p className="mt-2 text-xs text-rose-600">{error}</p>}
      </form>
      <section className="space-y-3">
        {items.map((item) => (
          <article key={item.id} className="flex items-center gap-4 rounded-2xl border border-line bg-white p-5 shadow-sm">
            <div className="min-w-0 flex-1"><h3 className="font-bold text-ink">{item.name}</h3><p className="mt-1 text-sm text-ink-muted">{item.criteria.district || "Mọi khu vực"} · tối đa {item.criteria.max_price?.toLocaleString("vi-VN") || "không giới hạn"}đ</p></div>
            <button type="button" onClick={() => void remove(item.id)} className="text-sm font-semibold text-rose-600">Xóa</button>
          </article>
        ))}
        {!items.length && <p className="rounded-2xl border border-line bg-white p-8 text-center text-ink-muted">Chưa có tìm kiếm đã lưu.</p>}
      </section>
    </div>
  );
}
