import { NextResponse } from "next/server";
import { markNotificationRead, type ApiError } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export async function PATCH(_: Request, { params }: { params: { id: string } }) {
  const token = getAccessToken();
  if (!token) return NextResponse.json({ detail: "Chưa đăng nhập" }, { status: 401 });
  try {
    return NextResponse.json(await markNotificationRead(token, Number(params.id)));
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
