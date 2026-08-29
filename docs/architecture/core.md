# Core 设计

`core/` 是 MuziTools 最底层的 Maya / Python 能力层。

## 一句话原则

> 一个清晰的 Maya 领域，一个 Core 模块。

目标既不是：

```text
一个函数 = 一个文件
```

也不是重新制造：

```text
pipelineUtils.py = 所有功能
```

当前颗粒度更接近：

```text
Animation       -> animation_utils.py
Scene           -> scene_utils.py
File            -> file_utils.py
Transform       -> transform_utils.py
Matrix          -> matrix_utils.py
Connection      -> connection_utils.py
Constraint      -> constraint_utils.py
Curve           -> curve_utils.py
Surface         -> surface_utils.py
Skin            -> skin_utils.py
BlendShape      -> blendshape_utils.py
ControllerShape -> control_shape_utils.py
```

---

## Core 应该做什么

Core 负责可以被多个 Tool / System 复用的底层能力，例如：

- 创建 / 查询 Maya 节点；
- Attribute / Message；
- DAG Parent；
- Matrix / Constraint / Connection；
- Curve / Surface / Mesh；
- Joint；
- Skin / BlendShape；
- Scene / File / Animation 数据；
- 模型检查和安全 Scene Cleanup。

典型调用关系：

```text
Tool / System
     ↓
明确参数
     ↓
Core API
     ↓
Maya Scene / DG / DAG
     ↓
返回 Node / List / Dict / Count
```

---

## Core 不应该做什么

Core 不应该：

- 创建 PySide 窗口；
- 决定按钮怎么布局；
- 硬编码某一个角色的完整绑定流程；
- 构建完整 Arm / Leg / Face / Ribbon Workflow；
- import `tools / systems / ui / app / legacy_reference`；
- 新增 PyMel 依赖。

例如：

```text
create_point_on_curve_attachment()
    -> Core，可以复用

build_eyelid_joints()
    -> Face System，因为它是完整绑定工作流
```

---

# 当前 Core 模块地图

## Animation / Scene / File

### `animation_utils.py`

负责：

```text
AnimCurve Query
Clear Animation
Transform Reset
Collect Animation Data
Animation JSON Export / Import
```

原 `animation_io_utils.py` 已合并进来。

### `scene_utils.py`

负责：

```text
Undo Chunk
Node
Selection
Object Set
Native Callback
Scene Path / Modified State
Open / Import / Reference
FBX Export
```

原 `scene_io_utils.py` 已合并进来。

### `file_utils.py`

只负责纯 Python 文件系统：

```text
Path
Directory
JSON
Find Files
File Name / Stem
```

判断方式很简单：

```text
涉及 Maya Scene -> scene_utils
只是硬盘文件     -> file_utils
```

---

# Transform / DG

## `transform_utils.py`

静态 Transform 数据：

```text
World Translation
World Matrix
Distance
Relative Move
```

## `matrix_utils.py`

动态 Matrix 网络：

```text
MMatrix
Offset Matrix
multMatrix
offsetParentMatrix
Matrix Parent Constraint
```

## `connection_utils.py`

通用 DG Plug：

```text
Input / Output Connection
Connect
Disconnect
Copy Input Connection
Batch Connection
```

## `constraint_utils.py`

Maya 原生：

```text
parentConstraint
pointConstraint
orientConstraint
scaleConstraint
aimConstraint
```

Matrix 和 Constraint 不合并，因为它们是两套不同的 Rig 驱动体系。

---

# DAG / Attribute / Naming

## `attrUtils.py`

负责：

```text
Attribute Create
Lock / Hide
Value
Message Config
String Config
Transform Limits
```

旧的 Connection API 继续保留，但内部已经统一调用 `connection_utils`。
旧 `reset_attr()` 也已经转调 `animation_utils`。

## `hierarchyUtils.py`

负责：

```text
Parent
Extra Group
Child Query
Group Creation
```

旧版 `create_default_grp()` 曾依赖已经退出正式 Core 的 `controlUtils`，当前已经修正为只创建 Group。
完整 Controller 构建属于 `systems.controller`。

## `jointUtils.py`

分成：

```text
Joint
JointCurve
JointChain
```

其中 `JointCurve` 不再自己维护 Curve Query，而是统一复用 `curve_utils`。

## `nameUtils.py`

负责标准命名语义：

```text
[type]_[side]_[part]_[function]_[index]
```

例如：

```text
jnt_lf_upper_lid_bind_001
ctrl_md_face_main_001
model_md_head_tweak_001
```

## `rename_utils.py`

负责批量 Rename Tool 行为：

```text
Prefix
Suffix
Search Replace
Auto Number
Pattern Rename
```

所以 `nameUtils` 与 `rename_utils` 不合并。

---

# Geometry / Deformer

## `curve_utils.py`

负责：

```text
Curve Shape / CV
MFnNurbsCurve
Arc Length Sample
Closest Parameter
Parameter <-> Length Percentage
pointOnCurve Attachment
Curve Creation
```

## `surface_utils.py`

负责：

```text
NURBS Surface
Loft
Follicle
Even Follicles
```

## `mesh_utils.py`

当前保持轻量：

```text
Node Validate
Independent Model Duplicate
```

Skin / BlendShape / Model Check 不继续堆到 Mesh Utils。

## `skin_utils.py`

负责 SkinCluster、Influence、Copy Weight、XML / JSON Weight IO。

## `blendshape_utils.py`

负责 BlendShape Target、Alias、Duplicate Targets、Invert Shape。

## `control_shape_utils.py`

负责 Controller Curve Shape 的 JSON、CV、Color、Radius、Translate / Scale / Rotate / Mirror。

---

# Scene Quality

## `model_check_utils.py`

默认是“检查器”：

```text
Non-Manifold
Lamina
Duplicate DAG Name
Construction History
Transform
Locked Normal
```

只有明确 `fixable=True` 的 Issue 才允许自动修复。

## `scene_clean_utils.py`

明确是“修改器”：

```text
Delete Empty Group
Delete History
Freeze
Unlock Attributes
Center Pivot
Delete Unknown
```

它会保护：

```text
Reference
Default Camera
Animation
Constraint
Rig Deformer
```

检查和清理必须保持两个模块，防止“检查一下”意外修改 Scene。

---

# 中文注释标准

每个正式 Core 模块头至少包含：

```text
模块职责
公开方法 / 类
每个 API 的功能介绍
典型使用场景
设计原则
本模块不负责什么
```

关键 Maya 操作按步骤解释：

```python
# -------------------------------------------------------------------------
# 步骤 1：整理输入节点。
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# 步骤 2：创建 Maya 节点。
#
# 为什么：
# pointOnCurveInfo.position 是 World Space，
# 不能直接连接到有 Parent 的 Child Local Translate。
# -------------------------------------------------------------------------
```

注释重点回答：

1. 这一阶段做什么；
2. 为什么不能用更简单的写法；
3. Maya 在这里有什么特殊行为；
4. 哪一步会修改 Scene；
5. 返回数据接下来给谁使用。

---

# CamelCase 文件兼容

以下早期正式文件名暂时保留：

```text
attrUtils.py
hierarchyUtils.py
jointUtils.py
nameUtils.py
```

原因不是推荐 CamelCase，而是现有正式代码可能已经依赖这些 Import。

如果未来统一 snake_case，正确迁移流程是：

```text
新 snake_case API
    ↓
旧模块兼容转发
    ↓
全仓库 Import 迁移
    ↓
Maya Smoke Test
    ↓
最后删除旧入口
```

---

# Core 与 Systems 的边界

一个简单判断：

```text
“这个能力能被 3 个不同 Rig 系统直接复用吗？”
    ↓ Yes
Core 候选

“这个函数是否已经知道它在做 Eyelid / Lip / Arm / Ribbon？”
    ↓ Yes
Systems
```

例如：

```text
curve_utils.get_closest_parameter()
    -> Core

systems.face.eyelid.build_eyelid_joints()
    -> System
```

这条边界可以避免未来再长出第二个 `pipelineUtils.py`。
