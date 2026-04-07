#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib.sh
source "${SCRIPT_DIR}/lib.sh"

VIBEKEYS="$(resolve_vibekeys_bin)"
DEMO_MESSAGE="${DEMO_MESSAGE:-$'PROMPT MODE:\nCLAUDE READY'}"

run_cmd "${VIBEKEYS}" send "${DEMO_MESSAGE}"

echo "Demo status sent."
