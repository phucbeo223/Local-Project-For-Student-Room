"use client";

import { Fragment, useRef, useState, type ReactNode } from "react";

type Reference = {
  rank: number;
  title: string;
  heading: string | null;
  page_from: number | null;
  page_to: number | null;
  excerpt?: string | null;
};

export default function ChatAnswer({ content, sources = [] }: { content: string; sources?: Reference[] }) {
  const [expanded, setExpanded] = useState(false);
  const [showSources, setShowSources] = useState(false);
  const [selected, setSelected] = useState<number | null>(null);
  const sourcePanel = useRef<HTMLDetailsElement>(null);
  const long = content.length > 600;
  const cut = Math.max(content.lastIndexOf("\n", 420), content.lastIndexOf(" ", 420));
  const visible = long && !expanded ? `${content.slice(0, cut > 0 ? cut : 420)}…` : content;

  function inline(text: string): ReactNode[] {
    return text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|\[\d+\])/g).map((part, index): ReactNode => {
      if (part.startsWith("**") && part.endsWith("**")) return <strong key={index}>{inline(part.slice(2, -2))}</strong>;
      if (part.startsWith("*") && part.endsWith("*")) return <em key={index}>{inline(part.slice(1, -1))}</em>;
      const citation = /^\[(\d+)\]$/.exec(part);
      const rank = citation ? Number(citation[1]) : null;
      if (rank !== null && sources.some((source) => source.rank === rank)) {
        return <button key={index} type="button" aria-label={`Xem nguồn ${rank}`}
          className="mx-0.5 inline-flex rounded bg-blue-50 px-1.5 text-xs font-semibold text-[#005baa] hover:bg-blue-100"
          onClick={() => {
            setShowSources(true);
            setSelected(rank);
            // Focus without scrolling the outer page or hiding the widget header.
            sourcePanel.current?.querySelector("summary")?.focus({ preventScroll: true });
          }}>{part}</button>;
      }
      // React escapes model output: never interpret HTML or arbitrary Markdown URLs.
      return <Fragment key={index}>{part}</Fragment>;
    });
  }

  const lines = visible.split(/\n+/).filter((line) => line.trim());
  const blocks = [];
  for (let i = 0; i < lines.length; i++) {
    if (/^\s*(?:[-*•]|\d+[.)])\s+/.test(lines[i])) {
      const items = [];
      const start = i;
      while (i < lines.length && /^\s*(?:[-*•]|\d+[.)])\s+/.test(lines[i])) {
        items.push(<li key={i}>{inline(lines[i].replace(/^\s*(?:[-*•]|\d+[.)])\s+/, ""))}</li>);
        i++;
      }
      i--;
      blocks.push(<ul key={start} className="list-disc space-y-2 pl-5 marker:text-blue-500">{items}</ul>);
    } else {
      blocks.push(<p key={i}>{inline(lines[i].replace(/^#{1,6}\s+/, ""))}</p>);
    }
  }

  return <div className="min-w-0 space-y-3 break-words [overflow-wrap:anywhere]">
    <div className="space-y-3" data-testid="chat-answer">{blocks}</div>
    {long && <button type="button" aria-expanded={expanded} className="text-xs font-semibold text-[#005baa]"
      onClick={() => setExpanded(!expanded)}>{expanded ? "Thu gọn câu trả lời" : "Xem toàn bộ câu trả lời"}</button>}
    {sources.length > 0 && <details ref={sourcePanel} open={showSources}
      onToggle={(event) => setShowSources(event.currentTarget.open)}
      className="rounded-xl border border-blue-100 bg-slate-50 text-xs">
      <summary className="cursor-pointer px-3 py-2 font-semibold text-[#005baa]">Nguồn tham khảo ({sources.length})</summary>
      <div className="space-y-2 px-3 pb-3">
        {sources.map((source) => <div key={source.rank} className={`rounded-lg border p-2.5 ${selected === source.rank ? "border-blue-400 bg-blue-50" : "border-slate-200 bg-white"}`}>
          <p className="font-semibold text-slate-700">[{source.rank}] {source.title}</p>
          {source.heading && <p className="mt-1 text-slate-500">{source.heading}</p>}
          {source.page_from && <p className="text-slate-500">Trang {source.page_from}{source.page_to && source.page_to !== source.page_from ? `–${source.page_to}` : ""}</p>}
          {source.excerpt && <details className="mt-2">
            <summary className="cursor-pointer text-[#005baa]">Đọc trích đoạn</summary>
            <p className="mt-2 whitespace-pre-line border-l-2 border-blue-200 pl-2 leading-5 text-slate-600">{source.excerpt}</p>
            <p className="mt-1 text-[10px] text-slate-400">Trích đoạn, không phải toàn bộ văn bản.</p>
          </details>}
        </div>)}
      </div>
    </details>}
  </div>;
}
