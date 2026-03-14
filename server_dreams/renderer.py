from __future__ import annotations

import subprocess
from pathlib import Path


def render_video(
    ffmpeg_bin: str,
    image_path: Path,
    audio_path: Path,
    title_text: str,
    out_path: Path,
    duration_seconds: int,
) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg_bin,
        "-y",
        "-loop",
        "1",
        "-i",
        str(image_path),
        "-i",
        str(audio_path),
        "-t",
        str(duration_seconds),
        "-vf",
        "scale=1920:1080,zoompan=z='min(zoom+0.0004,1.08)':d=125:s=1920x1080,drawtext=text='" + title_text.replace("'", "") + "':x=40:y=h-80:fontsize=36:fontcolor=white",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-shortest",
        str(out_path),
    ]
    subprocess.run(cmd, check=True)
    return out_path
