# Face System Architecture

Face Rig 使用 **Workflow Step 外层分包 + Build 内 Component 分包**。

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
│   ├── face_guide.py
│   ├── guide_data.py
│   ├── guide_template.py
│   └── guide_mirror.py
│
├── build/
│   ├── __init__.py
│   ├── curve_attachment.py
│   ├── eyelid/
│   │   ├── __init__.py
│   │   └── builder.py
│   └── lip/
│       ├── __init__.py
│       └── zip_builder.py
│
├── finalize/
│   └── __init__.py
│
├── data/
│   ├── __init__.py
│   └── shape_dictionary.py
│
└── ui/
    ├── __init__.py
    └── face_rig_ui.py
```

以后 Jaw、Lip、Eye、Eyelid、Brow、Nose、Cheek 等正式 Component 继续放在 `build/` 下，不重新平铺回 `systems/face/` 根目录。

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

每个真正需要提交状态的 Step 继续遵守 `StepBase`：

```text
collect_inputs()
      ↓
prepare_data()
      ↓
process_data()
      ↓
finalize_step()
```

Step 和 Component 不是同一个概念：

```text
Step
    用户工作流阶段

Component
    Jaw / Lip / Eyelid / Brow 等绑定模块

Builder
    Curve Attachment / Zip / Radial Joint 等可组合算法

Core
    Matrix / Curve / Joint / DAG / Attribute 等通用 Maya 能力
```

## 根目录公共层

### `face_base.py`

只保存所有 Face Step 共用的业务能力：

- Face 基础层级；
- Face Config；
- Setup 公共数据；
- Step 状态；
- 公共 Config 语义 API。

不要把 Guide Template 名称、Mirror、Repair 或具体 Component Algorithm 塞入 `FaceBase`。

### `config.py`

保存整个 Face System 的全局配置：

- Group Name；
- Set Name；
- Config Network Name；
- Center Axis；
- Face Hierarchy。

### `data/`

保存跨多个 Step 使用的 Face 公共数据，例如 Face Shape Dictionary。

## Step 01 - Setup

`setup/face_setup.py` 负责：

- Head / Eye / Teeth / Tongue / Gum 输入；
- 输入模型验证；
- Face Hierarchy；
- Tweak / Stretch / Deform Work Model；
- Mouth Joint Number；
- Step 01 Config。

## Step 02 - Guide

### `face_guide.py`

只负责 Step 02 调度、稳定查询、Validation 和 Config。

不再维护大量散落的固定名称算法。

### `guide_data.py`

定义 Template Contract：

```text
face_guide.ma 路径
Guide Root
Move Ctrl
Guide Version
完整 Locator Name Contract
Lip / Eyelid 有序 Guide
Controller 默认参数
```

全部标准 Locator 直接从 `resources/face/face_guide.ma` 读取，因此 Template 是 Locator 完整性的唯一来源。

### `guide_template.py`

负责：

- Import；
- Reset；
- Reimport / Repair；
- 导入同名 Root 冲突处理；
- Reimport 前记录现有 Locator 世界矩阵；
- Reimport 后恢复仍存在 Locator；
- 被误删 Locator 使用模板默认位置补回。

### `guide_mirror.py`

负责：

- LF → RT；
- RT → LF；
- 不建立永久左右连接；
- Maya Undo Chunk；
- 上一次 Mirror Snapshot；
- 独立 Undo Mirror。

`md` Guide 不参与左右 Mirror。

## Step 02 完整性规则

点击“下一步”前必须：

```text
读取 face_guide.ma 全部标准 Locator Name
            ↓
扫描当前正式 Face Guide
            ↓
逐个比较
            ↓
任意一个缺失 → 阻止进入 Step 03
```

错误必须明确列出缺失名称。

恢复流程：

```text
[重新导入模板]
        ↓
记录当前仍存在 Locator 世界位置
        ↓
重新导入完整 face_guide.ma
        ↓
按固定名称恢复已有 Locator
        ↓
被误删 Locator 保留 Template 默认位置
```

## Step 03 - Build

Build Package 按 Component 扩展：

```text
build/
├── jaw/
├── lip/
├── eye/
├── eyelid/
├── brow/
├── cheek/
└── nose/
```

现有的 `curve_attachment.py` 属于 Build Primitive；`eyelid/builder.py` 和 `lip/zip_builder.py` 属于具体面部构建算法。

完整 Component 未来负责：

```text
Inputs
Settings
Build
Connections
Outputs
Ownership
Rebuild
```

而 Builder 只负责单一算法，不承担整个 Component 生命周期。

## Step 04 - Finalize

后续统一放：

- Final Validation；
- Controller Set；
- Display State；
- Cleanup；
- Publish；
- Build Result Summary。

## Public API

外部 Tool 不依赖内部迁移路径。

继续使用：

```python
from muziToolset.systems import face

face.FaceSetup
face.FaceGuide
face.build_eyelid_joints
face.build_zip_lip
face.show()
```

这样内部目录未来继续扩展，也不会强迫上层 Tool 修改 Import。
