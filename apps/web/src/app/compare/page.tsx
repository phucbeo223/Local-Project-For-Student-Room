"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import SiteHeader from "../SiteHeader";
import type { ListingOut } from "@/lib/api";
import { readCompared } from "@/lib/compare";
import { AMENITY_LABELS } from "@/lib/amenities";
import {
  formatArea,
  formatDistance,
  formatPrice,
  riskBadge,
} from "@/lib/format";

export default function ComparePage() {
  const [items, setItems] = useState<ListingOut[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const ids = readCompared();
    void Promise.all(
      ids.map(async (id) => {
        const response = await fetch(`/api/listings/${id}`);
        return response.ok ? (response.json() as Promise<ListingOut>) : null;
      }),
    )
      .then((values) =>
        setItems(values.filter((value): value is ListingOut => value !== null)),
      )
      .catch(() =>
        setError("Không tải được bảng so sánh. Vui lòng tải lại trang."),
      )
      .finally(() => setLoading(false));
  }, []);

  function remove(id: number) {
    const next = items.filter((item) => item.id !== id);
    setItems(next);
    try {
      localStorage.setItem(
        "compare-listings",
        JSON.stringify(next.map((item) => item.id)),
      );
    } catch {
      setError("Không lưu được thay đổi vào trình duyệt.");
    }
  }

  return (
    <div className="min-h-screen bg-paper">
      <SiteHeader />
      <main className="mx-auto max-w-[1160px] px-5 py-10 sm:px-10">
        <h1 className="text-3xl font-extrabold text-ink">So sánh phòng</h1>
        <p className="mt-2 text-sm text-ink-muted">
          So sánh tối đa 3 phòng theo giá, vị trí, chất lượng và rủi ro.
        </p>
        {error && (
          <p role="alert" className="mt-4 text-red-700">
            {error}
          </p>
        )}
        {loading && <p role="status">Đang tải...</p>}
        {!loading && items.length === 1 && (
          <p className="mt-3">Thêm ít nhất một phòng nữa để so sánh.</p>
        )}
        {!items.length ? (
          <p className="mt-8 rounded-2xl border border-line bg-white p-8 text-center">
            Chưa có phòng để so sánh.{" "}
            <Link href="/" className="font-bold text-primary">
              Về trang tìm trọ
            </Link>
          </p>
        ) : (
          <div className="mt-7 overflow-x-auto rounded-2xl border border-line bg-white shadow-sm">
            <table className="min-w-full text-left text-sm">
              <thead className="bg-slate-50">
                <tr>
                  <th className="p-4">Phòng</th>
                  <th className="p-4">Giá</th>
                  <th className="p-4">Diện tích</th>
                  <th className="p-4">Khoảng cách</th>
                  <th className="p-4">Tiện ích</th>
                  <th className="p-4">Risk</th>
                  <th className="p-4"></th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => {
                  const badge = riskBadge(item.risk_level);
                  return (
                    <tr key={item.id} className="border-t border-line">
                      <td className="p-4">
                        <Link
                          href={`/listings/${item.id}`}
                          className="font-bold text-primary"
                        >
                          {item.title}
                        </Link>
                        <p className="mt-1 text-xs text-ink-muted">
                          {item.address || item.district}
                        </p>
                      </td>
                      <td className="p-4 font-semibold">
                        {formatPrice(item.price)}
                      </td>
                      <td className="p-4">{formatArea(item.area)}</td>
                      <td className="p-4">
                        {formatDistance(item.distance_to_ctu)}
                      </td>
                      <td className="p-4">
                        {Object.entries(item.parsed_amenities || {})
                          .filter(([, v]) => v)
                          .map(([key]) => AMENITY_LABELS[key] || key)
                          .join(", ") || "Chưa có dữ liệu"}
                      </td>
                      <td className="p-4">
                        <span
                          className={`rounded-full px-2 py-1 text-xs ${badge.className}`}
                        >
                          {badge.label}
                        </span>
                      </td>
                      <td className="p-4">
                        <button
                          onClick={() => remove(item.id)}
                          className="text-rose-600"
                        >
                          Bỏ
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}
