# MuziTools 用户手册

用户手册从“你现在想完成什么”出发，而不是从 Python 包结构出发。

如果你只想完成绑定工作，优先使用本手册；如果你正在写代码或修改系统，再进入 [API Reference](../reference/index.md)。

<div class="grid cards" markdown>

-   :material-play-circle-outline:{ .lg .middle } **第一次使用**

    ---

    安装、启动、确认 Maya Script Path，并打开主工具箱。

    [:octicons-arrow-right-24: 安装与启动](../getting-started/installation.md)

-   :material-hammer-wrench:{ .lg .middle } **基础工具**

    ---

    重命名、属性、连接、约束和吸附等高频操作。

    [:octicons-arrow-right-24: 基础工具](basic-tools.md)

-   :material-gamepad-variant-outline:{ .lg .middle } **Controller**

    ---

    创建标准 Controller、FK 控制器、Shape 和 Space Blend。

    [:octicons-arrow-right-24: Controller 工作流](controller.md)

-   :material-bone:{ .lg .middle } **Joint**

    ---

    创建、重采样、分布和整理 Joint。

    [:octicons-arrow-right-24: Joint 工作流](joint.md)

-   :material-human-handsup:{ .lg .middle } **Skin**

    ---

    SkinCluster、Influence、权重和变形检查。

    [:octicons-arrow-right-24: Skin 工作流](skin.md)

-   :material-shape-outline:{ .lg .middle } **BlendShape**

    ---

    Target、Corrective 和 Invert Shape。

    [:octicons-arrow-right-24: BlendShape 工作流](blendshape.md)

-   :material-broom:{ .lg .middle } **清理与检查**

    ---

    模型检查、层级清理和发布前 Scene Check。

    [:octicons-arrow-right-24: 场景清理与模型检查](cleanup.md)

-   :material-face-recognition:{ .lg .middle } **Face Rig**

    ---

    从 Face Setup、Guide 定位到后续 Builder 的标准步骤。

    [:octicons-arrow-right-24: Face Guide](face-guide.md)

</div>

## 快速选择

| 你的问题 | 先看哪里 |
| --- | --- |
| “MuziTools 怎么安装和启动？” | [安装与启动](../getting-started/installation.md) |
| “这个工具在哪里打开？” | [常用工具工作流](tools.md) |
| “我要批量重命名 / 管理属性” | [基础工具](basic-tools.md) |
| “我要创建标准 Controller” | [Controller 工作流](controller.md) |
| “我要创建或重采样 Joint” | [Joint 工作流](joint.md) |
| “我要绑定模型 / 处理权重” | [Skin 工作流](skin.md) |
| “我要做 Corrective / BlendShape” | [BlendShape 工作流](blendshape.md) |
| “我要发布前检查场景” | [场景清理与模型检查](cleanup.md) |
| “Face Guide 应该怎么走流程？” | [Face Guide](face-guide.md) |
| “完整角色绑定下一步做什么？” | [绑定工作流](rigging.md) |
| “这个功能应该写在 Core 还是 System？” | [总体架构](../architecture/index.md) |
| “`get_lip_guides()` 参数是什么？” | [API Reference](../reference/index.md) |
| “我要改源码，Docstring 怎么写？” | [文档维护](../development/documentation.md) |

## 推荐学习顺序

第一次接触项目：

```text
安装与启动
    ↓
基础工具
    ↓
Controller / Joint / Skin
    ↓
完整绑定工作流
    ↓
Face Rig
    ↓
架构
    ↓
API Reference
```

绑定师通常停留在用户手册和工作流层；开发者继续进入架构和 API。

## 用户手册和 API Reference 的区别

用户手册回答：

> 我要完成什么？应该按什么顺序做？

API Reference 回答：

> 这个具体 Python 文件、类或方法怎么调用？

例如：

```text
我要制作眼皮 Guide
    ↓
Face Guide 用户手册
    ↓
知道应该调用 FaceGuide
    ↓
face_guide.py API
    ↓
get_eyelid_guides(side, required=True)
```

## 使用搜索

用户手册适合搜索“任务”：

```text
创建控制器
重命名
刷权重
Face Guide
左右镜像
场景清理
```

API Reference 适合搜索真实代码名称：

```text
create_controller
FaceGuide
validate_symmetry
Attr
skin_utils
matrix_utils
```

两套入口最终都指向同一套源码，不重复维护两份 API 定义。
