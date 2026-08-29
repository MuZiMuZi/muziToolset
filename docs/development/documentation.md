# 文档维护

MuziTools 的文档分为两类：

## 1. 手写文档

用于解释：

- 架构；
- 设计原则；
- Rig Workflow；
- Maya 节点计算原理；
- 开发规范；
- 迁移记录。

这些文件放在：

```text
docs/getting-started/
docs/architecture/
docs/development/
docs/migration/
```

## 2. 自动 API Reference

由：

```text
scripts/generate_mkdocs_reference.py
```

使用 Python AST 扫描：

```text
core/
tools/
systems/
```

生成：

```text
docs/reference/core/
docs/reference/tools/
docs/reference/systems/
```

每个模块第一版页面固定包含：

```text
功能
使用场景
API
示例
源码位置
```

## 为什么不用运行时 Import 自动文档

Maya 模块通常包含：

```python
import maya.cmds as cmds
from PySide2 import QtWidgets
```

GitHub Actions 的 Linux Runner 没有 Maya。

因此如果文档生成器直接 import 模块，会导致在线构建失败。

当前方案使用 AST：

```text
读取源码
    ↓
ast.parse()
    ↓
提取 Docstring / Function / Class / Signature
    ↓
生成 Markdown
```

不会执行任何 Maya 代码。

## 本地生成

```bash
python scripts/generate_mkdocs_reference.py
```

然后：

```bash
mkdocs serve
```

## 构建检查

```bash
mkdocs build --strict
```

`--strict` 会把断链、导航缺页等问题直接作为错误处理。

## 更新 Core 时

当某个 Core 模块新增公开方法时：

1. 先更新模块头“当前公开方法”；
2. 给新函数补详细 Docstring；
3. 增加步骤中文注释；
4. 更新对应 Smoke Test；
5. 重新执行 API Reference Generator；
6. 检查生成页面是否正确。
