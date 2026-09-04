# Tools 与 Systems

## Tools

`tools/` 是用户直接使用的小工具层。

主要职责：

1. 创建 PySide UI；
2. 读取用户 Selection / 输入参数；
3. 做交互级错误提示；
4. 调用 Core / System；
5. 提供统一 `main()` 入口。

推荐数据流：

```text
User
  ↓
Tool UI
  ↓
Systems / Core
  ↓
Maya Scene
```

Tool 不复制 Core 或 System 算法。

例如 Controller Creator：

```text
Tool UI
    ↓
systems.ctrl_base.create_ctrl()
    ↓
core.control_shape_utils / hierarchy_utils / ...
```

---

# Systems

`systems/` 保存 Rig Object Identity、完整可复用 Rig Workflow 和业务 Module。

0.4 基础结构：

```text
systems/
├── rig_base.py
├── module_base.py
├── ctrl_base.py
├── face/
├── body/
└── rig/
```

## RigBase

负责：

```text
Rig Object Identity
    side / part / index

Rig Naming
    [node_type]_[side]_[part]_[function]_[index]

Side Semantic
    Mirror / Left / Right / Center
```

`RigBase` 是实例化基类，不作为 `RigBase.create_name(...)` 工具类使用。

例如：

```python
rig = RigBase(
    side="lf",
    part="arm",
    index=1
)

jnt_name = rig.create_name(
    node_type="jnt",
    function="bind"
)
```

## ModuleBase

负责 Module Lifecycle。

完整业务单元统一称为 Module，例如：

```text
TeethModule
JawModule
TongueModule
EyeModule
```

不再使用 Component 术语。

因为 `ModuleBase` 继承 `RigBase`，Module 自己就是一个带 Identity 的 Rig Object。

## CtrlBase

负责 Controller Workflow：

```text
Controller Hierarchy
FK Controller
Follow
Space Switch
Space Blend
```

Controller 的唯一正式实现是：

```text
systems/ctrl_base.py
```

旧 `systems/controller/` 已删除。

---

# Builder

Builder 是可组合算法，不等于完整 Module。

例如：

```text
systems/face/build/curve_attachment.py
systems/face/build/eyelid/
systems/face/build/lip/
```

这些 Builder 可以被未来的 EyeModule / BrowModule / LipModule 组合使用。

Builder 如果需要标准 Rig Naming，应创建明确的短生命周期 `RigBase` Identity 实例，而不是把 `RigBase` 当静态 Naming Utility。

---

# 如何判断放哪里

如果一个函数只是：

> 给我两个节点，我创建 Parent Constraint。

放：

```text
core/constraint_utils.py
```

如果一个流程是：

> 描述一个 Rig Object 的 side / part / index，并基于这个 Identity 创建节点名。

放：

```text
systems/rig_base.py
```

如果一个流程是：

> 创建标准 Controller 层级、Follow 或 Space Switch。

放：

```text
systems/ctrl_base.py
```

如果一个流程是：

> 根据 Teeth Guide 创建 Controller、Jnt、Matrix、Rigid Skin。

放：

```text
systems/face/modules/teeth.py
```

如果一个功能需要按钮、输入框或 Selection：

放：

```text
tools/
```

但实际 Rig 算法仍下沉 Core / System。

---

# 单一事实来源

正式架构禁止同一职责存在两套实现。

```text
Rig Identity / Naming -> systems.rig_base
Module Lifecycle      -> systems.module_base
Controller Rig        -> systems.ctrl_base
Maya Rename           -> core.rename_utils
```

RigBase Naming Keyword 统一为 `node_type=`；旧 `type=` 不保留 Compatibility Wrapper。

旧入口不保留 Compatibility Wrapper，避免后续新代码再次依赖退休架构。
