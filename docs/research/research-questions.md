# Research Questions

Each RQ names the metric(s) that answer it (defined in
[`evaluation-metrics.md`](./evaluation-metrics.md)) and the contribution it backs.

## Primary

- **RQ1 (Sufficiency → C1).** Can a transparent, feature-based Evidence
  Sufficiency Controller decide *answer vs. abstain* better than a single
  retrieval-score threshold?
  *Metrics:* AURC ↓, selective accuracy ↑, false-answer rate ↓, false-abstention
  rate, at matched coverage.

- **RQ2 (Calibration → C2).** Are Auralynq's confidence / hallucination-risk
  scores *calibrated* for document-grounded answering?
  *Metrics:* ECE, Abstain-ECE, Brier score, reliability diagrams, coverage–risk curve.

- **RQ3 (Trace predictivity → C3).** Which trace features (route, coverage,
  reranker margin, #supporting chunks, graph-path support, provider fallback,
  language mismatch) predict an unsupported / wrong answer?
  *Metrics:* feature importance / AUROC of a risk classifier; correlation with
  judge-labeled unsupported-claim rate.

- **RQ4 (Open models → C4).** Holding the pipeline fixed, how do open-source
  (Ollama) models compare on groundedness, abstention behavior, citation
  faithfulness, latency, and resource cost?
  *Metrics:* grounded-answer rate, unsupported-answer rate, citation
  precision/recall, abstention precision, p50/p95 latency, tokens/s, est. memory.

## Secondary

- **RQ5 (Retrieval ablation → C5).** Marginal value of hybrid, reranking, and
  graph expansion for sufficiency-aware answering?
  *Metrics:* Recall@k, nDCG@k, MRR; downstream grounded-answer & abstention rates.

- **RQ6 (Routing → C5).** Does the agentic corpus-vs-web router reduce
  "answered from wrong source" errors vs. no router / simple classifier?
  *Metrics:* routing accuracy, source-confusion rate, downstream faithfulness.

- **RQ7 (Judge reliability → C3).** How well do heuristic, LLM, and
  benchmark-label judges agree on "supported / should-abstain"?
  *Metrics:* Cohen's κ / Krippendorff's α across judges; per-failure-mode
  agreement (GroUSE-style).

## Falsifiable predictions (honest science)

- H1: ESC lowers AURC vs. score-threshold at equal coverage. *Falsified if* AURC
  is statistically indistinguishable.
- H2: At least one trace feature has non-trivial predictive power (AUROC > 0.65)
  for unsupported answers. *Falsified if* all features ≈ chance.
- H3: Smaller open models abstain *less* appropriately (higher false-answer rate)
  than larger ones at fixed thresholds. *Falsified if* no monotone trend.

We report negative results. Abstention behavior is never tuned to inflate metrics.
