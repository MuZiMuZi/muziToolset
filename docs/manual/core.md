# Core 能力选择指南

`core/` 是 MuziTools 的 Maya 通用底层能力层。

使用 Core 时，先问一个问题：

> 这个能力是否应该被多个 Tool / System 重复使用？

如果答案是“是”，它通常属于 Core；如果它已经包含完整绑定流程、Controller 层级或某个 Face Component，则更可能属于 `systems/`。

## 快速选择模块

| 你想做什么 | 模块 |
| --- | --- |
| 动画清理、Reset、动画数据 | `animation_utils.py` |
| Attribute / Message / Limits | `attr_utils.py` |
| BlendShape / Corrective | `blendshape_utils.py` |
| Plug 连接 / 断开 | `connection_utils.py` |
| Parent / Point / Orient / Aim Constraint | `constraint_utils.py` |
| Controller Shape | `control_shape_utils.py` |
| Curve 采样 / Parameter / Attachment | `curve_utils.py` |
| JSON、目录、路径 | `file_utils.py` |
| DAG Parent / Extra Group | `hierarchy_utils.py` |
| Joint / Joint Chain | `joint_utils.py` |
| Matrix / OPM / multMatrix | `matrix_utils.py` |
| Model Duplicate | `mesh_utils.py` |
| 模型检查 | `model_check_utils.py` |
| 五段式 Rig 名称 | `name_utils.py` |
| Prefix / Suffix / Auto Number | `rename_utils.py` |
| Scene / Selection / Set / Reference | `scene_utils.py` |
| 场景安全清理 | `scene_clean_utils.py` |
| SkinCluster / Weight | `skin_utils.py` |
| Object / Component Snap | `snap_utils.py` |
| Surface / Follicle | `surface_utils.py` |
| 世界位置、矩阵、距离 | `transform_utils.py` |

## 正式 Import

```python
from muziToolset.core import attr_utils
from muziToolset.core import hierarchy_utils
from muziToolset.core import joint_utils
from muziToolset.core import matrix_utils
```

正式模块统一使用 `snake_case`。

!!! warning "不要重新引入旧 CamelCase Core"

    `attrUtils.py`、`jointUtils.py`、`nameUtils.py` 等旧入口已经退出正式架构。
    Docs CI 会检查正式源码，避免旧 Import 重新进入项目。

## 常见组合

### 保存 Maya 节点引用

优先使用 Message，而不是字符串节点名：

```python
from muziToolset.core import attr_utils

config_attr = attr_utils.Attr(
    "network_md_face_config_001"
)

config_attr.connect_message(
    source_node="head_geo",
    attr="face_head_model"
)
```

这样节点 Rename 后连接仍然有效。

### 创建层级后匹配目标

```python
from muziToolset.core import hierarchy_utils
from muziToolset.core import transform_utils

zero_group = hierarchy_utils.Hierarchy.create_grp(
    "zero_md_example_001"
)

transform_utils.match_transform(
    target="jnt_md_example_001",
    source=zero_group
)
```

具体 Signature 以当前生成的 API 页面为准。

### Curve 驱动绑定

```text
curve_utils
    ↓
Attachment / Parameter
    ↓
joint_utils / systems
```

Core 只负责通用 Curve 与 Joint 能力；完整 Eyelid / Lip 逻辑仍放在 `systems/face/`。

## 不应该放进 Core 的内容

下面这些通常不应该继续塞进 Core：

- 某个具体 Face Component 的 Build 流程；
- PySide 窗口和按钮行为；
- 完整 Controller Rig 层级；
- 只服务一个工具的临时业务逻辑；
- 依赖某个项目角色命名的特殊流程。

## 查具体参数

进入 [Core API](../reference/core/index.md)。

每个 `.py` 文件现在都有独立页面，并展开：

```text
Signature
参数
默认值
返回值
异常
示例
Notes
```

例如直接搜索：

```text
Attr.connect_message
create_closest_point_attachment
create_joint_chain
matrix_constraint
```
