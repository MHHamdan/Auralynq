"""Maximal Marginal Relevance (Carbonell & Goldstein, 1998) de-duplication."""

from __future__ import annotations

import numpy as np

from auralynq.embeddings.base import Embedder
from auralynq.retrieval.models import ScoredChunk


def mmr_rerank(
    query_dense: np.ndarray,
    candidates: list[ScoredChunk],
    embedder: Embedder,
    k: int,
    lambda_mult: float = 0.6,
) -> list[ScoredChunk]:
    """Select k chunks balancing relevance to the query and novelty vs. selected."""
    if not candidates:
        return []
    k = min(k, len(candidates))
    doc_emb = embedder.embed([c.chunk.text for c in candidates]).dense
    q = np.asarray(query_dense, dtype=np.float32)

    def cos(a: np.ndarray, b: np.ndarray) -> float:
        denom = float(np.linalg.norm(a) * np.linalg.norm(b)) or 1.0
        return float(np.dot(a, b) / denom)

    rel = np.array([cos(q, doc_emb[i]) for i in range(len(candidates))])
    selected: list[int] = []
    remaining = list(range(len(candidates)))
    while remaining and len(selected) < k:
        best_i, best_score = remaining[0], -1e9
        for i in remaining:
            redundancy = max((cos(doc_emb[i], doc_emb[j]) for j in selected), default=0.0)
            score = lambda_mult * rel[i] - (1 - lambda_mult) * redundancy
            if score > best_score:
                best_score, best_i = score, i
        selected.append(best_i)
        remaining.remove(best_i)
    out = []
    for rank, idx in enumerate(selected):
        c = candidates[idx].model_copy(update={"rank": rank})
        out.append(c)
    return out
