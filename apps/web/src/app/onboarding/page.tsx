"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { AMENITY_LABELS } from "@/lib/amenities";
export default function Onboarding() {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const router = useRouter();
  return (
    <main className="mx-auto max-w-xl space-y-6 p-8">
      <h1 className="text-3xl font-bold">Phòng phù hợp với bạn</h1>
      <p>
        Ba tiêu chí để cá nhân hóa gợi ý. Có thể quay lại thay đổi bất cứ lúc
        nào.
      </p>
      <form
        className="space-y-6"
        onSubmit={async (e) => {
          e.preventDefault();
          const data = new FormData(e.currentTarget);
          setBusy(true);
          setError("");
          try {
            const r = await fetch("/api/recommend/quiz", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                max_price: Number(data.get("price")),
                max_distance_ctu: Number(data.get("distance")),
                amenities: data.getAll("amenities"),
              }),
            });
            const b = await r.json();
            if (!r.ok) throw new Error(b.detail);
            router.push("/recommendations");
            router.refresh();
          } catch (e) {
            setError((e as Error).message || "Không kết nối được");
          } finally {
            setBusy(false);
          }
        }}
      >
        <label className="block">
          1. Ngân sách tối đa mỗi tháng (đồng)
          <input
            name="price"
            type="number"
            min="100000"
            max="100000000"
            step="100000"
            defaultValue="2000000"
            required
            className="mt-2 w-full rounded border p-3"
          />
        </label>
        <label className="block">
          2. Khoảng cách tối đa đến CTU khu II (m)
          <input
            name="distance"
            type="number"
            min="100"
            max="100000"
            step="100"
            defaultValue="3000"
            required
            className="mt-2 w-full rounded border p-3"
          />
        </label>
        <fieldset>
          <legend>3. Tiện ích cần có</legend>
          {Object.entries(AMENITY_LABELS).map(([key, label]) => (
            <label key={key} className="mt-2 flex gap-3">
              <input type="checkbox" name="amenities" value={key} />
              {label}
            </label>
          ))}
        </fieldset>
        <p role="alert">{error}</p>
        <button
          disabled={busy}
          className="rounded bg-emerald-700 p-3 text-white"
        >
          Lưu và xem gợi ý
        </button>
      </form>
      <Link className="block underline" href="/recommendations">
        Bỏ qua, xem gợi ý phổ biến
      </Link>
    </main>
  );
}
