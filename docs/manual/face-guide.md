# Face Guide

`FaceGuide` 是 Face Rig 的 **Step 02 Guide 操作入口**。

进入 Step 02 时，UI 会自动导入或复用 `resources/face/face_guide.ma`。绑定师主要负责摆放 Locator、Mirror、Repair 和设置后续 Controller 参数。

## 标准流程

```text
Step 01 Setup 完成
        ↓
进入 Step 02 Guide
        ↓
自动导入 / 复用 face_guide.ma
        ↓
手动调整 Locator
        ↓
需要时 LF ↔ RT Mirror
        ↓
设置 Controller Size / Color
        ↓
点击“下一步”
        ↓
检查模板中的全部 Locator
        ↓
完整 → 保存 Config → 进入 Step 03
缺失 → 阻止继续并列出缺失名称
```

## 当前代码结构

```text
systems/face/guide/
├── __init__.py
└── face_guide.py
```

固定名称、默认 Controller 参数和 Step Visibility Rule 统一定义在：

```text
systems/face/config.py
```

---

# 名称生成

Guide / Jnt / Controller 等正式 Rig 名称统一使用 `RigBase`。

```python
from muziToolset.systems.rig_base import RigBase

name = RigBase.create_name(
    type="loc",
    side="md",
    part="upper_teeth",
    function="guide",
    index=1
)
```

结果：

```text
loc_md_upper_teeth_guide_001
```

`FaceGuide` 已经通过 `FaceBase -> RigModuleBase -> RigBase` 获得 Naming API，因此在 Face 代码内部可以直接：

```python
guide_name = face_guide.create_name(
    type="loc",
    side="md",
    part="upper_teeth",
    function="guide",
    index=1
)
```

左右名称：

```python
mirror_name = face_guide.mirror_name(
    "loc_lf_eye_ball_guide_001"
)
```

结果：

```text
loc_rt_eye_ball_guide_001
```

旧 `core/name_utils.py` 已删除。

---

# Guide 查询

## 查询一个明确 Guide

```python
from muziToolset.systems.face import FaceGuide

face_guide = FaceGuide()

guide_name = face_guide.create_name(
    type="loc",
    side="md",
    part="upper_teeth",
    function="guide",
    index=1
)

upper_teeth_guide = face_guide.get_guide_node(
    guide_name,
    required=True
)
```

## 查询一个部位

Tongue：

```python
tongue_guides = face_guide.get_part_guides(
    part="tongue"
)
```

左侧 Brow：

```python
lf_brow_guides = face_guide.get_part_guides(
    part="brow",
    side="lf"
)
```

不为了固定参数转发额外创建无业务价值的方法。

只有固定顺序、结构化结果或额外校验确实有价值时才保留专用 Query。

---

# 自动加载 Guide

```python
face_guide.build_guide()
```

如果 Guide 已存在就复用；不存在时导入：

```text
resources/face/face_guide.ma
```

---

# 重新导入模板

```python
result = face_guide.reimport_guide()
```

流程：

```text
记录当前仍存在 Locator 世界矩阵
        ↓
删除当前模板内容
        ↓
重新导入 face_guide.ma
        ↓
恢复原来仍存在 Locator 的位置
        ↓
被误删 Locator 使用模板默认位置
```

---

# Guide Mirror

```python
result = face_guide.mirror_guides(
    source_side="lf",
    target_side="rt"
)
```

或：

```python
result = face_guide.mirror_guides(
    source_side="rt",
    target_side="lf"
)
```

Mirror：

- 只复制当前状态；
- 不建立永久左右连接；
- `md` Guide 不参与；
- 使用 `RigBase.mirror_name()` 语义；
- 支持 Maya Undo Chunk；
- UI 保存最近一次 Mirror Snapshot。

目标 Guide 被误删时，应先使用 Reimport Repair，再执行 Mirror。

## 撤销最近一次 Mirror

```python
result = face_guide.undo_mirror(
    snapshot
)
```

也可以使用 Maya `Ctrl + Z`。

---

# 完整性检查

`face_guide.ma` 是 Locator 完整性的最终模板来源。

```python
validation = face_guide.validate_guides()

print(validation["valid"])
print(validation["missing_guide_names"])
print(validation["guide_count"])
print(validation["template_guide_count"])
```

任意标准 Locator 缺失，Step 02 都不能进入 Step 03。

---

# Controller Settings

Controller Settings 保存到统一 Face Config。

当前正式参数：

```text
Global Scale
LF Color
RT Color
MD Color
Brow Size
Eye Size
Eyelid Size
Nose Size
Cheek Size
Lip Size
Jaw Size
Teeth Size
Tongue Size
```

默认颜色：

```text
LF = 6
RT = 13
MD = 17
```

配置定义在：

```text
systems/face/config.py
```

---

# Step Visibility

静态规则：

```text
systems/face/config.py
```

执行：

```text
systems/face/ui/workflow_controller.py
```

Step 02 默认显示：

```text
Setup 原始输入模型
+
Face Guide
```

隐藏 Tweak / Stretch / Deform Work Model、Controller、Jnt 和内部 Rig Nodes。

---

# 给 Step 03 Module 使用

完整业务单元统一称为 **Module**。

例如 `TeethModule`：

```python
upper_teeth_name = self.create_name(
    type="loc",
    side="md",
    part="upper_teeth",
    function="guide",
    index=1
)

upper_teeth_guide = self.face_guide.get_guide_node(
    upper_teeth_name,
    required=True
)
```

推荐关系：

```text
RigBase Naming
    ↓
Guide Query
    ↓
Module Build
```

完整 Module 放在：

```text
systems/face/modules/
```

可复用构建算法放在：

```text
systems/face/build/
```

两者不要混在一起。

## 相关文档

- [Face System Architecture](../architecture/face-system.md)
- [Face Workflow State](../architecture/face-workflow-state.md)
- [总体架构](../architecture/index.md)

[返回用户手册](index.md){ .md-button }
