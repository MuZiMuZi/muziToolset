# 常用工具工作流

这页是绑定师的“任务目录”。

不需要先知道某个 Python 文件叫什么，只要先找到你想做的事情，再进入对应用户手册或 API。

## 快速选择

| 我想做什么 | 先看这里 | 主要 Tool / System |
| --- | --- | --- |
| 重命名、属性、连接、约束、吸附 | [基础工具](basic-tools.md) | `tools/basic/` |
| 创建 / 修改 Controller | [Controller 工作流](controller.md) | `tools/controller/` + `systems/controller/` |
| 创建 / 重采样 Joint | [Joint 工作流](joint.md) | `tools/joint/` + `core/joint_utils.py` |
| Skin、Influence、权重 | [Skin 工作流](skin.md) | `tools/skin/` + `core/skin_utils.py` |
| BlendShape / Corrective | [BlendShape 工作流](blendshape.md) | `tools/blendshape/` + `core/blendshape_utils.py` |
| 模型检查、场景清理 | [场景清理与模型检查](cleanup.md) | `tools/clean/` + Scene Core |
| Face Setup / Guide | [Face Guide](face-guide.md) | `tools/face/` + `systems/face/` |
| 完整 Rig Builder | [绑定工作流](rigging.md) | `systems/` |

---

# 基础操作

基础工具包括：

```text
Rename
Attribute
Connections
Constraint
Snap
```

进入：[基础工具](basic-tools.md)

对应 API：

- [rename_tool.py](../reference/tools/basic/rename_tool.md)
- [attr_tool.py](../reference/tools/basic/attr_tool.md)
- [connections_tool.py](../reference/tools/basic/connections_tool.md)
- [constraint_tool.py](../reference/tools/basic/constraint_tool.md)
- [snap_tool.py](../reference/tools/basic/snap_tool.md)

---

# Controller

如果你想：

- 创建标准 Controller；
- 创建 FK Controller；
- 改 Shape / 颜色 / 大小；
- 理解 Zero / Driven / Space / Connect / Offset；
- 使用 Parent Space Blend；

进入：[Controller 工作流](controller.md)

主要 API：

- [create_ctrl_tool.py](../reference/tools/controller/create_ctrl_tool.md)
- [create_fk_ctrl_tool.py](../reference/tools/controller/create_fk_ctrl_tool.md)
- [control_shape_tool.py](../reference/tools/controller/control_shape_tool.md)
- [systems/controller/builder.py](../reference/systems/controller/builder.md)
- [systems/controller/space_blend.py](../reference/systems/controller/space_blend.md)

---

# Joint

如果你想：

- 创建 Joint；
- 创建 Joint Chain；
- 重采样 Joint；
- 沿 Curve 分布骨骼；
- 检查 Joint Orient；

进入：[Joint 工作流](joint.md)

主要 API：

- [joint_tool.py](../reference/tools/joint/joint_tool.md)
- [joint_resamp_tool.py](../reference/tools/joint/joint_resamp_tool.md)
- [joint_utils.py](../reference/core/joint_utils.md)

---

# Skin

如果你想：

- 创建 SkinCluster；
- 查询 Influence；
- 导入 / 导出权重；
- 调整或检查权重；

进入：[Skin 工作流](skin.md)

主要 API：

- [skin_tool.py](../reference/tools/skin/skin_tool.md)
- [skin_utils.py](../reference/core/skin_utils.md)

---

# BlendShape

如果你想：

- 添加 BlendShape Target；
- 做 Corrective；
- Invert Shape；
- 管理 Face Shape；

进入：[BlendShape 工作流](blendshape.md)

主要 API：

- [add_blendshape_tool.py](../reference/tools/blendshape/add_blendshape_tool.md)
- [invert_shape_tool.py](../reference/tools/blendshape/invert_shape_tool.md)
- [blendshape_utils.py](../reference/core/blendshape_utils.md)

---

# 场景清理与模型检查

如果你想：

- 检查模型；
- 清理 Outliner；
- 删除明确无用节点；
- 发布前检查场景；

进入：[场景清理与模型检查](cleanup.md)

主要 API：

- [model_checker.py](../reference/tools/clean/model_checker.md)
- [hierarchy_cleaner.py](../reference/tools/clean/hierarchy_cleaner.md)
- [model_check_utils.py](../reference/core/model_check_utils.md)
- [scene_clean_utils.py](../reference/core/scene_clean_utils.md)

---

# Face

Face UI 入口：

- [face_rig_tool.py](../reference/tools/face/face_rig_tool.md)
- [face_select_key_tool.py](../reference/tools/face/face_select_key_tool.md)

正式 Face Rig 生命周期位于：

```text
systems/face/
```

从 [Face Guide](face-guide.md) 开始。

---

# Rig 辅助工具

`tools/rig/` 当前包含：

- [rig_tool.py](../reference/tools/rig/rig_tool.md)
- [skirt_ctrl_tool.py](../reference/tools/rig/skirt_ctrl_tool.md)

当一个 Tool 的核心逻辑开始拥有稳定输入、输出、可重复 Build 和完整节点网络时，应该把算法继续下沉到 `systems/`。

---

# 如何打开 Tool

多数 UI Tool 提供 `main()`：

```python
from muziToolset.tools.basic import attr_tool

window = attr_tool.main()
```

如果某个 Tool 是一次性执行操作，它的 `main()` 可能直接处理当前 Selection。

具体入口、参数和返回值请打开对应 `.py` API 页面。

---

# 我应该看用户手册还是 API？

```text
不知道怎么完成任务
    → 用户手册

知道模块，但不知道函数怎么调用
    → API Reference

准备修改整个 Rig 架构
    → 架构 + Systems API
```

继续查看：

- [绑定工作流](rigging.md)
- [API Reference](../reference/index.md)
