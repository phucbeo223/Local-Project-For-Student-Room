# Bàn giao FR1, FR2, FR4, FR6, FR7

## Phạm vi và Git

- Repo cá nhân: `https://github.com/phucbeo223/Local-Project-For-Student-Room`.
- Bản trước thay đổi: nhánh `codex/baseline-before-fr-updates`, commit `6d36e9a`.
- Nhánh triển khai: `codex/fr1-fr2-fr4-fr6-fr7`. Không force-push, không thay thế `main` có sẵn, không thay remote của nhóm.
- FR3 (crawler/chuẩn hóa/geocoding/POI) và FR8 (thông báo/quản trị) do nhóm khác làm. FR5 không thuộc lần này.
- Căn cứ: `docs/planning/SRS.md`, `05_DacTa_UseCase.md`, `Technical_Roadmap.md`.

## Những thay đổi đã triển khai

| FR | Chức năng | Điểm cần cấu hình/giới hạn |
|---|---|---|
| FR1 | OTP 6 số/5 phút/3 lần thử; gửi lại sau 60 giây; chỉ tạo tài khoản sau xác thực; reset qua link 30 phút; khóa 15 phút sau 5 lần sai; Google GIS; sửa tên hồ sơ | Cần SMTP thật và Google client ID; không trả OTP/token reset trong API hoặc log |
| FR1 | Access 15 phút, refresh 7 ngày mặc định; refresh rotation lưu hash DB; logout thu hồi refresh; reset thu hồi mọi refresh và access cũ | Refresh cũ trước migration không được chấp nhận. Logout thường không vô hiệu ngay access đã phát, nó hết hạn sau tối đa 15 phút |
| FR2 | Lọc tiện ích, phường/xã, diện tích tối đa; sắp xếp độ tươi; detail dùng tiện ích đã chuẩn hóa; so sánh tối đa 3; thêm GET proxy chi tiết | Phường chỉ khớp khi nguồn có `ward`; nhóm FR3 cần điền dữ liệu. Bảng so sánh lưu trên trình duyệt, yêu cầu đăng nhập để thêm/truy cập |
| FR2 | Đổi campus hoặc click nền bản đồ để chọn tâm truy vấn và vòng bán kính | Tối đa 300 tin gần nhất, không coi con số trên bản đồ là tổng toàn bộ; ORS cần API key để vẽ tuyến thực |
| FR4 | Quiz 3 tiêu chí; lưu vector 384 chiều; cosine + implicit feedback; phổ biến 30 ngày khi chưa có hồ sơ; 80/20 khai thác/khám phá | Vector **đặc trưng có cấu trúc**, không phải embedding E5. Không trộn vector này với `embedding_vector` của chatbot |
| FR4 | Chặn tin đã dismiss/rủi ro cao; giữ ngân sách/khoảng cách/tiện ích cả trong khám phá; bỏ tín hiệu bookmark sau khi bỏ yêu thích | `preference_vector` được tính lại khi lấy gợi ý. Xét toàn bộ ứng viên hợp lệ; dữ liệu lớn cần materialize/index riêng |
| FR6 | Bắt buộc đăng nhập; giới hạn 12 câu/phút/user; feedback theo chủ sở hữu; nhớ tối đa 5 lượt; tiêu chí mới ghi đè cũ; ngưỡng 0.65; citation sai → mẫu có nguồn | Kiểm tra citation không chứng minh mọi mệnh đề đúng. Cần đánh giá groundedness trên tập độc lập trước nghiệm thu AI |
| FR7 | Rule + IsolationForest + đối chiếu ảnh URL/pHash + báo cáo cộng đồng + tần suất đăng 24 giờ; lý do từng tín hiệu; bảo toàn manual override | IsolationForest cần ≥50 mẫu hợp lệ cùng khu vực trong 180 ngày. Thiếu dữ liệu/dependency báo trạng thái, không giả là đã chạy ML |

## Cài đặt / nâng cấp an toàn

1. Checkout nhánh triển khai. Sao lưu PostgreSQL trước migration. **Không dùng `docker compose down -v` để nâng cấp**.
2. Dùng `.env.example` làm tham chiếu; không ghi đè `.env` đang có. Sửa rõ `REFRESH_TOKEN_TTL_DAYS=7`, `ACCESS_TOKEN_TTL_MIN=15`, `CHATBOT_LLM_TIMEOUT_SECONDS=4` (file cũ có thể vẫn là 30 ngày/120 giây).
3. Đặt `JWT_SECRET` ngẫu nhiên mạnh, HTTPS + `AUTH_COOKIE_SECURE=true` khi public. Giá trị dev không phù hợp production.
4. Database mới được init theo migrations trong `infra/db`. Database đã có phải áp dụng `infra/db/migrations/95_fr_delivery.sql` một lần trước khi chạy API mới. Ví dụ PowerShell, với service DB đã chạy và user/database mặc định:

   ```powershell
   Get-Content infra/db/migrations/95_fr_delivery.sql -Raw | docker compose exec -T db psql -U nckh -d nckh -v ON_ERROR_STOP=1
   docker compose up -d --build api web
   ```

   Thay `nckh` bằng user/database thực tế. Migration chỉ thêm cột/bảng; không xóa hoặc seed lại dữ liệu. Rollback ứng dụng về baseline có thể giữ các cột mới, nhưng phiên đăng nhập mới cần đăng nhập lại.
5. Đăng nhập lại sau triển khai vì refresh legacy chưa có session DB. Các tài khoản cũ được giữ nguyên, không tự đặt lại mật khẩu hoặc đánh dấu email đã xác thực.

### SMTP và Google

- `SMTP_HOST`, `SMTP_PORT` (587), `SMTP_STARTTLS=true`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM`, `WEB_PUBLIC_URL` là URL HTTPS public dùng trong link reset.
- Local có thể dùng SMTP capture như Mailpit trên mạng tin cậy; tắt STARTTLS chỉ với máy nhận mail local. Không có SMTP → đăng ký báo 503 thay vì giả vờ đã gửi.
- OTP/hash mật khẩu chờ xác thực lưu ở `auth_challenges`, không phải `users`; reset token ngẫu nhiên 256 bit được lưu dạng HMAC. Cần job bảo trì định kỳ xóa challenge/session/bucket đã hết hạn theo chính sách lưu trữ (nhóm vận hành).
- Google: cấu hình Authorized JavaScript origins cho URL web, điền `GOOGLE_CLIENT_ID`. Docker chuyển ID này vào build web; chạy Next trực tiếp cần `NEXT_PUBLIC_GOOGLE_CLIENT_ID`. Build lại khi đổi ID. Không tự liên kết Google với email local đã tồn tại để tránh chiếm tài khoản.
- Đăng nhập sai bị giới hạn theo IP nhìn thấy ở API và theo tài khoản. Khi đi qua BFF, IP là BFF; cần rate limit ở reverse proxy theo IP người dùng thật, chỉ tin header từ proxy nội bộ.
- Nếu dữ liệu cũ có nhiều email chỉ khác hoa/thường, cần nhóm vận hành kiểm tra và hòa giải thủ công trước triển khai; không tự gộp tài khoản.

### API mới/thay đổi

| Endpoint | Quyền / hợp đồng |
|---|---|
| POST `/auth/register` | Trả 202 `{verification_required,email}`, **không trả token** |
| POST `/auth/verify-email` | `{email,code}` → token pair |
| POST `/auth/resend-otp` | `{email}`; cooldown 60 giây |
| POST `/auth/forgot-password` | `{email}`; thông báo chung, link hết hạn 30 phút |
| POST `/auth/reset-password` | `{email,token,password}`; token dùng một lần |
| POST `/auth/refresh`, `/auth/logout` | `{refresh_token}`; refresh dùng một lần |
| PATCH `/auth/me` | Bearer; `{name}`; không cho sửa role/email tùy ý |
| GET `/listings` | Thêm `max_area`, `ward`, `amenities=wifi&amenities=parking` |
| GET/POST `/recommend/quiz` | Bearer; `{max_price,max_distance_ctu,amenities,district?}` |
| GET `/recommend/for-you` | Bearer; alias tương thích `/recommendations`, mặc định 10 kết quả |
| GET `/recommend/popular` | Công khai; định dạng RecommendationResponse |
| POST `/recommend/feedback` | Bearer; alias ghi tương tác `{listing_id,type,duration_ms?}` |
| POST `/chat/ask`, `/chat/feedback` | Bearer bắt buộc; `include_evaluation_contexts` chỉ admin; feedback cần `event_id` của chính user |
| GET `/risk/listings/{id}` | Chỉ tin chưa hidden/expired; thêm `statistical_status` |

### Chatbot và mô hình

- Mặc định image API nhẹ không cài E5: structured/lexical fallback vẫn hoạt động và trả `degraded`. Muốn hybrid thật, đặt `INSTALL_ML=true`, build lại API; nạp embedding listing/legal bằng công cụ hiện có của nhóm dữ liệu.
- 384 chiều FR4 là vector cấu trúc phiên bản `structured-cosine-v1`: dải giá/khoảng cách và feature tiện ích/khu vực. Đây là lựa chọn triển khai minh bạch, **khác hướng sentence embedding ở T5**; muốn đổi sang E5 phải rebuild cả vector hồ sơ và ứng viên, đánh giá lại rồi tăng phiên bản.
- Provider LLM có timeout mặc định 4 giây và ngừng thử provider kế tiếp khi ngân sách đã hết. Đây **không phải cam kết end-to-end <5 giây**: cold model load, retrieval và mạng vẫn cần đo p95. Cần warm model/cache và hạ tầng phù hợp.
- Nội dung chat không lưu DB; chỉ telemetry aggregate + user ID phục vụ kiểm soát feedback. Client gửi tối đa 10 message (5 lượt); không tin nội dung assistant là tiêu chí người dùng.
- UI phải hiển thị thông báo khi phiên hết hạn; BFF không gửi token về JavaScript. Server Component không tự xoay token vì không thể lưu cookie; route renew nhận nhiệm vụ này.

### Risk 5 lớp và dữ liệu ảnh

- `requirements-risk.txt` cài IsolationForest/Pillow/ImageHash. API Docker cài sẵn phần risk, E5 vẫn là tùy chọn riêng.
- IsolationForest fit trong RAM, cache tối đa 1 giờ, seed cố định, 100 trees, contamination 0.05; feature log(giá), log(diện tích), log(giá/m²). Không load pickle ngoài, không huấn luyện từ `dev_seed`/`seed`/`test`.
- Tin khác nguồn, khác khu vực và trùng URL ảnh hoặc pHash Hamming ≤8 phát sinh tín hiệu cần xác minh; **không khẳng định ảnh đánh cắp**. Hiện không tự tải ảnh URL để tránh SSRF và crawler chồng trách nhiệm.
- Nhóm FR3 có thể cung cấp ảnh đã tải hợp lệ và manifest JSON `[{"listing_id":123,"image_url":"https://...","file":"room.jpg"}]`, rồi chạy:

  ```powershell
  python scripts/index_risk_images.py manifest.json --image-root D:/approved-room-images
  ```

  `DATABASE_URL` phải trỏ đúng database; đường dẫn ảnh phải nằm trong thư mục được chỉ định, URL phải đã thuộc listing. Script thêm hash trong một transaction, không tải mạng. Chạy assess lại sau khi bổ sung hash.
- Behavior hiện dựa trên tài khoản/tần suất đăng, chưa thu thập IP fingerprint. Nếu cần chống nhiều tài khoản cùng IP, FR3/FR8 phải bổ sung dữ liệu có thời hạn lưu, consent/chính sách riêng tư và giới hạn truy cập.
- `manual-override` được bảo toàn kể cả khi batch/UGC cập nhật. FR8 cần luồng rõ ràng để admin bỏ override, ghi audit, đặt `risk_model=NULL,risk_evaluated_at=NULL` rồi gọi assess lại; không tự xóa quyết định admin.
- Điểm risk là tín hiệu hỗ trợ, không phải xác suất lừa đảo đã hiệu chuẩn. Chưa có tập gán nhãn độc lập nên **chưa xác nhận mục tiêu recall/accuracy trong SRS**.

## Hướng dẫn bàn giao FR3 và FR8

### FR3 — nhóm dữ liệu/crawler

1. Giữ hợp đồng `aggregated_listings`: status/cleaning_status/listing_type, `price` VND, `area` m², `distance_to_ctu` mét, `geom` EPSG:4326, `ward`, `parsed_amenities` JSON boolean, images text[], source/source_url và timestamps.
2. Key tiện ích: wifi, air_conditioner, private_wc, parking, kitchen, fridge, washing_machine, free_hours. Không dùng nhãn hiển thị làm key; phân biệt không biết với false.
3. Khi dữ liệu thay đổi, cập nhật `updated_at`, làm mới embedding chat nếu content hash đổi; không dùng `users.preference_vector` của FR4 làm embedding listing.
4. Sau commit ingest/cleaner gọi `RiskService.assess(...,persist=True)` hoặc batch endpoint admin; cung cấp ảnh đã duyệt cho index pHash; POI và ward do pipeline bổ sung.
5. Việc còn của FR3: bảo vệ endpoint chạy crawler, kiểm soát nguồn/giới hạn batch; dedup cross-source; full sweep không tăng miss_count khi nguồn thất bại; kiểm thử 403/429/geocoding/POI. Lần này không sửa các file crawler.

### FR8 — nhóm quản trị/thông báo

1. Dùng dependency `require_admin` tại API, không chỉ ẩn nút giao diện. Không cho client cập nhật role qua profile.
2. Dùng risk history/override hiện có; hiển thị trạng thái thiếu cohort/model, không chỉ badge. Cần thao tác bỏ override có audit như trên.
3. Thông báo: sửa truy vấn hiện giới hạn 50 tin rồi đẩy watermark lên `now()`; cần pagination/cursor để không bỏ lỡ các tin chưa xử lý. Đồng bộ tiêu chí mới max_area/ward vào saved search và matcher khi FR8 hỗ trợ.
4. Bổ sung dashboard cấu hình crawler/khóa user và revoke auth sessions khi khóa; kiểm tra `auth_version` để thu hồi access. Không sửa trực tiếp JWT phía client.
5. Bảo trì challenge/session/rate buckets hết hạn; chính sách lưu telemetry có user ID. Metrics chatbot/risk cần ghi rõ phiên bản dataset/model.

## Kiểm thử và nghiệm thu

### Kết quả đã xác minh (20/09/2026)

- Commit `a904418`: **145/145 test backend passed**, gồm PostgreSQL integration, OTP/refresh/reset, search/quiz/vector/risk/feedback ownership; không skip trong CI.
- Frontend type-check và production build thành công cả local và GitHub Actions.
- Bằng chứng: [CI run 35489504367](https://github.com/phucbeo223/Local-Project-For-Student-Room/actions/runs/35489504367).
- Docker Engine trên máy làm việc chưa sẵn sàng; kiểm thử database thật được thực hiện trên CI, không trên database cá nhân. Email trong test được bắt bằng mock, chưa xác nhận nhà cung cấp SMTP/OAuth thực tế.
- Các thay đổi UI/tài liệu sau commit trên phải có Actions xanh của commit cuối cùng trước merge; không diễn giải 145 test này thành chứng nhận chất lượng dữ liệu/AI production.

```powershell
# Database test riêng, không mở cổng, không dùng volume dữ liệu ứng dụng:
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from api
# Sau khi đọc kết quả, tắt riêng dịch vụ test (không tác động compose chính):
docker compose -f docker-compose.test.yml down

# Frontend:
cd apps/web
npx tsc --noEmit
npm run build
```

- Test mới: `test_fr_delivery.py` (vector, ranking, auth gate, memory, citations, IsolationForest) và `test_fr_auth_db.py` (OTP/rotation/logout/lock/reset). Database tests chỉ bật qua `RUN_DB_TESTS=1` trên DB test.
- Test UGC cũ đã đổi helper đăng ký theo OTP; không thay đổi nghiệp vụ FR3. Test chatbot tích hợp gửi Bearer và chấp nhận fallback được khai báo.
- CI chép thêm scripts/eval để test dataset không thất bại vì thiếu file; chạy cả DB tests. Xem kết quả Actions của đúng commit trước merge.
- Nghiệm thu thủ công: nhận mail thật; sai OTP 3 lần; resend; Google lần đầu/email trùng; refresh/đăng xuất/reset; quiz→top10; bỏ bookmark/dismiss; lọc nhiều tiện ích; map đổi campus/chọn điểm; so sánh 2–3 tin; chat 3 lượt đổi giá; risk có/không cohort và manual override.
- Các mục chưa thể kết luận từ unit test: SMTP/OAuth thực tế, chất lượng AI trên dữ liệu thật, p95 end-to-end, pHash trên kho ảnh, tải lớn và an toàn triển khai public.
- Baseline còn cảnh báo phụ thuộc Next.js từ lần review; lần này chưa nâng major framework. Cần xử lý audit/upgrade và endpoint crawler thuộc FR3 trước public production.
