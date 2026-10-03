"""Audit selected housing recommendations against actual catalog fields; no model calls."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import argparse,hashlib,json,math
from sqlalchemy import create_engine,text
from app.config import settings
from app.room_service.chatbot.providers import normalize_text
from question_bank_ragas import save_report,summarize,METRIC_NAMES

PRESERVED={
 'question_bank_ragas_2026-10-01.json':'7ff5f20d087b4cfcc49c912c9bad0fe917f65d59ac1b6586d4c46fdd3075cb42',
 'legal_agent_local_v15_2026-10-04.json':'deff9af52f6192e129b5e8dd446874ab879472ebd502c815f7c64dc5d7026ea2',
 'legal_agent_after_v10_2026-10-03.json':'a5b3ec7507e4ece633e3bf4469b0575f272e73b4c6ec2e22793996691c2a36ed'}

def criteria(q,r,minimum):
    """Independent explicit numeric/field predicates; vague preferences remain unverified."""
    a=r.get('parsed_amenities') or {};price=r['price'];district=normalize_text(r.get('district') or '')
    if q==1:return price<2_000_000
    if q==2:return 1_500_000<=price<=2_000_000
    if q==3:return price==minimum
    if q==4:return price<=2_500_000
    if q==5:return 'ninh kieu' in district
    if q==6:return 'binh thuy' in district and r.get('distance_to_ctu') is not None and r['distance_to_ctu']<2000
    if q==9:return r.get('area') is not None and r['area']>=20 and a.get('mezzanine') is True
    if q==10:return all(a.get(k) is True for k in ('air_conditioner','wifi','parking'))
    if q==11:return all(a.get(k) is True for k in ('private_bathroom','flexible_hours'))
    return None

LABELS={1:'Giá < 2 triệu; gần trường chưa có ngưỡng',2:'Giá từ 1,5 đến 2 triệu',
 3:'Giá thấp nhất trong các phòng đủ điều kiện truy xuất; chưa xác minh còn phòng',4:'Giá ≤ 2,5 triệu',
 5:'Ninh Kiều',6:'Bình Thủy và chim bay < 2 km; chưa xác minh tuyến đường',
 7:'Gần khu II / thuận tiện: chưa có ngưỡng và dữ liệu tuyến đường',
 8:'Gần 3/2 hoặc Xuân Khánh: chưa có ranh giới/vị trí tham chiếu chính xác',
 9:'Diện tích ≥ 20 m² + gác theo trường có cấu trúc',10:'Máy lạnh + Wi-Fi + đỗ xe theo nguồn',
 11:'WC riêng + giờ tự do theo nguồn',12:'Ở ghép hai sinh viên: chưa có trường sức chứa / xác nhận chủ trọ'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True)
    p.add_argument('--import-report',type=Path,default=Path('/eval/reports/housing_import_2026-10-04.json'))
    p.add_argument('--output',type=Path,default=Path('/eval/reports/housing_audit_2026-10-04.json'))
    p.add_argument('--markdown',type=Path,default=Path('/eval/ragas_reports/housing_evaluation_2026-10-04.md'));a=p.parse_args()
    report=json.loads(a.input.read_text(encoding='utf-8'));summarize(report)
    engine=create_engine(settings.database_url)
    with engine.connect() as c:
        rows=[dict(r) for r in c.execute(text('SELECT id,price,area,district,address,title,description,parsed_amenities,distance_to_ctu,status,cleaning_status,listing_type FROM housing_v2.aggregated_listings')).mappings()]
    engine.dispose();byid={r['id']:r for r in rows}
    eligible=[r for r in rows if r['status']=='active' and r['cleaning_status']=='cleaned' and r['listing_type']=='phong_tro']
    minimum=min(r['price'] for r in eligible);checks=[]
    for case in report['cases']:
        number=case['id'];ids=case.get('listing_ids',[]);returned=[byid[i] for i in ids if i in byid]
        hard=number in (1,2,3,4,5,6,9,10,11)
        checked=returned[:1] if number==3 else returned
        valid=sum(criteria(number,r,minimum) is True for r in checked) if hard else None
        candidates=sum(criteria(number,r,minimum) is True for r in eligible) if hard else None
        issues=[]
        if any(i not in byid for i in ids):issues.append('ID trả về không thuộc kho đã nạp')
        if any(r not in eligible for r in returned):issues.append('Tin trả về không đủ điều kiện truy xuất phòng trọ thông thường')
        if hard and valid!=len(checked):issues.append('Gợi ý không khớp điều kiện giá/trường dữ liệu đã hỏi')
        ascending=not any(x['price']>y['price'] for x,y in zip(returned,returned[1:]))
        if number==3 and not ascending:issues.append('Danh sách giá chưa sắp xếp tăng dần')
        if hard and candidates and not returned:issues.append('Có tin khớp trường dữ liệu nhưng không trả kết quả')
        if number in (1,7,8,12):issues.append('Nhu cầu về vị trí/sức chứa cần xác minh thêm; audit chưa chứng minh toàn bộ câu hỏi')
        if number==3:issues.append('Active là trạng thái lập chỉ mục; chưa xác minh nguồn còn tin hoặc còn phòng')
        if number==9 and candidates==0:issues.append('Chưa có trường gác lửng trong parsed amenities; mô tả nguồn có thể có chứng cứ chưa trích')
        if number in (7,8,12) and case.get('no_answer') and case.get('confidence',0)>0:
            issues.append(f"Ứng viên bị chặn: confidence {case['confidence']} < {settings.chatbot_confidence_threshold}; chưa thể kết luận thiếu nguồn")
        if not case.get('contexts'):issues.append('RAGAS N/A: không có ngữ cảnh truy xuất, không gán điểm 0')
        checks.append({'id':number,'question':case['question'],'criterion':LABELS.get(number,'Selected housing question'),
            'returned':len(ids),'candidate_matches':candidates,'explicit_field_matches':valid,
            'field_check':'pass' if hard and ids and valid==len(checked) and not any(i not in byid for i in ids) and (number!=3 or ascending) else 'no_matching_data' if hard and candidates==0 and not ids else 'fail' if hard else 'requires_verification',
            'no_answer':case.get('no_answer'),'generation_provider':case.get('generation_provider'),
            'confidence':case.get('confidence'),'confidence_threshold':settings.chatbot_confidence_threshold,
            'qwen_calls':sum(x.get('provider') in ('qwen-local','ollama') and x.get('success') and x.get('method')=='generate' for x in case.get('provider_calls',[])),
            'degraded_reasons':case.get('degraded_reasons',[]),'citation_format_accuracy':case.get('citation_accuracy'),
            'execution_error':case.get('error'),'ragas':case.get('ragas',{}),'issues':issues})
    preserved={}
    for name,digest in PRESERVED.items():
        current=hashlib.sha256((a.input.parent/name).read_bytes()).hexdigest()
        preserved[name]={'sha256':current,'unchanged':current==digest}
    if not all(x['unchanged'] for x in preserved.values()):raise ValueError('An immutable prior report changed')
    status_path=a.input.with_suffix('.status.json');status=json.loads(status_path.read_text(encoding='utf-8')) if status_path.exists() else {}
    imported=json.loads(a.import_report.read_text(encoding='utf-8'))
    summary={'created_at_utc':datetime.now(timezone.utc).isoformat(),'selection':report['selected_original_ids'],
        'skipped_original_ids':[i for i in range(1,59) if i not in report['selected_original_ids']],
        'import':imported,'evaluation_summary':report['summary'],'field_checks':checks,'preserved_reports':preserved,
        'native_job':{'phase':status.get('phase'),'quota':status.get('quota') or report.get('quota_state')},
        'payload_policy':'Raw ads, source contexts, answers and package stay local and ignored by Git; report contains counts and test questions only',
        'comparison':'New corpus and exact model-visible clipped listing JSON; historical housing metrics are not directly comparable; no old or Qwen-judge metrics copied'}
    save_report(a.output,summary)
    counts=imported['counts'];s=report['summary'];lines=['# Nạp dữ liệu nhà trọ và kiểm thử 12 câu — 04/10/2026','',
        f"- Kho riêng `{imported['schema']}`: **{counts['rows']} tin / {counts['vectors']} vector E5**; {counts['eligible']} tin đủ điều kiện rental chung. Truy vấn phòng trọ chỉ lấy `phong_tro` ({len(eligible)} tin).",
        f"- Chọn câu **{', '.join(map(str,report['selected_original_ids']))}** trong bộ 58. Các câu khác được bỏ qua; SHA của ba báo cáo cũ đã kiểm tra không đổi.",
        f"- Đã thu câu trả lời **{s['completed']}/{s['questions']}**; lỗi thực thi **{s['errors']}**; có ngữ cảnh **{s['with_contexts']}**; không trả lời **{s['no_answer']}**; suy giảm **{s['degraded']}**.",
        f"- Trạng thái chấm native: **{status.get('phase','collection completed; scoring not started')}**.",'',
        '## Metrics RAGAS','', '| Metric | Số câu có điểm | Trung bình |','|---|---:|---:|']
    for m in METRIC_NAMES:
        v=s['ragas'][m];lines.append(f"| {m} | {v['scored']} | {v['mean'] if v['mean'] is not None else 'Chưa có'} |")
    quota=status.get('quota') or report.get('quota_state')
    if status.get('phase')=='awaiting_payload_authorization':
        lines+=['','**Chưa chạy worker Gemini cho dữ liệu nhà trọ.** Bộ duyệt tự động từ chối vì quyền gửi dữ liệu trước đó chỉ bao gồm nội dung pháp lý. Đang đợi người dùng cho phép gửi 12 câu hỏi, câu trả lời và các đoạn tin trọ có thể chứa thông tin cá nhân sang Gemini. Không dùng heartbeat/lệnh khác để vượt chặn; báo cáo và kiểm tra trường dữ liệu local đã hoàn tất.']
    if quota:
        vn=datetime.fromisoformat(quota['retry_at_utc']).astimezone(timezone(timedelta(hours=7)))
        lines+=['',f"Checkpoint giữ nguyên câu trả lời/điểm đã có. Mốc thử lại quota là **{vn:%d/%m/%Y %H:%M:%S} (Việt Nam)**. Khi worker được phép chạy, nó đợi mốc này rồi thăm dò server; nếu tiếp tục 429 sẽ lưu mốc nghỉ mới. Chưa khẳng định server đã hồi."]
    lines+=['','Gemini `gemini-3.1-flash-lite` là bộ chấm native; Qwen `qwen3.5:9b` trả lời local. Không đưa điểm bộ chấm Qwen vào ô Gemini. Không có ngữ cảnh thì metric N/A, không gán 0; chưa có đáp án chuẩn độc lập nên không báo answer correctness/context recall.',
        '', '## Kiểm tra từng câu', '', '| Câu | Tin trả về | Tin khớp trong kho | Kiểm tra trường | Lưu ý |','|---|---:|---:|---|---|']
    labels={'pass':'Khớp trường','no_matching_data':'Không có tin khớp trường','fail':'Chưa đạt','requires_verification':'Cần xác minh'}
    for x in checks:lines.append(f"| {x['id']} | {x['returned']} | {x['candidate_matches'] if x['candidate_matches'] is not None else 'Chưa xác định'} | {labels[x['field_check']]} | {'; '.join(x['issues']) or 'Khớp các điều kiện có cấu trúc'} |")
    lines+=['','## Provider và kiểm tra câu trả lời','', '| Câu | Provider cuối | Lượt Qwen thành công | Cảnh báo / hạ xuống mẫu |','|---|---|---:|---|']
    for x in checks:lines.append(f"| {x['id']} | {x['generation_provider'] or 'Chưa chạy'} | {x['qwen_calls']} | {'; '.join(x['degraded_reasons']) or x['execution_error'] or 'Không'} |")
    lines+=['','## Giới hạn dữ liệu và việc cần bổ sung','',
        f"- Diện tích có ở {counts['areas']}/789 tin; thời gian nguồn có ở {counts['source_timestamps']}/789; {counts['approximate_distances']} khoảng cách là đường chim bay tính từ tọa độ gần đúng. Không phải khoảng cách đi đường / thời gian đi học.",
        '- Giữ nguyên thiếu diện tích, thời gian, đánh giá rủi ro. Giá là giá quảng cáo; kỳ thu, phòng còn trống và tiện ích chưa được xác nhận thực tế. `active`/`cleaned` chỉ biểu thị trạng thái nạp có kiểm tra, không bảo đảm tin còn hiệu lực.',
        '- Alias WC riêng/giờ tự do/tủ lạnh được chuẩn hóa; không tự tạo tiện ích chưa được xác nhận trong trường có cấu trúc. Gác lửng chưa có trường parsed, cần trích chứng cứ từ mô tả trước khi kết luận câu 9 thiếu nguồn.',
        '- Câu 1/7 cần ngưỡng gần trường và thông tin tuyến đường; câu 8 cần vị trí tham chiếu/radius, câu 12 cần sức chứa / sự đồng ý ở ghép của chủ trọ. Kiểm tra giá đúng chưa đủ chứng minh đúng toàn bộ nhu cầu.',
        '- Nếu có ứng viên nhưng confidence thấp hơn ngưỡng 0,65, chatbot sẽ bỏ kết quả. Đây là vấn đề truy xuất/hiệu chỉnh confidence cần rà riêng, không phải bằng chứng nguồn không có phòng.',
        '- Dữ liệu cung cấp chỉ dùng nội bộ, quyền tái phát hành chưa xác định. Gói nguồn và payload đánh giá không đưa lên GitHub. Dữ liệu `public` cũ được kiểm tra fingerprint không đổi; chưa thay kho đang phục vụ chính thức trước khi xét kết quả.',
        '- Bộ cũ dùng dữ liệu và ngữ cảnh khác. Đợt này dùng đúng JSON/độ cắt mô tả mà Qwen nhìn thấy; chưa thể kết luận điểm tăng hay giảm bằng cách ghép trung bình cũ/mới.',
        '',f"Catalog SHA256: `{imported['catalog_sha256']}`."]
    a.markdown.parent.mkdir(parents=True,exist_ok=True);a.markdown.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'summary':s,'checks':[(x['id'],x['field_check']) for x in checks],'phase':status.get('phase'),'report':str(a.markdown)},ensure_ascii=False))

if __name__=='__main__':main()
