# Muzi Rigging Architecture

`muziToolset` 根包是当前项目唯一的正式运行框架。

不再保留额外的 `muzi_rigging/` 中间包。

## 当前目录职责

```text
muziToolset/
├─ app/                    # Maya 应用入口、主工具箱、窗口生命周期
├─ ui/                     # PySide Theme 与可复用 UI Widget
├─ core/                   # 不依赖 UI 的 Maya 通用底层能力
├─ tools/                  # 单功能、可独立启动的小工具
├─ systems/                # 可复用 Rig System / Builder
│  ├─ common/              # 系统级共享能力
│  ├─ controller/          # 统一 Controller Builder
│  ├─ body/
│  │  └─ skirt/            # 当前已迁移的 Skirt Rig Builder
│  └─ face/                # Face Rig System
├─ resources/              # 图标、Controller Shape 等静态资源
├─ legacy_reference/       # 历史代码，只用于参考
├─ config.py               # 根包路径和资源配置
├─ __init__.py             # 对外 show()/initialize() 入口
└─ start.py                # Maya 快速启动脚本
```

## 分层依赖规则

### core

`core` 是最底层 Maya 功能库。

允许：

- `maya.cmds`
- `maya.api.OpenMaya`
- Python 标准库
- 必要的 core 内部模块调用

禁止：

- import app
- import tools
- import systems
- import 具体 PySide 工具窗口
- import legacy_reference

Core 函数应该尽量：

1. 接收明确参数；
2. 校验 Maya 节点；
3. 完成单一场景操作；
4. 返回节点、列表或结果字典；
5. 不创建工具窗口。

当前正式职责模块包括：

```text
attrUtils.py
jointUtils.py
hierarchyUtils.py
nameUtils.py
control_shape_utils.py
rename_utils.py
snap_utils.py
skin_utils.py
blendshape_utils.py
scene_clean_utils.py
model_check_utils.py
mesh_utils.py
```

旧 `controlUtils / pipelineUtils / weightsUtils / qtUtils / snapUtils` 等重复模块已经退出正式 Core，原版保存在 `legacy_reference/core`。

### systems

`systems` 实现可以被多个工具复用的绑定流程和 Builder。

当前正式系统：

```text
systems/controller/
systems/body/skirt/
systems/face/
```

例如 Controller Creator、FK、IK 和 Skirt Rig 不应该各自维护一套 Controller 创建算法，而应该通过包内 System API 调用：

```python
from ...systems import controller
```

System 允许依赖：

- core
- systems/common
- 其它明确的 System 公共 API

System Build 逻辑不要写进 PySide UI 类。

完整 Body Rig System 暂缓，后续再扩展 Arm / Leg / Spine / Hand / Foot。

### tools

`tools` 是用户直接点击的小工具。

职责：

- 收集用户输入；
- 显示状态和错误；
- 调用 Core；
- 调用 System 公共 API；
- 提供统一 `main()` 入口。

推荐结构：

```python
def main():
    window = SomeTool()
    return window
```

窗口不要自己维护第二套全局引用，统一交给 `app.window_manager`。

### ui

`ui` 只维护视觉和通用交互组件。

当前包括：

```text
ui/theme.py
ui/widgets/object_picker.py
```

UI Widget 不负责具体 Rig Build 算法。

### app

`app` 是最外层应用层，只负责：

- 主工具箱；
- 工具发现与懒加载；
- PySide 子窗口生命周期；
- 启动和关闭。

具体 Maya Rig 算法不写在 app 中。

## Window Manager 规则

主工具箱通过包内 Window Manager 统一打开工具：

```python
from . import window_manager

window_manager.show_tool(
    "category/tool_key",
    tool_module.main
)
```

不要在每个工具中重新维护 `_window`、`child_windows`、`setParent(Qt.Window)` 等窗口生命周期代码。

## Python 命名规范

新模块统一使用小写 `snake_case`：

```text
controller/
blendshape/
attr_utils.py
joint_utils.py
window_manager.py
```

类使用 `PascalCase`。

函数、方法、变量使用 `snake_case`。

当前仍保留的 `attrUtils.py / jointUtils.py / hierarchyUtils.py / nameUtils.py` 属于迁移中的核心公共 API，为避免一次性破坏现有调用暂不强制重命名；后续可以逐个建立 snake_case API 后再迁移。

## 编码习惯

正式新代码默认：

- Maya 场景操作优先 `maya.cmds`；
- 不新增 PyMel 依赖；
- 普通流程使用完整 `for` 循环；
- 不为了压缩代码滥用列表推导式；
- 中文注释解释执行流程和设计原因；
- 正式模块 import 时不主动 reload 其它模块；
- 大型操作尽量使用一个 Maya Undo Chunk。

## 历史代码

`legacy_reference/` 只作为参考资料库。

当前包含旧：

```text
MuziTools/
bind/
core/
face/
pyside/
res/
rigging/
dev/
```

需要旧功能时，应重新提取有价值的算法并按职责进入新的 `core / tools / systems`，而不是让正式代码直接调用历史包。

## Maya 兼容策略

当前主要目标：Maya 2023。

- UI 优先 PySide2；
- 可保留 PySide6 fallback；
- Maya 场景操作优先 `maya.cmds`；
- 新代码不新增 PyMel 依赖。

## 对外启动方式

唯一推荐启动方式：

```python
import muziToolset
muziToolset.show()
```

正式代码内部使用包内相对 import，不再依赖 `muzi_rigging` 包名。
