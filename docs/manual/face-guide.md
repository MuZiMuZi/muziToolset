# Face Guide

`FaceGuide` 是 Face Rig 的 **Step 02 定位数据管理层**。

它只负责 Guide 的加载、查询、验证和最终确认，不创建正式 Joint 或动画 Controller。

<div class="grid cards" markdown>

-   :material-download-box-outline:{ .lg .middle } **Build Guide**

    ---

    加载或复用 `face_guide.ma` 模板。

    [:octicons-code-24: FaceGuide API](../reference/systems/face/face_guide.md)

-   :material-face-man-shimmer-outline:{ .lg .middle } **手动贴合**

    ---

    调整 Lip、Eye、Brow、Jaw、Nose 等 Locator 到角色位置。

-   :material-check-decagram-outline:{ .lg .middle } **Validate**

    ---

    检查必要 Guide、重复名称和左右镜像关系。

-   :material-flag-checkered:{ .lg .middle } **Finalize**

    ---

    确认 Step 02 完成，并把稳定 Guide 数据交给后续 Builder。

</div>

## 标准流程

```text
FaceSetup.build()
       ↓
FaceGuide.build()
       ↓
手动贴合 Guide
       ↓
validate_guides()
       ↓
FaceGuide.finalize()
       ↓
Step 03 Builder
```

## 1. 完成 Face Setup

```python
from muziToolset.systems.face import FaceSetup

setup = FaceSetup(
    face_head_model="head_geo",
    mouth_jnt_number=40
)

setup.build()
```

## 2. 创建 Guide

```python
from muziToolset.systems.face import FaceGuide

guide = FaceGuide()
guide.build()
```

`build()` 只准备可编辑 Guide。此时 Step 02 **还没有完成**。

## 3. 手动贴合

重点检查：

- Lip / Mouth Corner
- Eye Ball / Iris
- Upper / Lower Eyelid
- Brow
- Nose / Jaw
- Teeth / Tongue
- Ear / Zygoma

!!! tip "左右 Guide"
    正常左右结构已经保存在模板中。通常编辑 LF / MD Guide 即可，不需要每次重新创建 RT Guide。

## 4. 检查 Guide

```python
report = guide.validate_guides()

print(report["valid"])
print(report["errors"])
```

如果左右镜像被改坏：

```python
guide.repair_symmetry()
```

## 5. Finalize

```python
guide.finalize()
```

通过后：

```text
Step 02 = completed
Step 03 = not completed
Step 04 = not completed
```

## Guide 数据怎么给 Builder 使用

后续 Builder 不应该自己用 `cmds.ls()` 猜 Locator 顺序，而应该直接读取 FaceGuide：

```python
lip_data = guide.get_lip_guides()
lid_data = guide.get_eyelid_guides("lf")
brow_data = guide.get_brow_guides("lf")
```

## 相关 API

- [face_base.py](../reference/systems/face/face_base.md)
- [face_setup.py](../reference/systems/face/face_setup.md)
- [face_guide.py](../reference/systems/face/face_guide.md)
- [eyelid/builder.py](../reference/systems/face/eyelid/builder.md)
- [lip/zip_builder.py](../reference/systems/face/lip/zip_builder.md)

[返回用户手册](index.md){ .md-button }
[打开 FaceGuide API](../reference/systems/face/face_guide.md){ .md-button .md-button--primary }
