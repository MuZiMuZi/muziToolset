# Muzi Toolset Architecture

## 技术路线

Muzi Toolset 正式采用 **PyMEL-first** 架构。

Maya 场景对象的创建、属性、连接、层级、Constraint、Selection 等操作优先直接使用 PyMEL：

```python
import pymel.core as pm

joint = pm.createNode(
    "joint",
    name="jnt_md_test_bind_001"
)

joint.radius.set(0.1)
parent = joint.getParent()
controller.translate >> joint.translate
```

`maya.cmds` 不是禁用项。当某个 Maya 命令用 cmds 表达更直接、PyMEL 包装行为不够清楚，或某些 UI / 特殊命令更适合 cmds 时，可以直接使用；但普通 Node / Attribute / Connection / Hierarchy 操作仍以 PyMEL 为默认选择。

底层几何 / 数学计算优先使用 `maya.api.OpenMaya`。项目不恢复旧的 `*_utils` Wrapper，也不为了隐藏 PyMEL / cmds 而重复包装 Maya 已经提供的基础能力。

## 正式分层

```text
muziToolset/
├─ core/
│  ├─ name.py
│  ├─ control.py
│  ├─ curve.py
│  └─ undo.py
├─ systems/
│  ├─ component_base.py
│  └─ face/
│     ├─ config.py
│     ├─ face_config.py
│     ├─ face_base.py
│     ├─ setup/
│     ├─ guide/
│     ├─ build/
│     ├─ finalize/
│     ├─ data/
│     └─ ui/
├─ tools/
├─ resources/
│  └─ face/
└─ legacy_reference/
```

`core` 只保存真正增加项目语义的通用能力；不包装 PyNode、Transform、Joint、Attribute、Parent、Connection 或 Selection。

`systems` 负责完整 Rig 业务，Component 直接保存 PyNode。生命周期统一为：

```text
collect_inputs()
prepare_data()
process_data()
finalize_step()
run_step()
```

标准 Rig Component 的 `process_data()` 继续拆成：

```text
create_joint()
create_controller()
create_connection()
```

## Face Rig

当前正式 Workflow：

```text
FaceSetup
    ↓
FaceGuide
    ↓
FaceBuild
    ↓
FaceFinalize
```

公共业务对象：`FaceConfig`、`FaceBase`。

当前已迁移的 Build 能力：TeethComponent、Curve Attachment、Eyelid / Eye Bag Radial Joints、Matrix Zip Lip。

Face Guide Template：`resources/face/face_guide.ma`。

## 依赖方向

```text
UI / Tools
    ↓
Systems
    ↓
Core
    ↓
PyMEL / cmds / Maya API 2.0
    ↓
Maya
```

PyMEL 是普通 Maya Scene 操作的默认入口；cmds 按需使用；`maya.api.OpenMaya` 负责适合低层 API 的几何和数学工作。禁止正式代码依赖 `legacy_reference` 和旧 `*_utils`，也禁止 Core 反向依赖 Systems / Tools。

## 命名规范

```text
folder / file          snake_case
function / method      snake_case
variable               snake_case
config variable        snake_case
class                  PascalCase
```

项目自定义模块变量即使逻辑上是常量，也使用 snake_case 小写。GitHub / Python / 社区约定文件名，例如 `README.md`、`LICENSE`、`__init__.py` 保持标准名称。

## 历史代码

本次架构不维护旧接口兼容。旧实现只作为参考保存在 `legacy_reference/`；完整 cmds 架构固定保存在分支 `cmds-archive-2026-08-31`。
