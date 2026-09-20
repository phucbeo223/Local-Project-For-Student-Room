# Vận hành Docker local

Triển khai ngày 20/09/2026 trên Docker Desktop; chỉ truy cập từ máy hiện tại,
chưa phải cấu hình production/public.

## Địa chỉ

- Website: http://localhost:3000
- API / Swagger: http://localhost:8000/docs
- Hộp thư thử nghiệm: http://localhost:8025
- PostgreSQL và Redis chỉ mở trong mạng Docker, không publish cổng Windows.

Mailpit nhận OTP và liên kết reset của mọi địa chỉ email nhập trên website,
**không gửi ra email thật**. Không dùng mật khẩu thật để thử nghiệm. Hộp thư
Mailpit hiện không lưu bền qua lần recreate container; xin OTP mới nếu cần.
Google login chưa được bật vì chưa có Google client ID.

## Khởi động / dừng

Chạy PowerShell tại thư mục gốc dự án, bật Docker Desktop trước:

```powershell
docker compose up -d
docker compose ps
docker compose logs --tail 50 api web
docker compose stop
```

`stop` giữ container và volume. Không dùng `down -v`, `volume rm`, hay reset/seed
database đang có. `restart: unless-stopped` tự chạy lại dịch vụ theo Docker
Engine, trừ dịch vụ đã bị dừng thủ công.

Cấu hình riêng máy này nằm trong `docker-compose.override.yml` (đã ignore Git).
File mẫu không chứa secret: `docker-compose.local.example.yml`. Khi cài máy
mới, chỉ copy mẫu nếu chưa có override của riêng bạn; Docker Compose phải hỗ
trợ `!override` (2.24.4 trở lên). `.env` phải được cấu hình riêng, không commit.

```powershell
if (-not (Test-Path docker-compose.override.yml)) {
    Copy-Item docker-compose.local.example.yml docker-compose.override.yml
}
docker compose build api web
docker compose up -d
```

## Dữ liệu và migration

- Volume `nckh_pgdata` được giữ nguyên.
- Đã áp dụng migration 94 và 95 trong một transaction.
- Trước nâng cấp: 1.125 tin trọ, 74 tài khoản.
- Bản sao lưu custom-format, đã kiểm tra bằng `pg_restore -l`:
  `backups/pre-deploy-20260920-114438.dump` (290.009 byte).
- Bản sao lưu chứa dữ liệu riêng tư, nằm ngoài Git. Không restore đè database
  đang chạy nếu chưa kiểm tra và chưa được chủ dữ liệu đồng ý.
- Smoke test tạo thêm một tài khoản `deploy-smoke-…@example.com`, không sửa
  tài khoản cũ. Không in/lưu mật khẩu, OTP hoặc token của tài khoản này.
  Tài khoản thử lần triển khai này có ID 177; tổng tài khoản sau kiểm tra là 75.

Database có volume cũ không tự chạy migration mới trong entrypoint. Với lần
nâng cấp sau, backup trước rồi dùng `scripts/start_all.ps1 -SkipSeed` hoặc
`scripts/apply_room_services.py`; các script này áp cả migration 95 và 96.
Không chạy seed lại.

## Chỉ mục AI

API được build với `INSTALL_ML=true`, E5 CPU thật 384 chiều. Mô hình được lưu
bền trong `nckh_chat-model-cache`, chia sẻ với legal-indexer. Đã lập chỉ mục
915 tin có `status=active` và `cleaning_status=cleaned`; các tin khác không sửa.

Lập lại embedding tin khi nội dung thay đổi (script hiện tính lại toàn bộ tin
đủ điều kiện; cần chờ hoàn tất, lần đầu tải mô hình cần mạng):

```powershell
docker compose cp scripts api:/app/scripts
docker compose exec -T api python -c "import os,sys,runpy; sys.path.insert(0,'/app/scripts'); sys.argv=['index_listing_embeddings.py','--database-url',os.environ['DATABASE_URL'],'--batch-size','16']; runpy.run_path('/app/scripts/index_listing_embeddings.py',run_name='__main__')"
```

Nhập tài liệu `Data` bằng worker riêng (không bật crawler FR3):

```powershell
docker compose --profile tools build legal-indexer
docker compose --profile tools run --rm --no-deps legal-indexer --data-dir /data --no-apply-migration --batch-size 8
```

Worker có OCR tiếng Việt và tiếng Anh; chỉ đọc file gốc, lưu văn bản/chunk/vector
vào database. Script bỏ qua tài liệu có hash không đổi. Việc nhập thành công
không xác nhận tài liệu còn hiệu lực pháp luật; nhóm phụ trách phải kiểm duyệt
nguồn trước khi dùng để tư vấn thực tế.

Kết quả xác nhận ngày 20/09/2026: **26/26 tài liệu ready, 2.497 chunk đều có
embedding, 0 tài liệu failed**. Chạy lại worker cho kết quả `26 unchanged`,
không nhập trùng. Riêng `housing_contract/2026_204_79_VBHN-VPQH.docx` từng báo
không hợp lệ vì tên ZIP member là `word\document.xml`. Bộ đọc đã hỗ trợ cả
hai dấu phân cách, kiểm tra đúng một document part và vẫn từ chối ZIP/XML
hỏng hoặc nội dung trùng đường dẫn. File gốc không sửa; SHA-256 giữ nguyên:
`57889200d36ccd995b62bac71b0195984b66d85a73036561e249b946bda841b9`.
Tài liệu này tạo 269 chunk. Bản sửa đã build vào image API/legal-indexer;
152 kiểm thử backend đạt trên stack database tạm tách biệt.

## Kiểm tra

```powershell
Invoke-RestMethod http://localhost:8000/health/deps
Invoke-RestMethod http://localhost:8000/health/ai
docker compose cp scripts api:/app/scripts
docker compose exec -T api python -u /app/scripts/smoke_local_deployment.py --create-test-account --chat
```

Smoke test là thao tác **có ghi dữ liệu**, mỗi lần tạo một tài khoản thử và
một lượt chat nếu thêm `--chat`. Kiểm tra web, OTP, cookie, tìm kiếm, trang
gợi ý/bản đồ/so sánh/chat, reset mật khẩu, thu hồi phiên và logout. Không xóa
dữ liệu thử tự động. Bỏ `--chat` nếu không muốn gọi nhà cung cấp LLM.

`/health/ai` chỉ báo cấu hình, không chứng minh LLM sinh câu trả lời thành công.
Lần smoke test triển khai: hybrid retrieval trả 5 tin/5 nguồn; Gemini hết thời
gian 4 giây nên dùng template dự phòng. API liệt kê model Gemini đã trả HTTP
200 và xác nhận model cấu hình tồn tại. Không tăng timeout để che lỗi SLA.
Lần hỏi đầu sau restart còn tải model vào RAM (~16–17 giây); lần đã nóng đo
được 4.185 ms, vẫn fallback template. Chưa xác nhận Gemini sinh câu trả lời
thành công trong cấu hình timeout này.

Đã kiểm tra thêm: lưu quiz qua web, 10 gợi ý thỏa ngân sách 3 triệu/khoảng cách
5 km, tìm kiếm theo giá/diện tích, chi tiết và so sánh phòng. Risk preview chạy
không ghi dữ liệu; tin thử báo `insufficient_cohort` cho phần thống kê, không
phải lỗi dịch vụ nhưng cũng không phải kết quả IsolationForest đã huấn luyện.

## Qwen3.5 4B chạy local

Trên máy Windows có Ollama đang mở:

```powershell
ollama pull qwen3.5:4b
ollama list
```

Override local chọn `CHATBOT_LLM_PROVIDER=qwen`, `OLLAMA_MODEL=qwen3.5:4b`,
`CHATBOT_LLM_TIMEOUT_SECONDS=60` và `OLLAMA_CONTEXT_LENGTH=8192`.
API Docker gọi `http://host.docker.internal:11434`; Ollama chạy trên Windows,
không cần cấp GPU cho container API. Không mở cổng Ollama ra Internet.
Chế độ này không gọi Gemini; khi Ollama lỗi, dùng mẫu theo nguồn và báo dự phòng.
Giữ nguyên model embedding E5 và chỉ mục hiện có, không cần nhập lại tài liệu.

Request local đặt `think=false`, giới hạn đầu ra 700 token, giữ model 10 phút.
8.192 token dành cho các trích đoạn tiếng Việt; cần đo lại VRAM nếu tăng context.
Nếu chạm giới hạn đầu ra, hệ thống không dùng câu trả lời bị cắt làm kết luận.
60 giây là giới hạn chờ demo local, **không phải cam kết đạt SLA 4 giây**.
Chất lượng trích dẫn số không chứng minh kết luận pháp lý đúng: luôn đối chiếu nguồn.

Máy triển khai: Ryzen 5 7535HS, RAM 16 GB, RTX 4050 Laptop 6 GB.
Đóng bớt ứng dụng khi thiếu RAM. Ollama nhận GPU qua Vulkan; driver NVIDIA
528.83 cần được người dùng cập nhật riêng để kiểm tra CUDA với bản Ollama mới.
Không tự động cập nhật driver hay dừng ứng dụng của người dùng.

Sau khi sửa cấu hình/code:

```powershell
docker compose build api web
docker compose up -d --wait api web
ollama ps
```

Kiểm tra thực sự bằng câu hỏi trong `/chat`: dòng AI phải là
`Qwen local · qwen3.5:4b`, không phải `Mẫu trả lời an toàn`.
Giao diện chia đoạn/gạch đầu dòng, giữ toàn văn sau nút mở rộng và thu gọn nguồn.
Bấm `[1]` để mở nguồn; bấm `Đọc trích đoạn` để xem nội dung đối chiếu.

Kiểm thử hồi quy độc lập và giao diện (web Docker phải đang chạy bản mới):

```powershell
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from api
cd apps/web
npx playwright test e2e/chat.spec.ts --workers=1
```

Test giao diện trên dùng response giả lập để kiểm tra trình bày; không thay thế
smoke test model thật. Không chạy bộ test database trực tiếp trên dữ liệu local.

Smoke test model thật qua trình duyệt (đăng nhập tài khoản sinh viên demo,
ghi metric của hai lượt chat, không sửa phòng/tài liệu):

```powershell
# Chạy trong apps/web, sau khi web/API đã sẵn sàng.
$env:QWEN_SMOKE = '1'
npx playwright test e2e/chat.spec.ts e2e/chat-local-model.spec.ts --workers=1 --reporter=line
```

Có thể đặt `E2E_EMAIL`/`E2E_PASSWORD` cho tài khoản thử riêng.
Không in token đăng nhập. Bộ test xác nhận model thực sự sinh câu trả lời,
nguồn hợp lệ, không fallback, xem/thu gọn nội dung, trích dẫn trong chữ in đậm,
HTML không được thực thi, màn hình 390/1280 px và hội thoại tiếp nối.
Nó không thay thế đánh giá độ đúng nội dung/pháp lý trên tập câu hỏi độc lập.

Xác nhận bản cuối ngày 21/09/2026: build API/web thành công; **157 backend test
đạt (22,13 giây), 4 Playwright test đạt (1,4 phút)**. Hai câu hỏi thật trả về
`qwen-local / qwen3.5:4b`, `hybrid` và `legal_hybrid`, không fallback;
thời gian API lần lượt **36.505 ms và 42.723 ms** (lượt đầu gồm tải E5).
Ollama báo `100% GPU`, context 8.192. Đây là số đo demo trên máy hiện tại,
không phải benchmark tải đồng thời. Câu hỏi giá điện vẫn thiếu đoạn nguồn
trực tiếp để kết luận: cần đánh giá/cải thiện truy xuất tài liệu riêng,
không xem việc model chạy thành công là đã giải quyết chất lượng pháp lý.
Sau kiểm tra ảnh, phần xem trước được giảm còn khoảng 420 ký tự khi câu trả lời
dài hơn 600 ký tự; vẫn mở được toàn văn. Web đã build/triển khai lại và 3 test
giao diện được chạy lại đạt (3,8 giây), bao gồm kiểm tra độ dài phần xem trước.

## Trước khi đưa lên Internet

Cần cấu hình máy chủ/domain/TLS, secret mạnh, SMTP thật, Google OAuth origins,
cookie Secure, backup định kỳ và rà soát dependency/bảo mật. Không công khai
Mailpit, PostgreSQL, Redis hoặc dùng nguyên cấu hình local. FR3 và FR8 vẫn
thuộc nhóm phụ trách riêng theo `FR_DELIVERY_GUIDE.md`.
