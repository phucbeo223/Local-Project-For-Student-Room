import { NextResponse } from "next/server";
import { addFavorite, removeFavorite, type ApiError } from "@/lib/api";
import { getAccessToken } from "@/lib/session";

function unauthorized() {
  return NextResponse.json({ detail: "Chưa đăng nhập" }, { status: 401 });
}

export async function PUT(_: Request, { params }: { params: { id: string } }) {
  const token = getAccessToken();
  if (!token) return unauthorized();
  try {
    return NextResponse.json(await addFavorite(token, params.id));
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}

export async function DELETE(_: Request, { params }: { params: { id: string } }) {
  const token = getAccessToken();
  if (!token) return unauthorized();
  try {
    await removeFavorite(token, params.id);
    return new NextResponse(null, { status: 204 });
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
