# Artifact Checklist (submission-time)

Modeled on ACL/NeurIPS reproducibility checklists.

## Code & environment
- [ ] `auralynq[dev,eval]` install documented; Python 3.11+.
- [ ] `make research-smoke` passes offline at $0.
- [ ] ruff + mypy + pytest green.
- [ ] Exact dependency versions captured (pyproject + lock or freeze).

## Data
- [ ] Each dataset's source + license recorded (`metadata.license`).
- [ ] No raw benchmark data committed (git-ignored `data/research/`).
- [ ] Subset sizes and selection seed reported.

## Experiments
- [ ] Every reported number traces to a `runs/<id>/metrics.json`.
- [ ] `provenance.json` present for each run (commit, config, seed, hardware).
- [ ] CIs reported where N permits; proxy metrics labeled `*_proxy`.
- [ ] No fabricated / hand-edited results.

## Models
- [ ] Open-model names + Ollama tags listed; sizes/quantization recorded.
- [ ] No automatic large-model pulls (AUTO_PULL default false).
- [ ] API models clearly optional; pricing source cited for any cost estimate.

## Reporting integrity
- [ ] LLM-judge outputs never presented as ground truth; agreement study included.
- [ ] Honest abstention preserved; limitations section complete.
- [ ] All `[VERIFY]` citations cleared before camera-ready.

## Secrets
- [ ] No secrets in repo or run artifacts (`tests/test_research_*` asserts this).
- [ ] Only `.env.example` placeholders committed.
