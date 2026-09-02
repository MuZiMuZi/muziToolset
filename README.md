# muziToolset

面向 **Autodesk Maya 2023** 的 Rigging Toolset 与可扩展绑定框架。

当前架构版本：**0.4.0**。

正式 Python Package：

```python
import muziToolset
```

项目显示名称使用 **MuziTools**；源码根包始终使用 `muziToolset`。

---

# 快速开始

把 `muziToolset` 放到 Maya Python 可以访问的位置后，在 Maya Python Script Editor 中运行：

```python
import muziToolset
window = muziToolset.show()
```

---

# 当前架构

```text
core     Maya 通用底层能力
tools    用户直接操作的小工具 / UI
systems  RigBase / ModuleBase / CtrlBase / 完整 Rig System
ui       通用 PySide Theme / Widget
app      主程序和窗口生命周期
```

0.4 三个基础入口：

```text
systems/rig_base.py
    Rig Naming

systems/module_base.py
    Module Lifecycle

systems/ctrl_base.py
    Controller Workflow
```

正式业务单元统一使用 **Module** 术语，不再使用 Component。

Rig Naming 已从 Core 移到 `RigBase`；旧 `core/name_utils.py` 已删除。

Controller 的唯一正式实现是 `systems/ctrl_base.py`；旧 `systems/controller/` 已删除。

---

# Face Rig

当前工作流：

```text
01 Setup
    ↓
02 Guide
    ↓
03 Build
    ↓
04 Finalize
```

正式结构：

```text
systems/face/
├── setup/       # Step 01
├── guide/       # Step 02
├── modules/     # Step 03 完整 Rig Module
├── build/       # 可复用 Build Algorithm
├── finalize/    # Step 04
├── data/
├── ui/
├── face_base.py
└── config.py
```

当前已经接入的 Step 03 Module：

```text
TeethModule
```

Teeth Rig：

```text
Teeth Guide
    ↓
Controller
    ↓ Matrix
Bind Joint
    ↓ Rigid Skin
Teeth Model
```

Gum 不属于 Teeth 刚体绑定，后续由 Jaw / Mouth Deformation 处理。

Step 02 Controller Settings 当前包括：

```text
Global Scale
LF / RT / MD Color
Brow
Eye
Eyelid
Nose
Cheek
Lip
Jaw
Teeth
Tongue Size
```

---

# Rig Naming

正式 Maya Rig 节点格式：

```text
[type]_[side]_[part]_[function]_[index]
```

方向：

```text
lf / rt / md
```

正式入口：

```python
from muziToolset.systems.rig_base import RigBase
```

Maya 普通 Rename / Short Name 继续使用：

```python
from muziToolset.core import rename_utils
```

两者职责不混合。

---

# Controller

正式 Controller System：

```python
from muziToolset.systems import ctrl_base
```

标准层级：

```text
zero
  ↓
driven
  ↓
space
  ↓
connect
  ↓
offset
  ↓
ctrl
  ↓
output
```

Control Creator、FK Creator、Face Module、Body Skirt 都应直接调用 `ctrl_base`。

---

# UI Design System

项目正式 UI 统一使用：

```text
ui/theme.py
ui/widgets/
```

窗口生命周期：

```text
ui.window_utils
    独立 Tool

app.window_manager
    主工具箱打开的 Tool
```

---

# 测试

静态架构门禁：

```text
core_import_style_test.py
rig_architecture_gate_test.py
rig_base_contract_test.py
module_base_contract_test.py
```

Maya Runtime：

```python
import muziToolset

muziToolset.smoke_test()
muziToolset.pipeline_smoke_test()
muziToolset.extended_core_smoke_test()
muziToolset.ctrl_base_smoke_test()
muziToolset.face_build_smoke_test()
muziToolset.rig_integration_test()
muziToolset.maya2023_smoke_test()
muziToolset.functional_smoke_test()
```

其中 `rig_architecture_gate_test.py` 会阻止以下退休架构重新进入正式代码：

```text
core/name_utils.py
systems/component_base.py
systems/controller/
TeethComponent
```

---

# 文档

- [总体架构](docs/architecture/index.md)
- [Face System Architecture](docs/architecture/face-system.md)
- [Face Workflow State](docs/architecture/face-workflow-state.md)
- [Core 设计](docs/architecture/core.md)
- [Tools 与 Systems](docs/architecture/tools-systems.md)
- [测试](docs/development/testing.md)

API Reference 由源码 Docstring 通过 AST Generator 生成。

---

# 代码规范

```text
模块 / 文件 / 函数 / 变量    snake_case
Class                       PascalCase
Side                        lf / rt / md
Maya Rig Node               [type]_[side]_[part]_[function]_[index]
```

流程代码优先显式 `for` 循环和清晰中文注释；Maya 场景代码优先 `maya.cmds`，正式新代码不新增 PyMel。
