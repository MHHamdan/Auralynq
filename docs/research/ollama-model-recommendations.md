# Ollama Model Recommendations (local-first)

Generated reference for the C4 open-model study. **Auralynq never pulls models
automatically** unless `AURALYNQ_OLLAMA__AUTO_PULL=true`. Inspect availability:

```bash
auralynq-research list-models      # detects Ollama, lists local + missing + size fit
```

Model availability changes over time; the profiles in
`auralynq/research/models/ollama_profiles.py` are the source of truth and degrade
gracefully if a tag is unavailable. Sizes below are approximate (Q4 quant).

## Small (laptop / ≤8 GB VRAM or CPU)
| Model (Ollama tag) | ~Params | ~Q4 size | Notes |
|--------------------|--------|----------|-------|
| `llama3.2:3b` | 3B | ~2.0 GB | default; good grounding for size |
| `qwen2.5:3b` | 3B | ~2.0 GB | strong multilingual |
| `gemma2:2b` | 2B | ~1.6 GB | fastest; weaker abstention |
| `phi3:mini` | 3.8B | ~2.3 GB | reasoning-leaning |

## Balanced (16–24 GB)
| `llama3.1:8b` | 8B | ~4.7 GB | strong all-rounder |
| `mistral:7b` | 7B | ~4.1 GB | concise; watch citation discipline |
| `qwen2.5:7b` | 7B | ~4.7 GB | multilingual + tables |
| `gemma2:9b` | 9B | ~5.4 GB | quality > speed |

## Server (≥40 GB / multi-GPU)
| `qwen2.5:14b` / `:32b` | 14–32B | ~9–20 GB | strong faithfulness |
| `llama3.3:70b` | 70B | ~40 GB | best quality; heavy |
| `mixtral:8x7b` | 47B MoE | ~26 GB | good throughput/quality |
| `deepseek-r1` distills | varies | varies | reasoning; verify abstention behavior |

## Embeddings
| `nomic-embed-text` | strong open default |
| `mxbai-embed-large` | higher dim, slower |
| `nomic-embed-text` v2 / `qwen3-embedding` *(if available)* | evaluate when present |

(Auralynq's built-in default embedder is BGE-M3; Ollama embeddings are an ablation axis.)

## Selection guidance
- **Privacy/cost-first, modest hardware** → small profile, expect higher
  false-answer rate; rely more on the ESC abstention gate.
- **Balanced quality/latency** → `llama3.1:8b` or `qwen2.5:7b`.
- **Quality ceiling for the paper's strong column** → server profile, but report
  latency/resource honestly.

To pull manually (the tool prints these; it does not run them unless AUTO_PULL):
```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```
