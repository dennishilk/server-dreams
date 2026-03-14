from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _coerce_scalar(value: str) -> Any:
    v = value.strip()
    if v in {"true", "True"}:
        return True
    if v in {"false", "False"}:
        return False
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1]
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        return v


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1] if stack else root

        if value == "":
            node: dict[str, Any] = {}
            parent[key] = node
            stack.append((indent, node))
        else:
            parent[key] = _coerce_scalar(value)
    return root


@dataclass
class AppConfig:
    data: dict[str, Any]

    @classmethod
    def from_file(cls, path: str | Path) -> "AppConfig":
        p = Path(path)
        raw = p.read_text(encoding="utf-8")
        if p.suffix.lower() == ".json":
            content = json.loads(raw)
        else:
            try:
                import yaml  # type: ignore

                content = yaml.safe_load(raw) or {}
            except Exception:
                content = _parse_simple_yaml(raw)
        return cls(content)

    def get(self, dotted_key: str, default: Any = None) -> Any:
        node: Any = self.data
        for part in dotted_key.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node
