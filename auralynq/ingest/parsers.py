"""Document parsers → plain text with page/section structure preserved.

Text/Markdown/HTML parse with zero heavy deps. PDF (pypdf) and DOCX (python-docx)
need the ``ingest`` extra and are imported lazily. PDF parsing is layout-aware in
the sense that page boundaries are preserved as character ranges so citations can
report page numbers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from auralynq.ingest.models import SourceType
from auralynq.utils import normalize_text

_EXT_MAP = {
    ".pdf": SourceType.pdf,
    ".docx": SourceType.docx,
    ".html": SourceType.html,
    ".htm": SourceType.html,
    ".md": SourceType.markdown,
    ".markdown": SourceType.markdown,
    ".txt": SourceType.text,
    ".text": SourceType.text,
    ".rst": SourceType.text,
}
AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}


@dataclass
class ParsedDoc:
    text: str
    source_type: SourceType
    title: str | None = None
    language: str = "en"
    # (page_number, start_char, end_char) for PDFs; empty otherwise.
    pages: list[tuple[int, int, int]] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def page_for(self, start_char: int) -> int | None:
        for page, lo, hi in self.pages:
            if lo <= start_char < hi:
                return page
        return None


def detect_type(path: Path) -> SourceType:
    if path.suffix.lower() in AUDIO_EXTS:
        return SourceType.audio
    return _EXT_MAP.get(path.suffix.lower(), SourceType.unknown)


def parse_document(path: Path) -> ParsedDoc:
    st = detect_type(path)
    if st is SourceType.pdf:
        return _parse_pdf(path)
    if st is SourceType.docx:
        return _parse_docx(path)
    if st is SourceType.html:
        return _parse_html(path)
    if st in (SourceType.markdown, SourceType.text, SourceType.unknown):
        return _parse_text(path, st if st is not SourceType.unknown else SourceType.text)
    raise ValueError(f"Unsupported document type for parsing: {path}")


def _parse_text(path: Path, st: SourceType) -> ParsedDoc:
    raw = path.read_text(encoding="utf-8", errors="replace")
    title = _first_heading(raw) or path.stem
    return ParsedDoc(text=normalize_text(raw), source_type=st, title=title)


def _parse_html(path: Path) -> ParsedDoc:
    raw = path.read_text(encoding="utf-8", errors="replace")
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        title = (soup.title.string if soup.title else None) or path.stem
        text = soup.get_text("\n")
    except ImportError:  # fallback: strip tags with regex
        title = path.stem
        text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return ParsedDoc(text=normalize_text(text), source_type=SourceType.html, title=title)


def _parse_pdf(path: Path) -> ParsedDoc:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    parts: list[str] = []
    pages: list[tuple[int, int, int]] = []
    cursor = 0
    for i, page in enumerate(reader.pages, start=1):
        text = normalize_text(page.extract_text() or "")
        if not text:
            continue
        parts.append(text)
        start = cursor
        cursor += len(text) + 2  # account for the "\n\n" join
        pages.append((i, start, cursor))
    full = "\n\n".join(parts)
    meta: object = reader.metadata or {}
    title = getattr(meta, "title", None) or path.stem
    return ParsedDoc(
        text=full,
        source_type=SourceType.pdf,
        title=str(title),
        pages=pages,
        metadata={"n_pages": len(reader.pages)},
    )


def _parse_docx(path: Path) -> ParsedDoc:
    import docx

    document = docx.Document(str(path))
    paras = [p.text for p in document.paragraphs]
    text = normalize_text("\n\n".join(p for p in paras if p.strip()))
    title = next((p for p in paras if p.strip()), path.stem)
    return ParsedDoc(text=text, source_type=SourceType.docx, title=title[:120])


_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+)$", re.MULTILINE)


def _first_heading(text: str) -> str | None:
    m = _HEADING_RE.search(text)
    return m.group(1).strip() if m else None
