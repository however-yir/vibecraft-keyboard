#!/usr/bin/env bash
set -euo pipefail

if ! command -v vibekeys >/dev/null 2>&1; then
  echo "vibekeys command not found. Please install or build vibekeys_app first."
  exit 1
fi

run_keymap() {
  local key="$1"
  local binding="$2"
  echo "Configuring ${key} -> ${binding}"
  vibekeys keymap "${key}" "${binding}"
}

run_keymap MIC '"voice"'
run_keymap CUSTOM '"ultrathink"'
run_keymap ESC 'Ctrl+C'
run_keymap NEXT '"plan"'
run_keymap BACKSPACE 'Backspace'
run_keymap SWITCH '"claude"'
run_keymap ACCEPT 'Enter'
run_keymap ROTATE 'Space'

echo "Default keymap applied."
