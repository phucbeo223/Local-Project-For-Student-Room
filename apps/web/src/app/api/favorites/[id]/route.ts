import { NextResponse } from "next/server";
import { addFavorite, removeFavorite, type ApiError } from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";

export async function PUT(_: Request, { params }: { params: { id: string } }) {
  try {
    return NextResponse.json(
      await withAccessToken((token) => addFavorite(token, params.id)),
    );
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}

export async function DELETE(_: Request, { params }: { params: { id: string } }) {
  try {
    await withAccessToken((token) => removeFavorite(token, params.id));
    return new NextResponse(null, { status: 204 });
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
