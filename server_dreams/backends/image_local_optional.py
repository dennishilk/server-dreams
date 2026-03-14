from __future__ import annotations

import math
import random
import subprocess
import tempfile
from pathlib import Path

from .image_base import ImageBackend
from server_dreams.concept_engine import Concept


class LocalOptionalImageBackend(ImageBackend):
    """Deterministic local concept-art backend without heavy dependencies."""

    def generate(self, concept: Concept, out_path: Path, width: int, height: int) -> Path:
        seed = f"{concept.world}|{concept.mood}|{concept.subject}|{concept.scene}|{concept.time_of_day}"
        rng = random.Random(seed)
        pixels = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]

        palettes = {
            "playful": ((12, 18, 40), (67, 120, 230), (255, 106, 182)),
            "mysterious": ((8, 10, 22), (56, 214, 221), (129, 95, 255)),
            "heroic": ((14, 16, 26), (255, 131, 76), (255, 210, 110)),
            "dreamy": ((18, 14, 40), (120, 144, 255), (255, 120, 203)),
            "melancholic": ((10, 14, 24), (90, 133, 164), (169, 193, 228)),
            "energetic": ((12, 14, 32), (0, 250, 190), (255, 108, 79)),
        }
        bg_top, bg_bottom, accent = palettes.get(concept.mood, palettes["dreamy"])

        for y in range(height):
            t = y / max(1, (height - 1))
            row = (
                int(bg_top[0] * (1 - t) + bg_bottom[0] * t),
                int(bg_top[1] * (1 - t) + bg_bottom[1] * t),
                int(bg_top[2] * (1 - t) + bg_bottom[2] * t),
            )
            pixels[y] = [row for _ in range(width)]

        horizon = int(height * 0.58)
        self._stars(pixels, rng, width, height, concept.time_of_day)

        if concept.world == "terminal_city":
            self._terminal_city(pixels, rng, width, height, horizon, accent)
        elif concept.world == "floppy_ocean":
            self._floppy_ocean(pixels, rng, width, height, horizon, accent)
        elif concept.world == "linux_penguin":
            self._linux_penguin(pixels, width, height, horizon, accent)
        elif concept.world == "haunted_computer_room":
            self._haunted_room(pixels, width, height, horizon, accent)
        elif concept.world == "amiga_nightshift":
            self._amiga_nightshift(pixels, width, height, horizon, accent)
        else:
            self._retro_geometry(pixels, rng, width, height, horizon, accent)

        self._moon(pixels, width, height, concept.world)
        self._grid_floor(pixels, width, height, horizon, accent)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(suffix=".ppm", delete=False) as tmp:
            ppm_path = Path(tmp.name)
        self._save_ppm(ppm_path, pixels, width, height)
        subprocess.run(["ffmpeg", "-y", "-i", str(ppm_path), str(out_path)], check=True, capture_output=True)
        ppm_path.unlink(missing_ok=True)
        return out_path

    def _put(self, pixels, x, y, color):
        if 0 <= y < len(pixels) and 0 <= x < len(pixels[0]):
            pixels[y][x] = color

    def _rect(self, pixels, x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(len(pixels), y1)):
            row = pixels[y]
            for x in range(max(0, x0), min(len(row), x1)):
                row[x] = color

    def _stars(self, pixels, rng, width, height, time_of_day):
        count = 130 if "night" in time_of_day else 80
        for _ in range(count):
            x = rng.randrange(width)
            y = rng.randrange(int(height * 0.5))
            bright = 180 + rng.randrange(70)
            self._put(pixels, x, y, (bright, bright, min(255, bright + 20)))

    def _moon(self, pixels, width, height, world):
        cx = int(width * (0.72 if world == "floppy_ocean" else 0.82))
        cy = int(height * 0.2)
        r = int(min(width, height) * 0.08)
        for y in range(cy - r, cy + r):
            for x in range(cx - r, cx + r):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self._put(pixels, x, y, (226, 232, 255))
        for y in range(cy - r, cy + r):
            for x in range(cx - r // 2, cx + r + 24):
                if (x - (cx + r // 3)) ** 2 + (y - cy) ** 2 <= r * r:
                    if 0 <= y < height and 0 <= x < width:
                        pixels[y][x] = tuple(max(0, c - 32) for c in pixels[y][x])

    def _grid_floor(self, pixels, width, height, horizon, accent):
        for y in range(horizon, height):
            if (y - horizon) % 16 == 0:
                for x in range(width):
                    self._put(pixels, x, y, tuple(min(255, c // 2 + 40) for c in accent))
        center = width // 2
        for gx in range(-14, 15):
            x1 = int(width * (gx / 16 + 0.5))
            for t in range(height - horizon):
                y = horizon + t
                x = int(center + (x1 - center) * (t / max(1, height - horizon)))
                self._put(pixels, x, y, (60, 100, 160))

    def _terminal_city(self, pixels, rng, width, height, horizon, accent):
        for _ in range(22):
            bw = rng.randint(45, 120)
            bh = rng.randint(110, 330)
            x = rng.randint(0, max(1, width - bw - 1))
            y = horizon - bh
            self._rect(pixels, x, y, x + bw, horizon, (14, 18, 30))
            for wy in range(y + 8, horizon - 8, 14):
                for wx in range(x + 8, x + bw - 8, 12):
                    if rng.random() > 0.35:
                        self._rect(pixels, wx, wy, wx + 5, wy + 7, accent)

    def _floppy_ocean(self, pixels, rng, width, height, horizon, accent):
        for y in range(horizon, height):
            wave = int(10 * math.sin((y - horizon) / 7))
            c = (12, 55 + (height - y) // 5, 95 + (height - y) // 4)
            for x in range(width):
                self._put(pixels, x, y, c)
                if (x + wave) % 36 == 0:
                    self._put(pixels, x, y, accent)
        fx, fy = int(width * 0.68), horizon - 70
        self._rect(pixels, fx - 70, fy - 45, fx + 70, fy + 45, (200, 205, 238))
        self._rect(pixels, fx - 48, fy - 28, fx + 48, fy + 28, (55, 75, 122))

    def _linux_penguin(self, pixels, width, height, horizon, accent):
        desk = int(height * 0.72)
        self._rect(pixels, 0, desk, width, height, (24, 20, 30))
        mx, my = int(width * 0.64), int(height * 0.54)
        self._rect(pixels, mx - 180, my - 95, mx + 180, my + 95, (18, 28, 36))
        self._rect(pixels, mx - 160, my - 75, mx + 160, my + 75, (32, 186, 128))
        px, py = int(width * 0.34), int(height * 0.62)
        for y in range(py - 110, py + 110):
            for x in range(px - 80, px + 80):
                if ((x - px) / 78) ** 2 + ((y - py) / 108) ** 2 <= 1:
                    self._put(pixels, x, y, (14, 14, 20))
        for y in range(py - 74, py + 98):
            for x in range(px - 48, px + 48):
                if ((x - px) / 46) ** 2 + ((y - py) / 86) ** 2 <= 1:
                    self._put(pixels, x, y, (235, 235, 235))
        self._rect(pixels, px + 2, py - 8, px + 26, py + 8, (255, 174, 65))

    def _haunted_room(self, pixels, width, height, horizon, accent):
        self._rect(pixels, 0, horizon - 120, width, height, (14, 14, 20))
        for i in range(5):
            x = int(width * (0.1 + i * 0.18))
            self._rect(pixels, x, horizon - 115, x + 95, horizon + 40, (24, 28, 38))
            self._rect(pixels, x + 10, horizon - 95, x + 85, horizon - 30, (76, 210, 185))
        gx, gy = int(width * 0.8), int(height * 0.58)
        for y in range(gy - 80, gy + 70):
            for x in range(gx - 55, gx + 55):
                if ((x - gx) / 55) ** 2 + ((y - gy) / 78) ** 2 <= 1:
                    self._put(pixels, x, y, (155, 178, 208))

    def _amiga_nightshift(self, pixels, width, height, horizon, accent):
        floor = int(height * 0.72)
        self._rect(pixels, 0, floor, width, height, (30, 18, 42))
        self._rect(pixels, 120, horizon - 40, width - 120, floor, (36, 22, 52))
        cx, cy = width // 2, int(height * 0.56)
        self._rect(pixels, cx - 190, cy - 100, cx + 190, cy + 100, (22, 26, 38))
        for i in range(20):
            y = cy - 80 + i * 8
            c = (120 + i * 4, 90 + i * 2, 210 + i * 2)
            self._rect(pixels, cx - 165, y, cx + 165, y + 2, c)

    def _retro_geometry(self, pixels, rng, width, height, horizon, accent):
        for _ in range(48):
            x = rng.randint(0, width - 30)
            y = rng.randint(int(height * 0.2), height - 30)
            s = rng.randint(18, 90)
            self._rect(pixels, x, y, min(width, x + s), min(height, y + 2), accent)
            self._rect(pixels, x, y, min(width, x + 2), min(height, y + s), accent)

    def _save_ppm(self, path: Path, pixels, width: int, height: int):
        with path.open("wb") as fh:
            fh.write(f"P6\n{width} {height}\n255\n".encode("ascii"))
            for row in pixels:
                for r, g, b in row:
                    fh.write(bytes((r, g, b)))
