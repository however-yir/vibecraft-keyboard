# 软件搭建说明

## 1. 总体流程

软件链路建议按以下顺序推进：

1. 拉取本仓库
2. 用脚本拉取参考上游仓库
3. 准备 `Rust + ESP` 工具链
4. 编译上位机工具
5. 编译并烧录固件
6. 配置默认按键映射
7. 配置 Claude Hook
8. 发送测试文本验证整条链路

## 2. 拉取参考上游

在仓库根目录执行：

```bash
chmod +x scripts/bootstrap-upstream.sh
./scripts/bootstrap-upstream.sh
```

脚本会把参考项目拉到 `upstream/` 目录，避免污染主仓库结构。

## 3. 准备 ESP 开发环境

建议准备以下工具：

- `rustup`
- `espup`
- `espflash`
- `ldproxy`
- `cargo`

如果已经装好环境，可直接进入编译阶段。为了减少目录切换，当前仓库已经提供了辅助脚本，不要求你手动进入上游目录执行命令。

## 4. 编译上位机

```bash
./scripts/build-host-tools.sh
```

## 5. 编译固件

```bash
./scripts/build-firmware.sh keys
```

如果需要其他构建模式，可继续尝试：

```bash
./scripts/build-firmware.sh ota
./scripts/build-firmware.sh keys_bin
./scripts/build-firmware.sh keys_ota_bin
```

## 6. 烧录固件

```bash
ESP_PORT=/dev/cu.usbmodem1101 ./scripts/flash-firmware.sh keys
```

如果只想烧录不看串口监视：

```bash
ESP_PORT=/dev/cu.usbmodem1101 MONITOR=0 ./scripts/flash-firmware.sh keys
```

## 7. 上位机产物位置

编译完成后，`vibekeys` 主程序通常位于：

```text
upstream/vibekeys_app/target/release/vibekeys
```

## 8. 配置默认按键

回到本仓库目录执行：

```bash
chmod +x scripts/apply-default-keymap.sh
./scripts/apply-default-keymap.sh
```

如果需要自定义默认绑定，可先参考：

```text
config/default-keymap.env.example
docs/keymap-hook-profile.md
```

## 9. 配置 Hook

参考配置模板：

```text
config/claude-settings.example.json
```

把其中的 `command` 路径按你的本机实际情况修改后，再写入 `.claude/settings.json`。当前模板默认使用 `scripts/vibecraft-hook.sh`，会把 Hook 事件转换成更适合长条屏显示的两行状态文案。

## 10. 验证显示链路

```bash
chmod +x scripts/send-demo-status.sh
./scripts/send-demo-status.sh
```

如果屏幕正确显示两行状态文字，说明 BLE 文本链路已经打通。

## 11. 建议的调试顺序

1. 先验证屏幕点亮
2. 再验证 BLE 可发现
3. 再验证文本发送
4. 再验证按键映射
5. 最后再接 Hook 和语音

## 12. 更详细的实操文档

如果你准备直接开始编译与烧录，建议继续阅读：

- [固件编译与烧录实操](firmware-build-and-flash.md)
- [键位命名与 Hook 文案](keymap-hook-profile.md)
- [外壳尺寸与布局草图](enclosure-layout-sketch.md)
