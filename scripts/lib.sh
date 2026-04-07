#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

print_cmd() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
}

run_cmd() {
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    print_cmd "$@"
    return 0
  fi
  "$@"
}

require_command() {
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    return 0
  fi
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Required command not found: $1"
    exit 1
  fi
}

resolve_vibekeys_bin() {
  if [[ -n "${VIBEKEYS_BIN:-}" ]]; then
    if command -v "${VIBEKEYS_BIN}" >/dev/null 2>&1; then
      command -v "${VIBEKEYS_BIN}"
      return 0
    fi
    if [[ -x "${VIBEKEYS_BIN}" ]]; then
      printf '%s\n' "${VIBEKEYS_BIN}"
      return 0
    fi
    echo "Configured VIBEKEYS_BIN is not executable: ${VIBEKEYS_BIN}"
    exit 1
  fi

  if command -v vibekeys >/dev/null 2>&1; then
    command -v vibekeys
    return 0
  fi

  local local_bin="${ROOT_DIR}/upstream/vibekeys_app/target/release/vibekeys"
  if [[ -x "${local_bin}" ]]; then
    printf '%s\n' "${local_bin}"
    return 0
  fi

  echo "vibekeys executable not found. Build upstream/vibekeys_app first or set VIBEKEYS_BIN."
  exit 1
}
