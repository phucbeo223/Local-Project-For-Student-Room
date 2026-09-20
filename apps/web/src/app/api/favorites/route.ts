import { NextResponse } from "next/server";
import { getFavorites, type ApiError } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export async function GET() {
  const token = getAccessToken();
  if (!token) return NextResponse.json({ detail: "Chưa đăng nhập" }, { status: 401 });
  try {
    return NextResponse.json(await getFavorites(token));
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
