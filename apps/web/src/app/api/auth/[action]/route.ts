import { NextResponse } from "next/server";
import { apiFetch, type ApiError, type TokenPair } from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";
import { setAuthCookies } from "@/lib/session";

const actions: Record<string, string> = {
  "verify-email": "verify-email",
  "resend-otp": "resend-otp",
  "forgot-password": "forgot-password",
  "reset-password": "reset-password",
  google: "login/google",
  profile: "me",
};
export async function POST(
  req: Request,
  { params }: { params: { action: string } },
) {
  const path = actions[params.action];
  if (!path)
    return NextResponse.json({ detail: "Không tìm thấy" }, { status: 404 });
  try {
    const body = await req.json();
    const request = (token?: string) =>
      apiFetch<TokenPair>(`/auth/${path}`, {
        method: path === "me" ? "PATCH" : "POST",
        body: JSON.stringify(body),
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
    const result = path === "me"
      ? await withAccessToken((token) => request(token))
      : await request();
    if (result.access_token && result.refresh_token)
      setAuthCookies(result.access_token, result.refresh_token);
    return NextResponse.json({ ok: true });
  } catch (e) {
    const err = e as ApiError;
    return NextResponse.json(
      { detail: err.detail || "Yêu cầu thất bại" },
      { status: err.status || 400 },
    );
  }
}
