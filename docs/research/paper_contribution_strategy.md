# Paper Contribution Strategy

## Strongest framing (lead)
**Observable, local-first agentic RAG for calibrated document-grounded answering
and hallucination-risk evaluation.** The wedge is *jointness on one reproducible
pipeline* + *trace observability as evaluable signal* + *open models* — none of
the matrix rows do all of this (see `literature-gap-analysis.md` §3).

## Contributions (final set)
- **C1 Evidence Sufficiency Controller** — transparent, ablatable answer/abstain decision.
- **C2 Calibrated abstention** — risk/confidence with AURC/ECE/Brier; beats score-threshold.
- **C3 Observable agentic trace + hallucination-risk prediction** — trace features → risk.
- **C4 Local-first open-model benchmark** — fixed pipeline; groundedness/abstention/citation/cost.
- **C5 Retrieval × routing × abstention ablation** — including corpus-vs-web routing.

**Strongest angle:** C3 (trace → hallucination risk) — the clearest unfilled gap.
**Backup angle:** C2 (calibrated abstention on open models) — robust even if C3's
predictive power is modest; pairs naturally with a strong systems/demo story.

## Novelty risks → see risk register in `literature-gap-analysis.md` §4
Use "to our knowledge" until each `[VERIFY]` item is cleared. Run the
judge-agreement study so LLM-judge numbers are never presented as ground truth.

## Target venues (in priority order)
1. **arXiv technical report first** (timestamp + cite-ability), then:
2. **EMNLP / ACL / NAACL — System Demonstrations** (Auralynq is a working system) —
   strong fit; aligns with RAGAS (EACL demo), GroUSE (COLING), MIRAGE/FaithBench (NAACL).
3. **Workshops:** NeurIPS / ICLR / ICML workshops on RAG, agents, evaluation,
   trustworthy/foundation-model reliability; *KnowledgeNLP*, *TrustNLP*.
4. **COLING / EACL** applied NLP (full or findings) for the evaluation-study framing.
5. **AAAI / IJCAI** applied tracks if the calibration/abstention results are strong.

Pick based on which contribution lands hardest after P2.1–P2.2 experiments:
- If C3 trace-prediction is strong → main-conference *findings* / workshop spotlight.
- If C2 calibration + C4 open-model results are the story → demo track + tech report.

## Required experiments before submission (gating)
- [ ] ≥2 real benchmark subsets wired (CRAG-mini + RGB negative-rejection).
- [ ] ESC vs. score-threshold AURC with CIs (C1/C2).
- [ ] Trace-feature risk classifier AUROC + importances (C3).
- [ ] ≥3 open models swept on the fixed pipeline with latency/resource (C4).
- [ ] Judge-agreement (heuristic vs LLM vs labels) κ/α (C3 honesty).
- [ ] Retrieval + routing ablations with significance (C5).
- [ ] All `[VERIFY]` citations cleared; BibTeX pulled from canonical sources.

## What must never happen
Fabricated numbers, fabricated citations, tuning Auralynq to hallucinate,
presenting LLM-judge output as ground truth, committing secrets/raw datasets.
