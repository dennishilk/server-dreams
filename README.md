# Server Dreams

Server Dreams is a production-minded Debian project that turns a tiny always-on server into a nightly creative machine. Every day it generates one coherent YouTube-ready package from a **single shared concept**:

- concept object
- title
- image
- retro tracker-inspired music
- rendered video
- thumbnail text/image
- YouTube description, tags, pinned comment

The goal is charm and coherence: a small retro computer that dreams at night and publishes by morning.

## Features

- Deterministic date-seeded concept generation with recurring thematic worlds.
- Semantic concept engine that keeps title/image/music/metadata aligned.
- Modular image backends (dummy, API stub, local optional stub).
- Lightweight procedural music synthesis with deterministic seed.
- FFmpeg rendering for 1080p YouTube-compatible MP4 output.
- Robust fallback behavior for image and music generation failures.
- Archive-per-day structure under `/var/lib/server-dreams/YYYY/MM/DD/`.
- YouTube upload integration with dry-run support.
- Systemd service + timer (03:30 daily) and cron-friendly script wrapper.
- HTML gallery generation from archived manifests.

## Project layout

```text
README.md
pyproject.toml
.env.example
examples/config.example.yaml
scripts/bootstrap_debian.sh
scripts/daily_run.sh
systemd/server-dreams.service
systemd/server-dreams.timer
server_dreams/
  cli.py
  config.py
  pipeline.py
  concept_engine.py
  metadata.py
  music_engine.py
  renderer.py
  youtube.py
  archive.py
  gallery.py
  logging_utils.py
  backends/
    image_base.py
    image_dummy.py
    image_api.py
    image_local_optional.py
    music_base.py
    music_tracker.py
    music_midi.py
    music_wav_fallback.py
```

## Installation

1. Install system dependencies on Debian:

```bash
bash scripts/bootstrap_debian.sh
```

2. Create and activate virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

3. Configure:

```bash
cp examples/config.example.yaml ./config.yaml
cp .env.example .env
# edit config.yaml and .env
```

## YouTube API setup (OAuth2)

1. Create a Google Cloud project and enable YouTube Data API v3.
2. Create OAuth client credentials (Desktop app or Installed app).
3. Save credentials JSON path in `config.yaml` (`youtube.client_secrets_file`).
4. Run one interactive auth flow on the server (or another machine), then store token at `youtube.token_file`.

> `server_dreams.youtube.YouTubeUploader` is structured for OAuth upload and thumbnail calls, with dry-run support. You can replace internals with your preferred Google API client implementation.

## Usage

```bash
server-dreams generate --config config.yaml
server-dreams compose-music --config config.yaml
server-dreams render --config config.yaml
server-dreams upload --config config.yaml
server-dreams run-daily --config config.yaml
server-dreams dry-run --config config.yaml
```

## Systemd

Copy unit files:

```bash
sudo cp systemd/server-dreams.service /etc/systemd/system/
sudo cp systemd/server-dreams.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now server-dreams.timer
```

Timer schedule: daily at **03:30**.

## Cron alternative

Use wrapper:

```bash
bash scripts/daily_run.sh /path/to/config.yaml
```

## Dry run example

```bash
server-dreams dry-run --config config.yaml
```

This will generate all assets and metadata, render output, archive files, and skip actual upload while writing `upload_response.json` with simulated result.

## Troubleshooting

- **ffmpeg missing**: install ffmpeg package.
- **Image backend failure**: fallback title-card image is auto-generated.
- **Music generation failure**: fallback synth generator auto-creates WAV.
- **Upload errors**: pipeline exits non-zero after archiving all assets and logs.
- **Token/auth errors**: verify OAuth credentials paths and token permissions.

## Design principle

Prefer coherence and charm over complexity.
