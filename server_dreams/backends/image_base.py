from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from server_dreams.concept_engine import Concept


class ImageBackend(ABC):
    @abstractmethod
    def generate(self, concept: Concept, out_path: Path, width: int, height: int) -> Path:
        raise NotImplementedError
