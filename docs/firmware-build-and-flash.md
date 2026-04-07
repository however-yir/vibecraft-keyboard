# 固件编译与烧录实操

## 1. 文档目标

这份文档专门解决一件事：把 `VibeCraft 键盘` 的编译、烧录和首轮联调收紧成一条可以直接执行的命令链。默认假设你已经在本机克隆了当前仓库。

## 2. 目录约定

以下命令都以仓库根目录为起点：

```bash
cd /absolute/path/to/vibecraft-keyboard
```

参考上游会被拉到：

```text
upstream/vibekeys_firmware
upstream/vibekeys_app
upstream/vckb
upstream/CH582m_vibe_coding_BLE_keyboard
```

## 3. 一次性准备

### 3.1 拉取参考上游

```bash
./scripts/bootstrap-upstream.sh
```

### 3.2 检查工具

至少需要以下命令：

- `git`
- `cargo`
- `espflash`
- `jq`

如果 `esp` 工具链未安装完成，建议先补齐：

```bash
rustup toolchain install stable
cargo install espflash ldproxy
```

如果你已经通过 `espup` 完成过环境配置，可以直接进入下一步。

## 4. 编译上位机工具

### 4.1 直接执行脚本

```bash
./scripts/build-host-tools.sh
```

### 4.2 产物位置

编译完成后，默认可执行文件位于：

```text
upstream/vibekeys_app/target/release/vibekeys
```

## 5. 编译固件

### 5.1 编译键盘主固件

```bash
./scripts/build-firmware.sh keys
```

### 5.2 编译 OTA 固件

```bash
./scripts/build-firmware.sh ota
```

### 5.3 编译合并镜像

```bash
./scripts/build-firmware.sh keys_bin
./scripts/build-firmware.sh keys_ota_bin
```

## 6. 烧录固件

### 6.1 烧录主固件

先确认串口名，例如：

- macOS 常见为 `/dev/cu.usbmodem1101`
- Linux 常见为 `/dev/ttyACM0` 或 `/dev/ttyUSB0`

执行：

```bash
ESP_PORT=/dev/cu.usbmodem1101 ./scripts/flash-firmware.sh keys
```

### 6.2 烧录 OTA 固件

```bash
ESP_PORT=/dev/cu.usbmodem1101 ./scripts/flash-firmware.sh ota
```

### 6.3 不进入串口监视

默认脚本会带 `--monitor`。如果你只想烧录不看日志：

```bash
ESP_PORT=/dev/cu.usbmodem1101 MONITOR=0 ./scripts/flash-firmware.sh keys
```

## 7. 首轮联调顺序

建议严格按这个顺序走：

1. 执行 `./scripts/build-host-tools.sh`
2. 执行 `./scripts/build-firmware.sh keys`
3. 执行 `ESP_PORT=... ./scripts/flash-firmware.sh keys`
4. 执行 `./scripts/send-demo-status.sh`
5. 执行 `./scripts/apply-default-keymap.sh`
6. 配置 `.claude/settings.json`
7. 再接入 Hook 联动

## 8. 最短可执行链路

如果你想一次跑通关键步骤，可用下面这组命令：

```bash
cd /absolute/path/to/vibecraft-keyboard
./scripts/bootstrap-upstream.sh
./scripts/build-host-tools.sh
./scripts/build-firmware.sh keys
ESP_PORT=/dev/cu.usbmodem1101 ./scripts/flash-firmware.sh keys
VIBEKEYS_BIN="$PWD/upstream/vibekeys_app/target/release/vibekeys" ./scripts/send-demo-status.sh
VIBEKEYS_BIN="$PWD/upstream/vibekeys_app/target/release/vibekeys" ./scripts/apply-default-keymap.sh
```

## 9. 常见问题

### 9.1 `vibekeys` 命令找不到

优先使用本仓库脚本，并显式传入：

```bash
VIBEKEYS_BIN="$PWD/upstream/vibekeys_app/target/release/vibekeys" ./scripts/send-demo-status.sh
```

### 9.2 找不到固件目录

说明还没有执行：

```bash
./scripts/bootstrap-upstream.sh
```

### 9.3 串口连不上

优先排查：

- USB 数据线是否为可传输数据型号
- 设备是否真的进入下载模式
- 串口名称是否填写正确
- 是否有其他串口监视器占用了设备

### 9.4 屏幕不显示但烧录成功

优先排查：

- 屏幕排线和供电
- `MOSI / SCLK / CS / DC / RST / BL`
- 实际屏幕模组是否和当前驱动参数一致
