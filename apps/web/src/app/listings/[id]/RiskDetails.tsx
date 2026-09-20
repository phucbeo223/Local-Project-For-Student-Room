"use client";

import { useRef } from "react";

export default function RiskDetails({ reasons }: { reasons: string[] }) {
  const dialog = useRef<HTMLDialogElement>(null);
  return (
    <>
      <button
        type="button"
        className="mt-3 text-sm font-semibold text-primary underline"
        onClick={() => dialog.current?.showModal()}
      >
        Vì sao tin có mức cảnh báo này?
      </button>
      <dialog
        ref={dialog}
        aria-labelledby="risk-details-title"
        className="max-h-[85vh] w-[min(92vw,560px)] rounded-2xl p-6 shadow-xl backdrop:bg-black/40"
      >
        <h2 id="risk-details-title" className="text-xl font-bold">
          Giải thích mức cảnh báo
        </h2>
        {reasons.length ? (
          <ul className="my-4 list-disc space-y-2 pl-5">
            {reasons.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        ) : (
          <p className="my-4">
            Chưa ghi nhận tín hiệu cụ thể trong kết quả hiện có. Điều này không
            bảo đảm tin an toàn.
          </p>
        )}
        <p className="text-sm text-slate-600">
          Điểm hỗ trợ sàng lọc, không phải kết luận lừa đảo. Khi chưa đủ dữ liệu
          cùng khu vực, mô hình thống kê có thể chưa chạy. Luôn xem phòng và xác
          minh người cho thuê trước khi chuyển tiền.
        </p>
        <form method="dialog" className="mt-5">
          <button className="rounded bg-primary px-4 py-2 text-white">
            Đóng
          </button>
        </form>
      </dialog>
    </>
  );
}
