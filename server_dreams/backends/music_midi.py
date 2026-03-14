from __future__ import annotations

from pathlib import Path

from .music_base import MusicBackend
from .music_wav_fallback import WavFallbackMusicBackend
from server_dreams.concept_engine import Concept


class MidiMusicBackend(MusicBackend):
    """MIDI backend stub.

    Intended extension: write MIDI + optional FluidSynth render.
    Current implementation keeps deterministic fallback WAV generation.
    """

    def generate(self, concept: Concept, seed: int, length_seconds: int, sample_rate: int, out_path: Path) -> Path:
        return WavFallbackMusicBackend().generate(concept, seed, length_seconds, sample_rate, out_path)
