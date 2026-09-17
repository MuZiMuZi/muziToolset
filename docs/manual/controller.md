# Controller

MuziTools 当前 Controller 底层能力集中在：

```text
core/rigging/ctrl_utils.py
```

正式 Rig Module 不应该自己重复实现 Shape、颜色、大小、轴向和标准层级逻辑，而是通过 `Ctrl` 或 `RigModule.create_ctrl()` 复用这一层。

<div class="grid cards" markdown>

-   :material-vector-circle:{ .lg .middle } **创建 Controller**

    ---

    创建或读取 Controller Transform，并设置 Shape、颜色、大小、轴向和标准层级。

    [:octicons-code-24: Ctrl API](../reference/core/rigging/ctrl_utils.md)

-   :material-shape-outline:{ .lg .middle } **Shape Library**

    ---

    Controller Shape 统一来自 `resources/controller_shapes/` 中的 JSON 资源。

    [:octicons-code-24: 查看 Controller API](../reference/core/rigging/ctrl_utils.md)

-   :material-axis-arrow:{ .lg .middle } **外观调整**

    ---

    调整颜色、大小、轴向、Curve CV 旋转和 Shape Offset，不污染 Animator Transform。

    [:octicons-code-24: 查看 Ctrl 方法](../reference/core/rigging/ctrl_utils.md)

-   :material-sitemap-outline:{ .lg .middle } **Rig Module 集成**

    ---

    Face、FK Chain 等模块通过 `RigModule.create_ctrl()` 复用 Controller 能力。

    [:octicons-code-24: RigModule API](../reference/systems/rig_module.md)

</div>

## 当前正式实现

Controller 相关职责分成两层：

```text
core/rigging/ctrl_utils.py
    ↓
Controller 基础能力

systems/rig_module.py
    ↓
Module 构建时的 Controller 调度
```

`core/rigging/ctrl_utils.py` 负责：

- 创建或读取 Controller Transform；
- 读取和替换 Shape；
- 设置 Maya Index Color；
- 修改 Shape 显示大小；
- 设置 X+ / X- / Y+ / Y- / Z+ / Z- 轴向；
- Curve CV 额外旋转；
- Curve CV Offset；
- 创建 Sub Controller；
- 创建标准 Controller Hierarchy；
- 维护 Controller Shape Library。

`RigModule` 负责：

- Module Naming；
- Guide Match；
- 调用 Controller 底层能力；
- 把生成结果保存到 Module 生命周期中；
- 后续和 Joint / Connection 一起进入 Build / Rebuild。

## `Ctrl` 的基本使用

```python
from muziToolset.core.rigging import ctrl_utils

ctrl = ctrl_utils.Ctrl(
    "ctrl_lf_eye_main_001"
)

ctrl.create_ctrl(
    shape_name="shape_016",
    ctrl_color=6,
    ctrl_size=1.5,
    ctrl_axis="X+",
    create_hierarchy=True,
    match_transform_target="loc_lf_eye_iris_001"
)
```

实例化 `Ctrl(name)` 时：

```text
同名 Transform 已存在
    ↓
直接复用

同名对象不存在
    ↓
创建基础圆形 Controller

同名对象存在但不是 Transform
    ↓
抛出 TypeError
```

因此 `Ctrl` 本身是一个“获取或创建”的 Controller 对象封装。

## `create_ctrl()` 的执行顺序

当前实现顺序为：

```text
set_ctrl_shape()
    ↓
set_ctrl_color()
    ↓
set_ctrl_size()
    ↓
set_ctrl_axis()
    ↓
可选 Match Transform
    ↓
可选 create_ctrl_hierarchy()
```

这个顺序很重要。

Shape 必须先创建，因为替换 Shape 会删除旧 Shape；如果先改颜色或大小，再替换 Shape，之前的外观设置会丢失。

## 标准 Controller Hierarchy

当前标准结构：

```text
zero
└── driven
    └── space
        └── connect
            └── offset
                └── ctrl
                    ├── subctrl
                    └── output
```

各层职责：

| 层级 | 用途 |
| --- | --- |
| `zero_` | 保存 Controller 创建时的初始空间，保持控制器 Local TRS 干净 |
| `driven_` | 接收 Aim、Constraint、Corrective 等系统驱动 |
| `space_` | 为 Space / Follow 类逻辑预留独立空间 |
| `connect_` | 模块之间的上层连接入口 |
| `offset_` | 程序化或绑定师额外 Offset 层 |
| `ctrl_` | Animator 直接操作的主控制器 |
| `subctrl_` | 可选次级动画控制器 |
| `output_` | 后续 Rig 使用的稳定输出 Transform |

当前 `subctrl` 的 TRS 与 `rotateOrder` 会通过属性连接传到 `output`。

因此：

```text
Animator
    ↓
ctrl
    ↓
subctrl
    ↓
output
    ↓
后续 Joint / Driver / Module
```

## 为什么 Output 很重要

后续系统不应该随意读取 Controller Curve Shape，也不应该把动画师的 UI 节点直接当作内部驱动接口。

推荐：

```text
Controller
    ↓
output_*
    ↓
Rig Connection
```

这样以后替换 Controller Shape、修改显示大小、增加 SubCtrl 时，系统连接不会因为 UI 外观变化而失效。

Eye Rig 就使用这种模式：

```text
Aim Ctrl Output
    ↓
Main Driven
    ↓
Main Ctrl Output
    ↓
Pose Driver
    ↓
Pose Driven
    ↓
Eye Joint
```

## Shape Library

资源目录：

```text
resources/controller_shapes/
```

一个 Shape 通常对应：

```text
shape_xxx.json
shape_xxx.png / jpg   # 可选预览
```

`get_ctrl_shape_list()` 会扫描 JSON 文件并返回可用 Shape 名称。

Shape Library 的标准方向为：

```text
X+
```

加载 Shape 后，再通过 `set_ctrl_axis()` 转换到最终方向。

## 设置 Controller 颜色

```python
ctrl.set_ctrl_color(6)
```

使用 Maya Drawing Override Index Color。

如果 Controller 下有多个 Curve Shape，所有 Shape 会一起更新。

Rig Library Step 03 修改 `ctrl_color` 时，同样会走 Controller 底层能力更新已经生成的模块。

## 调整大小

```python
ctrl.set_ctrl_size(1.25)
```

这里修改的是：

```text
NurbsCurve CV
```

而不是：

```text
ctrl.scale
```

因此 Animator 看到的 Transform Scale 可以继续保持默认值。

这也是 Rig Library Step 03 能实时修改控制器视觉大小，而不破坏 Rig Transform 的关键。

## 设置轴向

```python
ctrl.set_ctrl_axis("Y+")
```

支持：

```text
X+
X-
Y+
Y-
Z+
Z-
```

轴向调整只修改 Shape CV，不修改 Controller Transform Rotate。

`ctrl_axis` 还会作为元数据保存在 Controller 上，使重复切换方向时能够按“绝对轴向”处理，而不是不断累积旋转。

## 额外 Shape Rotation

```python
ctrl.set_ctrl_rotate(
    rx=90,
    ry=0,
    rz=0
)
```

适合：

- Shape 已经面向正确基础轴；
- 还需要额外视觉旋转；
- 不希望改变 Controller Transform。

## Shape Offset

```python
ctrl.set_ctrl_offset(
    tx=0,
    ty=1.0,
    tz=0
)
```

同样只移动 Curve CV。

常见用途：

- 把控制器视觉图形从关节中心稍微移开；
- 保持真正的旋转中心不变；
- 让面部控制器更容易选择。

## Sub Controller

标准 Controller 可以创建 `subctrl`。

它通常用于：

- 更细一层动画调整；
- 保留 Main Ctrl 的大范围动作；
- 给 Animator 增加局部二级控制。

当前默认 SubCtrl Shape 大小通常来自主 Controller 大小的一定比例，例如：

```text
main size × 0.7
```

具体由调用方决定。

## 在 Rig Module 中创建 Controller

业务 Module 通常不直接处理 Controller Shape 细节。

例如概念上：

```python
self.main_ctrl_object = self.create_ctrl(
    name="ctrl_lf_eye_main_001",
    guide="loc_lf_eye_iris_001",
    shape_name="shape_016",
    ctrl_color=17,
    ctrl_size=1.0,
    ctrl_axis="X+",
    create_hierarchy=True
)
```

这样 Module 只负责表达：

```text
我要什么 Controller
它在哪里
它叫什么
```

Shape、颜色、层级创建由 Core Controller 层负责。

## Rig Library Step 03

当前绑定库中，Controller 外观设置集中在 Step 03：

```text
Controller Size
Controller Color
Controller Axis
```

已经 Build 的 Module 修改这些值时：

```text
RigLibraryService.update_module()
    ↓
_apply_display()
    ↓
Ctrl(...)
    ↓
set_ctrl_size / set_ctrl_color / set_ctrl_axis
```

这意味着 Step 03 是**外观调整阶段**，不是重新创建整个 Module。

如果 Guide 改变，需要回到 Step 02 走 Rebuild；如果只是外观变化，Step 03 可以直接更新。

## 独立 Controller Tool

入口：

```python
from muziToolset.tools.controller import create_ctrl_tool

window = create_ctrl_tool.main()
```

当前独立 UI 提供：

- Shape 浏览；
- Shape 搜索；
- Size；
- Axis；
- Extra Rotate X；
- Maya Index Color；
- Selection / Hierarchy / World 创建模式；
- 自定义命名；
- SubCtrl；
- `ctrl_set` 选项。

!!! warning "当前兼容状态"
    `tools/controller/create_ctrl_tool.py` 目前仍保留一层 `legacy_reference` 的 CtrlBase / RigBase 兼容调用。它不是 Rig Library / Face Module 的新系统主路径。正式 Module 构建应以 `systems/rig_module.py` + `core/rigging/ctrl_utils.py` 为准；这个独立工具后续可以继续迁移并删除兼容层。

## 常见问题

### Controller 创建后位置不正确

先检查：

```text
Guide / Target World Matrix
    ↓
Match Transform
    ↓
Hierarchy Parent
    ↓
Pivot
```

Face Eye Module 还有一个特殊规则：

```text
Main Ctrl 可见位置 = Iris Guide
Main Ctrl Rotate Pivot = Ball Guide
```

所以不能简单把整个 Controller Hierarchy 移到 Ball。

### 修改 Shape 后 Transform 有数值

正常 Shape 编辑应该发生在 Curve CV 上。

如果 `translate / rotate / scale` 被修改，说明操作到了 Transform，不是 Shape。

### 多次切轴向后越来越歪

应该使用 `set_ctrl_axis()` 的绝对轴向逻辑，不要不断对 Transform 或 CV 追加相对旋转。

### Controller 已经存在

`Ctrl(name)` 会尝试复用已有同名 Transform。

如果同名节点不是 Transform，会抛出错误，而不是覆盖用户节点。

## 相关 API

- [ctrl_utils.py](../reference/core/rigging/ctrl_utils.md)
- [rig_module.py](../reference/systems/rig_module.md)
- [create_ctrl_tool.py](../reference/tools/controller/create_ctrl_tool.md)
- [create_fk_ctrl_tool.py](../reference/tools/controller/create_fk_ctrl_tool.md)
- [control_shape_tool.py](../reference/tools/controller/control_shape_tool.md)
- [Rig Library](rig-library.md)

[返回常用工具](tools.md){ .md-button }
[打开 Controller API](../reference/core/rigging/ctrl_utils.md){ .md-button .md-button--primary }
