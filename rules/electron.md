---
paths:
  - "**/main.js"
  - "**/main.ts"
  - "**/preload.js"
  - "**/preload.ts"
  - "**/electron/**/*.js"
  - "**/electron/**/*.ts"
---

## Electron 开发规则

本文件补充 Electron 专属规则；若与项目级 `CLAUDE.md` 冲突，以项目级规则为准。

## 基本原则

1. Electron 不是普通网页环境，而是高权限桌面运行时。
2. 渲染进程里展示不可信内容时，默认按高风险处理。
3. 默认最小暴露、最小授权、最小 IPC 面。
4. 安全优先级高于开发便利。

## 版本与依赖

1. 优先使用当前稳定版 Electron，及时跟进安全更新。
2. 定期审查 npm 依赖，避免过期或高危依赖长期滞留。
3. 不要轻易引入来路不明的原生模块。

## BrowserWindow 安全基线

1. 默认保持 `contextIsolation: true`。
2. 默认保持 renderer sandbox 开启。
3. **禁止在远程内容场景开启 `nodeIntegration`**。
4. 默认使用 `preload` + `contextBridge` 暴露最小 API。
5. 保持 `webSecurity: true`。
6. 禁止为了“省事”开启 `allowRunningInsecureContent`。
7. 谨慎使用 `experimentalFeatures` 和 `enableBlinkFeatures`。

## 远程内容规则

1. 默认优先加载本地打包内容。
2. 如果必须加载远程内容，只允许可信 HTTPS 来源。
3. 远程页面绝不能直接拿到 Node.js 能力。
4. 所有导航、重定向、窗口打开动作都要显式校验目标 URL。

## IPC 与 preload 规则

1. preload 只暴露必要且收敛的 API，不透传整个 `ipcRenderer` 能力。
2. `contextBridge` 暴露的接口必须是明确、有限、语义化的。
3. `ipcMain.handle` / `ipcMain.on` 对 sender 做校验，不信任 renderer。
4. 不要把文件系统、shell、命令执行等高危能力直接裸暴露给前端。
5. IPC 参数必须做输入校验，避免任意路径、任意命令、任意 URL。

## 导航与外部打开

1. 对 `will-navigate` 做拦截和白名单校验。
2. 对 `window.open` / `setWindowOpenHandler` 做严格控制。
3. `shell.openExternal` 只能打开明确白名单 URL，不能直接吃用户输入。
4. `webview` 默认按高风险组件处理，非必要不用。

## CSP 与资源加载

1. 必须配置合理 CSP。
2. 默认仅允许 `self` 和必要白名单来源。
3. 禁止引入不必要的远程脚本。
4. 本地页面优先本地资源，不依赖 CDN 才能运行。

## 沙箱规则

1. 对大多数应用，sandbox 是默认正确选择。
2. 禁止生产环境使用 `--no-sandbox`。
3. 若确因兼容性关闭某个 renderer 的 sandbox，必须明确说明原因和风险。
4. 不可信内容永远优先放入受限上下文。

## 实现倾向

✅ 本地页面 + preload + contextBridge + 严格 IPC

✅ 默认启用 sandbox / contextIsolation

✅ 显式校验导航、sender、外链

✅ 高危能力留在 main process，并收窄调用入口

## 严禁事项

* ❌ 远程内容 + `nodeIntegration: true`
* ❌ 暴露整个 `ipcRenderer` 给前端
* ❌ 关闭 `webSecurity` 来绕问题
* ❌ 让 `shell.openExternal` 直接处理用户可控输入
* ❌ 生产环境 `--no-sandbox`