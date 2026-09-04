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

第一次使用：

- [安装与启动](docs/getting-started/installation.md)
- [在 Maya 中运行](docs/getting-started/maya-usage.md)

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
    Rig Object Attributes + Rig Naming

systems/module_base.py
    Module Lifecycle

systems/ctrl_base.py
    Controller Workflow
```

正式业务单元统一使用 **Module** 术语，不再使用 Component。

Rig Object 基础属性和 Rig Naming 由 `RigBase` 提供；旧 `core/name_utils.py` 已删除。

Controller 的唯一正式实现是 `systems/ctrl_base.py`；旧 `systems/controller/` 已删除。

---

# Face Rig

当前工作流：

```text
01 Setup
    ↓
02 Guide
    ↓
03 Build Modules
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
Bind Jnt
    ↓ Rigid Skin
Teeth Model
```

Gum 不属于 Teeth 刚体绑定，后续由 Jaw / Mouth Deformation 处理。

---

# RigBase / Rig Naming

`RigBase` 是可实例化的 Rig Object 基类。

每个实例直接保存：

```text
side
part
index
```

正式 Maya Rig 节点格式：

```text
[node_type]_[side]_[part]_[function]_[index]
```

方向：

```text
lf / rt / md
```

正式用法：

```python
from muziToolset.systems.rig_base import RigBase

rig = RigBase(
    side="lf",
    part="brow",
    index=1
)

print(rig.side)
print(rig.part)
print(rig.index)

jnt_name = rig.create_name(
    node_type="jnt",
    function="bind"
)

# jnt_lf_brow_bind_001
```

简单状态不再通过额外包装方法读取；直接使用：

```python
if rig.side == "lf":
    pass
```

`node_type` 和 `function` 描述具体 Maya 节点，不属于 Rig Object 实例属性。

纯解析 / 校验可以直接调用：

```python
fields = RigBase.parse_name(
    "jnt_lf_brow_bind_001"
)

valid = RigBase.validate_name(
    "jnt_lf_brow_bind_001"
)
```

RigBase Naming 正式参数使用 `node_type=`；旧 `type=` 已退休。

Maya 普通 Rename / Short Name：

```python
from muziToolset.core import rename_utils
```

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

---

# 文档导航

## 1. 用户手册

- [MuziTools 用户手册](docs/manual/index.md)
- [常用工具工作流](docs/manual/tools.md)
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
- [Procedural Rig 架构参考](docs/architecture/xiong-lin-procedure-auto-rig.md)

## 3. API Reference

- [API Reference](docs/reference/index.md)

API 页面由源码 Docstring 通过 AST Generator 自动生成。

## 4. 开发指南

- [文档维护](docs/development/documentation.md)
- [Core 编码规范](docs/development/core-style-guide.md)
- [测试](docs/development/testing.md)
- [UI Design System](docs/development/ui-design.md)

## 5. 迁移记录

- [Pipeline / Core Migration](docs/migration/pipeline.md)
- [Rig Architecture 0.4 Migration](docs/migration/rig-architecture-0.4.md)

---

# 代码规范

```text
模块 / 文件 / 函数 / 变量    snake_case
Class                       PascalCase
Side                        lf / rt / md
Maya Rig Node               [node_type]_[side]_[part]_[function]_[index]
```

流程代码优先显式 `for` 循环和清晰中文注释；Maya 场景代码优先 `maya.cmds`，正式新代码不新增 PyMel。
