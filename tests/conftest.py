"""Shared test fixtures. Everything runs offline with deterministic fallbacks."""

from __future__ import annotations

import pathlib

import pytest
from auralynq.config import reload_settings
from auralynq.ingest.models import Chunk, SourceType
from auralynq.utils import seed_everything


@pytest.fixture(autouse=True)
def _isolated_env(tmp_path, monkeypatch):
    """Force fully-local fallbacks and a temp data dir for every test."""
    monkeypatch.setenv("AURALYNQ_EMBEDDING__PROVIDER", "hash")
    monkeypatch.setenv("AURALYNQ_VECTOR__BACKEND", "memory")
    monkeypatch.setenv("AURALYNQ_LLM__PROVIDER", "extractive")
    monkeypatch.setenv("AURALYNQ_VOICE__ASR_PROVIDER", "null")
    monkeypatch.setenv("AURALYNQ_VOICE__TTS_PROVIDER", "null")
    monkeypatch.setenv("AURALYNQ_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("AURALYNQ_REPORTS_DIR", str(tmp_path / "reports"))
    # Silence logs in tests (also avoids structlog's cached stream being closed
    # across repeated in-process CLI invocations under CliRunner).
    monkeypatch.setenv("AURALYNQ_LOG_LEVEL", "CRITICAL")
    reload_settings()
    seed_everything(42)
    # reset cached singletons that read settings
    from auralynq.embeddings import factory as ef
    from auralynq.vectorstore import factory as vf

    ef.get_embedder.cache_clear()
    vf.get_store.cache_clear()
    yield
    reload_settings()


@pytest.fixture
def sample_texts() -> list[str]:
    return [
        "PathRAG prunes relational paths using a resource-flow algorithm.",
        "Flow-based pruning scores each graph path by its reliability.",
        "The capital of France is Paris, a city on the Seine.",
        "Reciprocal rank fusion combines dense and sparse rankings.",
        "Maximal marginal relevance removes redundant retrieved chunks.",
    ]


@pytest.fixture
def sample_chunks(sample_texts) -> list[Chunk]:
    return [
        Chunk(
            id=f"c{i}",
            doc_id="doc1",
            text=t,
            ordinal=i,
            source="sample.md",
            source_type=SourceType.markdown,
        )
        for i, t in enumerate(sample_texts)
    ]


@pytest.fixture
def corpus_dir(tmp_path) -> pathlib.Path:
    d = tmp_path / "corpus"
    d.mkdir()
    (d / "pathrag.md").write_text(
        "# PathRAG\n\nPathRAG is a graph retrieval method. It performs node "
        "retrieval, then relational path expansion, then flow-based pruning to "
        "keep only reliable paths. Paths are scored by reliability and rendered "
        "to text with golden-region ordering.\n\n"
        "## Hybrid retrieval\n\nAuralynq fuses dense and sparse vectors with "
        "reciprocal rank fusion, then reranks with a cross-encoder and applies "
        "maximal marginal relevance.\n",
        encoding="utf-8",
    )
    (d / "geography.txt").write_text(
        "Paris is the capital of France. France is a country in Europe. "
        "The Seine river flows through Paris.\n",
        encoding="utf-8",
    )
    return d
