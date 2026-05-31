"""Auralynq command-line interface.

Commands lazily import their subsystems so ``import auralynq.cli`` stays cheap and
the CLI works even when optional extras are absent (they degrade to fallbacks).
"""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from auralynq import __version__
from auralynq.config import get_settings

app = typer.Typer(
    name="auralynq",
    help="Auralynq — Talk to Your Data. Local-first agentic voice RAG with PathRAG.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


def _bootstrap():
    from auralynq.telemetry import configure_logging

    s = get_settings()
    configure_logging(level=s.log_level, json=s.log_json)
    s.ensure_dirs()
    return s


@app.callback(invoke_without_command=True)
def _main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version and exit."),
):
    if version:
        console.print(f"auralynq {__version__}")
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        raise typer.Exit()


@app.command()
def ingest(
    input: Path = typer.Argument(..., help="File or directory to ingest."),
    recursive: bool = typer.Option(True, help="Recurse into directories."),
) -> None:
    """Ingest documents/audio into chunks with spans and timestamps.

    Example: auralynq ingest data/corpus --recursive
    """
    _bootstrap()
    from auralynq.ingest.pipeline import ingest_path

    result = ingest_path(input, recursive=recursive)
    console.print(
        f"[green]✓[/] ingested {result.n_documents} documents → "
        f"{result.n_chunks} chunks ({result.n_skipped} unchanged/skipped)"
    )


@app.command()
def index(
    input: Path = typer.Option(Path("data/corpus"), help="Corpus directory."),
    rebuild: bool = typer.Option(False, help="Drop and rebuild the index."),
) -> None:
    """Build the vector index and knowledge graph.

    Example: auralynq index --input data/corpus
    """
    _bootstrap()
    from auralynq.pipeline import build_index

    stats = build_index(input, rebuild=rebuild)
    table = Table(title="Index built")
    table.add_column("metric")
    table.add_column("value", justify="right")
    for k, v in stats.items():
        table.add_row(k, str(v))
    console.print(table)


@app.command()
def ask(
    question: str = typer.Argument(..., help="Your question."),
    final_k: int | None = typer.Option(None, help="Number of context chunks."),
    show_trace: bool = typer.Option(False, "--trace", help="Print the agent trajectory."),
    json_out: bool = typer.Option(False, "--json", help="Emit JSON."),
) -> None:
    """Ask a question and get a grounded, cited answer.

    Example: auralynq ask "How does PathRAG prune paths?" --trace
    """
    _bootstrap()
    from auralynq.agent.runner import answer_question

    result = answer_question(question, final_k=final_k)
    if json_out:
        console.print_json(json.dumps(result.to_dict()))
        return
    console.print(Panel(result.answer, title="Answer", border_style="cyan"))
    if result.citations:
        table = Table(title="Citations")
        table.add_column("#")
        table.add_column("source")
        table.add_column("span/timestamp")
        for i, c in enumerate(result.citations, 1):
            table.add_row(str(i), c.get("source", "?"), c.get("locator", ""))
        console.print(table)
    if show_trace:
        for span in result.trace:
            console.print(f"  [dim]{span['name']}[/] {span['duration_ms']}ms")


@app.command()
def talk(
    audio: Path | None = typer.Option(None, help="Audio file (skip live mic)."),
    speak: bool = typer.Option(True, help="Speak the answer via TTS."),
) -> None:
    """Voice query: ASR → agent → grounded answer → optional TTS.

    Example: auralynq talk --audio question.wav
    """
    _bootstrap()
    from auralynq.voice.loop import run_voice_turn

    result = run_voice_turn(audio_path=audio, speak=speak)
    console.print(Panel(result.transcript, title="Heard", border_style="magenta"))
    console.print(Panel(result.answer, title="Answer", border_style="cyan"))
    if result.audio_out_path:
        console.print(f"[green]✓[/] spoken answer → {result.audio_out_path}")


@app.command()
def eval(
    report: bool = typer.Option(False, "--report", help="Write a full report to reports/."),
    smoke: bool = typer.Option(False, "--smoke", help="Tiny smoke eval for CI."),
) -> None:
    """Run the evaluation harness (Ragas + retrieval metrics + WER).

    Example: auralynq eval --report
    """
    _bootstrap()
    from auralynq.eval.report import run_eval

    out = run_eval(smoke=smoke, write_report=report)
    console.print_json(json.dumps(out))


@app.command()
def bench(
    report: bool = typer.Option(False, "--report", help="Write benchmark report to reports/."),
) -> None:
    """Benchmark Qdrant recall/latency/memory across quantization modes.

    Example: auralynq bench --report
    """
    _bootstrap()
    from auralynq.eval.bench import run_bench

    out = run_bench(write_report=report)
    console.print_json(json.dumps(out))


@app.command()
def data(
    sample: bool = typer.Option(True, help="Download small sample subsets."),
    full: bool = typer.Option(False, help="Download full datasets."),
) -> None:
    """Download evaluation datasets (text + voice). Never requires paid keys.

    Example: auralynq data --sample
    """
    _bootstrap()
    from scripts.download_data import download

    download(sample=sample and not full, full=full)


@app.command()
def serve(
    host: str | None = typer.Option(None),
    port: int | None = typer.Option(None),
    reload: bool = typer.Option(False),
) -> None:
    """Start the FastAPI backend (SSE chat + WebSocket voice).

    Example: auralynq serve --port 8000
    """
    s = _bootstrap()
    import uvicorn

    uvicorn.run(
        "auralynq.serving.app:app",
        host=host or s.serve.host,
        port=port or s.serve.port,
        reload=reload,
    )


@app.command()
def mcp() -> None:
    """Start the auralynq-mcp server over stdio."""
    _bootstrap()
    from auralynq.mcp_server.server import main as mcp_main

    mcp_main()


@app.command()
def info() -> None:
    """Show resolved providers and configuration (what's actually running)."""
    _bootstrap()
    from auralynq.providers import describe_providers

    table = Table(title="Auralynq — resolved providers")
    table.add_column("subsystem")
    table.add_column("provider")
    table.add_column("status")
    for row in describe_providers():
        table.add_row(row["subsystem"], row["provider"], row["status"])
    console.print(table)


if __name__ == "__main__":
    app()
