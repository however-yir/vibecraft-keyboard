#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib.sh
source "${SCRIPT_DIR}/lib.sh"

require_command jq

VIBEKEYS="$(resolve_vibekeys_bin)"
INPUT="$(cat)"

if [[ -z "${INPUT}" ]]; then
  exit 0
fi

trim_text() {
  local value="$1"
  value="${value//$'\n'/ }"
  value="${value//$'\r'/ }"
  printf '%s' "${value}" | cut -c1-28
}

if ! EVENT="$(printf '%s' "${INPUT}" | jq -r '.hook_event_name // empty' 2>/dev/null)"; then
  # Ignore malformed hook payloads so hook failures do not interrupt the user flow.
  exit 0
fi
if [[ -z "${EVENT}" ]]; then
  exit 0
fi

case "${EVENT}" in
  SessionStart)
    MESSAGE=$'WORKFLOW READY\nWAITING INPUT'
    ;;
  UserPromptSubmit)
    PROMPT="$(printf '%s' "${INPUT}" | jq -r '.prompt // empty')"
    MESSAGE=$(printf 'PROMPTING:\n%s' "$(trim_text "${PROMPT}")")
    ;;
  PreToolUse)
    TOOL="$(printf '%s' "${INPUT}" | jq -r '.tool_name // "tool"')"
    MESSAGE=$(printf 'RUNNING TOOL:\n%s' "$(trim_text "${TOOL}")")
    ;;
  PostToolUse)
    TOOL="$(printf '%s' "${INPUT}" | jq -r '.tool_name // "tool"')"
    MESSAGE=$(printf 'TOOL FINISHED:\n%s' "$(trim_text "${TOOL}")")
    ;;
  Notification)
    NOTICE="$(printf '%s' "${INPUT}" | jq -r '.message // empty')"
    MESSAGE=$(printf 'NOTICE:\n%s' "$(trim_text "${NOTICE}")")
    ;;
  Stop)
    MESSAGE=$'SESSION:\nSTOPPED'
    ;;
  StopFailure)
    ERROR_TEXT="$(printf '%s' "${INPUT}" | jq -r '.error // "unknown"')"
    MESSAGE=$(printf 'ERROR:\n%s' "$(trim_text "${ERROR_TEXT}")")
    ;;
  *)
    exit 0
    ;;
esac

run_cmd "${VIBEKEYS}" send "${MESSAGE}"
