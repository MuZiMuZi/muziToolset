# Core 能力选择

`core/` 只放**可被多个 Tool / System 复用的 Maya 通用能力**。

如果一个功能已经包含完整 Rig 流程、控制器层级或 Face Component，它通常不应该继续放在 Core。

## 快速选择

| 我想做什么 | Core 模块 |
| --- | --- |
| 动画查询、清理、Reset | [pipelineUtils.py](../reference/core/bake/pipelineUtils.md) |
| Attribute / Message / Limits | [attr_utils.py](../reference/core/common/attr_utils.md) |
| BlendShape / Corrective | [blendShapeUtils.py](../reference/core/bake/blendShapeUtils.md) |
| Plug 连接 | [connectionUtils.py](../reference/core/bake/connectionUtils.md) |
| Constraint | [advUtils.py](../reference/core/bake/advUtils.md) |
| Controller Shape | [controlUtils.py](../reference/core/bake/controlUtils.md) |
| Curve | [guide_utils.py](../reference/core/rigging/guide_utils.md) |
| JSON / 路径 / 文件 | [fileUtils.py](../reference/core/bake/fileUtils.md) |
| DAG 层级 | [hierarchy_utils.py](../reference/core/common/hierarchy_utils.md) |
| Jnt | [jnt_utils.py](../reference/core/rigging/jnt_utils.md) |
| Matrix / OPM | [transform_utils.py](../reference/core/common/transform_utils.md) |
| Mesh | [meshUtils.py](../reference/core/bake/meshUtils.md) |
| 模型检查 | [model_checker.py](../reference/tools/clean/model_checker.md) |
| Rig 命名 / 批量 Rename | [name_utils.py](../reference/core/common/name_utils.md) |
| Scene / Selection / Set | [pipelineUtils.py](../reference/core/bake/pipelineUtils.md) |
| 场景清理 | [hierarchy_cleaner.py](../reference/tools/clean/hierarchy_cleaner.md) |
| Skin / Weight | [weightsUtils.py](../reference/core/bake/weightsUtils.md) |
| Snap | [snapUtils.py](../reference/core/bake/snapUtils.md) |
| Surface / Follicle | [guide_utils.py](../reference/core/rigging/guide_utils.md) |
| Transform / Matrix / Distance | [transform_utils.py](../reference/core/common/transform_utils.md) |

## Import

```python
from muziToolset.core import attr_utils
from muziToolset.core import hierarchy_utils
from muziToolset.core import jnt_utils
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
    Core 可以创建 Jnt、Curve、Matrix Node，但不应该知道“嘴唇 Rig 应该创建几层控制器”这类具体业务规则。

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
