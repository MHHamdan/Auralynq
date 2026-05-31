"""End-to-end indexing pipeline: corpus → vector index + knowledge graph.

Ties together ingestion, embeddings, the vector store and the PathRAG knowledge
graph. Persists both indexes so retrieval/agent can run in a fresh process.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from auralynq.config import get_settings
from auralynq.embeddings.factory import get_embedder
from auralynq.ingest.models import Chunk
from auralynq.ingest.pipeline import ingest_path
from auralynq.retrieval.pathrag.builder import build_from_chunks
from auralynq.retrieval.pathrag.graph import KnowledgeGraph
from auralynq.telemetry import get_logger
from auralynq.utils import chunked
from auralynq.vectorstore.factory import get_store
from auralynq.vectorstore.memory_store import MemoryStore

_log = get_logger("auralynq.pipeline")


def graph_path() -> Path:
    return get_settings().index_dir / "graph.json"


def build_index(input_dir: Path, rebuild: bool = False) -> dict[str, Any]:
    s = get_settings()
    s.ensure_dirs()
    store = get_store()
    embedder = get_embedder()

    if rebuild:
        store.clear()

    result = ingest_path(Path(input_dir), recursive=True, force=rebuild)
    all_chunks: list[Chunk] = [c for d in result.documents for c in d.chunks]

    n_indexed = 0
    for batch in chunked(all_chunks, s.embedding.batch_size):
        emb = embedder.embed([c.text for c in batch])
        n_indexed += store.upsert(batch, emb)

    if isinstance(store, MemoryStore):
        store.save()

    # Build / update the knowledge graph from all chunks seen this run.
    kg = build_from_chunks(all_chunks)
    kg.save(graph_path())

    stats = {
        "backend": store.backend,
        "embedder": embedder.name,
        "documents": result.n_documents,
        "skipped": result.n_skipped,
        "chunks_indexed": n_indexed,
        "store_count": store.count(),
        "entities": kg.n_entities,
        "relations": kg.n_relations,
    }
    _log.info("index.built", **stats)
    return stats


def load_graph() -> KnowledgeGraph:
    p = graph_path()
    if p.exists():
        return KnowledgeGraph.load(p)
    return KnowledgeGraph()
