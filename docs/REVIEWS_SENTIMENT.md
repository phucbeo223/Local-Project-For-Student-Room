# Đánh giá phòng và giám sát cảm xúc bình luận

## Luồng người dùng

- Trang chi tiết phòng hiển thị điểm trung bình, phân bố 1–5 sao và các bình luận.
- Người dùng đã đăng nhập được gửi một đánh giá cho mỗi phòng; chủ tin không được tự đánh giá.
- Bình luận dài 10–2.000 ký tự và được chuẩn hóa khoảng trắng trước khi lưu.

## Mô hình machine learning

`VietnameseReviewSentimentModel` là mô hình Multinomial Naive Bayes chạy cục bộ, được huấn luyện từ tập câu tiếng Việt có nhãn tích cực/tiêu cực. Mô hình dùng unigram và bigram, sau đó tạo vùng trung tính cho các dự đoán chưa đủ chắc chắn.

- Model version: `vi-review-nb-v1`
- Ngưỡng gắn cờ tiêu cực: `negative_score >= 0.62`
- Không cần gọi API bên ngoài hoặc tải model khi khởi động.
- Kết quả dự đoán và phiên bản model được lưu cùng review để kiểm toán.

Review tiêu cực chuyển sang `moderation_status = 'flagged'`. Hệ thống không tự xóa review và không tự ẩn listing. Admin có thể lấy hàng chờ qua `GET /admin/reviews/flagged`, sau đó duyệt hoặc ẩn bằng `PATCH /admin/reviews/{id}`.

## API

| Method | Endpoint | Quyền | Mục đích |
|---|---|---|---|
| GET | `/listings/{id}/reviews` | Public | Danh sách và tổng hợp điểm sao |
| POST | `/listings/{id}/reviews` | User | Tạo đánh giá và chạy phân tích cảm xúc |
| GET | `/admin/reviews/flagged` | Admin | Hàng chờ review bị AI gắn cờ |
| PATCH | `/admin/reviews/{id}` | Admin | Duyệt (`approve`) hoặc ẩn (`hide`) |

Database mới tự chạy migration `infra/db/migrations/96_reviews_sentiment.sql`
qua Docker init. Với database đã có volume, dùng `scripts/start_all.ps1` hoặc
`scripts/apply_room_services.py`; cả hai script đều áp migration 95 và 96 theo
kiểu cộng thêm, không xóa dữ liệu.
