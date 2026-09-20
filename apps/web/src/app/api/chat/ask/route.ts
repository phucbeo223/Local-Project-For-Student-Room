import { NextRequest, NextResponse } from "next/server";
import { apiFetch, type ApiError } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export async function POST(req: NextRequest) {
  const token = getAccessToken();
  if (!token)
    return NextResponse.json(
      { detail: "Vui lòng đăng nhập để dùng trợ lý AI" },
      { status: 401 },
    );
  try {
    const body = await req.json();
    const result = await apiFetch<unknown>("/chat/ask", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(body),
    });
    return NextResponse.json(result);
  } catch (error) {
    const apiError = error as ApiError;
    return NextResponse.json(
      { detail: apiError.detail ?? "Không thể gửi câu hỏi" },
      { status: apiError.status ?? 500 },
    );
  }
}
