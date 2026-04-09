#!/usr/bin/env bash
set -euo pipefail

if command -v shellcheck >/dev/null 2>&1; then
  shellcheck -x -e SC1091 scripts/*.sh
else
  for file in scripts/*.sh; do
    bash -n "$file"
  done
fi

python3 -m pytest tests -q
