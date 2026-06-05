# Auralynq Phase 2 — Research Plan

**Working title (lead candidate):** *Auralynq: Observable, Local-First Agentic
RAG for Calibrated Document-Grounded Answering, Abstention, and
Hallucination-Risk Evaluation.*

**Branch:** `feat/research-phase2-agentic-rag-eval` · **Date:** 2026-06-03

## 1. Thesis

Transform Auralynq from an engineering artifact into a **research-grade,
reproducible framework** that, on one pipeline, measures: evidence sufficiency,
calibrated abstention, citation faithfulness, agentic routing correctness, and
trace-level observability — across **open-source (Ollama) models** — and tests
whether **trace features predict hallucination risk**. See
[`literature-gap-analysis.md`](./literature-gap-analysis.md) for the grounded gap.

## 2. Contributions (defensible set — detail in `../research/paper_contribution_strategy.md`)

- **C1 — Evidence Sufficiency Controller (ESC):** transparent, feature-based
  decision (retrieval scores, reranker margin, citation coverage, graph-path
  support, snippet agreement) for *answer vs. abstain*.
- **C2 — Calibrated Abstention:** maps ESC features to a risk score + confidence
  band; evaluated with AURC, ECE/Abstain-ECE, Brier, selective accuracy,
  coverage–risk, unsupported-answer rate.
- **C3 — Observable Agentic Trace + hallucination-risk prediction:** a typed
  per-query trace; study of which trace features predict wrong/unsupported answers.
- **C4 — Local-first open-model benchmarking:** same pipeline, swap Ollama models;
  report groundedness, abstention, citation, latency, and resource/privacy tradeoff.
- **C5 — Retrieval × routing × abstention ablation:** dense / hybrid / +rerank /
  +graph / +ESC / full-agentic, plus corpus-vs-web routing.

## 3. Scope guardrails (from the brief)

- No fabricated references; no fake results (TODO markers until experiments run).
- No automatic large-model or large-dataset downloads (env-gated).
- No paid APIs required; secrets only as `.env.example` placeholders.
- Preserve honest abstention — never tune Auralynq to hallucinate for nicer numbers.
- App stays functional; the research layer is additive (`auralynq/research/`).

> **Path note:** the brief referenced `backend/app/research/...`; this repo's
> package is `auralynq/`, so all research code lives under `auralynq/research/`.
> The LaTeX paper lives under `docs/paper/` and is **git-ignored** (kept local /
> built on Overleaf) per the request.

## 4. Workstreams & artifacts

| WS | Output | State |
|----|--------|-------|
| Literature | `literature-gap-analysis.md`, `literature_matrix.csv` | ✅ drafted |
| Questions | `research-questions.md` | ✅ |
| Datasets | `benchmark-datasets.md`, `dataset-setup.md`, adapters | ✅ scaffold |
| Models | `model-ablation-plan.md`, `ollama-model-recommendations.md`, profiles | ✅ scaffold |
| Metrics | `evaluation-metrics.md`, `auralynq/research/metrics.py` | ✅ |
| Sufficiency/calibration | `evidence_sufficiency.py`, `calibration.py` | ✅ heuristic v0 |
| Judges | `auralynq/research/evaluators/*` | ✅ |
| Runner/trace | `auralynq/research/runner.py`, `runs/<id>/` | ✅ |
| Configs | `configs/research/*.yaml` | ✅ |
| Protocol | `experimental-protocol.md`, `reproducibility.md` | ✅ |
| Paper | `docs/paper/*` | ✅ scaffold, TODO results |
| Smoke | `runs/smoke_*`, `generated/smoke_summary.md` | ✅ |

## 5. Phased timeline

1. **P2.0 (this PR):** research layer foundation + smoke validation + paper scaffold.
2. **P2.1:** wire 1–2 real benchmark subsets (CRAG-mini, RGB negative-rejection),
   run small ablations, learned calibrator (logistic regression).
3. **P2.2:** full open-model sweep, trace-feature hallucination-risk study,
   judge-agreement study, fill paper results + figures.
4. **P2.3:** writing, internal review, arXiv tech report → target venue submission.

## 6. Definition of done (this PR) — matches brief acceptance criteria

Research plan ✅ · literature matrix ✅ · contributions ✅ · benchmark adapter
architecture ✅ · Ollama ablation plan ✅ · sufficiency+calibration module ✅ ·
metrics module ✅ · trace-level logging ✅ · paper scaffold ✅ · ≥1 smoke
experiment ✅ · no fake results ✅ · no secrets ✅ · app functional ✅.
