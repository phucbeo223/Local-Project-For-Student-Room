import { NextResponse } from "next/server";
import { getFavorites, type ApiError } from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";

export async function GET() {
  try {
    return NextResponse.json(await withAccessToken(getFavorites));
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
