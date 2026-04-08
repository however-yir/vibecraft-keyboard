from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ENV_EXAMPLE = REPO_ROOT / "config" / "default-keymap.env.example"
KEYMAP_DOC = REPO_ROOT / "docs" / "keymap-hook-profile.md"
KEYMAP_SCRIPT = REPO_ROOT / "scripts" / "apply-default-keymap.sh"

ENV_TO_LOGIC_KEY = {
    "MIC_BINDING": "MIC",
    "CUSTOM_BINDING": "CUSTOM",
    "ESC_BINDING": "ESC",
    "NEXT_BINDING": "NEXT",
    "BACKSPACE_BINDING": "BACKSPACE",
    "SWITCH_BINDING": "SWITCH",
    "ACCEPT_BINDING": "ACCEPT",
    "ROTATE_BINDING": "ROTATE",
}

SCRIPT_DEFAULT_RE = re.compile(r'^(\w+)_BINDING="\$\{\1_BINDING:-(.+)\}"$')


def _normalize(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        value = value[1:-1]
    return value.strip()


def _parse_env_bindings(path: Path) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        bindings[key.strip()] = _normalize(value)
    return bindings


def _parse_doc_bindings(path: Path) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 2:
            continue
        key = cells[0].strip("`")
        value = cells[1].strip("`")
        if key in ENV_TO_LOGIC_KEY.values():
            bindings[key] = _normalize(value)
    return bindings


def _parse_script_defaults(path: Path) -> dict[str, str]:
    defaults: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        match = SCRIPT_DEFAULT_RE.match(line)
        if not match:
            continue
        env_key = f"{match.group(1)}_BINDING"
        defaults[env_key] = _normalize(match.group(2))
    return defaults


def test_env_defaults_match_keymap_docs_table() -> None:
    env_defaults = _parse_env_bindings(ENV_EXAMPLE)
    doc_defaults = _parse_doc_bindings(KEYMAP_DOC)

    for env_key, logic_key in ENV_TO_LOGIC_KEY.items():
        assert env_key in env_defaults
        assert logic_key in doc_defaults
        assert env_defaults[env_key] == doc_defaults[logic_key]


def test_env_defaults_match_apply_default_keymap_script_defaults() -> None:
    env_defaults = _parse_env_bindings(ENV_EXAMPLE)
    script_defaults = _parse_script_defaults(KEYMAP_SCRIPT)

    for env_key in ENV_TO_LOGIC_KEY:
        assert env_key in script_defaults
        assert env_defaults[env_key] == script_defaults[env_key]
