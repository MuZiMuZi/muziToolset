# BlendShape

用于创建和管理 BlendShape Target、Corrective 和 Invert Shape。

<div class="grid cards" markdown>

-   :material-shape-plus:{ .lg .middle } **添加 Target**

    ---

    把新模型加入 BlendShape，并管理 Target 权重。

    [:octicons-code-24: Add BlendShape API](../reference/tools/blendshape/add_blendshape_tool.md)

-   :material-shape-outline:{ .lg .middle } **Corrective**

    ---

    为关节姿势、脸部表情或变形问题制作修型。

    [:octicons-code-24: BlendShape Utils API](../reference/core/blendshape_utils.md)

-   :material-swap-horizontal:{ .lg .middle } **Invert Shape**

    ---

    根据变形结果反算 Corrective Shape。

    [:octicons-code-24: Invert Shape API](../reference/tools/blendshape/invert_shape_tool.md)

</div>

## 推荐步骤

1. 保留稳定的 Base Mesh。
2. 创建或雕刻 Target。
3. 加入 BlendShape。
4. 设置驱动关系。
5. 在最终姿势下验证 Corrective。

```text
Base Mesh
   ↓
Target Shape
   ↓
BlendShape
   ↓
Driver
   ↓
Corrective Check
```

!!! warning "拓扑一致"
    Target 和 Base Mesh 应保持兼容拓扑。Vertex 数量、顺序或 Shape 来源变化后，先确认数据关系再继续添加 Target。

## 常见问题

**Target 加进去但不动**：检查 BlendShape Weight、Target Index 和驱动连接。

**Corrective 形变方向不对**：确认是在正确的 Deformed Mesh 和姿势上进行反算。

**多个工具都在直接操作 BlendShape**：通用节点操作应优先收敛到 `core/blendshape_utils.py`。

## 相关 API

- [add_blendshape_tool.py](../reference/tools/blendshape/add_blendshape_tool.md)
- [invert_shape_tool.py](../reference/tools/blendshape/invert_shape_tool.md)
- [blendshape_utils.py](../reference/core/blendshape_utils.md)

[返回常用工具](tools.md){ .md-button }
[打开 BlendShape Utils API](../reference/core/blendshape_utils.md){ .md-button .md-button--primary }
