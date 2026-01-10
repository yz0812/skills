# Claude Code Skills

自定义 Claude Code Skills 集合。

---

## Git Report

基于 Git 提交记录自动生成周报/月报。

### 使用

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

### MCP 支持

- 优先使用 `git-server` MCP（如已安装）
- 未安装则自动降级为 `git` 命令

### 多仓库

指定多个路径时，会分别查询并合并结果：

```
生成本周周报，仓库路径：D:\project1, D:\project2
```

---

## Check Fix

对当前修改进行全面影响分析，检查是否对其他逻辑造成破坏。

### 使用

```bash
# 标准影响分析
/check-fix

# 深度分析（追踪调用链、共享状态、事件监听等）
/check-fix --deep

# 数据结构兼容性检查
/check-fix --data

# 仅检查破坏性变更
/check-fix --breaking
```

### 检查维度

| 维度 | 检查内容 |
|------|----------|
| 直接影响 | 函数调用方、参数签名兼容性、返回值变化、异常类型 |
| 间接影响 | 数据流向、共享状态、事件触发时机、缓存策略 |
| 数据结构 | 新增/删除字段、类型变更、嵌套结构、可选字段处理 |
| 边缘情况 | 空值、边界值、异常输入、并发场景、网络异常 |

### 输出报告

包含：变更摘要、风险等级（HIGH/MEDIUM/LOW）、调用方兼容性、潜在风险点、行动清单。

---

## Mindmap

将自然语言或结构化内容转换为可视化思维导图。

### 使用

直接描述需要可视化的内容：

```bash
# 项目架构可视化
帮我生成项目架构的思维导图

# 知识体系可视化
生成 React Hooks 知识点思维导图

# 需求/会议记录可视化
把这段需求文档转成思维导图
```

### 特性

- 自动解析层级结构（标题、列表）
- 生成 HTML 文件并自动在浏览器打开
- 保存到项目根目录

---

## 安装

### Skills 目录

所有 skills 位于 `~/.claude/skills/`，Claude Code 启动时自动加载。

```
~/.claude/skills/
├── git-report/
│   └── SKILL.md
├── check-fix/
│   └── SKILL.md
└── mindmap/
    └── SKILL.md
```

### MCP 服务器配置

部分 skills 依赖 MCP 服务器，需在 `~/.claude/mcp_servers.json` 中配置：

#### Mindmap（必需）

1. 安装 markmap-cli：

```bash
npm install -g markmap-cli
```

2. 配置 MCP 服务器：

```json
{
  "mindmap": {
    "command": "uvx",
    "args": [
      "mindmap-mcp-server",
      "--return-type",
      "html"
    ]
  }
}
```

#### Git Report（可选，推荐）

配置后可获得更丰富的 git 日志信息：

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

> 未配置时自动降级为 `git` 命令。
