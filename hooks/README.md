# cc-read-limit-hook

A Claude Code PreToolUse hook that enforces file read limits to optimize context usage.

一个 Claude Code PreToolUse 钩子，用于限制文件读取范围以优化上下文使用。

---

## Features / 功能

- **Block large file reads** - Files >1000 lines or >50KB require `offset` + `limit` parameters
- **Limit single reads** - Max 500 lines / 20KB per read operation
- **Auto-add limit** - Automatically adds limit when only offset is specified
- **Statistics logging** - Logs read attempts for analysis

---

- **阻止大文件读取** - 超过 1000 行或 50KB 的文件必须指定 `offset` + `limit` 参数
- **限制单次读取** - 每次最多读取 500 行 / 20KB
- **自动添加 limit** - 仅指定 offset 时自动补充 limit
- **统计日志** - 记录读取操作用于分析

## Installation / 安装

1. Copy `read-guard.py` to your hooks directory:
   ```bash
   cp read-guard.py "$USERPROFILE/.claude/hooks/"
   ```

2. Add to `~/.claude/settings.json`:
   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Read",
           "hooks": [
             {
               "type": "command",
               "command": "python \"$USERPROFILE/.claude/hooks/read-guard.py\""
             }
           ]
         }
       ]
     }
   }
   ```

## Configuration / 配置

Edit the constants in `read-guard.py`:

```python
MAX_FILE_LINES = 1000        # Line threshold / 行数阈值
MAX_FILE_BYTES = 50 * 1024   # Byte threshold / 字节阈值
MAX_SINGLE_READ_LINES = 500  # Max lines per read / 单次最大行数
MAX_SINGLE_READ_BYTES = 20 * 1024  # Max bytes per read / 单次最大字节
```

---

# cc-notify-hook

A Claude Code hook that sends desktop notifications when long-running tasks complete.

一个 Claude Code 钩子，当耗时任务完成时发送桌面通知。

---

## Features / 功能

- **Duration filter** - Only notifies when task takes 2~60 minutes (skips quick tasks and stale markers)
- **Windows toast** - Native Windows 10/11 toast notification via PowerShell
- **macOS support** - Native notification via `osascript`
- **Stale marker protection** - Discards markers older than 1 hour (e.g. after crash)
- **Debug logging** - Logs all events to `notify-debug.log` for troubleshooting

---

- **耗时过滤** - 仅在任务耗时 2~60 分钟时通知（跳过短任务和过期标记）
- **Windows 通知** - 通过 PowerShell 调用原生 Windows 10/11 Toast 通知
- **macOS 支持** - 通过 `osascript` 发送原生通知
- **过期标记保护** - 丢弃超过 1 小时的标记（如崩溃后残留）
- **调试日志** - 所有事件记录到 `notify-debug.log`

## How It Works / 工作原理

```
UserPromptSubmit → python notify.py mark    # 记录起始时间戳到 .task_start
       ↓
   (Claude 执行任务...)
       ↓
Stop             → python notify.py         # 计算耗时，超过阈值则发送通知
```

## Installation / 安装

1. Copy `notify.py` to your hooks directory:
   ```bash
   cp notify.py "$USERPROFILE/.claude/hooks/"
   ```

2. Add to `~/.claude/settings.json`:
   ```json
   {
     "hooks": {
       "UserPromptSubmit": [
         {
           "matcher": "",
           "hooks": [
             {
               "type": "command",
               "command": "python \"$USERPROFILE/.claude/hooks/notify.py\" mark"
             }
           ]
         }
       ],
       "Stop": [
         {
           "matcher": "",
           "hooks": [
             {
               "type": "command",
               "command": "python \"$USERPROFILE/.claude/hooks/notify.py\""
             }
           ]
         }
       ]
     }
   }
   ```

## Configuration / 配置

Edit the constants in `notify.py`:

```python
THRESHOLD = 120   # Minimum seconds to trigger notification / 触发通知的最小秒数
MAX_AGE = 3600    # Discard markers older than this / 丢弃超过此秒数的标记
```

## Generated Files / 生成文件

| File | Description |
|------|-------------|
| `.task_start` | Temporary timestamp marker, auto-deleted after each task |
| `notify-debug.log` | Debug log for troubleshooting |

---

## License / 许可

MIT
