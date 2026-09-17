# MuziTools

面向 **Autodesk Maya 2023** 的绑定工具集与 Rigging Framework。

当前架构版本：**0.4.0**。

这个网站是 MuziTools 的统一项目文档入口。你可以从这里总览整个仓库，也可以继续进入用户手册、系统架构、Face Rig Workflow、开发规范和完整 API Reference。

<div class="grid cards" markdown>

-   :material-view-dashboard-outline:{ .lg .middle } **项目总览**

    ---

    查看 `app / core / systems / tools / ui` 的职责、调用方向和项目结构。

    [:octicons-arrow-right-24: 查看总体架构](architecture/index.md)

-   :material-book-open-page-variant-outline:{ .lg .middle } **用户手册**

    ---

    从“我要完成什么”出发，查看安装、常用工具、Controller、Jnt、Skin、Face Rig 等工作流。

    [:octicons-arrow-right-24: 打开用户手册](manual/index.md)

-   :material-code-braces:{ .lg .middle } **完整 API Reference**

    ---

    自动扫描正式 Runtime Python 文件，并为公开 Function / Class / Method 生成独立参考文档。

    [:octicons-arrow-right-24: 浏览全部 API](reference/index.md)

-   :material-face-recognition:{ .lg .middle } **Face Rig**

    ---

    查看 Setup → Guide → Module Build → Finalize 的面部绑定工作流和当前模块实现。

    [:octicons-arrow-right-24: Face System](architecture/face-system.md)

-   :material-tools:{ .lg .middle } **绑定工具**

    ---

    浏览命名、属性、约束、控制器、Jnt、Skin、BlendShape、清理和 Rig 工具。

    [:octicons-arrow-right-24: 常用工具工作流](manual/tools.md)

-   :material-view-dashboard-variant-outline:{ .lg .middle } **UI Design System**

    ---

    查看 MuziTools 的统一 PySide Window、Theme、Card、Sidebar、Button 和 Widget 规范。

    [:octicons-arrow-right-24: UI 设计规范](development/ui-design.md)

</div>

## 项目一览

MuziTools 当前正式 Runtime 代码按照职责分成五层：

| 目录 | 定位 | 主要内容 |
| --- | --- | --- |
| `app/` | 应用入口层 | 主工具箱、窗口管理、应用启动 |
| `core/` | Maya 通用底层层 | 命名、属性、层级、Transform、Controller、Jnt 等可复用能力 |
| `systems/` | Rig System 层 | 完整、可重复构建的 Rig Module / Workflow |
| `tools/` | 工具层 | 绑定师直接操作的工具和参数收集 UI |
| `ui/` | 公共 UI 层 | Theme、Window、Widget 和统一视觉组件 |

推荐的依赖方向：

```text
app
 ↓
tools / systems
 ↓
core

ui 作为公共界面能力被 app / tools / systems 使用
```

完整设计原则见 [总体架构](architecture/index.md)。

## 源码结构

```text
muziToolset/
├── app/                 # 主应用与工具箱
├── core/                # Maya 通用底层能力
│   ├── common/          # 通用属性 / 层级 / 命名 / Transform
│   ├── rigging/         # Controller / Guide / Jnt 基础能力
│   └── bake/            # 旧版兼容与历史工具
├── systems/             # 完整 Rig System / Module
│   ├── face/            # Face Rig 模块
│   ├── rig/             # Rig Library / Modular Rig
│   ├── body/            # Body Rig
│   └── components/      # 可复用 Rig Component
├── tools/               # 绑定师直接使用的小工具
├── ui/                  # 公共 PySide UI
├── resources/           # Shape / Face Guide / 资源文件
├── scripts/             # 文档、迁移、审计和维护脚本
├── tests/               # 静态契约与文档测试
└── docs/                # 当前文档网站源码
```

## API 文档覆盖范围

网站会自动扫描以下正式 Runtime Python 文件：

```text
__init__.py
config.py
app/**/*.py
core/**/*.py
systems/**/*.py
tools/**/*.py
ui/**/*.py
```

每个正式 Python 文件都有独立 API 页面。公开 API 会继续展开到：

```text
Module
  ├── Functions
  └── Classes
       ├── __init__
       └── Public Methods
```

每一个 Function / Method 页面包含：

```text
作用
适用场景
Signature
参数
参数类型
默认值
返回值
异常
示例
Notes
源码位置
```

生成过程使用 Python AST，不 Import Maya，因此 GitHub Actions 可以安全生成整套 API Reference。

[:octicons-arrow-right-24: 打开 API 总览](reference/index.md)

## Face Rig 当前流程

MuziTools Face Rig 使用明确的阶段式 Workflow：

```text
01 Setup
    ↓
02 Guide
    ↓
03 Build Modules
    ↓
04 Finalize
```

当前 Face 相关代码主要位于：

```text
systems/face/
tools/face/
resources/face/
```

其中正式业务模块负责 Joint、Controller、Hierarchy、Connection 和可重复 Build；Guide 配置负责标准 Locator 语义；最终连接阶段负责把前面生成的结果组合成稳定的动画驱动结构。

当前 Eye Rig 已采用独立的 Ball / Iris / Aim Guide 语义，并提供 Main Ctrl、Aim Ctrl、Pose Driver / Pose Driven 和最终 Eye Joint 的连接结构。

详细说明：

- [Face System Architecture](architecture/face-system.md)
- [Face Workflow State](architecture/face-workflow-state.md)
- [Face Guide](manual/face-guide.md)
- [Face API](reference/systems/face/package.md)

## 常用开发入口

如果你正在修改代码，推荐从下面的位置进入：

| 想做的事 | 推荐入口 |
| --- | --- |
| 查一个方法怎么调用 | [API Reference](reference/index.md) |
| 理解项目结构 | [总体架构](architecture/index.md) |
| 修改 Core | [Core 设计](architecture/core.md) |
| 新增 Tool / System | [Tools 与 Systems](architecture/tools-systems.md) |
| 修改 Face Rig | [Face System](architecture/face-system.md) |
| 修改 UI | [UI Design System](development/ui-design.md) |
| 增加或修改测试 | [测试规范](development/testing.md) |
| 维护网站文档 | [文档维护](development/documentation.md) |

## 在 Maya 中打开 MuziTools

```python
import muziToolset

muziToolset.show()
```

## 如何快速查代码

如果你已经知道类名、方法名或文件名，直接使用网站顶部搜索框。例如：

```text
RigModule
EyeModule
connect_rig
create_ctrl
create_joint
get_guides
library_service
name_utils
matrix
```

如果你只知道自己想完成的任务，先从 [用户手册](manual/index.md) 开始；如果你已经在修改源码，则直接进入 [API Reference](reference/index.md)。

## 文档如何保持同步

文档网站和源码绑定在一起维护：

```text
修改 Runtime 源码
    ↓
补充 / 更新中文 Docstring
    ↓
GitHub Actions 静态检查
    ↓
AST 重新生成 API Reference
    ↓
MkDocs strict build
    ↓
GitHub Pages 发布
```

因此公开 API 的参数、返回值、异常和说明以源码 Docstring 为第一事实来源，网站不会再单独维护另一份容易过时的 API 描述。
