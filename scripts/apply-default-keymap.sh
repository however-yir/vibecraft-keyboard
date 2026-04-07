#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib.sh
source "${SCRIPT_DIR}/lib.sh"

KEYMAP_ENV_FILE="${KEYMAP_ENV_FILE:-${ROOT_DIR}/config/default-keymap.env}"
if [[ -f "${KEYMAP_ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${KEYMAP_ENV_FILE}"
fi

MIC_BINDING="${MIC_BINDING:-'"voice"'}"
CUSTOM_BINDING="${CUSTOM_BINDING:-'"ultrathink"'}"
ESC_BINDING="${ESC_BINDING:-Ctrl+C}"
NEXT_BINDING="${NEXT_BINDING:-'"plan"'}"
BACKSPACE_BINDING="${BACKSPACE_BINDING:-Backspace}"
SWITCH_BINDING="${SWITCH_BINDING:-'"claude"'}"
ACCEPT_BINDING="${ACCEPT_BINDING:-Enter}"
ROTATE_BINDING="${ROTATE_BINDING:-Space}"

VIBEKEYS="$(resolve_vibekeys_bin)"

run_keymap() {
  local key="$1"
  local binding="$2"
  echo "Configuring ${key} -> ${binding}"
  run_cmd "${VIBEKEYS}" keymap "${key}" "${binding}"
}

echo "Applying VibeCraft default keymap profile"
run_keymap MIC "${MIC_BINDING}"
run_keymap CUSTOM "${CUSTOM_BINDING}"
run_keymap ESC "${ESC_BINDING}"
run_keymap NEXT "${NEXT_BINDING}"
run_keymap BACKSPACE "${BACKSPACE_BINDING}"
run_keymap SWITCH "${SWITCH_BINDING}"
run_keymap ACCEPT "${ACCEPT_BINDING}"
run_keymap ROTATE "${ROTATE_BINDING}"

echo "Default keymap applied."
