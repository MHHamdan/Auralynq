"""LLM factory with ``auto`` resolution + extractive fallback."""

from __future__ import annotations

import functools
import importlib.util

import httpx

from auralynq.config import get_settings
from auralynq.llm.base import LLM
from auralynq.llm.fallback import ExtractiveLLM
from auralynq.telemetry import get_logger

_log = get_logger("auralynq.llm")


def _ollama_reachable(base_url: str) -> bool:
    try:  # pragma: no cover - network probe
        httpx.get(base_url.rstrip("/") + "/api/tags", timeout=0.5)
        return True
    except Exception:
        return False


def build_llm(provider: str | None = None) -> LLM:
    s = get_settings()
    provider = provider or s.llm.provider

    if provider == "auto":
        if s.anthropic_api_key and importlib.util.find_spec("anthropic"):
            provider = "anthropic"
        elif s.openai_api_key and importlib.util.find_spec("openai"):
            provider = "openai"
        elif _ollama_reachable(s.llm.base_url):
            provider = "ollama"
        else:
            provider = "extractive"

    try:
        if provider == "ollama":
            from auralynq.llm.providers import OllamaLLM

            return OllamaLLM(s.llm.model, s.llm.base_url)
        if provider == "openai":
            from auralynq.llm.providers import OpenAILLM

            return OpenAILLM(s.openai_api_key, s.llm.model)
        if provider == "anthropic":
            from auralynq.llm.providers import AnthropicLLM

            return AnthropicLLM(s.anthropic_api_key, s.llm.model)
    except Exception as exc:  # pragma: no cover
        _log.warning("llm.fallback_extractive", error=str(exc))

    _log.info("llm.using", provider="extractive")
    return ExtractiveLLM()


def resolved_provider() -> str:
    s = get_settings()
    if s.llm.provider != "auto":
        return s.llm.provider
    if s.anthropic_api_key and importlib.util.find_spec("anthropic"):
        return "anthropic"
    if s.openai_api_key and importlib.util.find_spec("openai"):
        return "openai"
    if _ollama_reachable(s.llm.base_url):
        return "ollama"
    return "extractive"


@functools.lru_cache(maxsize=1)
def get_llm() -> LLM:
    return build_llm()
