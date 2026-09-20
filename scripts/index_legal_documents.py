"""Scan, OCR, chunk and embed a folder of Vietnamese legal documents."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps/api"))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from sqlalchemy import create_engine

from app.room_service.chatbot.providers import E5EmbeddingProvider
from app.room_service.legal_knowledge import LegalDocumentIndexer, LegalKnowledgeRepository
from db_connection import local_database_url


MIGRATION = ROOT / "infra/db/migrations/94_legal_knowledge.sql"


def _sqlalchemy_url(value: str) -> str:
    return value.replace("postgresql://", "postgresql+psycopg://", 1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="OCR và lập chỉ mục pgvector cho thư mục văn bản pháp luật"
    )
    parser.add_argument("--data-dir", type=Path, default=ROOT / "Data")
    parser.add_argument("--database-url", help="Override URL; mặc định đọc host port từ Compose")
    parser.add_argument(
        "--model",
        default=os.getenv("CHATBOT_EMBEDDING_MODEL", "intfloat/multilingual-e5-small"),
    )
    parser.add_argument("--ocr-language", default="vie+eng")
    parser.add_argument("--batch-size", type=int, default=24)
    parser.add_argument("--force", action="store_true", help="Index lại cả file không đổi")
    parser.add_argument("--force-ocr", action="store_true", help="OCR tất cả trang PDF")
    parser.add_argument(
        "--lexical-only",
        action="store_true",
        help="Không tạo embedding; chatbot chỉ dùng BM25 (chế độ suy giảm)",
    )
    parser.add_argument(
        "--apply-migration",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Tự áp migration 94 trước khi index (mặc định: có)",
    )
    args = parser.parse_args()

    database_url = local_database_url(args.database_url or os.getenv("DATABASE_URL"))
    if args.apply_migration:
        import psycopg

        with psycopg.connect(database_url, autocommit=True) as connection:
            connection.execute(MIGRATION.read_text(encoding="utf-8"), prepare=False)
        print(f"Applied {MIGRATION.name}")

    engine = create_engine(_sqlalchemy_url(database_url), pool_pre_ping=True)

    embedder = None if args.lexical_only else E5EmbeddingProvider(args.model)
    indexer = LegalDocumentIndexer(
        LegalKnowledgeRepository(engine),
        embedder,
        batch_size=args.batch_size,
        ocr_language=args.ocr_language,
        force_ocr=args.force_ocr,
    )
    try:
        report = indexer.index_folder(args.data_dir, force=args.force)
    finally:
        engine.dispose()

    print(
        "Legal indexing complete: "
        f"{report.discovered} files, {report.indexed} indexed, {report.skipped} unchanged, "
        f"{report.failed} failed, {report.chunks} chunks, {report.ocr_pages} OCR pages"
    )
    for error in report.errors:
        print(f"ERROR {error}", file=sys.stderr)
    if report.failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
