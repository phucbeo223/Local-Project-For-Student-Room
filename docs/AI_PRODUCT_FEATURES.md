# Phạm vi chức năng AI và nghiệp vụ đã triển khai

Tài liệu này là bản bàn giao cho phần việc không thuộc crawler. Các endpoint nhận dữ liệu listing đã có; không sửa nguồn crawl, selector, lịch crawl hoặc logic thu thập.

## Chức năng hoàn thành

| Nhóm | Chức năng | Backend/UI | Trạng thái khoa học |
|---|---|---|---|
| Chatbot | Hybrid structured + lexical + pgvector, tối đa 5 nguồn, fallback Qwen → Gemini → template | `/chat/ask`, widget toàn site | Có RAGAS runner end-to-end |
| Chatbot | Đa lượt ngắn ở client, query rewrite, feedback 👍/👎 | history tối đa 5 lượt; `/chat/feedback` | Không lưu nội dung hội thoại |
| Chatbot | Telemetry, no-answer/degraded/citation, p95 latency | `chatbot_events`, dashboard AI | Chỉ lưu aggregate, không lưu prompt |
| Risk | Rule score có lý do, trạng thái chưa đánh giá tách khỏi “an toàn” | `/risk/*`, badge listing | Model version `room-risk-rules-v2` |
| Risk | Lịch sử đánh giá và admin override có ghi người/lý do | history + override endpoint/UI | Có audit trail |
| UGC | Validate dữ liệu, geocode cũ bị xóa khi đổi địa chỉ, tự chấm risk | create/update listing | UGC nghi ngờ chuyển `flagged` chờ admin |
| Người dùng | Yêu thích, so sánh tối đa 4, ghi interaction | `/favorites`, `/compare` | Tạo tín hiệu implicit có trọng số |
| Gợi ý | Cold-start + content/implicit preference, phạt risk, giải thích lý do | `/recommendations` | Chưa tuyên bố accuracy khi thiếu nhãn thật |
| Tìm kiếm | Lưu bộ lọc và đối chiếu tin mới | `/saved-searches`, `/notifications` | Refresh theo yêu cầu; sẵn hook cho pipeline khác gọi |
| Quản trị | Dashboard chatbot/risk/product và lưu evaluation run | `/admin/ai` | Theo dõi model/dataset/prompt version |
| Dữ liệu nghiên cứu | 1.000 listing + 200 Q&A deterministic, versioned | generator + metadata | Chỉ dùng dev/mô phỏng |

## Luồng nghiệp vụ chính

1. Người dùng tìm/xem/lưu tin; interaction được ghi với tài khoản đăng nhập.
2. Recommendation tổng hợp mức giá, quận và tiện ích từ tín hiệu dương; `dismiss` loại tin, risk cao bị giảm hạng; cold-start dùng quality/freshness/risk.
3. Người dùng lưu bộ lọc. Trang thông báo đối chiếu các listing thay đổi sau lần kiểm tra trước và chống tạo thông báo trùng.
4. Tin UGC được validate, định vị lại và risk assess. Tin mức `suspicious` chuyển `flagged`, admin xem xét và có thể override; mọi lần đánh giá/override có lịch sử.
5. Chatbot parse yêu cầu, retrieval dữ liệu thật, chỉ cho LLM dùng context và yêu cầu citation `[1]`–`[5]`. Khi embedding hoặc LLM lỗi, response công khai `degraded=true` thay vì che giấu.
6. Admin theo dõi tỷ lệ no-answer, degraded, feedback dương, latency, risk chưa chấm và evaluation run mới nhất.

## Những việc cố ý chưa “bịa kết quả”

- Chưa huấn luyện Isolation Forest: cần đủ dữ liệu thật và split độc lập; train trên dữ liệu giả sinh theo chính rule sẽ không có giá trị khoa học.
- Chưa công bố recall risk hay NDCG recommendation: runner đã có nhưng yêu cầu nhãn thủ công/survey/held-out.
- Chưa tự động phát thông báo theo cron: đó là điểm tích hợp của bộ phận ingestion/crawler; hiện người dùng có thể refresh an toàn theo yêu cầu.
- Không coi `risk_score=0` hoặc chưa chấm là an toàn; trạng thái `not_evaluated` được hiển thị riêng.

## Triển khai database

Khởi động toàn bộ hệ thống nghiên cứu trên Windows bằng một lệnh (crawler bị tắt,
migration được áp cả với volume cũ, dữ liệu ảo được upsert lặp an toàn):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start_all.ps1
```

Lần chạy lại nhanh, không build image và không nạp lại seed:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start_all.ps1 -SkipBuild -SkipSeed
```

Với database đang có, áp migration không xóa volume:

```powershell
docker compose up -d db
& .\.venv\Scripts\python.exe scripts\apply_room_services.py
```

Script áp tuần tự migration 90–96, gồm chatbot/risk, kiểm duyệt, kho pháp lý,
vòng đời tài khoản và đánh giá cảm xúc. Database mới cũng tự áp 90–96 từ image.

## Kiểm chứng

```powershell
& .\.venv\Scripts\python.exe scripts\generate_fake_listings.py --seed 2026
& .\.venv\Scripts\python.exe -m pytest apps\api\tests\test_chatbot.py apps\api\tests\test_chatbot_dataset.py apps\api\tests\test_risk.py apps\api\tests\test_engagement.py -q
& .\.venv\Scripts\python.exe eval\chatbot_eval.py
Set-Location apps\web
npx tsc --noEmit --incremental false
```

Phương pháp và nguồn nghiên cứu được ghi tại `eval/README.md`; nguồn cốt lõi là RAGAS/ARES cho RAG evaluation, NDCG cho ranked retrieval, implicit feedback cho recommendation và NIST AI RMF cho provenance/TEVV.
