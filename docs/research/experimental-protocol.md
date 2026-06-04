# Experimental Protocol

## Run lifecycle
1. `auralynq-research run --config <cfg> --dataset <name> --output runs/<id>`
2. For each example: build pipeline from config → answer → ESC/calibration →
   judges (optional) → metrics → write `traces/<question_id>.json`.
3. `runs/<id>/` contains: `provenance.json`, `config.snapshot.yaml`,
   `results.json` (per-example), `metrics.json` (aggregate), `traces/`.
4. `auralynq-research evaluate --run runs/<id>` recomputes aggregate metrics.
5. `auralynq-research compare --runs ...` / `export-paper-tables` build tables.

## Controls / fairness
- **One factor per comparison.** Pinned factors recorded in `provenance.json`.
- Same dataset subset + same seed (`AURALYNQ_SEED`, default 42) across compared runs.
- Same prompts/templates across models; temperature pinned (default 0.1).
- Abstention thresholds set on a **dev split**, frozen before the test split.

## Provenance (every run records)
git commit hash · config file + snapshot · dataset name+version/hash · model name ·
provider · embedding model · retrieval mode · hardware summary · random seed ·
**env var names only (values redacted)** · timestamp · run duration.

## Statistical reporting
- Bootstrap 95% CIs for headline metrics when N ≥ 30.
- Paired comparisons (same questions) use paired bootstrap / McNemar for binary outcomes.
- Multiple-comparison note when sweeping many configs.

## Reproducibility
- `make research-smoke` must pass offline at $0 (extractive/hash fallbacks).
- Seeds fixed; non-determinism (LLM sampling) reported and minimized (temp=0.1).
- See [`reproducibility.md`](./reproducibility.md) and
  [`artifact-checklist.md`](./artifact-checklist.md).

## Ethics & safety
- Honest abstention preserved; no tuning toward hallucination.
- No secrets in artifacts (a test asserts this).
- Datasets used under their licenses; raw data never committed.
