import { NextResponse } from "next/server";
import { apiFetch, type ApiError } from "@/lib/api";

export async function POST(req: Request) {
  const body = await req.json();
  try {
    return NextResponse.json(
      await apiFetch("/chat/feedback", { method: "POST", body: JSON.stringify(body) }),
      { status: 201 },
    );
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
