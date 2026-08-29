# muziToolset

木子的 Maya Rigging Toolset。

当前项目正在整理为一个可长期维护的大型绑定工具集，主要目标是：

- Maya 2023 优先；
- PySide2 UI，保留 PySide6 fallback；
- Maya 场景操作优先 `maya.cmds`；
- 新代码不新增 PyMel 依赖；
- UI、底层功能、独立工具、完整 Rig System 分层维护；
- 历史代码逐步退出正式运行路径。

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
├─ core/                         # 旧 Face Rig 仍依赖的临时兼容 Core
├─ face/                         # 尚未完成新 Face System 提取的旧 Face Rig
├─ legacy_reference/             # 已退出运行路径的历史参考代码
├─ README.md
├─ LICENSE
└─ start.py
```

完整分层规则见：

```text
muzi_rigging/ARCHITECTURE.md
```

## 过渡目录说明

仓库根目录的 `core/` 与 `face/` **暂时保留**。

当前旧 `face/` 中仍有类似下面的相对依赖：

```python
from ..core import hierarchyUtils
from ..core import pipelineUtils
from ..core import nameUtils
```

因此在新的 Face System 尚未提取完成之前，不应只移动或删除根目录 `core/`。正确迁移顺序是：

1. 把旧 Face Rig 中仍有价值的算法提取到 `muzi_rigging/systems/face` 和 `muzi_rigging/core`；
2. 让新的 Face Tool / Face System 不再依赖根目录 `face/` 与 `core/`；
3. 验证 Maya 中的新 Face Rig 工作流；
4. 再把根目录 `face/` 与 `core/` 归档到 `legacy_reference/`。

这两个目录属于同一批迁移依赖，不应该拆开归档。

## 代码职责

### `muzi_rigging/core`

放通用 Maya 能力，例如属性、连接、命名、Joint、Controller、Hierarchy、权重和 Pipeline 工具。

`core` 不应该反向 import UI、Tools 或 Systems。

当前已经独立出的正式模块包括：

- `control_shape_utils.py`
- `rename_utils.py`
- `snap_utils.py`
- `skin_utils.py`
- `blendshape_utils.py`
- `scene_clean_utils.py`
- `model_check_utils.py`

### `muzi_rigging/tools`

放可以独立打开的小工具，例如：

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

工具文件负责 UI、参数收集和用户入口，不应该重复维护大型 Rig 算法。

### `muzi_rigging/systems`

放可复用的绑定系统和 Builder。

当前已经建立统一 `Controller System`，Controller Creator、FK Creator 和专项 Rig Tool 应优先调用这一层，而不是分别复制控制器创建代码。

完整 Body Rig System 暂未作为当前迁移阶段的强制目标，可以在基础工具和 Face System 稳定后继续扩展。

### `muzi_rigging/ui`

维护统一 UI Theme 和可复用控件。

旧的 `muzi_rigging/ui_theme.py` 迁移桥已经删除；正式工具直接 import `muzi_rigging.ui.theme`。

### `legacy_reference`

这里保存已经退出正式运行路径的旧 `MuziTools / bind / pyside / res / rigging` 等历史实现。

正式代码禁止直接 import 这些目录。需要旧功能时，把有价值的算法重新整理后迁入正式架构。

## 编程规范

项目新代码默认遵循：

- 使用完整、可读的 `for` 循环，不写压缩式循环；
- 函数、方法、变量使用 `snake_case`；
- 类使用 `PascalCase`；
- Maya 节点命名可以继续使用 `ctrl_ / jnt_ / grp_` 等绑定命名约定；
- 中文注释重点解释执行流程和设计原因；
- UI 不直接堆积复杂 Rig 算法；
- 正式模块 import 时不主动 reload 依赖；
- 子工具窗口统一交给 Window Manager 管理。

## 开发状态

目前 Controller、Basic、Skin、BlendShape、Clean 等新工具正在逐步完成正式 Core / System 分层。

根目录旧 `core/` 与 `face/` 暂不强行移动，等新的 Face System 完整提取并验证后再一起归档，避免 Maya 中现有 Face Rig 工作流在迁移中断裂。
