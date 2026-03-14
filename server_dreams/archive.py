from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


class ArchiveManager:
    def __init__(self, root_dir: str):
        self.root = Path(root_dir)

    def run_dir(self, day: dt.date) -> Path:
        d = self.root / f"{day.year:04d}" / f"{day.month:02d}" / f"{day.day:02d}"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def write_json(self, path: Path, payload: dict) -> None:
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
