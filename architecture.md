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

正式运行代码不使用 `maya.cmds`，也不恢复旧的 `*_utils` Wrapper。只有 PyMEL 不适合承担的底层几何 / 数学计算，才使用 `maya.api.OpenMaya`。

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
PyMEL
    ↓
Maya
```

允许 `Core -> maya.api.OpenMaya` 处理低层几何算法。禁止正式代码依赖 `legacy_reference`、`maya.cmds`、旧 `*_utils`，也禁止 Core 反向依赖 Systems / Tools。

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
