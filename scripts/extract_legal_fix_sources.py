"""Extract downloaded sources with per-page caches; no inferred OCR corrections."""
from pathlib import Path
import json,sys,hashlib,subprocess
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'apps/api'))
from app.room_service.legal_knowledge.extractor import extract_document


def page_text(task):
    import fitz
    path,number=task
    with fitz.open(path) as doc:
        page=doc[number-1];text=page.get_text()
        if len(text.strip())<500:
            from PIL import Image
            from app.room_service.legal_knowledge.extractor import _ocr_image
            pix=page.get_pixmap(matrix=fitz.Matrix(2.5,2.5),alpha=False)
            text=_ocr_image(Image.frombytes('RGB',(pix.width,pix.height),pix.samples),'vie+eng')
    return {'page':number,'text':text}


def main():
    folder=ROOT/'docs/legal_fix_originals_20261004'
    manifest=json.loads((folder/'download_manifest.json').read_text(encoding='utf-8'))
    cache=ROOT/'eval/legal_fix_ocr_20261004';cache.mkdir(parents=True,exist_ok=True)
    for source in manifest['sources']:
        attachments=source.get('attachments',[])
        if not attachments:continue
        raw=next((a for a in attachments if a['path'].endswith('.doc')),attachments[0])
        path=ROOT/raw['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==raw['sha256']
        target=cache/(source['id']+'.json')
        if target.exists():continue
        if path.suffix=='.doc':
            doc=extract_document(path,path.parent)
            pages=[{'page':p.number,'text':p.text} for p in doc.pages]
        else:
            import fitz
            # Decree forms are not operative clauses; article parser excludes them.
            with fitz.open(path) as doc:count=len(doc)
            tasks=[(path,n) for n in range(1,count+1)]
            pages=[]
            with ThreadPoolExecutor(max_workers=3) as pool:
                for page in pool.map(page_text,tasks):
                    pages.append(page);print(source['id'],page['page'],'/',count,flush=True)
        target.write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
