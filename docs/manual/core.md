# Core 使用手册

`core/` 是 MuziTools 中可被多个 Tool / System 复用的 Maya 基础能力层。

当前推荐入口已经收敛到：

```text
core/common/
core/rigging/
```

`core/bake/` 仍然保留在仓库中，但它主要承担历史代码和兼容用途；新功能不应该默认继续往 `bake` 中增加。

---

# 快速选择

| 我想做什么 | 当前推荐模块 |
| --- | --- |
| 创建 / 修改 Attribute | [`core/common/attr_utils.py`](../reference/core/common/attr_utils.md) |
| Lock / Hide Attribute | [`core/common/attr_utils.py`](../reference/core/common/attr_utils.md) |
| Message / Attribute Connection | [`core/common/attr_utils.py`](../reference/core/common/attr_utils.md) |
| Parent / Group / DAG 层级 | [`core/common/hierarchy_utils.py`](../reference/core/common/hierarchy_utils.md) |
| 组合标准 Rig 名称 | [`core/common/name_utils.py`](../reference/core/common/name_utils.md) |
| 解析标准 Rig 名称 | [`core/common/name_utils.py`](../reference/core/common/name_utils.md) |
| 左右命名翻转 | [`core/common/name_utils.py`](../reference/core/common/name_utils.md) |
| Transform 匹配 / 对齐 | [`core/common/transform_utils.py`](../reference/core/common/transform_utils.md) |
| 创建 / 设置 Controller | [`core/rigging/ctrl_utils.py`](../reference/core/rigging/ctrl_utils.md) |
| Controller Shape / Color / Size / Axis | [`core/rigging/ctrl_utils.py`](../reference/core/rigging/ctrl_utils.md) |
| 创建标准 Controller Hierarchy | [`core/rigging/ctrl_utils.py`](../reference/core/rigging/ctrl_utils.md) |
| Guide 基础能力 | [`core/rigging/guide_utils.py`](../reference/core/rigging/guide_utils.md) |
| Joint 基础创建 / 匹配 | [`core/rigging/jnt_utils.py`](../reference/core/rigging/jnt_utils.md) |
| 完整 Rig Module 构建 | [`systems/rig_module.py`](../reference/systems/rig_module.md) |

---

# 正确 Import

## Common

```python
from muziToolset.core.common import attr_utils
from muziToolset.core.common import hierarchy_utils
from muziToolset.core.common import name_utils
from muziToolset.core.common import transform_utils
```

## Rigging

```python
from muziToolset.core.rigging import ctrl_utils
from muziToolset.core.rigging import guide_utils
from muziToolset.core.rigging import jnt_utils
```

不要再使用旧文档中的：

```python
from muziToolset.core import attr_utils
from muziToolset.core import hierarchy_utils
from muziToolset.core import jnt_utils
```

当前源码结构已经明确分为 `common` 与 `rigging` 两层。

---

# 1. Naming

当前标准命名工具：

```python
from muziToolset.core.common import name_utils

name_object = name_utils.Name(
    type="ctrl",
    side="lf",
    part="eye",
    function="main",
    index=1
)

print(name_object.name)
```

输出：

```text
ctrl_lf_eye_main_001
```

标准格式：

```text
[type]_[side]_[part]_[function]_[index]
```

例如：

```text
ctrl_lf_eye_main_001
ctrl_rt_eye_aim_001
jnt_lf_eye_bind_001
grp_md_face_master_001
loc_lf_upper_lid_bind_001
```

`part` 可以包含下划线，例如：

```text
upper_lid
nose_center
mouth_corner
```

## 解析名称

```python
name_object = name_utils.Name(
    name="loc_lf_upper_lid_bind_001"
)

print(name_object.type)
print(name_object.side)
print(name_object.part)
print(name_object.function)
print(name_object.index)
```

## 左右翻转

```python
name_object.flip()
```

用于镜像命名时非常方便。

---

# 2. Attribute

当前入口：

```python
from muziToolset.core.common import attr_utils
```

适合处理：

```text
创建 Attribute
读取 / 设置值
Lock / Unlock
Hide / Show
Message Attribute
基础 Attribute Connection
```

这里处理的是通用 Attribute 行为。

例如“Eye Main Controller 需要哪些自定义 Attribute”不应该由 `attr_utils` 决定，而应该由 Eye Module 或对应 Tool 决定。

---

# 3. Hierarchy

当前入口：

```python
from muziToolset.core.common import hierarchy_utils
```

适合处理：

```text
Parent
创建 Group
添加 Extra Group
查询层级
整理 DAG
```

如果你只是想把一个节点挂到另一个节点下面，优先使用这里的通用能力。

如果你要创建完整 Controller 层级，则应该使用 `ctrl_utils.Ctrl`。

---

# 4. Transform

当前入口：

```python
from muziToolset.core.common import transform_utils
```

适合处理：

```text
Match Transform
Position
Rotation
Scale
基础 Transform 对齐
```

它只处理 Transform 本身，不理解 Eye、Lip、Brow 等具体 Rig 语义。

---

# 5. Controller

当前入口：

```python
from muziToolset.core.rigging import ctrl_utils

ctrl_object = ctrl_utils.Ctrl(
    "ctrl_lf_eye_main_001"
)
```

`Ctrl` 当前负责：

```text
创建 / 获取 Controller
Shape
Color
Size
Axis
Shape Rotate
Shape Offset
SubCtrl
Controller Hierarchy
```

## 创建完整 Controller

```python
ctrl_object.create_ctrl(
    shape_name="shape_016",
    ctrl_color=17,
    ctrl_size=1.0,
    ctrl_axis="X+",
    create_hierarchy=True
)
```

当前标准层级：

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

这个结构可以被 Eye、Ear 等 Rig Module 复用。

!!! note "当前实现状态"
    `ctrl_utils.py` 当前仍同时使用 `maya.cmds` 和 PyMEL。文档以真实源码为准；后续如果迁移成纯 `maya.cmds`，会再单独更新 Runtime 与 API。

---

# 6. Guide

当前入口：

```python
from muziToolset.core.rigging import guide_utils
```

Guide Core 只负责通用 Guide 能力。

例如：

```text
创建 Guide
读取 Guide
定位 Guide
基础 Guide 数据处理
```

具体语义：

```text
Eye Ball
Eye Iris
Eye Aim
Upper Lid
Mouth Corner
```

由具体 System 决定，而不是由 Core 猜测。

---

# 7. Joint

当前入口：

```python
from muziToolset.core.rigging import jnt_utils
```

Joint Core 负责单个 Joint 或基础 Joint 创建能力。

如果你在写完整模块，通常不会直接让 UI 大量调用 `jnt_utils`，而是让 `RigModule` 或具体 Module 组合它。

例如 Eye Module：

```text
EyeModule.create_joints()
        ↓
RigModule.create_joint()
        ↓
jnt_utils.Jnt
```

---

# 8. 完整 Rig Module 不属于 Core

如果你需要做的是：

```text
创建 Eye Joint
创建 Main / Aim Controller
创建模块 Group
建立 Aim Constraint
建立 Pose Driver
连接最终 Joint
```

这已经不是 Core 能力，而是完整 System。

当前通用模块基类：

```python
from muziToolset.systems import rig_module
```

具体模块例如：

```python
from muziToolset.systems.face import eye_module

rig_object = eye_module.EyeModule(
    side="lf"
)

rig_object.build()
```

---

# 9. `core/bake/` 怎么看

你在 API 左侧仍然会看到：

```text
core/bake/attrUtils.py
core/bake/controlUtils.py
core/bake/jointUtils.py
core/bake/pipelineUtils.py
core/bake/weightsUtils.py
...
```

这些文件是旧版工具和历史兼容代码。

阅读规则：

```text
当前新功能
    -> 优先 common / rigging

维护旧功能
    -> 必要时查询 bake

准备删除旧文件
    -> 先检查 Runtime import / Tests / Tools 依赖
```

不要因为网站还有 API 页面，就认为 `bake` 是当前首选架构。

---

# 判断一个功能应该放哪里

```text
只是通用 Maya 数据 / DAG / Transform？
        ↓
core/common

是多个 Rig Module 共用的 Ctrl / Guide / Jnt 基础能力？
        ↓
core/rigging

已经是一整个 Eye / Ear / Lip / Brow Rig？
        ↓
systems

主要是给绑定师点击和输入参数？
        ↓
tools

是公共 PySide Widget / Theme / Window？
        ↓
ui
```

---

# 常见误区

## 不要把业务逻辑下沉到 Core

错误思路：

```text
core/rigging/jnt_utils.py
    create_eye_joint_system()
```

更合理：

```text
systems/face/eye_module.py
    EyeModule.create_joints()
```

因为“Eye Joint System”已经是具体业务。

## 不要优先从 `bake` 复制旧代码

如果旧文件里存在需要复用的算法，先判断：

```text
它是否应该迁移到 common / rigging？
```

而不是在新模块里再复制一份。

## 不要根据旧文档猜模块名

当前 Core 的真实目录很小：

```text
common:  4 个正式模块
rigging: 3 个正式模块
```

详细方法以自动生成 API 为准。

---

# 继续查看

[Core 架构设计](../architecture/core.md){ .md-button }
[打开 Core API](../reference/core/index.md){ .md-button .md-button--primary }
[Tools 与 Systems](../architecture/tools-systems.md){ .md-button }
