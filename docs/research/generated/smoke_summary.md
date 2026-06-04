# Smoke Experiment Summary

> **SMOKE VALIDATION ONLY — NOT A PAPER RESULT.** Tiny synthetic corpus, the 6-item built-in `mini` benchmark, offline hash embeddings + extractive LLM. It validates that the research pipeline runs end-to-end and that abstention is honest. Real results require the benchmark datasets, real models, and larger N (see `experimental-protocol.md`).

- Generated (UTC): `20260604_042210`
- Variants: baseline_vector, full_agentic

## Headline comparison

| config | n | abstention_rate | mean_token_f1 | grounded_answer_rate | mean_citation_precision_proxy | aurc | ece | brier | sel_acc | false_answer | latency_p50_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline_vector | 6 | 0.0 | 0.2086 | 1.0 | 0.8333 | 1.0 | 0.5732 | 0.3286 | 0.0 | 1.0 | 0.53 |
| full_agentic | 6 | 0.6667 | 0.1073 | 0.3333 | 0.3333 | 0.8361 | 0.4 | 0.2909 | 0.0 | 0.3333 | 21.02 |

## Per-variant metrics (excerpt)

- **baseline_vector**: abstention_rate=0.0, grounded_answer_rate=1.0, mean_token_f1=0.2086, AURC=1.0, ECE=0.5732  ·  `/home/mhamdan/Auralynq/runs/smoke_20260604_042210/baseline_vector`
- **full_agentic**: abstention_rate=0.6667, grounded_answer_rate=0.3333, mean_token_f1=0.1073, AURC=0.8361, ECE=0.4  ·  `/home/mhamdan/Auralynq/runs/smoke_20260604_042210/full_agentic`

_Numbers come straight from each run's `metrics.json`; nothing hand-edited._

