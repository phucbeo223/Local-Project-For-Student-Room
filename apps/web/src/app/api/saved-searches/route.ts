import { NextResponse } from "next/server";
import { createSavedSearch, getSavedSearches, type ApiError, type SavedSearchCriteria } from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";

export async function GET() {
  try {
    return NextResponse.json(await withAccessToken(getSavedSearches));
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}

export async function POST(req: Request) {
  const body = (await req.json()) as { name: string; criteria: SavedSearchCriteria; notify_enabled: boolean };
  try {
    return NextResponse.json(
      await withAccessToken((token) => createSavedSearch(token, body)),
      { status: 201 },
    );
  } catch (error) {
    const value = error as ApiError;
    return NextResponse.json({ detail: value.detail }, { status: value.status ?? 500 });
  }
}
