# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 概述

Claude Code Skills 集合项目。每个 Skill 是一个独立目录，包含 `SKILL.md` 定义文件，打包为 `.skill`（ZIP）后安装到 `~/.claude/skills/`。

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

| Skill | 入口 | 触发方式 | MCP 依赖 |
|-------|------|----------|----------|
| git-commit | `git-commit/SKILL.md` | `/git-commit` 斜杠命令 | 无 |
| git-report | `git-report/SKILL.md` | 自然语言："生成周报"、"生成月报" | `mcp-server-git`（可选，降级为 git 命令） |
| mindmap | `mindmap/SKILL.md` | 自然语言："生成思维导图" | `mindmap-mcp-server`（必需） |
| my-init | `my-init/SKILL.md` | `/my-init` 斜杠命令 | 无 |

## 打包与安装

```bash
# 打包单个 skill（在项目根目录执行）
cd git-commit && zip -r ../git-commit.skill . && cd ..

# 安装到 Claude Code
cp *.skill ~/.claude/skills/
```

根目录的 `.skill` 文件是各目录的 ZIP 打包产物。

## MCP 服务器配置

部分 Skill 依赖 MCP 服务器，配置在 `~/.claude/mcp_servers.json`：

- **mindmap**（必需）：需先 `npm install -g markmap-cli`，然后配置 `uvx mindmap-mcp-server --return-type html`
- **git-server**（可选）：`uvx mcp-server-git --repository <路径>`，未配置时 git-report 自动降级为 git 命令
