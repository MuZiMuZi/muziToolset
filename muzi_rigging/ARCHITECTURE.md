# Muzi Rigging Architecture

`muzi_rigging` 是当前项目唯一的正式运行包。

## 目录职责

```text
muzi_rigging/
├─ app/                    # Maya 应用入口、工具注册、窗口生命周期
├─ ui/                     # PySide 主题与可复用 UI 组件
├─ core/                   # Maya 通用底层能力，不包含具体工具界面
├─ tools/                  # 单功能、可独立启动的小工具
├─ systems/                # 完整绑定系统
│  ├─ common/              # 系统级共享构建能力
│  ├─ body/                # 身体绑定系统
│  └─ face/                # 面部绑定系统
├─ resources/              # 图标、控制器 Shape、模板等静态资源
├─ config.py               # 包路径、版本与全局配置
└─ __init__.py             # 对外 show()/initialize() 入口
```

## 分层依赖规则

### core

`core` 是最底层 Maya 功能库。

允许：

- maya.cmds / maya.api.OpenMaya
- Python 标准库
- core 内部模块互相调用

禁止：

- import app
- import tools
- import systems
- import 具体工具 UI

底层模块应尽量只接收参数、返回结果，不弹出工具窗口。

### systems

`systems` 用来实现完整的绑定系统，例如 Face Rig、Body Rig、Limb、Spine。

允许依赖：

- core
- systems/common

系统构建逻辑与系统 UI 分开维护。

### tools

`tools` 是用户点击后直接使用的独立工具，例如：

- Rename
- Constraint
- Joint Resample
- Controller Creator
- Skin Tool
- BlendShape Tool

工具 UI 可以调用 core，也可以启动 systems 的公开入口，但不要把通用算法写回 UI 类。

### ui

`ui` 只维护视觉系统与可复用控件。

例如：

- Theme
- Card
- Search Box
- Navigation
- Maya Object Picker
- Status Banner

UI 组件不负责具体绑定算法。

### app

`app` 是最外层应用层，只负责：

- 主工具箱
- 工具注册与发现
- PySide 窗口生命周期
- 启动与关闭

具体绑定功能不写在 app 中。

## 命名规范

Python 包和文件统一使用小写 snake_case。

推荐：

```text
controller/
blendshape/
attr_utils.py
joint_utils.py
window_manager.py
```

类使用 PascalCase，函数、方法和变量使用 snake_case。

## 历史代码

`legacy_reference/` 中的代码仅作为参考资料，不属于正式运行架构。

正式代码禁止新增对 `legacy_reference` 的 import。

需要旧功能时，应把需要的算法重新整理后迁入 `core / tools / systems`，而不是直接调用历史包。

## Maya 兼容策略

当前主要目标：Maya 2023。

- UI 优先 PySide2
- 可保留 PySide6 fallback
- Maya 场景操作优先 maya.cmds
- 新代码不新增 pymel 依赖

## 对外启动方式

最终统一为：

```python
import muzi_rigging
muzi_rigging.show()
```
