# Repository Scope

This repository is currently a **documentation + workflow integration** project.

## What is included

- Hardware planning and wiring documentation
- Keymap and hook integration scripts
- Build/flash wrappers that target upstream firmware projects

## What is not included (yet)

- Full, standalone firmware source tree owned by this repository
- Board-specific production firmware implementation

## How to get runnable firmware sources

Run:

```bash
./scripts/bootstrap-upstream.sh
./scripts/check_firmware_sources.sh
```

The firmware/host source trees will be materialized under `upstream/` from upstream repositories.
