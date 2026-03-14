from __future__ import annotations

from pathlib import Path

from .music_base import MusicBackend
from .music_wav_fallback import WavFallbackMusicBackend
from server_dreams.concept_engine import Concept


class TrackerMusicBackend(MusicBackend):
    """Tracker-style lightweight generator.

    Uses fallback waveform synthesis to stay tiny and Atom-friendly.
    """

    def generate(self, concept: Concept, seed: int, length_seconds: int, sample_rate: int, out_path: Path) -> Path:
        return WavFallbackMusicBackend().generate(concept, seed, length_seconds, sample_rate, out_path)
