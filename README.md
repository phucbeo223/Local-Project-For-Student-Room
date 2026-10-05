# TimTroSV — Local Project for Student Room

Hệ thống hỗ trợ sinh viên Đại học Cần Thơ tìm nhà trọ.

Nhánh hiện tại dùng Datahouse làm kho phòng chính và Graph RAG với nguồn pháp lý từ Word. Chỉ hỗ trợ tìm trọ và pháp lý thuê trọ cơ bản; không soạn hợp đồng hoặc điền tờ khai. Dùng hướng dẫn `WORD_ONLY_TENANT_SUPPORT_20261005.md` cho phiên bản đang chạy.

- [Hướng dẫn triển khai FR1 / FR2 / FR4 / FR6 / FR7 và bàn giao FR3 / FR8](docs/FR_DELIVERY_GUIDE.md)
- [Đặc tả yêu cầu](docs/planning/SRS.md)
- [Tài liệu dự án](docs/README.md)
- [Vận hành Docker local và kiểm tra hệ thống](docs/LOCAL_DEPLOYMENT.md)
- [Kho embedding pháp lý cập nhật và kiểm thử 36 câu ngày 04/10/2026](docs/LEGAL_REFRESH_20261004.md)
- [Nhánh Graph RAG, kho nhà trọ riêng và kiểm thử 56 câu](docs/GRAPH_RAG_20261004.md)
- [Datahouse làm kho chính, nguồn nguyên gốc và Graph RAG tối ưu](docs/SOURCE_GROUNDED_DATAHOUSE_20261004.md)
- [Phiên bản Word: phạm vi thuê trọ cơ bản, bỏ PDF/OCR và kiểm thử 36 câu](docs/WORD_ONLY_TENANT_SUPPORT_20261005.md)

Nhánh Datahouse/Graph RAG: `codex/source-grounded-datahouse-20261004`.
Các mốc trước đó: nhánh sao lưu `codex/baseline-before-fr-updates` (`6d36e9a`) và triển khai FR `codex/fr1-fr2-fr4-fr6-fr7`.

Đọc hướng dẫn migration trước khi chạy phiên bản mới trên database đang có.
Không commit `.env` hoặc dùng cấu hình dev để triển khai public.
