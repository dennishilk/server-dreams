from __future__ import annotations

import datetime as dt
import logging
import subprocess
from pathlib import Path

from .archive import ArchiveManager
from .concept_engine import generate_concept, seed_from_date
from .config import AppConfig
from .gallery import build_gallery
from .metadata import build_metadata
from .music_engine import compose_music
from .renderer import render_video
from .youtube import YouTubeUploader, write_upload_response
from .backends.image_api import APIImageBackend
from .backends.image_dummy import DummyImageBackend
from .backends.image_local_optional import LocalOptionalImageBackend

LOGGER = logging.getLogger(__name__)


def _image_backend(name: str):
    if name == "api":
        return APIImageBackend()
    if name == "local":
        return LocalOptionalImageBackend()
    return DummyImageBackend()


def _fallback_title_card(text: str, out_path: Path, width: int = 1920, height: int = 1080) -> Path:
    safe = text.replace("'", "")
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=#080812:s={width}x{height}:d=1",
        "-vf",
        "drawtext=text='SERVER DREAMS':x=80:y=120:fontsize=42:fontcolor=0x77ffcc,"
        + "drawtext=text='"
        + safe
        + "':x=80:y=190:fontsize=32:fontcolor=white",
        "-frames:v",
        "1",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path


def run_daily(config: AppConfig, day: dt.date | None = None, dry_run: bool = False) -> dict:
    day = day or dt.date.today()
    seed = seed_from_date(day)
    concept = generate_concept(seed)
    metadata = build_metadata(concept, day)

    archive = ArchiveManager(config.get("archive.root_dir", "/var/lib/server-dreams"))
    run_dir = archive.run_dir(day)

    image_path = run_dir / "image.png"
    thumbnail_path = run_dir / "thumbnail.png"
    music_path = run_dir / "music.wav"
    video_path = run_dir / "video.mp4"

    image_backend = _image_backend(config.get("image.backend", "dummy"))
    width = int(config.get("image.width", 1920))
    height = int(config.get("image.height", 1080))

    try:
        image_backend.generate(concept, image_path, width, height)
    except Exception as exc:
        LOGGER.exception("Image generation failed: %s", exc)
        _fallback_title_card(metadata.title, image_path, width, height)

    _fallback_title_card(metadata.thumbnail_text, thumbnail_path, 1280, 720)

    try:
        compose_music(
            concept=concept,
            seed=seed,
            backend_name=config.get("music.backend", "tracker"),
            length_seconds=int(config.get("music.length_seconds", config.get("runtime.default_track_length_seconds", 45))),
            sample_rate=int(config.get("music.sample_rate", 44100)),
            out_path=music_path,
        )
    except Exception as exc:
        LOGGER.exception("Music generation failed: %s", exc)
        compose_music(concept, seed, "fallback", 45, 44100, music_path)

    render_video(
        ffmpeg_bin=config.get("runtime.ffmpeg_bin", "ffmpeg"),
        image_path=image_path,
        audio_path=music_path,
        title_text=metadata.title,
        out_path=video_path,
        duration_seconds=int(config.get("music.length_seconds", 45)),
    )

    publish = bool(config.get("youtube.publish", True)) and not dry_run
    uploader = YouTubeUploader(
        client_secrets_file=config.get("youtube.client_secrets_file", ""),
        token_file=config.get("youtube.token_file", ""),
    )
    upload_result = uploader.upload_video(
        video_path=video_path,
        title=metadata.title,
        description=metadata.description,
        tags=metadata.tags,
        visibility=config.get("youtube.visibility", "unlisted"),
        publish=publish,
    )
    thumb_result = uploader.upload_thumbnail(upload_result.video_id, thumbnail_path, publish=publish)

    manifest = {
        "date": day.isoformat(),
        "seed": seed,
        "concept": concept.to_dict(),
        "metadata": metadata.to_dict(),
        "paths": {
            "image": str(image_path),
            "thumbnail": str(thumbnail_path),
            "music": str(music_path),
            "video": str(video_path),
        },
        "upload": {"video": upload_result.raw_response, "thumbnail": thumb_result, "video_id": upload_result.video_id},
    }

    archive.write_json(run_dir / "manifest.json", manifest)
    archive.write_json(run_dir / "youtube_metadata.json", metadata.to_dict())
    write_upload_response(run_dir / "upload_response.json", manifest["upload"])
    (run_dir / "logs.txt").write_text("Pipeline completed successfully\n", encoding="utf-8")

    gallery_path = Path(config.get("archive.gallery_file", str(archive.root / "gallery.html")))
    build_gallery(archive.root, gallery_path)

    return manifest
