import Link from "next/link";
import SiteHeader from "../SiteHeader";

export const metadata = { title: "Trợ lý tìm trọ | Trọ CTU" };

export default function ChatPage() {
  return (
    <>
      <SiteHeader />
      <main className="min-h-[calc(100vh-76px)] overflow-hidden bg-gradient-to-br from-[#edf6ff] via-white to-cyan-50 px-5 py-12 sm:px-10">
        <div className="mx-auto max-w-5xl">
          <Link href="/" className="text-sm font-semibold text-[#005baa] hover:underline">← Về trang tìm trọ</Link>
          <div className="mt-16 max-w-2xl">
            <p className="text-sm font-bold uppercase tracking-[0.2em] text-[#005baa]">Đại học Cần Thơ</p>
            <h1 className="mt-4 text-4xl font-black leading-tight text-slate-900 sm:text-6xl">Tìm đúng phòng trọ bằng <span className="text-[#005baa]">Hybrid AI</span></h1>
            <p className="mt-6 text-lg leading-8 text-slate-600">Mô tả ngân sách, khu vực và tiện ích bạn cần. Trợ lý tìm phòng từ dữ liệu hiện có hoặc tra cứu tài liệu thuê trọ. Nguồn tham khảo nằm ngay dưới câu trả lời; mô hình thực sự sử dụng được ghi ở từng lượt.</p>
            <div className="mt-8 flex flex-wrap gap-3 text-sm font-semibold text-slate-600">
              <span className="rounded-full bg-white px-4 py-2 shadow-sm">✓ Hỗ trợ AI local</span>
              <span className="rounded-full bg-white px-4 py-2 shadow-sm">✓ Không lưu lịch sử</span>
              <span className="rounded-full bg-white px-4 py-2 shadow-sm">✓ Trả lời có nguồn tin</span>
            </div>
            <p className="mt-8 text-sm text-slate-500">Cửa sổ trò chuyện đã mở ở góc phải. Bạn có thể phóng to, thu nhỏ hoặc đóng bất cứ lúc nào.</p>
          </div>
        </div>
      </main>
    </>
  );
}
