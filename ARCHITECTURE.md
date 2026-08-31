# MuziTools Architecture

`muziToolset` 根包是项目唯一正式运行框架。

## 目录职责

```text
muziToolset/
├─ app/                    # Maya 应用入口、主工具箱、窗口生命周期
├─ ui/                     # PySide Theme、通用 Widget、Window Helper
├─ core/                   # Maya / Python 通用底层能力
├─ tools/                  # 单功能、可独立启动的小工具
├─ systems/                # 可复用 Rig System / Component / Builder
├─ resources/              # Guide Template、Controller Shape 等资源
├─ tests/                  # Static Gate + Maya Smoke
├─ docs/                   # 用户手册、架构、开发指南、API Reference
├─ scripts/                # 文档生成与开发脚本
├─ legacy_reference/       # 历史资料，只用于参考
├─ mkdocs.yml
├─ config.py
├─ __init__.py
└─ start.py
```

## 分层依赖

```text
app / ui / tools
        ↓
      systems
        ↓
       core
```

允许同层通过明确公共 API 复用，但禁止让 `core` 反向 import `tools / systems / ui / app`。

---

# Core

`core` 是最底层能力库，采用“一个 Maya 领域一个 utils 模块”的颗粒度。

允许：

- `maya.cmds`
- `maya.api.OpenMaya`
- Python 标准库
- 其它职责明确的 Core 模块

禁止：

- `app`
- `ui`
- `tools`
- `systems`
- `legacy_reference`
- PyMel

当前主要 Core：

```text
animation_utils.py
attr_utils.py
blendshape_utils.py
config_utils.py
connection_utils.py
constraint_utils.py
control_shape_utils.py
curve_utils.py
file_utils.py
hierarchy_utils.py
joint_utils.py
matrix_utils.py
mesh_utils.py
model_check_utils.py
name_utils.py
rename_utils.py
scene_clean_utils.py
scene_utils.py
skin_utils.py
surface_utils.py
transform_utils.py
```

`config_utils.ConfigNode` 统一负责 Maya `network` Config Node、Message 引用和普通 Value 配置。Face / Body 等 System 不重复实现 Config CRUD。

## Core 编码规则

正式 Runtime 默认遵守：

1. 接收明确参数；
2. 先验证输入和 Maya 节点；
3. 中文注释说明流程目的和 Maya 特有原因；
4. 返回节点、列表、数量或结果字典；
5. Core 不弹 UI；
6. 大型场景操作使用单个 Maya Undo Chunk；
7. 普通流程使用展开 `for` 循环，不为了短代码滥用列表推导；
8. 新代码不新增 PyMel；
9. 文件、模块变量、函数使用 `snake_case`，Class 使用 `PascalCase`；
10. 已存在于 Core 的能力禁止在 Tool / System 再复制一套。

---

# Naming

正式 Maya Rig 节点命名：

```text
[类型]_[方向]_[部位]_[功能]_[序号]
```

方向统一：

```text
lf
rt
md
```

标准名称统一由：

```python
name_utils.Name.create_name(...)
```

生成。

左右名称统一由：

```python
name_utils.Name.mirror_name(...)
```

计算。

System / Component 不再复制第二套字符串 Naming Logic。

正式 Python 命名：

```text
module / file / function / variable  snake_case
Class                                PascalCase
```

---

# Systems

`systems` 实现完整且可复用的 Rig Workflow、Component 和 Builder。

## Step 生命周期

凡是“按步骤提交、可以返回修改并重新执行”的 System Step，统一继承：

```python
from muziToolset.systems.common import StepBase
```

固定生命周期：

```text
collect_inputs()
      ↓
prepare_data()
      ↓
process_data()
      ↓
finalize_step()
```

统一入口：

```python
run_step()
```

不要重新发明另一套同义顶层生命周期。

## Face System

Face Rig 正式采用 **Workflow Step 外层分包 + Build 内 Component 分包**：

```text
systems/face/
├── __init__.py
├── config.py
├── face_base.py
│
├── setup/                 # 01 Setup
│   └── face_setup.py
│
├── guide/                 # 02 Guide
│   └── face_guide.py
│
├── build/                 # 03 Build
│   ├── curve_attachment.py
│   ├── teeth_component.py
│   ├── eyelid/
│   └── lip/
│
├── finalize/              # 04 Finalize
│
├── data/
│   └── shape_dictionary.py
│
└── ui/
    ├── face_rig_ui.py
    └── workflow_controller.py
```

详细规范见：

```text
docs/architecture/face-system.md
```

### Step ≠ Component

```text
Step
    Setup / Guide / Build / Finalize 用户工作流阶段

Component
    Teeth / Tongue / Jaw / Lip / Eye / Eyelid / Brow 等绑定模块

Builder
    Curve Attachment / Zip / Radial Joint 等可组合算法

Core
    Matrix / Curve / Joint / DAG / Attribute / Naming 等通用能力
```

简单 Component 优先保持单文件；只有真正复杂后再拆 Package。

Component 可以复用四阶段构建思路，但 Component 完成不代表整个 Step 03 Completed。

### FaceBase 边界

`face_base.py` 只负责所有 Face Step 共用的：

- Face Hierarchy；
- Face Config；
- Setup 公共数据；
- Step State；
- Current Face Step；
- Config Step 分区；
- 公共 Config 语义 API。

具体 Guide / Component 构建算法不放进 FaceBase。

### Face Config

`systems/face/config.py` 是 Face System 的统一静态配置入口。

保存：

- Face Group / Set / Config Node 名称；
- Guide Template 路径、Move Ctrl 和 Version；
- Controller 默认 Size / Color；
- Controller Module 顺序；
- Step 顶层 Visibility Rule；
- Step Model Display Rule。

Config 只定义“是什么”，不执行 Maya Rig 操作。

### Face Guide

Guide 当前故意保持单文件：

```text
systems/face/guide/
├── __init__.py
└── face_guide.py
```

`FaceGuide` 直接负责：

- Template Import；
- Reimport / Repair；
- Guide Query；
- LF ↔ RT Mirror；
- Mirror Undo；
- Locator 完整性检查；
- Controller Settings Config；
- Step 02 Lifecycle。

不再维护 `guide_data.py / guide_template.py / guide_mirror.py`。

简单 Guide 查询直接使用：

```python
face_guide.get_part_guides(
    part="tongue"
)
```

或用 `name_utils.Name.create_name()` 动态生成明确名称，再调用：

```python
face_guide.get_guide_node(...)
```

不为单纯固定参数转发额外创建 `get_xxx_guides()`。

只有固定顺序、结构化返回或额外校验确实有价值时才保留专用 Query。

### Guide Template Contract

`resources/face/face_guide.ma` 仍然是标准 Locator 完整性的最终来源。

点击 Step 02“下一步”时：

```text
Template 全部 Locator
        ↓
当前 Scene Guide
        ↓
逐个检查
        ↓
任意缺失 → 阻止进入 Step 03
```

重新导入模板：

```text
记录仍存在 Locator 世界位置
        ↓
重新导入完整模板
        ↓
恢复已有 Locator
        ↓
误删 Locator 使用模板默认位置补回
```

Guide Mirror 使用 Naming API 查找对应左右节点，不负责创建被误删的目标 Guide；缺失时先 Repair。

### Face Workflow Visibility

不再单独维护 `systems/face/workflow.py`。

静态显示规则统一定义在：

```text
systems/face/config.py
```

`ui/workflow_controller.py` 在 Step 切换时直接执行这些规则。

Step 01 / 02 只显示 Setup Config 中保存的原始输入模型，自动隐藏 Tweak / Stretch / Deform 工作副本。

---

# Tools

`tools` 负责：

- 读取 Selection / Channel Box；
- 接收用户参数；
- 显示状态和 Warning；
- 调用 Core / System；
- 提供统一 `main()`。

Tool 不复制 Core 或 System 算法。

UI Tool 的 `main()` 应直接显示并返回 QWidget / QDialog；直接执行工具不强行创建 UI。

---

# UI / App

## UI

`ui` 维护：

```text
theme.py
widgets/
window_utils.py
```

所有正式 PySide 界面优先复用统一 Theme 和 Widget。

当前 MuziTools UI 参考 Arc Browser 的 **clean / calm / sidebar-first** 信息组织：

- 柔和背景；
- 轻量边界；
- 浮层式 Card；
- 稳定 Sidebar；
- 清晰 Active State；
- Primary / Secondary / Ghost / Danger 明确分级；
- 关键修复和提交操作不能因为弱样式而难以发现。

这里借鉴布局与交互原则，不复制 Arc 的 Logo、图标、品牌资产或一比一视觉。

正式规范：

```text
docs/development/ui-design.md
```

## App

`app` 负责：

- 主工具箱；
- Tool Discovery；
- 分类 Sidebar；
- Window Manager；
- 应用级生命周期。

窗口管理职责：

```text
ui.window_utils
    单个 Tool.main() 直接运行时保证窗口生命周期。

app.window_manager
    从主工具箱打开 Tool 时管理 Parent、Window Flags、单实例。
```

---

# 文档系统

```text
源码 Docstring
      ↓
AST 静态扫描
      ↓
docs/reference/
      ↓
MkDocs Material
      ↓
GitHub Pages
```

人工文档主要维护：

```text
docs/manual/          用户任务工作流
docs/architecture/    系统边界和目录结构
docs/development/     编码、UI、文档、测试规范
docs/migration/       迁移记录
```

UI 和文档网站使用同一套 calm / layered 信息设计原则，文档视觉由 `docs/stylesheets/manual.css` 维护。

---

# 测试门槛

GitHub CI：

```text
Static Import / Style Gate
        ↓
AST API Reference Generation
        ↓
mkdocs build --strict
```

Maya 2023 真机 Smoke：

- Core Maya 行为；
- Tool Window；
- Face Component；
- 后续各 Workflow Step。

静态测试负责架构和文档不回退，Maya Smoke 负责真实 Maya 行为。

---

# Legacy

`legacy_reference/` 只作为历史资料，不属于正式运行架构。

需要旧算法时：

```text
理解旧算法
    ↓
提取有效逻辑
    ↓
按新 Core / System 边界重写
    ↓
加入正式测试
```

正式代码禁止直接 Import Legacy。

---

# Maya 兼容策略

当前主要目标：Maya 2023。

- UI 优先 PySide2；
- 可保留 PySide6 fallback；
- 场景操作优先 `maya.cmds`；
- 必要矩阵 / Curve 数学使用 Maya API 2.0；
- 不新增 PyMel。

启动：

```python
import muziToolset
muziToolset.show()
```
