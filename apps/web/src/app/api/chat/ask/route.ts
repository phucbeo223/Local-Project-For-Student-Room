import { NextRequest, NextResponse } from "next/server";
import { apiFetch, type ApiError } from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const result = await withAccessToken((token) =>
      apiFetch<unknown>("/chat/ask", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: JSON.stringify(body),
      }),
    );
    return NextResponse.json(result);
  } catch (error) {
    const apiError = error as ApiError;
    return NextResponse.json(
      { detail: apiError.detail ?? "Không thể gửi câu hỏi" },
      { status: apiError.status ?? 500 },
    );
  }
}
