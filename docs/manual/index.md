# MuziTools 用户手册

这里从“**我要完成什么**”出发，而不是按源码文件顺序解释项目。

如果你正在 Maya 里实际做绑定，优先从这里开始；如果你已经在修改 Python 源码，则进入 [API Reference](../reference/index.md)。

---

## 绑定库 / Modular Rig

当前最重要的工作流入口：

[打开 Rig Library 使用手册](rig-library.md)

当前四步：

```text
01 Setup
02 Guide
03 Ctrl
04 Final
```

适合：

- 添加 Eye / Ear / Tongue / FK Chain；
- 导入并调整 Guide；
- 生成 Joint / Controller；
- 调整 Controller 和 Joint 显示；
- Mirror；
- Rebuild；
- Final Connect。

---

## Face Rig

### Face Guide

[Face Guide 使用手册](face-guide.md)

用于理解 Face Locator、标准命名、左右镜像和 Module Guide Contract。

### Face System

如果你需要理解 Eye / Ear / Tongue Module 的实现结构，进入：

[Face System Architecture](../architecture/face-system.md)

---

## Controller

[Controller 使用手册](controller.md)

包括：

```text
创建 Controller
Shape Library
颜色
大小
Axis
Offset / Rotate
SubCtrl
标准 Hierarchy
```

当前底层正式入口：

```text
core/rigging/ctrl_utils.py
```

---

## Joint

[Jnt 使用手册](jnt.md)

包括：

```text
创建 Joint
Guide 对齐
Radius
Local Axis Display
Module Joint Output
```

当前底层正式入口：

```text
core/rigging/jnt_utils.py
```

---

## Core

[Core 使用手册](core.md)

适合需要直接调用底层 API 的开发者。

当前正式 Core：

```text
core/common/
core/rigging/
```

架构说明见 [Core 架构](../architecture/core.md)。

---

## 日常基础工具

[基础工具](basic-tools.md)

包含：

```text
Rename
Attribute
Connection
Constraint
Snap
```

工具目录：

```text
tools/basic/
```

---

## Skin

[Skin 使用手册](skin.md)

用于日常 Skin 相关工具入口和工作流说明。

---

## BlendShape

[BlendShape 使用手册](blendshape.md)

用于 BlendShape Target、Shape 操作等工具入口。

---

## 场景清理

[Cleanup / Model Check](cleanup.md)

用于：

```text
Hierarchy Clean
Model Check
提交绑定前检查
```

---

## 绑定工作流

[绑定工作流](rigging.md)

用于理解普通绑定任务和 Modular Rig 在项目中的关系。

---

## 工具总览

[Tools 总览](tools.md)

按目录查看当前：

```text
basic
blendshape
clean
controller
face
jnt
rig
skin
```

---

# 我应该看哪一份文档？

| 需求 | 推荐 |
| --- | --- |
| 我想直接使用 Rig Library | [Rig Library](rig-library.md) |
| 我要调整 Face Guide | [Face Guide](face-guide.md) |
| 我要创建/调整 Controller | [Controller](controller.md) |
| 我要处理 Joint | [Jnt](jnt.md) |
| 我要理解项目分层 | [总体架构](../architecture/index.md) |
| 我要理解 Face Module | [Face System](../architecture/face-system.md) |
| 我要查函数参数 | [API Reference](../reference/index.md) |
| 我要维护文档 | [文档维护](../development/documentation.md) |

---

# 文档搜索建议

如果你知道真实名称，直接使用顶部搜索：

```text
EyeModule
RigLibraryService
Ctrl
Jnt
Name
connect_rig
rebuild_module
mirror_module
create_ctrl
get_guides
```

用户手册负责“怎么做”，API Reference 负责“怎么调用”。
