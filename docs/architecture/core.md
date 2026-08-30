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
Attribute       -> attr_utils.py
Hierarchy       -> hierarchy_utils.py
Joint           -> joint_utils.py
Naming          -> name_utils.py
Batch Rename    -> rename_utils.py
Curve           -> curve_utils.py
Surface         -> surface_utils.py
Mesh            -> mesh_utils.py
Skin            -> skin_utils.py
BlendShape      -> blendshape_utils.py
ControllerShape -> control_shape_utils.py
Model Check     -> model_check_utils.py
Scene Clean     -> scene_clean_utils.py
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

原 `animation_io_utils.py` 已合并进来并删除旧文件。

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

原 `scene_io_utils.py` 已合并进来并删除旧文件。

### `file_utils.py`

只负责纯 Python 文件系统：

```text
Path
Directory
JSON
Find Files
File Name / Stem
```

判断方式：

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

## `attr_utils.py`

正式 Import：

```python
from muziToolset.core import attr_utils
```

负责：

```text
Attribute Create
Lock / Hide
Value
Message Config
String Config
Transform Limits
```

旧的 Connection API 继续作为兼容方法存在于 `Attr` 类中，但底层已经统一调用 `connection_utils`。
旧 `reset_attr()` 也已经转调 `animation_utils`，避免第二套 Reset 实现。

## `hierarchy_utils.py`

正式 Import：

```python
from muziToolset.core import hierarchy_utils
```

负责：

```text
Parent
Extra Group
Child Query
Group Creation
```

旧版 `create_default_grp()` 曾依赖已经退出正式 Core 的 `controlUtils`，当前已经修正为只创建 Group。
完整 Controller 构建属于上层 Controller System。

## `joint_utils.py`

正式 Import：

```python
from muziToolset.core import joint_utils
```

分成：

```text
Joint
JointCurve
JointChain
```

其中 `JointCurve` 不再自己维护 Curve Query，而是统一复用 `curve_utils`；
`JointChain` 的正式命名依赖统一使用 `name_utils`。

## `name_utils.py`

正式 Import：

```python
from muziToolset.core import name_utils
```

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

正式 Import：

```python
from muziToolset.core import rename_utils
```

负责批量 Rename Tool 行为：

```text
Prefix
Suffix
Search Replace
Auto Number
Pattern Rename
```

所以 `name_utils` 与 `rename_utils` 不合并：

```text
name_utils
    -> 一个 Rig 名称应该是什么

rename_utils
    -> 对一批 Maya 节点执行什么 Rename 操作
```

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

# snake_case 迁移已经完成

以下早期 CamelCase Core 文件已经完成迁移并删除：

```text
attrUtils.py        -> attr_utils.py
hierarchyUtils.py   -> hierarchy_utils.py
jointUtils.py       -> joint_utils.py
nameUtils.py        -> name_utils.py
```

迁移过程已经走完：

```text
建立正式 snake_case 实现
    ↓
旧文件兼容转发
    ↓
Tools / Systems / Tests 切换正式 Import
    ↓
Maya 2023 Extended Core Smoke
    ↓
GitHub CI Import Gate 归零
    ↓
删除旧兼容文件
```

GitHub Actions 现在会执行：

```bash
python tests/core_import_style_test.py
```

该测试使用 AST 静态扫描正式 Python 源码，不需要 Maya。
如果以后有人重新写入旧 CamelCase Core Import，CI 会直接失败。

---

# 当前验证状态

## Extended Core Smoke

Maya 2023 已验证：

```text
attr_utils          PASS
hierarchy_utils     PASS
joint_utils         PASS
naming              PASS
model_check_utils   PASS
scene_clean_utils   PASS

Total: 6 | Passed: 6 | Failed: 0
```

## Tool Window Smoke

Maya 2023 已验证：

```text
Total: 17 | Passed: 17 | Failed: 0
```

## 文档 / 静态架构 CI

GitHub Actions 的文档构建链：

```text
Core Import Style Gate
        ↓
AST API Reference Generation
        ↓
mkdocs build --strict
        ↓
GitHub Pages
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
