from __future__ import annotations

import os
from pathlib import Path

from .image_base import ImageBackend
from server_dreams.concept_engine import Concept


class APIImageBackend(ImageBackend):
    """External image API backend placeholder.

    This class intentionally raises when not configured so the pipeline can
    clearly fall back to the deterministic local concept-art backend.
    """

    def generate(self, concept: Concept, out_path: Path, width: int, height: int) -> Path:
        api_key = os.getenv("SERVER_DREAMS_IMAGE_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("SERVER_DREAMS_IMAGE_API_KEY is not configured")
        raise RuntimeError("Configured image API backend is not implemented in this build")
