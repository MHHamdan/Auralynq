# Literature Gap Analysis — Auralynq Phase 2

> Status: **living document**. Every citation below was verified against arXiv /
> ACL Anthology / proceedings pages during the search log dated 2026-06-03.
> The structured version lives in [`literature_matrix.csv`](./literature_matrix.csv).
> **No reference in this file is fabricated.** Where a fact could not be verified
> it is marked `[VERIFY]`.

## 1. Reproducible search log

Searches were run via the Claude Code web-search tool on **2026-06-03**. To
reproduce manually, paste each query into Google Scholar / Semantic Scholar /
arXiv full-text search. Exact queries used:

| # | Query | Primary hit (verified) |
|---|-------|------------------------|
| Q1 | `ARES automated RAG evaluation framework arxiv` | arXiv:2311.09476 |
| Q2 | `RAGBench benchmark RAG evaluation TRACe` | arXiv:2407.11005 |
| Q3 | `CRAG Comprehensive RAG Benchmark Meta KDD Cup` | arXiv:2406.04744 |
| Q4 | `Benchmarking Large Language Models in Retrieval-Augmented Generation` (RGB) | arXiv:2309.01431 |
| Q5 | `MIRAGE-Bench multilingual RAG benchmark` | arXiv:2410.13716 (NAACL'25) |
| Q6 | `GroUSE benchmark grounded question answering evaluators LLM judge` | arXiv:2409.06595 (COLING'25) |
| Q7 | `FaithBench hallucination benchmark summarization Vectara` | arXiv:2410.13210 (NAACL'25) |
| Q8 | `RAGAS automated evaluation retrieval augmented generation` | arXiv:2309.15217 (EACL'24) |
| Q9 | `selective prediction abstention large language models calibration` | arXiv:2407.18418 (TACL'25), arXiv:2407.16221 |
| Q10 | `PathRAG pruning graph-based RAG relational paths` | arXiv:2502.14902 |
| Q11 | `GraphRAG From Local to Global query-focused summarization Microsoft` | arXiv:2404.16130 |
| Q12 | `agentic retrieval augmented generation survey` | arXiv:2501.09136 |
| Q13 | `Judging LLM-as-a-Judge MT-Bench Chatbot Arena` | arXiv:2306.05685 (NeurIPS'23) |
| Q14 | `Lewis 2020 Retrieval-Augmented Generation Knowledge-Intensive NLP Tasks` | arXiv:2005.11401 (NeurIPS'20) |
| Q15 | `On Calibration of Modern Neural Networks Guo 2017 ECE` | arXiv:1706.04599 (ICML'17) |
| Q16 | `Enabling Large Language Models to Generate Text with Citations ALCE` | arXiv:2305.14627 (EMNLP'23) |

### Still-to-check manually (access not confirmed in this session)
These are **named in the Phase-2 brief** but not yet individually verified — do
not cite them in the paper until each is confirmed against its source:

- **VLR-Bench** (visual/legal RAG) — `[VERIFY]` candidate, not yet located.
- **FaithJudge / Vectara HHEM hallucination leaderboard** — confirm exact paper vs. leaderboard artifact.
- **Legal-domain RAG hallucination benchmark** (e.g. Stanford "Hallucinating Law") — `[VERIFY]`.
- **Finance / SEC GraphRAG hallucination benchmark** — `[VERIFY]`.
- **MEMERAG** multilingual meta-eval (arXiv:2502.17163 appeared in results) — confirm before use.
- Classic IR/QA sets (BEIR, MIRACL, HotpotQA, NQ, SQuAD, TriviaQA, PubMedQA) and
  hallucination sets (HaluEval, TruthfulQA, FEVER) — well-known; cite canonical
  papers only after pulling the exact BibTeX.

## 2. What the field already covers well

- **Generation-quality / faithfulness scoring** is mature: RAGAS (L03), ARES
  (L04), RAGBench/TRACe (L06) all score faithfulness/relevance, often with
  LLM-as-judge. ALCE (L11) defines citation precision/recall.
- **Benchmark breadth**: CRAG (L05) covers web+KG QA with hallucination/missing
  labels; RGB (L02) probes noise robustness and *negative rejection*; T2-RAGBench
  (L07) covers text+table; MIRAGE-Bench (L08) covers 18 languages.
- **Judge reliability** is itself studied: MT-Bench (L15) documents judge biases;
  GroUSE (L09) meta-evaluates grounded-QA judges on 7 failure modes.
- **Graph RAG** is established: GraphRAG (L12) and PathRAG (L13).
- **Abstention/calibration theory** exists in isolation: abstention survey (L16),
  abstention-ability probing (L18), ECE/temperature scaling (L17).

## 3. What is missing (the gap)

Cross-referencing the `evaluates_*` columns of the matrix, **no single existing
system or benchmark jointly evaluates all of**:

1. **Evidence sufficiency** as an explicit, feature-based decision (RGB's
   "negative rejection" is the closest, but it is a label, not a controller with
   inspectable features).
2. **Calibrated abstention** with selective-prediction metrics (AURC, ECE/Abstain-ECE,
   Brier, coverage–risk) — calibration (L17) and abstention (L16, L18) are studied
   *separately from* RAG benchmarks.
3. **Citation faithfulness** (L11 does this, but without abstention or routing).
4. **Agentic routing decisions** (corpus-vs-web) tied to outcome quality — CRAG
   (L05) simulates web+KG but does not analyze the *routing decision* as a
   predictor of hallucination.
5. **Trace-level observability** as evaluable signal — the agentic-RAG survey
   (L14) explicitly notes the absence of standardized agentic-trace evaluation.
   **No matrix row has `evaluates_trace_observability = yes`.**
6. **Multilingual / corpus-inventory behavior** under the *same* pipeline
   (L08 is multilingual but not abstention/trace aware).
7. **Local open-source model performance** under one reproducible pipeline —
   benchmarks evaluate models, but rarely hold the *retrieval+agent pipeline*
   fixed while swapping Ollama-class models and reporting groundedness +
   abstention + citation + latency + resource cost together.

### Gap statement (the hypothesis the paper defends)

> Existing RAG evaluation isolates retrieval quality, generation faithfulness, or
> abstention/calibration, and almost always assumes a hosted frontier model.
> **There is no observable, local-first agentic RAG framework that, on a single
> reproducible pipeline, jointly measures evidence sufficiency, calibrated
> abstention, citation faithfulness, agentic routing correctness, and
> trace-level observability across open-source models — and tests whether trace
> features predict hallucination risk.**

This gap is *measurable* and *implementable*, which is the bar the brief set.

## 4. Novelty risk register

| Claim | Risk | Mitigation |
|-------|------|------------|
| "First to evaluate trace features as hallucination predictors" | Medium — adjacent work may exist | Frame as *first open, reproducible* study; cite L14's stated gap; run correlation study, report effect sizes honestly |
| "Calibrated abstention for doc-grounded RAG" | High — abstention+calibration both exist | Position as *integration + benchmarking on one pipeline*, not inventing calibration; emphasize feature-based sufficiency controller + open models |
| "Local-first open-model RAG benchmark" | Medium — CRAG/RGB use multiple LLMs | Differentiate: fixed pipeline, Ollama-class, report resource/privacy tradeoff explicitly |
| "Evidence Sufficiency Controller" as a contribution | Medium | Keep heuristics transparent + ablatable; show it beats score-threshold baselines on AURC |

**Rule for the paper:** every "first / novel" word must trace to a matrix row or
a `[VERIFY]`-cleared citation. Until verified, write "to our knowledge".
