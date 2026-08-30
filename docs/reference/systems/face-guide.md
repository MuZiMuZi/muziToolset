# Face Guide 工作流

`FaceGuide` 是 Muzi Toolset Face Rig 的 **Step 02 定位数据管理层**。

它不负责创建正式嘴唇、眉毛、眼皮 Joint，也不负责创建动画 Controller。
它的主要任务是把 `resources/face/face_guide.ma` 这份 Maya Guide 模板稳定地加载到 Face Rig 场景中，并向后续 Builder 提供清晰、有顺序、可验证的 Guide 数据。

---

## 1. 设计职责

当前 Face Guide 系统分为三层：

```text
resources/face/face_guide.ma
        │
        │ 静态模板
        ▼
FaceGuide
        │
        │ 有序 Guide 数据
        ▼
Lip / Brow / Eyelid / Jaw Builder
        │
        ▼
Curve / Joint / Controller
```

### `face_guide.ma` 负责

模板文件负责视觉和初始场景结构：

```text
Guide Locator
Guide Zero Group
Guide Group
Face Move Ctrl
左右 Guide 节点
默认 LF -> RT 连接
Locator 颜色
Locator Shape 大小
初始 Guide 位置
```

这些内容属于 Maya 模板本身，不由 Python 在每次 Build 时重新创建。

### `FaceGuide` 负责

`systems/face/face_guide.py` 负责运行时管理：

```text
读取 Step 01 配置
加载 Guide 模板
删除 / 重置 Guide
查询 Guide
读取世界坐标
整理各部位 Guide 顺序
检查 Guide 完整性
检查左右镜像
修复损坏的镜像关系
保存 Guide Config
完成 Step 02
```

### 后续 Builder 负责

例如未来的 Lip Builder：

```text
FaceGuide.get_lip_guides()
        ↓
得到有顺序的 Locator
        ↓
LipBuilder 创建 Curve
        ↓
根据 mouth_jnt_number 创建 Joint
        ↓
创建 Controller / Deform Network
```

因此不要在 `FaceGuide` 里直接创建正式 Lip Curve 或 Lip Joint。

---

# 2. 使用前提

使用 Step 02 以前必须先完成 Step 01：

```python
from muziToolset.systems.face import FaceSetup

setup = FaceSetup(
    face_head_model="head_geo",
    mouth_jnt_number=40
)

setup.build()
```

Step 01 会把模型引用和构建参数保存到 Face Config Network Node。

`FaceGuide` 会通过 `FaceBase.refresh_setup_data()` 读取这些最新配置。

---

# 3. 标准使用流程

推荐工作流只有四个主要阶段：

```text
Build Guide
    ↓
手动贴合角色
    ↓
Validate Guide
    ↓
Finalize Guide
```

## 3.1 创建 FaceGuide 对象

```python
from muziToolset.systems.face import FaceGuide

guide = FaceGuide()
```

这里只创建 Python 管理对象，不会自动修改 Maya 场景。

---

## 3.2 Build Guide

```python
result = guide.build()
```

`build()` 会执行：

```text
检查 Step 01
    ↓
确保 Face 主层级存在
    ↓
检查 face_guide.ma
    ↓
导入或复用 Guide
    ↓
保存 Guide Root / Move Ctrl 到 Config
    ↓
Step 02 保持未完成状态
```

返回值示例：

```python
{
    "imported": True,
    "guide_root": "grp_md_face_guide_001",
    "guide_move_ctrl": "ctrl_md_face_move_001",
    "new_nodes": [...]
}
```

如果 Guide 已经存在，再次执行 `build()` 不会重复导入模板。

---

# 4. 为什么 Build 后 Step 02 还没有完成

Face Guide 天生需要绑定师手动贴合角色。

因此：

```python
guide.build()
```

只代表：

> Guide 已经准备好，可以开始调整。

并不代表：

> Guide 已经可以直接交给正式 Rig Builder。

绑定师需要在 Maya 里调整：

```text
Lip
Eye
Eyelid
Brow
Nose
Jaw
Cheek / Zygoma
Ear
Teeth
Tongue
```

完成贴合后再执行 `finalize()`。

---

# 5. 检查 Guide

```python
report = guide.validate_guides()
print(report)
```

返回结构：

```python
{
    "valid": True,
    "errors": [],
    "warnings": [],
    "guide_count": 0,
    "symmetry": {...}
}
```

建议 UI 不要只显示一个 `True / False`，而是把 `errors` 和 `warnings` 展示出来。

这样以后 Wizard Step 02 可以显示类似：

```text
✓ Face Guide Template
✓ Lip Guide
✓ Eye Guide
✓ Left / Right Symmetry

✕ loc_lf_mouth_corner_guide_001 missing
⚠ Right Brow connection broken
```

---

# 6. Finalize Guide

绑定师完成手动调整后：

```python
report = guide.finalize()
```

`finalize()` 会：

```text
重新读取 Step 01
    ↓
检查 Guide
    ↓
检查左右镜像
    ↓
保存 Guide Config
    ↓
step_02_completed = True
    ↓
Step 03 / 04 标记为未完成
```

如果 Validation 失败，会直接抛出 `RuntimeError`，并列出具体缺失内容。

---

# 7. 重置 Guide

如果 Guide 被改乱，希望恢复模板初始状态：

```python
guide.reset_guide()
```

它等价于：

```text
删除当前 Guide 内容
    ↓
重新导入 face_guide.ma
    ↓
重新保存 Config
    ↓
Step 02 标记为未完成
```

注意：

`reset_guide()` 会删除当前已经手动调整过的 Guide 数据。

---

# 8. 删除 Guide

```python
guide.remove_guide()
```

只会删除：

```text
grp_md_face_guide_001
    └── 模板内容
```

不会删除系统级的：

```text
grp_md_face_guide_001
```

因为这个 Group 属于 `FaceBase.ensure_hierarchy()` 创建的 Face Rig 主层级。

---

# 9. 通用 Guide 查询

## 获取全部 Locator

```python
locators = guide.get_guide_locators()
```

返回：

```python
[
    "|...|loc_lf_eye_ball_guide_001",
    "|...|loc_lf_upper_lid_guide_001",
    ...
]
```

---

## 根据短名称获取 Guide

```python
node = guide.get_guide_node(
    "loc_lf_eye_ball_guide_001",
    required=True
)
```

`required=True` 时，如果节点不存在会直接报错。

`required=False` 时，不存在返回 `None`。

---

## 获取 Guide 世界坐标

```python
position = guide.get_world_position(
    "loc_lf_eye_ball_guide_001"
)
```

返回：

```python
[x, y, z]
```

---

## 批量获取世界坐标

```python
positions = guide.get_guide_positions(
    guides
)
```

返回顺序和输入 Guide 顺序完全一致。

这一点非常重要，因为后续 Curve Builder 必须依赖稳定的点顺序。

---

# 10. 嘴唇 Guide

```python
lip_data = guide.get_lip_guides()
```

返回：

```python
{
    "upper": [...],
    "lower": [...],
    "corners": [...]
}
```

Upper / Lower 的方向统一为：

```text
RT Mouth Corner
    ↓
RT Lip
    ↓
MD Lip
    ↓
LF Lip
    ↓
LF Mouth Corner
```

因此后面的 Lip Builder 不需要自己猜 Locator 顺序。

示例：

```python
lip_data = guide.get_lip_guides()

upper_positions = guide.get_guide_positions(
    lip_data["upper"]
)

lower_positions = guide.get_guide_positions(
    lip_data["lower"]
)
```

后续就可以用这些位置创建 Upper / Lower Lip Curve。

---

# 11. 眼皮 Guide

```python
left_lid = guide.get_eyelid_guides(
    "lf"
)
```

返回：

```python
{
    "upper": [...],
    "lower": [...]
}
```

Upper 顺序：

```text
Inner
Upper 001
Upper 002
Upper 003
Outer
```

Lower 顺序：

```text
Inner
Lower 001
Lower 002
Lower 003
Outer
```

例如：

```python
upper_positions = guide.get_guide_positions(
    left_lid["upper"]
)
```

后续 Eyelid Builder 可以直接用这五个点创建 Eyelid Curve。

---

# 12. Brow Guide

```python
left_brow = guide.get_brow_guides(
    "lf"
)
```

返回：

```python
{
    "main": "...",
    "points": [...],
    "all": [...]
}
```

其中：

- `main` 是 Brow 主 Guide；
- `points` 是实际眉毛定位点；
- `all` 是全部 Brow Locator。

---

# 13. 其它部位查询

## Eye

```python
eye_data = guide.get_eye_guides(
    "lf"
)
```

返回：

```python
{
    "eye_ball": "...",
    "eye_iris": "..."
}
```

## Eye Bag

```python
eye_bag_guides = guide.get_eye_bag_guides(
    "lf"
)
```

## Nose

```python
nose_guides = guide.get_nose_guides()
```

## Jaw

```python
jaw_guides = guide.get_jaw_guides()
```

## Teeth

```python
teeth_guides = guide.get_teeth_guides()
```

## Tongue

```python
tongue_guides = guide.get_tongue_guides()
```

## Ear

```python
left_ear_guides = guide.get_ear_guides(
    side="lf"
)
```

## Zygoma

```python
zygoma_guides = guide.get_zygoma_guides()
```

---

# 14. 通用 Part 查询

如果以后模板增加新部位，不一定马上需要增加专门方法。

可以先使用：

```python
result = guide.get_part_guides(
    part="cheek",
    side="lf"
)
```

还可以增加 Token 限制：

```python
result = guide.get_part_guides(
    part="lid",
    side="lf",
    include_tokens=["upper"],
    exclude_tokens=["bag"]
)
```

这个接口主要用于开发和扩展。

正式 Builder 更推荐调用具有明确语义的方法，例如：

```python
get_lip_guides()
get_eyelid_guides()
get_brow_guides()
```

因为这些方法可以保证顺序和数据结构。

---

# 15. 左右镜像系统

正常 Face Guide 的左右结构已经保存于：

```text
resources/face/face_guide.ma
```

因此正常流程：

```python
guide.build()
```

**不会重新创建 Right Guide。**

这是刻意设计的。

模板负责：

```text
LF Guide
RT Guide
Zero Mirror Space
LF -> RT Transform Connection
LF Shape -> RT Shape Connection
```

Python 只负责检查。

---

# 16. 检查左右镜像

```python
symmetry_report = guide.validate_symmetry()
```

返回：

```python
{
    "valid": True,
    "missing_nodes": [],
    "wrong_parents": [],
    "broken_connections": []
}
```

这个函数不会修改场景。

---

# 17. Repair Symmetry

只有 Guide 镜像结构被破坏时才使用：

```python
result = guide.repair_symmetry()
```

例如：

```text
Right Locator 被删除
Right Zero Parent 被改错
LF -> RT Connection 被断开
```

`repair_symmetry()` 会尝试恢复它们。

### Nested Guide

新的 Repair 逻辑会区分 Root Guide 和 Nested Guide。

例如：

```text
loc_lf_eye_ball
    └── zero_lf_eye_iris
```

对应右侧必须是：

```text
loc_rt_eye_ball
    └── zero_rt_eye_iris
```

而不是：

```text
loc_lf_eye_ball
    └── zero_rt_eye_iris
```

同样，Nested Zero 已经位于右侧镜像 Parent Space 中，不会再次创建第二次负 X Scale。

---

# 18. 旧 Mirror API

为了兼容开发阶段已有调用，下面两个 API 暂时保留：

```python
guide.mirror_left_guide(
    left_zero_group
)
```

以及：

```python
guide.mirror_left_guides()
```

但新代码应优先使用：

```python
guide.repair_symmetry()
```

旧函数现在属于 Repair Helper，不属于标准 Build 工作流。

---

# 19. Face Config 保存的数据

Step 01 常见 Message：

```text
face_head_model
face_lf_eye_model
face_rt_eye_model
upper_teech_model
lower_teech_model
face_tongue_model
face_gum_model
```

Step 01 Value：

```text
mouth_jnt_number
```

Step 02 新增：

```text
face_guide_root
face_guide_move_ctrl
face_guide_version
```

Step 状态：

```text
step_01_completed
step_02_completed
step_03_completed
step_04_completed
```

节点引用使用 Maya Message 保存，不使用节点名称 String。

---

# 20. Step 状态规则

Step 01 重新 Build：

```text
Step 01 = True
Step 02 = False
Step 03 = False
Step 04 = False
```

Guide Build：

```text
Step 02 = False
Step 03 = False
Step 04 = False
```

Guide Finalize：

```text
Step 02 = True
Step 03 = False
Step 04 = False
```

这样 Wizard 可以判断后续数据是不是已经过期。

---

# 21. Maya 开发测试建议

修改 `face_base.py` / `face_guide.py` 后，建议在 Maya 2023 新场景中按以下顺序测试。

## Test 01 - Step 01

```python
from muziToolset.systems.face import FaceSetup

setup = FaceSetup(
    face_head_model="你的头部模型",
    mouth_jnt_number=40
)

setup.build()
```

检查：

```text
Face 主层级创建成功
Config Network Node 存在
三个 Head 工作模型存在
step_01_completed = True
```

## Test 02 - Guide Build

```python
from muziToolset.systems.face import FaceGuide

guide = FaceGuide()
result = guide.build()
print(result)
```

检查：

```text
face_guide.ma 正常导入
grp_md_face_guide_001 没有出现重复正式 Root
ctrl_md_face_move_001 存在
Guide Locator 颜色保持模板颜色
LF / RT Connection 保持正常
```

## Test 03 - Query

```python
print(
    guide.get_lip_guides()
)

print(
    guide.get_eyelid_guides("lf")
)

print(
    guide.get_brow_guides("lf")
)
```

检查返回顺序是否符合预期。

## Test 04 - Validation

```python
report = guide.validate_guides()
print(report)
```

## Test 05 - Repair

手动断开一个 LF -> RT Connection 后：

```python
print(
    guide.validate_symmetry()
)

guide.repair_symmetry()

print(
    guide.validate_symmetry()
)
```

## Test 06 - Finalize

```python
guide.finalize()
```

检查：

```text
step_02_completed = True
face_guide_root Message 正常
face_guide_move_ctrl Message 正常
```

---

# 22. 下一阶段

`FaceGuide` 稳定后，建议按下面顺序继续：

```text
01. Wizard Step 02 UI 接入
02. Lip Builder
03. Jaw Builder
04. Eyelid Builder 接入 Guide
05. Brow Builder
06. Nose / Cheek / Zygoma
07. Corrective / Pose Driver
```

其中 Lip / Eyelid / Brow Builder 不应该直接用 `cmds.ls()` 猜 Guide。

推荐始终通过：

```text
FaceGuide
    ↓
有语义、有顺序的数据
    ↓
Builder
```

这样后续即使修改 `face_guide.ma` 的内部层级，只要 FaceGuide 的公开 API 保持稳定，正式绑定模块就不需要跟着大改。
