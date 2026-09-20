import { NextResponse } from "next/server";
import { markNotificationRead, type ApiError } from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";

export async function PATCH(_: Request, { params }: { params: { id: string } }) {
  try {
    return NextResponse.json(
      await withAccessToken((token) => markNotificationRead(token, Number(params.id))),
    );
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
