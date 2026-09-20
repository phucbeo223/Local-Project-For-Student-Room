import { NextResponse } from "next/server";
import { overrideRisk, type ApiError } from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";

export async function PUT(req: Request, { params }: { params: { id: string } }) {
  const body = (await req.json()) as { risk_score: number; note: string };
  try {
    return NextResponse.json(
      await withAccessToken((token) =>
        overrideRisk(token, params.id, body.risk_score, body.note),
      ),
    );
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
