#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_DIR="${ROOT_DIR}/upstream"

required=(
  "vibekeys_firmware"
  "vibekeys_app"
)

missing=0
for repo in "${required[@]}"; do
  if [[ ! -d "${UPSTREAM_DIR}/${repo}/.git" ]]; then
    echo "[missing] ${repo}"
    missing=1
  else
    echo "[ok] ${repo}"
  fi
done

if [[ "${missing}" -eq 1 ]]; then
  echo "Some upstream sources are missing. Run ./scripts/bootstrap-upstream.sh first." >&2
  exit 1
fi

echo "Firmware source prerequisites are present under upstream/."
