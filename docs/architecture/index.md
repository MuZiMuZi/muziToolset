# 总体架构

MuziTools 当前唯一正式运行框架是仓库根包 `muziToolset`。

```text
muziToolset/
├─ app/         # 应用入口、主工具箱、窗口生命周期
├─ ui/          # Theme 与通用 UI Widget
├─ core/        # Maya 通用底层能力
├─ tools/       # 用户直接使用的小工具
├─ systems/     # RigBase / ModuleBase / CtrlBase / Rig System
├─ resources/   # Guide Template、Controller Shape 等静态资源
└─ tests/       # Static Gate + Maya Smoke
```

## 依赖方向

```text
app / ui / tools
        ↓
      systems
        ↓
       core
```

`core` 不能反向依赖 `tools / systems / app / ui`。

## Systems 0.4 基础

```text
systems/
├── rig_base.py
├── module_base.py
├── ctrl_base.py
├── face/
├── body/
└── rig/
```

三个基础职责：

```text
RigBase
    Rig Naming

ModuleBase / RigModuleBase
    Module Lifecycle

CtrlBase
    Controller Workflow
```

完整业务单元统一称为 **Module**，不再使用 Component。

## Step / Module / Builder / Core

```text
Step
    用户工作流阶段

Module
    Teeth / Jaw / Tongue / Lip / Eye / Eyelid / Brow 等完整业务单元

Builder
    Curve Attachment / Zip / Radial Joint 等可组合算法

Core
    Matrix / Curve / Joint / DAG / Attribute 等通用 Maya 能力
```

## Face System

Face System 按四步 Workflow 分包：

```text
systems/face/
├── face_base.py
├── config.py
├── setup/
├── guide/
├── modules/
├── build/
├── finalize/
├── data/
└── ui/
```

其中：

```text
config      Face 静态配置和 Step 显示规则
setup       Step 01 输入和基础场景
guide       Step 02 Template / Query / Mirror / Repair / Validation
modules     Step 03 完整 Rig Module
build       可复用 Face Build Algorithm
finalize    Step 04 Final Check / Cleanup / Publish
data        跨 Step 的 Face 公共数据
ui          Face Wizard / Config Restore / Step Visibility / Build UI
```

当前正式 Step 03 Module：

```text
systems/face/modules/teeth.py
    TeethModule
```

完整说明见：[Face System Architecture](face-system.md)。

Face Config 恢复和 UI 状态见：[Face Workflow State](face-workflow-state.md)。

## Core Naming 边界

Rig Naming 已从 Core 移到：

```text
systems/rig_base.py
```

`core/rename_utils.py` 只处理 Maya Short Name 和 Rename 等通用节点操作。

旧 `core/name_utils.py` 已删除。

## Controller 边界

Controller 的唯一正式业务入口：

```text
systems/ctrl_base.py
```

旧 `systems/controller/` 已删除。

Tool 和 Module 都直接调用 `ctrl_base`，不再维护第二套 Controller Builder。

## 为什么不再使用万能 Utils，也不做无意义拆分

Core 继续采用“一个 Maya 领域一个模块”：

```text
scene_utils.py
transform_utils.py
matrix_utils.py
connection_utils.py
constraint_utils.py
curve_utils.py
surface_utils.py
skin_utils.py
...
```

System 层则按业务语义组织：

```text
RigBase
ModuleBase
CtrlBase
Face Module
Body Module
```

目标是：

```text
职责清楚
+
单一事实来源
+
调用路径短
+
容易测试
+
容易继续扩展
```
