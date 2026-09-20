import { NextResponse } from "next/server";
import { apiFetch, type ApiError } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export async function POST(req: Request) {
  const token = getAccessToken();
  if (!token)
    return NextResponse.json({ detail: "Vui lòng đăng nhập" }, { status: 401 });
  try {
    const body = await req.json();
    return NextResponse.json(
      await apiFetch("/chat/feedback", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: JSON.stringify(body),
      }),
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
