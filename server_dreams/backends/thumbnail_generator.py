from __future__ import annotations

import subprocess
from pathlib import Path


def build_thumbnail(image_path: Path, out_path: Path, title_text: str, width: int = 1280, height: int = 720) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    safe = title_text.replace("'", "").replace(":", "-")
    vf = (
        f"scale={width}:{height},"
        "eq=contrast=1.1:saturation=1.12,"
        f"drawbox=x=0:y={int(height*0.62)}:w=iw:h={int(height*0.38)}:color=black@0.68:t=fill,"
        f"drawbox=x=0:y={int(height*0.58)}:w=iw:h={int(height*0.04)}:color=0x35f5cc@0.86:t=fill,"
        "drawtext=text='SERVER DREAMS':x=42:y=h*0.595:fontsize=40:fontcolor=0x90ffd0,"
        f"drawtext=text='{safe}':x=42:y=h*0.67:fontsize=62:fontcolor=white:line_spacing=10:box=0"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(image_path),
        "-vf",
        vf,
        "-frames:v",
        "1",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path
