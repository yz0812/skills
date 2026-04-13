---
paths:
  - "**/next.config.js"
  - "**/next.config.mjs"
  - "**/next.config.ts"
  - "**/app/**/*.js"
  - "**/app/**/*.jsx"
  - "**/app/**/*.ts"
  - "**/app/**/*.tsx"
  - "**/app/**/*.mdx"
  - "**/pages/**/*.js"
  - "**/pages/**/*.jsx"
  - "**/pages/**/*.ts"
  - "**/pages/**/*.tsx"
  - "**/middleware.js"
  - "**/middleware.ts"
---

## Next.js 开发规则

本文件补充 Next.js 专属规则；若与项目级 `CLAUDE.md` 冲突，以项目级规则为准。

## 基本原则

1. 默认按 **App Router** 思维组织项目。
2. 明确区分 Server Components、Client Components、Server Actions、Route Handlers。
3. 数据获取、鉴权、授权、返回值控制必须边界清晰。
4. 优先稳定架构，不混乱叠加多种数据获取方式。

## 路由与结构规则

1. 使用文件系统路由组织 `app` 目录。
2. `page` 负责页面入口，`layout` 负责共享 UI。
3. 根布局必须清晰承载 `html` 和 `body`。
4. 动态路由、嵌套路由、布局嵌套应服从 URL 语义，不搞目录花活。
5. 对 `[param]`、`searchParams` 一律按用户输入处理。

## 组件边界规则

1. 默认优先 Server Components，只有确实需要客户端交互时才使用 Client Components。
2. Client Component props 必须最小化，禁止把整包敏感对象直接下发。
3. 不要把 server-only 代码、数据库访问、环境变量读取混进客户端边界。
4. `server-only` 模块只留在服务端使用。

## 数据获取规则

1. 一个项目尽量选定主要数据获取策略，不要混三四套。
2. 新项目优先考虑 **Data Access Layer（DAL）**。
3. DAL 负责：鉴权、授权、最小 DTO 返回、服务端边界收口。
4. 原型阶段可临时组件级获取数据，但上线代码要防止敏感数据误下发。
5. 从数据库或后端取回的数据，只返回 UI 真正需要的字段。

## 安全规则

1. 服务端拿到的数据默认不应直接透传给 Client Components。
2. 所有客户端输入都必须重新验证：formData、params、searchParams、headers、cookies。
3. Page 级鉴权不等于 Action 级鉴权，**Server Action 内必须再次鉴权和授权**。
4. Action 返回值必须最小化，禁止直接回传原始数据库记录。
5. 对资源操作必须校验所有权，防止 IDOR。
6. 对昂贵操作考虑限流。

## Server Actions 规则

1. Server Actions 视为可被直接 POST 命中的入口，不要因为“按钮只有前端有”就放松安全。
2. 每个 Action 内都要重新做认证与授权。
3. Action 尽量保持薄，核心业务放进 `server-only` 的 DAL。
4. Action 返回值只给前端必要的结果，比如 `{ success: true }`。
5. 不在 render 过程中做 mutation。

## 变更与副作用规则

1. 修改数据库、写缓存、登出、删记录等副作用只能通过 Action / 明确服务端入口执行。
2. 禁止在 Server Component / Client Component render 阶段偷偷做副作用。
3. 读取 searchParams 导致的动态渲染要有意识，不要无意扩大动态范围。

## 环境变量与机密规则

1. 机密信息只允许在服务端访问。
2. 只有明确允许暴露给前端的变量才使用 `NEXT_PUBLIC_` 前缀。
3. `process.env` 的访问尽量收口在 DAL 或服务端基础设施层。
4. 不要依赖“看起来没传到前端”这种侥幸心理。

## 实现倾向

✅ App Router + 清晰 layout/page 结构

✅ 默认 Server Components，按需 Client Components

✅ 用 DAL 收口数据访问

✅ Action 内重复鉴权、授权、参数校验

✅ 只返回最小 DTO 和最小 Action 响应

## 严禁事项

* ❌ 把数据库原始记录直接传给 Client Component
* ❌ 只做页面鉴权，不做 Action 鉴权
* ❌ 在 render 阶段做 mutation
* ❌ 把服务端机密访问逻辑带进客户端边界
* ❌ 混乱叠加多种数据访问模式导致边界失控