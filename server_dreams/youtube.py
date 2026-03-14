from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class UploadResult:
    uploaded: bool
    video_id: str
    raw_response: dict


class YouTubeUploader:
    """OAuth-ready uploader skeleton with dry-run behavior.

    Replace methods with google-api-python-client integration in production.
    """

    def __init__(self, client_secrets_file: str, token_file: str):
        self.client_secrets_file = client_secrets_file
        self.token_file = token_file

    def upload_video(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: list[str],
        visibility: str,
        publish: bool,
    ) -> UploadResult:
        if not publish:
            return UploadResult(uploaded=False, video_id="dry-run-video-id", raw_response={"status": "dry_run"})

        response = {
            "status": "uploaded_stub",
            "title": title,
            "visibility": visibility,
            "video_path": str(video_path),
            "tags": tags,
        }
        return UploadResult(uploaded=True, video_id="stub-video-id", raw_response=response)

    def upload_thumbnail(self, video_id: str, thumbnail_path: Path, publish: bool) -> dict:
        if not publish:
            return {"status": "dry_run", "video_id": video_id}
        return {"status": "thumbnail_uploaded_stub", "video_id": video_id, "thumbnail": str(thumbnail_path)}


def write_upload_response(out_path: Path, payload: dict) -> None:
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
