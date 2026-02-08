# Conventional Commits 规范

## 格式

```
<type>(<scope>): <description>

[body]

[footer]
```

## Type 详解

| Type | 说明 | SemVer | 示例 |
|------|------|--------|------|
| `feat` | 新功能 | MINOR | `feat(auth): 添加 JWT 认证` |
| `fix` | Bug 修复 | PATCH | `fix(api): 修复空指针异常` |
| `docs` | 文档更新 | - | `docs: 更新 API 文档` |
| `style` | 代码格式（不影响逻辑） | - | `style: 格式化代码` |
| `refactor` | 重构（不改变行为） | - | `refactor(utils): 提取公共方法` |
| `perf` | 性能优化 | PATCH | `perf(db): 优化查询性能` |
| `test` | 测试相关 | - | `test(auth): 添加登录测试` |
| `build` | 构建系统/依赖 | - | `build: 升级 pydantic 到 v2` |
| `ci` | CI/CD 配置 | - | `ci: 添加 GitHub Actions` |
| `chore` | 其他杂项 | - | `chore: 更新 .gitignore` |

## Scope 规范

Scope 表示影响范围，通常是模块/目录名：

```
feat(api): ...       # API 模块
fix(auth): ...       # 认证模块
refactor(models): ...# 数据模型
test(utils): ...     # 工具函数测试
build(deps): ...     # 依赖更新
```

**多 scope：** `fix(api,auth): ...`（逗号分隔，尽量避免）

## Description 规范

- 使用祈使句/动词开头
- 首字母小写（英文）或动词开头（中文）
- 不超过 50 字符
- 不加句号

**中文动词：** 添加、修复、更新、重构、优化、删除、移除、调整、实现

## Body 规范

- 空一行后开始
- 解释 what 和 why（不是 how）
- 每行不超过 72 字符

```
feat(auth): 添加 OAuth2.0 支持

实现 Google 和 GitHub 第三方登录，
用户可以选择绑定已有账户或创建新账户
```

## Footer 规范

### Breaking Change

```
feat(api)!: 重构用户接口

BREAKING CHANGE: /api/user 接口返回格式变更，
data 字段从数组改为对象
```

**两种写法：**
1. type 后加 `!`：`feat(api)!: ...`
2. footer 中声明：`BREAKING CHANGE: 描述`

### Issue 关联

```
fix(auth): 修复登录超时问题

Closes #123
Refs #456, #789
```

## 完整示例

```
feat(auth): 添加微信扫码登录

实现微信 OAuth2.0 授权流程：
- 生成带参数二维码
- 轮询扫码状态
- 获取用户信息并创建/绑定账户

BREAKING CHANGE: 移除旧版 /api/wechat/login 接口，
请迁移至 /api/auth/wechat/callback

Closes #234
```

## 自动化工具

- **commitlint** - 校验 commit 消息格式
- **standard-version** - 自动生成 CHANGELOG
- **semantic-release** - 自动发布版本
