"""Structured error handling for the API."""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse


class AuralynqError(Exception):
    def __init__(self, message: str, *, status_code: int = 400, detail: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.detail = detail


async def auralynq_error_handler(request: Request, exc: AuralynqError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "detail": exc.detail,
            "request_id": getattr(request.state, "request_id", ""),
        },
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "detail": str(exc),
            "request_id": getattr(request.state, "request_id", ""),
        },
    )
