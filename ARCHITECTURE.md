# Muzi Rigging Architecture

`muziToolset` 根包是当前项目唯一的正式运行框架。

## 当前目录职责

```text
muziToolset/
├─ app/                    # Maya 应用入口、主工具箱、窗口生命周期
├─ ui/                     # PySide Theme 与可复用 UI Widget
├─ core/                   # 不依赖 UI 的 Maya 通用底层能力
├─ tools/                  # 单功能、可独立启动的小工具
├─ systems/                # 可复用 Rig System / Builder
│  ├─ common/
│  ├─ controller/          # Controller Builder / Parent Space Blend
│  ├─ body/
│  │  └─ skirt/
│  └─ face/
├─ resources/
├─ tests/
├─ legacy_reference/       # 历史资料，只用于参考
├─ config.py
├─ __init__.py
└─ start.py
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

当前正式职责模块：

```text
# 基础节点 / 场景
attrUtils.py
hierarchyUtils.py
jointUtils.py
nameUtils.py
scene_utils.py
transform_utils.py
connection_utils.py
matrix_utils.py

# Rig / Geometry
animation_utils.py
constraint_utils.py
curve_utils.py
surface_utils.py
snap_utils.py
mesh_utils.py
skin_utils.py
blendshape_utils.py
control_shape_utils.py

# 文件 / 数据
file_utils.py
scene_io_utils.py
animation_io_utils.py

# 工具支持
rename_utils.py
scene_clean_utils.py
model_check_utils.py
```

旧 `pipelineUtils / controlUtils / connectionUtils / vectorUtils / fileUtils / weightsUtils / qtUtils` 等万能或重复模块已经退出正式 Core。

其中 `pipelineUtils` 已完成拆分并删除；正式替代分别位于 `core/`、`systems/controller/` 和 `systems/face/`。大型历史 Rig Workflow 只允许保留在 `legacy_reference/rigging/` 作为参考。

### systems

`systems` 实现可被多个工具复用的绑定流程和 Builder。

当前正式系统：

```text
systems/controller/
├─ builder.py
└─ space_blend.py

systems/body/skirt/

systems/face/
├─ face_setup.py
├─ face_guide.py
├─ curve_attachment.py
├─ eyelid/
├─ lip/
└─ wizard.py
```

System 允许依赖 `core`、`systems/common` 和其它明确的 System 公共 API。System Build 逻辑不要写进 PySide UI 类。

### tools

`tools` 只负责收集用户输入、显示状态、调用 Core/System，并提供统一 `main()` 入口。

Tool 中不要复制 Core 算法。例如属性连接统一调用 `core.connection_utils`，Controller Shape 编辑统一调用 `core.control_shape_utils`。

### ui

`ui` 只维护视觉和通用交互组件，不负责具体 Rig Build 算法。

### app

`app` 只负责主工具箱、工具发现与懒加载、PySide 子窗口生命周期、启动和关闭。具体 Maya Rig 算法不写进 app。

## Window Manager 规则

主工具箱统一通过 `app.window_manager` 打开工具。不要在每个工具中重新维护 `_window`、`child_windows` 或第二套窗口生命周期。

## Python 命名规范

新模块统一使用小写 `snake_case`，类使用 `PascalCase`，函数、方法、变量使用 `snake_case`。

当前仍保留的 `attrUtils.py / jointUtils.py / hierarchyUtils.py / nameUtils.py` 属于迁移中的核心公共 API，为避免一次性破坏现有调用暂不强制重命名；后续逐个建立 snake_case API 再迁移。

## 编码习惯

正式新代码默认：

- Maya 场景操作优先 `maya.cmds`；
- 不新增 PyMel 依赖；
- 普通流程使用完整 `for` 循环；
- 不为了压缩代码滥用列表推导式；
- 中文注释解释执行流程和设计原因；
- import 时不主动 reload 其它模块；
- 大型操作尽量使用一个 Maya Undo Chunk。

## 历史代码

`legacy_reference/` 只作为参考资料库，不属于正式运行架构。

```text
legacy_reference/
├─ bind/
├─ core/
│  └─ PIPELINE_MIGRATION.md
├─ dev/
├─ integrations/
│  ├─ advanced_skeleton.py
│  ├─ metahuman.py
│  └─ README.md
├─ pyside/
├─ res/
└─ rigging/
```

旧 `legacy_reference/face/`、旧 `MuziTools/` 和旧 `pipelineUtils.py` 都已经完成迁移后删除。

`legacy_reference/core/` 现在只是文档目录，不是 Python Package。旧 Controller 中剩余 Ribbon / IK Spine / IK Curve Rig 等大型流程放在 `legacy_reference/rigging/controlUtils.py`；第三方 AdvancedSkeleton / MetaHuman 参考位于 `legacy_reference/integrations/`。

需要旧功能时，应重新提取有价值的算法并按职责进入新的 `core / tools / systems`，而不是让正式代码直接调用历史包。

## Maya 兼容策略

当前主要目标：Maya 2023。

- UI 优先 PySide2；
- 可保留 PySide6 fallback；
- Maya 场景操作优先 `maya.cmds`；
- 新代码不新增 PyMel 依赖。

## 对外启动方式

```python
import muziToolset
muziToolset.show()
```

正式代码内部使用包内相对 import，不再依赖额外中间包。
