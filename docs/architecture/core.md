# Core 设计

`core/` 是 MuziTools 当前 Runtime 中最底层的**可复用 Maya 能力层**。

这一页已经按照当前仓库重新整理，不再保留旧版本中已经不存在的 `animation_utils.py`、`matrix_utils.py`、`constraint_utils.py`、`rename_utils.py`、`skin_utils.py` 等模块清单。

当前真实结构只有三部分：

```text
core/
├── common/
│   ├── attr_utils.py
│   ├── hierarchy_utils.py
│   ├── name_utils.py
│   └── transform_utils.py
│
├── rigging/
│   ├── ctrl_utils.py
│   ├── guide_utils.py
│   └── jnt_utils.py
│
└── bake/
    └── 历史工具与兼容代码
```

## 一句话原则

> Core 只提供可以被多个 Rig Module / Tool 重复使用的基础能力，不决定一个完整绑定模块应该怎样构建。

当前主要调用方向：

```text
App / Tool / Rig System
          ↓
      RigModule
          ↓
core.common + core.rigging
          ↓
      Maya Scene
```

---

# 当前 Core 的三个区域

## `core/common/`

负责最基础的 Maya Transform / DAG / Attribute / Naming 能力。

这些模块不应该理解 Eye、Ear、Brow、Lip、Teeth 等具体 Rig 业务。

```text
attr_utils.py
    Attribute、Lock / Hide、Message、连接相关基础操作

hierarchy_utils.py
    Parent、Group、额外层级、DAG 组织

name_utils.py
    MuziTools 当前标准 Rig 名称的组合、解析和左右翻转

transform_utils.py
    Transform 匹配、位置 / 旋转 / Scale 等通用变换操作
```

推荐 Import：

```python
from muziToolset.core.common import attr_utils
from muziToolset.core.common import hierarchy_utils
from muziToolset.core.common import name_utils
from muziToolset.core.common import transform_utils
```

---

## `core/rigging/`

负责比 `common` 更靠近绑定业务、但仍然可以被多个 Module 复用的基础对象。

```text
ctrl_utils.py
    单个 Controller 的创建、Shape、颜色、大小、轴向和 Controller Hierarchy

guide_utils.py
    Guide 的创建、读取和基础 Guide 操作

jnt_utils.py
    单个 Joint / Joint 基础结构的创建与匹配
```

推荐 Import：

```python
from muziToolset.core.rigging import ctrl_utils
from muziToolset.core.rigging import guide_utils
from muziToolset.core.rigging import jnt_utils
```

这些模块负责的是“一个基础对象怎么创建”，而不是“一个完整 Eye Rig 应该有哪些 Joint 和 Controller”。

例如：

```text
Ctrl.create_ctrl()
    -> Core Rigging

EyeModule.create_ctrls()
    -> Face Rig System
```

---

## `core/bake/`

`core/bake/` 是当前仓库中保留的**历史能力 / 旧工具兼容区**。

目录里仍包含旧版 CamelCase 工具，例如：

```text
attrUtils.py
controlUtils.py
jointUtils.py
hierarchyUtils.py
pipelineUtils.py
weightsUtils.py
...
```

它们仍然存在于仓库中，因此不能仅因为“文件旧”就直接删除。

但是新系统的架构文档、示例和新代码不应该继续把 `core/bake/` 当作默认入口。

推荐原则：

```text
新代码
    ↓
优先 core/common 或 core/rigging

旧代码仍有依赖
    ↓
保留 core/bake 兼容

确认无 Runtime / Tool / Test 依赖
    ↓
再单独做迁移或删除
```

因此 `bake` 在网站中仍会有 API 页面，但它属于**兼容参考**，不是当前推荐架构。

---

# 当前命名系统

旧文档中曾写过：

```text
core/name_utils.py 已删除
RigBase 负责全部 Naming
```

这已经不符合当前源码。

当前标准命名实现位于：

```text
core/common/name_utils.py
```

核心类：

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
# ctrl_lf_eye_main_001
```

当前名称格式：

```text
[type]_[side]_[part]_[function]_[index]
```

示例：

```text
grp_md_face_master_001
ctrl_lf_eye_main_001
ctrl_rt_eye_aim_001
jnt_lf_eye_bind_001
loc_rt_upper_lid_bind_001
```

`part` 可以包含下划线，因此：

```text
loc_lf_upper_lid_bind_001
```

可以正确解析为：

```text
type      = loc
side      = lf
part      = upper_lid
function  = bind
index     = 1
```

左右镜像命名可以使用：

```python
name_object.flip()
```

---

# Attribute：`attr_utils.py`

`core/common/attr_utils.py` 负责可以被多个系统重复使用的 Attribute 能力。

典型职责：

```text
创建 Attribute
读取 / 设置 Value
Lock / Unlock
Hide / Show
Message Attribute
Attribute Connection
```

它不应该决定：

```text
某个 Eye Controller 应该有哪些自定义属性
某个 Face Module 的属性如何组织
某个 UI 应该显示哪些参数
```

这些属于上层 Tool / System。

---

# Hierarchy：`hierarchy_utils.py`

`core/common/hierarchy_utils.py` 负责通用 DAG 层级操作。

典型职责：

```text
Parent
Group
创建额外 Group
查询 Parent / Child
整理通用 DAG 层级
```

Controller 的标准层级虽然最终会调用这里的基础能力，但完整 Controller Hierarchy 由：

```text
core/rigging/ctrl_utils.py
```

统一管理。

当前 Controller Hierarchy：

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

这个结构是当前 Eye、Ear 等 Module 可以复用的基础 Controller Contract。

---

# Transform：`transform_utils.py`

`core/common/transform_utils.py` 负责 Transform 层面的通用操作。

适合放在这里的能力：

```text
Match Transform
读取 / 设置世界空间位置
读取 / 设置旋转
读取 / 设置 Scale
基础 Transform 对齐
```

不适合放在这里的能力：

```text
Eye Main Ctrl 的 Pivot 必须位于 Ball Guide
Lip Joint 必须沿 Curve 分布
Brow Controller 必须跟随 Surface
```

这些都带有明确 Rig 业务语义，应该留在具体 `systems/` Module 中。

---

# Controller：`ctrl_utils.py`

`core/rigging/ctrl_utils.py` 是当前 Controller 基础实现。

主要职责包括：

```text
创建 / 获取 Controller Transform
加载 Shape Library
修改 Shape
设置颜色
设置大小
设置轴向
额外 Shape Rotate
Shape Offset
创建 SubCtrl
创建标准 Controller Hierarchy
```

当前 Shape 修改原则：

```text
颜色 / 大小 / 轴向 / Offset
        ↓
修改 NurbsCurve Shape / CV
        ↓
尽量保持 Controller Transform 干净
```

这也是 Step 03 调整 Controller 外观时使用的基础能力。

!!! note "当前迁移状态"
    当前 `ctrl_utils.py` 仍然同时使用 `maya.cmds` 与 PyMEL。它属于当前真实 Runtime 状态，因此文档不会假装它已经完全 cmds 化。后续如果继续执行“移除 PyMEL”的重构，应作为独立 Runtime 重构提交处理，而不是在文档中提前写成已经完成。

---

# Guide：`guide_utils.py`

`core/rigging/guide_utils.py` 提供可复用 Guide 基础能力。

Core Guide 只理解“Guide 是一个可以被创建、定位、查询的绑定辅助对象”。

具体模块的语义，例如：

```text
Eye Ball Guide
Eye Iris Guide
Eye Aim Guide
Upper Lid Guide
Mouth Corner Guide
```

不应该硬编码进 Core。

这些业务语义应该由：

```text
systems/face/face_guide_config.py
具体 Face Module
```

负责。

---

# Joint：`jnt_utils.py`

`core/rigging/jnt_utils.py` 负责 Joint 的基础创建和匹配能力。

例如完整 Eye Module 的职责分工是：

```text
EyeModule
    ↓
决定需要 1 个 Eye Bind Joint
决定 Joint 使用 Ball Guide
决定 Joint 名称
    ↓
RigModule.create_joint()
    ↓
core.rigging.jnt_utils.Jnt
    ↓
创建 / 匹配具体 Maya Joint
```

因此 Core 不应该自行决定：

```text
一个 Ear 要创建几个 Joint
一个 Lip 要创建多少 Joint
一个 Eye Joint 应该由哪个 Controller 驱动
```

---

# Core 与 `RigModule` 的边界

当前通用 Rig Module 基类位于：

```text
systems/rig_module.py
```

`RigModule` 负责把 Core 的单个基础对象组合进统一 Module Lifecycle。

当前主要公共能力：

```text
get_guides()
create_joint()
create_ctrl()
create_joints()
create_ctrls()
setup_hierarchy()
connect_rig()
build()
```

典型关系：

```text
EyeModule
    ↓
RigModule.create_ctrl()
    ↓
ctrl_utils.Ctrl
```

以及：

```text
EyeModule
    ↓
RigModule.create_joint()
    ↓
jnt_utils.Jnt
```

所以：

```text
Core
    负责基础对象能力

RigModule
    负责 Module 级通用 Lifecycle

EyeModule / EarModule / TongueModule
    负责具体 Rig 业务
```

---

# Core 不应该做什么

当前 Core 不应该负责：

- PySide 工具窗口；
- Rig Library UI；
- Step 01 / 02 / 03 / 04 Workflow 状态；
- Eye / Ear / Brow / Lip / Teeth 等完整业务模块；
- 自动决定某个 Face Module 应该创建哪些节点；
- 保存整个 Module 的 Build 状态；
- 把具体业务规则写进通用 Helper。

例如：

```text
创建单个 Controller
    -> core/rigging/ctrl_utils.py

创建 Eye Main + Eye Aim Controller
    -> systems/face/eye_module.py

把 Eye Module 注册到 Rig Library
    -> systems/rig/library_catalog.py
```

---

# 新代码应该放哪里

判断顺序：

```text
这是最基础的 Maya 通用操作吗？
    ↓ 是
core/common/

这是多个 Rig Module 都会复用的 Controller / Guide / Joint 能力吗？
    ↓ 是
core/rigging/

这是完整 Rig 模块或 Workflow 吗？
    ↓ 是
systems/

这是绑定师直接点击使用的小工具吗？
    ↓ 是
tools/

这是公共 PySide 组件吗？
    ↓ 是
ui/
```

如果一个函数名字已经带有：

```text
eye
brow
lip
ear
teeth
jaw
```

通常说明它已经具有明确业务语义，不应该继续下沉到 Core，除非它确实只是非常通用的数据查询。

---

# 当前 Core 开发规则

新 Core 代码遵守：

1. 优先明确参数，不依赖当前 Selection；
2. 先验证节点和输入；
3. 返回明确的 Node / List / Dict / Value；
4. 不创建 Tool UI；
5. 不决定完整 Rig Workflow；
6. 通用能力只实现一份，上层直接复用；
7. 中文注释重点解释 Maya / DG / DAG 特有原因；
8. 保持函数粒度清楚；
9. 优先显式 `for` 循环，避免为了缩短代码使用复杂推导式；
10. 新模块优先使用当前 snake_case 目录和文件命名；
11. `core/bake/` 只用于兼容，不作为新功能默认落点；
12. Runtime 重构和文档清理分开提交。

---

# 查看完整 Core API

当前 `core/` 的每个正式 Python 文件都会自动生成独立 API 页面。

进入：

[Core API Reference](../reference/core/index.md)

如果网站内容和源码发生冲突，以**当前源码 + Docstring** 为事实来源，生成文档应该随后被重新同步。
