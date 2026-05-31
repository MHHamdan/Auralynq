"""LLM provider interface.

Generation is grounded-RAG oriented: the primary entry point is
``answer(question, contexts)`` / ``stream_answer(...)`` where ``contexts`` are
numbered evidence snippets. The default implementation builds a strict grounded
prompt and delegates to ``generate``/``stream``; the extractive fallback overrides
it to quote context directly (citation-faithful, no hallucination).
"""

from __future__ import annotations

import abc
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Context:
    marker: int  # 1-based citation index
    text: str
    source: str = ""
    locator: str = ""


GROUNDED_SYSTEM = (
    "You are Auralynq, a grounded question-answering assistant. Answer ONLY using "
    "the numbered context. Cite every claim with bracketed markers like [1] that "
    "refer to the context items you used. If the context does not contain the "
    "answer, say you don't have enough evidence. Be concise."
)


def build_prompt(question: str, contexts: list[Context]) -> str:
    lines = ["Context:"]
    for c in contexts:
        loc = f" ({c.source} {c.locator})".rstrip() if c.source else ""
        lines.append(f"[{c.marker}]{loc} {c.text}")
    lines.append("")
    lines.append(f"Question: {question}")
    lines.append("Answer (with [n] citations):")
    return "\n".join(lines)


class LLM(abc.ABC):
    name = "base"

    @abc.abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str: ...

    def stream(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> Iterator[str]:
        # Default: non-streaming providers yield the whole answer once.
        yield self.generate(prompt, system=system, temperature=temperature, max_tokens=max_tokens)

    def answer(self, question: str, contexts: list[Context], **kw) -> str:
        return self.generate(build_prompt(question, contexts), system=GROUNDED_SYSTEM, **kw)

    def stream_answer(self, question: str, contexts: list[Context], **kw) -> Iterator[str]:
        yield from self.stream(build_prompt(question, contexts), system=GROUNDED_SYSTEM, **kw)
