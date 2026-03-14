from __future__ import annotations

import datetime as dt
import json
import shutil
from pathlib import Path


class ArchiveManager:
    def __init__(self, root_dir: str):
        self.root = Path(root_dir)

    def run_dir(self, day: dt.date, mode: str = "latest") -> Path:
        if mode == "dated":
            d = self.root / f"{day.year:04d}" / f"{day.month:02d}" / f"{day.day:02d}"
            d.mkdir(parents=True, exist_ok=True)
            return d

        self.root.mkdir(parents=True, exist_ok=True)
        for child in self.root.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
        return self.root

    def write_json(self, path: Path, payload: dict) -> None:
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
