# Auralynq API / worker image. Multi-stage, rootless-friendly.
FROM docker.io/library/python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System deps for audio + parsing (kept minimal). ffmpeg powers audio decode.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libsndfile1 curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first for layer caching.
COPY pyproject.toml README.md ./
COPY auralynq ./auralynq
RUN pip install -e ".[ingest,eval,vector]"

COPY scripts ./scripts

# Non-root user (rootless containers map this safely).
RUN useradd -m -u 10001 auralynq && chown -R auralynq:auralynq /app
USER auralynq

EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=5s --retries=5 \
    CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["uvicorn", "auralynq.serving.app:app", "--host", "0.0.0.0", "--port", "8000"]
