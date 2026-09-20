import { NextResponse } from "next/server";
import { deleteSavedSearch, type ApiError } from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";

export async function DELETE(_: Request, { params }: { params: { id: string } }) {
  try {
    await withAccessToken((token) => deleteSavedSearch(token, Number(params.id)));
    return new NextResponse(null, { status: 204 });
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
