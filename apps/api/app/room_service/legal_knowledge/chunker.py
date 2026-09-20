from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Iterable

from .extractor import ExtractedPage


HEADING_RE = re.compile(
    r"^(?:PHẦN|CHƯƠNG|MỤC|TIỂU MỤC)\s+[IVXLCDM\d]+\b|^Điều\s+\d+[a-zA-Z]?\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class LegalChunk:
    chunk_index: int
    page_from: int
    page_to: int
    heading: str | None
    content: str
    content_sha256: str


@dataclass(frozen=True)
class _Unit:
    page: int
    heading: str | None
    text: str


def _units(pages: Iterable[ExtractedPage]) -> list[_Unit]:
    result: list[_Unit] = []
    current_heading: str | None = None
    for page in pages:
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n|(?<=\.)\s*\n", page.text) if part.strip()]
        for paragraph in paragraphs:
            first_line = paragraph.splitlines()[0].strip()
            if HEADING_RE.search(first_line):
                current_heading = first_line[:300]
            result.append(_Unit(page.number, current_heading, re.sub(r"\s+", " ", paragraph)))
    return result


def chunk_pages(
    pages: Iterable[ExtractedPage],
    *,
    target_chars: int = 1600,
    overlap_chars: int = 220,
    min_chars: int = 120,
) -> list[LegalChunk]:
    """Chunk legal text while retaining article/chapter headings and page ranges."""
    if target_chars < 400 or overlap_chars < 0 or overlap_chars >= target_chars:
        raise ValueError("Kích thước chunk/overlap không hợp lệ")
    units = _units(pages)
    chunks: list[LegalChunk] = []
    buffer: list[_Unit] = []
    size = 0

    def flush() -> None:
        nonlocal buffer, size
        if not buffer:
            return
        content = "\n\n".join(unit.text for unit in buffer).strip()
        if len(content) >= min_chars or not chunks:
            chunks.append(
                LegalChunk(
                    chunk_index=len(chunks),
                    page_from=min(unit.page for unit in buffer),
                    page_to=max(unit.page for unit in buffer),
                    heading=next((unit.heading for unit in reversed(buffer) if unit.heading), None),
                    content=content,
                    content_sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
                )
            )
        overlap: list[_Unit] = []
        overlap_size = 0
        for unit in reversed(buffer):
            remaining = overlap_chars - overlap_size
            if remaining <= 0:
                break
            tail = unit.text[-remaining:]
            overlap.insert(0, _Unit(unit.page, unit.heading, tail))
            overlap_size += len(tail)
        buffer = overlap
        size = overlap_size

    for unit in units:
        # Split pathological OCR paragraphs without dropping any text.
        parts = [unit.text[index : index + target_chars] for index in range(0, len(unit.text), target_chars)]
        for part in parts:
            part_unit = _Unit(unit.page, unit.heading, part)
            if buffer and size + len(part) + 2 > target_chars:
                flush()
            buffer.append(part_unit)
            size += len(part) + 2
    flush()
    return chunks
