# muziToolset

面向 **Autodesk Maya 2023** 的 Rigging Toolset 与可扩展绑定框架。

正式 Python Package：

```python
import muziToolset
```

项目显示名称使用 **MuziTools**；源码根包始终使用 `muziToolset`。

---

# 快速开始

把 `muziToolset` 放到 Maya Python 可以访问的位置后，在 Maya Python Script Editor 中运行：

```python
import muziToolset
window = muziToolset.show()
```

第一次使用：

- [安装与启动](docs/getting-started/installation.md)
- [在 Maya 中运行](docs/getting-started/maya-usage.md)

在线文档：<https://muzimuzi.github.io/muziToolset/>

---

# 当前架构

```text
core     Maya 通用底层能力
tools    用户直接操作的小工具 / UI
systems  可复用 Rig Component / Workflow
ui       通用 PySide Theme / Widget
app      主程序和窗口生命周期
```

Face Rig 已采用正式四步 Package：

```text
systems/face/
├── setup/       # 01 Setup
├── guide/       # 02 Guide
├── build/       # 03 Build
├── finalize/    # 04 Finalize
├── data/        # Face 公共数据
├── ui/          # Face Wizard
├── face_base.py
└── config.py
```

详细说明：

- [总体架构](docs/architecture/index.md)
- [Face System Architecture](docs/architecture/face-system.md)
- [Core 设计](docs/architecture/core.md)
- [Tools 与 Systems](docs/architecture/tools-systems.md)

---

# Face Rig

当前工作流：

```text
01 Setup
    ↓
02 Guide
    ↓
03 Build
    ↓
04 Finalize
```

Step 02 会自动导入或复用 `resources/face/face_guide.ma`。

点击“下一步”时会检查 Template 中的**全部标准 Locator**。如果绑定师误删定位器，会阻止进入 Step 03，并列出缺失名称。

Step 02 还提供：

```text
重新导入模板
    保留现有 Locator 位置并补回缺失 Locator

LF → RT / RT → LF
    一次性镜像，不建立永久左右连接

撤销上次镜像
    同时支持 Maya Ctrl + Z

Controller Settings
    Size 使用 1 位小数 QDoubleSpinBox
    LF = 6 蓝 / RT = 13 红 / MD = 17 黄
```

详见：[Face Guide](docs/manual/face-guide.md)。

---

# UI Design System

项目正式 UI 统一使用：

```text
ui/theme.py
ui/widgets/
```

当前视觉方向参考 Arc Browser 的 **clean / calm / sidebar-first** 信息组织：柔和背景、轻量边框、浮层 Card、明确主次操作和稳定 Sidebar。

这里借鉴的是布局和交互原则，MuziTools 保留自己的品牌、Maya 工作流和 Theme Token，不复制 Arc 的 Logo、专有图标或品牌素材。

详见：[MuziTools UI Design System](docs/development/ui-design.md)。

---

# 文档导航

## 用户手册

- [MuziTools 用户手册](docs/manual/index.md)
- [常用工具工作流](docs/manual/tools.md)
- [Controller](docs/manual/controller.md)
- [Joint](docs/manual/joint.md)
- [Skin](docs/manual/skin.md)
- [BlendShape](docs/manual/blendshape.md)
- [场景清理与模型检查](docs/manual/cleanup.md)
- [完整绑定工作流](docs/manual/rigging.md)
- [Face Guide](docs/manual/face-guide.md)

## 开发指南

- [UI Design System](docs/development/ui-design.md)
- [文档维护与 Docstring 规范](docs/development/documentation.md)
- [Core 编码规范](docs/development/core-style-guide.md)
- [测试](docs/development/testing.md)

## API Reference

- [API Reference 说明](docs/reference/index.md)

AST Generator 会为正式 Runtime Python 文件自动生成 API 页面：

```text
__init__.py
config.py
app/**/*.py
core/**/*.py
systems/**/*.py
tools/**/*.py
ui/**/*.py
```

源码 Docstring 是 API 文档的第一事实来源。

---

# 代码规范

正式 Runtime 继续遵守：

```text
模块 / 文件 / 函数 / 变量    snake_case
Class                       PascalCase
Side                        lf / rt / md
Maya Scene Node             [类型]_[方向]_[部位]_[功能]_[序号]
```

流程代码优先显式 `for` 循环和清晰中文注释，不为了缩短行数滥用列表推导；Maya 场景代码优先 `maya.cmds`，正式新代码不新增 PyMel。
