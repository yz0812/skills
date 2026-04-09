# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 概述

Claude Code Skills 集合项目。当前采用混合形态 `ac`：`ac-plugin/` 中集中承载 6 个仅手动触发的 skill 实现，`.claude/skills/ac-*` 作为兼容入口保留 `/ac-plan`、`/ac-execute`、`/ac-debug`、`/ac-init`、`/ac-report`、`/ac-commit` 命令；其余独立 skill 如 `mindmap` 按原方式保留。

## Skill 结构约定

每个 Skill 目录的核心文件是 `SKILL.md`，必须包含 YAML frontmatter：

```yaml
---
name: skill-name
description: '触发描述，Claude Code 用此判断何时激活该 skill'
---
```

可选子目录：
- `references/` — 参考规范文档（如 `conventional-commits.md`）
- `assets/templates/` — 模板文件（如周报/月报 Markdown 模板）

## 模块

| 形态 | 入口 | 触发方式 | MCP 依赖 |
|-------|------|----------|----------|
| ac plugin + wrappers | `.claude/skills/ac-*` + `ac-plugin/.claude-plugin/plugin.json` + `ac-plugin/skills/*` | `/ac-plan`、`/ac-execute`、`/ac-debug`、`/ac-init`、`/ac-report`、`/ac-commit` | `ac-report` 可选 `git-server`；其余按各自流程执行 |
| mindmap | `mindmap/SKILL.md` | 自然语言："生成思维导图" | `mindmap-mcp-server`（必需） |

## 打包与安装

```bash
# 加载本地 plugin 进行测试
claude --plugin-dir ./ac-plugin
```

plugin 压缩包根目录应直接包含 `.claude-plugin/` 与 `skills/`，不应额外嵌套 plugin 目录。

## MCP 服务器配置

部分 Skill 依赖 MCP 服务器，配置在 `~/.claude/mcp_servers.json`：

- **mindmap**（必需）：需先 `npm install -g markmap-cli`，然后配置 `uvx mindmap-mcp-server --return-type html`
- **git-server**（可选）：`uvx mcp-server-git --repository <路径>`，未配置时 `/ac-report` 自动降级为 git 命令
