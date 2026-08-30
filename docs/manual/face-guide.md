# Face Guide

`FaceGuide` 是 Face Rig 的 **Step 02 定位数据管理层**。

这一步不创建正式 Joint，也不创建最终动画 Controller。它的目标是：

> 把一套可编辑的面部 Guide 放进场景，让绑定师把它贴合到角色，然后把稳定、有顺序的定位数据交给后续 Builder。

## 开始前

先完成 Step 01：

```python
from muziToolset.systems.face import FaceSetup

setup = FaceSetup(
    face_head_model="head_geo",
    mouth_jnt_number=40
)

setup.build()
```

Step 01 会保存 Head、Eye、Teeth、Tongue、Gum 和 `mouth_jnt_number` 等配置。

## 创建 Guide

```python
from muziToolset.systems.face import FaceGuide

guide = FaceGuide()
result = guide.build()
```

`build()` 负责：

```text
读取 Step 01 Config
        ↓
确保 Face 主层级
        ↓
导入或复用 face_guide.ma
        ↓
保存 Guide Root / Move Ctrl
        ↓
等待绑定师手动贴合
```

!!! note "Build 不等于完成 Step 02"

    Face Guide 必须经过人工贴合，所以 `build()` 后 Step 02 仍保持未完成。

## 调整 Guide

模板中的颜色、初始 Locator、左右节点和默认连接属于：

```text
resources/face/face_guide.ma
```

Python 不应该在每次 Build 时重新创建这些视觉模板内容。

推荐编辑规则：

```text
MD Guide
    直接调整中心点

LF Guide
    作为主要编辑侧

RT Guide
    默认跟随模板中的左右镜像连接
```

常见需要调整的部位：

- Lip / Mouth Corner；
- Eye Ball / Iris；
- Upper / Lower Eyelid；
- Eye Bag；
- Brow；
- Nose；
- Jaw；
- Teeth；
- Tongue；
- Ear；
- Zygoma。

## 检查 Guide

```python
report = guide.validate_guides()
print(report)
```

返回结构类似：

```python
{
    "valid": True,
    "errors": [],
    "warnings": [],
    "guide_count": 0,
    "symmetry": {...},
}
```

推荐先检查 `valid`，失败时再显示 `errors`。

## 检查左右镜像

```python
symmetry_report = guide.validate_symmetry()
print(symmetry_report)
```

这个操作只检查，不修改场景。

常见问题：

```text
Right Locator 被删除
Right Zero Parent 错误
LF -> RT Connection 断开
Nested Guide 挂到了错误的 LF Parent
```

## 修复左右镜像

仅当模板关系被破坏时使用：

```python
guide.repair_symmetry()
```

正常 `build()` 不会主动重建 Right Guide。

这是当前职责划分：

```text
face_guide.ma
    静态模板 / 颜色 / 初始左右结构

FaceGuide
    加载 / 查询 / 验证 / Repair / 数据输出
```

## 完成 Step 02

贴合完成后：

```python
validation = guide.finalize()
```

`finalize()` 会重新验证 Guide，并把：

```text
step_02_completed = True
```

写入 Config。

如果验证失败，会列出具体缺失的 Guide 或镜像问题。

## 重置 Guide

如果 Guide 被改乱，希望恢复模板初始状态：

```python
guide.reset_guide()
```

!!! warning "Reset 会丢失当前手动贴合结果"

    `reset_guide()` 会删除当前 Guide 内容并重新导入模板。

## 删除 Guide

```python
guide.remove_guide()
```

系统级 `grp_md_face_guide_001` 会保留；删除的是它下面的模板内容。

## 查询嘴唇 Guide

```python
lip_data = guide.get_lip_guides()
```

返回：

```python
{
    "upper": [...],
    "lower": [...],
    "corners": [...],
}
```

顺序已经由 `FaceGuide` 统一管理，后续 Lip Builder 不应该再次自行排序。

## 查询眼皮 Guide

```python
left_lid = guide.get_eyelid_guides(
    side="lf"
)

upper_guides = left_lid["upper"]
lower_guides = left_lid["lower"]
```

Upper / Lower 都按照 Inner → 中间点 → Outer 的顺序返回。

## 查询 Brow / Eye / Jaw

```python
left_brow = guide.get_brow_guides("lf")
left_eye = guide.get_eye_guides("lf")
jaw_guides = guide.get_jaw_guides()
```

具体返回结构、参数和示例请直接查看自动 API 页面。

## Guide 数据如何进入后续 Builder

推荐关系：

```text
Guide Locator
    ↓
FaceGuide
    ↓
有语义、有顺序的数据
    ↓
Lip / Eyelid / Brow / Jaw Builder
    ↓
Curve / Joint / Controller
```

不要让 Builder 直接到场景里使用：

```python
cmds.ls("loc_lf_*")
```

去猜 Guide 顺序。

## 相关 API

- [Face Base](../reference/systems/face/face_base.md)
- [Face Setup](../reference/systems/face/face_setup.md)
- [Face Guide](../reference/systems/face/face_guide.md)
- [Curve Attachment](../reference/systems/face/curve_attachment.md)
- [Eyelid Builder](../reference/systems/face/eyelid/builder.md)
- [Zip Lip Builder](../reference/systems/face/lip/zip_builder.md)

## 推荐下一步

Face Guide 稳定后，建议按顺序继续：

```text
Wizard Step 02 UI
    ↓
Lip Builder
    ↓
Jaw Builder
    ↓
Eyelid Builder
    ↓
Brow Builder
    ↓
Corrective / Pose Driver
```
