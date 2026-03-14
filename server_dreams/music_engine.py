from __future__ import annotations

from pathlib import Path

from .backends.music_midi import MidiMusicBackend
from .backends.music_tracker import TrackerMusicBackend
from .backends.music_wav_fallback import WavFallbackMusicBackend
from .concept_engine import Concept


def get_music_backend(name: str):
    if name == "midi":
        return MidiMusicBackend()
    if name == "fallback":
        return WavFallbackMusicBackend()
    return TrackerMusicBackend()


def compose_music(
    concept: Concept,
    seed: int,
    backend_name: str,
    length_seconds: int,
    sample_rate: int,
    out_path: Path,
) -> Path:
    backend = get_music_backend(backend_name)
    return backend.generate(concept, seed, length_seconds, sample_rate, out_path)
