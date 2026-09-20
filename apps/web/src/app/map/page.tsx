import { getNearby, type ApiError, type ListingOut } from "@/lib/api";
import SiteHeader from "../SiteHeader";
import MapScreen from "./MapScreen";
import { CAMPUSES } from "./campuses";

export const dynamic = "force-dynamic";

// Tâm tìm kiếm = CTU khu II, khớp CAMPUSES[1] backend (apps/api/app/listings/routing.py).
const CTU_LAT = 10.0322;
const CTU_LNG = 105.7683;
const DEFAULT_RADIUS = 3000;
const MIN_RADIUS = 500;
const MAX_RADIUS = 5000;

export default async function MapPage({
  searchParams,
}: {
  searchParams: {
    radius?: string;
    lat?: string;
    lng?: string;
    campus?: string;
  };
}) {
  const campus = [0, 1, 2].includes(Number(searchParams.campus))
    ? Number(searchParams.campus)
    : 1;
  const candidateLat = Number(searchParams.lat),
    candidateLng = Number(searchParams.lng);
  const lat =
    searchParams.lat &&
    Number.isFinite(candidateLat) &&
    Math.abs(candidateLat) <= 90
      ? candidateLat
      : CAMPUSES[campus].lat;
  const lng =
    searchParams.lng &&
    Number.isFinite(candidateLng) &&
    Math.abs(candidateLng) <= 180
      ? candidateLng
      : CAMPUSES[campus].lng;
  const parsed = Number(searchParams.radius);
  const radius = Number.isFinite(parsed)
    ? Math.min(MAX_RADIUS, Math.max(MIN_RADIUS, parsed))
    : DEFAULT_RADIUS;

  let items: ListingOut[] = [];
  let errorMessage: string | null = null;
  try {
    items = await getNearby(lat, lng, radius);
  } catch (e) {
    errorMessage =
      (e as ApiError).detail ?? "Không thể tải danh sách tin lân cận";
  }

  return (
    <div className="flex h-screen flex-col bg-paper">
      <SiteHeader />
      <MapScreen
        key={`${lat}:${lng}:${radius}:${campus}`}
        items={items}
        radius={radius}
        error={errorMessage}
        center={[lat, lng]}
        initialCampus={campus}
      />
    </div>
  );
}
