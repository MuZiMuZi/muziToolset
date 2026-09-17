# BlendShape

MuziTools 的 BlendShape 工具目前也处于**新 Core 收敛前的迁移阶段**。

当前仓库包含：

```text
tools/blendshape/add_blendshape_tool.py
tools/blendshape/invert_shape_tool.py
core/bake/blendShapeUtils.py
```

两个新 UI 都按“统一调用 `core.blendshape_utils`”的思路编写，但当前正式 `core/` 目录中还没有完成这个新模块，因此它们属于**新 UI 已成形、底层新 Core 待迁移**的状态。

<div class="grid cards" markdown>

-   :material-shape-plus:{ .lg .middle } **Target Tool**

    ---

    查看真实 Weight Index、添加 / 同名替换 Target、烘焙全部 Target Mesh。

    [:octicons-code-24: Target Tool API](../reference/tools/blendshape/add_blendshape_tool.md)

-   :material-swap-horizontal:{ .lg .middle } **Invert Shape**

    ---

    把蒙皮后姿势中的修型反算成可用于 BlendShape 的 Corrective Shape。

    [:octicons-code-24: Invert Shape API](../reference/tools/blendshape/invert_shape_tool.md)

-   :material-history:{ .lg .middle } **历史 BlendShape Helper**

    ---

    `core/bake/blendShapeUtils.py` 保留旧查询实现。

    [:octicons-code-24: Historical API](../reference/core/bake/blendShapeUtils.md)

</div>

## 推荐工作流

```text
稳定 Base Mesh
    ↓
制作 Target / Corrective
    ↓
创建或选择 BlendShape Node
    ↓
添加 / 替换 Target
    ↓
建立 Driver
    ↓
姿势验证
    ↓
必要时 Invert Shape
```

BlendShape 依赖稳定拓扑。

在制作 Corrective 前，先确认：

```text
Vertex Count
Vertex Order
Base Shape
Deformation Stack
```

## Target Tool

入口：

```python
from muziToolset.tools.blendshape import add_blendshape_tool

window = add_blendshape_tool.main()
```

当前 UI 设计包括：

```text
指定 BlendShape Node
从选择获取 BlendShape
刷新 Target 列表
显示真实 Weight Index
添加 / 同名替换 Target
复制全部 Target Mesh
```

## 为什么要使用真实 Weight Index

BlendShape 的 Target Alias 和 `weight[index]` 不是简单的“列表第几项”。

例如删除中间 Target 后可能出现：

```text
weight[0]
weight[1]
weight[4]
weight[7]
```

所以 UI 不能用：

```text
list row index == blendShape weight index
```

当前 Target Tool 的设计明确显示真实 Index，就是为了避免删除 Target 后发生索引错位。

## 添加 / 同名替换 Target

当前 UI 设计调用：

```python
blendshape_utils.add_or_replace_target(
    blendshape_node,
    target_mesh
)
```

语义是：

```text
Target Alias 不存在
    ↓
添加新 Target

Target Alias 已存在
    ↓
替换已有 Target
```

这样制作修型时可以持续更新同一个 Target，而不是每次生成新的 Weight Slot。

## 复制全部 Target Mesh

当前 UI 设计调用：

```python
blendshape_utils.duplicate_all_targets(
    blendshape_node
)
```

目标是把 BlendShape 中的 Target 烘焙成实际 Mesh，方便：

- 修改修型；
- 导出；
- 重新雕刻；
- 比较版本；
- 制作 Corrective。

## Invert Shape

入口：

```python
from muziToolset.tools.blendshape import invert_shape_tool

window = invert_shape_tool.main()
```

Invert Shape 用于这样的情况：

```text
Base Mesh
    ↓
Skin / Deformer
    ↓
角色进入目标姿势
    ↓
在变形结果上雕刻 Corrective
    ↓
反算
    ↓
得到可以放回 Base Space 的 BlendShape Target
```

这不是简单 Duplicate Mesh。

它需要补偿已有 Deformer 对空间的影响。

## Invert Shape 输入

当前 UI 要求：

```text
Base Mesh
Corrective Mesh List
```

并明确检查：

```text
基础模型与 Corrective Vertex Count 必须一致
```

不匹配的修型应该跳过或报错，而不是强行计算。

## 当前迁移状态

两个新 Tool 当前源码仍引用：

```python
from ...core import blendshape_utils
```

以及 Target Tool 中的：

```python
from ...core import scene_utils
```

这些平铺模块当前并不属于正式 `core/common/`、`core/rigging/` 结构。

因此当前状态是：

```text
新 UI / API 设计
    已存在

新 BlendShape Core
    待正式落地 / 迁移

历史 BlendShape Helper
    core/bake/blendShapeUtils.py
```

!!! warning "不要把旧 Bake 当成新 Core"
    `core/bake/blendShapeUtils.py` 目前主要提供旧版 BlendShape Node / Weight 查询；它不等于 Target Tool 所期望的新 `blendshape_utils` 完整 API。后续迁移时应该新建正式实现，再让 Tool 接入，而不是继续往 Bake 里堆新业务。

## 历史 `BlendShape` 类

旧实现：

```python
from muziToolset.core.bake import blendShapeUtils

bs = blendShapeUtils.BlendShape(
    "face_geo"
)
```

当前历史方法包括：

```text
get_blendshape_node()
get_blendshape_name()
get_blendshape_weight()
get_blendshape_weight_list()
```

这些方法会继续出现在 API Reference 中，但属于 Compatibility / Historical 区。

## Corrective 推荐思路

对于关节姿势 Corrective：

```text
Driver Rotation / Pose
    ↓
Pose Detection
    ↓
Corrective Weight
    ↓
BlendShape Target
```

对于 Face Corrective：

```text
Controller / Pose Driver
    ↓
RBF / Driven Mapping
    ↓
Corrective Weight
    ↓
BlendShape Target
```

MuziTools Eye Rig 已经预留：

```text
Pose Driver
Pose Driven
```

未来可以在这两个接口之间加入 RBF / Corrective，再驱动 BlendShape。

## Deformer 顺序

BlendShape 的实际效果还取决于 Deformer Stack。

例如：

```text
BlendShape Before Skin
```

和：

```text
BlendShape After Skin
```

在 Corrective 语义上完全不同。

所以遇到“Target 数值正确但结果不对”时，要检查：

```text
Deformer Order
Envelope
Weight
Driver
Base Mesh
Target Topology
```

## 常见问题

### Target 加进去但不动

检查：

```text
BlendShape Envelope
Target Weight
Driver Connection
Target Index
```

### Target List Index 错位

不要用 UI Row 直接代替 `weight[index]`。

### Corrective 方向错误

确认 Corrective 是在正确的 Deformed Pose 上制作，并使用正确 Invert / Compensation 流程。

### Corrective 爆点

优先检查 Base 与 Corrective：

```text
Vertex Count
Vertex Order
Topology
```

## 后续新 BlendShape Core 建议

正式新实现至少应该提供：

```text
find_blendshape
get_targets
get_target_index
add_or_replace_target
duplicate_target
duplicate_all_targets
get_mesh_shape
invert_shape
invert_shapes
```

并统一处理：

```text
真实 Weight Index
Alias
Undo
Topology Validation
Error Handling
```

完成后再把两个 Tool 的旧平铺 import 迁移过去。

## 相关 API

- [add_blendshape_tool.py](../reference/tools/blendshape/add_blendshape_tool.md)
- [invert_shape_tool.py](../reference/tools/blendshape/invert_shape_tool.md)
- [blendShapeUtils.py](../reference/core/bake/blendShapeUtils.md)
- [Eye Rig](../reference/systems/face/eye_module.md)

[返回常用工具](tools.md){ .md-button }
[打开 BlendShape Tool API](../reference/tools/blendshape/add_blendshape_tool.md){ .md-button .md-button--primary }
