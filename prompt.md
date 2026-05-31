# Claude Code Build Prompt — Auralynq: "Talk to Your Data"

> Paste everything below into Claude Code. This prompt is designed for autonomous execution. Claude Code must make senior engineering decisions, implement the project end-to-end, and never pause to ask clarifying questions. When a decision is ambiguous, choose the strongest practical default used in production-grade FAANG-style engineering, document it in `DECISIONS.md`, and continue.

---

## 0. Global project identity

The project name is **Auralynq**.

Use the name consistently everywhere:

* Product name: `Auralynq`
* Python package: `auralynq`
* CLI command: `auralynq`
* MCP server package/command: `auralynq-mcp`
* Container image/container prefixes: `auralynq-*`
* Main repository folder: `auralynq/`
* Web UI branding: `Auralynq`
* Tagline: `"Talk to Your Data"`

Strict naming rules:

1. Use **Auralynq** as the only product name.
2. Use `auralynq` for package names, folders, CLI commands, modules, scripts, and service names.
3. Keep **PathRAG** unchanged only when referring to the graph-retrieval algorithm or paper.
4. Before finalizing, run a repository-wide name audit and confirm that all product/package/service references use the Auralynq naming convention.
5. If any inconsistent product naming remains, rename it before continuing.
6. Record the final naming convention in `DECISIONS.md`.

---

## 1. Operating contract

You are an autonomous senior ML/infra engineer. Build a production-grade, portfolio-quality, agentic voice-enabled RAG system named **Auralynq**.

Auralynq lets users talk to their own data by text or voice and receive grounded, cited answers, optionally spoken back. It ingests text and audio sources, builds a hybrid vector index and a relational knowledge graph, and answers through an adaptive agentic RAG loop whose graph path uses **PathRAG**.

Hard rules:

1. Do not ask clarifying questions.
2. Make optimal implementation decisions yourself.
3. Document important decisions in `DECISIONS.md` using short ADRs:

   * context
   * decision
   * rationale
   * alternatives rejected
4. Everything must run locally at `$0` by default.
5. The only required secret is `HUGGINGFACE_TOKEN`.
6. All other providers must be optional and detected from environment variables.
7. Missing paid API keys must never break the local demo.
8. Prefer Apache-2.0 / MIT-compatible components where possible.
9. Attribute third-party code, papers, datasets, and models in `THIRD_PARTY.md`.
10. Work in small, verifiable phases.
11. After each phase, run relevant tests, linting, type checks, and smoke checks.
12. Fix failures before moving to the next phase.
13. Do not oversell results. Any README benchmark claim must come from the implemented evaluation harness.
14. Optimize for correctness, maintainability, reproducibility, observability, and a clean demo experience.

---

## 2. Mission

Build **Auralynq**, an agentic voice-enabled RAG platform for private data.

Core product promise:

> Talk to your documents, audio, and knowledge base. Get grounded answers with citations, source spans, speaker labels, and timestamps.

Auralynq must support:

* text query → cited answer
* voice query → ASR → cited answer → optional TTS
* document ingestion
* audio ingestion with transcription and diarization
* hybrid vector retrieval
* PathRAG graph retrieval
* adaptive routing between fast retrieval and deep graph retrieval
* evaluation
* tracing
* benchmarking
* CLI
* FastAPI backend
* MCP server
* web UI

---

## 3. Container runtime requirement

The user does **not** have Docker installed.

Use **Podman** as the default container runtime.

Container rules:

1. Do not require Docker.
2. Do not assume Docker is installed.
3. Use Podman-compatible containers and Compose files.
4. Prefer `podman compose` when available.
5. Support `podman-compose` as a fallback.
6. Auto-detect the available Podman Compose command in scripts and Makefile targets.
7. If neither Podman Compose option exists, print a clear setup message and stop gracefully.
8. Keep Compose configuration compatible with Podman.
9. Use `compose.yml` as the Compose file name.
10. Documentation, Makefile targets, README quickstart, and local deployment instructions must use Podman.

Create:

```text
containers/
compose.yml
scripts/check_container_runtime.sh
```

The runtime check script must expose a reusable command detector:

```bash
#!/usr/bin/env bash
set -euo pipefail

if podman compose version >/dev/null 2>&1; then
  echo "podman compose"
elif command -v podman-compose >/dev/null 2>&1; then
  echo "podman-compose"
else
  echo "Podman Compose is required. Install either 'podman compose' or 'podman-compose'." >&2
  exit 1
fi
```

The Makefile must expose:

```makefile
runtime-check
stack-up
stack-down
stack-logs
stack-build
```

Expected behavior:

```bash
make runtime-check
make stack-build
make stack-up
make stack-logs
make stack-down
```

`make stack-up` must start:

* Qdrant
* API
* worker
* web UI
* Phoenix tracing

---

## 4. Non-negotiable implementation requirements

Implement the following capabilities.

### 4.1 Ingestion

Support:

* PDF
* DOCX
* HTML
* Markdown
* TXT
* WAV
* MP3
* M4A

Requirements:

* layout-aware PDF parsing
* semantic chunking
* late chunking where useful
* audio transcription
* speaker diarization
* timestamp preservation
* source-span preservation
* idempotent ingestion
* metadata-rich document records
* incremental re-indexing

---

### 4.2 Indexes

Build two complementary indexes:

1. **Vector index**

   * Qdrant
   * dense vectors
   * sparse vectors
   * hybrid retrieval
   * metadata filters
   * payload indexes
   * quantization support
   * benchmarked recall/latency/memory trade-offs

2. **Relational knowledge graph**

   * entities
   * relations
   * provenance
   * source spans
   * audio timestamps
   * reliability scores
   * graph paths for PathRAG retrieval

---

### 4.3 Retrieval

Implement:

* naive baseline retriever
* hybrid dense+sparse retriever
* reciprocal rank fusion
* cross-encoder reranking
* MMR deduplication
* lost-in-the-middle context reordering
* PathRAG graph retrieval:

  * node retrieval
  * relational path expansion
  * flow-based path pruning
  * path reliability scoring
  * path-to-text prompting
  * golden-region ordering

PathRAG implementation must be isolated under:

```text
auralynq/retrieval/pathrag/
```

If adapting third-party implementation details, isolate the adapted code, add attribution, and document license details in `THIRD_PARTY.md`.

---

### 4.4 Agentic LangGraph loop

Implement a LangGraph state machine with these nodes:

1. Planner
2. Adaptive router
3. Hybrid retriever
4. PathRAG retriever
5. Context fusion
6. Evidence-gap critic
7. Query rewrite / retry loop
8. Synthesizer
9. Self-check
10. Citation validator
11. Response streamer

Requirements:

* explicit latency budgets
* explicit iteration caps
* route simple queries to the fast path
* route relational/multi-hop queries to PathRAG
* support hybrid routing when uncertain
* trace every node
* expose trajectory in the UI
* keep unsupported claims out of final answers

---

### 4.5 Voice

Implement voice input and output:

* faster-whisper default ASR
* WhisperX alignment when available
* pyannote diarization using `HUGGINGFACE_TOKEN`
* Silero VAD
* Kokoro-82M default TTS
* streaming push-to-talk loop
* audio timestamp citations
* speaker-aware citations

The end-to-end voice demo must support:

```text
push-to-talk → VAD → ASR → agent → grounded answer → TTS
```

---

### 4.6 Serving

Implement a FastAPI backend with:

* async architecture
* SSE token streaming for chat
* WebSocket endpoint for voice
* ingest endpoint
* text query endpoint
* voice query endpoint
* health endpoint
* metrics endpoint
* eval-report endpoint
* structured error responses
* request IDs
* basic rate limiting
* safe file handling

---

### 4.7 MCP server

Implement an MCP server named:

```text
auralynq-mcp
```

Expose tools:

* `ingest_documents`
* `search`
* `graph_path_query`
* `transcribe`
* `talk_to_data`
* `run_eval`
* `get_trace`

The MCP server must be callable from an MCP-compatible client.

---

### 4.8 Web UI

Build a Next.js + React + Tailwind UI.

Required UI features:

* chat interface
* streaming tokens
* visible citations
* push-to-talk microphone
* waveform or recording indicator
* live partial transcript
* final transcript
* spoken answer toggle
* retrieval trace panel
* evidence path viewer
* dataset/ingest panel
* eval report viewer
* clean portfolio-ready design

The UI should look professional, minimal, and demo-ready.

---

### 4.9 CLI

Implement:

```bash
auralynq ingest
auralynq ask
auralynq talk
auralynq eval
auralynq bench
auralynq data
auralynq serve
auralynq mcp
```

The CLI must provide helpful errors, examples, and `--help` output.

---

## 5. Recommended default stack

Use these defaults unless a better choice is documented in `DECISIONS.md`.

### Orchestration

* LangGraph
* LangChain or LlamaIndex only where they reduce complexity
* Pydantic v2 for typed state/config models

### Embeddings

Default:

* `BAAI/bge-m3`

Requirements:

* dense retrieval
* sparse retrieval
* multilingual support
* local execution
* provider abstraction
* optional paid provider upgrades via environment variables

### Reranking

Default:

* BGE reranker v2 or another strong local cross-encoder that fits the demo environment

Optional upgrade:

* Cohere rerank when `COHERE_API_KEY` exists

### Vector database

Default:

* Qdrant via Podman

Requirements:

* named vectors when useful
* payload indexes
* quantization benchmark
* metadata filtering
* hybrid dense+sparse strategy

### Generation LLM

Default:

* local open model through Ollama or vLLM

Requirements:

* provider abstraction
* streaming tokens
* local default
* optional upgrade to commercial providers when keys exist
* no hard failure when optional keys are missing

### ASR

Default:

* faster-whisper

Optional:

* WhisperX
* pyannote diarization
* stronger GPU ASR backends if available

### TTS

Default:

* Kokoro-82M

### Observability

Default:

* OpenTelemetry
* structured logs
* Phoenix local tracing

Optional:

* Langfuse when keys exist

### Evaluation

Use:

* Ragas
* retrieval metrics
* jiwer
* frozen golden set
* drift check

---

## 6. Real datasets

Create:

```text
scripts/download_data.py
```

Requirements:

* use Hugging Face `datasets`
* support `--sample`
* support `--full`
* cache downloads
* verify checksums where practical
* never require paid keys
* use `HUGGINGFACE_TOKEN` where dataset access requires authentication

Text datasets:

* HotpotQA
* MuSiQue
* 2WikiMultiHopQA
* a Wikipedia subset or MS MARCO sample

Voice datasets:

* LibriSpeech
* Common Voice sample where access is available
* FLEURS sample where practical
* one spoken-knowledge corpus sample where practical

The default demo must be small enough to run on a laptop.

---

## 7. Repository layout

Use this layout exactly unless a superior choice is documented in `DECISIONS.md`:

```text
auralynq/
  auralynq/
    config/
    ingest/
    embeddings/
    vectorstore/
    retrieval/
      hybrid/
      pathrag/
      router.py
    agent/
    llm/
    voice/
    eval/
    serving/
    telemetry/
  web/
  scripts/
  tests/
  containers/
    compose.yml
  reports/
  docs/
  Makefile
  .env.example
  pyproject.toml
  README.md
  DECISIONS.md
  THIRD_PARTY.md
  LICENSE
  CONTRIBUTING.md
  .github/workflows/ci.yml
```

---

## 8. Engineering quality bar

Use production-grade engineering practices.

Requirements:

* Python 3.12
* typed Python package
* pydantic v2
* pydantic-settings
* ruff linting and formatting
* mypy clean
* pytest
* unit tests
* integration tests
* one true end-to-end smoke test
* ≥80% coverage on retrieval/agent/eval core
* deterministic seeds where practical
* pinned dependencies
* uv or Poetry lockfile
* pre-commit hooks
* no secrets in code
* `.env` gitignored
* safe file handling
* structured logging
* request tracing
* OpenTelemetry spans
* GitHub Actions CI
* reproducible `make demo`

---

## 9. README requirements

The README must be portfolio-grade and honest.

Include, in this order:

1. One-line pitch
2. Demo GIF/video placeholder:

   * `docs/demo.gif`
3. Architecture diagram using Mermaid
4. Why the project is technically interesting
5. Quickstart using Podman
6. Configuration table
7. Provider table:

   * local default
   * optional upgrade
   * required environment variable
8. Benchmarks table with measured values only:

   * Ragas faithfulness
   * answer relevancy
   * context precision
   * recall@k
   * nDCG@10
   * MRR
   * ASR WER
   * latency
   * memory
9. Retrieval comparison:

   * naive
   * hybrid
   * PathRAG
   * full agentic Auralynq
10. Architecture notes
11. Design decisions link
12. Limitations
13. Roadmap
14. License

Do not invent benchmark numbers. If a metric was not measured, state that it is pending.

---

## 10. Makefile targets

Implement:

```makefile
setup
runtime-check
data
index
run
serve
mcp
test
lint
typecheck
coverage
eval
bench
demo
stack-build
stack-up
stack-down
stack-logs
clean
```

Expected core commands:

```bash
make setup
make runtime-check
make data
make index
make demo
make eval
make bench
make stack-up
make stack-down
```

---

## 11. Acceptance criteria

All criteria must pass before calling the project complete.

1. `make runtime-check` confirms Podman Compose support.
2. `make setup` installs dependencies.
3. `make data` downloads sample text and voice datasets.
4. `make index` builds the vector index and knowledge graph.
5. `make demo` runs locally with only `HUGGINGFACE_TOKEN`.
6. Demo answers a typed question with grounded citations.
7. Demo answers a spoken question with speaker/timestamp citations.
8. The adaptive router sends simple questions to the fast path.
9. The adaptive router sends relational or multi-hop questions to PathRAG.
10. The trace panel shows retrieval path and evidence paths.
11. `make eval` writes reports under `reports/`.
12. `make bench` reports Qdrant recall/latency/memory trade-offs.
13. `make stack-up` starts Qdrant, API, worker, UI, and Phoenix using Podman.
14. `auralynq-mcp` exposes callable MCP tools.
15. CI passes:

    * ruff
    * mypy
    * pytest
    * coverage threshold
    * eval smoke
16. README uses measured benchmark values only.
17. Repository naming is consistent with Auralynq across package, CLI, services, UI, docs, and config.

---

## 12. Execution plan

Proceed phase by phase.

### Phase 1 — Scaffold

Create:

* repository structure
* Python package
* pyproject
* config system
* `.env.example`
* Makefile
* Podman Compose setup
* CI skeleton
* initial README
* DECISIONS.md
* THIRD_PARTY.md

Run:

```bash
make lint
make typecheck
make test
```

Commit.

---

### Phase 2 — Data

Implement:

* dataset downloader
* sample mode
* full mode
* cache handling
* dataset manifests

Run:

```bash
make data
make test
```

Commit.

---

### Phase 3 — Ingestion

Implement:

* document parsers
* audio transcription
* diarization integration
* chunking
* metadata extraction
* source-span tracking
* timestamp tracking

Run:

```bash
make test
```

Commit.

---

### Phase 4 — Indexing

Implement:

* Qdrant client
* hybrid vector indexing
* sparse vector support
* metadata filters
* knowledge graph builder
* graph persistence

Run:

```bash
make index
make test
```

Commit.

---

### Phase 5 — Retrieval

Implement:

* naive retriever
* hybrid retriever
* RRF
* reranking
* MMR
* PathRAG
* adaptive router

Run:

```bash
make test
```

Commit.

---

### Phase 6 — Agent

Implement:

* LangGraph state
* planner
* router node
* retrieval nodes
* critic
* rewrite loop
* synthesizer
* self-check
* citation validator
* semantic cache
* tracing

Run:

```bash
make test
```

Commit.

---

### Phase 7 — Voice

Implement:

* ASR provider interface
* TTS provider interface
* VAD
* streaming voice loop
* speaker/timestamp citation output

Run:

```bash
make test
```

Commit.

---

### Phase 8 — Serving

Implement:

* FastAPI app
* SSE streaming
* WebSocket voice endpoint
* MCP server
* health/metrics/eval endpoints

Run:

```bash
make test
make stack-up
make stack-down
```

Commit.

---

### Phase 9 — Web UI

Implement:

* chat UI
* voice UI
* trace panel
* evidence viewer
* ingest panel
* eval report viewer

Run:

```bash
make test
```

Commit.

---

### Phase 10 — Evaluation and benchmarks

Implement:

* Ragas metrics
* retrieval metrics
* ASR WER
* Qdrant quantization benchmark
* report generation
* frozen golden-set drift check

Run:

```bash
make eval
make bench
```

Commit.

---

### Phase 11 — Documentation and hardening

Finalize:

* README
* architecture diagram
* measured benchmark table
* limitations
* roadmap
* THIRD_PARTY.md
* DECISIONS.md
* CI
* coverage
* demo flow

Run:

```bash
make demo
make lint
make typecheck
make test
make eval
make bench
```

Final commit and tag:

```bash
git tag v0.1.0
```

---

## 13. Final instruction

Begin now.

Make all decisions yourself.

Build **Auralynq** as a clean, reproducible, production-ready, portfolio-grade project.

Prioritize:

1. correctness
2. reproducibility
3. clean architecture
4. observability
5. measurable evaluation
6. professional UI/UX
7. local-first execution
8. Podman-based deployment
9. honest documentation
10. maintainable code
