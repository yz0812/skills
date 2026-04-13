# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 概述

Claude Code Skills 集合项目。当前采用混合形态 `ac`：`ac-plugin/` 中集中承载 8 个仅手动触发的 skill 实现，`.claude/skills/ac-*` 作为兼容入口保留 `/ac-plan`、`/ac-execute`、`/ac-debug`、`/ac-init`、`/ac-review`、`/ac-report`、`/ac-commit`、`/ac-diagram` 命令。多个 ac skill 采用“主线程 + 按需 subagents 辅助”的执行模式。

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
- `*.md` prompt 文件 — 供主线程或 subagents 复用的只读角色提示词（如 `reviewer.md`、`analyzer.md`、`architect.md`）

## 模块

| 形态 | 入口 | 触发方式 | MCP 依赖 |
|-------|------|----------|----------|
| ac plugin + wrappers | `.claude/skills/ac-*` + `ac-plugin/.claude-plugin/plugin.json` + `ac-plugin/skills/*` | `/ac-plan`、`/ac-execute`、`/ac-debug`、`/ac-init`、`/ac-review`、`/ac-report`、`/ac-commit`、`/ac-diagram` | `ac-report` 可选 `git-server`，`ac-diagram` 依赖 `mermaid-live`；其余按各自流程执行，其中多个 skill 支持主线程统筹 + 按需 subagents 辅助 |

## 打包与安装

```bash
# 加载本地 plugin 进行测试
claude --plugin-dir ./ac-plugin
```

plugin 压缩包根目录应直接包含 `.claude-plugin/` 与 `skills/`，不应额外嵌套 plugin 目录。

## MCP 服务器配置

部分 Skill 依赖 MCP 服务器，配置在 `~/.claude/mcp_servers.json`：

- **git-server**（可选）：`uvx mcp-server-git --repository <路径>`，未配置时 `/ac-report` 自动降级为 git 命令
- **mermaid-live**（推荐）：供 `/ac-diagram` 生成 Mermaid Live URL 或导出本地 `svg/png/pdf` 图文件；涉及内部结构时默认优先本地导出
