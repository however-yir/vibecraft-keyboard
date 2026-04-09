from __future__ import annotations

import os
import shutil
import stat
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _create_sandbox(tmp_path: Path) -> Path:
    sandbox = tmp_path / "repo"
    (sandbox / "scripts").mkdir(parents=True)
    shutil.copy2(REPO_ROOT / "scripts" / "lib.sh", sandbox / "scripts" / "lib.sh")
    return sandbox


def _write_exec(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def _run_bash(sandbox: Path, command: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    run_env = os.environ.copy()
    if env:
        run_env.update(env)

    return subprocess.run(
        ["bash", "-c", command],
        cwd=sandbox,
        text=True,
        capture_output=True,
        env=run_env,
        check=False,
    )


def test_resolve_vibekeys_bin_accepts_explicit_executable_path(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)
    vibekeys = sandbox / "bin" / "vibekeys-local"
    _write_exec(vibekeys, "#!/usr/bin/env bash\nexit 0\n")

    result = _run_bash(
        sandbox,
        "source scripts/lib.sh; resolve_vibekeys_bin",
        env={"VIBEKEYS_BIN": str(vibekeys)},
    )

    assert result.returncode == 0
    assert result.stdout.strip() == str(vibekeys)


def test_resolve_vibekeys_bin_fails_when_explicit_path_is_not_executable(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)
    broken = sandbox / "bin" / "not-exec"
    broken.parent.mkdir(parents=True, exist_ok=True)
    broken.write_text("plain text", encoding="utf-8")

    result = _run_bash(
        sandbox,
        "source scripts/lib.sh; resolve_vibekeys_bin",
        env={"VIBEKEYS_BIN": str(broken)},
    )

    assert result.returncode == 1
    assert "not executable" in result.stdout


def test_require_command_fails_for_missing_command(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)

    result = _run_bash(sandbox, "source scripts/lib.sh; require_command definitely_missing_cmd_xyz")

    assert result.returncode == 1
    assert "Required command not found" in result.stdout


def test_run_cmd_prints_command_in_dry_run_mode(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)

    result = _run_bash(
        sandbox,
        "source scripts/lib.sh; DRY_RUN=1; run_cmd echo hello world",
    )

    assert result.returncode == 0
    assert "+ echo hello world" in result.stdout
