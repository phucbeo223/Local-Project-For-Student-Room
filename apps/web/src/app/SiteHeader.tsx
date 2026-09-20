"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useId, useRef, useState } from "react";
import type { User } from "@/lib/api";

const ICONS = {
  menu: "M4 6h16M4 12h16M4 18h16",
  close: "m6 6 12 12M6 18 18 6",
  search: "m21 21-4.4-4.4M19 11a8 8 0 1 1-16 0 8 8 0 0 1 16 0",
  pin: "M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0ZM15 10a3 3 0 1 1-6 0 3 3 0 0 1 6 0",
  heart: "M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z",
  bell: "M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4",
  chat: "M21 11.5a8.5 8.5 0 0 1-8.5 8.5H4l-2 2V11.5a9.5 9.5 0 0 1 19 0ZM7 9h10M7 13h6",
  home: "m3 10 9-7 9 7M5 9v12h14V9M9 21v-8h6v8",
  spark: "m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5Z",
  compare: "M8 3v18M16 3v18M3 7h10M11 17h10",
  bookmark: "M6 3h12v18l-6-4-6 4Z",
  listing: "M5 3h14v18H5ZM8 7h8M8 12h8M8 17h5",
  shield: "m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6ZM8 12l3 3 5-6",
  plus: "M12 5v14M5 12h14",
} as const;

function Icon({ name, className = "h-5 w-5" }: { name: keyof typeof ICONS; className?: string }) {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <path d={ICONS[name]} />
    </svg>
  );
}

const NAV: { href: string; label: string; icon: keyof typeof ICONS }[] = [
  { href: "/", label: "Tìm trọ", icon: "home" },
  { href: "/map", label: "Bản đồ", icon: "pin" },
  { href: "/chat", label: "Trợ lý AI", icon: "chat" },
  { href: "/recommendations", label: "Dành cho bạn", icon: "spark" },
  { href: "/favorites", label: "Yêu thích", icon: "heart" },
  { href: "/compare", label: "So sánh phòng", icon: "compare" },
  { href: "/saved-searches", label: "Tìm kiếm đã lưu", icon: "bookmark" },
  { href: "/notifications", label: "Thông báo", icon: "bell" },
  { href: "/listings/mine", label: "Tin của tôi", icon: "listing" },
];
const FOCUS = "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2";
const ICON_LINK = "hidden h-11 w-11 place-items-center rounded-full text-ink transition hover:bg-tint sm:grid " + FOCUS;
const PILL = "hidden min-h-11 items-center rounded-full border border-line px-4 text-sm font-semibold text-ink transition hover:bg-tint sm:flex " + FOCUS;

export default function SiteHeader() {
  const pathname = usePathname();
  const menuId = useId();
  const searchId = useId();
  const dialogRef = useRef<HTMLDialogElement>(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [user, setUser] = useState<User | null | undefined>(undefined);

  useEffect(() => {
    let active = true;
    fetch("/api/auth/me", { cache: "no-store" })
      .then(async (response) => (response.ok ? ((await response.json()) as User) : null))
      .then((value) => { if (active) setUser(value); })
      .catch(() => { if (active) setUser(null); });
    return () => { active = false; };
  }, [pathname]);

  useEffect(() => {
    dialogRef.current?.close();
    setMenuOpen(false);
  }, [pathname]);

  useEffect(() => {
    if (!menuOpen) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = previousOverflow; };
  }, [menuOpen]);

  function closeMenu() {
    dialogRef.current?.close();
    setMenuOpen(false);
  }

  return (
    <header className="relative z-[1100] shrink-0 border-b border-line bg-white">
      <div className="mx-auto flex min-h-16 max-w-[1920px] flex-wrap items-center gap-2 px-3 py-2 sm:gap-3 sm:px-5 lg:flex-nowrap lg:px-7">
        <button
          type="button" aria-label="Mở menu điều hướng" aria-expanded={menuOpen}
          aria-controls={menuId} aria-haspopup="dialog"
          onClick={() => { dialogRef.current?.showModal(); setMenuOpen(true); }}
          className={"grid h-11 w-11 shrink-0 place-items-center rounded-full text-ink-soft transition hover:bg-tint " + FOCUS}
        ><Icon name="menu" /></button>

        <Link href="/" aria-label="Trọ CTU — Trang chủ" className={"shrink-0 rounded-lg text-xl font-black tracking-tight text-primary sm:text-2xl " + FOCUS}>
          TRỌ<span className="ml-1 text-primary-bright">CTU</span>
        </Link>
        <Link href="/map" className={"hidden min-h-11 shrink-0 items-center gap-1.5 rounded-full bg-tint px-3 text-sm font-semibold text-ink sm:flex " + FOCUS}>
          <Icon name="pin" className="h-[18px] w-[18px] text-primary" />Cần Thơ
        </Link>

        <form action="/" method="get" role="search" aria-label="Tìm phòng trọ" className="order-last flex h-11 w-full min-w-0 items-center gap-2 rounded-full border border-transparent bg-[#f4f4f5] pl-4 pr-1 focus-within:border-primary/40 lg:order-none lg:w-auto lg:flex-1">
          <Icon name="search" className="h-[18px] w-[18px] shrink-0 text-ink-faint" />
          <label htmlFor={searchId} className="sr-only">Từ khóa tìm phòng trọ</label>
          <input id={searchId} name="q" type="search" placeholder="Tìm phòng trọ ở Cần Thơ..." className="min-w-0 flex-1 bg-transparent text-sm text-ink outline-none placeholder:text-ink-muted" />
          <button type="submit" aria-label="Tìm kiếm" className={"grid h-9 w-9 shrink-0 place-items-center rounded-full bg-primary text-white transition hover:bg-navy " + FOCUS}>
            <Icon name="search" className="h-[18px] w-[18px]" />
          </button>
        </form>

        <div className="ml-auto flex shrink-0 items-center gap-1 sm:gap-2 lg:ml-1">
          <Link href="/favorites" aria-label="Yêu thích" title="Yêu thích" className={ICON_LINK}><Icon name="heart" className="h-6 w-6" /></Link>
          <Link href="/notifications" aria-label="Thông báo" title="Thông báo" className={ICON_LINK}><Icon name="bell" className="h-[22px] w-[22px]" /></Link>
          <Link href="/chat" className={"hidden min-h-11 items-center gap-2 rounded-full border border-line px-4 text-sm font-semibold text-ink transition hover:bg-tint xl:flex " + FOCUS}><Icon name="chat" />Trợ lý AI</Link>
          {user ? (
            <Link href="/me" aria-label={"Tài khoản: " + (user.name || user.email)} title={user.email} className={"hidden h-11 max-w-[150px] items-center gap-2 rounded-full border border-line px-2 text-sm font-semibold text-ink transition hover:bg-tint sm:flex " + FOCUS}>
              <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-primary-soft text-primary">{(user.name || user.email).trim().charAt(0).toUpperCase()}</span>
              <span className="hidden truncate pr-2 2xl:block">{user.name || user.email}</span>
            </Link>
          ) : user === null ? (
            <Link href="/login" className={PILL}>Đăng nhập</Link>
          ) : <span aria-label="Đang tải tài khoản" className="hidden h-11 w-11 animate-pulse rounded-full bg-tint sm:block" />}
          <Link href="/listings/new" className={"inline-flex min-h-11 items-center gap-1.5 whitespace-nowrap rounded-full bg-primary px-3 text-sm font-bold text-white transition hover:bg-navy sm:px-4 " + FOCUS}>
            <Icon name="plus" className="hidden h-[18px] w-[18px] sm:block" />Đăng tin
          </Link>
        </div>
      </div>

      <dialog
        ref={dialogRef} id={menuId} aria-labelledby={menuId + "-title"}
        onClose={() => setMenuOpen(false)}
        onClick={(event) => {
          if (event.target !== event.currentTarget) return;
          const rect = event.currentTarget.getBoundingClientRect();
          if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeMenu();
        }}
        className="fixed inset-y-0 left-0 m-0 h-dvh max-h-none w-[340px] max-w-[calc(100vw-32px)] border-0 bg-white p-0 text-ink shadow-2xl backdrop:bg-slate-950/40"
      >
        <div className="flex min-h-full flex-col">
          <div className="flex min-h-16 shrink-0 items-center justify-between border-b border-line px-5">
            <h2 id={menuId + "-title"} className="text-xl font-extrabold text-primary">Khám phá Trọ CTU</h2>
            <button autoFocus type="button" onClick={closeMenu} aria-label="Đóng menu" className={"grid h-11 w-11 place-items-center rounded-full text-ink-soft hover:bg-tint " + FOCUS}><Icon name="close" /></button>
          </div>
          <div className="border-b border-line bg-tint px-5 py-4">
            {user ? (
              <Link href="/me" onClick={closeMenu} className={"flex items-center gap-3 rounded-xl " + FOCUS}>
                <span className="grid h-11 w-11 shrink-0 place-items-center rounded-full bg-primary-soft text-lg font-bold text-primary">{(user.name || user.email).trim().charAt(0).toUpperCase()}</span>
                <span className="min-w-0"><span className="block truncate font-bold">{user.name || user.email}</span><span className="text-sm text-ink-muted">Xem tài khoản của bạn →</span></span>
              </Link>
            ) : user === null ? (
              <div>
                <p className="text-sm text-ink-muted">Tìm nơi ở phù hợp cùng Trọ CTU</p>
                <div className="mt-3 flex gap-2">
                  <Link href="/login" onClick={closeMenu} className={"flex min-h-11 flex-1 items-center justify-center rounded-full bg-primary px-4 text-sm font-bold text-white hover:bg-navy " + FOCUS}>Đăng nhập</Link>
                  <Link href="/register" onClick={closeMenu} className={"flex min-h-11 flex-1 items-center justify-center rounded-full border border-line bg-white px-4 text-sm font-bold text-primary hover:bg-primary-soft " + FOCUS}>Đăng ký</Link>
                </div>
              </div>
            ) : <p role="status" className="py-3 text-sm text-ink-muted">Đang tải tài khoản...</p>}
          </div>
          <nav aria-label="Điều hướng chính" className="space-y-1 p-3">
            {NAV.map((item) => {
              const active = item.href === "/" ? pathname === "/" : pathname === item.href || pathname.startsWith(item.href + "/");
              return (
                <Link key={item.href} href={item.href} onClick={closeMenu} aria-current={active ? "page" : undefined} className={"flex min-h-11 items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition " + (active ? "bg-primary-soft font-bold text-primary " : "font-medium text-ink-soft hover:bg-tint ") + FOCUS}>
                  <Icon name={item.icon} /><span>{item.label}</span>
                </Link>
              );
            })}
            {user?.role === "admin" && (
              <Link href="/admin" onClick={closeMenu} aria-current={pathname.startsWith("/admin") ? "page" : undefined} className={"flex min-h-11 items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-bold text-primary hover:bg-primary-soft " + FOCUS}><Icon name="shield" />Quản trị hệ thống</Link>
            )}
          </nav>
          <div className="mt-auto border-t border-line p-5 pb-[max(20px,env(safe-area-inset-bottom))]">
            <Link href="/listings/new" onClick={closeMenu} className={"flex min-h-11 items-center justify-center gap-2 rounded-full bg-primary px-4 text-sm font-bold text-white hover:bg-navy " + FOCUS}><Icon name="plus" />Đăng tin miễn phí</Link>
            <p className="mt-3 text-center text-xs text-ink-muted">Đồng hành cùng sinh viên ĐH Cần Thơ</p>
          </div>
        </div>
      </dialog>
    </header>
  );
}
