# Claude Code Skills

自定义 Claude Code Skills 集合。

---

## 当前技能

| 形态 | 入口 | 说明 |
|---|---|---|
| `ac` plugin + project wrappers | `/ac-plan`、`/ac-execute`、`/ac-debug`、`/ac-init`、`/ac-review`、`/ac-report`、`/ac-commit`、`/ac-diagram` | 对外保留旧命令名，核心实现收敛到一个 plugin，全部仅手动触发；其中多个 skill 采用“主线程 + 按需 subagents 辅助”模式 |

## ac plugin 用法

```bash
/ac-plan 为登录流程补一个实施计划
/ac-execute .claude/plan/login-flow.md
/ac-debug 登录接口 500 错误
/ac-init 电商后台 --modules
/ac-review HEAD~1
/ac-report 生成最近7天周报
/ac-commit --scope auth --type fix
/ac-diagram 登录流程 --type all --format svg
```

> `/ac-review` 采用两段式流转：先生成 `.claude/review/<功能名>.md` 审查报告；确认整改范围后，再生成 `.claude/plan/review-<功能名>.md` 供 `/ac-execute` 执行。

### plugin 内资源

```text
.claude/
└── skills/
    ├── ac-plan/
    ├── ac-execute/
    ├── ac-debug/
    ├── ac-init/
    ├── ac-review/
    ├── ac-report/
    ├── ac-commit/
    └── ac-diagram/

ac-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── ac-plan/
    ├── ac-execute/
    ├── ac-debug/
    ├── ac-init/
    ├── ac-review/
    ├── ac-report/
    ├── ac-commit/
    └── ac-diagram/
```

---

## 安装

### Plugin 目录

`ac` 采用“project wrapper + Claude Code plugin”混合形态分发：`.claude/skills/ac-*` 保留旧命令名，`ac-plugin/skills/ac-*` 承载核心实现。

```text
ac-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── ac-plan/
    │   ├── SKILL.md
    │   ├── analyzer.md
    │   └── architect.md
    ├── ac-execute/
    │   └── SKILL.md
    ├── ac-debug/
    │   └── SKILL.md
    ├── ac-init/
    │   └── SKILL.md
    ├── ac-review/
    │   ├── SKILL.md
    │   └── reviewer.md
    ├── ac-report/
    │   ├── SKILL.md
    │   └── assets/
    │       └── templates/
    ├── ac-commit/
    │   ├── SKILL.md
    │   └── references/
    └── ac-diagram/
        ├── SKILL.md
        └── analyzer.md
```

### 打包

plugin 压缩包根目录应直接包含 `.claude-plugin/` 与 `skills/`，不应再额外嵌套一层目录。

### 校验与打包 skill

仓库内提供了本地脚本，兼容 Claude Code 扩展 frontmatter（如 `disable-model-invocation`、`user-invocable`、`allowed-tools`、`context` 等）。

```bash
# 校验单个 skill
python scripts/validate_skill.py skills/ac-plan
python scripts/validate_skill.py skills/ac-diagram

# 打包单个 skill 到 dist/
python scripts/package_skill.py skills/ac-plan dist
python scripts/package_skill.py skills/ac-diagram dist
```

这套脚本用于替代仅支持基础 Agent Skills 字段的旧校验逻辑。

### 本地 marketplace 安装

```bash
claude plugin marketplace add .
claude plugin install ac@skills-local --scope user
claude plugin uninstall ac@skills-local --scope user
```

> 首次安装前先执行一次 `claude plugin marketplace add .`。安装或卸载后，如需当前会话立即生效，执行 `/reload-plugins` 或重开 Claude Code。

### MCP 服务器配置

部分 skills 依赖 MCP 服务器，需在 `~/.claude/mcp_servers.json` 中配置。

#### Mermaid Diagram（可选，推荐）

`/ac-diagram` 依赖 `mermaid-live` MCP，用于将 Mermaid 源码生成可视化链接，或导出本地 `svg/png/pdf` 文件。涉及内部代码结构或业务链路时，默认优先本地导出，不默认生成外部可分享 URL。

#### Git Report（可选，推荐）

```json
{
  "git-server": {
    "command": "uvx",
    "args": [
      "mcp-server-git",
      "--repository",
      "你的仓库路径"
    ]
  }
}
```

> 未配置时 `/ac-report` 自动降级为 `git` 命令。

---

## 安装产物

根目录保留以下 plugin 安装包：

- `ac-plugin.zip`
