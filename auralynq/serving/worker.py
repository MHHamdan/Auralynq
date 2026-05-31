"""Background ingestion worker.

Watches ``<data_dir>/inbox`` for new files, ingests + indexes them, then moves
them to ``<data_dir>/processed``. Runs in the ``auralynq-worker`` container. This
is a deliberately simple file-queue worker; swap for a real broker at scale.
"""

from __future__ import annotations

import shutil
import time

from auralynq.config import get_settings
from auralynq.pipeline import build_index
from auralynq.telemetry import configure_logging, get_logger

_log = get_logger("auralynq.worker")


def process_once() -> int:
    s = get_settings()
    inbox = s.data_dir / "inbox"
    processed = s.data_dir / "processed"
    inbox.mkdir(parents=True, exist_ok=True)
    processed.mkdir(parents=True, exist_ok=True)
    pending = [p for p in inbox.iterdir() if p.is_file()]
    if not pending:
        return 0
    stats = build_index(inbox, rebuild=False)
    for p in pending:
        shutil.move(str(p), str(processed / p.name))
    _log.info("worker.processed", files=len(pending), **stats)
    return len(pending)


def main(poll_seconds: float = 5.0) -> None:  # pragma: no cover - long-running
    s = get_settings()
    configure_logging(level=s.log_level, json=s.log_json)
    _log.info("worker.start", inbox=str(s.data_dir / "inbox"))
    while True:
        try:
            process_once()
        except Exception as exc:
            _log.warning("worker.error", error=str(exc))
        time.sleep(poll_seconds)


if __name__ == "__main__":  # pragma: no cover
    main()
