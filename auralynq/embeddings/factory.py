"""Embedder factory with ``auto`` resolution (ADR-0004)."""

from __future__ import annotations

import functools
import importlib.util

from auralynq.config import get_settings
from auralynq.embeddings.base import Embedder
from auralynq.embeddings.hashing import HashingEmbedder
from auralynq.telemetry import get_logger

_log = get_logger("auralynq.embeddings")


def _have(pkg: str) -> bool:
    return importlib.util.find_spec(pkg) is not None


def build_embedder(provider: str | None = None) -> Embedder:
    s = get_settings()
    provider = provider or s.embedding.provider

    if provider == "auto":
        if _have("FlagEmbedding"):
            provider = "bge"
        elif s.openai_api_key and _have("openai"):
            provider = "openai"
        else:
            provider = "hash"

    if provider == "bge":
        try:
            from auralynq.embeddings.bge import BGEM3Embedder

            return BGEM3Embedder(
                model=s.embedding.model, device=s.embedding.device, dim=s.embedding.dim
            )
        except Exception as exc:  # pragma: no cover - heavy path
            _log.warning("embeddings.bge_failed_fallback_hash", error=str(exc))
            provider = "hash"

    if provider == "openai":  # pragma: no cover - paid path
        try:
            from auralynq.embeddings.openai_embed import OpenAIEmbedder

            return OpenAIEmbedder(api_key=s.openai_api_key)
        except Exception as exc:
            _log.warning("embeddings.openai_failed_fallback_hash", error=str(exc))
            provider = "hash"

    _log.info("embeddings.using", provider="hash")
    return HashingEmbedder(dim=min(s.embedding.dim, 256))


@functools.lru_cache(maxsize=1)
def get_embedder() -> Embedder:
    return build_embedder()


def resolved_provider() -> str:
    s = get_settings()
    if s.embedding.provider != "auto":
        return s.embedding.provider
    if _have("FlagEmbedding"):
        return "bge"
    if s.openai_api_key and _have("openai"):
        return "openai"
    return "hash"
