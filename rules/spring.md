---
paths:
  - "**/*Application.java"
  - "**/*Controller.java"
  - "**/*Service.java"
  - "**/*Repository.java"
  - "**/*Config.java"
  - "**/*Configuration.java"
  - "**/application*.yml"
  - "**/application*.yaml"
  - "**/application*.properties"
---

## Spring / Spring Boot 开发规则

本文件补充 Spring 专属规则；若与项目级 `CLAUDE.md` 冲突，以项目级规则为准。

## 基本原则

1. Spring 只是工具，不是过度抽象的理由。
2. 优先遵循 Spring 官方推荐结构和默认机制，不手搓对抗框架的奇怪写法。
3. 能通过清晰的包结构、依赖注入、配置绑定解决的问题，就不要堆额外层级。
4. 对自动装配、事务、配置、扫描边界保持敬畏。

## 项目结构规则

1. 避免使用 default package。
2. 主启动类通常放在项目根包上层，便于 `@SpringBootApplication` 默认扫描子包。
3. 包结构优先围绕业务和模块组织，不围绕“Controller/Service/Util”机械堆目录。
4. 不要让 `@ComponentScan`、`@EntityScan`、`@ConfigurationPropertiesScan` 漫无边界扫全世界。

## Bean 与依赖注入规则

1. **优先构造器注入**。
2. 必须依赖用构造器表达，避免字段注入隐藏依赖关系。
3. 可选依赖才考虑 setter / 其他方式。
4. Bean 依赖关系要清晰，避免循环依赖设计。
5. 不要为了少写代码，把所有东西都做成 Spring Bean。

## 组件边界规则

1. `@Component`、`@Service`、`@Repository`、`@Controller` 只标真正需要纳入容器管理的类。
2. 普通工具类、纯函数逻辑、简单值对象不要无脑做成 Bean。
3. Service 保持业务语义，不做万能中转站。
4. Controller 负责协议边界，不承担复杂业务编排。
5. Repository / Mapper 负责持久层访问，不掺业务规则。

## 配置规则

1. 外部配置优先通过 **Externalized Configuration** 管理。
2. 复杂配置优先使用 `@ConfigurationProperties` 做类型安全绑定。
3. 避免在业务代码里到处 `@Value` 零散读取配置。
4. 配置项命名、层级、默认值要清晰，避免魔法配置。
5. 敏感配置通过环境变量或安全配置源注入，不写死在代码和仓库里。

## 自动配置与注解使用

1. 优先利用 Spring Boot 默认约定，而不是提前覆盖默认行为。
2. 新增自动配置、自定义 starter、复杂条件装配前先确认是否真的有必要。
3. 不要为了“优雅”滥用 AOP、事件、反射、动态代理。
4. 修改自动配置、条件注解、Bean 生命周期相关逻辑前，先评估影响面。

## 事务规则

1. 事务边界要清晰，只包真正需要原子性的业务步骤。
2. `@Transactional` 默认用于业务服务层，不乱贴到所有方法上。
3. Spring 默认对 **RuntimeException 和 Error 回滚**，对 checked exception 不自动回滚，必须有意识处理。
4. 不要误以为写了 `@Transactional` 就万事大吉，调用路径、代理边界、异常类型都要看清。
5. 长事务、跨远程调用事务、事务里做重 IO 操作都要谨慎。

## Web 与接口规则

1. Controller 入参必须校验，边界错误尽早失败。
2. 请求 DTO、响应 DTO、内部领域对象尽量分层，避免协议对象污染内部模型。
3. 异常返回、校验失败、权限失败等接口行为要一致。
4. 不要把内部异常栈和敏感信息直接暴露给接口调用方。

## 数据访问规则

1. 先看项目当前是 JPA、MyBatis、JdbcTemplate 还是混合方案，再决定怎么写。
2. 不随意在同一个模块里混多套持久层风格。
3. JPA 场景注意实体加载、事务边界、N+1、懒加载副作用。
4. MyBatis 场景注意 SQL 显式性、分页、索引、批量操作成本。

## 测试规则

1. 优先使用 Spring Boot Test 提供的最小测试切片，而不是默认全量起容器。
2. 纯单元逻辑优先普通单测，不必强拉 Spring 上下文。
3. 修 bug 优先补复现测试。
4. 涉及配置绑定、事务、自动配置、Bean 扫描边界时，必须做针对性验证。

## 实现倾向

✅ 主类放根包，利用默认扫描边界

✅ 构造器注入优先

✅ `@ConfigurationProperties` 优于到处 `@Value`

✅ 事务边界只覆盖真正原子业务

✅ 组件职责清晰，少做万能 Bean

## 严禁事项

* ❌ 使用 default package
* ❌ 大量字段注入掩盖依赖关系
* ❌ 到处乱贴 `@Transactional`
* ❌ 未评估就扩大扫描范围或改自动配置
* ❌ 把配置、事务、自动装配问题用“魔法注解叠叠乐”糊过去
* ❌ 擅自升级 Spring Boot / Spring Framework 版本