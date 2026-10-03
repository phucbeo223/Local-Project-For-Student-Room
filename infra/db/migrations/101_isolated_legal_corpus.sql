-- Build a separate corpus without copying any old text or embeddings.
CREATE SCHEMA IF NOT EXISTS legal_v2;
CREATE SEQUENCE IF NOT EXISTS legal_v2.document_id;
CREATE SEQUENCE IF NOT EXISTS legal_v2.chunk_id;
CREATE TABLE IF NOT EXISTS legal_v2.legal_documents
    (LIKE public.legal_documents INCLUDING ALL);
ALTER TABLE legal_v2.legal_documents ALTER COLUMN id SET DEFAULT nextval('legal_v2.document_id');
ALTER TABLE legal_v2.legal_documents ADD COLUMN IF NOT EXISTS source_metadata JSONB NOT NULL DEFAULT '{}';
CREATE TABLE IF NOT EXISTS legal_v2.legal_chunks
    (LIKE public.legal_chunks INCLUDING ALL);
ALTER TABLE legal_v2.legal_chunks ALTER COLUMN id SET DEFAULT nextval('legal_v2.chunk_id');
ALTER TABLE legal_v2.legal_chunks ADD COLUMN IF NOT EXISTS provision_id TEXT;
ALTER TABLE legal_v2.legal_chunks ADD COLUMN IF NOT EXISTS parent_content TEXT;
ALTER TABLE legal_v2.legal_chunks ADD COLUMN IF NOT EXISTS source_metadata JSONB NOT NULL DEFAULT '{}';
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='legal_v2_document_fk') THEN
        ALTER TABLE legal_v2.legal_chunks ADD CONSTRAINT legal_v2_document_fk
        FOREIGN KEY(document_id) REFERENCES legal_v2.legal_documents(id) ON DELETE CASCADE;
    END IF;
END $$;
CREATE TABLE IF NOT EXISTS public.legal_corpus_releases (
    schema_name TEXT PRIMARY KEY,
    status TEXT NOT NULL CHECK(status IN ('staging','validated','active','retired')),
    manifest_sha256 TEXT,
    validation JSONB NOT NULL DEFAULT '{}',
    activated_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
INSERT INTO public.legal_corpus_releases(schema_name,status) VALUES('public','active'),('legal_v2','staging')
ON CONFLICT(schema_name) DO NOTHING;
