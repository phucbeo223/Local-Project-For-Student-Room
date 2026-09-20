-- OCR + RAG knowledge base for Vietnamese housing-related legal documents.
-- Additive and idempotent: safe to run against an existing development volume.

CREATE TABLE IF NOT EXISTS legal_documents (
    id                  BIGSERIAL PRIMARY KEY,
    source_path         TEXT NOT NULL UNIQUE,
    title               TEXT NOT NULL,
    category            VARCHAR(80) NOT NULL DEFAULT 'uncategorized',
    document_type       VARCHAR(16) NOT NULL,
    content_sha256      CHAR(64) NOT NULL,
    page_count          INTEGER NOT NULL DEFAULT 0 CHECK (page_count >= 0),
    ocr_page_count      INTEGER NOT NULL DEFAULT 0 CHECK (ocr_page_count >= 0),
    ocr_engine          VARCHAR(80),
    status              VARCHAR(20) NOT NULL DEFAULT 'ready'
                        CHECK (status IN ('indexing', 'ready', 'failed')),
    error_message       TEXT,
    indexed_at          TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_legal_documents_category_status
    ON legal_documents (category, status);

CREATE TABLE IF NOT EXISTS legal_chunks (
    id                  BIGSERIAL PRIMARY KEY,
    document_id         BIGINT NOT NULL REFERENCES legal_documents(id) ON DELETE CASCADE,
    chunk_index         INTEGER NOT NULL CHECK (chunk_index >= 0),
    page_from           INTEGER CHECK (page_from IS NULL OR page_from >= 1),
    page_to             INTEGER CHECK (page_to IS NULL OR page_to >= 1),
    heading             TEXT,
    content             TEXT NOT NULL,
    content_sha256      CHAR(64) NOT NULL,
    content_tsv         TSVECTOR GENERATED ALWAYS AS (
                            to_tsvector('simple', coalesce(heading, '') || ' ' || content)
                        ) STORED,
    embedding_vector    VECTOR(384),
    embedding_model     VARCHAR(120),
    embedded_at         TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (document_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS idx_legal_chunks_document
    ON legal_chunks (document_id, chunk_index);
CREATE INDEX IF NOT EXISTS idx_legal_chunks_tsv
    ON legal_chunks USING GIN (content_tsv);

-- The initial legal corpus is small enough for exact cosine search. Add HNSW only
-- after measuring a production corpus; this avoids an unnecessary build-time cost.

