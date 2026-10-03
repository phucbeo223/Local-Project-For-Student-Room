"""Read-only comparison of indexed legal documents with the current Data folder."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import psycopg

SUPPORTED = {".pdf", ".doc", ".docx", ".txt", ".md", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("/data"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    actual = {
        path.relative_to(args.data_dir).as_posix()
        for path in args.data_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED
    }
    database_url = os.environ["DATABASE_URL"].replace("postgresql+psycopg://", "postgresql://", 1)
    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT d.source_path, count(c.id), count(c.id) FILTER (WHERE c.embedding_vector IS NOT NULL) "
                "FROM legal_documents d LEFT JOIN legal_chunks c ON c.document_id=d.id "
                "WHERE d.status='ready' GROUP BY d.id ORDER BY d.source_path"
            )
            indexed = {path: (chunks, vectors) for path, chunks, vectors in cursor.fetchall()}
            cursor.execute(
                "SELECT count(*), count(*) FILTER (WHERE embedding_vector IS NOT NULL) "
                "FROM aggregated_listings WHERE status='active' AND cleaning_status='cleaned'"
            )
            listing_count, listing_vectors = cursor.fetchone()
    current_chunks = sum(indexed[path][0] for path in actual & indexed.keys())
    current_vectors = sum(indexed[path][1] for path in actual & indexed.keys())
    report = {
        "data_files": len(actual),
        "indexed_documents": len(indexed),
        "missing_from_index": sorted(actual - indexed.keys()),
        "indexed_but_missing_from_data": sorted(indexed.keys() - actual),
        "current_document_chunks": current_chunks,
        "current_document_vectors": current_vectors,
        "listing_records": listing_count,
        "listing_vectors": listing_vectors,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
