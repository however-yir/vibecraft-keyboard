#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib.sh
source "${SCRIPT_DIR}/lib.sh"

MODE="${1:-keys}"
FIRMWARE_DIR="${ROOT_DIR}/upstream/vibekeys_firmware"

if [[ ! -d "${FIRMWARE_DIR}" ]]; then
  echo "Missing ${FIRMWARE_DIR}. Run ./scripts/bootstrap-upstream.sh first."
  exit 1
fi

cd "${FIRMWARE_DIR}"
run_cmd ./build.sh "${MODE}"

echo "Firmware build finished for mode: ${MODE}"
