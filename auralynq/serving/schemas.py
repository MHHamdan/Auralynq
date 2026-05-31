"""Pydantic request/response schemas for the FastAPI backend."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)
    final_k: int | None = Field(default=None, ge=1, le=50)
    use_cache: bool | None = None


class Citation(BaseModel):
    marker: int
    source: str
    locator: str = ""
    source_type: str = "unknown"
    speaker: str | None = None
    start_s: float | None = None
    end_s: float | None = None
    page: int | None = None


class QueryResponse(BaseModel):
    answer: str
    citations: list[dict[str, Any]] = Field(default_factory=list)
    route: str = "fast"
    route_confidence: float = 0.0
    route_rationale: str = ""
    path_evidence: list[dict[str, Any]] = Field(default_factory=list)
    seeds: list[str] = Field(default_factory=list)
    iterations: int = 0
    confidence: float = 0.0
    cached: bool = False
    elapsed_ms: float = 0.0
    trace: list[dict[str, Any]] = Field(default_factory=list)
    request_id: str = ""


class IngestResponse(BaseModel):
    documents: int
    chunks: int
    skipped: int
    request_id: str = ""


class VoiceResponse(BaseModel):
    transcript: str
    answer: str
    citations: list[dict[str, Any]] = Field(default_factory=list)
    route: str = "fast"
    audio_out_url: str | None = None
    asr_provider: str = "null"
    tts_provider: str | None = None
    request_id: str = ""


class HealthResponse(BaseModel):
    status: str
    version: str
    env: str
    providers: list[dict[str, str]]
    hf_token_present: bool
    index: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: str
    detail: str = ""
    request_id: str = ""
