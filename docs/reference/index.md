# API 参考

MuziTools 的 API Reference 由源码自动生成。

## 生成范围

```text
core/**/*.py
tools/**/*.py
systems/**/*.py
```

默认不为 `__init__.py`、私有模块、`legacy_reference/` 和 `tests/` 单独生成 API 页面。

## 页面结构

每个正式模块第一版都会包含：

```text
功能
使用场景
API
示例
源码位置
```

## 生成命令

```bash
python scripts/generate_mkdocs_reference.py
```

生成器使用 Python AST 静态读取源码，因此不需要 Maya，也不会执行任何 Scene 操作。

## 分类

- [Core](core/index.md)：Maya 通用底层能力；
- [Tools](tools/index.md)：用户直接打开的小工具；
- [Systems](systems/index.md)：完整 Rig Builder / Workflow。

!!! note
    自动生成页适合作为 API 第一版索引。复杂的 Face、Controller、Body Rig 原理仍建议在手写架构文档中继续补充节点网络图和完整使用流程。
