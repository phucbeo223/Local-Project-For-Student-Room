"""Import the supplied sealed catalog into an isolated, resumable local corpus."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, sys
from sqlalchemy import create_engine, text
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'apps/api'))
from app.config import settings
from app.room_service.chatbot.providers import E5EmbeddingProvider, normalize_text
from app.crawler.geocode import CTU_LAT, CTU_LNG, haversine_m

SCHEMA='housing_v2'
ALIASES={'free_hours':'flexible_hours','private_wc':'private_bathroom','fridge':'refrigerator'}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(conn):
    return dict(conn.execute(text("SELECT count(*) AS rows,count(embedding_vector) AS vectors, "
        "md5(string_agg(id::text||coalesce(content_hash,'')||coalesce(embedding_vector::text,''),'|' ORDER BY id)) AS digest "
        "FROM public.aggregated_listings")).mappings().one())

def prepare(r):
    if not isinstance(r['id'],int) or not r.get('title') or r['source']!='chotot':raise ValueError('Invalid source record')
    if not isinstance(r.get('price'),int) or r['price']<=0:raise ValueError('Missing/invalid price; do not impute')
    if r.get('area') is not None and (not math.isfinite(r['area']) or r['area']<=0):raise ValueError('Invalid area')
    amenities={ALIASES.get(k,k):v for k,v in (r.get('parsed_amenities') or {}).items()}
    district=r.get('district')
    if district and normalize_text(district)=='quan binh thuy':district='Quận Bình Thủy'
    lat,lng=r.get('latitude'),r.get('longitude')
    distance=None
    if lat is not None and lng is not None:
        if not all(math.isfinite(x) for x in (lat,lng)) or not(-90<=lat<=90 and -180<=lng<=180):raise ValueError('Invalid coordinates')
        distance=haversine_m(lat,lng,CTU_LAT,CTU_LNG)
    eligible=r.get('housing_type') in ('room','mini_house','studio') and r.get('offer_kind')=='rental' and not r.get('offer_context_uncertain')
    notes=['Thông tin quảng cáo theo nguồn; chưa xác minh còn phòng, kỳ thu giá hoặc tiện ích.',
           'Diện tích thiếu là chưa biết, không tự điền. Loại chỗ ở theo tin: '+str(r.get('housing_type'))+'.']
    if distance is not None:notes.append(f'Khoảng cách đường chim bay ước tính đến cổng khu II CTU: {distance/1000:.3f} km; tọa độ gần đúng, chưa đo tuyến đường.')
    if r.get('description_is_partial'):notes.append('Mô tả đã bỏ một phần liên hệ; xem nguồn để đối chiếu nội dung đầy đủ.')
    if r.get('description_state')=='WITHHELD_UNSAFE_CONTACT':notes.append('Mô tả gốc bị giữ lại, không suy ra nguồn không có nội dung.')
    description='\n'.join(notes)+'\n'+(r.get('description') or '')
    return {'id':r['id'],'title':r['title'],'price':r['price'],'area':r.get('area'),
        'address':r.get('address'),'district':district,'images':r.get('images') or [],
        'description':description,'source':r['source'],'source_id':r['source_id'],'source_url':r['source_url'],
        'amenities':json.dumps(amenities,ensure_ascii=False),'lat':lat,'lng':lng,'distance':distance,
        'geocode_confidence':r.get('geocode_confidence'),'first_seen':r.get('first_seen'),'last_seen':r.get('last_seen'),
        'listing_type':r['listing_type'],'quality_score':r.get('quality_score'),
        'status':'active' if eligible else 'flagged','raw':json.dumps(r,ensure_ascii=False),
        'row_sha':hashlib.sha256(json.dumps(r,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()}

def main():
    global SCHEMA
    p=argparse.ArgumentParser();p.add_argument('--catalog-dir',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
    p.add_argument('--schema',default=SCHEMA);a=p.parse_args()
    import re
    if not re.fullmatch(r'housing_[a-z0-9_]{1,48}',a.schema):raise ValueError('Invalid isolated housing schema')
    SCHEMA=a.schema
    catalog=a.catalog_dir/'CATALOG.jsonl';rows=[json.loads(l) for l in catalog.read_text(encoding='utf-8').splitlines()]
    source_manifest=json.loads((a.catalog_dir.parent/'SOURCE_MANIFEST.json').read_text(encoding='utf-8'))
    assert sha(catalog)==source_manifest['files']['CATALOG.jsonl']
    assert len(rows)==789 and len({r['id'] for r in rows})==789 and len({r['source_id'] for r in rows})==789
    records=[prepare(r) for r in rows];digest=sha(catalog)
    engine=create_engine(settings.database_url)
    with engine.begin() as c:
        before=snapshot(c)
        c.execute(text(f'CREATE SCHEMA IF NOT EXISTS {SCHEMA}'))
        c.execute(text(f'CREATE TABLE IF NOT EXISTS {SCHEMA}.aggregated_listings (LIKE public.aggregated_listings INCLUDING ALL)'))
        c.execute(text(f'CREATE TABLE IF NOT EXISTS {SCHEMA}.catalog_records (id integer PRIMARY KEY,source_record jsonb NOT NULL,row_sha256 text NOT NULL)'))
        c.execute(text(f'CREATE TABLE IF NOT EXISTS {SCHEMA}.release (id integer PRIMARY KEY CHECK(id=1),catalog_sha256 text NOT NULL,imported_at timestamptz NOT NULL)'))
        old=c.execute(text(f'SELECT catalog_sha256 FROM {SCHEMA}.release WHERE id=1')).scalar_one_or_none()
        if old and old!=digest:raise ValueError('Different catalog already loaded; use a new schema/version')
        if not old:
            assert c.execute(text(f'SELECT count(*) FROM {SCHEMA}.aggregated_listings')).scalar_one()==0
            for r in records:
                c.execute(text(f'INSERT INTO {SCHEMA}.catalog_records VALUES(:id,CAST(:raw AS jsonb),:row_sha)'),r)
                c.execute(text(f"INSERT INTO {SCHEMA}.aggregated_listings "
                    "(id,title,price,area,address,district,images,description,source,source_id,source_url,parsed_amenities,geom,distance_to_ctu,geocode_confidence,first_seen,last_seen,listing_type,quality_score,status,cleaning_status,risk_score,risk_status,freshness_score,updated_at) "
                    "VALUES(:id,:title,:price,:area,:address,:district,:images,:description,:source,:source_id,:source_url,CAST(:amenities AS jsonb),CASE WHEN CAST(:lat AS double precision) IS NULL THEN NULL ELSE ST_SetSRID(ST_MakePoint(CAST(:lng AS double precision),CAST(:lat AS double precision)),4326) END,:distance,:geocode_confidence,:first_seen,:last_seen,CAST(:listing_type AS public.listing_type_enum),:quality_score,CAST(:status AS public.listing_status),'cleaned',NULL,'unknown',NULL,NULL)"),r)
            c.execute(text(f'INSERT INTO {SCHEMA}.release VALUES(1,:sha,now())'),{'sha':digest})
    # E5 only; no fabricated vectors. Resume only missing vectors.
    embedder=E5EmbeddingProvider(settings.chatbot_embedding_model);embedder.warmup()
    with engine.connect() as c:
        todo=[dict(r) for r in c.execute(text(f'SELECT id,title,description,address,district,price,area,parsed_amenities FROM {SCHEMA}.aggregated_listings WHERE embedding_vector IS NULL ORDER BY id')).mappings()]
    for start in range(0,len(todo),16):
        batch=todo[start:start+16];texts=[' | '.join(str(r.get(k) or '') for k in ('title','description','address','district','price','area','parsed_amenities')) for r in batch]
        vectors=embedder.embed_passages(texts)
        with engine.begin() as c:
            for r,content,v in zip(batch,texts,vectors):
                assert len(v)==384 and all(math.isfinite(x) for x in v)
                c.execute(text(f'UPDATE {SCHEMA}.aggregated_listings SET embedding_vector=CAST(:v AS public.vector),embedding_model=:model,embedded_content_hash=:sha,embedded_at=now() WHERE id=:id'),
                    {'id':r['id'],'v':'['+','.join(f'{x:.9g}' for x in v)+']','model':settings.chatbot_embedding_model,'sha':hashlib.sha256(content.encode()).hexdigest()})
        print(f'Embedded {min(start+16,len(todo))}/{len(todo)} missing records',flush=True)
    with engine.connect() as c:
        after=snapshot(c);assert before==after,'Original public listings changed'
        counts=dict(c.execute(text(f"SELECT count(*) AS rows,count(embedding_vector) AS vectors,count(area) AS areas,count(distance_to_ctu) AS approximate_distances,count(last_seen) AS source_timestamps,count(*) FILTER(WHERE status='active') AS eligible FROM {SCHEMA}.aggregated_listings")).mappings().one())
        assert counts['rows']==counts['vectors']==789
    report={'created_at_utc':datetime.now(timezone.utc).isoformat(),'schema':SCHEMA,'catalog_sha256':digest,'counts':counts,'original_before':before,'original_after':after,
        'scope':'internal development and evaluation; source rights unverified; no public publication',
        'normalization':'amenity aliases only; Bình Thuỷ spelling normalized; missing area/time/risk unchanged; no vacancy or monthly-price verification',
        'cleaning_status_meaning':'validated import of supplied retained text; not physical/source verification or full production cleaner certification',
        'distance_method':{'kind':'approximate haversine; not route distance','ctu_khu_II':[CTU_LAT,CTU_LNG]},'unknown_or_transfer_offers':'retained flagged, excluded from ordinary rental recommendations','embedding_model':settings.chatbot_embedding_model}
    a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False),flush=True);engine.dispose()

if __name__=='__main__':main()
