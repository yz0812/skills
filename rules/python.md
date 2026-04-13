---
paths:
  - "**/*.py"
  - "**/pyproject.toml"
  - "**/requirements*.txt"
  - "**/Pipfile"
  - "**/poetry.lock"
  - "**/pdm.lock"
  - "**/tox.ini"
---

## Python 开发规则

本文件补充 Python 专属规则；若与项目级 `CLAUDE.md` 冲突，以项目级规则为准。

## 核心原则

1. 遵循 **PEP 20（The Zen of Python）**。
2. 代码风格默认遵循 **PEP 8**。
3. 文档字符串默认遵循 **PEP 257**。
4. 优先标准库和项目现有依赖，避免无意义新增包。

## 风格规则

1. 命名清晰直白，避免缩写污染可读性。
2. 函数保持短小，单一职责。
3. 不为了“高级感”堆叠装饰器、元类、动态魔法。
4. 明确优于隐式，简单优于复杂。
5. 注释只写必要内容，不解释显而易见的代码。

## 项目与环境

1. 项目环境优先使用 `venv` 或 `virtualenv`。
2. CLI 工具型 Python 应用可优先考虑 `pipx` 安装。
3. 涉及依赖或打包时，优先检查项目是否已有 `pyproject.toml`。
4. 新项目优先现代打包方式，不再依赖过时 `setup.py` 工作流。

## 打包与构建

1. 优先使用 `pyproject.toml` 作为项目配置入口。
2. 构建分发包优先使用 `build`。
3. 上传优先使用 **Trusted Publishing** 或 `twine`。
4. 不强推单一 build backend，优先沿用项目现有方案。

## 明确禁止的旧做法

* ❌ `easy_install`
* ❌ `python setup.py install`
* ❌ `python setup.py develop`
* ❌ `python setup.py upload`
* ❌ `python setup.py sdist`
* ❌ `python setup.py bdist_wheel`
* ❌ 继续依赖 `distutils`

## 依赖与工具选择

1. 安装依赖默认使用 `pip`。
2. 需要锁定依赖时，优先看项目现有方案，如 `pip-tools`、`Pipenv`、`Poetry`。
3. 先沿用项目已有工具链，不要混入第二套生态。
4. 不要因为个人偏好强改项目的环境管理方式。

## 代码实现规则

1. 优先写可读代码，不炫技。
2. 能用标准库解决，就不要新增第三方依赖。
3. 边界输入必须校验；内部稳定流程不要过度防御式编程。
4. 对文件、网络、子进程、反序列化等风险点要保守处理。
5. 修改公共 API、序列化结构、CLI 参数时，先评估兼容性。

## 测试与质量

1. 优先遵循项目现有测试框架和组织方式，如 `pytest`、`unittest`。
2. 修 bug 时优先补复现测试。
3. 能跑最小相关测试，就不要默认全量跑。
4. 如果项目已有 lint / format / type check 工具，优先沿用。

## 实现倾向

✅ 用 `pathlib` 代替手写路径拼接

✅ 用标准库和清晰数据结构代替花哨抽象

✅ 用现代 `pyproject.toml` 流程代替过时 `setup.py` 命令

✅ 先看项目是否已经采用 `pytest` / `poetry` / `pdm` / `setuptools`

## 严禁事项

* ❌ 未确认前随意切换打包后端
* ❌ 未确认前替换项目现有依赖管理工具
* ❌ 为小需求引入重量级框架
* ❌ 写过度动态、难静态分析、难维护的 Python 代码