# 常用工具

这页从“**我要完成什么**”出发，同时标明当前工具在新架构中的状态。

主工具箱已接入 20 个工具入口，按基础、骨骼、控制器、绑定、面部、蒙皮、BlendShape、检查与清理八个分类显示。

在 Maya Python Script Editor 中运行：

```python
import muziToolset
window = muziToolset.show()
```

点击工具卡片的“打开”显示独立窗口；快速吸附和创建 FK 控制器是“执行”按钮，会按当前选择直接操作场景。再次打开会恢复已有窗口。

工具底层操作按职责放在 `core/common`、`core/rigging`、`core/geometry` 和 `core/deformation`，运行时不导入历史归档。控制器创建由 `systems/components/controller_builder.py` 调用当前 `Ctrl` 实现。

验证范围：普通 Qt 环境检查所有窗口的创建、显示与复用；真实 Maya 的场景操作需运行 `tests/tool_window_smoke_test.py` 等 Maya 测试，并使用实际模型验证。

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

| 分组 | 负责的操作 |
|---|---|
| `core/common` | 属性、层级、命名、变换、选择、连接、文件、数学和动画 |
| `core/rigging` | 控制器、Guide、骨骼、骨骼链、约束和吸附 |
| `core/geometry` | 曲线创建、Shape 查询和曲线采样 |
| `core/deformation` | 蒙皮、BlendShape 和模型检查 |

工具使用分组路径导入，例如：

```python
from muziToolset.core.common import scene_utils
from muziToolset.core.deformation import skin_utils
from muziToolset.core.rigging import constraint_utils
```

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

## Controller 与骨骼工具接入

创建控制器、创建 FK 控制器、Rig IK 控制器和裙子控制器使用同一个 `controller_builder`。它负责收集 Shape、大小、轴向、目标和 SubCtrl 开关，实际图形与标准层级由当前 `Ctrl` 创建。FK 链将后一个 Zero 挂到前一个 Output，约束也使用 Output。

Jnt 工具和关节链重采样已归入“骨骼工具”，使用 `core/rigging/jnt_utils.py` 和 `jnt_chain_utils.py`；不再依赖已删除的平铺路径。

详细见 [Controller 手册](controller.md) 与 [Jnt 手册](jnt.md)。
