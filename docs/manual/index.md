# MuziTools 用户手册

用户手册从“你现在想完成什么”出发，而不是从 Python 包结构出发。

如果你只想完成绑定工作，优先使用本手册；如果你正在写代码或修改系统，再进入 [API Reference](../reference/index.md)。

<div class="grid cards" markdown>

-   :material-play-circle-outline:{ .lg .middle } **第一次使用**

    ---

    安装、启动、确认 Maya Script Path，并打开主工具箱。

    [:octicons-arrow-right-24: 安装与启动](../getting-started/installation.md)

-   :material-hammer-wrench:{ .lg .middle } **日常小工具**

    ---

    命名、属性、连接、约束、控制器、Joint、Skin 等常用操作。

    [:octicons-arrow-right-24: 常用工具工作流](tools.md)

-   :material-source-branch:{ .lg .middle } **完整绑定系统**

    ---

    Controller、Joint、Skin、BlendShape、Body、Face 等系统化绑定流程。

    [:octicons-arrow-right-24: 绑定工作流](rigging.md)

-   :material-face-recognition:{ .lg .middle } **Face Rig**

    ---

    从 Face Setup、Guide 定位到后续 Builder 的标准步骤。

    [:octicons-arrow-right-24: Face Guide](face-guide.md)

</div>

## 如何选择文档入口

| 你的问题 | 先看哪里 |
| --- | --- |
| “这个工具在哪里打开？” | [常用工具工作流](tools.md) |
| “Face Guide 应该怎么走流程？” | [Face Guide](face-guide.md) |
| “这个功能应该写在 Core 还是 System？” | [总体架构](../architecture/index.md) |
| “`get_lip_guides()` 参数是什么？” | [API Reference](../reference/index.md) |
| “为什么这个模块这样设计？” | [架构](../architecture/index.md) |
| “我要改源码，Docstring 怎么写？” | [文档维护](../development/documentation.md) |

## 推荐学习顺序

如果你第一次接触这个项目，建议：

```text
安装与启动
    ↓
常用工具
    ↓
绑定工作流
    ↓
架构
    ↓
API Reference
```

绑定师可以停留在前三层；开发者继续进入架构和 API。

## 使用搜索

用户手册适合搜索“任务”：

```text
创建控制器
重命名
刷权重
Face Guide
左右镜像
```

API Reference 适合搜索真实代码名称：

```text
create_controller
FaceGuide
validate_symmetry
Attr.connect_message
```

两套入口指向同一份源码和同一套功能，不再重复维护两份接口说明。
