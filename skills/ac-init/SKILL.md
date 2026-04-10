---
name: ac-init
description: '扫描项目结构并生成 CLAUDE.md 上下文文档。'
disable-model-invocation: true
---

# Init - 主线程生成文档 + Subagents 扫描

扫描项目结构，必要时由 Claude 主线程统筹 subagents 并行摸排模块，最终生成分层的 `CLAUDE.md` 文档索引。

## 使用方法

```bash
/ac-init [项目简述] [--modules]
```

**参数说明：**
- `项目简述`：可选，项目的简要描述
- `--modules`：可选，添加此参数时生成模块级 `CLAUDE.md` 文件

---

## 角色分工

| 角色 | 职责 |
|------|------|
| Claude（主线程） | 获取时间戳、决定是否启用 subagents、汇总扫描结果、写入根级与模块级 `CLAUDE.md` |
| subagents | 只读扫描项目结构、模块职责、关键文件、依赖关系，不写文件 |

---

## 执行约束

**工作目录**：
- 使用当前工作目录作为项目扫描根目录
- 如果用户通过 `/add-dir` 添加了多个工作区，先用 Glob/Grep 确定目标工作区
- 如果无法确定，用 `AskUserQuestion` 询问用户选择目标工作区

**subagents 使用条件**：
- 适用：项目目录较大、模块较多、需要并行梳理结构或依赖关系
- 优先：`Explore` 用于只读扫描项目结构、入口文件、模块边界和依赖关系
- 不适用：小型项目、目录结构简单、主线程几次读取即可完成的场景

**重要**：
- 只生成或更新文档文件：根级 `CLAUDE.md` 与模块级 `CLAUDE.md`
- 不修改任何源代码、配置或依赖
- subagents 只做扫描与分析，不写文件
- 已委托给 subagents 的扫描内容，主线程不要重复执行
- 跳过生成物和缓存目录：`node_modules`、`dist`、`build`、`.git`、`__pycache__`

---

## 执行工作流

### 步骤 1：获取时间戳 + 根级扫描

`[模式：扫描]`

1. 主线程获取当前时间戳
2. 主线程先识别项目类型与最小入口信息：
   - 项目名称（从 `package.json`、`pyproject.toml` 或目录名推断）
   - 技术栈（语言、框架、构建工具）
   - 入口文件
3. 若项目结构简单：主线程直接完成扫描
4. 若项目较大或目录较多：使用 `Agent` 工具按需启动 `Explore` subagents，返回结构化扫描结果：

```json
{
  "name": "项目名称",
  "tech": { "language": "", "framework": "", "build": "" },
  "entry": ["入口文件路径"],
  "modules": [
    { "path": "模块路径", "name": "模块名", "role": "职责", "files": ["关键文件"] }
  ],
  "commands": { "install": "", "dev": "", "test": "" }
}
```

### 步骤 2：生成根级 `CLAUDE.md`

`[模式：写文档]`

由主线程用 Write 工具在项目根目录生成 `CLAUDE.md`，内容包括：

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

### 步骤 3：生成模块级 `CLAUDE.md`（仅当指定 `--modules`）

`[模式：模块分析]`

**跳过条件**：如果用户未指定 `--modules` 参数，跳过此步骤。

1. 主线程确定需要生成文档的模块列表
2. 若模块较多，使用 `Agent` 工具在同一轮并行启动多个 `Explore` subagents，按模块或模块组返回：
   - 模块职责
   - 关键文件
   - 依赖：本模块依赖谁
   - 被依赖：谁依赖本模块
3. 主线程汇总结果后，用 Write 工具在每个模块目录下创建 `CLAUDE.md`：

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

- 依赖：{分析 import / 引用关系}
- 被依赖：{分析其他模块的 import / 引用关系}
```

### 步骤 4：输出摘要

`[模式：总结]`

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
- [ ] 如需模块级文档，使用 `/ac-init --modules` 重新生成
```

---

## 规则

1. **主线程写文件** – 所有 `CLAUDE.md` 均由当前会话主线程生成
2. **subagents 只读扫描** – 仅按需启用，不默认开启，不写文件
3. **只写文档** – 不修改源代码
4. **跳过生成物** – `node_modules`、`dist`、`build`、`__pycache__`、`.git`
5. **模块识别** – 优先识别含 `__init__.py`（Python）或 `index.*`（JS/TS）的目录

## Mermaid 规范

- 根级：`graph TD`（自上而下）
- 模块级：`graph LR`（左到右）
- 节点 ID 用驼峰命名
