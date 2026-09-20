import { NextResponse } from "next/server";
import { getNotifications, refreshNotifications, type ApiError } from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";

export async function GET() {
  try { return NextResponse.json(await withAccessToken(getNotifications)); }
  catch (error) { const value = error as ApiError; return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 }); }
}

export async function POST() {
  try { return NextResponse.json(await withAccessToken(refreshNotifications)); }
  catch (error) { const value = error as ApiError; return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 }); }
}
