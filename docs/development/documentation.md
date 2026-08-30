# 文档维护

MuziTools 的文档分为两类：

## 1. 手写文档

用于解释：

- 架构；
- 设计原则；
- Rig Workflow；
- Maya 节点计算原理；
- 开发规范；
- 迁移记录；
- Smoke Test 与质量门槛。

这些文件放在：

```text
docs/getting-started/
docs/architecture/
docs/development/
docs/migration/
```

手写文档负责解释“为什么”和“什么时候用”，不会被 AST Generator 覆盖。

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

正式源码使用 snake_case 文件名，因此生成页面会自动跟随：

```text
attr_utils.py
hierarchy_utils.py
joint_utils.py
name_utils.py
rename_utils.py
```

已经删除的 CamelCase Compatibility 模块不会再生成 API 页面。

## 为什么不用运行时 Import 自动文档

Maya 模块通常包含：

```python
import maya.cmds as cmds
from PySide2 import QtWidgets
```

GitHub Actions 的 Linux Runner 没有 Maya。

因此如果文档生成器直接 Import 模块，会导致在线构建失败。

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

推荐完整检查顺序：

```bash
python tests/core_import_style_test.py
python scripts/generate_mkdocs_reference.py
mkdocs build --strict
```

确认构建通过后，再启动本地预览：

```bash
mkdocs serve
```

## 为什么先运行 Core Import Style Gate

API Generator 会忠实扫描当前源码。
如果一个已经退休的旧模块被错误地重新加入仓库，单纯运行 Generator 反而可能把错误架构也生成成文档。

因此正式 CI 顺序固定为：

```text
Core Import Style Gate
        ↓
Generate API Reference
        ↓
mkdocs build --strict
        ↓
Upload Pages Artifact
        ↓
Deploy GitHub Pages
```

只有源码架构先通过 Gate，才允许继续生成和发布文档。

## 构建检查

```bash
mkdocs build --strict
```

`--strict` 会把断链、导航缺页等问题直接作为错误处理。

## 更新 Core 时

当某个 Core 模块新增公开方法时：

1. 先确认功能确实属于 Core，而不是完整 Rig System；
2. 更新模块头“当前公开方法 / 类”；
3. 给新函数补详细 Docstring；
4. 增加“步骤 1 / 步骤 2 / 为什么”的中文注释；
5. 更新对应 Smoke Test；
6. 运行 `core_import_style_test.py`；
7. 重新执行 API Reference Generator；
8. 执行 `mkdocs build --strict`；
9. 检查生成页面的签名、功能摘要和示例是否正确；
10. 需要解释设计原理时，再同步更新手写 Core Guide。

文档不是代码完成后的附加物，而是正式 API 的一部分。
