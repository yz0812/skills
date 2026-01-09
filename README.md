# Claude Code Skills

这是一个 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 技能集合仓库，包含多个实用的自定义 Skill。

## 安装

将本仓库克隆到 Claude Code 的 skills 目录：

```bash
git clone https://github.com/your-username/skills.git ~/.claude/skills
```

或将单个 skill 目录复制到 `~/.claude/skills/` 下。

## 技能列表

### git-report

基于 Git 提交记录自动生成周报/月报。

**触发方式：**

```
生成本周周报
生成本月月报
生成12月月报
生成周报 @用户名
生成最近10天的周报
```

**特性：**

- 自动解析日期范围、用户名
- 智能合并相似提交，过滤噪音
- 支持自定义模板（`assets/templates/`）
- 优先使用 git-server MCP，自动降级为 git 命令
- 支持多仓库合并统计

详见 [git-report/README.md](./git-report/README.md)

## 目录结构

```
skills/
├── git-report/
│   ├── SKILL.md           # Skill 定义文件（Claude Code 读取）
│   ├── README.md          # 使用说明
│   └── assets/
│       └── templates/
│           ├── weekly.md  # 周报模板
│           └── monthly.md # 月报模板
└── README.md              # 本文件
```

## 创建新 Skill

1. 在仓库根目录创建新文件夹
2. 添加 `SKILL.md` 文件，包含 frontmatter 元数据和技能说明
3. （可选）添加 `README.md` 和资源文件

**SKILL.md 格式示例：**

```markdown
---
name: my-skill
description: 技能描述，用于触发匹配
---

# My Skill

技能的详细说明和执行流程...
```

## License

MIT
