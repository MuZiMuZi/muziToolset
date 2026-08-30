# Controller 工作流

这页说明 MuziTools 中 Controller 的推荐使用方式，以及 Tool、System、Core 三层分别负责什么。

## 你什么时候需要看这页

- 创建标准绑定控制器；
- 创建 FK Controller；
- 修改 Controller Shape；
- 调整控制器颜色、大小和轴向；
- 创建 Sub Control；
- 修改 Zero / Driven / Space / Connect / Offset 层级；
- 排查控制器创建后层级不正确的问题。

## 推荐架构

```text
Create Ctrl Tool
        ↓
systems/controller/builder.py
        ↓
core/control_shape_utils.py
```

UI Tool 负责选择和参数；Builder 负责标准控制器结构；Core 只处理 Shape 等通用底层能力。

## 创建标准 Controller

UI 入口：

- [create_ctrl_tool.py](../reference/tools/controller/create_ctrl_tool.md)

核心 Builder：

- [systems/controller/builder.py](../reference/systems/controller/builder.md)

打开工具：

```python
from muziToolset.tools.controller import create_ctrl_tool

window = create_ctrl_tool.main()
```

## 标准层级

Controller Builder 当前的目标层级是：

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

这些 Group 的用途应该保持稳定：

| Group | 作用 |
| --- | --- |
| `zero_` | 保存 Controller 初始零值空间 |
| `driven_` | 接收驱动、修正或系统输出 |
| `space_` | 空间切换 |
| `connect_` | 上层 Rig 连接 |
| `offset_` | 本地偏移 |
| `ctrl_` | Animator 直接操作 |
| `output_` | 向后续 Rig 输出稳定 Transform |

## 创建 FK Controller

快速入口：

- [create_fk_ctrl_tool.py](../reference/tools/controller/create_fk_ctrl_tool.md)

适合：

- 选中一条 Joint Chain；
- 快速生成 FK Controls；
- Controller 跟随 Joint 命名；
- 需要标准父子层级时。

## 修改 Controller Shape

入口：

- [control_shape_tool.py](../reference/tools/controller/control_shape_tool.md)

底层：

- [control_shape_utils.py](../reference/core/control_shape_utils.md)

适合：

- 应用 Shape Preset；
- 调整 Shape 大小；
- 旋转 Shape；
- 改颜色；
- 上传 / 保存 Shape 数据。

注意：Shape 修改应该尽量只操作 Curve CV / Shape，而不要无意改变 Controller Transform。

## 轴向与大小

创建 Controller 时常见参数：

```text
shape
radius
axis
target
parent
color
rotate_x
create_sub_control
create_extra_groups
add_to_set
```

具体类型和默认值直接查看：

- [Controller Builder API](../reference/systems/controller/builder.md)

## 颜色

标准左右颜色应由统一规则生成，而不是每个 Tool 自己写一套。

常见约定：

```text
LF / Left    → 蓝色系
RT / Right   → 红色系
MD / Center  → 黄色系
```

如果修改颜色规则，应该优先检查 Builder 的统一逻辑。

## Sub Control

Sub Control 适合：

- 局部二级调整；
- Face / Ribbon / Secondary Control；
- Animator 不希望主控制器过度复杂时。

推荐用主 Controller 的属性控制 Sub Control Visibility，而不是单独让 Animator 去 Outliner 找节点。

## Output Group

后续 Rig 尽量读取稳定输出层：

```text
output_*
```

而不是直接把所有系统连接到动画 Controller 本身。

这样后续增加 Secondary / Offset / Space 时，不容易破坏已有连接。

## Space Blend

空间切换相关系统：

- [space_blend.py](../reference/systems/controller/space_blend.md)

适合：

- World / Root / Chest / Hand Space；
- 多 Parent Matrix Blend；
- Animator 可切换的 Follow 行为。

## 常见问题

### Controller 创建出来方向不对

检查：

1. `axis` 是否正确；
2. Shape Rotation 是否只是修改 CV；
3. Target Joint Orientation 是否与期望一致；
4. 是否把 Transform Rotate 和 Shape Rotate 混在一起。

### Controller 重复创建出现 `_001_001`

通常意味着 Name 或 Rebuild 策略没有统一。优先检查 Builder 的 `next available name` 和目标命名规则，而不是在 Tool UI 中追加临时后缀。

### Tool 修改了但 Rig 结构没变

如果结构来自 `systems/controller/builder.py`，只改 `create_ctrl_tool.py` 不会改变底层层级。

## 继续查看

- [绑定工作流](rigging.md)
- [Controller Builder API](../reference/systems/controller/builder.md)
- [Control Shape Utils](../reference/core/control_shape_utils.md)
