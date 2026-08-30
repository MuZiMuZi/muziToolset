# API Reference

API Reference 面向修改源码、编写 Builder 和排查调用关系的开发者。

它不再只是一张“函数名列表”。现在每一个正式 Python 文件都会生成独立页面，并展开公开 Function / Class / Method。

## 生成范围

```text
__init__.py
config.py
app/**/*.py
core/**/*.py
systems/**/*.py
tools/**/*.py
ui/**/*.py
```

默认不把下面内容当作正式 Runtime API：

```text
legacy_reference/
tests/
scripts/
__pycache__/
私有模块
```

## 每个文件页面包含什么

以 `systems/face/face_guide.py` 为例，页面结构是：

```text
概览
    ↓
常用任务
    ↓
Import
    ↓
API 一览
    ↓
Functions 详细 API
    ↓
Classes 详细 API
    ↓
源码位置
```

每一个公开方法进一步展开：

```text
方法作用
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

## 参数信息从哪里来

优先级：

```text
源码 Docstring
    ↓
Python Annotation
    ↓
AST Signature / Default
    ↓
安全的自动占位说明
```

因此源码中的 Docstring 越完整，网站 API 就越完整。

推荐写法参见 [文档维护](../development/documentation.md)。

## 如何查一个 API

### 已知文件名

直接从左侧源码树进入，例如：

```text
API 参考
└── Systems
    └── Face
        └── face_guide.py
```

### 已知方法名

直接使用顶部搜索：

```text
get_lip_guides
repair_symmetry
create_controller
connect_message
```

### 只知道自己想做什么

不要从 API 开始猜。

先去 [用户手册](../manual/index.md)，按任务找到推荐模块，然后再跳进 API。

## 分类

### 根包

包含：

```text
muziToolset/__init__.py
config.py
```

### App

主程序、工具箱、顶层窗口管理。

### Core

Maya 通用底层能力，不包含完整 Rig Workflow。

### Tools

绑定师直接使用的小工具，主要负责 UI、Selection 和参数收集。

### Systems

完整、可复用的 Rig Builder / Workflow。

### UI

PySide 公共窗口、主题和 Widget。

## 为什么使用 AST

Maya 模块经常包含：

```python
import maya.cmds as cmds
from PySide2 import QtWidgets
```

GitHub Actions 没有 Maya，所以文档生成器不能直接 Import Runtime 模块。

当前流程：

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
MkDocs Build
```

整个过程不会执行 Maya Scene 操作。

## 本地重新生成

```bash
python tests/core_import_style_test.py
python tests/docs_reference_generator_test.py
python scripts/generate_mkdocs_reference.py
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

> 这个函数具体怎么调用？

一个复杂工作流可以有一篇手写 User Guide，但公开函数签名、参数和返回值只维护在源码 Docstring 与自动 API 中，避免双重维护。
