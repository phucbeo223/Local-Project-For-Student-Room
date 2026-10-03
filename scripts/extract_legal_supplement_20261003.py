"""Extract official files; OCR only the relevant scans, never generate legal text."""
from pathlib import Path
import json
from concurrent.futures import ThreadPoolExecutor
import fitz
from PIL import Image
from app.room_service.legal_knowledge.extractor import _ocr_image, extract_document

OUT = Path('/eval/source_supplement_20261003')
RAW = Path('/source-docs/legal_sources_originals_20261003')

def extract_scan(key):
    target = OUT / (key + '.pages.json')
    if target.exists(): return
    document = fitz.open(RAW / (key + '.pdf'))
    def page_text(index):
        # Each worker owns its PDF handle; PyMuPDF document handles are not shared.
        with fitz.open(RAW / (key + '.pdf')) as copy:
            pix = copy[index].get_pixmap(matrix=fitz.Matrix(2.5, 2.5), alpha=False)
        image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        return {'page': index + 1, 'text': _ocr_image(image, 'vie+eng'), 'ocr': True}
    with ThreadPoolExecutor(max_workers=2) as pool:
        pages = list(pool.map(page_text, range(len(document))))
    target.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / (key + '.txt')).write_text('\n'.join(p['text'] for p in pages), encoding='utf-8')
    print(key, len(pages), 'OCR pages', flush=True)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for key, path in [('fire105', 'legal_sources_originals_20261001/Nghị-định-105-2025-NĐ-CP.docx'),
                      ('housing79', 'legal_sources_originals_20261001/metadata_followup/2026_204_79_VBHN-VPQH.docx')]:
        doc = extract_document(Path('/source-docs') / path, Path('/source-docs'))
        pages = [{'page': p.number, 'text': p.text, 'reused_original': path} for p in doc.pages]
        (OUT / (key + '.pages.json')).write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
        (OUT / (key + '.txt')).write_text('\n'.join(p['text'] for p in pages), encoding='utf-8')
        print(key, sum(len(p['text']) for p in pages), 'chars from archived original', flush=True)
    for key in ('fire55', 'broker29', 'amend347'):
        (OUT / (key + '.pages.json')).write_bytes((RAW / (key + '.pages.json')).read_bytes())
        (OUT / (key + '.txt')).write_bytes((RAW / (key + '.txt')).read_bytes())
    for key in ('civil91', 'civil91first', 'residence68', 'amend118'): extract_scan(key)

if __name__ == '__main__': main()
