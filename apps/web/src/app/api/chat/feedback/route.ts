import { NextResponse } from "next/server";
import { apiFetch, type ApiError } from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    return NextResponse.json(
      await withAccessToken((token) =>
        apiFetch("/chat/feedback", {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
          body: JSON.stringify(body),
        }),
      ),
      { status: 201 },
    );
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json(
      { detail: value.detail },
      { status: value.status ?? 500 },
    );
  }
}
