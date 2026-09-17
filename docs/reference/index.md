# API Reference

API Reference 是 MuziTools 的**完整源码参考中心**，面向修改源码、编写 Builder、排查调用关系和理解 Rig System 的开发者。

这里不是一张简单的函数名列表，而是把正式 Runtime Python 文件按源码目录映射成可搜索的网站页面，并继续展开公开 Function、Class、Constructor 和 Method。

<div class="grid cards" markdown>

-   :material-application-braces-outline:{ .lg .middle } **App**

    ---

    主应用入口、工具箱和顶层窗口生命周期。

    [:octicons-arrow-right-24: 浏览 App API](app/index.md)

-   :material-cube-outline:{ .lg .middle } **Core**

    ---

    Maya 通用底层能力：命名、属性、层级、Transform、Controller、Guide、Jnt 等。

    [:octicons-arrow-right-24: 浏览 Core API](core/index.md)

-   :material-sitemap-outline:{ .lg .middle } **Systems**

    ---

    完整、可重复构建的 Rig Module / Workflow，包括 Face Rig、Rig Library 和 Body Rig。

    [:octicons-arrow-right-24: 浏览 Systems API](systems/index.md)

-   :material-tools:{ .lg .middle } **Tools**

    ---

    绑定师直接使用的操作工具、UI 和参数收集层。

    [:octicons-arrow-right-24: 浏览 Tools API](tools/index.md)

-   :material-widgets-outline:{ .lg .middle } **UI**

    ---

    公共 PySide Window、Theme、Widget 和界面基础设施。

    [:octicons-arrow-right-24: 浏览 UI API](ui/index.md)

-   :material-package-variant-closed:{ .lg .middle } **Root Package**

    ---

    `muziToolset` 根包和全局配置入口。

    [:octicons-arrow-right-24: 浏览根包 API](package-index.md)

</div>

## 自动生成范围

API Generator 会扫描正式 Runtime：

```text
__init__.py
config.py
app/**/*.py
core/**/*.py
systems/**/*.py
tools/**/*.py
ui/**/*.py
```

默认不会把下面内容作为正式 Runtime API：

```text
legacy_reference/
tests/
scripts/
__pycache__/
私有模块
```

这意味着测试、迁移脚本和文档维护脚本不会污染绑定 Runtime 的 API 索引。

## 源码和网站如何对应

每一个正式 Python 文件都会映射到一个独立页面：

```text
systems/face/eye_module.py
        ↓
docs/reference/systems/face/eye_module.md
        ↓
网站 /reference/systems/face/eye_module/
```

Package 文件会映射为：

```text
systems/face/__init__.py
        ↓
docs/reference/systems/face/package.md
```

因此你可以把网站左侧导航直接当作**可浏览的源码树**。

## 每个文件页面包含什么

标准模块页结构：

```text
概览
    ↓
常用任务
    ↓
Import
    ↓
API 一览
    ↓
公共常量
    ↓
Functions 详细 API
    ↓
Classes 详细 API
    ↓
源码位置
```

每一个公开 Function / Method 继续展开：

```text
作用
适用场景
Signature
参数表
参数类型
是否必填
默认值
返回值
异常
使用示例
Notes
```

## 文档信息从哪里来

生成优先级：

```text
源码 Docstring
    ↓
Python Annotation
    ↓
AST Signature / Default
    ↓
安全的自动占位说明
```

因此源码中的中文 Docstring 是 API 文档的第一事实来源。

公开 API 如果新增参数、修改返回值或改变异常行为，应优先更新源码 Docstring，而不是直接手改自动生成的 Markdown。

详见 [文档维护规范](../development/documentation.md)。

## 如何查一个 API

### 已知文件

直接从左侧源码树进入，例如：

```text
API 参考
└── Systems
    └── Face
        └── eye_module.py
```

### 已知类或方法名

使用网站顶部搜索，例如：

```text
EyeModule
RigModule
create_ctrl
create_joint
get_guides
connect_rig
load_outputs
library_service
```

### 只知道自己想完成什么

先进入 [用户手册](../manual/index.md)，按任务找到推荐 Tool / System，再跳回对应 API。

## 推荐阅读顺序

第一次阅读代码时，建议：

```text
总体架构
    ↓
Core API
    ↓
Systems API
    ↓
Tools API
    ↓
App / UI API
```

如果你正在做 Face Rig，则建议：

```text
Face System Architecture
    ↓
face_guide_config.py
    ↓
eye_module.py / ear_module.py / tongue_module.py
    ↓
Rig Library
    ↓
对应 Tool / UI
```

## 为什么使用 AST

Maya Runtime 文件经常包含：

```python
import maya.cmds as cmds
from PySide2 import QtWidgets
```

GitHub Actions 环境没有 Maya，因此文档生成器不能通过直接 Import Runtime 模块来收集 API。

当前流程使用静态 AST：

```text
读取源码
    ↓
ast.parse()
    ↓
提取 Module / Class / Function / Signature / Docstring
    ↓
生成 Markdown
    ↓
生成 SUMMARY.md
    ↓
MkDocs strict build
    ↓
GitHub Pages
```

整个过程不会执行 Maya Scene 操作。

## 文档覆盖保证

仓库包含专门的静态测试，用于验证：

- `app / core / systems / tools / ui` 都进入扫描范围；
- 根目录 `__init__.py` 与 `config.py` 进入扫描范围；
- 每个 Runtime Python 文件都有唯一 API 页面；
- 不同源码文件不会覆盖同一个 Markdown 页面；
- 每个公开 Function / Class / Method 都能被 Generator 收集；
- 所有生成页面都位于 `docs/reference/`。

这样新增源码文件时，如果没有进入 API Reference，文档测试会直接失败。

## 本地重新生成

```bash
python scripts/normalize_runtime_docstrings.py --check
python scripts/refine_runtime_docstring_semantics.py --check
python tests/docs_reference_generator_test.py
python tests/docs_runtime_api_coverage_test.py
python scripts/generate_mkdocs_reference.py
python scripts/refine_generated_reference.py
python scripts/extend_docs_summary.py
mkdocs build --strict
```

本地预览：

```bash
mkdocs serve
```

## API 和用户手册的边界

用户手册回答：

> 我要怎么完成这件事？

API Reference 回答：

> 这个模块、类或方法具体怎么调用？

一个复杂工作流可以拥有一篇手写 User Guide，但公开函数签名、参数和返回值只维护在源码 Docstring 与自动 API 中，避免同一份技术事实被重复维护后发生漂移。
