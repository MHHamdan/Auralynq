# Dataset Setup (manual)

Auralynq **never auto-downloads** benchmark data. To enable any download you must
set both:

```bash
AURALYNQ_RESEARCH__ALLOW_DATASET_DOWNLOAD=true
AURALYNQ_RESEARCH__MAX_EXAMPLES=100        # subset cap (default 100)
AURALYNQ_RESEARCH__DATA_DIR=./data/research # git-ignored
```

Place data under `$AURALYNQ_RESEARCH__DATA_DIR/<dataset>/`. Adapters read from
there and normalize to the common schema. List what's available:

```bash
auralynq-research list-datasets
```

## Per-dataset instructions

### custom_corpus (no download needed)
Point at any local folder of docs already ingested into Auralynq, plus a
`qa.jsonl` of `{question, gold_answer, supporting:[...]}`. Used for the smoke run.

### CRAG (arXiv:2406.04744)
Repo: `facebookresearch/CRAG`. Download per their license, place the QA JSONL at
`data/research/crag/`. The adapter maps `domain`, web/KG flags, and
`requires_abstention` from CRAG's answerability labels.

### RAGBench (arXiv:2407.11005)
HuggingFace `rungalileo/ragbench`. Place a subset parquet/JSONL at
`data/research/ragbench/`. Adapter maps TRACe fields into `metadata`.

### MIRAGE-Bench (arXiv:2410.13716)
`vectara/mirage-bench`. Multilingual; adapter sets `language` per example —
feeds the language-mismatch trace feature.

### T2-RAGBench (arXiv:2506.12071)
Text+table financial QA; adapter sets `requires_table_reasoning=true`.

### ARES tasks (arXiv:2311.09476)
Used for judge cross-checking, not as primary QA. Place under `data/research/ares/`.

## Reminder
Datasets carry their own licenses. The adapter records `metadata.license`; raw
data is git-ignored and never redistributed via this repo.
