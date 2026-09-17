# 绑定工作流

MuziTools 当前推荐把完整绑定拆成两条并行思路：

```text
模块化 Rig Library
    用于可重复构建的 Rig Module

独立 Tools
    用于命名、Controller、Joint、Skin、BlendShape、清理等局部任务
```

两者共享同一套 Core 基础能力，不应该各自复制底层算法。

## 推荐总流程

```text
01 模型 / 场景检查
        ↓
02 Rig Library Setup
        ↓
03 Guide 定位与镜像
        ↓
04 生成 Joint + Controller
        ↓
05 调整 Controller / Joint 外观
        ↓
06 Final 建立模块连接
        ↓
07 Skin / Deformer
        ↓
08 BlendShape / Corrective
        ↓
09 发布前检查
```

<div class="grid cards" markdown>

-   :material-broom:{ .lg .middle } **模型与场景**

    ---

    检查 Transform、History、Outliner、命名和发布前状态。

    [:octicons-arrow-right-24: 场景清理](cleanup.md)

-   :material-view-dashboard-outline:{ .lg .middle } **Rig Library**

    ---

    使用四步模块化流程创建、调整、重建并最终连接 Rig Module。

    [:octicons-arrow-right-24: Rig Library](rig-library.md)

-   :material-face-recognition:{ .lg .middle } **Face Guide**

    ---

    调整标准 Face Locator，并作为 Eye / Ear / Tongue 等模块的构建来源。

    [:octicons-arrow-right-24: Face Guide](face-guide.md)

-   :material-vector-circle:{ .lg .middle } **Controller**

    ---

    Shape、颜色、大小、轴向、标准 Hierarchy 和 Output。

    [:octicons-arrow-right-24: Controller](controller.md)

-   :material-bone:{ .lg .middle } **Joint**

    ---

    Joint 创建、Guide Match、Radius、显示和 Module Joint System。

    [:octicons-arrow-right-24: Jnt](jnt.md)

-   :material-human-handsup:{ .lg .middle } **Skin**

    ---

    SkinCluster、Influence 和权重工作流。

    [:octicons-arrow-right-24: Skin](skin.md)

-   :material-shape-plus:{ .lg .middle } **BlendShape**

    ---

    Target、Corrective、Invert Shape 和后续表情修型。

    [:octicons-arrow-right-24: BlendShape](blendshape.md)

-   :material-tools:{ .lg .middle } **独立工具**

    ---

    需要局部操作时，从任务导向的工具页进入。

    [:octicons-arrow-right-24: 常用工具](tools.md)

</div>

## Rig Library 的四步流程

当前绑定库 UI 是：

```text
Step 01  Setup
Step 02  Guide
Step 03  Ctrl
Step 04  Final
```

但真正的数据阶段更准确地理解为：

```text
Setup
    ↓
Guide
    ↓
Build Outputs
    ├── Joint
    ├── Controller
    └── Hierarchy
    ↓
Adjust
    ├── Controller Appearance
    └── Joint Display
    ↓
Connect Outputs
```

### Step 01 — Setup

负责：

- 添加 Module / Template；
- 保存模块配置；
- 创建 Rig Library 根组；
- 创建 Joint Root；
- 创建 Controller Root。

当前根层级：

```text
grp_md_rig_library_001
├── grp_md_rig_jnt_001
└── grp_md_rig_ctrl_001
```

### Step 02 — Guide

负责：

- 导入 / 复用 Face Guide；
- 调整 Guide；
- 镜像左右 Guide；
- 从 Guide 生成 Joint / Controller；
- 已构建 Module 可以按最新 Guide Rebuild。

当前原则：

```text
Guide = Build Source
```

不要把已经生成的 Joint / Controller Transform 当成新的构建事实来源。

### Step 03 — Ctrl

这个阶段实际上同时调整：

```text
Controller
Joint
```

Controller：

```text
Size
Color
Axis
Visibility
```

Joint：

```text
Radius
Local Axis
Visibility
```

这类显示调整不应该重建 Module，也不应该修改 Guide。

### Step 04 — Final

负责：

```text
load_outputs()
    ↓
connect_rig()
```

最终为已经确认的 Joint / Controller 建立正式驱动连接。

因此 Final 不应该再承担 Controller 外观编辑。

## 当前模块构建生命周期

所有正式 `RigModule` 子类都遵循统一生命周期：

```text
get_guides()
    ↓
create_joints()
    ↓
create_ctrls()
    ↓
setup_hierarchy()
    ↓
connect_rig()
```

为了支持四步 UI，又拆成：

```text
build_outputs()
    ↓
Joint + Controller + Hierarchy

connect_outputs()
    ↓
Connection
```

这就是为什么你可以在 Final 之前修改 Controller / Joint。

## 当前 Rig Library 正式模块

`RigLibraryService._make_builder()` 当前调度：

```text
EarModule
EyeModule
TongueModule
FKChain
```

因此网站和 UI 中应该把这些视为当前已接入模块。

未来 Brow / Lip / Eyelid 等进入正式 Builder 后，再加入 Module Catalog 与文档；不要提前把尚未接入的模块写成“已经可用”。

## Eye Rig 示例

Eye 是当前比较完整的模块示例。

Guide：

```text
Ball
Iris
Aim
```

Build Outputs：

```text
Eye Joint
Main Controller
Aim Controller
Module Groups
```

Final：

```text
Aim Output
    ↓
Aim Constraint
    ↓
Main Driven
    ↓
Main Output
    ↓
Pose Driver
    ↓
Pose Driven
    ↓
Orient Constraint
    ↓
Eye Joint
```

这展示了 MuziTools 当前推荐的模块思路：

```text
Guide 决定结构位置
Controller 提供动画输入
Output / Driver 提供稳定接口
Joint 接收最终结果
```

## Rebuild

当 Guide 变化时：

```text
删除当前 Module 自己拥有的输出
    ↓
重新 build_outputs()
    ↓
重新写入 Ownership Tag
    ↓
connected = False
    ↓
等待 Step 04 Final
```

Rebuild 不应该：

- 删除其他 Module；
- 接管用户同名节点；
- 自动认为旧连接仍然有效；
- 用旧 Joint / Controller 位置反推 Guide。

## Mirror

前三个阶段可以镜像左右模块。

镜像本质上是：

```text
Source Module Settings
    ↓
Target Module Settings

Source Guide World Position
    ↓
X = 0 Mirror
    ↓
Target Guide
```

如果目标 Module 已经 Build，会按镜像后的 Guide 重新生成输出。

Final 阶段不提供镜像，因为 Final 表示当前输出已经确认，正在建立最终驱动关系。

## 项目分层怎么选

当前目录选择规则：

| 需求 | 放在哪里 |
| --- | --- |
| 通用 Attribute / DAG / Naming / Transform | `core/common/` |
| Controller / Guide / Joint 基础能力 | `core/rigging/` |
| 完整可重建 Rig Module | `systems/` |
| Rig Library 配置 / 调度 / UI | `systems/rig/` |
| 绑定师直接打开的小工具 | `tools/` |
| Theme / Window / Widget | `ui/` |
| 顶层应用和工具箱 | `app/` |
| 自动化维护脚本 | `scripts/` |
| 静态契约与文档检查 | `tests/` |

不存在“某个完整 Rig Workflow 应该放 Core”的情况。

## Core / System / Tool 的正确关系

```text
Core
    提供原子能力

System
    组合原子能力成为完整 Rig

Tool
    收集用户输入并调用能力
```

错误模式：

```text
Tool 自己重写一套 Controller
System 再重写一套 Controller
Core 又有一套 Controller
```

正确模式：

```text
core/rigging/ctrl_utils.py
        ↑
RigModule / System
        ↑
UI / Tool
```

## Compatibility 代码怎么看

仓库中仍存在：

```text
core/bake/
legacy_reference/
```

这些内容不应该再定义当前架构。

如果某个现有 Tool 仍然引用旧入口，应该把它标记为兼容 / 待迁移，而不是为了迁就旧 Tool，把整个 Core 文档重新写回旧结构。

## 发布前检查

一个 Module 完成后至少确认：

```text
Guide Naming
Joint Naming
Controller Naming
Hierarchy
Controller Zero Values
Controller Output
Joint Radius / Axis
Ownership Tag
Build State
Connection State
Rebuild
Mirror
Maya Undo
```

完整角色还需要继续检查：

```text
Skin
BlendShape
History
Unused Nodes
Outliner
Animation Set
最终控制器选择
```

## 继续查看

[Rig Library](rig-library.md){ .md-button }
[总体架构](../architecture/index.md){ .md-button }
[API Reference](../reference/index.md){ .md-button .md-button--primary }
