# Core 架构

`core/` 是 MuziTools 当前 Runtime 中最底层的 Maya / Rigging 基础能力层。

这一页已经按照当前仓库结构重新编写。旧版本中以大量平铺 `*_utils.py` 作为正式 Core 的说明不再适用；现在正式结构以 **`common/` + `rigging/`** 为主，`bake/` 作为历史兼容区保留。

---

## 当前目录结构

```text
core/
├── __init__.py
├── common/
│   ├── __init__.py
│   ├── attr_utils.py
│   ├── hierarchy_utils.py
│   ├── name_utils.py
│   └── transform_utils.py
├── rigging/
│   ├── __init__.py
│   ├── ctrl_utils.py
│   ├── guide_utils.py
│   └── jnt_utils.py
└── bake/
    └── ... legacy / compatibility modules
```

Core 当前只承担**可被多个 Tool / System 重复使用的基础能力**，不负责完整业务 Workflow。

---

# 一句话原则

> **Common 处理通用 Maya 数据与节点操作，Rigging 处理可复用的绑定基础对象，完整 Rig Workflow 放到 Systems。**

这条边界非常重要。

例如：

```text
生成一个标准名称
    -> core/common/name_utils.py

创建一个 Controller 和 Controller Hierarchy
    -> core/rigging/ctrl_utils.py

创建一整套 Eye Rig
    -> systems/face/eye_module.py

组织模块库和 Step Workflow
    -> systems/rig/
```

---

# `core/common/`

`common/` 负责不绑定某个特定 Rig Module 的基础操作。

## `name_utils.py`

负责 MuziTools 的标准命名数据。

当前命名规则：

```text
[type]_[side]_[part]_[function]_[index]
```

示例：

```text
ctrl_lf_eye_main_001
jnt_rt_brow_bind_003
grp_md_face_master_001
loc_lf_upper_lid_bind_001
```

`part` 允许包含下划线，因此：

```text
upper_lid
nose_center
mouth_corner
```

都可以作为一个完整 Part 处理。

主要职责：

```text
Name
├── compose_name()
├── decompose_name()
└── flip()
```

适用场景：

- Joint / Controller / Group / Locator 创建前统一命名；
- 从已有节点名拆出 side / part / function；
- 左右镜像时翻转 `lf / rt`；
- Rig Module 创建稳定、可预测的节点名称。

API：[`core/common/name_utils.py`](../reference/core/common/name_utils.md)

---

## `attr_utils.py`

负责 Maya Attribute 的基础操作。

当前核心对象：

```text
Attr
```

主要能力包括：

```text
检查属性
添加属性
读取 / 设置属性
Lock / Unlock
Hide / Show
Lock + Hide
连接属性
断开属性
```

常见使用场景：

- Controller 增加 `follow`、`ikFk`、`visibility` 等自定义属性；
- 锁定不希望动画师修改的通道；
- 构建 Controller → Joint / Utility Node 的属性连接；
- 重建 Rig 前清理已有连接。

!!! note "当前实现"
    当前 `attr_utils.py` 仍包含 PyMEL 实现。它属于当前仓库真实 Runtime 状态，因此文档按现状记录；未来如果统一迁移到 `maya.cmds`，应在源码迁移完成后同步更新这里，而不是提前写成不存在的架构。

API：[`core/common/attr_utils.py`](../reference/core/common/attr_utils.md)

---

## `hierarchy_utils.py`

负责 DAG Parent、额外 Group 和层级相关的通用操作。

它解决的问题不是“某个 Eye Rig 的层级是什么”，而是：

```text
如何安全 Parent
如何获取 / 创建额外层级
如何在重复 Build 时复用已有 Group
如何保持 Transform / Hierarchy 操作一致
```

Controller 和 Rig Module 可以在此基础上搭建自己的业务层级。

例如 Controller Hierarchy 的创建会由 `ctrl_utils.py` 调用这里的基础层级能力，而不是每个 System 自己复制一套 Parent Helper。

API：[`core/common/hierarchy_utils.py`](../reference/core/common/hierarchy_utils.md)

---

## `transform_utils.py`

负责通用 Transform 数据操作。

典型职责包括：

```text
位置 / 旋转 / 缩放
Transform Match
世界空间数据
矩阵或 Transform 对齐辅助
```

边界：

- 可以处理任意 Maya Transform；
- 不应该知道 Eye / Brow / Lip 等业务语义；
- 不应该创建完整 Rig Module。

API：[`core/common/transform_utils.py`](../reference/core/common/transform_utils.md)

---

# `core/rigging/`

`rigging/` 比 `common/` 更接近绑定业务，但仍然只提供**基础绑定对象能力**。

当前正式模块：

```text
ctrl_utils.py
guide_utils.py
jnt_utils.py
```

---

## `ctrl_utils.py`

Controller 基础能力中心。

当前核心对象：

```text
Ctrl
```

主要职责：

```text
Controller Transform 创建 / 获取
Controller Shape Library
颜色
大小
轴向
Shape CV Rotate / Offset
SubCtrl
Controller Hierarchy
Shape 保存与读取
```

当前标准 Controller Hierarchy：

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

其中：

- `zero`：模块对齐后的干净入口；
- `driven`：系统驱动层，例如 Aim / Space 等；
- `space`：空间切换预留层；
- `connect`：模块连接预留层；
- `offset`：额外偏移；
- `ctrl`：动画师操作 Transform；
- `subctrl`：次级控制；
- `output`：稳定输出接口。

Shape 修改尽量发生在 Curve CV 层，而不是污染 Controller Transform。

例如：

```text
set_ctrl_size()
set_ctrl_axis()
set_ctrl_rotate()
set_ctrl_offset()
```

都用于保持动画 Transform 尽可能干净。

API：[`core/rigging/ctrl_utils.py`](../reference/core/rigging/ctrl_utils.md)

---

## `guide_utils.py`

负责可复用 Guide 基础能力。

Guide 是 Rig 构建之前的定位数据，不等于最终 Joint / Controller。

该层应该负责：

```text
Guide Transform
Guide 查询
Guide 数据读取
Guide 通用操作
```

而具体“Eye 需要 Ball / Iris / Aim 三个 Locator”这种语义应该放在：

```text
systems/face/face_guide_config.py
systems/face/eye_module.py
```

因此：

```text
Guide 基础操作 -> core/rigging/guide_utils.py
Face Guide 业务规则 -> systems/face/
```

API：[`core/rigging/guide_utils.py`](../reference/core/rigging/guide_utils.md)

---

## `jnt_utils.py`

负责 Joint 基础创建和通用 Joint 操作。

它提供的是：

```text
如何创建 Joint
如何根据 Guide 对齐 Joint
如何处理 Joint 基础属性
```

而不是：

```text
Eye Joint 应该有几个
Brow Joint 应该如何排列
Lip Joint 应该如何连接
```

这些数量、语义和驱动关系属于 `systems/`。

API：[`core/rigging/jnt_utils.py`](../reference/core/rigging/jnt_utils.md)

---

# `core/bake/`

`core/bake/` 是仓库中的历史兼容区域。

这里仍保存较早版本的完整 Utility 实现，例如历史 Controller、Joint、Attribute、File、Skin 等工具。

它存在的原因主要是：

```text
兼容旧代码
保留迁移参考
避免一次性删除导致未知 Runtime 依赖断裂
```

但新架构开发时，不应该因为 `bake/` 中存在某个 Helper，就默认它仍是当前推荐入口。

当前推荐优先级：

```text
core/common/
    +
core/rigging/
    ↓
如果当前正式层确实没有对应能力
    ↓
再检查 bake / legacy 依赖与迁移状态
```

!!! warning "不要直接批量删除 bake"
    `bake/` 是否可以删除必须通过真实 Import、测试和 Runtime 使用情况确认。文档可以把它从“推荐架构”中移除，但源码删除应该单独作为 Runtime 重构处理。

---

# Core 不应该做什么

下面这些内容不应该塞进 Core：

## 1. 完整 Face Rig Module

错误方向：

```text
core/eye_rig.py
core/lip_rig.py
```

正确方向：

```text
systems/face/eye_module.py
systems/face/...
```

---

## 2. 具体 Step Workflow

例如：

```text
Step 01 Setup
Step 02 Guide
Step 03 Build
Step 04 Connect
```

这是业务 Workflow，不属于 Core。

---

## 3. Tool UI

按钮、Selection、用户输入和工具窗口应该在：

```text
tools/
ui/
app/
```

---

## 4. 重复 System Helper

如果一个 System 需要：

```text
创建 Controller
创建 Joint
标准命名
安全 Parent
```

应该调用 Core，而不是在 System 中重新复制一份通用实现。

---

# Core 与 Systems 的关系

一个典型 Eye Rig 的调用关系可以理解成：

```text
systems/face/eye_module.py
    │
    ├── name_utils.Name
    │       -> 生成稳定节点名
    │
    ├── RigModule.create_joint()
    │       -> 底层 Joint 能力
    │
    ├── RigModule.create_ctrl()
    │       -> ctrl_utils.Ctrl
    │
    ├── hierarchy_utils.parent()
    │       -> DAG 层级
    │
    └── maya.cmds constraint / connection
            -> Eye Module 专属业务连接
```

Core 提供“积木”，System 决定“积木怎么组合成一个完整绑定模块”。

---

# 新增能力时放在哪里

可以用下面的判断顺序：

```text
这个能力是否与具体 Rig 部位无关？
    │
    ├── 是
    │   ↓
    │   是否属于基础 Maya 数据 / DAG / Attr / Naming / Transform？
    │       ├── 是 -> core/common/
    │       └── 否
    │           ↓
    │           是否属于通用 Controller / Guide / Joint？
    │               ├── 是 -> core/rigging/
    │               └── 否 -> 再判断是否应该是 System
    │
    └── 否
        ↓
        systems/
```

例如：

| 新功能 | 应放位置 |
| --- | --- |
| 标准名称解析 | `core/common/name_utils.py` |
| 安全 Parent | `core/common/hierarchy_utils.py` |
| Controller Shape 大小 | `core/rigging/ctrl_utils.py` |
| 通用 Joint 创建 | `core/rigging/jnt_utils.py` |
| Eye Aim 驱动 | `systems/face/eye_module.py` |
| Rig Library Catalog | `systems/rig/` |
| UI Object Picker | `ui/widgets/` |

---

# 推荐阅读

如果你准备修改 Core，建议按顺序阅读：

1. [总体架构](index.md)
2. 当前页面
3. [Tools 与 Systems](tools-systems.md)
4. [Core API](../reference/core/index.md)
5. [文档维护规范](../development/documentation.md)

查具体方法时不要继续在架构文档里找，直接进入自动生成的 [Core API Reference](../reference/core/index.md)。
