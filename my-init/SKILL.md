---
name: my-init
description: '初始化项目 AI 上下文：扫描项目结构并生成 CLAUDE.md 索引文档。当用户说"初始化项目"、"生成项目文档"、"创建 CLAUDE.md"、"/my-init" 时触发。采用「根级简明 + 模块级详尽」策略，自动生成 Mermaid 架构图和模块导航。'
---

# Init - 初始化项目 AI 上下文

扫描项目结构，生成分层的 `CLAUDE.md` 文档索引。

## 使用方法

```bash
/my-init [项目简述] [--modules]
```

**参数说明：**
- `项目简述`：可选，项目的简要描述
- `--modules`：可选，添加此参数时生成模块级 CLAUDE.md 文件

## 执行工作流

### 步骤 1：获取时间戳 + 扫描项目

**并行执行：**

```javascript
// 1. 获取时间戳
Bash({ command: "powershell -Command \"Get-Date -Format 'yyyy-MM-dd HH:mm'\"" })
// Unix: date "+%Y-%m-%d %H:%M"

// 2. 扫描项目结构（只读，返回结构信息）
Task({
  subagent_type: "Explore",
  prompt: `分析项目结构并返回 JSON 格式报告：
{
  "name": "项目名称（从 package.json/pyproject.toml 或目录名推断）",
  "tech": { "language": "", "framework": "", "build": "" },
  "entry": ["入口文件路径"],
  "modules": [
    { "path": "模块路径", "name": "模块名", "role": "职责", "files": ["关键文件"] }
  ],
  "commands": { "install": "", "dev": "", "test": "" }
}
跳过：node_modules、dist、build、.git、__pycache__`,
  description: "扫描项目结构"
})
```

### 步骤 2：生成根级 CLAUDE.md

**用 Write 工具**在项目根目录创建 `CLAUDE.md`：

```markdown
# {项目名称}

> 生成时间：{TIMESTAMP}

## 概述

{根据扫描结果写 1-2 句项目简述}

## 技术栈

- 语言：{language}
- 框架：{framework}
- 构建：{build}

## 项目结构

```mermaid
graph TD
    ROOT[{项目名}]
    ROOT --> M1[{模块1}]
    ROOT --> M2[{模块2}]
```

## 模块索引

| 模块 | 路径 | 职责 |
|------|------|------|
| {name} | `{path}` | {role} |

## 入口文件

- `{entry}` - {描述}

## 快速命令

```bash
{commands.install}
{commands.dev}
{commands.test}
```
```

### 步骤 3：生成模块级 CLAUDE.md（仅当指定 `--modules` 参数时）

**跳过条件**：如果用户未指定 `--modules` 参数，跳过此步骤。

**对每个模块**，用 Write 工具在其目录下创建 `CLAUDE.md`：

```markdown
# {模块名}

> [← 返回根目录](../CLAUDE.md) | 更新：{TIMESTAMP}

## 职责

{role}

## 关键文件

| 文件 | 职责 |
|------|------|
| `{file}` | {描述} |

## 依赖关系

- 依赖：{分析 import 语句}
- 被依赖：{分析其他模块的 import}
```

### 步骤 4：输出摘要

```markdown
## 初始化完成

### 生成文档
- ✅ `./CLAUDE.md`
- ✅ 模块级：{N} 个（仅当使用 `--modules` 参数时显示）

### 识别模块
1. `{path}` - {role}

### 推荐下一步
- [ ] 检查文档准确性
- [ ] 补充业务逻辑
- [ ] 如需模块级文档，使用 `/my-init --modules` 重新生成
```

## 规则

1. **Explore 只读** - 子智能体只返回分析结果，不写文件
2. **主流程写文件** - 由你（执行 skill 的 Claude）用 Write 工具生成文档
3. **只写文档** - 不修改源代码
4. **跳过生成物** - `node_modules`、`dist`、`build`、`__pycache__`、`.git`
5. **模块识别** - 含 `__init__.py`（Python）或 `index.*`（JS/TS）的目录

## Mermaid 规范

- 根级：`graph TD`（自上而下）
- 模块级：`graph LR`（左到右）
- 节点 ID 用驼峰命名
