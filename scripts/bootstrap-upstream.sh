#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_DIR="${ROOT_DIR}/upstream"

mkdir -p "${UPSTREAM_DIR}"

clone_or_pull() {
  local repo_url="$1"
  local repo_dir="$2"

  if [[ -d "${repo_dir}/.git" ]]; then
    echo "Updating $(basename "${repo_dir}")"
    git -C "${repo_dir}" pull --ff-only
  else
    echo "Cloning ${repo_url}"
    git clone "${repo_url}" "${repo_dir}"
  fi
}

clone_or_pull "https://github.com/second-state/vibekeys_firmware.git" "${UPSTREAM_DIR}/vibekeys_firmware"
clone_or_pull "https://github.com/second-state/vibekeys_app.git" "${UPSTREAM_DIR}/vibekeys_app"
clone_or_pull "https://github.com/WellsWang/vckb.git" "${UPSTREAM_DIR}/vckb"
clone_or_pull "https://github.com/XiaoQiaoAI/CH582m_vibe_coding_BLE_keyboard.git" "${UPSTREAM_DIR}/CH582m_vibe_coding_BLE_keyboard"

echo "Upstream repositories are ready in ${UPSTREAM_DIR}"
