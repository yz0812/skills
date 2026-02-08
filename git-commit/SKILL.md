---
name: git-commit
description: '智能 Git 提交：分析改动自动生成 Conventional Commits 信息，支持 type/scope 推断、Breaking Change 检测、拆分建议'
---

# Git Commit - 智能提交助手

分析当前 Git 变更，自动生成符合 Conventional Commits 规范的提交信息。

## 使用方法

```bash
/git-commit [files...] [options]
```

## 选项

| 选项 | 说明 |
|------|------|
| `files...` | 指定要提交的文件（可选，默认全部） |
| `--all` | 暂存所有改动后提交 |
| `--amend` | 修补上次提交 |
| `--dry-run` | 仅预览 commit 消息，不实际提交 |
| `--no-verify` | 跳过 Git 钩子 |
| `--signoff` | 附加 Signed-off-by 签名 |
| `--emoji` | 使用 emoji 前缀 |
| `--type <type>` | 手动指定提交类型（跳过推断） |
| `--scope <scope>` | 手动指定作用域（跳过推断） |

## 示例

```bash
/git-commit                              # 提交所有暂存的变更
/git-commit src/api.py                   # 只提交指定文件
/git-commit --all                        # 暂存所有并提交
/git-commit --dry-run                    # 预览 commit 消息
/git-commit --emoji --type feat          # 带 emoji，指定类型
/git-commit --amend --signoff            # 修补上次提交并签名
```

---

## 执行工作流

### 阶段 1：仓库校验

**[模式：检查]**

1. 验证当前目录是 Git 仓库
2. 检测是否处于 rebase/merge 状态
3. 获取当前分支和 HEAD 状态

### 阶段 2：改动检测

**[模式：分析]**

```bash
git status              # 获取变更状态
git diff --cached       # 已暂存的变更
git diff                # 未暂存的变更
```

处理逻辑：
- 若指定了 `files...`，只分析指定文件
- 若暂存区为空：
  - `--all` → 执行 `git add -A`
  - 否则提示用户选择要暂存的文件

### 阶段 3：智能推断

**[模式：推断]**

#### Type 推断

根据变更内容和文件路径自动推断：

| Type | 触发条件 | 优先级 |
|------|----------|--------|
| `test` | `test_*.py`, `*_test.py`, `tests/` 目录 | 1 |
| `docs` | `.md/.rst/.txt` 文件，或仅修改注释/docstring | 2 |
| `ci` | `.github/`, `.gitlab-ci.yml`, CI 配置 | 3 |
| `build` | `pyproject.toml`, `setup.py`, `requirements.txt`, `Dockerfile` | 4 |
| `fix` | 包含 bug/fix/修复/error 关键词，异常处理修改 | 5 |
| `feat` | 新文件、新函数/类、新 API 端点 | 6 |
| `refactor` | 重命名、提取函数、结构调整但不改变行为 | 7 |
| `style` | 仅格式化、空格、分号调整 | 8 |
| `perf` | 性能优化、缓存、算法改进 | 9 |
| `chore` | 配置文件、工具脚本、无法归类的杂项 | 10 |

#### Scope 推断

根据变更文件的目录结构推断：

```
src/api/users.py      → scope: api
src/auth/login.py     → scope: auth
tests/test_api.py     → scope: api（去掉 tests 前缀）
app/routes/order.py   → scope: routes
```

规则：
- 取 `src/` 或 `app/` 下的第一级目录名
- 单文件变更可用文件名作为 scope
- 变更跨多个不相关目录时，不设置 scope

### 阶段 4：拆分建议

**[模式：建议]**

当检测到以下情况时，建议拆分提交：

- 变更涉及 3+ 个不相关模块
- 同时包含 `feat` 和 `fix` 类型的变更
- 变更行数 > 300 且逻辑不相关
- 跨多个顶级目录（源码 vs 文档 vs 测试）

建议格式：
```
⚠️ 建议拆分为多次提交：
1. feat(auth): 添加 OAuth 登录 → src/auth/oauth.py
2. fix(api): 修复用户查询 bug → src/api/users.py
3. docs: 更新 README → README.md

是否继续合并提交，还是先暂存部分文件？
```

### 阶段 5：Breaking Change 检测

**[模式：检测]**

检测以下模式时自动标记 BREAKING CHANGE：

- 删除公开函数/类/方法
- 修改函数签名（参数增删、类型变更）
- 重命名导出的符号
- 修改 API 返回值结构
- 删除配置项或环境变量

### 阶段 6：生成 Commit 消息

**[模式：生成]**

#### 格式

```
[emoji] <type>(<scope>): <subject>

[body]

[footer]
```

#### 规范

- **Subject**: ≤ 50 字符，动词开头，不加句号
- **动词**: 添加、修复、更新、重构、优化、删除、移除
- **Body**: 说明动机、实现要点、影响范围（可选）
- **Footer**: BREAKING CHANGE、关联 Issue（可选）

#### 语言判断

读取最近 20 条 commit 消息，判断项目主语言：
- 中文占比 > 50% → 生成中文消息
- 否则 → 生成英文消息

### 阶段 7：执行提交

**[模式：执行]**

```bash
# 暂存文件（如果指定）
git add <files>

# 写入消息文件
echo "<message>" > .git/COMMIT_EDITMSG

# 执行提交
git commit [-S] [--no-verify] [-s] [--amend] -F .git/COMMIT_EDITMSG
```

---

## Type 与 Emoji 映射

| Emoji | Type | 说明 |
|-------|------|------|
| ✨ | `feat` | 新增功能 |
| 🐛 | `fix` | 缺陷修复 |
| 📝 | `docs` | 文档更新 |
| 🎨 | `style` | 代码格式 |
| ♻️ | `refactor` | 代码重构 |
| ⚡️ | `perf` | 性能优化 |
| ✅ | `test` | 测试相关 |
| 🔧 | `chore` | 构建/杂项 |
| 👷 | `ci` | CI/CD 配置 |
| ⏪️ | `revert` | 回滚提交 |
| 🔨 | `build` | 构建系统 |

---

## 示例输出

### 简单功能添加

```
✨ feat(auth): 添加微信扫码登录

实现微信 OAuth2.0 授权流程，支持绑定已有账户
```

### 带 Breaking Change

```
♻️ refactor(api)!: 重构用户接口返回格式

将 user 对象从扁平结构改为嵌套结构，统一响应格式

BREAKING CHANGE: /api/users 接口返回值结构变更
- 原: { id, name, email }
- 新: { data: { id, name, email }, meta: {...} }
```

### Bug 修复

```
🐛 fix(parser): 修复空字符串解析异常

当输入为空字符串时跳过解析，返回默认值

Closes #123
```

---

## 关键规则

1. **仅操作 Git** — 不调用包管理器或运行项目代码
2. **尊重钩子** — 默认执行 pre-commit，`--no-verify` 可跳过
3. **不改源码** — 只读取 diff，写入 `.git/COMMIT_EDITMSG`
4. **原子提交** — 一次提交只做一件事，复杂变更建议拆分
5. **幂等安全** — `--dry-run` 不产生任何副作用
