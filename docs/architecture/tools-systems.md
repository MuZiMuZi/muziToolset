# Tools 与 Systems

MuziTools 当前把“用户直接操作的工具”和“可重复构建的 Rig 业务系统”明确分开。

这两个目录经常同时参与一个功能，但职责不同：

```text
Tool
    负责用户交互、选择、参数收集

System
    负责完整业务逻辑、Scene Build、Rebuild、Connection
```

推荐调用方向：

```text
Tool
 ↓
System
 ↓
Core
```

而不是：

```text
System -> Tool
```

---

# `tools/` 是什么

当前目录：

```text
tools/
├── basic/
├── blendshape/
├── clean/
├── controller/
├── face/
├── jnt/
├── rig/
└── skin/
```

这些目录按绑定师实际任务分类。

Tool 典型职责：

```text
读取 Selection
读取输入框 / Slider / ComboBox
检查用户输入
组织调用参数
调用 Core / System
显示结果、Warning、Error
```

Tool 可以有 UI，但不应该成为完整 Rig 算法的唯一实现位置。

---

## `tools/basic/`

处理通用日常工具，例如：

```text
Attribute
Connection
Constraint
Rename
Snap
```

这些工具适合做“立即执行的小操作”。

如果某个操作需要被多个 System 反复复用，底层逻辑应该尽量下沉到 Core。

---

## `tools/controller/`

Controller 相关用户工具。

当前主要方向包括：

```text
创建 Controller
创建 FK Controller
修改 Controller Shape
```

推荐结构：

```text
Tool UI / Selection
    ↓
core/rigging/ctrl_utils.py
    ↓
Maya Controller Scene Result
```

Tool 不应复制 `Ctrl` 类中的 Shape、Axis、Hierarchy 实现。

---

## `tools/jnt/`

Joint 相关用户工具。

例如：

```text
Joint 创建
Joint Resample
Joint 调整
```

基础 Joint 能力来自：

```text
core/rigging/jnt_utils.py
```

复杂 Rig Joint 结构则应由对应 System 创建。

---

## `tools/face/`

Face Rig 的用户入口层。

这里可以负责：

```text
打开 Face 工具
用户选择
模块触发
Step 操作
Face Controller Selection
```

但 Eye / Ear / Tongue 等模块的正式构建逻辑位于：

```text
systems/face/
```

---

## `tools/rig/`

Rig / Modular Rig 的用户入口。

当前包括：

```text
modular_rig_tool.py
rig_tool.py
skirt_ctrl_tool.py
```

Modular Rig Tool 应以调用 `systems/rig/` 和具体 Rig Module 为主，而不是把 Catalog、Builder、Connection Lifecycle 全部塞在 UI 文件中。

---

# `systems/` 是什么

当前结构：

```text
systems/
├── rig_module.py
├── face/
├── rig/
├── body/
└── components/
```

System 是“可以不依赖某个按钮也能独立执行”的业务层。

理想状态下：

```python
from muziToolset.systems.face import eye_module

eye_module.build(side="lf")
```

和通过 UI 点击“创建 Eye Rig”应该最终走同一套业务代码。

---

# `systems/rig_module.py`

这是当前模块化 Rig 的重要公共基类层。

它负责把重复的 Module 行为统一起来，例如：

```text
Guide 获取
Joint 创建入口
Controller 创建入口
Master Group
Hierarchy
Build Lifecycle
输出连接入口
```

具体模块继承后，只实现自己的业务语义。

例如：

```text
EyeModule
EarModule
TongueModule
```

都不应该重新发明一套 Module 生命周期。

API：[`systems/rig_module.py`](../reference/systems/rig_module.md)

---

# `systems/face/`

当前正式文件：

```text
ear_module.py
eye_module.py
face_guide_config.py
tongue_module.py
```

## `face_guide_config.py`

负责 Face Guide 的稳定命名和语义配置。

这类配置解决的是：

```text
某个 Guide 叫什么
属于哪一侧
属于什么功能
如何兼容旧 Locator 名称
```

它是 Face Module 与 Guide Scene 之间的重要契约。

---

## `eye_module.py`

当前 Eye Rig 已经是完整业务 Module。

它负责：

```text
Ball / Iris / Aim Guide
Eye Bind Joint
Main Controller
Aim Controller
Controller Pivot
Module Hierarchy
World Up
Pose Driver / Pose Driven
Aim Constraint
Orient Constraint
Connection Cleanup
Rebuild
Validation
```

这是典型“System 应该做什么”的例子。

详细设计见 [Face System](face-system.md)。

---

## `ear_module.py` / `tongue_module.py`

这两个模块同样属于 Face 业务层。

它们应该逐步遵循统一的 Module Lifecycle：

```text
Guide
Joint
Controller
Hierarchy
Connect
Validate
Rebuild
```

如果后续扩展 Brow / Lip / Eyelid，也应继续放在 `systems/face/`，而不是回到单一巨型 Face Script。

---

# `systems/rig/`

负责 Rig Library / Modular Rig 的系统能力。

当前主要内容：

```text
library_catalog.py
library_service.py
ui/
```

建议理解为三层：

```text
Catalog
    定义有哪些 Module / Card / Metadata

Service
    处理业务分发、Build、Rebuild、Mirror、状态

UI
    把 Catalog / Service 展示给用户
```

这比把所有逻辑塞在一个 Window Class 中更容易测试和维护。

---

# `systems/components/`

用于保存可复用 Rig Component。

当前包含 FK Chain 相关实现。

Component 适合表示：

```text
可以被多个更大 Rig System 使用
但本身已经比 Core 原子能力更完整
```

例如：

```text
FK Chain
Ribbon Segment
Generic Aim Unit
```

如果后续出现更多通用组件，可以继续扩展这里。

---

# `systems/body/`

身体绑定业务区域。

当前已经存在 Skirt Builder 相关结构。

这里与 `systems/face/` 一样，属于领域业务层：

```text
Body System
Face System
```

两者都可以共享 `core/`，但不应该互相复制基础 Helper。

---

# Tool 和 System 的边界示例

假设用户点击：

```text
Create Left Eye Rig
```

正确分层可以是：

```text
Tool / UI
    读取 side = "lf"
    读取 ctrl_shape
    读取 ctrl_size
        ↓
EyeModule / eye_module.build()
    获取 Guide
    创建 Joint
    创建 Controller
    整理 Hierarchy
    建立连接
        ↓
Core
    Name
    Ctrl
    Joint
    Hierarchy
```

错误分层是：

```text
UI Button Callback
    直接写 500 行 maya.cmds
    自己创建所有 Joint
    自己创建所有 Controller
    自己处理命名
    自己处理 Rebuild
```

这种做法会导致：

- 无法无 UI 测试；
- 无法在其他工具复用；
- Mirror / Rebuild 逻辑重复；
- UI 修改容易破坏 Rig；
- 文档也无法稳定描述 API。

---

# Rebuild 是 System 的正式职责

当前 Modular Rig 方向已经不再把 Module 当成“一次性生成”。

推荐生命周期：

```text
Guide
    ↓
Generate Joint / Controller
    ↓
用户调整 Controller / Joint
    ↓
Connect
    ↓
如果需要修改
    ↓
回退前面阶段
    ↓
Rebuild / Reconnect
```

因此 System 应该明确区分：

```text
生成节点
读取已有输出
删除连接
重新连接
完整重建
验证
```

Eye Module 当前已经开始采用这种结构：

```text
load_outputs()
delete_connections()
connect_rig()
build()
validate()
```

---

# Mirror 应该放在哪里

Mirror 不是单纯 UI 功能。

UI 可以提供按钮，但镜像真正涉及：

```text
Guide 数据
Side Name
Controller Shape / Transform
Joint
Module Metadata
Rebuild
```

因此推荐：

```text
UI 触发 Mirror
    ↓
System / Service 处理 Mirror Workflow
    ↓
Core 提供 Name / Transform 等通用能力
```

这样 Step 01～03 都可以共享同一套镜像能力。

---

# 新功能判断表

| 功能 | 推荐位置 |
| --- | --- |
| Rename Window | `tools/basic/` |
| 通用名称解析 | `core/common/name_utils.py` |
| Controller Shape 操作 | `core/rigging/ctrl_utils.py` |
| Eye Rig | `systems/face/eye_module.py` |
| Brow Rig | `systems/face/` |
| Lip Rig | `systems/face/` |
| FK Chain Component | `systems/components/` |
| Rig Library Catalog | `systems/rig/` |
| Modular Rig Window | `tools/rig/` 或 `systems/rig/ui/`（按职责拆分） |
| 公共 Object Picker | `ui/widgets/` |

---

# 依赖约束

推荐：

```text
app -> tools
app -> systems
app -> ui

tools -> systems
tools -> core
tools -> ui

systems -> core
systems -> ui（仅系统专属 UI 场景）

core -> Maya / Python
```

尽量避免：

```text
core -> systems
core -> tools
systems -> tools
```

否则底层会反向依赖上层，模块越来越难拆。

---

# 文档对应关系

如果你想了解“怎么用工具”：

[用户手册](../manual/index.md)

如果你想了解“为什么这样分层”：

当前页面与 [总体架构](index.md)

如果你要看真实函数、参数和返回值：

- [Tools API](../reference/tools/index.md)
- [Systems API](../reference/systems/index.md)

API 页面由当前源码自动生成，不再维护旧版函数清单。
