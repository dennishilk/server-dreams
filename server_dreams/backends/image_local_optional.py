from __future__ import annotations

from pathlib import Path

from .image_base import ImageBackend
from .image_dummy import DummyImageBackend
from server_dreams.concept_engine import Concept


class LocalOptionalImageBackend(ImageBackend):
    """Optional local backend stub.

    Intentionally lightweight; defaults to dummy rendering unless replaced.
    """

    def generate(self, concept: Concept, out_path: Path, width: int, height: int) -> Path:
        return DummyImageBackend().generate(concept, out_path, width, height)
