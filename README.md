# Server Dreams

Server Dreams is a Debian-friendly project that turns a tiny always-on server into a deterministic nightly creative machine. Each date maps to one seed and one coherent package: concept, title, image, music, video, thumbnail, and metadata.

## Features

- Deterministic date-seeded concept generation (same date => same concept stack).
- Semantic concept engine keeps title/image/music/metadata aligned.
- Image generation flow:
  1. configured API backend (if available)
  2. deterministic local concept-art backend (default)
  3. text-only title card fallback (last resort only)
- Local concept-art backend draws lightweight retro-themed artwork using Pillow.
- Thumbnail generation reuses the generated image and overlays readable YouTube text.
- FFmpeg rendering for 1080p YouTube-compatible MP4 output.
- Lightweight deterministic procedural music synthesis.

## Output behavior (default)

By default, every run writes to exactly one directory:

- `./output/`

And replaces its previous contents. The latest run should contain:

- `manifest.json`
- `image.png`
- `thumbnail.png`
- `music.wav`
- `video.mp4`
- `youtube_metadata.json`
- `upload_response.json` (if applicable)
- `logs.txt` (if applicable)

> Dated archive folders (`/var/lib/server-dreams/YYYY/MM/DD/`) are **not** created by default. A dated mode exists only for explicit opt-in (`output.mode: dated`).

## Installation

```bash
bash scripts/bootstrap_debian.sh
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

## Configure

```bash
cp examples/config.example.yaml ./config.yaml
# edit config.yaml
```

## Usage

```bash
server-dreams run-daily --config config.yaml
server-dreams dry-run --config config.yaml
```

## Determinism notes

- The pipeline seed is derived from `YYYY-MM-DD`.
- Running the same date intentionally reproduces the same concept/title/image/music choices.
- No random variation tokens are injected beyond deterministic seeded behavior.

## Troubleshooting

- If API image generation is unavailable, local concept-art fallback is used.
- Text-only title-card images are generated only when both API and local concept-art fail.
- If music backend fails, fallback WAV synthesis is used.
- If upload is disabled or dry-run, upload responses are still written for inspection.
