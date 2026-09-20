"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useRouter } from "next/navigation";

const registerSchema = z.object({
  name: z.union([z.string().max(100), z.literal("")]).optional(),
  email: z.string().email("Email không hợp lệ"),
  password: z.string().min(8, "Mật khẩu tối thiểu 8 ký tự"),
  confirm: z.string(),
}).refine(data=>data.password === data.confirm,{message:"Mật khẩu nhập lại chưa khớp",path:["confirm"]});

type RegisterFormValues = z.infer<typeof registerSchema>;

export default function RegisterForm() {
  const router = useRouter();
  const [formError, setFormError] = useState<string | null>(null);
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  async function verify(resend = false) {
    setBusy(true);
    setFormError(null);
    setNotice("");
    try {
      const res = await fetch(
        `/api/auth/${resend ? "resend-otp" : "verify-email"}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, code }),
        },
      );
      const body = await res.json();
      if (!res.ok) throw new Error(body.detail || "Xác thực thất bại");
      if (resend)
        setNotice("Đã gửi mã mới. Đợi ít nhất 60 giây trước khi gửi lại.");
      else {
        router.push("/onboarding");
        router.refresh();
      }
    } catch (e) {
      setFormError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormValues) => {
    setFormError(null);
    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (res.ok) {
        setEmail(data.email);
        return;
      }

      const body = (await res.json().catch(() => ({}))) as {
        detail?: string;
      };
      setFormError(body.detail ?? "Đăng ký thất bại");
    } catch {
      setFormError("Không thể kết nối tới máy chủ");
    }
  };

  if (email)
    return (
      <form
        className="space-y-4"
        onSubmit={(e) => {
          e.preventDefault();
          void verify();
        }}
      >
        <p>
          Mã OTP 6 số đã gửi đến {email}, có hiệu lực 5 phút, tối đa 3 lần thử.
        </p>
        <label className="block">
          Mã xác thực
          <input
            className="mt-2 w-full rounded border p-3"
            inputMode="numeric"
            autoComplete="one-time-code"
            pattern="[0-9]{6}"
            maxLength={6}
            required
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
        </label>
        <p role="status">{formError || notice}</p>
        <button
          disabled={busy}
          className="rounded bg-emerald-700 p-3 text-white"
        >
          Xác thực
        </button>
        <button
          type="button"
          disabled={busy}
          className="ml-4 underline"
          onClick={() => void verify(true)}
        >
          Gửi lại OTP
        </button>
      </form>
    );
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {formError && (
        <p className="rounded-md bg-rose-50 px-3 py-2 text-sm text-rose-600">
          {formError}
        </p>
      )}

      <div>
        <label
          htmlFor="name"
          className="block text-sm font-medium text-slate-700"
        >
          Họ tên (tùy chọn)
        </label>
        <input
          id="name"
          type="text"
          autoComplete="name"
          className="mt-1 w-full rounded border border-slate-300 px-3 py-2 text-slate-800 focus:border-emerald-500 focus:outline-none"
          {...register("name")}
        />
        {errors.name && (
          <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
        )}
      </div>

      <div>
        <label
          htmlFor="email"
          className="block text-sm font-medium text-slate-700"
        >
          Email
        </label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          className="mt-1 w-full rounded border border-slate-300 px-3 py-2 text-slate-800 focus:border-emerald-500 focus:outline-none"
          {...register("email")}
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
        )}
      </div>

      <div>
        <label
          htmlFor="password"
          className="block text-sm font-medium text-slate-700"
        >
          Mật khẩu
        </label>
        <input
          id="password"
          type="password"
          autoComplete="new-password"
          className="mt-1 w-full rounded border border-slate-300 px-3 py-2 text-slate-800 focus:border-emerald-500 focus:outline-none"
          {...register("password")}
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
        )}
      </div>

      <label className="block text-sm font-medium text-slate-700">Nhập lại mật khẩu<input type="password" autoComplete="new-password" className="mt-1 w-full rounded border border-slate-300 px-3 py-2" {...register("confirm")}/>{errors.confirm && <span className="text-red-600">{errors.confirm.message}</span>}</label>
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded bg-emerald-600 px-4 py-2 font-medium text-white hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isSubmitting ? "Đang xử lý..." : "Đăng ký"}
      </button>
    </form>
  );
}
