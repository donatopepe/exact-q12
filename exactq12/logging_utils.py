from __future__ import annotations

import json
from pathlib import Path
from time import time_ns
from typing import Any


class JsonlLogger:
    def __init__(self, path: str | Path | None) -> None:
        self.path = Path(path) if path else None

    def write(self, event: str, **fields: Any) -> None:
        if self.path is None:
            return
        record = {"time_ns": time_ns(), "event": event, **fields}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
