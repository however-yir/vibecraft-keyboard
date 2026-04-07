#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib.sh
source "${SCRIPT_DIR}/lib.sh"

require_command cargo
require_command espflash

TARGET_KIND="${1:-keys}"
MONITOR="${MONITOR:-1}"
FIRMWARE_DIR="${ROOT_DIR}/upstream/vibekeys_firmware"

if [[ ! -d "${FIRMWARE_DIR}" ]]; then
  echo "Missing ${FIRMWARE_DIR}. Run ./scripts/bootstrap-upstream.sh first."
  exit 1
fi

cd "${FIRMWARE_DIR}"

case "${TARGET_KIND}" in
  keys)
    run_cmd cargo build --bin vibekeys --release
    BIN_PATH="target/xtensa-esp32s3-espidf/release/vibekeys"
    PARTITION="ota_1"
    ;;
  ota)
    run_cmd cargo build --bin ota --release
    BIN_PATH="target/xtensa-esp32s3-espidf/release/ota"
    PARTITION="ota_0"
    ;;
  *)
    echo "Usage: $0 [keys|ota]"
    exit 1
    ;;
esac

CMD=(espflash flash --partition-table partitions.csv --target-app-partition "${PARTITION}" --flash-size 16mb)
if [[ -n "${ESP_PORT:-}" ]]; then
  CMD+=(--port "${ESP_PORT}")
fi
if [[ "${MONITOR}" == "1" ]]; then
  CMD+=(--monitor)
fi
CMD+=("${BIN_PATH}")

run_cmd "${CMD[@]}"

echo "Flash completed for target: ${TARGET_KIND}"
