# MuziTools 用户手册

从你现在要完成的任务开始，不需要先记住 Python 文件名。

<div class="grid cards" markdown>

-   :material-play-circle-outline:{ .lg .middle } **第一次使用**

    ---

    安装、启动和 Maya Script Path。

    [:octicons-arrow-right-24: 安装与启动](../getting-started/installation.md)

-   :material-hammer-wrench:{ .lg .middle } **常用工具**

    ---

    基础操作、Controller、Joint、Skin、BlendShape 和清理。

    [:octicons-arrow-right-24: 选择一个任务](tools.md)

-   :material-source-branch:{ .lg .middle } **完整绑定流程**

    ---

    从模型检查到 Skeleton、Controller、Skin 和 Face Rig。

    [:octicons-arrow-right-24: 绑定工作流](rigging.md)

-   :material-face-recognition:{ .lg .middle } **Face Rig**

    ---

    Face Setup、Guide、验证和后续 Builder。

    [:octicons-arrow-right-24: Face Guide](face-guide.md)

-   :material-library-outline:{ .lg .middle } **Core 能力**

    ---

    想知道某个 Maya 底层操作应该调用哪个 Core 模块。

    [:octicons-arrow-right-24: Core 能力选择](core.md)

-   :material-code-braces:{ .lg .middle } **API Reference**

    ---

    查询具体 `.py` 文件、类、方法、参数、返回值和示例。

    [:octicons-arrow-right-24: 打开 API Reference](../reference/index.md)

</div>

## 三种使用方式

=== "我是绑定师"

    ```text
    用户手册
        ↓
    选择任务
        ↓
    按步骤执行
    ```

=== "我要查代码"

    ```text
    API Reference
        ↓
    找到 .py 文件
        ↓
    查看方法参数和示例
    ```

=== "我要改架构"

    ```text
    架构文档
        ↓
    Core / Tool / System 边界
        ↓
    API Reference
    ```

!!! tip "搜索建议"
    搜“创建控制器、Face Guide、刷权重”这类任务时优先看用户手册；搜 `FaceGuide`、`Attr.connect_message` 这类真实代码名时直接进入 API Reference。

[查看总体架构](../architecture/index.md){ .md-button }
[打开 API Reference](../reference/index.md){ .md-button .md-button--primary }
