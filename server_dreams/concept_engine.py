from __future__ import annotations

import datetime as dt
import hashlib
import random
from dataclasses import asdict, dataclass

THEMATIC_WORLDS = [
    "linux_penguin",
    "terminal_city",
    "floppy_ocean",
    "retro_space",
    "haunted_computer_room",
    "pixel_lab",
    "synth_dungeon",
    "amiga_nightshift",
]

WORLD_SCENES = {
    "linux_penguin": [
        ("penguin", "debugging a tiny game", "CRT desk", "playful"),
        ("penguin", "compiling kernels", "moonlit server rack", "heroic"),
    ],
    "terminal_city": [
        ("hooded coder", "walking through neon terminals", "terminal city alley", "mysterious"),
        ("sysadmin", "surfing command windows", "skyline shell towers", "energetic"),
    ],
    "floppy_ocean": [
        ("robot sailor", "navigating floppy waves", "diskette sea", "dreamy"),
        ("pixel diver", "collecting old data", "underwater archive", "melancholic"),
    ],
    "retro_space": [
        ("retro astronaut", "repairing a DOS satellite", "low-orbit lab", "heroic"),
        ("space penguin", "playing synth keys", "orbital workstation", "dreamy"),
    ],
    "haunted_computer_room": [
        ("friendly ghost", "typing on a beige keyboard", "abandoned computer room", "mysterious"),
        ("night janitor bot", "watching blinking LEDs", "empty office", "melancholic"),
    ],
    "pixel_lab": [
        ("pixel scientist", "mixing neon code", "retro lab", "energetic"),
        ("hobby hacker", "testing demo effects", "basement workstation", "playful"),
    ],
    "synth_dungeon": [
        ("chip bard", "summoning arpeggios", "synth dungeon", "heroic"),
        ("terminal knight", "unlocking byte gates", "underground vault", "mysterious"),
    ],
    "amiga_nightshift": [
        ("night operator", "rendering demo parts", "amiga desk", "dreamy"),
        ("disk archivist", "indexing tracker songs", "nightshift studio", "melancholic"),
    ],
}


@dataclass
class Concept:
    world: str
    scene: str
    subject: str
    action: str
    location: str
    time_of_day: str
    mood: str
    visual_style: str
    music_style: str
    core_keywords: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def seed_from_date(date: dt.date) -> int:
    digest = hashlib.sha256(date.isoformat().encode("utf-8")).hexdigest()
    return int(digest[:12], 16)


def generate_concept(seed: int) -> Concept:
    rng = random.Random(seed)
    world = rng.choice(THEMATIC_WORLDS)
    subject, action, location, mood = rng.choice(WORLD_SCENES[world])
    time_of_day = rng.choice(["night", "late night", "midnight"])
    scene = f"{subject} {action} at {location}"
    keywords = sorted({"linux", "retro computer", "demoscene", subject, location, world.replace('_', ' ')})

    return Concept(
        world=world,
        scene=scene,
        subject=subject,
        action=action,
        location=location,
        time_of_day=time_of_day,
        mood=mood,
        visual_style="retro demoscene digital art, surreal but readable, 90s computer underground",
        music_style="amiga tracker chiptune with keygen energy",
        core_keywords=keywords,
    )
