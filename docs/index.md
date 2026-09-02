# MuziTools

面向 **Autodesk Maya 2023** 的绑定工具集与 Rigging Framework。

当前架构版本：**0.4.0**。

MuziTools 把使用流程、Rig System 和 UI Design System 分开维护：

- **用户手册**：从“我想完成什么”开始；
- **架构文档**：说明 `core / tools / systems / ui / app`；
- **Rig 架构**：`RigBase / ModuleBase / CtrlBase`；
- **UI Design System**：统一所有 PySide 工具；
- **API Reference**：查看真实 Python 文件、类、方法和参数。

<div class="grid cards" markdown>

-   :material-rocket-launch-outline:{ .lg .middle } **开始使用**

    ---

    安装 MuziTools，在 Maya 中启动主工具箱，并确认脚本路径。

    [:octicons-arrow-right-24: 安装与启动](getting-started/installation.md)

-   :material-tools:{ .lg .middle } **常用工具**

    ---

    从命名、属性、约束、控制器、Joint、Skin 等日常任务开始。

    [:octicons-arrow-right-24: 浏览常用工具](manual/tools.md)

-   :material-face-recognition:{ .lg .middle } **Face Rig**

    ---

    Setup → Guide → Module Build → Finalize。

    [:octicons-arrow-right-24: Face Guide](manual/face-guide.md)

-   :material-code-braces:{ .lg .middle } **架构**

    ---

    RigBase Naming、Module Lifecycle、CtrlBase Controller Workflow。

    [:octicons-arrow-right-24: 总体架构](architecture/index.md)

-   :material-view-dashboard-outline:{ .lg .middle } **UI Design System**

    ---

    MuziTools 统一 Theme、Card、Sidebar、Button 和 Widget 规范。

    [:octicons-arrow-right-24: UI 规范](development/ui-design.md)

-   :material-code-braces:{ .lg .middle } **API Reference**

    ---

    正式 Runtime Python 文件的自动生成 API 页面。

    [:octicons-arrow-right-24: 打开 API Reference](reference/index.md)

</div>

## 打开 MuziTools

```python
import muziToolset

muziToolset.show()
```

## 0.4 Rig 架构

```text
systems/rig_base.py
    Rig Naming

systems/module_base.py
    Module Lifecycle

systems/ctrl_base.py
    Controller Workflow
```

完整业务单元统一称为 **Module**，不再使用 Component。

旧 `core/name_utils.py`、`systems/component_base.py`、`systems/controller/` 已退出正式架构。

## Face Rig 当前流程

```text
01 Setup
    ↓
02 Guide
    ↓
03 Build Modules
    ↓
04 Finalize
```

Step 02 进入时会导入或复用 `resources/face/face_guide.ma`，提交前检查全部标准 Locator。

当前 Step 03 已接入：

```text
TeethModule
```

完整业务 Module 位于：

```text
systems/face/modules/
```

可复用算法位于：

```text
systems/face/build/
```

详见 [Face System Architecture](architecture/face-system.md) 和 [Face Workflow State](architecture/face-workflow-state.md)。

## 开发者入口

建议顺序：

1. [总体架构](architecture/index.md)
2. [Core 设计](architecture/core.md)
3. [Tools 与 Systems](architecture/tools-systems.md)
4. [Face System Architecture](architecture/face-system.md)
5. [测试](development/testing.md)
6. [API Reference](reference/index.md)

## 文档搜索

建议搜索真实 Python 名称：

```text
RigBase
ModuleBase
RigModuleBase
ctrl_base
FaceGuide
TeethModule
build_teeth
create_follow
matrix
```
