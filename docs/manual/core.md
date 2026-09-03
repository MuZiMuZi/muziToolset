# Core 能力选择

`core/` 只放**可被多个 Tool / System 复用的 Maya 通用能力**。

如果一个功能已经包含完整 Rig 流程、控制器层级或 Face Component，它通常不应该继续放在 Core。

## 快速选择

| 我想做什么 | Core 模块 |
| --- | --- |
| 动画查询、清理、Reset | [animation_utils.py](../reference/core/animation_utils.md) |
| Attribute / Message / Limits | [attr_utils.py](../reference/core/attr_utils.md) |
| BlendShape / Corrective | [blendshape_utils.py](../reference/core/blendshape_utils.md) |
| Plug 连接 | [connection_utils.py](../reference/core/connection_utils.md) |
| Constraint | [constraint_utils.py](../reference/core/constraint_utils.md) |
| Controller Shape | [control_shape_utils.py](../reference/core/control_shape_utils.md) |
| Curve | [curve_utils.py](../reference/core/curve_utils.md) |
| JSON / 路径 / 文件 | [file_utils.py](../reference/core/file_utils.md) |
| DAG 层级 | [hierarchy_utils.py](../reference/core/hierarchy_utils.md) |
| Joint | [joint_utils.py](../reference/core/joint_utils.md) |
| Matrix / OPM | [matrix_utils.py](../reference/core/matrix_utils.md) |
| Mesh | [mesh_utils.py](../reference/core/mesh_utils.md) |
| 模型检查 | [model_check_utils.py](../reference/core/model_check_utils.md) |
| Rig 命名 / 批量 Rename | [rename_utils.py](../reference/core/rename_utils.md) |
| Scene / Selection / Set | [scene_utils.py](../reference/core/scene_utils.md) |
| 场景清理 | [scene_utils.py](../reference/core/scene_utils.md) |
| Skin / Weight | [skin_utils.py](../reference/core/skin_utils.md) |
| Snap | [snap_utils.py](../reference/core/snap_utils.md) |
| Surface / Follicle | [surface_utils.py](../reference/core/surface_utils.md) |
| Transform / Matrix / Distance | [transform_utils.py](../reference/core/transform_utils.md) |

## Import

```python
from muziToolset.core import attr_utils
from muziToolset.core import hierarchy_utils
from muziToolset.core import joint_utils
```

## 判断一个功能该不该进 Core

```text
多个模块都需要同一 Maya 算法？
        │
       是
        ↓
      Core

只负责 UI / Selection？
        ↓
      Tools

已经是完整 Rig Component？
        ↓
     Systems
```

!!! warning "Core 不负责完整业务流程"
    Core 可以创建 Joint、Curve、Matrix Node，但不应该知道“嘴唇 Rig 应该创建几层控制器”这类具体业务规则。

## 查看详细方法

进入具体 `.py` API 页面后，可以直接查看：

- 方法作用
- Signature
- 参数类型和说明
- 默认值
- 返回值
- 异常
- 示例

[打开 Core API](../reference/core/index.md){ .md-button .md-button--primary }
[查看总体架构](../architecture/index.md){ .md-button }
