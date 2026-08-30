# muziToolset

木子的 Maya Rigging Toolset。

`muziToolset` 根目录本身就是正式 Python Package，不再额外包一层旧运行包。

当前开发原则：

- Maya 2023 优先；
- PySide2 UI，保留 PySide6 fallback；
- Maya 场景操作优先 `maya.cmds`；
- 新代码不新增 PyMel 依赖；
- 文件、函数、变量统一使用 `snake_case`，Class 使用 `PascalCase`；
- UI、Core、独立 Tool、完整 Rig System 分层维护；
- 历史代码统一放入 `legacy_reference/`，不参与正式运行；
- Core 代码和 MkDocs 文档同步维护；
- GitHub CI 负责静态架构、API 文档和 Pages 构建；
- Maya 2023 Smoke Test 负责真实 Scene / DG / DAG / UI 验证。

## 启动

把 `muziToolset` 放到 Maya Python 可以访问的位置后，在 Maya Python Script Editor 中运行：

```python
import muziToolset

window = muziToolset.show()
```

也可以执行仓库中的：

```python
start.py
```

## 在线文档

MkDocs Material 文档站：

```text
https://muzimuzi.github.io/muziToolset/
```

文档包括：

```text
快速开始
架构设计
Core API 使用手册
自动 API Reference
开发规范
测试说明
迁移记录
```

API Reference 使用 Python AST 从源码自动生成，不需要在 GitHub Actions 中安装 Maya。

## 正式架构

```text
muziToolset/
├─ app/                       # 主工具箱、应用级窗口管理、应用入口
├─ ui/                        # Theme、Window Utils 与可复用 UI Widgets
├─ core/                      # Maya 通用底层功能
├─ tools/                     # 独立小工具
│  ├─ basic/
│  ├─ joint/
│  ├─ controller/
│  ├─ rig/
│  ├─ face/
│  ├─ skin/
│  ├─ blendshape/
│  └─ clean/
├─ systems/                   # 可复用 Rig System / Builder
├─ resources/
│  ├─ icons/
│  └─ controller_shapes/
├─ tests/                     # Maya Smoke + 静态架构 Gate
├─ docs/                      # MkDocs 手写文档
├─ scripts/                   # AST API 文档生成器等开发脚本
├─ legacy_reference/          # 历史参考代码，不参与正式运行
├─ .github/workflows/docs.yml
├─ mkdocs.yml
├─ config.py
├─ ARCHITECTURE.md
├─ README.md
├─ README.en.md
├─ LICENSE
├─ __init__.py
└─ start.py
```

完整分层规则见：

```text
ARCHITECTURE.md
```

## `core/`

Core 放不依赖 UI 的 Maya 通用能力。

当前正式模块统一使用 snake_case：

```text
Animation / Scene / File
├─ animation_utils.py
├─ scene_utils.py
└─ file_utils.py

Transform / DG
├─ transform_utils.py
├─ matrix_utils.py
├─ connection_utils.py
└─ constraint_utils.py

DAG / Attribute / Naming
├─ attr_utils.py
├─ hierarchy_utils.py
├─ joint_utils.py
├─ name_utils.py
├─ rename_utils.py
└─ snap_utils.py

Geometry / Deformer
├─ curve_utils.py
├─ surface_utils.py
├─ mesh_utils.py
├─ skin_utils.py
├─ blendshape_utils.py
└─ control_shape_utils.py

Scene Quality
├─ model_check_utils.py
└─ scene_clean_utils.py
```

早期 CamelCase Core 入口：

```text
attrUtils.py
hierarchyUtils.py
jointUtils.py
nameUtils.py
```

已经完成正式代码迁移并删除。

新代码只使用：

```python
from muziToolset.core import attr_utils
from muziToolset.core import hierarchy_utils
from muziToolset.core import joint_utils
from muziToolset.core import name_utils
```

`core` 禁止反向 Import：

```text
ui
tools
systems
app
legacy_reference
```

## `tools/`

Tools 放可以独立执行或独立打开的小工具，例如：

- Rename Tool；
- Attribute Tool；
- Constraint Tool；
- Joint Tool；
- Controller Creator；
- Skin Tool；
- BlendShape Tool；
- Model Checker。

### UI Tool

UI Tool 的 `main()` 必须在 Maya Script Editor 中直接显示并返回窗口：

```python
from muziToolset.tools.controller import create_ctrl_tool

window = create_ctrl_tool.main()
```

独立 Tool 的窗口强引用和显示统一使用：

```text
ui/window_utils.py
```

主工具箱打开子工具时仍由：

```text
app/window_manager.py
```

负责应用级 Maya Parent、Window Flags 和跨 Tool 生命周期。

### 执行型 Tool

Quick Snap、根据 Selection 直接创建 FK Controller 等 `main()` 本身就是一次操作，不创建 QWidget，因此不强行套窗口入口。

Tool 负责 UI、参数收集和用户入口，不重复维护大型 Core / Rig 算法。

## `systems/`

Systems 放可复用的完整绑定系统和 Builder。

完整 Face、Controller、Body、Hair、Ribbon Workflow 不允许重新塞回 Core。

当前系统代码继续通过稳定的 Core API 组合底层能力。

## `ui/`

维护统一 UI Theme 和可复用控件：

```text
ui/theme.py
ui/widgets/
ui/window_utils.py
```

职责：

```text
Theme
Object Picker
通用 Widget
独立 Tool Window 强引用 / 显示 / 单实例
```

具体 Maya Rig 算法不写在 UI 层。

## `app/`

只负责应用层：

- 主工具箱；
- 工具注册；
- 工具搜索；
- 应用级子窗口生命周期；
- 应用启动与关闭。

具体 Maya Rig 算法不写在 `app`。

## `resources/`

只保存正式运行需要的静态资源，例如：

- UI Icons；
- Controller Shape JSON；
- Controller Shape Preview；
- 后续 Rig Template。

## `legacy_reference/`

这里只保存历史实现和参考资料。

正式代码禁止直接 Import `legacy_reference`。
需要旧功能时，先提取有价值的算法，再进入新的 Core / Tool / System API。

## 分层依赖

推荐依赖方向：

```text
app / ui
    ↓
tools
    ↓
systems
    ↓
core
    ↓
Maya
```

禁止反向依赖：

```text
core -> tools
core -> systems
core -> app
core -> ui
systems -> tools
formal code -> legacy_reference
```

## 编程规范

项目新代码默认遵循：

- 使用完整、可读的 `for` 循环，不把 Maya 场景操作压缩成列表推导式；
- 文件、函数、方法、变量使用 `snake_case`；
- 类使用 `PascalCase`；
- Maya 节点命名可以继续使用 `ctrl_ / jnt_ / grp_` 等绑定命名约定；
- Maya 场景操作优先使用 `maya.cmds`；
- 中文注释按“步骤 1 / 步骤 2 / 为什么”解释执行流程和 Maya 特殊行为；
- 模块头列出职责、公开 API、功能简介、边界和设计原则；
- UI 不直接堆积复杂 Rig 算法；
- 正式模块 Import 时不主动 reload 依赖；
- 历史代码只能作为参考，不能从正式包直接 Import。

## 测试

### Core Import Style Gate

不需要 Maya：

```bash
python tests/core_import_style_test.py
```

检查：

```text
退休 CamelCase Core 文件不得重新出现
正式代码不得重新 Import 退休模块
```

该 Gate 已接入 GitHub Actions。

### Pipeline Smoke

Maya：

```python
import muziToolset

muziToolset.pipeline_smoke_test()
```

### Extended Core Smoke

Maya 2023 已验证：

```python
muziToolset.extended_core_smoke_test()
```

当前已记录结果：

```text
Total: 6 | Passed: 6 | Failed: 0
```

### Tool Window Smoke

Maya 2023 已验证：

```python
muziToolset.tool_window_smoke_test()
```

当前已记录结果：

```text
Total: 17 | Passed: 17 | Failed: 0
```

## 文档 CI

GitHub Actions 顺序：

```text
Core Import Style Gate
        ↓
AST Generate API Reference
        ↓
mkdocs build --strict
        ↓
Upload Pages Artifact
        ↓
Deploy GitHub Pages
```

## 当前开发状态

已经完成的主要架构迁移：

- `muziToolset` 根包成为唯一正式框架；
- 旧 `pipelineUtils.py` 完成职责拆分并删除；
- `animation_io_utils.py` 合并到 `animation_utils.py`；
- `scene_io_utils.py` 合并到 `scene_utils.py`；
- `attrUtils / hierarchyUtils / jointUtils / nameUtils` 完成 snake_case 迁移并删除；
- Controller 创建能力已从通用 Core 边界中分离；
- Basic / Skin / BlendShape / Clean 的主要算法从 UI 抽到 Core；
- UI Tool Direct Main 已统一窗口生命周期；
- Tool Window Smoke 已通过 Maya 2023 17/17；
- Extended Core Smoke 已通过 Maya 2023 6/6；
- MkDocs Material + AST API Reference + GitHub Pages 已接入。

后续新增功能应继续沿现有分层扩展，而不是重新制造大型万能模块。
