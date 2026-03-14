from __future__ import annotations

import subprocess
from pathlib import Path

from .image_base import ImageBackend
from server_dreams.concept_engine import Concept


class DummyImageBackend(ImageBackend):
    def generate(self, concept: Concept, out_path: Path, width: int, height: int) -> Path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        text = f"SERVER DREAMS | {concept.scene} | Mood: {concept.mood}".replace("'", "")
        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c=#111433:s={width}x{height}:d=1",
            "-vf",
            "drawtext=text='" + text + "':x=40:y=80:fontsize=32:fontcolor=white",
            "-frames:v",
            "1",
            str(out_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return out_path
