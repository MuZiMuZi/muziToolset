# Tools API

Tools 是 MuziTools 面向用户的独立工具层。

当前主要分类：

```text
tools/basic/
tools/blendshape/
tools/clean/
tools/controller/
tools/face/
tools/jnt/
tools/rig/
tools/skin/
```

Tool 的典型职责：

```text
UI / Selection / 用户参数
        ↓
调用 Core / System
        ↓
更新 Maya Scene
```

运行：

```bash
python scripts/generate_mkdocs_reference.py
```

后，本页会自动列出当前 `tools/**/*.py` 的真实模块，并为每个 Tool 生成：

```text
功能
使用场景
API
示例
源码位置
```

如果 Tool 暴露 `main()`，自动示例会优先生成标准窗口启动方式。
