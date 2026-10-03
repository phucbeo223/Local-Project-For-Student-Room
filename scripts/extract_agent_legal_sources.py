"""OCR original government PDFs, preserving physical page provenance."""
from pathlib import Path
import concurrent.futures
import hashlib
import json
import os
import sys
os.environ['OMP_THREAD_LIMIT'] = '1'
import fitz
import pytesseract
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/'docs/legal_agent_originals_20261003'
OUT = ROOT/'eval/agent_source_ocr'


def page_text(task):
    name, number = task
    target = OUT/name/(str(number)+'.txt')
    if target.exists():
        return
    with fitz.open(RAW/(name+'.pdf')) as doc:
        pix = doc[number-1].get_pixmap(matrix=fitz.Matrix(2,2))
        image = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(image, lang='vie+eng', config='--psm 6', timeout=90)
    target.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    manifest = json.loads((RAW/'manifest.json').read_text(encoding='utf-8'))
    tasks = []
    for source in manifest['sources']:
        name = source['id']
        assert hashlib.sha256((RAW/(name+'.pdf')).read_bytes()).hexdigest() == source['sha256']
        (OUT/name).mkdir(parents=True, exist_ok=True)
        tasks.extend((name, n) for n in range(1, source['pages']+1))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for i, _ in enumerate(pool.map(page_text, tasks),1):
            if i%10 == 0: print('OCR', i, '/', len(tasks), flush=True)
    for source in manifest['sources']:
        name = source['id']
        pages = [{'page': n, 'text': (OUT/name/(str(n)+'.txt')).read_text(encoding='utf-8')}
                 for n in range(1, source['pages']+1)]
        (OUT/(name+'.json')).write_text(json.dumps(pages, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('OCR completed',len(tasks),'pages',flush=True)
