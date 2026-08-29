# muziToolset

木子的 Maya Rigging Toolset。

项目正在整理为一个可长期维护的大型绑定工具集，当前原则：

- Maya 2023 优先；
- PySide2 UI，保留 PySide6 fallback；
- Maya 场景操作优先 `maya.cmds`；
- 新代码不新增 PyMel 依赖；
- UI、Core、独立 Tool、完整 Rig System 分层维护；
- 历史代码统一放入 `legacy_reference`，不参与正式运行。

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

## 当前正式架构

```text
muziToolset/
├─ muzi_rigging/                 # 当前正式运行代码
│  ├─ app/                       # 主工具箱、窗口管理、应用入口
│  ├─ ui/                        # Theme 与可复用 UI Widgets
│  ├─ core/                      # Maya 通用底层功能
│  ├─ tools/                     # 独立小工具
│  │  ├─ basic/
│  │  ├─ joint/
│  │  ├─ controller/
│  │  ├─ rig/
│  │  ├─ face/
│  │  ├─ skin/
│  │  ├─ blendshape/
│  │  └─ clean/
│  ├─ systems/                   # 可复用 Rig System / Builder
│  │  ├─ common/
│  │  ├─ controller/
│  │  ├─ body/
│  │  └─ face/
│  ├─ resources/
│  │  ├─ icons/
│  │  └─ controller_shapes/
│  ├─ config.py
│  └─ ARCHITECTURE.md
│
├─ legacy_reference/             # 历史参考代码，不参与正式运行
│  ├─ MuziTools/
│  ├─ bind/
│  ├─ core/
│  ├─ face/
│  ├─ pyside/
│  ├─ res/
│  └─ rigging/
│
├─ README.md
├─ LICENSE
├─ __init__.py
└─ start.py
```

完整分层规则见：

```text
muzi_rigging/ARCHITECTURE.md
```

## 代码职责

### `muzi_rigging/core`

放不依赖 UI 的 Maya 通用能力，例如：

- Attribute
- Connection
- Naming
- Joint
- Controller Shape
- Hierarchy
- Skin Weight
- BlendShape
- Scene Clean
- Model Check
- Snap

已经独立出的新模块包括：

- `control_shape_utils.py`
- `rename_utils.py`
- `snap_utils.py`
- `skin_utils.py`
- `blendshape_utils.py`
- `scene_clean_utils.py`
- `model_check_utils.py`

`core` 不应该反向 import `ui / tools / systems`。

### `muzi_rigging/tools`

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

### `muzi_rigging/systems`

放可复用的完整绑定系统和 Builder。

当前已经建立：

```text
systems/controller/
systems/face/
systems/body/skirt/
```

Controller Creator、FK Creator、IK Rig、Skirt Rig 等功能应优先调用 System API，而不是分别复制控制器创建逻辑。

完整 Body Rig System 暂时不作为当前阶段目标，后续再扩展 Arm / Leg / Spine / Hand / Foot 等系统。

### `muzi_rigging/ui`

维护统一 UI Theme 和可复用控件。

当前已经建立：

```text
ui/theme.py
ui/widgets/object_picker.py
```

子工具窗口统一交给 `app/window_manager.py` 管理。

### `legacy_reference`

这里只保存历史实现和参考代码。

根目录旧 `core/` 与 `face/` 已经退出正式运行路径，并与旧 `MuziTools / bind / pyside / res / rigging` 一起归档到这里。

正式代码禁止直接 import `legacy_reference`。需要旧功能时，先把有价值的算法重新整理成新的 Core 或 System API，再接入正式工具。

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

- `MuziTools` 退出根目录并归档；
- 正式运行代码集中到 `muzi_rigging`；
- Controller 创建统一到 `systems/controller`；
- Skirt Rig Build 逻辑进入 `systems/body/skirt`；
- Basic / Skin / BlendShape / Clean 的主要算法开始从 UI 抽到 Core；
- 根目录旧 `core / face` 已归档到 `legacy_reference`；
- 临时 `ui_theme.py` 和 `tools/ctrl` 迁移桥已经删除；
- 根目录备份、测试草稿、上传 cfg 和旧说明文档已经清理。

`muzi_rigging/` 这一层当前继续保留，用于稳定正式运行包。后续等项目完全稳定后，再考虑把 `app / ui / core / tools / systems / resources` 扁平迁移到 `muziToolset` 根包。
