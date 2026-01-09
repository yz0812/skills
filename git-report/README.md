# Git Report Skill

基于 Git 提交记录自动生成周报/月报。

## 安装

skill 位于 `~/.claude/skills/git-report/`，Claude Code 会自动加载。

## 使用

直接输入自然语言触发：

```bash
# 基础用法
生成本周周报
生成本月月报

# 指定月份
生成12月月报
生成2025年1月月报

# 指定用户
生成周报 @张三
生成月报 @李四

# 指定天数
生成最近10天的周报
生成最近30天的月报

# 组合使用
生成用户@张三 最近7天的周报
```

## 模板自定义

模板位于 `assets/templates/`：

```
assets/templates/
├── weekly.md    # 周报模板
└── monthly.md   # 月报模板
```

### 可用变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{DATE_RANGE}}` | 日期范围 | 2025-01-06 ~ 2025-01-10 |
| `{{USER}}` | 用户名 | 张三 |
| `{{COMMITS}}` | 提交列表 | 每行一条提交记录 |
| `{{COMMIT_COUNT}}` | 提交总数 | 15 |
| `{{REPOS}}` | 涉及仓库 | my-project |
| `{{STAT_LINES}}` | 代码统计 | +500 -200 (可选) |

### 模板示例

```markdown
# 周报 {{DATE_RANGE}}

**汇报人**: {{USER}}

## 本周工作内容

{{COMMITS}}

## 统计

- 提交次数: {{COMMIT_COUNT}}
- 涉及仓库: {{REPOS}}
```

## MCP 支持

- 优先使用 `git-server` MCP（如已安装）
- 未安装则自动降级为 `git` 命令

## 多仓库

指定多个路径时，会分别查询并合并结果：

```
生成本周周报，仓库路径：D:\project1, D:\project2
```
