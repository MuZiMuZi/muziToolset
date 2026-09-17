# Rig Architecture 0.4 — 已退休历史记录

这份页面过去记录过一版已经退出当前仓库的 Rig 架构，例如：

```text
systems/rig_base.py
systems/module_base.py
systems/ctrl_base.py
```

以及：

```text
RigBase
ModuleBase
RigModuleBase
CtrlBase
systems/face/modules/
systems/face/build/
```

这些路径和类型**已经不是当前 MuziTools 正式架构**。

为了避免旧链接直接 404，本页保留文件名，但旧迁移正文已经删除。

## 当前架构入口

请以这些页面为准：

- [总体架构](../architecture/index.md)
- [Core 设计](../architecture/core.md)
- [Tools 与 Systems](../architecture/tools-systems.md)
- [Face System](../architecture/face-system.md)
- [Face Workflow State](../architecture/face-workflow-state.md)
- [Rig Library](../manual/rig-library.md)
- [API Reference](../reference/index.md)

## 当前正式核心结构

```text
core/common/
    attr_utils.py
    hierarchy_utils.py
    name_utils.py
    transform_utils.py

core/rigging/
    ctrl_utils.py
    guide_utils.py
    jnt_utils.py

systems/
    rig_module.py
    face/
    components/
    rig/
```

当前完整业务 Module 使用：

```text
systems/rig_module.py
```

Controller 基础能力使用：

```text
core/rigging/ctrl_utils.py
```

Joint 基础能力使用：

```text
core/rigging/jnt_utils.py
```

Rig 标准命名使用：

```text
core/common/name_utils.py
```

## 当前 Rig Library Workflow

```text
01 Setup
02 Guide
03 Ctrl
04 Final
```

详细行为以 [Rig Library](../manual/rig-library.md) 和 [Face Workflow State](../architecture/face-workflow-state.md) 为准。

!!! warning "不要继续引用旧 0.4 API"
    新代码和新文档不应再引用 `RigBase / ModuleBase / CtrlBase` 那套已退休架构。保留本页只为了让历史链接明确告诉读者“旧版本已经退出”，而不是继续维护旧实现说明。
