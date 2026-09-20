"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
export default function ProfileForm({ name }: { name: string }) {
  const [message, setMessage] = useState("");
  const router = useRouter();
  return (
    <form
      className="mt-5 space-y-3"
      onSubmit={async (e) => {
        e.preventDefault();
        const data = new FormData(e.currentTarget);
        try {
          const r = await fetch("/api/auth/profile", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: data.get("name") }),
          });
          const b = await r.json();
          setMessage(r.ok ? "Đã lưu" : b.detail);
          if (r.ok) router.refresh();
        } catch {
          setMessage("Không kết nối được máy chủ");
        }
      }}
    >
      <label className="block">
        Họ tên
        <input
          name="name"
          defaultValue={name}
          minLength={1}
          maxLength={100}
          required
          className="mt-1 w-full rounded border p-2"
        />
      </label>
      <button className="rounded bg-emerald-700 p-2 text-white">
        Lưu hồ sơ
      </button>
      <p role="status">{message}</p>
    </form>
  );
}
