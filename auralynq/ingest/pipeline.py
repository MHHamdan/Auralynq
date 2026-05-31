"""Ingestion pipeline: parse → chunk → provenance, with idempotent re-indexing.

A JSON manifest under ``<storage_dir>/ingest_manifest.json`` records each source's
content hash. Re-ingesting an unchanged file is skipped (idempotent); a changed
file is re-chunked and re-indexed (incremental re-indexing).
"""

from __future__ import annotations

import json
from pathlib import Path

from auralynq.config import get_settings
from auralynq.ingest.audio import transcribe_to_chunks
from auralynq.ingest.chunking import chunk_text
from auralynq.ingest.models import Chunk, Document, IngestResult, SourceSpan, SourceType
from auralynq.ingest.parsers import AUDIO_EXTS, detect_type, parse_document
from auralynq.telemetry import get_logger
from auralynq.utils import content_hash, stable_id

_log = get_logger("auralynq.ingest")

_SUPPORTED = {".pdf", ".docx", ".html", ".htm", ".md", ".markdown", ".txt", ".text", ".rst"}
_SUPPORTED |= AUDIO_EXTS


class _Manifest:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data: dict[str, str] = {}
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8"))

    def unchanged(self, key: str, digest: str) -> bool:
        return self.data.get(key) == digest

    def update(self, key: str, digest: str) -> None:
        self.data[key] = digest

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")


def ingest_file(
    path: Path, manifest: _Manifest | None = None, force: bool = False
) -> Document | None:
    """Parse and chunk one file. Returns None if unchanged (idempotent skip)."""
    path = Path(path)
    doc_id = stable_id(str(path.resolve()))
    st = detect_type(path)

    if st is SourceType.audio:
        digest = content_hash(str(path.stat().st_mtime) + str(path.stat().st_size))
        if manifest and not force and manifest.unchanged(str(path), digest):
            return None
        title, language, chunks = transcribe_to_chunks(
            path, doc_id, diarize=get_settings().voice.diarize
        )
        doc = Document(
            id=doc_id,
            source=str(path),
            source_type=SourceType.audio,
            title=title,
            language=language,
            content_hash=digest,
            chunks=chunks,
        )
        if manifest:
            manifest.update(str(path), digest)
        _log.info("ingest.audio", source=path.name, chunks=len(chunks))
        return doc

    parsed = parse_document(path)
    digest = content_hash(parsed.text)
    if manifest and not force and manifest.unchanged(str(path), digest):
        return None

    text_chunks: list[Chunk] = []
    for ordinal, tc in enumerate(chunk_text(parsed.text)):
        page = parsed.page_for(tc.start_char)
        text_chunks.append(
            Chunk(
                id=Chunk.make_id(doc_id, ordinal),
                doc_id=doc_id,
                text=tc.text,
                ordinal=ordinal,
                span=SourceSpan(
                    start_char=tc.start_char, end_char=tc.end_char, page=page, section=tc.section
                ),
                title=parsed.title,
                source=str(path),
                source_type=parsed.source_type,
                metadata={"language": parsed.language},
            )
        )
    doc = Document(
        id=doc_id,
        source=str(path),
        source_type=parsed.source_type,
        title=parsed.title,
        language=parsed.language,
        content_hash=digest,
        metadata=parsed.metadata,
        chunks=text_chunks,
    )
    if manifest:
        manifest.update(str(path), digest)
    _log.info(
        "ingest.document",
        source=path.name,
        type=parsed.source_type.value,
        chunks=len(text_chunks),
    )
    return doc


def ingest_path(target: Path, recursive: bool = True, force: bool = False) -> IngestResult:
    """Ingest a file or directory tree of supported sources."""
    s = get_settings()
    s.ensure_dirs()
    target = Path(target)
    manifest = _Manifest(s.storage_dir / "ingest_manifest.json")

    files: list[Path]
    if target.is_dir():
        it = target.rglob("*") if recursive else target.glob("*")
        files = sorted(
            p
            for p in it
            if p.is_file()
            and p.suffix.lower() in _SUPPORTED
            and not p.name.endswith(".transcript.json")
        )
    else:
        files = [target]

    result = IngestResult()
    for fp in files:
        try:
            doc = ingest_file(fp, manifest=manifest, force=force)
        except Exception as exc:  # never let one bad file abort the batch
            _log.warning("ingest.error", source=str(fp), error=str(exc))
            continue
        if doc is None:
            result.n_skipped += 1
            continue
        result.n_documents += 1
        result.n_chunks += doc.n_chunks
        result.documents.append(doc)
    manifest.save()
    return result
