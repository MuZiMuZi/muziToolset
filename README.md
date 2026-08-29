# muziToolset

木子的 Maya Rigging Toolset。

当前项目正在整理为一个可长期维护的大型绑定工具集，主要目标是：

- Maya 2023 优先；
- PySide2 UI，保留 PySide6 fallback；
- Maya 场景操作优先 `maya.cmds`；
- 新代码不新增 PyMel 依赖；
- UI、底层功能、独立工具、完整 Rig System 分层维护；
- 历史代码只作为参考，不参与正式运行。

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
│  ├─ systems/                   # 完整绑定系统
│  │  ├─ common/
│  │  ├─ body/
│  │  └─ face/
│  ├─ resources/
│  │  ├─ icons/
│  │  └─ controller_shapes/
│  ├─ config.py
│  └─ ARCHITECTURE.md
│
├─ legacy_reference/             # 历史参考代码，不参与正式运行
├─ README.md
├─ LICENSE
└─ start.py
```

完整分层规则见：

```text
muzi_rigging/ARCHITECTURE.md
```

## 代码职责

### `muzi_rigging/core`

放通用 Maya 能力，例如属性、连接、命名、Joint、Controller、Hierarchy、权重和 Pipeline 工具。

`core` 不应该反向 import UI、Tools 或 Systems。

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

### `muzi_rigging/systems`

放完整绑定系统，例如：

- Face Rig
- Body Rig
- Limb
- Spine
- Hand
- Foot

System 的 Build 逻辑与 UI 分开维护。

### `muzi_rigging/ui`

维护统一 UI Theme 和可复用控件。

当前视觉方向参考桌面端音乐应用的清爽布局语言：浅灰背景、白色内容区域、红色强调色、左侧导航、轻边框与大量留白。

### `legacy_reference`

这里保存旧 `bind / pyside / res / rigging` 等历史实现。

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

当前正在把旧 `MuziTools / core / face` 中仍然有效的代码逐步迁入 `muzi_rigging`。

迁移原则是：先建立新实现并验证，再删除旧运行目录，避免 Maya 工具在中间版本突然不可用。
