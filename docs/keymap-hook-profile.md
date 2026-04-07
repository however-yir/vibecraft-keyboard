# 键位命名与 Hook 文案

## 1. 目标

这份文档用于统一三件事：

1. 图片上的按键标签如何映射到固件逻辑键位
2. 默认 keymap 如何设置
3. Hook 上屏时采用什么文案风格

## 2. 图片标签与逻辑键位映射

| 图片标签 | 项目命名 | 上游逻辑键位 | 默认动作 |
|---|---|---|---|
| 麦克风图标 | `MIC` | `MIC` | 语音入口占位或文本宏 |
| `ultrathink` | `ULTRATHINK` | `CUSTOM` | 发送 `ultrathink` |
| `ESC` | `CANCEL` | `ESC` | 中断 |
| `claude` | `MODEL` | `SWITCH` | 发送 `claude` |
| `Plan` | `PLAN` | `NEXT` | 发送 `plan` |
| `←` | `BACK` | `BACKSPACE` | 删除 / 回退 |
| `Accept` | `ACCEPT` | `ACCEPT` | 回车 / 确认 |
| 旋钮按压 | `KNOB_PRESS` | `ROTATE` | 空格 / 确认 |

这里采用了“双层命名”：

- 对外展示时，用图片更自然的命名，例如 `ULTRATHINK`、`MODEL`、`PLAN`
- 对接现成上游工具时，用 `vibekeys` 现有的逻辑键位，例如 `CUSTOM`、`SWITCH`、`NEXT`

## 3. 默认 keymap

当前仓库默认脚本采用下面这组映射：

| 逻辑键位 | 默认绑定 |
|---|---|
| `MIC` | `"voice"` |
| `CUSTOM` | `"ultrathink"` |
| `ESC` | `Ctrl+C` |
| `NEXT` | `"plan"` |
| `BACKSPACE` | `Backspace` |
| `SWITCH` | `"claude"` |
| `ACCEPT` | `Enter` |
| `ROTATE` | `Space` |

如果你要改默认值，可复制：

```text
config/default-keymap.env.example
```

再用环境变量覆盖脚本中的默认绑定。

## 4. Hook 文案风格

为贴近参考图的“状态面板”感觉，建议上屏文案尽量短、尽量像设备状态，而不是长句聊天文本。

推荐文案如下：

| Hook 事件 | 上屏文案 |
|---|---|
| `SessionStart` | `WORKFLOW READY` / `WAITING INPUT` |
| `UserPromptSubmit` | `PROMPTING:` / `<用户输入摘要>` |
| `PreToolUse` | `RUNNING TOOL:` / `<工具名>` |
| `PostToolUse` | `TOOL FINISHED:` / `<工具名>` |
| `Notification` | `NOTICE:` / `<通知摘要>` |
| `Stop` | `SESSION:` / `STOPPED` |
| `StopFailure` | `ERROR:` / `<错误摘要>` |

## 5. 当前 Hook 脚本

本仓库提供：

```text
scripts/vibecraft-hook.sh
```

它会读取 Claude Hook JSON，并把消息格式化成更适合长条屏展示的两行文本。

## 6. 使用建议

- 屏幕一屏只表达一个状态，不要堆太多字。
- 第一行优先放状态类型，例如 `PROMPTING:`、`RUNNING TOOL:`。
- 第二行优先放核心内容，例如模型名、工具名、摘要词。
- 如果你后面改成彩屏 UI，再考虑更复杂的状态页和图标。
