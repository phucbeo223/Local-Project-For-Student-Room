import { NextResponse } from "next/server";
import { apiFetch, type ApiError } from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";
export async function POST(req: Request) {
  try {
    const body = await req.json();
    return NextResponse.json(
      await withAccessToken((token) =>
        apiFetch("/recommend/quiz", {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
          body: JSON.stringify(body),
        }),
      ),
    );
  } catch (e) {
    const err = e as ApiError;
    return NextResponse.json(
      { detail: err.detail || "Không lưu được tiêu chí" },
      { status: err.status || 400 },
    );
  }
}
