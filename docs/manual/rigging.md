# 绑定工作流

这页只回答一个问题：**完整角色绑定下一步应该做什么？**

```text
模型检查
   ↓
基础整理
   ↓
Joint
   ↓
Controller
   ↓
Skin
   ↓
BlendShape / Corrective
   ↓
Face / Body System
   ↓
发布前检查
```

<div class="grid cards" markdown>

-   :material-cube-scan:{ .lg .middle } **1. 模型与场景**

    ---

    检查模型、Transform、History 和 Outliner。

    [:octicons-arrow-right-24: 场景检查](cleanup.md)

-   :material-form-textbox:{ .lg .middle } **2. 基础整理**

    ---

    命名、属性、连接、约束和吸附。

    [:octicons-arrow-right-24: 基础工具](basic-tools.md)

-   :material-bone:{ .lg .middle } **3. Joint**

    ---

    创建 Skeleton、Joint Chain 和 Orient。

    [:octicons-arrow-right-24: Joint](joint.md)

-   :material-vector-circle:{ .lg .middle } **4. Controller**

    ---

    创建标准控制器、FK、Follow 和 Space。

    [:octicons-arrow-right-24: Controller](controller.md)

-   :material-human-handsup:{ .lg .middle } **5. Skin**

    ---

    SkinCluster、Influence 和权重。

    [:octicons-arrow-right-24: Skin](skin.md)

-   :material-shape-plus:{ .lg .middle } **6. Corrective**

    ---

    BlendShape、Corrective 和 Invert Shape。

    [:octicons-arrow-right-24: BlendShape](blendshape.md)

-   :material-face-recognition:{ .lg .middle } **7. Face Rig**

    ---

    Face Setup、Guide、Module Build 和 Finalize。

    [:octicons-arrow-right-24: Face Guide](face-guide.md)

-   :material-check-decagram:{ .lg .middle } **8. 发布检查**

    ---

    重新检查场景、层级和模型状态。

    [:octicons-arrow-right-24: 发布前检查](cleanup.md)

</div>

## 开发时怎么选目录

```text
通用 Maya 算法           → core/
用户操作 / UI            → tools/
Rig Naming               → systems/rig_base.py
Module Lifecycle         → systems/module_base.py
Controller Workflow      → systems/ctrl_base.py
完整 Rig Module / System → systems/
公共界面组件             → ui/
应用入口和窗口管理       → app/
```

!!! tip "不要跨层重复实现"
    如果一个算法已经存在于 Core，Tool 和 System 应直接复用；如果完整 Rig Module 已经进入 System，Tool 只负责收集输入和触发正式 API。

## 继续查看

[用户手册](index.md){ .md-button }
[总体架构](../architecture/index.md){ .md-button }
[API Reference](../reference/index.md){ .md-button .md-button--primary }
