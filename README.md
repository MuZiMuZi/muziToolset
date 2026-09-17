# muziToolset

面向 **Autodesk Maya 2023** 的 Rigging Toolset、模块化绑定库与可扩展 Rig Framework。

当前 Python Package：

```python
import muziToolset
```

当前包版本：

```text
0.4.0
```

> 版本号仍为 0.4.0，但 2026-09 之后仓库结构已经继续演进。当前架构请以本 README、`docs/architecture/` 与自动 API Reference 为准，不再使用旧 `RigBase / ModuleBase / CtrlBase` 文档作为当前实现说明。

---

# 快速开始

把 `muziToolset` 放到 Maya Python 可以访问的位置后，在 Maya Python Script Editor 中运行：

```python
import muziToolset

window = muziToolset.show()
```

打开当前模块化绑定库：

```python
import muziToolset

window = muziToolset.show_rig_library()
```

第一次使用：

- [安装与启动](docs/getting-started/installation.md)
- [在 Maya 中运行](docs/getting-started/maya-usage.md)
- [MuziTools 用户手册](docs/manual/index.md)
- [绑定库](docs/manual/rig-library.md)

---

# 当前架构

当前正式 Runtime 代码按职责分成：

```text
app/
    Maya 应用入口、工具箱和窗口管理

ui/
    通用 PySide Theme、Window、Widget

core/
    Maya / Rig 底层可复用能力

systems/
    完整、可重复构建的 Rig Module / Workflow

tools/
    绑定师直接使用的小型 UI / Action Tool
```

辅助目录：

```text
resources/
    Controller Shape、Face Guide、图标等资源

scripts/
    文档生成、迁移、审计和维护脚本

tests/
    静态架构门禁、文档检查和 Runtime Contract

docs/
    MkDocs 网站源码
```

推荐依赖方向：

```text
app
 ↓
tools / systems
 ↓
core

ui 为 app / tools / systems 提供公共界面能力
```

详细说明见 [总体架构](docs/architecture/index.md)。

---

# 当前 Core

正式 Core 已收敛到：

```text
core/common/
├── attr_utils.py
├── hierarchy_utils.py
├── name_utils.py
└── transform_utils.py

core/rigging/
├── ctrl_utils.py
├── guide_utils.py
└── jnt_utils.py
```

其中：

```text
common
    Attribute / Hierarchy / Naming / Transform

rigging
    Controller / Guide / Joint 基础能力
```

历史实现仍保留在：

```text
core/bake/
legacy_reference/
```

这些目录不再定义新架构；新功能不应默认继续扩展到兼容区。

详见：

- [Core 设计](docs/architecture/core.md)
- [Core 使用手册](docs/manual/core.md)

---

# Rig Module

当前通用模块基类：

```text
systems/rig_module.py
```

统一生命周期：

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

为了支持绑定库分阶段修改，又拆成：

```text
build_outputs()
    Joint + Controller + Hierarchy

connect_outputs()
    Final Connection
```

这样 Guide 修改后可以只 Rebuild 输出，最后再重新建立正式连接。

---

# Rig Library

当前模块化绑定主入口：

```python
import muziToolset

window = muziToolset.show_rig_library()
```

四步 UI：

```text
01 Setup
02 Guide
03 Ctrl
04 Final
```

实际数据阶段：

```text
Setup
    ↓
Guide
    ↓
Build Joint + Controller
    ↓
Adjust Controller + Joint
    ↓
Final Connection
```

当前 `RigLibraryService` 正式调度模块：

```text
EarModule
EyeModule
TongueModule
FKChain
```

支持：

```text
Module Catalog
Template
Guide Import
Mirror
Build
Rebuild
Controller Appearance
Joint Display
Final Connect
Scene Config Persistence
Ownership Tag
Maya Undo Chunk
```

详见 [绑定库使用手册](docs/manual/rig-library.md)。

---

# Face Rig

当前正式 Face Runtime：

```text
systems/face/
├── face_guide_config.py
├── eye_module.py
├── ear_module.py
└── tongue_module.py
```

Face Guide 使用统一 Locator 命名：

```text
loc_<side>_<part>_<function>_<index>
```

Eye 使用固定语义：

```text
loc_<side>_eye_ball_001
loc_<side>_eye_iris_001
loc_<side>_eye_aim_001
```

Eye Rig 的正式驱动结构：

```text
Aim Ctrl Output
    ↓
Aim Constraint
    ↓
Main Driven
    ↓
Main Ctrl Output
    ↓
Pose Driver
    ↓
Pose Driven
    ↓
Orient Constraint
    ↓
Eye Joint
```

详见：

- [Face Guide](docs/manual/face-guide.md)
- [Face System Architecture](docs/architecture/face-system.md)
- [Face Workflow State](docs/architecture/face-workflow-state.md)

---

# Controller

当前正式 Controller 基础实现：

```text
core/rigging/ctrl_utils.py
```

标准 Hierarchy：

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

Controller Shape 数据来自：

```text
resources/controller_shapes/
```

支持：

```text
Shape
Color
Size
Axis
Shape Rotate
Shape Offset
SubCtrl
Hierarchy
Output
```

详见 [Controller 使用手册](docs/manual/controller.md)。

---

# Joint

当前正式 Joint 基础实现：

```text
core/rigging/jnt_utils.py
```

`RigModule.create_joint()` 负责单个 Joint 创建 / Guide Match；具体 Joint 数量和拓扑由 Module 的 `create_joints()` 决定。

Rig Library Step 03 允许调整：

```text
Joint Radius
Local Axis
Joint Visibility
```

详见 [Jnt 使用手册](docs/manual/jnt.md)。

---

# Tools 当前状态

`tools/` 仍包含大量绑定师直接使用的 UI：

```text
basic
blendshape
clean
controller
face
jnt
rig
skin
```

其中部分 Tool 仍引用旧的平铺 Core 名称，例如：

```text
core.scene_utils
core.skin_utils
core.constraint_utils
core.blendshape_utils
```

而这些入口当前已经不属于正式 Core 结构。

因此当前原则是：

```text
Tool 的 UI / Workflow 可以继续维护
    ↓
底层依赖逐步迁移到当前 Core
```

不要为了兼容旧 Tool，把已退休的 Core 平铺架构恢复回来。

详见 [常用工具工作流](docs/manual/tools.md)。

---

# API Reference

项目网站通过 Python AST 自动扫描：

```text
__init__.py
config.py
app/**/*.py
core/**/*.py
systems/**/*.py
tools/**/*.py
ui/**/*.py
```

每个正式 Runtime Python 文件都会生成独立 API 页面，并展开：

```text
Module Summary
Functions
Classes
Constructors
Methods
Signatures
Parameters
Returns
Raises
Examples
Notes
Source Path
```

源码 Docstring 是 API 文档第一事实来源。

入口：

- [API Reference](docs/reference/index.md)
- [文档维护](docs/development/documentation.md)

---

# 测试与文档门禁

GitHub Actions 当前会执行多类静态检查，包括：

```text
Core Import Style
Jnt Naming Contract
Rig Architecture Gate
Core Public API
System -> Core Reuse
Runtime Docstring Standard
Rigging Terminology Quality
API Generator Test
Runtime API Coverage
Generated Layout
README / Navigation Consistency
MkDocs Strict Build
```

文档站构建流程：

```text
源码
    ↓
Docstring Check
    ↓
AST API Generator
    ↓
Reference Layout Refine
    ↓
SUMMARY Navigation
    ↓
mkdocs build --strict
    ↓
GitHub Pages
```

---

# 文档导航

## 1. 用户手册

- [MuziTools 用户手册](docs/manual/index.md)
- [绑定库](docs/manual/rig-library.md)
- [常用工具工作流](docs/manual/tools.md)
- [Core 使用手册](docs/manual/core.md)
- [基础工具](docs/manual/basic-tools.md)
- [Controller](docs/manual/controller.md)
- [Jnt](docs/manual/jnt.md)
- [Skin](docs/manual/skin.md)
- [BlendShape](docs/manual/blendshape.md)
- [场景清理与模型检查](docs/manual/cleanup.md)
- [完整绑定工作流](docs/manual/rigging.md)
- [Face Guide](docs/manual/face-guide.md)

## 2. 架构

- [总体架构](docs/architecture/index.md)
- [Core 设计](docs/architecture/core.md)
- [Tools 与 Systems](docs/architecture/tools-systems.md)
- [Face System Architecture](docs/architecture/face-system.md)
- [Face Workflow State](docs/architecture/face-workflow-state.md)

## 3. API Reference

- [API Reference](docs/reference/index.md)

## 4. 开发指南

- [文档维护](docs/development/documentation.md)
- [Core 编码规范](docs/development/core-style-guide.md)
- [测试](docs/development/testing.md)
- [UI Design System](docs/development/ui-design.md)

## 5. 迁移记录

旧迁移页仅用于把历史链接导向当前架构，不再作为当前设计说明：

- [Pipeline / Core Migration（已退休）](docs/migration/pipeline.md)
- [Rig Architecture 0.4 Migration（已退休）](docs/migration/rig-architecture-0.4.md)

---

# 代码与文档规范

```text
模块 / 文件 / 函数 / 变量    snake_case
Class                       PascalCase
Side                        lf / rt / md
Maya Rig Node               [type]_[side]_[part]_[function]_[index]
```

项目代码继续优先：

- 清晰中文注释；
- 显式 `for` 循环；
- Tool / System 不重复 Core；
- 公开 API 写完整 Docstring；
- 文档与源码一起提交；
- 小步骤、小 Commit；
- Maya Runtime 逻辑最终必须回到 Maya 2023 验证。
