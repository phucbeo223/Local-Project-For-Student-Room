import { NextResponse } from "next/server";
import { deleteSavedSearch, type ApiError } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

export async function DELETE(_: Request, { params }: { params: { id: string } }) {
  const token = getAccessToken();
  if (!token) return NextResponse.json({ detail: "Chưa đăng nhập" }, { status: 401 });
  try {
    await deleteSavedSearch(token, Number(params.id));
    return new NextResponse(null, { status: 204 });
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
