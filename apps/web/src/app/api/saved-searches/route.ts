import { NextResponse } from "next/server";
import { createSavedSearch, getSavedSearches, type ApiError, type SavedSearchCriteria } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export async function GET() {
  const token = getAccessToken();
  if (!token) return NextResponse.json({ detail: "Chưa đăng nhập" }, { status: 401 });
  try {
    return NextResponse.json(await getSavedSearches(token));
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}

export async function POST(req: Request) {
  const token = getAccessToken();
  if (!token) return NextResponse.json({ detail: "Chưa đăng nhập" }, { status: 401 });
  const body = (await req.json()) as { name: string; criteria: SavedSearchCriteria; notify_enabled: boolean };
  try {
    return NextResponse.json(await createSavedSearch(token, body), { status: 201 });
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
