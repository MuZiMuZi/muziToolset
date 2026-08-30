# MuziTools Architecture

`muziToolset` 根包是项目唯一的正式运行框架。

## 目录职责

```text
muziToolset/
├─ app/                    # Maya 应用入口、主工具箱、窗口生命周期
├─ ui/                     # PySide Theme、窗口辅助与可复用 UI Widget
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

### DAG / Attribute / Naming / Config

正式模块统一使用 snake_case：

```text
attr_utils.py
config_utils.py
hierarchy_utils.py
joint_utils.py
name_utils.py
rename_utils.py
snap_utils.py
```

`config_utils.ConfigNode` 负责通用 Maya `network` Config Node 的生命周期、Message 引用和普通 Value 配置。
Face / Body / Hand 等 System 不应重复实现一套 Config CRUD。

`name_utils` 与 `rename_utils` 不合并：

- `name_utils` 负责标准 Rig 名称语义；
- `rename_utils` 负责批量 Rename Tool 行为和通用 DAG Short Name 查询。

正式代码统一使用：

```python
from muziToolset.core import attr_utils
from muziToolset.core import config_utils
from muziToolset.core import hierarchy_utils
from muziToolset.core import joint_utils
from muziToolset.core import name_utils
from muziToolset.core import rename_utils
```

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
9. 新代码不新增 PyMel；
10. 文件名、模块变量和函数统一使用 snake_case，Class 使用 PascalCase；
11. 已经存在于 Core 的基础能力禁止在 Tool / System 中复制第二套实现。

## CamelCase Core 迁移完成

以下早期兼容入口已经完成全仓库迁移并从正式 Core 删除：

```text
attrUtils.py        -> attr_utils.py
hierarchyUtils.py   -> hierarchy_utils.py
jointUtils.py       -> joint_utils.py
nameUtils.py        -> name_utils.py
```

正式源码现在只维护 snake_case 实现，不再存在第二套 Compatibility Shim。

为防止旧入口重新进入正式代码，GitHub Actions 会执行：

```bash
python tests/core_import_style_test.py
```

该测试使用 Python AST 扫描 `app / ui / core / tools / systems / tests`，不需要 Maya。
如果正式代码重新引用已退休的 CamelCase Core 模块，CI 会直接失败。

本次迁移遵循并已经完成：

```text
创建正式 snake_case 模块
    ↓
旧文件兼容转发
    ↓
全仓库正式代码迁移
    ↓
Maya 真机 Smoke Test
    ↓
CI Import Gate 归零
    ↓
删除旧兼容入口
```

---

# Systems

`systems` 实现完整且可复用的 Rig Component / Builder。

当前主要系统：

```text
systems/common/
└─ step_base.py

systems/controller/
├─ builder.py
└─ space_blend.py

systems/body/
└─ skirt/

systems/face/
├─ face_base.py
├─ face_setup.py
├─ face_guide.py
├─ face_rig_ui.py
├─ curve_attachment.py
├─ eyelid/
└─ lip/
```

完整 Face、Controller、Body、Hair、Ribbon Workflow 不允许重新塞回 Core。

## Step 生命周期规范

凡是“按步骤提交、可以回退修改并重新执行”的 System Step，统一继承：

```python
from muziToolset.systems.common import StepBase
```

生命周期固定为：

```text
collect_inputs()
      ↓
prepare_data()
      ↓
process_data()
      ↓
finalize_step()
```

统一总入口为：

```python
run_step()
```

四个阶段的固定含义：

```text
collect_inputs
    收集输入，同时完成输入规范化和有效性检查。

prepare_data
    准备层级、名称、中间数据，并清理会影响本次执行的旧结果。

process_data
    执行当前 Step 真正的核心数据或场景处理。

finalize_step
    检查输出、保存 Config、清理状态，并准备交给下一 Step。
```

不要重新拆成另一套同义顶层生命周期，例如：

```text
validate_inputs
prepare_scene
build_outputs
complete_build
```

业务内部仍然允许存在更小的辅助方法，但它们必须归属于上述四个阶段之一。

## 自定义方法调用注释规范

在生命周期大方法或其它 Workflow 大方法中，只要调用项目自己封装的 Core / System / Tool 方法，
调用前必须写一行中文注释，说明该调用在当前流程中的目的。

推荐：

```python
def prepare_data(self):
    # 确保 Face Rig 的基础层级已经创建完成。
    self.ensure_hierarchy()

    # 生成本次 Step 需要使用的 Work Model 名称。
    self.work_model_name_dict = self.get_work_model_names()

    # 删除上一次执行留下的旧 Work Model，避免旧数据冲突。
    self.delete_old_work_models(
        self.work_model_name_dict
    )
```

不推荐：

```python
def prepare_data(self):
    self.ensure_hierarchy()
    self.work_model_name_dict = self.get_work_model_names()
    self.delete_old_work_models(self.work_model_name_dict)
```

注释强调“**为什么调用**”，而不是机械重复方法名。
普通变量赋值、简单 `if / for` 和明显的 Python 基础操作不要求逐行注释，避免代码被无意义注释淹没。

---

# Tools

`tools` 负责：

- 读取 Selection / Channel Box；
- 接收用户参数；
- 显示状态与 Warning；
- 调用 Core / System；
- 提供统一 `main()` 入口。

Tool 中不要复制 Core 算法。已经存在于 `core` 的 Attribute、DAG、Connection、Constraint、Rename、Animation 等算法，应直接组合 Core API。

例如：

```text
connections_tool.py
    -> core.connection_utils

control_shape_tool.py
    -> core.control_shape_utils

face_select_key_tool.py
    -> core.hierarchy_utils
```

## Tool main() 规则

Tool 分两类，不要为了形式统一而混淆行为。

### UI Tool

UI Tool 的 `main()` 必须直接显示并返回 QWidget / QDialog：

```python
def main():
    return window_utils.show_window(
        "tools.basic.rename_tool",
        RenameTool
    )
```

`ui.window_utils` 负责用户在 Maya Script Editor 直接运行 Tool 时的：

- Python 强引用；
- `show()`；
- 最小化恢复；
- `raise_()`；
- `activateWindow()`；
- 同 Key 单实例。

### 执行型 Tool

例如 Quick Snap、根据 Selection 直接创建 FK Controller 这一类 Tool，`main()` 本身就是一次操作，不创建 QWidget，因此不要强行套 `window_utils`。

当前 UI Tool Direct Main 已通过 Maya 2023 真机 Smoke Test：

```text
Total: 17 | Passed: 17 | Failed: 0
```

---

# UI / App

`ui` 维护视觉和通用 UI 能力：

```text
theme.py
widgets/
window_utils.py
```

`app` 维护主工具箱、工具发现、懒加载、Window Manager 和应用生命周期。

窗口管理职责分开：

```text
ui.window_utils
    用户直接调用单个 UI Tool.main() 时，保证窗口可见且不被 Python 回收。

app.window_manager
    从 MuziTools 主工具箱打开工具时，负责 Maya Main Window Parent、Window Flags、
    应用级单实例和统一窗口生命周期。
```

Tool 不应各自再维护一套 `_window` 全局变量。

---

# 测试门槛

当前正式质量门槛分成两层。

## GitHub CI

不依赖 Maya：

```text
Core Import Style Gate
        ↓
AST API Reference Generation
        ↓
mkdocs build --strict
        ↓
GitHub Pages
```

## Maya 2023 真机 Smoke

Extended Core 已验证：

```text
attr_utils
hierarchy_utils
joint_utils
naming
model_check_utils
scene_clean_utils

Total: 6 | Passed: 6 | Failed: 0
```

Tool Window 已验证：

```text
Total: 17 | Passed: 17 | Failed: 0
```

这两类测试互相补充：CI 保证静态架构和文档不会回退，Maya Smoke 保证真实 Maya 行为可运行。

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
