# Reproducibility

## One-command smoke ($0, offline)
```bash
make research-smoke
```
Runs a tiny synthetic mini-benchmark through vector-only vs. full-agentic+ESC
using the offline extractive/hash fallbacks (no model downloads, no keys).
Writes `runs/smoke_<ts>/{results,metrics}.json` and
`docs/research/generated/smoke_summary.md` (clearly labeled **smoke validation**).

## Reproducing a real run
```bash
auralynq-research run --config configs/research/full_agentic.yaml \
  --dataset custom_corpus --output runs/<run_id>
auralynq-research evaluate --run runs/<run_id>
auralynq-research compare --runs runs/a runs/b runs/c
auralynq-research export-paper-tables --runs runs/* --output docs/research/generated/
```

## What guarantees reproducibility
- **Seed** pinned (`AURALYNQ_SEED`, default 42).
- **Provenance** captured per run (`provenance.json`): git commit, config snapshot,
  dataset version/hash, model + provider + embedder, retrieval mode, hardware
  summary, env-var *names* (values redacted), timestamp, duration.
- **Config snapshot** (`config.snapshot.yaml`) frozen at run time.
- **Subset-first**: small N by default; downloads env-gated and capped.

## Known non-determinism
- LLM sampling: pin `temperature` (default 0.1); report variance across seeds for
  headline numbers; prefer greedy where supported.
- Reranker/embedding numerics may vary across hardware; record hardware summary.

See `artifact-checklist.md` for the submission-time checklist.
