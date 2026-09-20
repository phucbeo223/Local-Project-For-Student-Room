import { NextResponse } from "next/server";
import { overrideRisk, type ApiError } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export async function PUT(req: Request, { params }: { params: { id: string } }) {
  const token = getAccessToken();
  if (!token) return NextResponse.json({ detail: "Chưa đăng nhập" }, { status: 401 });
  const body = (await req.json()) as { risk_score: number; note: string };
  try {
    return NextResponse.json(await overrideRisk(token, params.id, body.risk_score, body.note));
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
