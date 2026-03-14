#!/usr/bin/env bash
set -euo pipefail

CONFIG_PATH="${1:-${SERVER_DREAMS_CONFIG:-./config.yaml}}"

server-dreams run-daily --config "$CONFIG_PATH"
