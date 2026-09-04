# 常用工具

这里不讲源码结构，只回答一件事：**你现在想完成什么？**

先选择任务，再进入对应手册；需要查参数和方法时，再跳到 API Reference。

<div class="grid cards" markdown>

-   :material-form-textbox:{ .lg .middle } **基础操作**

    ---

    重命名、属性、连接、约束和吸附。

    [:octicons-arrow-right-24: 打开基础工具](basic-tools.md)

-   :material-vector-circle:{ .lg .middle } **Controller**

    ---

    创建标准控制器、FK 控制器、修改 Shape、颜色和层级。

    [:octicons-arrow-right-24: 打开 Controller 手册](controller.md)

-   :material-bone:{ .lg .middle } **Jnt**

    ---

    创建 Jnt、Jnt Chain、重采样和 Orient。

    [:octicons-arrow-right-24: 打开 Jnt 手册](jnt.md)

-   :material-human-handsup:{ .lg .middle } **Skin**

    ---

    SkinCluster、Influence、权重查询和权重数据处理。

    [:octicons-arrow-right-24: 打开 Skin 手册](skin.md)

-   :material-shape-plus:{ .lg .middle } **BlendShape**

    ---

    添加 Target、Corrective、Invert Shape 和 Face Shape 管理。

    [:octicons-arrow-right-24: 打开 BlendShape 手册](blendshape.md)

-   :material-broom:{ .lg .middle } **场景清理**

    ---

    模型检查、层级清理、发布前检查和无用节点处理。

    [:octicons-arrow-right-24: 打开清理手册](cleanup.md)

-   :material-face-recognition:{ .lg .middle } **Face Rig**

    ---

    Face Setup、Guide、Eyelid、Lip 和后续 Face Builder。

    [:octicons-arrow-right-24: 打开 Face Guide](face-guide.md)

-   :material-source-branch:{ .lg .middle } **完整 Rig Workflow**

    ---

    了解 Tool、System、Core 如何组合成完整绑定系统。

    [:octicons-arrow-right-24: 打开绑定工作流](rigging.md)

</div>

## 怎么使用这套文档

1. **不知道怎么完成任务**：先看用户手册。
2. **知道文件，但不知道方法参数**：进入 [API Reference](../reference/index.md)。
3. **准备改底层架构**：先看 [架构](../architecture/index.md)，再修改代码。

!!! tip "推荐"
    日常使用时不要先记 Python 文件名。先从任务页进入，页面底部会给出对应源码和 API。
