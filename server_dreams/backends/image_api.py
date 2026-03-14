from __future__ import annotations

from pathlib import Path

from .image_base import ImageBackend
from .image_dummy import DummyImageBackend
from server_dreams.concept_engine import Concept


class APIImageBackend(ImageBackend):
    """Placeholder for an external image API.

    In production, replace this with a provider call (OpenAI Images, SDXL API, etc.)
    using the concept object as the single source of truth.
    """

    def generate(self, concept: Concept, out_path: Path, width: int, height: int) -> Path:
        return DummyImageBackend().generate(concept, out_path, width, height)
