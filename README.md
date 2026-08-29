# muziToolset

木子的 Maya Rigging Toolset。

`muziToolset` 根目录本身就是正式 Python Package，不再额外包一层 `muzi_rigging/`。

当前开发原则：

- Maya 2023 优先；
- PySide2 UI，保留 PySide6 fallback；
- Maya 场景操作优先 `maya.cmds`；
- 新代码不新增 PyMel 依赖；
- UI、Core、独立 Tool、完整 Rig System 分层维护；
- 历史代码统一放入 `legacy_reference/`，不参与正式运行。

## 启动

把 `muziToolset` 放到 Maya Python 可以访问的位置后，在 Maya Python Script Editor 中运行：

```python
import muziToolset
muziToolset.show()
```

也可以执行仓库中的：

```python
start.py
```

## 正式架构

```text
muziToolset/
├─ app/                       # 主工具箱、窗口管理、应用入口
├─ ui/                        # Theme 与可复用 UI Widgets
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
│  ├─ common/
│  ├─ controller/
│  ├─ body/
│  └─ face/
├─ resources/
│  ├─ icons/
│  └─ controller_shapes/
├─ legacy_reference/         # 历史参考代码，不参与正式运行
│  ├─ MuziTools/
│  ├─ bind/
│  ├─ core/
│  ├─ dev/
│  ├─ face/
│  ├─ pyside/
│  ├─ res/
│  └─ rigging/
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

## 代码职责

### `core/`

放不依赖 UI 的 Maya 通用能力，例如：

- Attribute
- Naming
- Joint
- Controller Shape
- Hierarchy
- Skin Weight
- BlendShape
- Scene Clean
- Model Check
- Snap
- Mesh

当前正式模块包括：

- `attrUtils.py`
- `jointUtils.py`
- `hierarchyUtils.py`
- `nameUtils.py`
- `control_shape_utils.py`
- `rename_utils.py`
- `snap_utils.py`
- `skin_utils.py`
- `blendshape_utils.py`
- `scene_clean_utils.py`
- `model_check_utils.py`
- `mesh_utils.py`

`core` 不应该反向 import `ui / tools / systems / app`。

### `tools/`

放可以独立执行或独立打开的小工具，例如：

- Rename Tool
- Attribute Tool
- Constraint Tool
- Joint Tool
- Controller Creator
- Skin Tool
- BlendShape Tool
- Model Checker

每个可发现工具提供：

```python
def main():
    ...
```

主工具箱只在用户点击时才 import 对应模块。

工具文件负责 UI、参数收集和用户入口，不重复维护大型 Rig 算法。

### `systems/`

放可复用的完整绑定系统和 Builder。

当前已经建立：

```text
systems/controller/
systems/face/
systems/body/skirt/
```

Controller Creator、FK Creator、IK Rig、Skirt Rig 等功能应优先调用 System API，而不是分别复制控制器创建逻辑。

完整 Body Rig System 暂缓，后续再扩展 Arm / Leg / Spine / Hand / Foot 等系统。

### `ui/`

维护统一 UI Theme 和可复用控件。

当前包括：

```text
ui/theme.py
ui/widgets/object_picker.py
```

子工具窗口统一交给：

```text
app/window_manager.py
```

管理。

### `app/`

只负责应用层：

- 主工具箱；
- 工具注册；
- 工具搜索；
- 子窗口生命周期；
- 应用启动与关闭。

具体 Maya Rig 算法不写在 `app`。

### `resources/`

只保存正式运行需要的静态资源，例如：

- UI Icons；
- Controller Shape JSON；
- Controller Shape Preview；
- 后续 Rig Template。

### `legacy_reference/`

这里只保存历史实现和参考代码。

旧 `MuziTools / core / face / bind / pyside / res / rigging` 已经退出正式运行路径。

正式代码禁止直接 import `legacy_reference`。需要旧功能时，先把有价值的算法重新整理成新的 Core 或 System API，再接入正式工具。

## 分层依赖

推荐依赖方向：

```text
app
 ↓
tools / systems
 ↓
core
 ↓
Maya
```

`ui` 是横向公共层，只负责 Theme 与通用控件。

禁止产生这些反向依赖：

```text
core -> tools
core -> systems
core -> app
systems -> tools
legacy_reference -> 正式运行链
```

## 编程规范

项目新代码默认遵循：

- 使用完整、可读的 `for` 循环，不写压缩式循环；
- 函数、方法、变量使用 `snake_case`；
- 类使用 `PascalCase`；
- Maya 节点命名可以继续使用 `ctrl_ / jnt_ / grp_` 等绑定命名约定；
- Maya 场景操作优先使用 `maya.cmds`；
- 中文注释重点解释执行流程和设计原因；
- UI 不直接堆积复杂 Rig 算法；
- 正式模块 import 时不主动 reload 依赖；
- 子工具窗口统一交给 Window Manager 管理；
- 历史代码只能作为参考，不能从正式包直接 import。

## 当前开发状态

已经完成的主要架构迁移：

- `MuziTools` 退出正式运行路径并归档；
- 根目录旧 `core / face` 已归档到 `legacy_reference`；
- `muzi_rigging/` 中间包已经删除；
- `muziToolset` 根包成为唯一正式框架；
- Controller 创建统一到 `systems/controller`；
- Skirt Rig Build 逻辑进入 `systems/body/skirt`；
- Basic / Skin / BlendShape / Clean 的主要算法从 UI 抽到 Core；
- 临时 `ui_theme.py` 和 `tools/ctrl` 迁移桥已经删除；
- 根目录备份、测试草稿、上传 cfg 和旧说明文档已经清理。

下一阶段重点是 Maya 2023 全工具 Smoke Test，以及继续清理正式模块内部遗留的旧 API 和命名风格。
