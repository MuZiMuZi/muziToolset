# MuziTools Architecture

`muziToolset` 根包是项目唯一的正式运行框架。

## 目录职责

```text
muziToolset/
├─ app/                    # Maya 应用入口、主工具箱、窗口生命周期
├─ ui/                     # PySide Theme 与可复用 UI Widget
├─ core/                   # 不依赖 UI 的 Maya / Python 通用底层能力
├─ tools/                  # 单功能、可独立启动的小工具
├─ systems/                # 可复用 Rig System / Builder
│  ├─ common/
│  ├─ controller/
│  ├─ body/
│  └─ face/
├─ resources/
├─ tests/
├─ docs/                   # MkDocs 手写文档 + 自动 API Reference
├─ scripts/                # 文档生成等开发脚本
├─ legacy_reference/       # 历史资料，只用于参考
├─ mkdocs.yml
├─ config.py
├─ __init__.py
└─ start.py
```

## 分层依赖

```text
app / ui
    ↓
tools
    ↓
systems
    ↓
core
```

允许同层按明确公共 API 复用，但禁止让 `core` 反向 import `tools / systems / ui / app`。

---

# Core

`core` 是最底层能力库，采用“**一个 Maya 领域一个 utils 模块**”的颗粒度。

允许依赖：

- `maya.cmds`
- `maya.api.OpenMaya`
- Python 标准库
- 其它职责明确的 Core 模块

禁止依赖：

- `app`
- `ui`
- `tools`
- `systems`
- `legacy_reference`
- PyMel

## 当前 Core 模块

### Animation / Scene / File

```text
animation_utils.py
    AnimCurve、Reset、Animation JSON IO

scene_utils.py
    Undo、Node、Selection、Object Set、Callback、Scene IO、FBX

file_utils.py
    Path、Directory、JSON、文件扫描
```

原来的：

```text
animation_io_utils.py -> 已合并到 animation_utils.py
scene_io_utils.py     -> 已合并到 scene_utils.py
```

这样避免同一个领域被拆成过多小文件。

### Transform / DG

```text
transform_utils.py
matrix_utils.py
connection_utils.py
constraint_utils.py
```

保持独立的原因：

- `transform_utils` 是静态 Transform 数据；
- `matrix_utils` 是 Matrix / offsetParentMatrix 网络；
- `connection_utils` 是通用 Plug 连接；
- `constraint_utils` 是 Maya 原生 Constraint。

### DAG / Attribute / Naming

```text
attrUtils.py
hierarchyUtils.py
jointUtils.py
nameUtils.py
rename_utils.py
snap_utils.py
```

`nameUtils` 与 `rename_utils` 不合并：

- `nameUtils` 负责标准 Rig 名称语义；
- `rename_utils` 负责批量 Rename Tool 行为。

### Geometry / Deformer

```text
curve_utils.py
surface_utils.py
mesh_utils.py
skin_utils.py
blendshape_utils.py
control_shape_utils.py
```

Curve / Surface 保持独立，因为 Face、Ribbon 等系统会大量分别复用两类 NURBS 能力。

### Scene Quality

```text
model_check_utils.py
scene_clean_utils.py
```

两者必须分开：

- Model Check 默认尽量只读，只发现问题；
- Scene Clean 明确修改场景，并带安全保护。

## Core 编码规则

Core 函数默认遵循：

1. 接收明确参数；
2. 先验证数据和 Maya 节点；
3. 用“步骤 1 / 步骤 2 / 步骤 3”中文注释解释流程；
4. 对 Matrix、DAG、Deformer 等 Maya 特有行为解释“为什么”；
5. 返回节点、列表、数量或结果字典；
6. 不弹 UI；
7. 大型操作使用单个 Maya Undo Chunk；
8. 普通流程使用展开的 `for` 循环，不为了压缩代码滥用列表推导式；
9. 新代码不新增 PyMel。

## CamelCase 文件兼容

目前：

```text
attrUtils.py
hierarchyUtils.py
jointUtils.py
nameUtils.py
```

仍保留早期文件名，因为现有正式代码可能依赖这些 Import。

本轮已经完成它们的内部重构、详细中文注释与重复逻辑收口，但不做破坏性文件改名。
后续如统一 snake_case，应采用：

```text
新 snake_case 模块
    ↓
旧文件兼容转发
    ↓
全仓库迁移
    ↓
真机测试
    ↓
最后删除旧入口
```

---

# Systems

`systems` 实现完整且可复用的 Rig Component / Builder。

当前主要系统：

```text
systems/controller/
├─ builder.py
└─ space_blend.py

systems/body/
└─ skirt/

systems/face/
├─ face_setup.py
├─ face_guide.py
├─ curve_attachment.py
├─ eyelid/
├─ lip/
└─ wizard.py
```

完整 Face、Controller、Body、Hair、Ribbon Workflow 不允许重新塞回 Core。

---

# Tools

`tools` 负责：

- 读取 Selection / Channel Box；
- 接收用户参数；
- 显示状态与 Warning；
- 调用 Core / System；
- 提供统一 `main()` 窗口入口。

Tool 中不要复制 Core 算法。

例如：

```text
connections_tool.py
    -> core.connection_utils

control_shape_tool.py
    -> core.control_shape_utils
```

---

# UI / App

`ui` 只维护视觉和通用交互组件。

`app` 只维护主工具箱、工具发现、懒加载、Window Manager 和应用生命周期。

主工具箱统一通过 `app.window_manager` 管理窗口，不在每个 Tool 重新维护第二套全局窗口引用。

---

# 文档系统

项目已接入 MkDocs Material：

```text
源码
  ↓
Python AST 静态扫描
  ↓
docs/reference/core|tools|systems
  ↓
MkDocs Material
  ↓
GitHub Pages
```

AST 生成器不 Import Maya，因此可以在普通 GitHub Actions Linux Runner 上构建 API 文档。

API 页面第一版统一包含：

```text
功能
使用场景
API
示例
源码位置
```

重要模块再人工补充：

- 节点网络原理；
- 为什么这样设计；
- 错误用法；
- 完整 Maya 示例；
- Core / Tool / System 边界。

---

# 历史代码

`legacy_reference/` 只作为参考资料库，不属于正式运行架构。

```text
legacy_reference/
├─ bind/
├─ core/
│  └─ PIPELINE_MIGRATION.md
├─ dev/
├─ integrations/
├─ pyside/
├─ res/
└─ rigging/
```

旧 `pipelineUtils.py` 已完成拆分并删除；`legacy_reference/core/` 现在只是迁移文档目录。
需要历史算法时，应重新提取后进入新的 `core / tools / systems`，正式代码禁止直接 Import Legacy。

---

# Maya 兼容策略

当前主要目标：Maya 2023。

- UI 优先 PySide2；
- 可保留 PySide6 fallback；
- 场景操作优先 `maya.cmds`；
- 必要矩阵 / Curve 数学使用 Maya API 2.0；
- 不新增 PyMel 依赖。

## 对外启动

```python
import muziToolset
muziToolset.show()
```
