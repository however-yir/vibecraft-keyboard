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

如果已经装好环境，可直接进入 `upstream/vibekeys_firmware` 构建。

## 4. 编译固件

```bash
cd upstream/vibekeys_firmware
./build.sh keys
```

如果需要 OTA 相关镜像，可继续尝试：

```bash
./build.sh ota
./build.sh keys_ota_bin
```

## 5. 编译上位机

```bash
cd ../vibekeys_app
cargo build --release
```

编译完成后，主程序通常位于：

```text
upstream/vibekeys_app/target/release/vibekeys
```

## 6. 配置默认按键

回到本仓库目录执行：

```bash
chmod +x scripts/apply-default-keymap.sh
./scripts/apply-default-keymap.sh
```

## 7. 配置 Hook

参考配置模板：

```text
config/claude-settings.example.json
```

把其中的 `command` 路径按你的本机实际情况修改后，再写入 `.claude/settings.json`。

## 8. 验证显示链路

```bash
chmod +x scripts/send-demo-status.sh
./scripts/send-demo-status.sh
```

如果屏幕正确显示两行状态文字，说明 BLE 文本链路已经打通。

## 9. 建议的调试顺序

1. 先验证屏幕点亮
2. 再验证 BLE 可发现
3. 再验证文本发送
4. 再验证按键映射
5. 最后再接 Hook 和语音
