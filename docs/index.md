# MuziTools

面向 **Autodesk Maya 2023** 的绑定工具集与 Rigging Framework。

MuziTools 现在把使用流程、Rig System 和 UI Design System 分开维护：

- **用户手册**：从“我想完成什么”开始；
- **架构文档**：说明 `core / tools / systems / ui / app` 和 Face 四步 Workflow；
- **UI Design System**：统一所有 PySide 工具的视觉和交互；
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

    Setup → Guide → Build → Finalize。Guide 支持自动加载、完整性检查、修复、镜像和撤销。

    [:octicons-arrow-right-24: Face Guide](manual/face-guide.md)

-   :material-view-dashboard-outline:{ .lg .middle } **UI Design System**

    ---

    Arc-inspired 的 MuziTools 统一 Theme、Card、Sidebar、Button 和 Widget 规范。

    [:octicons-arrow-right-24: UI 规范](development/ui-design.md)

-   :material-code-braces:{ .lg .middle } **API Reference**

    ---

    每一个正式 Runtime Python 文件都有独立 API 页面。

    [:octicons-arrow-right-24: 打开 API Reference](reference/index.md)

</div>

## 打开 MuziTools

```python
import muziToolset

muziToolset.show()
```

第一次运行先看 [在 Maya 中运行](getting-started/maya-usage.md)。

## Face Rig 当前流程

```text
01 Setup
    ↓
02 Guide
    ↓
03 Build
    ↓
04 Finalize
```

Step 02 进入时会自动导入或复用 `resources/face/face_guide.ma`。

点击下一步之前会以 Template Contract 检查**全部标准 Locator**；任意 Locator 被误删都会阻止进入 Step 03，并列出缺失名称。

如果 Guide 被误删：

```text
重新导入模板
    ↓
记录仍存在 Locator 位置
    ↓
恢复完整模板
    ↓
已有 Locator 吸附回原位置
    ↓
缺失 Locator 使用模板默认位置
```

详见 [Face Guide](manual/face-guide.md) 和 [Face System Architecture](architecture/face-system.md)。

## UI 方向

所有正式 PySide UI 统一由：

```text
ui/theme.py
ui/widgets/
```

管理。

当前信息设计参考 Arc Browser 的 clean / calm / sidebar-first 思路，但 MuziTools 保留自己的品牌、配色 Token、Maya 工作流和组件，不复制外部产品的 Logo、图标或品牌素材。

详见 [UI Design System](development/ui-design.md)。

## 开发者入口

建议顺序：

1. [总体架构](architecture/index.md)
2. [Face System Architecture](architecture/face-system.md)
3. [UI Design System](development/ui-design.md)
4. [文档维护](development/documentation.md)
5. [API Reference](reference/index.md)
6. [测试](development/testing.md)

## 文档搜索

建议直接搜索真实 Python 名称：

```text
FaceGuide
get_lip_guides
validate_guides
reimport_guide
mirror_guides
create_controller
skinCluster
matrix
```
