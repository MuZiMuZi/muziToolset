# Face System Architecture

Face Rig 使用 **Workflow Step + Module + Build Algorithm** 三层结构。

## 正式目录

```text
systems/face/
├── __init__.py
├── config.py
├── face_base.py
│
├── setup/
│   ├── __init__.py
│   └── face_setup.py
│
├── guide/
│   ├── __init__.py
│   └── face_guide.py
│
├── modules/
│   ├── __init__.py
│   └── teeth.py
│
├── build/
│   ├── __init__.py
│   ├── curve_attachment.py
│   ├── eyelid/
│   └── lip/
│
├── finalize/
├── data/
└── ui/
    ├── __init__.py
    ├── face_rig_ui.py
    ├── workflow_controller.py
    └── build_controller.py
```

## 四步 Workflow

```text
01 Setup
    ↓
02 Guide
    ↓
03 Build
    ↓
04 Finalize
```

Workflow Module 使用统一生命周期：

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

---

# Step / Module / Builder / Core

```text
Step
    Setup / Guide / Build / Finalize 用户工作流阶段

Module
    Teeth / Tongue / Jaw / Lip / Eye / Eyelid / Brow 等完整绑定业务单元

Builder
    Curve Attachment / Zip Lip / Radial Joint 等可组合构建算法

Core
    Matrix / Curve / Joint / DAG / Attribute 等通用 Maya 能力
```

完整业务单元不再称为 Component。

---

# FaceBase

`face_base.py` 是所有 Face Workflow / Rig Module 的公共业务底座。

负责：

- 继承 `RigModuleBase`；
- Face Hierarchy；
- Face Config；
- Setup 公共数据；
- Step 完成状态；
- Current Face Step；
- Config Step 分区；
- 公共 Config 语义 API。

继承关系：

```text
RigBase
   ↓
ModuleBase
   ↓
RigModuleBase
   ↓
FaceBase
```

具体 Guide / Teeth / Jaw 等业务不塞回 `FaceBase`。

---

# Face Config

`systems/face/config.py` 是 Face 静态配置入口。

负责：

- Face Group / Set / Config Node 名称；
- Guide Template 路径、Move Ctrl、Version；
- Controller 默认 Size / Color；
- Controller Module 顺序；
- Step Visibility Rule；
- Step Model Display Rule。

Rig Name 使用：

```python
from muziToolset.systems.rig_base import RigBase

RigBase.create_name(...)
```

Face Module 内部通常直接使用继承来的：

```python
self.create_name(...)
self.mirror_name(...)
```

`core/name_utils.py` 已删除。

---

# Step 01 - Setup

`setup/face_setup.py` 负责：

- Head / Eye / Teeth / Tongue / Gum 输入；
- 输入模型验证；
- Face Hierarchy；
- Tweak / Stretch / Deform Work Model；
- Mouth Joint Number；
- Step 01 Config；
- Step 01 完成后推进到 Step 02。

`FaceSetup` 属于特殊 Workflow Module，因此覆盖自己的 `process_data()`。

---

# Step 02 - Guide

`FaceGuide` 负责：

- Template Import；
- Reimport / Repair；
- Guide Query；
- LF ↔ RT Mirror；
- Mirror Undo Snapshot；
- Locator 完整性检查；
- Controller Settings Config；
- Step 02 Lifecycle。

简单查询：

```python
guide.get_part_guides(
    part="tongue"
)
```

查询明确 Guide：

```python
guide_name = guide.create_name(
    type="loc",
    side="md",
    part="upper_teeth",
    function="guide",
    index=1
)

guide_node = guide.get_guide_node(
    guide_name,
    required=True
)
```

左右 Mirror 名称直接使用：

```python
mirror_name = guide.mirror_name(
    source_name
)
```

---

# Guide Template Contract

`resources/face/face_guide.ma` 是标准 Locator 完整性的最终来源。

Step 02 提交时：

```text
Template 全部 Locator
        ↓
当前 Scene Guide
        ↓
逐个检查
        ↓
任意缺失 → 阻止进入 Step 03
```

Reimport：

```text
记录现有 Locator 世界位置
        ↓
重新导入完整模板
        ↓
恢复现有 Locator
        ↓
误删 Locator 使用模板默认位置补回
```

---

# Step 03 - Modules

完整业务 Module 统一放：

```text
systems/face/modules/
```

当前：

```text
teeth.py
    TeethModule
```

后续计划：

```text
JawModule
TongueModule
LipModule
EyeModule
EyelidModule
BrowModule
NoseModule
CheekModule
```

真正 Rig Module 统一使用：

```text
collect_inputs()
      ↓
prepare_data()
      ↓
create_joint()
      ↓
create_controller()
      ↓
create_connection()
      ↓
finalize_step()
```

Module 构建完成不等于整个 Step 03 Completed。只有 Step 03 要求的 Module 全部完成后才推进 Workflow。

---

# Face Build Algorithms

可复用算法统一放：

```text
systems/face/build/
```

当前包括：

```text
curve_attachment.py
    Curve Attachment

eyelid/
    Radial Curve Joint

lip/
    Matrix Zip Lip
```

这些文件是 Builder / Algorithm，不是完整业务 Module。

例如未来 `EyelidModule` 可以组合 Eyelid Builder，`LipModule` 可以组合 Zip Lip Builder。

---

# Controller

所有 Face Module 创建 Controller 时统一调用：

```python
from muziToolset.systems import ctrl_base

ctrl_base.create_ctrl(...)
```

旧：

```text
systems/controller/
```

已经删除。

---

# Workflow Visibility

静态规则：

```text
systems/face/config.py
```

执行：

```text
systems/face/ui/workflow_controller.py
```

Step 01 / 02 显示 Setup 原始输入模型；Step 03 / 04 当前模型内部规则保持 `preserve`，后续按正式需求扩展。

---

# UI 入口

```text
systems.face.show()
    ↓
systems.face.ui.show()
    ↓
ui/build_controller.py
    ↓
ui/workflow_controller.py
    ↓
ui/face_rig_ui.py
```

`build_controller.py` 在稳定 Workflow UI 上扩展 Step 03 Module Build 页面。

---

# Public API

```python
from muziToolset.systems import face

face.FaceSetup
face.FaceGuide
face.TeethModule
face.build_teeth()
face.show()
```

上层 Tool 应优先依赖这些稳定入口，不直接依赖内部 Builder 文件。
