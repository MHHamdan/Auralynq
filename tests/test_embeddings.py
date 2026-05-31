from __future__ import annotations

import numpy as np
from auralynq.embeddings import HashingEmbedder, get_embedder, resolved_provider


def test_hashing_embedder_is_deterministic():
    e1 = HashingEmbedder(dim=128)
    e2 = HashingEmbedder(dim=128)
    a = e1.embed(["flow based pruning"]).dense
    b = e2.embed(["flow based pruning"]).dense
    assert np.allclose(a, b)


def test_embedding_similarity_ranks_overlap_higher(sample_texts):
    emb = HashingEmbedder(dim=256)
    batch = emb.embed(sample_texts)
    q = emb.embed_query("flow based pruning of graph paths")
    sims = [emb.cosine(q.dense, batch.dense[i]) for i in range(len(sample_texts))]
    # The flow-pruning sentences should outrank the Paris sentence.
    assert sims[1] > sims[2]
    assert sims[0] > sims[2]


def test_sparse_vectors_present(sample_texts):
    emb = HashingEmbedder(dim=64)
    batch = emb.embed(sample_texts)
    assert len(batch.sparse) == len(sample_texts)
    assert all(isinstance(sp, dict) and sp for sp in batch.sparse)


def test_factory_resolves_hash_in_test_env():
    assert resolved_provider() == "hash"
    assert get_embedder().name == "hash"
