import { NextResponse } from "next/server";
import { recordInteraction, type ApiError, type InteractionType } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export async function POST(req: Request) {
  const token = getAccessToken();
  if (!token) return NextResponse.json({ detail: "Chưa đăng nhập" }, { status: 401 });
  const body = (await req.json()) as { listing_id: number; type: InteractionType; duration_ms?: number };
  try {
    return NextResponse.json(
      await recordInteraction(token, body.listing_id, body.type, body.duration_ms),
      { status: 201 },
    );
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
