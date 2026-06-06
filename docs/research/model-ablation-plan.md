# Model Ablation Plan

Goal: hold the Auralynq pipeline fixed and vary one factor at a time. Each cell is
a `configs/research/*.yaml` config; results land in `runs/<id>/`.

## A. Retrieval ablation (RQ5)
1. dense only — `baseline_vector.yaml`
2. sparse/BM25 only *(if keyword index available)*
3. hybrid dense+sparse — `hybrid_retrieval.yaml`
4. hybrid + reranker — `rerank_only.yaml`
5. graph expansion only — `graph_rag.yaml`
6. vector + graph
7. vector + graph + reranker
8. vector + graph + reranker + ESC — `abstention_calibrated.yaml`
9. full agentic pipeline — `full_agentic.yaml`

## B. Agentic routing ablation (RQ6)
no router · simple classifier · agentic router · agentic router + trace verification.

## C. Abstention ablation (RQ1/RQ2)
none · score threshold · evidence-sufficiency heuristic · calibrated sufficiency ·
judge-assisted sufficiency.

## D. Model ablation (RQ4) — open-source first, API optional
- Ollama small: `ollama_small.yaml`
- Ollama balanced: `ollama_balanced.yaml`
- Ollama server: `ollama_server.yaml`
- embedding models: BGE-M3 (default) vs nomic-embed-text vs mxbai-embed-large
- rerankers: bge-reranker-v2-m3 vs none
- API model (only if a key is present): optional comparison column.

## E. Corpus-type ablation (RQ5)
clean PDFs · noisy extracted PDFs · scanned/OCR · multilingual · text+table.

## Reporting

Each ablation produces a row in the generated tables (`export-paper-tables`):
retrieval (Recall@k, nDCG, MRR), generation (faithfulness, citation P/R,
unsupported rate), abstention (AURC, ECE, selective acc), efficiency (p50/p95
latency, tokens/s, est. memory). One factor changes per row; the rest are pinned
and recorded in `provenance.json`. Significance via bootstrap CIs where N permits.
