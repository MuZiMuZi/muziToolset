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
│   └── face_guide.py
│
├── build/
│   ├── __init__.py
│   ├── curve_attachment.py
│   ├── teeth_component.py
│   ├── eyelid/
│   └── lip/
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
    ├── face_rig_ui.py
    └── workflow_controller.py
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

真正的 Workflow Step 继续使用统一生命周期：

```text
collect_inputs()
      ↓
prepare_data()
      ↓
process_data()
      ↓
finalize_step()
```

Step 和 Component 是两个概念：

```text
Step
    Setup / Guide / Build / Finalize 用户工作流阶段

Component
    Teeth / Tongue / Jaw / Lip / Eye / Eyelid / Brow 等绑定模块

Builder
    Curve Attachment / Zip / Radial Joint 等可复用构建算法

Core
    Matrix / Curve / Joint / DAG / Attribute / Naming 等通用 Maya 能力
```

## 根目录公共层

### `face_base.py`

只保存所有 Face Step 共用的业务能力：

- Face Hierarchy；
- Face Config；
- Setup 公共数据；
- Step 完成状态；
- Current Face Step；
- Config Step 分区；
- 公共 Config 读写语义。

不要把具体 Guide / Component 构建算法继续塞入 `FaceBase`。

### `config.py`

`config.py` 是 Face System 的统一静态配置入口。

负责定义：

- Face Group / Set / Config Node 名称；
- Guide Template 路径、Move Ctrl 名称和 Version；
- Controller 默认 Size / Color；
- Controller Module 顺序；
- Step 顶层 Group Visibility Rule；
- Step Model Display Rule。

所有标准 Maya 节点名称优先使用：

```python
name_utils.Name.create_name(...)
```

左右名称优先使用：

```python
name_utils.Name.mirror_name(...)
```

不要在 Face System 里再复制第二套 Naming Logic。

## Step 01 - Setup

`setup/face_setup.py` 负责：

- Head / Eye / Teeth / Tongue / Gum 输入；
- 输入模型验证；
- Face Hierarchy；
- Tweak / Stretch / Deform Work Model；
- Mouth Joint Number；
- Step 01 Config；
- Step 01 完成后推进到 Step 02。

## Step 02 - Guide

Guide 现在故意保持为单一实现文件：

```text
guide/
├── __init__.py
└── face_guide.py
```

`FaceGuide` 直接负责：

- Template Import；
- Reimport / Repair；
- Guide Query；
- LF ↔ RT Mirror；
- Mirror Undo Snapshot；
- Locator 完整性检查；
- Controller Settings Config；
- Step 02 Lifecycle。

不再维护：

```text
guide_data.py
guide_template.py
guide_mirror.py
```

这些文件原本只是把一个很直接的 Step 02 行为拆成多层调用，当前规模下没有足够收益。

### Guide 查询原则

简单查询直接使用通用 API：

```python
guide.get_part_guides(
    part="tongue"
)
```

或者先使用 Naming API 创建明确名称，再查询单个 Guide：

```python
guide_name = name_utils.Name.create_name(
    node_type="loc",
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

不再为了：

```python
get_tongue_guides()
```

这种仅仅转发一个固定参数的调用额外创建方法。

只有真正增加了固定顺序、分组结构或额外语义的方法才保留，例如 Lip / Eyelid 等有序 Guide Query。

## Guide Template 完整性

`resources/face/face_guide.ma` 仍然是 Locator 完整性的最终模板来源。

Step 02 点击“下一步”时：

```text
读取 Template 全部 loc_*_guide_###
        ↓
扫描当前 Face Guide
        ↓
逐个检查
        ↓
任意缺失
        ↓
阻止进入 Step 03
```

重新导入模板时：

```text
记录当前仍存在 Locator 世界位置
        ↓
重新导入完整 face_guide.ma
        ↓
恢复原来仍存在 Locator 的位置
        ↓
误删 Locator 使用模板默认位置补回
```

## Guide Mirror

Mirror 直接由 `FaceGuide` 执行：

```python
face_guide.mirror_guides(
    source_side="lf",
    target_side="rt"
)
```

左右名称统一通过 `name_utils.Name.mirror_name()` 获取。

Mirror 不负责 Repair。如果目标 Guide 被误删，应先重新导入模板补回，再执行 Mirror。

## Workflow 显示规则

不再单独维护 `systems/face/workflow.py`。

静态规则统一放在：

```text
systems/face/config.py
```

例如：

```text
Step 01
    Model Show
    Guide Hide
    Ctrl Hide
    Joint Hide

Step 02
    Model Show
    Guide Show
    Ctrl Hide
    Joint Hide

Step 03
    Model Show
    Guide Hide
    Ctrl Show
    Joint Show
```

`ui/workflow_controller.py` 在 Step 切换时直接读取这些规则并设置 Maya Visibility。

Step 01 / 02 的 Model Group 内部继续只显示 Setup Config 中保存的原始输入模型，Tweak / Stretch / Deform 工作副本隐藏。

## Face Config Workflow State

Face Config 保存：

```text
face_current_step
```

用于重新打开工具时恢复真正制作进度。

规则：

```text
Step 01 完成
    → Current Step = 02

Step 02 完成
    → Current Step = 03

Step 02 被修改
    → Step 02 Dirty
    → Step 03 / 04 Invalid
    → Current Step = 02
```

UI 临时查看旧页面不会修改正式 Workflow Progress。

## Step 03 - Build

Build 内按 Component 扩展。

简单 Component 优先保持单文件：

```text
build/
├── teeth_component.py
├── tongue_component.py
```

只有模块真正复杂后再拆 Package：

```text
build/
├── jaw/
├── lip/
├── eyelid/
└── ...
```

Component 可以继续使用四阶段构建思路：

```text
collect_inputs()
prepare_data()
process_data()
finalize_step()
```

但 Component 不等于 Step 03 本身。整个 FaceBuild 完成全部 Component 后，才正式标记 Step 03 Completed。

## Step 04 - Finalize

后续统一放：

- Final Validation；
- Controller Set；
- Display State；
- Cleanup；
- Publish；
- Build Result Summary。

## Public API

外部 Tool 继续通过稳定入口：

```python
from muziToolset.systems import face

face.FaceSetup
face.FaceGuide
face.show()
```

内部目录继续调整时，上层 Tool 不需要跟着修改 Import。
