from __future__ import annotations

import math
import random
import wave
from pathlib import Path

from .music_base import MusicBackend
from server_dreams.concept_engine import Concept


class WavFallbackMusicBackend(MusicBackend):
    def generate(self, concept: Concept, seed: int, length_seconds: int, sample_rate: int, out_path: Path) -> Path:
        rng = random.Random(seed)
        tempo = {"energetic": 168, "heroic": 150, "playful": 140, "dreamy": 110, "mysterious": 120, "melancholic": 96}.get(
            concept.mood, 128
        )
        base_freq = rng.choice([220, 247, 262, 294, 330])
        step = 60.0 / tempo / 2

        notes = [0, 3, 7, 10, 12, 10, 7, 3]
        total_samples = length_seconds * sample_rate
        data = bytearray()

        for i in range(total_samples):
            t = i / sample_rate
            idx = int(t / step) % len(notes)
            freq = base_freq * (2 ** (notes[idx] / 12))
            lead = 0.35 * math.sin(2 * math.pi * freq * t)
            arp = 0.2 * math.sin(2 * math.pi * (freq * 2) * t)
            bass = 0.25 * math.sin(2 * math.pi * (freq / 2) * t)
            pulse = 0.1 if (int(t * tempo / 60 * 4) % 4 == 0) else 0.0
            val = max(-1.0, min(1.0, lead + arp + bass + pulse))
            pcm = int(val * 32767)
            data.extend(pcm.to_bytes(2, byteorder="little", signed=True))

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(out_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(bytes(data))
        return out_path
