"use client";
import { useState } from "react";
import Link from "next/link";
export default function ResetPassword() {
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  return (
    <main className="mx-auto max-w-md space-y-5 p-8">
      <h1 className="text-2xl font-bold">Đặt lại mật khẩu</h1>
      <form
        className="space-y-4"
        onSubmit={async (e) => {
          e.preventDefault();
          const data = new FormData(e.currentTarget);
          if (data.get("password") !== data.get("confirm")) {
            setMessage("Mật khẩu nhập lại chưa khớp");
            return;
          }
          setBusy(true);
          const q = new URLSearchParams(window.location.search);
          try {
            const r = await fetch("/api/auth/reset-password", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                email: q.get("email"),
                token: q.get("token"),
                password: data.get("password"),
              }),
            });
            const b = await r.json();
            setMessage(
              r.ok ? "Đã đổi mật khẩu. Vui lòng đăng nhập lại." : b.detail,
            );
          } catch {
            setMessage("Không kết nối được máy chủ");
          } finally {
            setBusy(false);
          }
        }}
      >
        <label className="block">
          Mật khẩu mới
          <input
            name="password"
            type="password"
            minLength={8}
            maxLength={128}
            required
            autoComplete="new-password"
            className="w-full rounded border p-3"
          />
        </label>
        <label className="block">
          Nhập lại mật khẩu
          <input
            name="confirm"
            type="password"
            required
            autoComplete="new-password"
            className="w-full rounded border p-3"
          />
        </label>
        <button
          disabled={busy}
          className="rounded bg-emerald-700 p-3 text-white"
        >
          Đổi mật khẩu
        </button>
      </form>
      <p role="status">{message}</p>
      <Link href="/login">Đăng nhập</Link>
    </main>
  );
}
