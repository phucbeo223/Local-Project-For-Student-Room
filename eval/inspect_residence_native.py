"""Inspect native official Word clauses locally; never reads PDF or OCR."""
import sys
from pathlib import Path
sys.path.insert(0, '/workspace/scripts')
import prepare_priority7_corpus as native

for key in ('nd154.doc','nd58.docx'):
    path=Path('/eval/provider_sources_20261006/residence_native')/key
    document=native.extract_document(path,path.parent)
    assert document.ocr_engine is None and not any(p.ocr_used for p in document.pages)
    body='\n\n'.join(p.text for p in document.pages)
    (path.with_suffix('.native.txt')).write_text(body,encoding='utf-8')
    parts=native.structure_provisions(body,native.sha(path))
    for p in parts:
        if (key=='nd154.doc' and p.article in ('5','10','21')) or (key=='nd58.docx' and p.article in ('4','7')):
            print(key,p.article,p.clause,p.heading,'\n',p.content,'\n')
