from __future__ import annotations

import argparse
import datetime as dt
import json

from .config import AppConfig
from .logging_utils import setup_logging
from .pipeline import run_daily


def _load_config(path: str) -> AppConfig:
    return AppConfig.from_file(path)


def main() -> None:
    setup_logging()

    parser = argparse.ArgumentParser(prog="server-dreams")
    parser.add_argument("command", choices=["generate", "compose-music", "render", "upload", "run-daily", "dry-run"])
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD")
    args = parser.parse_args()

    cfg = _load_config(args.config)
    day = dt.date.fromisoformat(args.date) if args.date else dt.date.today()

    if args.command in {"generate", "compose-music", "render", "upload", "run-daily"}:
        manifest = run_daily(cfg, day=day, dry_run=False)
    elif args.command == "dry-run":
        manifest = run_daily(cfg, day=day, dry_run=True)
    else:
        raise SystemExit(2)

    print(json.dumps({"date": manifest["date"], "title": manifest["metadata"]["title"]}, indent=2))


if __name__ == "__main__":
    main()
