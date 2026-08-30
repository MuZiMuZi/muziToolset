# MuziTools

面向 **Autodesk Maya 2023** 的绑定工具集与 Rigging Framework。

文档现在分成两条清晰路径：

- **用户手册**：从“我想完成什么”开始，按任务寻找操作步骤；
- **API Reference**：从具体 Python 文件、类和方法进入，查看参数、返回值、异常和示例。

<div class="grid cards" markdown>

-   :material-rocket-launch-outline:{ .lg .middle } **开始使用**

    ---

    安装 MuziTools，在 Maya 中启动主工具箱，并确认脚本路径。

    [:octicons-arrow-right-24: 安装与启动](getting-started/installation.md)

-   :material-tools:{ .lg .middle } **常用工具**

    ---

    从命名、属性、约束、控制器、Joint、Skin 等日常任务开始。

    [:octicons-arrow-right-24: 浏览常用工具](manual/tools.md)

-   :material-axis-arrow:{ .lg .middle } **绑定工作流**

    ---

    从 Controller、Joint、Skin、BlendShape 到 Face Rig，按绑定阶段查看推荐流程。

    [:octicons-arrow-right-24: 浏览绑定工作流](manual/rigging.md)

-   :material-code-braces:{ .lg .middle } **API Reference**

    ---

    每一个正式 Python 文件都有独立页面，并展开公开 Function / Class / Method。

    [:octicons-arrow-right-24: 打开 API Reference](reference/index.md)

</div>

## 你想做什么？

### 打开 MuziTools

```python
import muziToolset

muziToolset.show()
```

如果这是第一次运行，先看 [在 Maya 中运行](getting-started/maya-usage.md)。

### 查一个工具怎么用

进入 [常用工具工作流](manual/tools.md)，先按任务找到工具，再跳转到对应 API。

例如：

```text
我想批量改名
    ↓
Tools / Basic / Rename
    ↓
rename_tool.py API
```

### 查一个绑定系统怎么构建

进入 [绑定工作流](manual/rigging.md)。完整 Rig Component 放在 `systems/`，UI 工具只负责收集参数和调用它们。

### 做 Face Rig

从 [Face Guide](manual/face-guide.md) 开始。当前推荐流程：

```text
FaceSetup.build()
        ↓
FaceGuide.build()
        ↓
手动贴合 Guide
        ↓
FaceGuide.validate_guides()
        ↓
FaceGuide.finalize()
        ↓
Step 03 Builder
```

## 开发者入口

如果你正在修改源码，建议按下面顺序查文档：

1. [总体架构](architecture/index.md)：先确认功能应该放到 `core / tools / systems / ui / app` 哪一层；
2. [文档维护](development/documentation.md)：查看 Docstring 与 API 文档规范；
3. [API Reference](reference/index.md)：确认现有公开接口和调用方式；
4. [测试](development/testing.md)：运行对应 Smoke Test。

## 文档搜索

顶部搜索支持中文和英文关键词。建议直接搜索：

```text
FaceGuide
get_lip_guides
create_controller
skinCluster
message
matrix
```

API 页面会保留真实 Python 名称，因此搜索方法名通常是最快的入口。
