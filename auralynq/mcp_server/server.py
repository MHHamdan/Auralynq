"""``auralynq-mcp`` — MCP server exposing Auralynq tools over stdio.

Uses the official MCP Python SDK (``mcp`` extra). If the SDK is not installed,
``main()`` prints clear install guidance and exits non-zero. The tool logic lives
in :mod:`auralynq.mcp_server.tools` and is fully testable without the SDK.
"""

from __future__ import annotations

import sys

from auralynq.mcp_server.tools import (
    get_trace,
    graph_path_query,
    ingest_documents,
    run_eval,
    search,
    talk_to_data,
    transcribe,
)
from auralynq.telemetry import configure_logging, get_logger

_log = get_logger("auralynq.mcp")


def build_server():
    """Construct a FastMCP server with the seven Auralynq tools registered."""
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("auralynq-mcp")

    mcp.tool(name="ingest_documents", description="Ingest and index a file or directory.")(
        ingest_documents
    )
    mcp.tool(name="search", description="Hybrid dense+sparse search over indexed data.")(search)
    mcp.tool(name="graph_path_query", description="PathRAG relational path retrieval.")(
        graph_path_query
    )
    mcp.tool(name="transcribe", description="Transcribe and diarize an audio file.")(transcribe)
    mcp.tool(name="talk_to_data", description="Agentic, cited answer to a question.")(talk_to_data)
    mcp.tool(name="run_eval", description="Run the evaluation harness.")(run_eval)
    mcp.tool(name="get_trace", description="Return the agent trace for a question.")(get_trace)
    return mcp


def main() -> None:
    configure_logging()
    try:
        server = build_server()
    except ImportError:
        sys.stderr.write(
            "auralynq-mcp requires the MCP SDK. Install it with:\n  pip install 'auralynq[mcp]'\n"
        )
        raise SystemExit(1) from None
    _log.info("mcp.start", tools=7)
    server.run()


if __name__ == "__main__":  # pragma: no cover
    main()
