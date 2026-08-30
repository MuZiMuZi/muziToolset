# Core API 使用手册

这份文档是 Core 的**人工维护使用指南**。

自动生成页面负责从源码 AST 同步函数签名；本页负责说明：

- 这个模块解决什么问题；
- 什么情况下应该调用它；
- 什么情况下不应该调用它；
- 常用 API 怎么组合；
- Core 与 Tool / System 的边界在哪里。

---

# 正式 Import 规则

正式 Core 模块已经统一使用 `snake_case`。

```python
from muziToolset.core import attr_utils
from muziToolset.core import hierarchy_utils
from muziToolset.core import joint_utils
from muziToolset.core import name_utils
from muziToolset.core import rename_utils
```

旧的 CamelCase 模块：

```text
attrUtils.py
hierarchyUtils.py
jointUtils.py
nameUtils.py
```

已经完成迁移并从正式 Core 删除。

!!! warning "不要在新代码中重新使用旧 CamelCase Import"

    GitHub Actions 已经加入 `Core Import Style Gate`。正式源码重新引用旧 CamelCase 模块时，CI 会直接失败。

---

# 快速选择模块

| 你想做什么 | 模块 |
| --- | --- |
| 清关键帧、Reset、动画 JSON | `animation_utils` |
| Scene / Selection / Set / Reference / FBX | `scene_utils` |
| JSON、目录、文件扫描 | `file_utils` |
| 世界位置、矩阵、距离 | `transform_utils` |
| OPM / multMatrix / Matrix Constraint | `matrix_utils` |
| Plug 连接 / 断开 | `connection_utils` |
| Parent / Point / Orient / Aim Constraint | `constraint_utils` |
| Attribute / Message / Limits | `attr_utils` |
| DAG Parent / Extra Group | `hierarchy_utils` |
| Joint / Joint Chain | `joint_utils` |
| 五段式 Rig 名称 | `name_utils` |
| Prefix / Suffix / Auto Number | `rename_utils` |
| Curve 采样 / Parameter / Attachment | `curve_utils` |
| Surface / Follicle | `surface_utils` |
| Model Duplicate | `mesh_utils` |
| SkinCluster / Weight | `skin_utils` |
| BlendShape / Corrective | `blendshape_utils` |
| Controller Shape | `control_shape_utils` |
| Object / Component Snap | `snap_utils` |
| 模型检查 | `model_check_utils` |
| 场景安全清理 | `scene_clean_utils` |

---

# 1. Animation

模块：

```python
from muziToolset.core import animation_utils
```

## 使用场景

- 删除控制器动画；
- Reset Transform；
- 导出一组 Controller 动画 JSON；
- 把动画 JSON 恢复到当前 Maya Scene。

## Reset Transform

```python
nodes = [
    "ctrl_md_root_001",
    "ctrl_md_cog_001",
]

animation_utils.reset_transform_channels(
    nodes
)
```

## 动画 JSON

```python
animation_utils.export_animation(
    nodes=[
        "ctrl_md_root_001",
        "ctrl_md_cog_001",
    ],
    file_path="D:/animation/walk.json"
)
```

恢复：

```python
animation_utils.import_animation(
    file_path="D:/animation/walk.json",
    clear_existing=True,
    strict=True
)
```

!!! info "为什么 Animation IO 不再单独一个文件"

    当前动画导入导出仍然属于 Animation 领域，因此已经从 `animation_io_utils.py` 收口到 `animation_utils.py`。

---

# 2. Scene / File

## Scene

```python
from muziToolset.core import scene_utils
```

适合：

```text
Node
Selection
Object Set
Undo
Callback
Open Scene
Import Scene
Reference
FBX
```

例如创建节点并 Match：

```python
node = scene_utils.create_node(
    node_type="transform",
    name="grp_md_test_001",
    match_node="jnt_md_spine_bind_001"
)
```

## File

```python
from muziToolset.core import file_utils
```

只处理硬盘文件：

```python
file_utils.write_json(
    "D:/rig/config.json",
    {
        "character": "hero",
        "version": 1,
    }
)
```

判断规则：

```text
需要 cmds.file() -> scene_utils
不需要 Maya       -> file_utils
```

---

# 3. Transform / Matrix / Connection / Constraint

这是 Rig 开发里最容易混淆的四个模块。

## Transform Utils

用于**读取 / 设置静态 Transform 数据**：

```python
from muziToolset.core import transform_utils

position = transform_utils.get_world_translation(
    "jnt_lf_hand_bind_001"
)
```

## Matrix Utils

用于**动态 Matrix 网络**：

```python
from muziToolset.core import matrix_utils

matrix_node = matrix_utils.create_parent_matrix_constraint(
    driver="ctrl_md_root_001",
    driven="grp_md_follow_001",
    maintain_offset=True
)
```

典型网络：

```text
driver.worldMatrix
        ↓
   multMatrix
        ↑
parent.worldInverseMatrix
        ↓
driven.offsetParentMatrix
```

!!! warning "不要重新读取 Driven 自己的 parentInverseMatrix 形成 OPM 回路"

    Matrix Constraint 应从真实 Parent 获取 `worldInverseMatrix[0]`，避免 Evaluation Graph 报 Cycle Warning。

## Connection Utils

用于普通 DG Plug：

```python
from muziToolset.core import connection_utils

connection_utils.connect_plugs(
    "ctrl_md_settings_001.stretch",
    "md_stretch_mult.input1X",
    force=True
)
```

## Constraint Utils

用于 Maya 原生 Constraint：

```python
from muziToolset.core import constraint_utils

constraint_utils.create_constraint(
    driver_objects=["ctrl_md_root_001"],
    driven_object="grp_md_follow_001",
    constraint_type="parentConstraint",
    maintain_offset=True
)
```

选择方式：

```text
只想连接属性        -> connection_utils
静态位置 / Matrix    -> transform_utils
OPM / multMatrix     -> matrix_utils
Maya Constraint Node -> constraint_utils
```

---

# 4. Attribute

```python
from muziToolset.core import attr_utils
```

## 创建属性

```python
attr = attr_utils.Attr(
    "ctrl_md_settings_001"
)

attr.add_attr(
    "stretch",
    attr_type="double",
    default_value=1.0,
    min_value=0.0,
    max_value=1.0,
    lock=False,
    hide=False
)
```

## Message Config

保存 Maya 节点引用时优先使用 Message：

```python
config_attr = attr_utils.Attr(
    "network_md_face_config_001"
)

config_attr.connect_message(
    source_node="model_md_head_base_001",
    attr="face_head_model",
    force=True,
    clear_empty=True
)
```

原因：

```text
String 保存 "model_md_head_base_001"
    ↓ Rename
字符串不会自动更新

Message Connection
    ↓ Rename
Maya 自动维护连接
```

Attribute Plug 的通用连接逻辑不会在这里再维护第二份，底层统一复用 `connection_utils`。

---

# 5. Hierarchy

```python
from muziToolset.core import hierarchy_utils
```

## 插入 Extra Group

```python
zero_group = hierarchy_utils.Hierarchy.add_extra_group(
    obj="ctrl_lf_hand_main_001",
    grp_name="zero_lf_hand_main_001",
    world_orient=False
)
```

流程：

```text
记录 Obj World Transform + Parent
          ↓
创建 Extra Group
          ↓
Group 对齐 Obj
          ↓
Group Parent 回原层级
          ↓
Obj Parent 到 Group
```

完整 Controller 层级不应该继续写在这里，应调用上层 Controller System。

---

# 6. Joint

```python
from muziToolset.core import joint_utils
```

## 创建 Joint

```python
joint = joint_utils.Joint.create(
    name="jnt_lf_elbow_bind_001",
    position=[3.0, 8.0, 0.0],
    radius=0.5
)
```

## Joint Label

```python
joint_utils.Joint(
    "jnt_lf_elbow_bind_001"
).tag()
```

当前正式 Side Token：

```text
lf / rt / md
```

同时兼容旧名称输入：

```text
l / r / m
```

## Curve CV 创建 Joint

```python
result = joint_utils.JointCurve.create_joints_on_curve_points(
    curve="crv_md_spine_guide_001",
    joint_base_name="jnt_md_spine_bind",
    parent_chain=True
)
```

`JointCurve` 的 Curve Query 已统一调用 `curve_utils`。

## Joint Chain

```python
joint_utils.JointChain.parent_joints_as_chain(
    [
        "jnt_md_spine_bind_001",
        "jnt_md_spine_bind_002",
        "jnt_md_spine_bind_003",
    ]
)
```

---

# 7. Naming

## 标准名称

```python
from muziToolset.core import name_utils

name = name_utils.Name.create_name(
    node_type="jnt",
    side="lf",
    part="upper_lid",
    function="bind",
    index=1
)
```

结果：

```text
jnt_lf_upper_lid_bind_001
```

## Side 兼容

```python
name_utils.Name.normalize_side("left")
# lf

name_utils.Name.normalize_side("r")
# rt

name_utils.Name.normalize_side("center")
# md
```

## Mirror Name

```python
mirror_name = name_utils.Name.mirror_name(
    "jnt_lf_upper_lid_bind_001"
)
```

结果：

```text
jnt_rt_upper_lid_bind_001
```

`name_utils` 负责的是“一个 Rig 名称应该是什么”，而不是批量 Selection Rename。

---

# 8. Batch Rename

```python
from muziToolset.core import rename_utils
```

## Pattern Rename

选择几个 Joint 后：

```python
rename_utils.pattern_rename(
    "jnt_md_spine_bind_***"
)
```

得到：

```text
jnt_md_spine_bind_001
jnt_md_spine_bind_002
jnt_md_spine_bind_003
```

`name_utils` 和 `rename_utils` 保持独立：前者负责名称语义，后者负责批量操作。

---

# 9. Curve

```python
from muziToolset.core import curve_utils
```

## 弧长均匀采样

```python
sample_data = curve_utils.sample_curve_by_length(
    curve="crv_md_spine_001",
    sample_count=5
)
```

返回：

```python
{
    "points": [],
    "tangents": [],
    "parameters": [],
}
```

## 最近 Parameter

```python
parameter = curve_utils.get_closest_parameter(
    curve="crv_lf_upper_lid_001",
    world_position=[3.0, 12.0, 1.5]
)
```

!!! warning "Parameter 不等于 0~1 百分比"

    多条 Curve 同步位置时先转换成 Arc Length Percentage。

```python
percentage = curve_utils.parameter_to_length_percentage(
    drive_curve,
    drive_parameter
)

parameter = curve_utils.length_percentage_to_parameter(
    aim_curve,
    percentage
)
```

## Curve Attachment

```python
attachment_data = curve_utils.create_point_on_curve_attachment(
    curve="crv_lf_upper_lid_001",
    parameter=parameter,
    name="attach_lf_upper_lid_001",
    parent="grp_lf_upper_lid_attach_001"
)
```

Parent 存在时自动处理：

```text
World Position
    ↓
composeMatrix
    ↓
multMatrix <- Parent World Inverse
    ↓
decomposeMatrix
    ↓
Child Local Translate
```

---

# 10. Surface

```python
from muziToolset.core import surface_utils
```

## Curve Loft Surface

```python
surface = surface_utils.create_surface_from_curve(
    curve="crv_md_ribbon_001",
    name="srf_md_ribbon_001",
    offset=0.25,
    offset_axis="Y"
)
```

## Follicle

```python
follicle = surface_utils.create_follicle(
    surface=surface,
    name="fol_md_ribbon_001",
    parameter_u=0.5,
    parameter_v=0.5
)
```

Joint / Controller 不由 Surface Utils 创建，由上层 Rig System 决定。

---

# 11. Mesh

```python
from muziToolset.core import mesh_utils
```

```python
work_model = mesh_utils.duplicate_model(
    source_model="model_md_head_base_001",
    new_name="model_md_head_tweak_001",
    parent="grp_md_face_model_001"
)
```

`duplicate_model()` 不复制 Input Connection / Upstream DG Network，适合制作相对独立的工作模型。

---

# 12. Skin

```python
from muziToolset.core import skin_utils
```

## 找 SkinCluster

```python
skin_cluster = skin_utils.find_skin_cluster(
    "model_md_body_geo_001"
)
```

## Copy Weight

```python
skin_utils.copy_skin_weights(
    source="model_md_body_geo_001",
    targets=[
        "model_md_shirt_geo_001",
        "model_md_pants_geo_001",
    ]
)
```

## Weight IO

```python
skin_utils.export_skin_weights(
    geometry="model_md_body_geo_001",
    directory="D:/weights/body"
)
```

---

# 13. BlendShape

```python
from muziToolset.core import blendshape_utils
```

## 添加或替换 Target

```python
result = blendshape_utils.add_or_replace_target(
    blendshape_node="bs_md_face_001",
    target_transform="model_md_smile_geo_001"
)
```

## 读取真实 Alias

```python
targets = blendshape_utils.get_targets(
    "bs_md_face_001"
)
```

这里使用真实 `alias -> weight[index]`，不假设 Target Index 连续。

---

# 14. Controller Shape

```python
from muziToolset.core import control_shape_utils
```

## Shape Radius

```python
radius = control_shape_utils.get_shape_radius(
    "ctrl_lf_hand_main_001"
)

control_shape_utils.set_shape_radius(
    "ctrl_lf_hand_main_001",
    4.0
)
```

## Mirror Shape

```python
control_shape_utils.mirror_shape(
    "ctrl_lf_hand_main_001",
    axis="x"
)
```

这里操作的是 Curve CV，不是 Transform Scale。

---

# 15. Snap

```python
from muziToolset.core import snap_utils
```

例如 Joint 放在两个 Vertex 中间：

```python
snap_utils.snap_to_average(
    reference_items=[
        "model_md_head_geo_001.vtx[100]",
        "model_md_head_geo_001.vtx[101]",
    ],
    target_item="jnt_md_nose_bind_001",
    include_rotation=False
)
```

Component 参与 Position，但不会被当作 Transform Rotation 参考。

---

# 16. Model Check

```python
from muziToolset.core import model_check_utils
```

```python
issues = model_check_utils.run_checks(
    nodes=["model_md_head_geo_001"]
)

for issue in issues:
    print(issue)
```

Issue：

```python
{
    "node": "model_md_head_geo_001",
    "type": "遗留建模历史",
    "details": "2 个节点：polyExtrudeFace",
    "fixable": True,
}
```

只有 `fixable=True` 才允许：

```python
model_check_utils.fix_issues(
    issues
)
```

---

# 17. Scene Clean

```python
from muziToolset.core import scene_clean_utils
```

```python
result = scene_clean_utils.run_cleanup(
    nodes=["grp_md_model_001"],
    selected_only=True,
    delete_empty=True,
    delete_history_enabled=True,
    freeze_enabled=False,
    delete_unknown_enabled=True
)
```

Scene Clean 会主动保护：

```text
Reference
Default Camera
AnimCurve
Constraint
SkinCluster
BlendShape
Wrap / Other Deformer
```

---

# 已验证的质量门槛

## Maya 2023 Extended Core Smoke

这批正式 Core 已经在 Maya 2023 真机运行：

```python
import muziToolset

muziToolset.extended_core_smoke_test()
```

已验证结果：

```text
attr_utils          PASS
hierarchy_utils     PASS
joint_utils         PASS
naming              PASS
model_check_utils   PASS
scene_clean_utils   PASS

Total: 6 | Passed: 6 | Failed: 0
```

## Tool Window Smoke

所有正式 UI Tool 的 Direct Main / Visible / Single Instance 已经在 Maya 2023 验证：

```python
muziToolset.tool_window_smoke_test()
```

已验证结果：

```text
Total: 17 | Passed: 17 | Failed: 0
```

## Core Import Style Gate

GitHub Actions 会执行：

```bash
python tests/core_import_style_test.py
```

它使用 Python AST 检查正式代码，确保已经退休的 CamelCase Core Import 不会重新进入仓库。

---

# Core 开发检查表

新增 Core API 前检查：

- [ ] 这个功能是否可以被多个 Tool / System 复用？
- [ ] 是否已经有同领域模块可以承载它？
- [ ] 文件名和 Import 是否统一为 `snake_case`？
- [ ] 是否意外读取 UI / Selection？
- [ ] 是否应该其实属于完整 Rig System？
- [ ] 是否有重复的 Matrix / Connection / Curve Helper？
- [ ] 模块头是否列出公开方法？
- [ ] Maya 特殊行为是否解释“为什么”？
- [ ] 大操作是否有 Undo Chunk？
- [ ] 是否需要补 Smoke Test？
- [ ] MkDocs API 是否能从 AST 正确读到函数签名？
- [ ] Core Import Style Gate 是否保持通过？

这份检查表的目标只有一个：**Core 保持稳定、清晰、可复用，不再重新长成万能工具类。**
