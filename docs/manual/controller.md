# Controller

用于创建和维护 MuziTools 标准绑定控制器。

<div class="grid cards" markdown>

-   :material-vector-circle:{ .lg .middle } **创建标准 Controller**

    ---

    生成标准层级、Shape、颜色和 Output。

    [:octicons-code-24: CtrlBase API](../reference/systems/ctrl_base.md)

-   :material-axis-arrow:{ .lg .middle } **创建 FK Controller**

    ---

    根据 Joint Chain 快速生成 FK 控制器。

    [:octicons-code-24: FK Tool API](../reference/tools/controller/create_fk_ctrl_tool.md)

-   :material-shape-outline:{ .lg .middle } **修改 Shape**

    ---

    调整 Shape、大小、旋转和颜色。

    [:octicons-code-24: Shape Tool API](../reference/tools/controller/control_shape_tool.md)

-   :material-source-branch:{ .lg .middle } **Follow / Space**

    ---

    Follow、Space Switch 和 Space Blend 都由 CtrlBase 统一提供。

    [:octicons-code-24: CtrlBase API](../reference/systems/ctrl_base.md)

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
                    └── output
```

如果启用 Sub Controller，Sub Shape / Node 会由 `ctrl_base.create_ctrl()` 按当前正式配置创建。

| 层级 | 作用 |
| --- | --- |
| `zero_` | 保存初始零值空间 |
| `driven_` | 接收系统驱动或修正 |
| `space_` | 空间切换 |
| `connect_` | 上层 Rig 连接 |
| `offset_` | 本地偏移 |
| `ctrl_` | Animator 操作 |
| `output_` | 向后续 Rig 输出稳定 Transform |

## Controller 的唯一正式实现

```text
systems/ctrl_base.py
```

Controller Tool、Face Module、Body Module 都应直接调用 CtrlBase。

例如：

```python
from muziToolset.systems import ctrl_base

result = ctrl_base.create_ctrl(
    name="ctrl_md_hand_main_001",
    shape="circle",
    radius=1.0,
    axis="Y+",
    target_node="jnt_md_hand_bind_001"
)
```

旧目录：

```text
systems/controller/
```

已经删除，不再维护 `builder.py` 或 `space_blend.py` 包装层。

## 推荐步骤

1. 选择目标 Joint / Transform。
2. 打开 Controller Tool。
3. 选择 Shape、方向、大小和颜色。
4. 创建后检查 Zero / Ctrl / Output 层级。
5. 后续 Rig 优先使用公开的 Controller Result 数据连接系统。

!!! tip "Shape 和 Transform"
    修改 Controller 外观时尽量只改 Curve CV / Shape，避免无意改变动画控制器 Transform。

## 常见问题

**方向不对**：检查 `axis`、目标 Joint Orientation，以及是否把 Shape Rotation 和 Transform Rotation 混用。

**改了 Tool 但层级没变化**：标准层级来自 `systems/ctrl_base.py`，UI Tool 只负责收集参数和调用正式 API。

## 相关 API

- [CtrlBase](../reference/systems/ctrl_base.md)
- [create_ctrl_tool.py](../reference/tools/controller/create_ctrl_tool.md)
- [create_fk_ctrl_tool.py](../reference/tools/controller/create_fk_ctrl_tool.md)
- [control_shape_utils.py](../reference/core/control_shape_utils.md)

[返回常用工具](tools.md){ .md-button }
[打开 CtrlBase API](../reference/systems/ctrl_base.md){ .md-button .md-button--primary }
