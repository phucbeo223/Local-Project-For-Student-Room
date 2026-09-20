import { NextResponse } from "next/server";
import {
  deleteListing,
  updateListing,
  getListing,
  type ApiError,
  type ListingInput,
} from "@/lib/api";
import { withAccessToken } from "@/lib/authenticated-api";

export async function GET(
  _req: Request,
  { params }: { params: { id: string } },
) {
  try {
    return NextResponse.json(await getListing(params.id));
  } catch (e) {
    const err = e as ApiError;
    return NextResponse.json(
      { detail: err.detail || "Không tải được tin" },
      { status: err.status || 502 },
    );
  }
}

export async function PUT(
  req: Request,
  { params }: { params: { id: string } },
) {
  let body: Partial<ListingInput>;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ detail: "Body không hợp lệ" }, { status: 400 });
  }

  try {
    const listing = await withAccessToken((token) =>
      updateListing(token, params.id, body),
    );
    return NextResponse.json(listing);
  } catch (e) {
    const err = e as ApiError;
    return NextResponse.json(
      { detail: err.detail ?? "Sửa tin thất bại" },
      { status: err.status ?? 500 },
    );
  }
}

export async function DELETE(
  _req: Request,
  { params }: { params: { id: string } },
) {
  try {
    await withAccessToken((token) => deleteListing(token, params.id));
    return new NextResponse(null, { status: 204 });
  } catch (e) {
    const err = e as ApiError;
    return NextResponse.json(
      { detail: err.detail ?? "Xóa tin thất bại" },
      { status: err.status ?? 500 },
    );
  }
}
