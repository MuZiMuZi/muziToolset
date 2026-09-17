# 常用工具

这页从“**我要完成什么**”出发，同时标明当前工具在新架构中的状态。

MuziTools 目前同时存在两类入口：

```text
正式新架构入口
    Rig Library / RigModule / core/common / core/rigging

独立 Tool UI
    tools/*
    其中部分仍在迁移旧 Core 平铺依赖
```

因此看到一个 Tool 文件存在，并不代表它已经完全迁移到当前正式 Core。

<div class="grid cards" markdown>

-   :material-view-dashboard-outline:{ .lg .middle } **Rig Library**

    ---

    当前模块化绑定主入口。Setup → Guide → Ctrl → Final。

    [:octicons-arrow-right-24: Rig Library](rig-library.md)

-   :material-vector-circle:{ .lg .middle } **Controller**

    ---

    Shape、颜色、大小、轴向、标准 Hierarchy 和 Output。

    [:octicons-arrow-right-24: Controller](controller.md)

-   :material-bone:{ .lg .middle } **Jnt**

    ---

    Joint 创建、Guide Match、Radius、Local Axis 和 Module Joint Output。

    [:octicons-arrow-right-24: Jnt](jnt.md)

-   :material-face-recognition:{ .lg .middle } **Face Rig**

    ---

    当前正式模块以 Eye / Ear / Tongue 为主，Guide 由标准 Face Locator 提供。

    [:octicons-arrow-right-24: Face Guide](face-guide.md)

-   :material-form-textbox:{ .lg .middle } **基础操作**

    ---

    Rename、Attribute、Connection、Constraint、Snap 等独立工具。

    [:octicons-arrow-right-24: 基础工具](basic-tools.md)

-   :material-human-handsup:{ .lg .middle } **Skin**

    ---

    Smooth Bind、Copy Weight、Influence、Normalize 和权重文件。

    [:octicons-arrow-right-24: Skin](skin.md)

-   :material-shape-plus:{ .lg .middle } **BlendShape**

    ---

    Add Target、Invert Shape 与历史 BlendShape Helper。

    [:octicons-arrow-right-24: BlendShape](blendshape.md)

-   :material-broom:{ .lg .middle } **Cleanup**

    ---

    Model Checker 与 Hierarchy Cleaner。

    [:octicons-arrow-right-24: Cleanup](cleanup.md)

</div>

## 当前 Tools 目录

```text
tools/
├── basic/
│   ├── attr_tool.py
│   ├── connections_tool.py
│   ├── constraint_tool.py
│   ├── rename_tool.py
│   └── snap_tool.py
│
├── blendshape/
│   ├── add_blendshape_tool.py
│   └── invert_shape_tool.py
│
├── clean/
│   ├── hierarchy_cleaner.py
│   └── model_checker.py
│
├── controller/
│   ├── control_shape_tool.py
│   ├── create_ctrl_tool.py
│   └── create_fk_ctrl_tool.py
│
├── face/
│   ├── face_rig_tool.py
│   └── face_select_key_tool.py
│
├── jnt/
│   ├── jnt_resamp_tool.py
│   └── jnt_tool.py
│
├── rig/
│   ├── modular_rig_tool.py
│   ├── rig_tool.py
│   └── skirt_ctrl_tool.py
│
└── skin/
    └── skin_tool.py
```

API Reference 会为这些正式 Runtime Python 文件生成独立页面。

## Tool 的职责

Tool 主要负责：

```text
Qt UI
Selection
用户输入
Maya Warning / Status
调用底层 API
```

Tool 不应该负责：

```text
完整 Rig Module Lifecycle
重复实现 Naming
重复实现 Controller Core
重复实现 Joint Core
复制多个系统都会用到的 Maya 算法
```

## 当前正式 Core 路径

新架构已经收敛到：

```text
core/common/
    attr_utils.py
    hierarchy_utils.py
    name_utils.py
    transform_utils.py

core/rigging/
    ctrl_utils.py
    guide_utils.py
    jnt_utils.py
```

这些是当前网站和新 Module 文档应优先引用的 Core。

## 为什么有些 Tool 还写着旧 `core.xxx_utils`

仓库中部分独立 UI 是在 Core 收敛前编写的，例如源码仍可能看到：

```python
from ...core import scene_utils
from ...core import rename_utils
from ...core import skin_utils
from ...core import constraint_utils
```

但当前 `core/` 根目录已经不再以这些平铺模块作为正式结构。

这类文件应理解为：

```text
UI / 功能意图仍有价值
    ↓
底层依赖待迁移
```

而不是反过来把正式 Core 架构重新定义成旧结构。

!!! warning "文档原则"
    网站会如实展示这些源码文件和 API，但用户手册会明确区分“当前正式实现”和“待迁移独立 Tool”。这样可以避免旧 Tool 的 import 关系再次污染新架构说明。

## 当前最稳定的开发入口

如果你正在开发新 Rig 功能，推荐优先顺序：

```text
1. core/common
2. core/rigging
3. systems/rig_module.py
4. systems/face / systems/components
5. systems/rig/library_service.py
6. systems/rig/ui
```

如果只是做 UI 操作工具，再进入：

```text
tools/
```

## Tool 和 Rig Library 的区别

### Tool

适合一次性操作：

```text
Rename
改 Attribute
改 Controller Shape
Copy Skin Weight
检查 Model
```

### Rig Library

适合有状态、可重建的模块：

```text
Eye
Ear
Tongue
FK Chain
```

Rig Library 会记录：

```text
Module Config
Build State
Connection State
Ownership
Guide Contract
```

普通 Tool 不应该伪装成完整模块生命周期。

## 当前 Face Tool 与 Face System

当前正式 Face System：

```text
systems/face/ear_module.py
systems/face/eye_module.py
systems/face/tongue_module.py
systems/face/face_guide_config.py
```

`tools/face/` 是独立 UI / 辅助入口，不应该作为 Face Rig 架构事实来源。

真正的 Module Build 由 System 完成。

## 当前 Controller Tool 状态

`tools/controller/create_ctrl_tool.py` 仍保留 `legacy_reference` 兼容调用。

因此：

```text
Rig Library / Face Module
    -> core/rigging/ctrl_utils.py

独立 Create Ctrl Tool
    -> 仍有兼容层，待迁移
```

详细见 [Controller 手册](controller.md)。

## 当前 Jnt Tool 状态

`tools/jnt/jnt_tool.py` 的 UI 功能很多，但底层仍引用若干旧 Core 平铺模块。

正式 Module Joint 路径：

```text
systems/rig_module.py
    ↓
core/rigging/jnt_utils.py
```

详细见 [Jnt 手册](jnt.md)。

## 我应该从哪里开始？

| 需求 | 推荐入口 |
| --- | --- |
| 做模块化角色绑定 | [Rig Library](rig-library.md) |
| 调 Face 定位 | [Face Guide](face-guide.md) |
| 改 Controller Core | [Controller](controller.md) |
| 改 Joint Core | [Jnt](jnt.md) |
| 做局部小操作 | 本页对应 Tool |
| 查源码参数 | [API Reference](../reference/index.md) |
| 判断代码应该放哪 | [总体架构](../architecture/index.md) |

## 文档阅读建议

```text
任务
    ↓
用户手册
    ↓
确定正式模块 / Tool
    ↓
API Reference
    ↓
源码
```

不要只根据文件名猜当前推荐实现。

[用户手册](index.md){ .md-button }
[API Reference](../reference/index.md){ .md-button .md-button--primary }
