import { NextResponse } from "next/server";
import { apiFetch, type ApiError } from "@/lib/api";
import { getAccessToken } from "@/lib/session";
export async function POST(req: Request) {
  const token = getAccessToken();
  if (!token)
    return NextResponse.json({ detail: "Chưa đăng nhập" }, { status: 401 });
  try {
    return NextResponse.json(
      await apiFetch("/recommend/quiz", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: JSON.stringify(await req.json()),
      }),
    );
  } catch (e) {
    const err = e as ApiError;
    return NextResponse.json(
      { detail: err.detail || "Không lưu được tiêu chí" },
      { status: err.status || 400 },
    );
  }
}
