from __future__ import annotations

from typing import Sequence

from sqlalchemy import text
from sqlalchemy.engine import Engine

from .chunker import LegalChunk
from .extractor import ExtractedDocument


def _vector_literal(vector: Sequence[float]) -> str:
    return "[" + ",".join(f"{value:.9g}" for value in vector) + "]"


class LegalKnowledgeRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def current_hash(self, source_path: str) -> str | None:
        with self.engine.connect() as connection:
            return connection.execute(
                text(
                    "SELECT content_sha256 FROM legal_documents "
                    "WHERE source_path=:source_path AND status='ready'"
                ),
                {"source_path": source_path},
            ).scalar_one_or_none()

    def replace_document(
        self,
        document: ExtractedDocument,
        chunks: Sequence[LegalChunk],
        vectors: Sequence[Sequence[float] | None],
        embedding_model: str | None,
    ) -> int:
        if len(chunks) != len(vectors):
            raise ValueError("Số vector không khớp số chunk")
        with self.engine.begin() as connection:
            document_id = int(
                connection.execute(
                    text(
                        "INSERT INTO legal_documents "
                        "(source_path,title,category,document_type,content_sha256,page_count,"
                        "ocr_page_count,ocr_engine,status,error_message,indexed_at,updated_at) "
                        "VALUES (:source_path,:title,:category,:document_type,:content_sha256,"
                        ":page_count,:ocr_page_count,:ocr_engine,'indexing',NULL,NULL,now()) "
                        "ON CONFLICT (source_path) DO UPDATE SET title=EXCLUDED.title,"
                        "category=EXCLUDED.category,document_type=EXCLUDED.document_type,"
                        "content_sha256=EXCLUDED.content_sha256,page_count=EXCLUDED.page_count,"
                        "ocr_page_count=EXCLUDED.ocr_page_count,ocr_engine=EXCLUDED.ocr_engine,"
                        "status='indexing',error_message=NULL,updated_at=now() RETURNING id"
                    ),
                    {
                        "source_path": document.source_path,
                        "title": document.title,
                        "category": document.category,
                        "document_type": document.document_type,
                        "content_sha256": document.content_sha256,
                        "page_count": document.page_count,
                        "ocr_page_count": document.ocr_page_count,
                        "ocr_engine": document.ocr_engine,
                    },
                ).scalar_one()
            )
            connection.execute(text("DELETE FROM legal_chunks WHERE document_id=:id"), {"id": document_id})
            for chunk, vector in zip(chunks, vectors):
                connection.execute(
                    text(
                        "INSERT INTO legal_chunks "
                        "(document_id,chunk_index,page_from,page_to,heading,content,content_sha256,"
                        "embedding_vector,embedding_model,embedded_at) VALUES "
                        "(:document_id,:chunk_index,:page_from,:page_to,:heading,:content,"
                        ":content_sha256,CAST(:embedding_vector AS vector),:embedding_model,"
                        "CASE WHEN :embedding_vector IS NULL THEN NULL ELSE now() END)"
                    ),
                    {
                        "document_id": document_id,
                        "chunk_index": chunk.chunk_index,
                        "page_from": chunk.page_from,
                        "page_to": chunk.page_to,
                        "heading": chunk.heading,
                        "content": chunk.content,
                        "content_sha256": chunk.content_sha256,
                        "embedding_vector": _vector_literal(vector) if vector is not None else None,
                        "embedding_model": embedding_model if vector is not None else None,
                    },
                )
            connection.execute(
                text(
                    "UPDATE legal_documents SET status='ready',indexed_at=now(),updated_at=now() "
                    "WHERE id=:id"
                ),
                {"id": document_id},
            )
        return document_id

    def mark_failed(self, source_path: str, path_name: str, category: str, sha256: str, error: str) -> None:
        with self.engine.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO legal_documents "
                    "(source_path,title,category,document_type,content_sha256,status,error_message,updated_at) "
                    "VALUES (:source_path,:title,:category,:document_type,:sha,'failed',:error,now()) "
                    "ON CONFLICT (source_path) DO UPDATE SET content_sha256=EXCLUDED.content_sha256,"
                    "status='failed',error_message=EXCLUDED.error_message,updated_at=now()"
                ),
                {
                    "source_path": source_path,
                    "title": path_name,
                    "category": category,
                    "document_type": source_path.rsplit(".", 1)[-1].lower(),
                    "sha": sha256,
                    "error": error[:2000],
                },
            )
