# MuziTools Architecture

`muziToolset` 根包是项目唯一正式运行框架。

当前架构版本：**0.4**。

## 目录职责

```text
muziToolset/
├─ app/                    # Maya 应用入口、主工具箱、窗口生命周期
├─ ui/                     # PySide Theme、通用 Widget、Window Helper
├─ core/                   # Maya / Python 通用底层能力
├─ tools/                  # 用户直接使用的小工具
├─ systems/                # RigBase / ModuleBase / CtrlBase / 完整 Rig System
├─ resources/              # Guide Template、Controller Shape 等静态资源
├─ tests/                  # Static Gate + Maya Smoke
├─ docs/                   # 用户手册、架构、开发指南、API Reference
├─ scripts/                # 文档生成与开发脚本
└─ legacy_reference/       # 历史资料，只用于参考
```

## 分层依赖

```text
app / ui / tools
        ↓
      systems
        ↓
       core
```

`core` 禁止反向 import `systems / tools / ui / app`。

---

# 0.4 核心基座

## RigBase

正式位置：

```text
systems/rig_base.py
```

`RigBase` 是所有 Rig Object / Module 共用的**可实例化基础类**，不是 Naming Utility，也不是单个 Maya Node 的 Name Object。

每个实例直接保存三个基础属性：

```text
side
part
index
```

例如：

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
```

具体 Maya Node 的 `node_type` 和 `function` 在创建名称时提供：

```python
joint_name = rig.create_name(
    node_type="jnt",
    function="bind"
)

# jnt_lf_brow_bind_001
```

标准 Rig Naming：

```text
[node_type]_[side]_[part]_[function]_[index]
```

方向统一为：

```text
lf / rt / md
```

字段规则：

```text
node_type   单一 Token
side        lf / rt / md
part        可以包含下划线
function    单一 Token
index       001 ~ 999
```

正式实例属性：

```text
side
part
index
```

正式实例方法：

```text
create_name()
mirror_name()
get_next_index()
create_unique_name()
get_opposite_side()
```

纯解析 / 校验能力可以直接通过类调用：

```python
fields = RigBase.parse_name(
    "jnt_lf_brow_bind_001"
)

valid = RigBase.validate_name(
    "jnt_lf_brow_bind_001"
)

side = RigBase.normalize_side(
    "left"
)
```

正式 Naming 参数统一使用：

```text
node_type=
```

旧 `type=` Keyword 已退休，不再提供兼容入口。

为了保持基础类简单，以下属性包装 API 已删除：

```text
identity
set_identity()
resolve_identity()
flip_side()
is_left()
is_right()
is_center()
```

同时继续保持退休：

```text
RigBase(name=...)
name
compose()
decompose()
flip()
```

读取状态直接使用：

```python
rig.side
rig.part
rig.index
```

判断 Side 直接使用：

```python
if rig.side == "lf":
    pass
```

需要修改属性时直接赋值；正式 Naming 时 `create_name()` 会再次执行字段校验和规范化。

`parse_name()` 只返回解析字段，不会反向修改 RigBase 实例。

Rig Naming 已从 Core 移出。旧 `core/name_utils.py` 已删除。

`core/rename_utils.py` 只负责 Maya Short Name、Rename 等通用节点改名行为。

## ModuleBase

正式位置：

```text
systems/module_base.py
```

完整业务单元统一使用 **Module** 术语，不再使用 Component。

普通 Module 生命周期：

```text
collect_inputs()
      ↓
prepare_data()
      ↓
process_data()
      ↓
finalize_step()
```

统一入口：

```python
run_step()
```

需要 Joint / Controller / Connection 的 Rig Module 使用 `RigModuleBase`：

```text
process_data()
      ├─ create_joint()
      ├─ create_controller()
      └─ create_connection()
```

继承关系：

```text
RigBase
   ↓
ModuleBase
   ↓
RigModuleBase
```

因此每个 Module 都天然拥有自己的 `side / part / index` 属性和 Naming 能力。

旧 `systems/component_base.py` 已删除。

## CtrlBase

正式位置：

```text
systems/ctrl_base.py
```

Controller Workflow 统一由 `CtrlBase` 提供，不再维护第二套 Controller Builder。

主要能力：

```text
create_ctrl()
create_fk_ctrl()
create_follow()
create_space_switch()
create_space_blend()
```

标准 Controller Hierarchy：

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

旧 `systems/controller/` 已删除。

---

# Core

`core` 只保存与具体 Rig 业务无关的 Maya / Python 基础能力。

主要模块：

```text
animation_utils.py
attr_utils.py
blendshape_utils.py
config_utils.py
connection_utils.py
constraint_utils.py
control_shape_utils.py
curve_utils.py
file_utils.py
hierarchy_utils.py
joint_utils.py
matrix_utils.py
mesh_utils.py
model_check_utils.py
rename_utils.py
scene_utils.py
scene_utils.py
skin_utils.py
surface_utils.py
transform_utils.py
```

Core 可以负责：

- Maya Node / DAG / DG；
- Attribute；
- Matrix / Constraint / Connection；
- Curve / Surface / Mesh；
- Joint；
- Skin / BlendShape；
- Scene / File / Animation；
- Model Check / Scene Clean。

Core 不负责：

- Teeth / Jaw / Face / Body 等业务语义；
- 完整 Rig Workflow；
- Rig Object 基础属性 / Rig Naming Convention；
- PySide UI；
- PyMel。

---

# Systems

`systems` 负责 Rig Object 基础属性、完整 Rig Workflow、Module 和可复用 Builder。

当前基础结构：

```text
systems/
├── rig_base.py
├── module_base.py
├── ctrl_base.py
├── face/
├── body/
└── rig/
```

## Step / Module / Builder / Core

```text
Step
    用户工作流阶段，例如 Setup / Guide / Build / Finalize

Module
    完整业务绑定单元，例如 Teeth / Jaw / Tongue / Lip / Eye / Brow

Builder
    可被多个 Module 组合的构建算法，例如 Curve Attachment / Zip Lip

Core
    与具体 Rig 业务无关的 Maya 基础能力
```

正式代码不再使用 Component 表示完整 Rig 业务单元。

---

# Face System

Face Rig Workflow：

```text
01 Setup
    ↓
02 Guide
    ↓
03 Build
    ↓
04 Finalize
```

正式目录：

```text
systems/face/
├── __init__.py
├── config.py
├── face_base.py
├── setup/
│   └── face_setup.py
├── guide/
│   └── face_guide.py
├── modules/
│   └── teeth.py
├── build/
│   ├── curve_attachment.py
│   ├── eyelid/
│   └── lip/
├── finalize/
├── data/
└── ui/
    ├── face_rig_ui.py
    ├── workflow_controller.py
    └── build_controller.py
```

`systems/face/modules/` 保存完整业务 Module。

当前正式 Module：

```text
TeethModule
```

后续继续扩展：

```text
JawModule
TongueModule
LipModule
EyeModule
EyelidModule
BrowModule
NoseModule
CheekModule
```

`systems/face/build/` 只保存可复用构建算法，不保存完整业务 Module。

Face 继承关系：

```text
RigBase
   ↓
ModuleBase
   ↓
RigModuleBase
   ↓
FaceBase
   ↓
FaceSetup / FaceGuide / TeethModule / ...
```

`FaceBase` 默认实例属性：

```text
side = md
part = face
index = 1
```

具体业务 Module 应设置自己的实例属性，例如：

```text
TeethModule
    side = md
    part = teeth
    index = 1
```

`FaceSetup`、`FaceGuide` 属于特殊 Workflow Module，因此可以覆盖 `process_data()`。

真正的 Rig Module 使用标准三段构建：

```text
create_joint()
create_controller()
create_connection()
```

---

# Face Config 与 Workflow

`systems/face/config.py` 负责：

- Face Hierarchy Name；
- Controller Config Attribute；
- Controller 默认 Size / Color；
- Guide Template 信息；
- Step Visibility Rule；
- Step Model Display Rule。

`network_md_face_config_001` 是 Face UI 可恢复参数的持久化来源。

UI 正式入口：

```text
systems.face.show()
    ↓
systems.face.ui.show()
    ↓
ui/build_controller.py
    ↓
ui/workflow_controller.py
    ↓
ui/face_rig_ui.py
```

---

# Tools

`tools` 负责：

- 读取 Selection / Channel Box；
- 收集用户参数；
- 显示状态和 Warning；
- 调用 Core / Systems；
- 提供统一 `main()`。

Tool 不复制 Core / System 算法。

需要 Rig Naming 的 Tool 应先创建一个明确的 `RigBase` 实例，再通过 `rig.side / rig.part / rig.index` 和 Naming 方法完成工作。

Controller Tool 必须调用 `systems.ctrl_base`，不允许重新建立 Controller Builder。

---

# UI / App

`ui` 保存通用 Theme、Widget 和独立窗口生命周期。

`app` 保存主工具箱、Tool Discovery 和应用级 Window Manager。

---

# 测试门槛

静态架构测试：

```text
core_import_style_test.py
rig_architecture_gate_test.py
rig_base_contract_test.py
module_base_contract_test.py
```

Maya 2023 Runtime Smoke：

```text
maya_smoke_test.py
pipeline_refactor_smoke_test.py
extended_core_smoke_test.py
ctrl_base_smoke_test.py
face_build_smoke_test.py
rig_integration_test.py
maya2023_smoke_test.py
```

`rig_architecture_gate_test.py` 明确禁止以下架构回退：

```text
core/name_utils.py
systems/component_base.py
systems/controller/
TeethComponent
RigBase.create_name(...)
RigBase(name=...)
create_name(type=...)
identity / set_identity / resolve_identity
flip_side / is_left / is_right / is_center
```

静态测试负责阻止架构回退；Maya Smoke 负责验证真实 Maya 行为。

---

# Legacy

`legacy_reference/` 只用于历史算法参考，不属于正式 Runtime。

正式代码禁止直接 Import Legacy。
