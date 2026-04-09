from __future__ import annotations

import os
import shutil
import stat
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_NAMES = [
    "lib.sh",
    "apply-default-keymap.sh",
    "build-firmware.sh",
    "build-host-tools.sh",
    "flash-firmware.sh",
    "send-demo-status.sh",
    "vibecraft-hook.sh",
]


def _create_sandbox(tmp_path: Path, *, include_config: bool = False) -> Path:
    sandbox = tmp_path / "repo"
    (sandbox / "scripts").mkdir(parents=True)

    for name in SCRIPT_NAMES:
        src = REPO_ROOT / "scripts" / name
        dst = sandbox / "scripts" / name
        shutil.copy2(src, dst)
        dst.chmod(dst.stat().st_mode | stat.S_IXUSR)

    if include_config:
        (sandbox / "config").mkdir(parents=True)

    return sandbox


def _write_executable(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def _run_script(
    sandbox: Path,
    script_name: str,
    *args: str,
    env: dict[str, str] | None = None,
    stdin: str | None = None,
) -> subprocess.CompletedProcess[str]:
    run_env = os.environ.copy()
    if env:
        run_env.update(env)

    return subprocess.run(
        ["bash", str(sandbox / "scripts" / script_name), *args],
        cwd=sandbox,
        text=True,
        input=stdin,
        capture_output=True,
        env=run_env,
        check=False,
    )


def test_build_firmware_missing_upstream_dir_fails(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)

    result = _run_script(sandbox, "build-firmware.sh", "keys")

    assert result.returncode == 1
    assert "Missing" in result.stdout
    assert "bootstrap-upstream.sh" in result.stdout


def test_build_firmware_dry_run_forwards_mode_argument(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)
    firmware_dir = sandbox / "upstream" / "vibekeys_firmware"
    firmware_dir.mkdir(parents=True)

    result = _run_script(
        sandbox,
        "build-firmware.sh",
        "keys_ota_bin",
        env={"DRY_RUN": "1"},
    )

    assert result.returncode == 0
    assert "+ ./build.sh keys_ota_bin" in result.stdout
    assert "Firmware build finished for mode: keys_ota_bin" in result.stdout


def test_build_firmware_generates_artifact_with_minimal_stub(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)
    firmware_dir = sandbox / "upstream" / "vibekeys_firmware"
    firmware_dir.mkdir(parents=True)

    _write_executable(
        firmware_dir / "build.sh",
        """#!/usr/bin/env bash
set -euo pipefail
mode=\"${1:-keys}\"
mkdir -p target
printf '%s' \"$mode\" > \"target/${mode}.bin\"
""",
    )

    result = _run_script(sandbox, "build-firmware.sh", "ota")

    assert result.returncode == 0
    artifact = firmware_dir / "target" / "ota.bin"
    assert artifact.exists()
    assert artifact.read_text(encoding="utf-8") == "ota"


def test_flash_firmware_invalid_target_hits_usage_branch(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)
    (sandbox / "upstream" / "vibekeys_firmware").mkdir(parents=True)

    result = _run_script(
        sandbox,
        "flash-firmware.sh",
        "invalid-target",
        env={"DRY_RUN": "1"},
    )

    assert result.returncode == 1
    assert "Usage:" in result.stdout


def test_flash_firmware_dry_run_includes_port_and_monitor_flag_for_keys(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)
    (sandbox / "upstream" / "vibekeys_firmware").mkdir(parents=True)

    result = _run_script(
        sandbox,
        "flash-firmware.sh",
        "keys",
        env={"DRY_RUN": "1", "ESP_PORT": "/dev/ttyUSB42", "MONITOR": "1"},
    )

    assert result.returncode == 0
    assert "+ cargo build --bin vibekeys --release" in result.stdout
    assert "--target-app-partition ota_1" in result.stdout
    assert "--port /dev/ttyUSB42" in result.stdout
    assert "--monitor" in result.stdout
    assert "target/xtensa-esp32s3-espidf/release/vibekeys" in result.stdout


def test_flash_firmware_dry_run_ota_without_monitor_flag(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)
    (sandbox / "upstream" / "vibekeys_firmware").mkdir(parents=True)

    result = _run_script(
        sandbox,
        "flash-firmware.sh",
        "ota",
        env={"DRY_RUN": "1", "ESP_PORT": "/dev/ttyUSB77", "MONITOR": "0"},
    )

    assert result.returncode == 0
    assert "+ cargo build --bin ota --release" in result.stdout
    assert "--target-app-partition ota_0" in result.stdout
    assert "--port /dev/ttyUSB77" in result.stdout
    assert "--monitor" not in result.stdout
    assert "target/xtensa-esp32s3-espidf/release/ota" in result.stdout


def test_build_host_tools_missing_upstream_app_fails(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)

    result = _run_script(sandbox, "build-host-tools.sh", env={"DRY_RUN": "1"})

    assert result.returncode == 1
    assert "Missing" in result.stdout
    assert "upstream/vibekeys_app" in result.stdout


def test_apply_default_keymap_reads_env_and_prints_dry_run_commands(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path, include_config=True)

    keymap_env = sandbox / "config" / "default-keymap.env"
    keymap_env.write_text(
        "\n".join(
            [
                "MIC_BINDING='\"mic-custom\"'",
                "CUSTOM_BINDING='\"ultra\"'",
                "ESC_BINDING='Ctrl+K'",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    fake_vibekeys = sandbox / "bin" / "fake-vibekeys"
    _write_executable(
        fake_vibekeys,
        """#!/usr/bin/env bash
printf 'fake vibekeys invoked: %s\\n' \"$*\"
""",
    )

    result = _run_script(
        sandbox,
        "apply-default-keymap.sh",
        env={"DRY_RUN": "1", "VIBEKEYS_BIN": str(fake_vibekeys)},
    )

    assert result.returncode == 0
    assert 'Configuring MIC -> "mic-custom"' in result.stdout
    assert 'Configuring CUSTOM -> "ultra"' in result.stdout
    assert "Configuring ESC -> Ctrl+K" in result.stdout
    assert f"+ {fake_vibekeys}" in result.stdout


def test_vibecraft_hook_formats_pre_tool_use_event_in_dry_run(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)
    fake_vibekeys = sandbox / "bin" / "vibekeys"
    _write_executable(fake_vibekeys, "#!/usr/bin/env bash\nexit 0\n")

    payload = '{"hook_event_name":"PreToolUse","tool_name":"really_long_tool_name_for_trim_check"}'
    result = _run_script(
        sandbox,
        "vibecraft-hook.sh",
        env={"DRY_RUN": "1", "VIBEKEYS_BIN": str(fake_vibekeys)},
        stdin=payload,
    )

    assert result.returncode == 0
    assert "RUNNING TOOL:" in result.stdout
    assert f"+ {fake_vibekeys}" in result.stdout


def test_vibecraft_hook_ignores_malformed_json_input(tmp_path: Path) -> None:
    sandbox = _create_sandbox(tmp_path)
    fake_vibekeys = sandbox / "bin" / "vibekeys"
    _write_executable(fake_vibekeys, "#!/usr/bin/env bash\nexit 0\n")

    result = _run_script(
        sandbox,
        "vibecraft-hook.sh",
        env={"DRY_RUN": "1", "VIBEKEYS_BIN": str(fake_vibekeys)},
        stdin="{not-json",
    )

    assert result.returncode == 0
    assert result.stdout.strip() == ""
