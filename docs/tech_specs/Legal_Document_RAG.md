# RAG văn bản pháp luật: scan, OCR và embedding

## Luồng dữ liệu

`Data/` → dò file hỗ trợ → trích text/OCR theo trang → chia đoạn theo `PHẦN/CHƯƠNG/MỤC/Điều`
→ E5 passage embedding 384 chiều → `legal_documents` + `legal_chunks` (PostgreSQL/pgvector).

Chatbot nhận diện câu hỏi pháp lý trước luồng tìm phòng. Nó chạy hybrid retrieval riêng trên
`legal_chunks`, sinh câu trả lời grounded bằng Qwen/Gemini/template và trả nguồn gồm tên văn bản,
Điều/Chương, trang và đường dẫn tương đối trong corpus. Luồng listing cũ không thay đổi.

## Định dạng và OCR

- Hỗ trợ: PDF, DOC, DOCX, TXT, Markdown, PNG/JPEG/TIFF.
- PDF dùng lớp text sẵn có. Trang có ít hơn 80 ký tự hữu ích sẽ được render 200 DPI và OCR.
- OCR dùng Tesseract `vie+eng`; `.doc` cũ dùng `antiword`.
- `Dockerfile.legal-indexer` chứa đủ Tesseract tiếng Việt, antiword, PyMuPDF và E5 CPU.
- Mỗi file được nhận dạng bằng SHA-256; chạy lại sẽ bỏ qua file không đổi. File đổi được thay
  toàn bộ chunk trong một transaction, nên không để lẫn phiên bản cũ/mới.

## Chạy chuẩn bằng Docker

Bật Docker Desktop, sau đó:

```powershell
docker compose up -d db --build
docker compose --profile tools run --rm legal-indexer
```

Lần đầu worker tải `intfloat/multilingual-e5-small`; cache được giữ trong volume
`legal-model-cache`. Các lần sau chỉ index file mới hoặc thay đổi.

Có thể chạy toàn hệ thống và index legal cùng lúc:

```powershell
.\scripts\start_all.ps1 -IndexLegal
```

Các tùy chọn hữu ích:

```powershell
# Index lại toàn bộ
docker compose --profile tools run --rm legal-indexer --force

# OCR mọi trang (chậm hơn, chỉ dùng khi lớp text PDF bị lỗi)
docker compose --profile tools run --rm legal-indexer --force --force-ocr

# Chế độ BM25 nếu chưa muốn tải model embedding
docker compose --profile tools run --rm legal-indexer --lexical-only
```

## Chạy trực tiếp bằng Python

Máy phải có Tesseract (`vie`, `eng`) và antiword trong PATH:

```powershell
python -m pip install -r apps/api/requirements-legal.txt
python scripts/index_legal_documents.py --data-dir Data
```

## Truy vấn kiểm tra

```text
Chủ trọ được thu tiền điện của người thuê như thế nào theo quy định?
Hợp đồng thuê nhà có bắt buộc công chứng không?
Sinh viên thuê trọ phải đăng ký tạm trú trong thời hạn nào?
Nhà trọ thuộc diện nào phải đáp ứng quy định PCCC?
```

API vẫn dùng `POST /chat/ask`. Với câu hỏi pháp lý, response có:

- `intent = legal_question`
- `retrieval_mode = legal_hybrid` hoặc `legal_lexical`
- `listings = []`
- `sources[].kind = legal_document`, cùng `title`, `heading`, `page_from/page_to`, `source_path`

## An toàn và giới hạn

- Prompt bắt buộc chỉ dùng context, trích dẫn `[1]..[5]`, không làm theo chỉ dẫn trong tài liệu.
- Câu trả lời luôn là thông tin tham khảo và nhắc kiểm tra hiệu lực văn bản.
- Hệ thống chưa tự suy luận văn bản hết hiệu lực/thay thế. Metadata hiệu lực cần một quy trình
  pháp chế riêng trước khi dùng cho tình huống có rủi ro cao.
- Không mở file trực tiếp qua API; `source_path` là đường dẫn tương đối, không lộ path máy chủ.

