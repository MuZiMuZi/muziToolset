# MuziTools 总体架构

这一页描述 **当前仓库真实运行时结构**。

旧版本中已经退出主流程的目录、类和分层不再作为推荐架构展示；历史实现如果仍保留在仓库中，会明确标记为 Compatibility / Legacy，而不是继续混在正式设计里。

---

## 当前项目分层

MuziTools 目前采用五层 Runtime 结构：

```text
app/
    应用入口与顶层窗口

ui/
    公共 PySide UI 基础设施

tools/
    绑定师直接使用的工具层

systems/
    完整 Rig Module / Workflow

core/
    Maya / Rigging 基础能力
```

推荐依赖方向：

```text
app
 │
 ├──────────────┐
 ↓              ↓
tools         systems
 │              │
 └──────┬───────┘
        ↓
       core

ui 作为公共界面层被 app / tools / systems 使用
```

核心原则：

> **越靠下越通用，越靠上越接近用户任务和完整 Rig Workflow。**

---

# 1. `core/` — 基础能力层

当前正式结构：

```text
core/
├── common/
│   ├── attr_utils.py
│   ├── hierarchy_utils.py
│   ├── name_utils.py
│   └── transform_utils.py
├── rigging/
│   ├── ctrl_utils.py
│   ├── guide_utils.py
│   └── jnt_utils.py
└── bake/
    └── legacy compatibility code
```

职责：

```text
Naming
Attribute
Hierarchy
Transform
Controller
Guide
Joint
```

Core 不应该知道“这是 Eye、Brow、Lip 还是 Ear”。

详细设计：[Core 架构](core.md)

---

# 2. `systems/` — 完整 Rig 业务层

当前顶层结构：

```text
systems/
├── rig_module.py
├── face/
├── rig/
├── body/
└── components/
```

Systems 负责把 Core 基础能力组合成可重复构建的业务模块。

例如：

```text
systems/face/eye_module.py
```

不是简单“创建一个 Controller”，而是负责：

```text
读取 Eye Guide
创建 Eye Joint
创建 Main / Aim Controller
整理模块 Hierarchy
建立 Aim / Orient Connection
提供 Rebuild / Connect / Validate 流程
```

也就是说：

```text
Core = 原子能力
Systems = 完整业务单元
```

当前重要 Systems 区域：

### `systems/face/`

Face Rig 模块与 Guide 语义。

当前可见正式模块包括：

```text
ear_module.py
eye_module.py
face_guide_config.py
tongue_module.py
```

### `systems/rig/`

Modular Rig / Rig Library 相关能力。

当前主要内容：

```text
library_catalog.py
library_service.py
ui/
```

### `systems/body/`

身体绑定相关 Builder。

### `systems/components/`

可复用 Rig Component，例如 FK Chain。

API：[Systems API](../reference/systems/index.md)

---

# 3. `tools/` — 用户工具层

当前目录按任务分类：

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

Tool 的职责是把底层 API 变成绑定师可以直接操作的功能。

典型工作：

```text
读取 Maya Selection
收集 UI 参数
做输入校验
调用 Core / System
显示结果或警告
```

Tool 不应该重新实现系统底层逻辑。

例如：

```text
create_ctrl_tool.py
```

可以负责读取用户选中的 Guide、Shape、颜色和大小，但 Controller 的 Shape / Hierarchy 基础能力应该来自 `core/rigging/ctrl_utils.py`。

详细设计：[Tools 与 Systems](tools-systems.md)

---

# 4. `ui/` — 公共界面层

当前结构：

```text
ui/
├── theme.py
├── window_utils.py
└── widgets/
```

其中：

```text
theme.py
    统一颜色、字体、QSS 与视觉 Token

window_utils.py
    Maya Window / Dock / 生命周期相关公共能力

widgets/
    可复用 Widget，例如 Object Picker、Color Slider
```

业务专属 UI 可以存在于 Tool / System 中，但通用 Widget 应尽量回收到 `ui/`。

API：[UI API](../reference/ui/index.md)

---

# 5. `app/` — 应用入口层

当前主要文件：

```text
app/main.py
app/toolbox.py
app/window_manager.py
```

职责：

```text
启动 MuziTools
组织主工具箱
统一窗口生命周期
将多个 Tool / System 暴露给用户
```

App 是组合层，不应该成为新的业务逻辑堆积区。

API：[App API](../reference/app/index.md)

---

# 6. `resources/` — 数据与资源

这里用于存放不属于 Python 业务代码的资源，例如：

```text
Controller Shape 数据
Face Guide Maya 文件
图片 / 图标
其他运行时资源
```

资源和逻辑要分开。

例如 Controller Shape 应通过 Shape Library 数据读取，而不是把所有 CV 点硬编码在 UI 中。

---

# 7. `tests/` — 架构契约与静态测试

测试不仅用于检查“函数有没有报错”，还承担架构门禁。

当前文档 Workflow 会检查：

```text
Core Import Style
Jnt Naming Contract
Rig Architecture Migration
RigBase / ModuleBase Contract
Core Single Source
Core Public API
System -> Core Reuse
Maya 2023 Smoke Contract
Runtime Docstring
Rigging Terminology
API Generator
API Coverage
Generated Layout
README / Navigation
MkDocs Strict Build
```

因此文档网站本身也是受测试保护的项目产物。

---

# 8. `scripts/` — 维护与生成工具

`scripts/` 不属于 Maya Runtime API。

它主要用于：

```text
代码迁移
架构清理
Docstring 规范化
Step Comment 审计
API Reference 生成
MkDocs 导航生成
旧命名迁移
```

典型文档脚本：

```text
normalize_runtime_docstrings.py
refine_runtime_docstring_semantics.py
generate_mkdocs_reference.py
refine_generated_reference.py
refine_generated_callable_layout.py
extend_docs_summary.py
```

这些脚本服务项目维护，不应该出现在 Runtime API 树中。

---

# 9. `docs/` — 项目文档网站

当前文档分为：

```text
docs/
├── index.md
├── getting-started/
├── manual/
├── architecture/
├── development/
├── migration/
└── reference/
```

其中：

```text
manual / architecture / development
    人工维护

reference
    根据 Runtime AST 自动生成
```

详细规则：[文档维护](../development/documentation.md)

---

# 当前 Rig Module 思路

当前仓库的完整业务 Module 基于：

```text
systems/rig_module.py
```

具体 Module 继承公共 Rig Module 行为后，负责实现自己的：

```text
Guide
Joint
Controller
Hierarchy
Connection
Rebuild
Validation
```

以 Eye 为例：

```text
EyeModule
    ↓
get_guides()
    ↓
create_joints()
    ↓
create_ctrls()
    ↓
setup_hierarchy()
    ↓
connect_rig()
```

对于已经生成过的模块，还需要支持：

```text
load_outputs()
delete_connections()
重新 Connect
安全 Rebuild
```

这也是当前 Modular Rig Workflow 的重要设计方向。

---

# 当前 Face Rig 方向

Face Rig 不是单一大脚本，而是逐步拆成独立 Module。

当前主思路：

```text
Guide
    ↓
单模块 Build
    ↓
Controller / Joint 调整
    ↓
最终 Connection
    ↓
需要时回退并 Rebuild
```

Eye Module 当前已经明确区分：

```text
Ball Guide
Iris Guide
Aim Guide
```

并通过稳定输出层连接到最终 Joint。

详细说明：[Face System](face-system.md)

---

# 新代码应该放在哪里

## 通用 Maya 操作

```text
core/common/
```

## Controller / Guide / Joint 基础能力

```text
core/rigging/
```

## 完整 Rig 部位或业务 Workflow

```text
systems/
```

## 用户直接打开的小工具

```text
tools/
```

## 公共 UI Widget / Theme

```text
ui/
```

## 主应用入口

```text
app/
```

## 生成器 / 迁移 / 审计

```text
scripts/
```

---

# 当前架构的几个重要约束

### 1. 不重复实现 Core

如果 `core/` 已经有通用能力，System / Tool 不应该复制第二份。

### 2. System 不依赖 Tool

推荐方向：

```text
Tool -> System -> Core
```

而不是：

```text
System -> Tool
```

### 3. UI 不保存核心业务状态

UI 收集和显示数据，核心 Rig 状态应该由 System / Scene / Config 管理。

### 4. Rebuild 必须是正式能力

模块不是“一次生成后不能再动”。

当前设计强调：

```text
Guide 可修改
Controller / Joint 可调
Connection 可删除并重建
模块可安全 Rebuild
```

### 5. 文档必须来自当前源码

API 参数、返回值和公开方法以 Runtime Docstring 为第一事实来源，避免人工 Markdown 长期失真。

---

# 推荐阅读顺序

如果第一次看项目：

1. 当前页面
2. [Core 架构](core.md)
3. [Tools 与 Systems](tools-systems.md)
4. [Face System](face-system.md)
5. [API Reference](../reference/index.md)

如果准备修改一个具体函数，直接进入自动生成的 API 页面，不要依赖旧截图或旧版本 Markdown。
