# Evaluation Metrics

Implemented in `auralynq/research/metrics.py`. Formulas chosen to match the
literature so numbers are comparable (citations in `literature_matrix.csv`).

## Retrieval
- **Recall@k, Precision@k, nDCG@k, MRR** — reuse `auralynq.eval.retrieval_metrics`.
- **Context precision / recall / relevance** — fraction of retrieved contexts that
  overlap gold contexts (token-overlap proxy; RAGAS-style optional).

## Generation / grounding
- **Answer relevance** — embedding cosine (question, answer) when embedder present;
  else token-overlap proxy.
- **Exact match / token-F1** — when gold short answers exist.
- **Semantic similarity** — embedding cosine (answer, gold) if available.
- **Citation coverage / precision / recall** — ALCE-style: do cited spans support
  the sentences they're attached to (heuristic overlap v0; judge upgrade later).
- **Faithfulness / groundedness** — fraction of answer sentences supported by
  retrieved contexts (heuristic NLI proxy; LLM-judge optional).
- **Unsupported-claim rate** — 1 − groundedness.

## Abstention / calibration (core contribution)
- **Abstention rate** — fraction abstained.
- **Selective accuracy** — accuracy on the answered subset.
- **Coverage–risk curve** + **AURC** (area under risk–coverage) — lower is better.
- **ECE** (Guo et al. 2017, arXiv:1706.04599) + **Abstain-ECE** (abstention survey,
  arXiv:2407.18418).
- **Brier score** of the confidence vs. correctness.
- **False-answer rate** — answered but wrong/unsupported.
- **False-abstention rate** — abstained but evidence was sufficient.
- **Unsupported-answer rate**, **grounded-answer rate**.

## Trace / observability
- total / retrieval / rerank / generation latency.
- **trace completeness** — fraction of expected steps that emitted a span.
- failure-step distribution; fallback frequency; provider error rate.

## Efficiency
- tokens in/out; time-to-first-token; throughput (tokens/s); est. memory;
  local-model latency; API cost estimate *(only if pricing configured)*.

## Honesty rules
- Proxy metrics are **labeled `*_proxy`** in output so they are never mistaken for
  judge/human scores.
- Every metric records `n` and, where N permits, a bootstrap 95% CI.
- No metric is back-filled with synthetic ground truth.
