# Core 设计

`core/` 是 MuziTools 最底层的 Maya 功能层。

## Core 应该做什么

Core 负责可以被多个 Tool / System 复用的 Maya 通用能力，例如：

```text
Attribute
Animation
Connection
Constraint
Curve
File
Hierarchy
Joint
Matrix
Mesh
Naming
Scene
Skin
Surface
Transform
```

## Core 不应该做什么

Core 不应该：

- 创建 PySide 窗口；
- 从按钮或 Channel Box 读取 UI 状态；
- 硬编码某一个角色的 Controller 名称；
- 构建完整 Arm / Leg / Face / Ribbon Workflow；
- import `tools / systems / app / legacy_reference`。

## 当前颗粒度原则

目标不是“一个函数一个文件”，也不是重新制造 `pipelineUtils.py`。

采用：

> 一个清晰 Maya 领域，一个 utils 模块。

例如：

```text
animation_utils.py
    动画曲线、Reset、动画 JSON

scene_utils.py
    Scene、Selection、Set、Callback、Scene IO、FBX

file_utils.py
    纯 Python Path / JSON / 文件扫描

matrix_utils.py
    Matrix 与 offsetParentMatrix DG 网络

constraint_utils.py
    Maya 原生 Constraint Node
```

## 中文注释规范

关键场景操作按步骤说明：

```python
# -------------------------------------------------------------------------
# 步骤 1：整理输入节点。
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# 步骤 2：创建 Maya 节点。
# 为什么：这里需要保留 World Offset，不能直接连接 Local Matrix。
# -------------------------------------------------------------------------
```

注释重点解释：

- 为什么这样做；
- Maya 的特殊行为；
- 节点网络数据流；
- 哪一步会修改 Scene；
- 返回结果给谁使用。
