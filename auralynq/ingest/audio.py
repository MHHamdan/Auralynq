"""Audio ingestion: transcribe → diarize → timestamped, speaker-labelled chunks."""

from __future__ import annotations

from pathlib import Path

from auralynq.ingest.models import AudioSegment, Chunk, SourceType
from auralynq.voice.asr import ASRSegment
from auralynq.voice.diarize import diarize_segments
from auralynq.voice.factory import build_asr


def transcribe_to_chunks(
    path: Path,
    doc_id: str,
    *,
    target_chars: int = 600,
    diarize: bool = True,
) -> tuple[str, str, list[Chunk]]:
    """Return (title, language, chunks) for an audio document.

    Consecutive ASR segments from the same speaker are packed into chunks (up to
    ``target_chars``) so each chunk carries a coherent timestamped, speaker-
    attributed span for citation.
    """
    asr = build_asr()
    transcript = asr.transcribe(path)
    segments: list[ASRSegment] = transcript.segments
    if diarize:
        segments = diarize_segments(path, segments)

    chunks: list[Chunk] = []
    buf: list[ASRSegment] = []
    ordinal = 0

    def flush() -> None:
        nonlocal ordinal
        if not buf:
            return
        text = " ".join(s.text.strip() for s in buf).strip()
        if not text:
            buf.clear()
            return
        seg = AudioSegment(start_s=buf[0].start_s, end_s=buf[-1].end_s, speaker=buf[0].speaker)
        chunks.append(
            Chunk(
                id=Chunk.make_id(doc_id, ordinal),
                doc_id=doc_id,
                text=text,
                ordinal=ordinal,
                audio=seg,
                source=path.name,
                source_type=SourceType.audio,
                title=path.stem,
                metadata={"asr_provider": transcript.provider, "language": transcript.language},
            )
        )
        ordinal += 1
        buf.clear()

    cur_len = 0
    cur_speaker = None
    for seg in segments:
        if (cur_speaker is not None and seg.speaker != cur_speaker) or cur_len > target_chars:
            flush()
            cur_len = 0
        buf.append(seg)
        cur_speaker = seg.speaker
        cur_len += len(seg.text)
    flush()
    return path.stem, transcript.language, chunks
