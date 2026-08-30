# Controller

用于创建和维护标准绑定控制器。

<div class="grid cards" markdown>

-   :material-vector-circle:{ .lg .middle } **创建标准 Controller**

    ---

    生成标准层级、Shape、颜色和 Output。

    [:octicons-code-24: Builder API](../reference/systems/controller/builder.md)

-   :material-axis-arrow:{ .lg .middle } **创建 FK Controller**

    ---

    根据 Joint Chain 快速生成 FK 控制器。

    [:octicons-code-24: FK Tool API](../reference/tools/controller/create_fk_ctrl_tool.md)

-   :material-shape-outline:{ .lg .middle } **修改 Shape**

    ---

    调整 Shape、大小、旋转和颜色。

    [:octicons-code-24: Shape Tool API](../reference/tools/controller/control_shape_tool.md)

-   :material-source-branch:{ .lg .middle } **Space Blend**

    ---

    World / Root / Chest 等空间切换。

    [:octicons-code-24: Space Blend API](../reference/systems/controller/space_blend.md)

</div>

## 打开创建工具

```python
from muziToolset.tools.controller import create_ctrl_tool

window = create_ctrl_tool.main()
```

## 标准层级

```text
zero
└── driven
    └── space
        └── connect
            └── offset
                └── ctrl
                    ├── ctrlSub
                    └── output
```

| 层级 | 作用 |
| --- | --- |
| `zero_` | 保存初始零值空间 |
| `driven_` | 接收系统驱动或修正 |
| `space_` | 空间切换 |
| `connect_` | 上层 Rig 连接 |
| `offset_` | 本地偏移 |
| `ctrl_` | Animator 操作 |
| `output_` | 向后续 Rig 输出稳定 Transform |

## 推荐步骤

1. 选择目标 Joint / Transform。
2. 打开 Controller Tool。
3. 选择 Shape、方向、大小和颜色。
4. 创建后先检查 Zero 和 Output 层级。
5. 后续 Rig 尽量连接 `output_*`，不要把所有系统直接接在动画控制器上。

!!! tip "Shape 和 Transform"
    修改 Controller 外观时尽量只改 Curve CV / Shape，避免无意改变动画控制器 Transform。

## 常见问题

**方向不对**：先检查 `axis`、目标 Joint Orientation，以及是否把 Shape Rotation 和 Transform Rotation 混用了。

**改了 Tool 但层级没变化**：标准控制器结构来自 `systems/controller/builder.py`，不是 UI Tool 本身。

## 相关 API

- [create_ctrl_tool.py](../reference/tools/controller/create_ctrl_tool.md)
- [create_fk_ctrl_tool.py](../reference/tools/controller/create_fk_ctrl_tool.md)
- [control_shape_utils.py](../reference/core/control_shape_utils.md)
- [systems/controller/builder.py](../reference/systems/controller/builder.md)
- [systems/controller/space_blend.py](../reference/systems/controller/space_blend.md)

[返回常用工具](tools.md){ .md-button }
[打开 Controller Builder API](../reference/systems/controller/builder.md){ .md-button .md-button--primary }
