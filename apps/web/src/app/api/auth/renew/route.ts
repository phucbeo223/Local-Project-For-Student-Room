import { NextRequest, NextResponse } from "next/server";
import { refresh } from "@/lib/api";
import {
  getRefreshToken,
  setAuthCookies,
  clearAuthCookies,
} from "@/lib/session";

export async function GET(req: NextRequest) {
  const next = req.nextUrl.searchParams.get("next") || "/";
  const safe =
    next.startsWith("/") &&
    !next.startsWith("//") &&
    !next.includes("\\") &&
    !next.startsWith("/api/")
      ? next
      : "/";
  try {
    const token = getRefreshToken();
    if (!token) throw new Error("No session");
    const pair = await refresh(token);
    setAuthCookies(pair.access_token, pair.refresh_token);
    return NextResponse.redirect(new URL(safe, req.url));
  } catch {
    clearAuthCookies();
    return NextResponse.redirect(
      new URL(`/login?next=${encodeURIComponent(safe)}`, req.url),
    );
  }
}
