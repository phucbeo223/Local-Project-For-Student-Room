"""Index approved local listing images for FR7. Never fetch arbitrary URLs.

Input JSON array: [{"listing_id":123,"image_url":"https://...","file":"room.jpg"}].
Files must resolve within --image-root. URLs must already belong to the listing.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api"))


def main():
    from PIL import Image
    import imagehash
    from sqlalchemy import create_engine, text
    from app.config import settings

    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--image-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.image_root.resolve(strict=True)
    engine = create_engine(settings.database_url)
    count = 0
    with engine.begin() as conn:
        for row in json.loads(args.manifest.read_text(encoding="utf-8")):
            path = (root / row["file"]).resolve(strict=True)
            if not path.is_relative_to(root):
                raise ValueError("Image outside approved root")
            exists = conn.execute(
                text(
                    "SELECT 1 FROM aggregated_listings WHERE id=:id AND :url=ANY(images)"
                ),
                {"id": row["listing_id"], "url": row["image_url"]},
            ).first()
            if not exists:
                raise ValueError("Image URL does not belong to listing")
            with Image.open(path) as im:
                value = f"{int(str(imagehash.phash(im)),16):064b}"
            conn.execute(
                text(
                    "INSERT INTO listing_image_hashes(listing_id,image_url,phash) VALUES (:id,:url,CAST(:hash AS bit(64))) ON CONFLICT(listing_id,image_url) DO UPDATE SET phash=excluded.phash"
                ),
                {"id": row["listing_id"], "url": row["image_url"], "hash": value},
            )
            count += 1
    print(f"Indexed {count} approved images")


if __name__ == "__main__":
    main()
