import { NextResponse } from "next/server";
import { getNotifications, refreshNotifications, type ApiError } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export async function GET() {
  const token = getAccessToken();
  if (!token) return NextResponse.json({ detail: "Chưa đăng nhập" }, { status: 401 });
  try { return NextResponse.json(await getNotifications(token)); }
  catch (error) { const value = error as ApiError; return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 }); }
}

export async function POST() {
  const token = getAccessToken();
  if (!token) return NextResponse.json({ detail: "Chưa đăng nhập" }, { status: 401 });
  try { return NextResponse.json(await refreshNotifications(token)); }
  catch (error) { const value = error as ApiError; return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 }); }
}
