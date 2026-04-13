---
paths:
  - "**/manifest.json"
  - "**/background*.js"
  - "**/background*.ts"
  - "**/service-worker*.js"
  - "**/service-worker*.ts"
  - "**/content*.js"
  - "**/content*.ts"
---

## Chrome Extension / Google 浏览器扩展开发规则

本文件补充 Chrome Extension 专属规则；若与项目级 `CLAUDE.md` 冲突，以项目级规则为准。

## 基本原则

1. 默认按 **Manifest V3** 规范开发。
2. 优先最小权限、最小暴露面、最小注入范围。
3. 能用声明式能力解决，就不要用更高风险的动态能力。
4. 任何涉及远程内容、脚本注入、权限申请的改动，都必须先评估安全影响。

## 架构规则

1. 后台逻辑默认基于 **service worker** 设计。
2. service worker 可能被回收，禁止依赖全局变量持久化状态。
3. 需要持久化的数据应放入 `chrome.storage`、IndexedDB 或其他合适存储。
4. content script、service worker、extension page 的职责要分清，不要混写。

## 安全规则

1. **禁止远程托管代码**：所有 JS / CSS / Wasm 必须随扩展一起打包。
2. **禁止 `eval`、`new Function`、任意字符串执行**。
3. 注入脚本优先 `chrome.scripting.executeScript({ files })` 或 `func`，不要拼接代码字符串。
4. 所有网络通信优先 HTTPS。
5. 处理页面数据、远端返回、DOM 注入内容时，必须防 XSS。
6. `content_security_policy` 保持严格，不能为了省事放宽到危险配置。
7. `web_accessible_resources` 只开放最小必要资源和最小匹配范围。
8. 对来自页面环境的消息要做校验，不信任 `postMessage` 输入。

## Content Script 规则

1. 默认运行在 **isolated world**，不要假设可以直接访问页面 JS 上下文变量。
2. 只在必要页面注入，严格控制 `matches` / `exclude_matches` / `include_globs`。
3. 默认使用 `document_idle`，除非明确需要 `document_start` / `document_end`。
4. 能不注入全 frame，就不要 `all_frames: true`。
5. 需要访问扩展资源时，使用 `runtime.getURL()`，并同步配置 `web_accessible_resources`。
6. 页面与扩展通信时，优先消息桥接，不要直接共享危险能力。

## 权限规则

1. 权限声明最小化，优先 `activeTab`，谨慎申请广域 host permissions。
2. 新增权限前，先说明原因、影响范围、用户感知。
3. 会触发权限警告的改动，必须评估是否有更小权限替代方案。
4. 不要为了方便直接申请 `*://*/*`，除非需求本身就是全站型。

## 性能规则

1. 禁止使用 `unload` 作为关键逻辑依赖。
2. 长连接（如 WebSocket）优先放到 background/service worker 侧，而不是 content script。
3. 避免因为扩展逻辑破坏页面 back/forward cache。
4. 对注入频率、DOM 观察、消息广播要有节制，避免拖慢页面。

## 用户体验与发布

1. store listing 必须准确描述功能，不夸大、不误导。
2. 权限使用与隐私声明必须一致。
3. 如果收集用户数据，必须明确说明收集内容、用途、存储方式。
4. 上架前至少验证：不同页面、不同站点、不同系统、不同网络条件下的行为。

## 实现倾向

✅ 用本地 bundle 替代 CDN 脚本

✅ 用 `chrome.scripting` 和消息传递替代危险动态执行

✅ 用 `chrome.storage` 保存状态，而不是依赖 service worker 全局变量

✅ 精准匹配注入页面，而不是全站乱注入

## 严禁事项

* ❌ 远程下发并执行 JS 逻辑
* ❌ 放宽 CSP 以兼容危险写法
* ❌ 用字符串拼接执行脚本
* ❌ 无边界地暴露 `web_accessible_resources`
* ❌ 未评估就扩大 host permissions