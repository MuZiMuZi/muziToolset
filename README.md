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

也可以执行仓库中的：

```python
start.py
```

第一次使用建议先看：

- [安装与启动](docs/getting-started/installation.md)
- [在 Maya 中运行](docs/getting-started/maya-usage.md)

在线文档：

```text
https://muzimuzi.github.io/muziToolset/
```

---

# 文档导航

MuziTools 文档采用两层结构：

```text
用户手册
    回答“我要完成什么、应该怎么做”

API Reference
    回答“这个 Python 文件 / 类 / 方法怎么调用”
```

## 1. 用户手册

用户手册入口：

- [MuziTools 用户手册](docs/manual/index.md)
- [常用工具工作流](docs/manual/tools.md)
- [完整绑定工作流](docs/manual/rigging.md)

按任务进入：

| 我想做什么 | 文档 |
| --- | --- |
| 重命名、属性、连接、约束、吸附 | [基础工具](docs/manual/basic-tools.md) |
| 创建 / 修改 Controller | [Controller 工作流](docs/manual/controller.md) |
| 创建 / 重采样 Joint | [Joint 工作流](docs/manual/joint.md) |
| SkinCluster、Influence、权重 | [Skin 工作流](docs/manual/skin.md) |
| BlendShape、Corrective、Invert Shape | [BlendShape 工作流](docs/manual/blendshape.md) |
| 模型检查、层级清理、发布前检查 | [场景清理与模型检查](docs/manual/cleanup.md) |
| Face Setup、Guide、左右镜像 | [Face Guide](docs/manual/face-guide.md) |
| 整体角色绑定顺序 | [绑定工作流](docs/manual/rigging.md) |

推荐学习顺序：

```text
安装与启动
    ↓
基础工具
    ↓
Controller / Joint / Skin
    ↓
完整绑定工作流
    ↓
Face Rig
    ↓
架构
    ↓
API Reference
```

## 2. 架构

- [总体架构](docs/architecture/index.md)
- [Core 设计](docs/architecture/core.md)
- [Tools 与 Systems](docs/architecture/tools-systems.md)

如果你准备增加新功能，先确认它应该属于：

```text
core
    Maya 通用底层能力

tools
    用户直接打开的小工具 / UI

systems
    可复用完整 Rig Component / Workflow

ui
    通用 PySide UI 能力

app
    主程序和应用级窗口管理
```

## 3. API Reference

API 总览：

- [API Reference 说明](docs/reference/index.md)

API 页面由：

```text
scripts/generate_mkdocs_reference.py
```

使用 Python AST 自动扫描正式 Runtime 源码生成。

正式覆盖范围：

```text
__init__.py
config.py
app/**/*.py
core/**/*.py
systems/**/*.py
tools/**/*.py
ui/**/*.py
```

也就是说，**每一个正式 Python 文件都会拥有独立 API 页面**。

API 页面会展开：

```text
模块作用
常用场景
Import
API 一览
Class / Function / Method
Signature
参数
必填 / 默认值
返回值
异常
示例
Notes
源码位置
```

### 源码与 API 文档路径映射

源码目录与网站 API 目录保持一致：

```text
core/attr_utils.py
    → docs/reference/core/attr_utils.md
    → /reference/core/attr_utils/

systems/face/face_guide.py
    → docs/reference/systems/face/face_guide.md
    → /reference/systems/face/face_guide/

tools/controller/create_ctrl_tool.py
    → docs/reference/tools/controller/create_ctrl_tool.md
    → /reference/tools/controller/create_ctrl_tool/

ui/theme.py
    → docs/reference/ui/theme.md
    → /reference/ui/theme/

app/main.py
    → docs/reference/app/main.md
    → /reference/app/main/

__init__.py
    → docs/reference/package.md

config.py
    → docs/reference/config.md
```

生成页面不需要手工复制函数说明；源码 Docstring 是 API 文档第一事实来源。

## 4. 开发指南

- [文档维护与 Docstring 规范](docs/development/documentation.md)
- [Core 编码规范](docs/development/core-style-guide.md)
- [测试](docs/development/testing.md)

## 5. 迁移记录

- [Pipeline 重构](docs/migration/pipeline.md)

---

# 文档目录与网站导航

当前手写文档目录：

```text
docs/
├── index.md
│
├── getting-started/
│   ├── installation.md
│   └── maya-usage.md
│
├── manual/
│   ├── index.md
│   ├── tools.md
│   ├── basic-tools.md
│   ├── controller.md
│   ├── joint.md
│   ├── skin.md
│   ├── blendshape.md
│   ├── cleanup.md
│   ├── rigging.md
│   └── face-guide.md
│
├── architecture/
│   ├── index.md
│   ├── core.md
│   └── tools-systems.md
│
├── reference/
│   └── index.md
│       └── 其余 API 页面由 AST Generator 自动生成
│
├── development/
│   ├── documentation.md
│   ├── core-style-guide.md
│   └── testing.md
│
├── migration/
│   └── pipeline.md
│
├── stylesheets/
│   └── manual.css
│
└── SUMMARY.md
    └── 由 API Generator 自动生成完整网站导航
```

README、`docs/` 目录和网站导航使用同一套分类，避免出现三套不同的文档结构。

---

# 正式源码架构

```text
muziToolset/
├── app/                       # 主工具箱、应用入口、窗口生命周期
├── ui/                        # Theme、Window Utils、可复用 Widgets
├── core/                      # Maya 通用底层能力
├── tools/                     # 用户可直接打开的小工具
│   ├── basic/
│   ├── joint/
│   ├── controller/
│   ├── rig/
│   ├── face/
│   ├── skin/
│   ├── blendshape/
│   └── clean/
├── systems/                   # 可复用完整 Rig System / Builder
│   ├── body/
│   ├── common/
│   ├── controller/
│   └── face/
├── resources/                 # Icons、Controller Shapes、Rig Template
├── tests/                     # 静态 Gate + Maya Smoke Test
├── docs/                      # 用户手册 / 架构 / 开发文档
├── scripts/                   # AST API Generator 等开发脚本
├── legacy_reference/          # 历史参考，不参与正式运行
├── .github/workflows/docs.yml
├── mkdocs.yml
├── config.py
├── ARCHITECTURE.md
├── README.md
├── README.en.md
├── LICENSE
├── __init__.py
└── start.py
```

完整分层规则见：

- [ARCHITECTURE.md](ARCHITECTURE.md)

---

# Core

`core/` 只放不依赖 UI 的 Maya 通用能力。

主要分类：

```text
Animation / Scene / File
├── animation_utils.py
├── scene_utils.py
└── file_utils.py

Transform / DG
├── transform_utils.py
├── matrix_utils.py
├── connection_utils.py
└── constraint_utils.py

DAG / Attribute / Naming
├── attr_utils.py
├── hierarchy_utils.py
├── joint_utils.py
├── name_utils.py
├── rename_utils.py
└── snap_utils.py

Geometry / Deformer
├── curve_utils.py
├── surface_utils.py
├── mesh_utils.py
├── skin_utils.py
├── blendshape_utils.py
└── control_shape_utils.py

Scene Quality
├── model_check_utils.py
└── scene_clean_utils.py
```

正式模块统一使用 `snake_case`：

```python
from muziToolset.core import attr_utils
from muziToolset.core import hierarchy_utils
from muziToolset.core import joint_utils
from muziToolset.core import name_utils
```

旧 CamelCase Core 入口已经退出正式架构。

---

# Tools

`tools/` 是绑定师直接使用的入口。

例如：

```python
from muziToolset.tools.controller import create_ctrl_tool

window = create_ctrl_tool.main()
```

Tool 负责：

```text
UI
Selection
参数收集
用户交互
```

复杂算法不要重复写进 Tool。

先看：[常用工具工作流](docs/manual/tools.md)

---

# Systems

`systems/` 放稳定、可复用、可以重复 Build 的完整 Rig Component。

例如：

```text
systems/controller/
systems/face/
systems/body/
```

推荐关系：

```text
Tool
    ↓
System
    ↓
Core
    ↓
Maya
```

完整 Face / Controller / Body Workflow 不放回 Core。

---

# Face Rig

当前 Face Rig 推荐流程：

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
Lip / Jaw / Eyelid / Brow Builder
        ↓
Corrective / Picker / Finalize
```

用户手册：

- [Face Guide](docs/manual/face-guide.md)

主要源码：

```text
systems/face/face_base.py
systems/face/face_setup.py
systems/face/face_guide.py
systems/face/curve_attachment.py
systems/face/eyelid/builder.py
systems/face/lip/zip_builder.py
```

---

# 编程规范

项目新代码默认遵循：

- Maya 2023 优先；
- Maya Scene 操作优先 `maya.cmds`；
- 新代码不新增 PyMEL 依赖；
- UI 使用 PySide2，并保留需要的 PySide6 fallback；
- 文件、函数、方法、变量使用 `snake_case`；
- Class 使用 `PascalCase`；
- 有意义的 Maya 场景逻辑使用完整、可读的 `for` 循环；
- 不把主要业务流程压缩成列表推导式；
- 中文注释解释“步骤”和“为什么”；
- 模块头说明职责、边界和主要公开 API；
- 公开 API 使用详细 Docstring；
- Tool 不重复维护大型 Core / System 算法；
- Core 不反向 Import Tools / Systems / UI / App；
- 正式模块 Import 时不主动 reload 依赖；
- `legacy_reference/` 只能作为参考。

Docstring 规范见：

- [文档维护](docs/development/documentation.md)

---

# 测试与文档 CI

不需要 Maya 的静态检查：

```bash
python tests/core_import_style_test.py
python tests/docs_reference_generator_test.py
python tests/docs_runtime_api_coverage_test.py
python scripts/generate_mkdocs_reference.py
mkdocs build --strict
```

Docs CI 顺序：

```text
Core Import Style Gate
        ↓
API Generator Smoke Test
        ↓
Runtime API Coverage Test
        ↓
AST Generate API Reference
        ↓
mkdocs build --strict
        ↓
Upload Pages Artifact
        ↓
Deploy GitHub Pages
```

`docs_runtime_api_coverage_test.py` 会保证以后新增正式 Python 文件时不会悄悄漏掉 API 文档。

Maya 2023 真机测试仍用于验证：

```text
Scene
DG / DAG
UI
Rig Builder
真实节点连接
```

---

# 当前开发原则

- `muziToolset` 根包是唯一正式运行架构；
- 历史实现统一放入 `legacy_reference/`；
- Core、Tools、Systems、UI、App 分层维护；
- API 文档与源码自动同步；
- 用户手册按任务组织；
- README、文档路径和网站导航保持同一套结构；
- GitHub CI 负责文档覆盖、生成和严格构建；
- Maya 2023 Smoke Test 负责真实运行验证。

后续新增功能应继续沿当前分层扩展，不重新制造大型万能模块。
