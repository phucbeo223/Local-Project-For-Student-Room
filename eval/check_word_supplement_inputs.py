"""Check genuine page-to-Word-to-provision fidelity without any DB/model call."""
from pathlib import Path
import hashlib
import json
from docx import Document
from lxml import html

ROOT=Path(__file__).resolve().parents[1]
CAP=ROOT/'eval/provider_sources_20261005/word_supplement_v8'
FOLDER=ROOT/'docs/legal_word_supplement_corpus_v8_20261005'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=json.loads((FOLDER/'manifest.json').read_text(encoding='utf-8'))
 base=json.loads((ROOT/'docs/legal_word_corpus_v7_20261005/manifest.json').read_text(encoding='utf-8'))
 assert manifest['documents'][:16]==base['documents'] and len(manifest['documents'])==30
 checked=[]
 for entry in manifest['documents']:
  path=ROOT/entry['file'];assert sha(path)==entry['sha256']
  value=json.loads(path.read_text(encoding='utf-8'));s=value['source']
  assert s['ocr_used'] is False and sha(ROOT/s['path'])==s['sha256']
  if not s['id'].startswith('supplement-'): continue
  word=Document(ROOT/s['path']);paras=[p.text for p in word.paragraphs if p.text.strip()]
  body='\n\n'.join(paras)
  for p in value['provisions']:
   assert p['content'] in body and hashlib.sha256(p['content'].encode()).hexdigest()==p['content_sha256']
   assert hashlib.sha256(body.encode()).hexdigest()==p['extraction_text_sha256']
  if s['source_content_kind']=='publisher_guidance_word_conversion':
   key=s['id'].split('-')[1].upper();raw=CAP/(key+'.html')
   assert sha(raw)==s['original_html_sha256']
   tree=html.fromstring(raw.read_text(encoding='utf-8-sig'))
   if key=='S14': blocks=[' '.join(e.text_content().split()) for e in tree.xpath('//div[@id="articleContent"]/div') if e.text_content().strip()]
   else:
    for e in tree.xpath('//script|//style|//noscript'): e.drop_tree()
    blocks=[]
    for e in tree.xpath('//h1|//h2|//h3|//h4|//p|//li[not(.//p)]|//td[not(.//p)]'):
     if e.tag=='p' and e.xpath('.//p'): continue
     text=' '.join(e.text_content().split())
     if text: blocks.append(text)
   assert paras==[blocks[i] for i in s['original_block_indices']]
  else: assert sha(ROOT/s['path'])==s['original_sha256']
  checked.append(s['id'])
 print(json.dumps({'passed':True,'unchanged_old_documents':16,'verified_supplements':len(checked),'literal_source_word_provisions':True,'ocr_used':False},ensure_ascii=False))
if __name__=='__main__':main()
