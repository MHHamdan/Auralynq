from __future__ import annotations

from auralynq.cli import app
from auralynq.providers import describe_providers, health_snapshot
from auralynq.voice.asr import NullASR
from auralynq.voice.diarize import _heuristic
from auralynq.voice.factory import build_asr, build_tts
from typer.testing import CliRunner

runner = CliRunner()


def test_cli_version():
    res = runner.invoke(app, ["--version"])
    assert res.exit_code == 0
    assert "auralynq" in res.stdout


def test_cli_help_lists_commands():
    res = runner.invoke(app, ["--help"])
    assert res.exit_code == 0
    for cmd in ("ingest", "ask", "talk", "eval", "bench", "data", "serve", "mcp", "index"):
        assert cmd in res.stdout


def test_cli_ingest_and_ask(corpus_dir):
    res = runner.invoke(app, ["index", "--input", str(corpus_dir)])
    assert res.exit_code == 0, res.stdout
    from auralynq.agent import runner as ar

    ar._CACHE.clear()
    res2 = runner.invoke(app, ["ask", "What is the capital of France?", "--json"])
    assert res2.exit_code == 0, res2.stdout
    assert "answer" in res2.stdout


def test_cli_info(corpus_dir):
    res = runner.invoke(app, ["info"])
    assert res.exit_code == 0
    assert "embeddings" in res.stdout


def test_describe_providers_resolves_fallbacks():
    rows = {r["subsystem"]: r["provider"] for r in describe_providers()}
    assert rows["embeddings"] == "hash"
    assert rows["vector_store"] == "memory"
    assert rows["llm"] == "extractive"
    assert rows["asr"] == "null"


def test_health_snapshot():
    snap = health_snapshot()
    assert snap["status"] == "ok"
    assert "providers" in snap


def test_factory_fallbacks():
    assert build_asr().name == "null"
    assert build_tts().name == "null"
    assert isinstance(build_asr(), NullASR)


def test_diarize_heuristic_alternates_on_pause():
    from auralynq.voice.asr import ASRSegment

    segs = [ASRSegment(0.0, 1.0, "a"), ASRSegment(3.0, 4.0, "b")]  # >1s gap
    out = _heuristic(segs)
    assert out[0].speaker != out[1].speaker
