# Benchmark Datasets

All datasets are normalized by adapters in `auralynq/research/datasets/` into the
**common schema** (see `base.py` / `NormalizedExample`):

```json
{
  "question_id": "...", "question": "...", "gold_answer": "...",
  "gold_contexts": ["..."], "source_documents": ["..."],
  "domain": "...", "language": "...", "task_type": "...",
  "requires_abstention": false, "requires_multihop": false,
  "requires_table_reasoning": false, "metadata": {}
}
```

**No dataset is downloaded automatically.** Downloads require
`AURALYNQ_RESEARCH__ALLOW_DATASET_DOWNLOAD=true` and are capped by
`AURALYNQ_RESEARCH__MAX_EXAMPLES` (default 100). Manual instructions:
[`dataset-setup.md`](./dataset-setup.md).

## Priority datasets (verified)

| Adapter | Dataset | Why it fits a contribution | Source |
|---------|---------|----------------------------|--------|
| `custom_corpus` | Auralynq mini / your corpus | smoke + corpus-vs-web routing | local |
| `crag` | CRAG (4,409 QA, web+KG mock) | abstention labels, routing (C2/C5) | arXiv:2406.04744 |
| `ragbench` | RAGBench (TRACe) | adherence/completeness ↔ sufficiency (C1) | arXiv:2407.11005 |
| `mirage` | MIRAGE-Bench (18 langs) | multilingual + language-mismatch feature (C3/C4) | arXiv:2410.13716 |
| `t2_ragbench` | T2-RAGBench (text+table) | table-reasoning corpus ablation (C5) | arXiv:2506.12071 |
| `ares` | ARES eval tasks | judge-reliability cross-check (C3) | arXiv:2311.09476 |

RGB (arXiv:2309.01431) negative-rejection testbed is the clearest *abstention*
signal and is planned via a thin adapter in P2.1.

## Subset-first policy

Start at **20–100 examples/dataset** for reproducible, $0, offline-friendly runs;
scale later. Every run records the dataset name, version/hash, and example count
in `runs/<id>/provenance.json`.

## Licensing / ethics

Each adapter records the dataset's license in `metadata.license` and refuses to
redistribute raw data through the repo. Users place data under
`AURALYNQ_RESEARCH__DATA_DIR` (default `./data/research`, git-ignored).
