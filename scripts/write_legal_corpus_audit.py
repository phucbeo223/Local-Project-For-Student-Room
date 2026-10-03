"""Generate a source register from hashed corpus metadata, without creating legal text."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
manifest_path=ROOT/'docs/legal_corpus_v2/manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
lines=['# Sổ nguồn kho pháp lý legal_v2','',
       'Được tạo từ manifest và metadata thực tế. Bản gốc lấy từ cơ quan nhà nước hoặc đơn vị cấp nước công khai quyết định có chữ ký; bản OCR/trích cấu trúc do dự án tạo, không phải một bản hợp nhất được Chính phủ phê duyệt.',
       'Không suy ra hiệu lực hiện hành chỉ từ việc tải được tệp. Tài liệu trích tuyển kế thừa chưa được xác nhận từng chữ với toàn văn.',
       '`source_start` và `source_end` là vị trí ký tự trong văn bản trích đã chuẩn hóa, không phải vị trí byte/trang của PDF gốc. Số trang PDF là trang vật lý; nguồn DOC/DOCX/Markdown dùng trang trong bản trích.', '',
       f"Manifest SHA-256: `{hashlib.sha256(manifest_path.read_bytes()).hexdigest()}`.", '',
       '| Tài liệu đầu vào | Chủ đề | Điều đã chọn | Số đơn vị | Nguồn công bố | Cách trích/kiểm chứng |',
       '|---|---|---|---:|---|---|']
for entry in manifest['documents']:
    path=ROOT/entry['file']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
    data=json.loads(path.read_text(encoding='utf-8'));s=data['source']
    articles=', '.join(str(a) for a in entry['articles'] if a is not None) or 'Hướng dẫn/khuyến cáo, không đánh số điều'
    publisher='Đơn vị cấp nước công bố bản ký' if entry['id']=='water215' else 'Cơ quan nhà nước'
    values=[s['title'],entry['category'],articles,str(entry['provisions']),
            f"[{publisher}]({s['source_url']})",s.get('extraction','')+'; '+str(s.get('verification',''))]
    lines.append('| '+' | '.join(v.replace('|','\\|').replace('\n',' ') for v in values)+' |')
lines+=['','## Dấu vết từng nguồn','',
        'SHA đầu vào dưới đây áp dụng cho tệp đầu vào nêu trong metadata. Với bản trích kế thừa, đây là hash bản trích; hash bản gốc được lưu riêng trong manifest tải nguồn và `origin_documents` nếu đã xác thực.', '']
for entry in manifest['documents']:
    s=json.loads((ROOT/entry['file']).read_text(encoding='utf-8'))['source']
    lines +=[f"### {entry['id']}",'',f"- Tệp cấu trúc: `{entry['file']}`.",
             f"- SHA cấu trúc: `{entry['sha256']}`.",f"- Đầu vào: `{s.get('path','')}`.",
             f"- SHA đầu vào: `{s.get('sha256','')}`.",f"- Nguồn: {s['source_url']}"]
    for original in s.get('origin_documents',[]):
        lines.append(f"- Bản gốc đối chiếu: `{original.get('path','')}`; SHA `{original.get('sha256','')}`; {original.get('source_page_url') or original.get('source_url','')}")
    lines.append('')
lines+=['## Tài liệu giữ lại nhưng chưa nạp','']
for excluded in manifest['excluded']:
    lines.append(f"- `{excluded['path']}`: {excluded['reason']}.")
lines +=['','Không xóa tài liệu gốc, bản OCR hoặc bản sao lưu khi loại một nguồn khỏi kho truy xuất.']
(ROOT/'docs/LEGAL_CORPUS_V2_SOURCES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'documents':len(manifest['documents']),'excluded':len(manifest['excluded']),
                  'output':'docs/LEGAL_CORPUS_V2_SOURCES.md'}))
