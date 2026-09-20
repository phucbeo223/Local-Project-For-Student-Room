import { NextResponse } from "next/server";
import { clearAuthCookies, getRefreshToken } from "@/lib/session";
import { apiFetch } from "@/lib/api";

export async function POST() {
  const token = getRefreshToken();
  if (token) {
    try {
      await apiFetch("/auth/logout", {
        method: "POST",
        body: JSON.stringify({ refresh_token: token }),
      });
    } catch {
      return NextResponse.json(
        { detail: "Máy chủ chưa thu hồi được phiên. Vui lòng thử lại." },
        { status: 503 },
      );
    }
  }
  clearAuthCookies();
  return NextResponse.json({ ok: true });
}
