"use client";
import { useState } from "react";
import Link from "next/link";
export default function ForgotPassword() {
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  return (
    <main className="mx-auto max-w-md space-y-5 p-8">
      <h1 className="text-2xl font-bold">Quên mật khẩu</h1>
      <form
        className="space-y-4"
        onSubmit={async (e) => {
          e.preventDefault();
          const data = new FormData(e.currentTarget);
          setBusy(true);
          try {
            const r = await fetch("/api/auth/forgot-password", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ email: data.get("email") }),
            });
            const b = await r.json();
            setMessage(
              r.ok
                ? "Nếu email đã đăng ký, bạn sẽ nhận được hướng dẫn (hết hạn sau 30 phút)."
                : b.detail,
            );
          } catch {
            setMessage("Không kết nối được máy chủ");
          } finally {
            setBusy(false);
          }
        }}
      >
        <label className="block">
          Email
          <input
            name="email"
            type="email"
            required
            className="w-full rounded border p-3"
          />
        </label>
        <button
          disabled={busy}
          className="rounded bg-emerald-700 p-3 text-white"
        >
          Gửi hướng dẫn
        </button>
      </form>
      <p role="status">{message}</p>
      <Link href="/login">Đăng nhập</Link>
    </main>
  );
}
