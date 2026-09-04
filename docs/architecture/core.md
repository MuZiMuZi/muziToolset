# Core 设计

`core/` 是 MuziTools 最底层的 Maya / Python 通用能力层。

## 一句话原则

> 一个清晰的 Maya 领域，一个 Core 模块。

当前主要领域：

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
Jnt           -> jnt_utils.py
Maya Rename     -> rename_utils.py
Curve           -> curve_utils.py
Surface         -> surface_utils.py
Mesh            -> mesh_utils.py
Skin            -> skin_utils.py
BlendShape      -> blendshape_utils.py
ControllerShape -> control_shape_utils.py
Model Check     -> model_check_utils.py
Scene Clean     -> scene_utils.py
```

---

# Core 应该做什么

Core 负责可以被多个 Tool / System 复用的底层能力，例如：

- 创建 / 查询 Maya 节点；
- Attribute / Message；
- DAG Parent；
- Matrix / Constraint / Connection；
- Curve / Surface / Mesh；
- Jnt；
- Skin / BlendShape；
- Scene / File / Animation；
- 模型检查和安全 Scene Cleanup。

典型调用：

```text
Tool / System
     ↓
明确参数
     ↓
Core API
     ↓
Maya Scene / DG / DAG
```

---

# Core 不应该做什么

Core 不应该：

- 创建 PySide 窗口；
- 决定具体 Rig Workflow；
- 硬编码 Face / Teeth / Jaw / Body 等业务；
- 负责 Rig Object Identity / Rig Naming Convention；
- import `tools / systems / ui / app / legacy_reference`；
- 新增 PyMel。

例如：

```text
create_parent_matrix_constraint()
    -> Core

create_ctrl()
    -> CtrlBase

TeethModule
    -> Face System Module
```

---

# DAG / Attribute / Rename

## `attr_utils.py`

负责：

```text
Attribute Create
Lock / Hide
Value
Message Config
String Config
Transform Limits
```

## `hierarchy_utils.py`

负责：

```text
Parent
Child Query
Extra Group
Group Creation
DAG Depth
```

完整 Controller Hierarchy 不属于这里，统一交给 `systems.ctrl_base`。

## `jnt_utils.py`

负责 Jnt 的通用 Maya 能力：

```text
Jnt Create
Create At Object
Jnt Chain
Jnt Label
Jnt Curve 辅助
```

Jnt 的正式 Rig 名称由上层 `RigBase` 实例或 Module 生成后传入。

## `rename_utils.py`

正式 Import：

```python
from muziToolset.core import rename_utils
```

负责 Maya 节点通用 Rename 行为，例如：

```text
get_short_name()
rename_node()
Prefix / Suffix
Search Replace
Auto Number
Pattern Rename
```

它不定义 Rig Object Identity，也不定义 Rig 名称应该是什么。

---

# Rig Identity / Naming 不属于 Core

正式入口：

```text
systems/rig_base.py
```

`RigBase` 是可实例化 Rig Object 基类，Identity 为：

```text
side / part / index
```

正式用法：

```python
from muziToolset.systems.rig_base import RigBase

rig = RigBase(
    side="lf",
    part="upper_arm",
    index=1
)

name = rig.create_name(
    node_type="jnt",
    function="bind"
)
```

解析已有名称可以使用：

```python
fields = RigBase.parse_name(
    "jnt_lf_upper_arm_bind_001"
)
```

旧 `type=` RigBase Naming Keyword 已退休，统一使用 `node_type=`。

旧文件：

```text
core/name_utils.py
```

已经删除。

职责边界：

```text
RigBase
    描述一个 Rig Object 的 side / part / index
    基于 Identity 创建正式 Rig Node 名称

rename_utils
    对 Maya 节点执行 Rename / Short Name 等通用操作
```

---

# Matrix / Connection / Constraint

## `matrix_utils.py`

负责：

```text
Offset Matrix
multMatrix
offsetParentMatrix
Matrix Parent Constraint
```

## `connection_utils.py`

负责：

```text
Input / Output Plug Query
Connect
Disconnect
Copy Input Connection
Batch Connection
```

## `constraint_utils.py`

负责 Maya 原生 Constraint：

```text
parentConstraint
pointConstraint
orientConstraint
scaleConstraint
aimConstraint
```

Matrix 与 Constraint 保持为两个领域，不合并。

---

# Curve / Surface / Mesh

这些模块只提供可组合的 Maya 几何基础能力。

例如：

```text
curve_utils.create_point_on_curve_attachment()
    -> Core

face.build.attach_jnts_to_curves()
    -> Face Build Algorithm
```

如果方法已经带有明确的 Face / Brow / Lip / Eyelid 业务语义，就不应继续放 Core。

---

# Core 编码规则

正式 Runtime 遵守：

1. 接收明确参数；
2. 先验证输入；
3. 中文注释解释 Maya 特有原因；
4. 返回 Node / List / Dict / Count；
5. Core 不弹 UI；
6. 大型场景操作使用 Maya Undo Chunk；
7. 优先显式 `for` 循环；
8. 不新增 PyMel；
9. Module / Function / Variable 使用 `snake_case`；
10. 已存在能力禁止在 Tool / System 再复制一套。
