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

`systems/` 保存完整、可复用的 Rig Workflow 和业务 Module。

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

负责 Rig Naming。

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

---

# 如何判断放哪里

如果一个函数只是：

> 给我两个节点，我创建 Parent Constraint。

放：

```text
core/constraint_utils.py
```

如果一个流程是：

> 创建标准 Controller 层级、Follow 或 Space Switch。

放：

```text
systems/ctrl_base.py
```

如果一个流程是：

> 根据 Teeth Guide 创建 Controller、Joint、Matrix、Rigid Skin。

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
Rig Naming       -> systems.rig_base
Module Lifecycle -> systems.module_base
Controller Rig   -> systems.ctrl_base
Maya Rename      -> core.rename_utils
```

旧入口不保留 Compatibility Wrapper，避免后续新代码再次依赖退休架构。
