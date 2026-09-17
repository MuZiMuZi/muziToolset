# 总体架构

本页描述 **当前 `main` 分支真实存在的 MuziTools 架构**。

旧版 `RigBase / ModuleBase / CtrlBase`、旧 `systems/face/modules/` 分包和旧四层 Face System 说明已经不再作为当前架构文档保留。当前文档以仓库现有源码为准。

## 当前项目结构

```text
muziToolset/
├── app/                 # 应用入口、主工具箱、窗口生命周期
├── core/                # Maya 通用底层能力
│   ├── common/          # Name / Attr / Hierarchy / Transform
│   ├── rigging/         # Ctrl / Guide / Jnt
│   └── bake/            # 历史兼容与旧工具能力
├── systems/             # 完整 Rig System / Module
│   ├── rig_module.py    # 当前通用 Rig Module 生命周期基础类
│   ├── face/            # Face Rig Module
│   ├── rig/             # Rig Library 与 Modular Rig System
│   ├── body/            # Body Rig
│   └── components/      # 可复用 Rig Component
├── tools/               # 绑定师直接使用的小工具与 Tool Entry
├── ui/                  # 通用 PySide Window / Theme / Widget
├── resources/           # Controller Shape、Face Guide 等静态资源
├── scripts/             # 文档、迁移、审计和维护脚本
├── tests/               # 静态 Contract、文档与 Rig Library 测试
└── docs/                # MkDocs 文档网站源码
```

## 五层职责

### App

`app/` 负责 MuziTools 顶层应用体验：

```text
启动
主工具箱
窗口管理
Tool Discovery
```

App 不应该重新实现 Rig 算法。

### Core

`core/` 是最底层的 Maya 通用能力。

当前正式代码主要分成：

```text
core/common/
    name_utils.py
    attr_utils.py
    hierarchy_utils.py
    transform_utils.py

core/rigging/
    ctrl_utils.py
    guide_utils.py
    jnt_utils.py
```

Core 的目标是提供不依赖具体 Face / Body 业务语义的基础操作。

`core/bake/` 仍保留历史兼容能力，但新代码应优先使用当前 `core/common` 与 `core/rigging` 接口。

### Systems

`systems/` 负责完整、可重复构建的 Rig 业务系统。

它可以组合多个 Core 能力，并定义：

```text
Guide Contract
Joint / Controller Creation
Hierarchy
Connection
Build / Rebuild
Module Output
```

当前最重要的基础类是：

```text
systems/rig_module.py
    RigModule
```

### Tools

`tools/` 是用户操作入口。

Tool 层主要负责：

```text
读取 Maya Selection
收集用户参数
显示 UI
调用 Core 或 System
反馈结果
```

复杂 Rig 构建逻辑不应该长期堆在 Tool 文件中。

例如：

```text
tools/rig/modular_rig_tool.py
```

只负责打开 Modular Rig System UI，而不实现 Module Build 算法。

### UI

`ui/` 提供公共 PySide 基础设施：

```text
Theme
Window Utility
Reusable Widget
统一视觉和交互规范
```

业务 UI 可以位于具体 System 内，例如：

```text
systems/rig/ui/
```

但应该复用公共 `ui/` 能力。

## 推荐依赖方向

```text
app
 ↓
tools ──────┐
 ↓           │
systems     ui
 ↓           │
core  ←──────┘
```

更准确地说：

- `core` 不依赖具体 Tool / System 业务；
- `systems` 可以依赖 `core`；
- `tools` 可以调用 `systems` 或较小的 `core` 能力；
- `app` 负责发现和打开 Tool；
- `ui` 是界面基础设施，不承担 Rig Build 事实来源。

## 当前 Rig Module 生命周期

当前统一 Module 基础类是：

```python
from muziToolset.systems.rig_module import RigModule
```

`RigModule` 提供的核心阶段：

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

同时支持把“生成输出”和“最终连接”拆开：

```text
build_outputs()
    Joint + Controller + Hierarchy

connect_outputs()
    Load Existing Outputs + Connection

build()
    完整构建
```

这种拆分非常重要，因为当前 Modular Rig Workflow 允许用户在前面阶段修改 Guide、Controller 或 Joint 后，再重新生成连接。

## Rig Module 基础职责

`RigModule` 当前提供：

```text
get_guides
    读取外部 Guide 数据

create_joint
    创建 / 获取单个 Joint，并可匹配 Guide

create_ctrl
    创建 / 获取单个 Controller，并设置 Shape / Color / Size / Axis

create_joints
    子类定义完整 Joint System

create_ctrls
    子类定义完整 Controller System

setup_hierarchy
    创建 Module Joint / Controller Master Group

load_outputs
    子类读取已经存在的构建结果

connect_rig
    子类建立 Constraint / Matrix / Utility / Deformer 连接

build_outputs
    生成 Joint / Controller / Hierarchy

connect_outputs
    读取已有结果并建立连接

build
    完整生命周期
```

## 当前 Face System

当前正式 Face System 位于：

```text
systems/face/
├── __init__.py
├── face_guide_config.py
├── eye_module.py
├── ear_module.py
└── tongue_module.py
```

这里已经不再使用旧文档中的：

```text
systems/face/setup/
systems/face/guide/
systems/face/modules/
systems/face/build/
systems/face/finalize/
```

这些旧目录关系不再作为当前架构说明。

当前 Face Module 直接基于 `RigModule` 构建。

### Eye Module

`systems/face/eye_module.py` 是当前完成度最高的 Face Module 之一。

Guide Contract：

```text
loc_<side>_eye_ball_001
loc_<side>_eye_iris_001
loc_<side>_eye_aim_001
```

驱动链：

```text
Aim Ctrl
    ↓
Aim Output
    ↓
Aim Constraint
    ↓
Main Driven
    ↓
Main Ctrl
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

关键原则：

- Main Ctrl 可见位置保持在 Iris；
- Main 旋转 Pivot 位于 Ball；
- Aim 只驱动旋转；
- Eye Joint 最终只接收 Orientation；
- Pose Driver / Pose Driven 为后续 Eyelid、RBF 和 Corrective 保留稳定接口。

### Ear / Tongue

`ear_module.py` 与 `tongue_module.py` 继续使用 `RigModule` 的模块化构建方式，负责各自 Guide、Joint、Controller 和 Hierarchy。

详细 API 以自动生成页面为准。

## 当前 Rig Library

模块化绑定系统当前位于：

```text
systems/rig/
├── __init__.py
├── library_catalog.py
├── library_service.py
└── ui/
    ├── library_style.py
    ├── library_widgets.py
    └── modular_rig_ui.py
```

职责划分：

```text
library_catalog.py
    定义可用 Rig Module 元数据和分类

library_service.py
    Rig Library 的创建、镜像、重建、调度和业务服务

ui/
    Rig Library / Modular Rig 用户界面
```

Tool 入口：

```text
tools/rig/modular_rig_tool.py
```

只负责调用：

```python
from muziToolset.systems import rig as rig_system
rig_system.create_ui()
```

## Controller / Joint 基础能力

当前 Controller 与 Joint 的底层正式能力位于：

```text
core/rigging/ctrl_utils.py
core/rigging/jnt_utils.py
```

Module 通过 `RigModule.create_ctrl()` 和 `RigModule.create_joint()` 统一使用这些能力。

因此当前文档不再把已经不存在的旧 `systems/ctrl_base.py` 当作 Controller 唯一入口。

## Naming

当前 Module 代码使用：

```python
from muziToolset.core.common import name_utils
```

典型调用：

```python
name_utils.Name(
    type="ctrl",
    side="lf",
    part="eye",
    function="main",
    index=1
).name
```

文档和示例应以当前真实 API 为准，不再沿用旧版 `RigBase.create_name(node_type=...)` 示例。

## Build 与 Rebuild 原则

当前 Rig 架构非常强调可重建性。

一个 Module 应尽量做到：

```text
已有节点可读取
重复 Build 不无限叠加
旧连接可安全删除
Guide 调整后可重新生成输出
Controller / Joint 调整后可重新连接
稳定节点名称可被其他模块引用
```

Eye Module 已经提供：

```text
load_outputs()
delete_connections()
connect_rig()
build()
```

用于支持这种工作方式。

## 文档事实来源

当前架构文档描述职责和调用方向；具体类、方法、参数和返回值以源码 Docstring + 自动 API Reference 为准。

继续查看：

- [Face System](face-system.md)
- [Tools 与 Systems](tools-systems.md)
- [API Reference](../reference/index.md)
- [RigModule API](../reference/systems/rig_module.md)
- [Rig Library API](../reference/systems/rig/index.md)
- [Face API](../reference/systems/face/index.md)
