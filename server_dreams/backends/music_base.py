from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from server_dreams.concept_engine import Concept


class MusicBackend(ABC):
    @abstractmethod
    def generate(self, concept: Concept, seed: int, length_seconds: int, sample_rate: int, out_path: Path) -> Path:
        raise NotImplementedError
