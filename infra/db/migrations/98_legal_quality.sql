-- Old OCR remains identifiable and is automatically reprocessed by the indexer.
ALTER TABLE legal_documents ADD COLUMN IF NOT EXISTS extraction_version TEXT;
ALTER TABLE legal_chunks ADD COLUMN IF NOT EXISTS text_quality REAL;
ALTER TABLE legal_chunks ADD COLUMN IF NOT EXISTS quality_warning TEXT;
