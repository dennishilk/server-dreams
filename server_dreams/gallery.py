from __future__ import annotations

import json
from pathlib import Path


def build_gallery(archive_root: Path, out_html: Path) -> Path:
    rows: list[str] = []
    for manifest in sorted(archive_root.glob("*/*/*/manifest.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        rel = manifest.parent.relative_to(archive_root)
        title = data.get("metadata", {}).get("title", "Untitled")
        scene = data.get("concept", {}).get("scene", "")
        rows.append(f"<li><b>{title}</b><br/><small>{rel}</small><br/>{scene}</li>")

    html = (
        "<html><head><meta charset='utf-8'><title>Server Dreams Gallery</title></head><body>"
        "<h1>Server Dreams Archive</h1><ul>"
        + "\n".join(rows)
        + "</ul></body></html>"
    )
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(html, encoding="utf-8")
    return out_html
