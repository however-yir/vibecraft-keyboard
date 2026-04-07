#!/usr/bin/env bash
set -euo pipefail

if ! command -v vibekeys >/dev/null 2>&1; then
  echo "vibekeys command not found. Please install or build vibekeys_app first."
  exit 1
fi

vibekeys send $'PROMPTING LEVEL:\nLEVEL: CLAUDE'

echo "Demo status sent."
