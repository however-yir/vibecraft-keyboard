#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib.sh
source "${SCRIPT_DIR}/lib.sh"

require_command cargo

APP_DIR="${ROOT_DIR}/upstream/vibekeys_app"

if [[ ! -d "${APP_DIR}" ]]; then
  echo "Missing ${APP_DIR}. Run ./scripts/bootstrap-upstream.sh first."
  exit 1
fi

cd "${APP_DIR}"
run_cmd cargo build --release

echo "Host tool build completed at ${APP_DIR}/target/release/vibekeys"
