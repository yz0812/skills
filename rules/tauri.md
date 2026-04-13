---
paths:
  - "**/src-tauri/**/*"
  - "**/tauri.conf.json"
  - "**/Cargo.toml"
---

## Tauri 开发规则

本文件补充 Tauri 专属规则；若与项目级 `CLAUDE.md` 冲突，以项目级规则为准。

## 基本原则

1. Tauri 的核心安全边界是 **WebView 前端** 与 **Rust Core**。
2. 前端默认不可信，Rust Core 默认高权限。
3. 任何跨边界数据与命令都必须显式验证。
4. 默认最小权限、最小 capabilities、最小 commands 暴露。

## 架构规则

1. 前端只负责 UI 与受限交互。
2. 系统能力、文件能力、进程能力、敏感逻辑尽量放在 Rust Core。
3. 不要把本应在 Rust 侧约束的权限逻辑丢给前端自己“自觉遵守”。
4. command 的职责要单一，不要做万能入口。

## 安全边界规则

1. 所有 invoke 参数都要按不可信输入处理。
2. 所有来自 WebView 的数据都必须校验格式、范围和语义。
3. 不要把整个文件系统、命令执行、系统接口默认开放给前端。
4. Rust 端是最高权限区，代码必须保守。

## Permissions / Capabilities 规则

1. 使用 **permissions** 描述具体命令权限。
2. 使用 **capabilities** 把权限绑定到特定 window / webview / platform。
3. 只授予需要的 permission，禁止图省事直接全开。
4. capability 配置优先拆分成单独文件，不要把所有安全配置堆进一个大文件。
5. 若启用 remote API access，必须做明确来源白名单。

## 命令暴露规则

1. 只注册真正需要暴露给前端的 commands。
2. command 名称保持清晰，避免模糊的“万能命令”。
3. command 内部要自行做 scope / path / 参数校验。
4. 修改 command 对外能力前，先评估权限边界是否扩大。

## 前端与 WebView 规则

1. 优先本地打包前端，不依赖远程页面运行核心逻辑。
2. 保持 CSP 严格，减少远程资源依赖。
3. 若允许远程内容访问 Tauri API，必须通过 capability 明确限制 URL。
4. 不要默认相信前端框架自身就能解决安全问题。

## 平台与配置规则

1. capability 可按 `windows`、`platforms`、`remote.urls` 细化限制。
2. 桌面与移动端能力差异要显式区分，不要混配。
3. 先检查 `src-tauri/capabilities`、`permissions`、`tauri.conf.json` 的现状，再修改。
4. 安全配置变更前，先说明影响面。

## Rust 侧实现规则

1. Rust 核心代码优先显式、可审计、可推理。
2. 不为小需求堆宏、黑魔法、过度 trait 抽象。
3. 文件路径、命令参数、网络输入必须做白名单或边界校验。
4. 错误处理要有清晰语义，不要 silently ignore。

## 实现倾向

✅ 前端最小调用面 + Rust 侧收口

✅ 用 capabilities / permissions 做细粒度授权

✅ 每个窗口按需授权，而不是全局授权

✅ 对 remote API access 做白名单限制

## 严禁事项

* ❌ 默认把所有 commands 暴露给所有窗口
* ❌ 不校验 invoke 参数就直接执行高权限逻辑
* ❌ 为图方便直接给宽泛文件系统访问权限
* ❌ 把权限判断全丢给前端
* ❌ 让 `tauri.conf.json` 和 capability 配置无限膨胀而无人维护