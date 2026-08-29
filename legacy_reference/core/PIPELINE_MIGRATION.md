# pipelineUtils Migration Complete

旧 `pipelineUtils.py` 曾经同时承担动画、场景、约束、Curve、Surface、Face、Controller、Hair 等多种职责。

该万能 `Pipeline` 类现已完成拆分，并从仓库中删除。正式代码不得恢复或重新 import 旧实现。

## Maya 2023 验证结果

迁移完成前的最终真机测试：

```text
muziToolset.pipeline_smoke_test()
Total: 9 | Passed: 9 | Failed: 0

muziToolset.controller_component_smoke_test()
Total: 1 | Passed: 1 | Failed: 0
```

Matrix Parent Constraint 的 offsetParentMatrix 循环警告也已修复，最终测试无 cycle warning。

## Core 正式替代

| 旧职责 | 正式位置 |
| --- | --- |
| 动画清除 / Controller TRS Reset | `core.animation_utils` |
| 动画 JSON IO | `core.animation_io_utils` |
| Transform / Distance / Matrix Query | `core.transform_utils` |
| Matrix / offsetParentMatrix Constraint | `core.matrix_utils` |
| 属性连接 | `core.connection_utils` |
| Maya 原生 Constraint | `core.constraint_utils` |
| Scene / Object Set / Callback / Undo | `core.scene_utils` |
| Curve 查询 / 采样 / Attachment | `core.curve_utils` |
| Surface / Follicle | `core.surface_utils` |
| Mesh Duplicate | `core.mesh_utils` |
| Skin Weight | `core.skin_utils` |
| 文件 / JSON | `core.file_utils` |
| Maya Scene / Reference / FBX | `core.scene_io_utils` |

## System 正式替代

| 旧 Pipeline Workflow | 正式位置 |
| --- | --- |
| `create_eyelid_joints_on_curve` | `systems.face.eyelid` |
| `attach_joints_on_curve` | `systems.face.curve_attachment` |
| `create_zip_lip` | `systems.face.lip.build_zip_lip` |
| `create_doble_constraint` | `systems.controller.create_parent_space_blend` |
| 标准 Controller 创建 / 层级 | `systems.controller` |

## 明确淘汰的旧逻辑

以下旧实现不迁移：

- `add_face_tag` / `remove_non_face_objs`：旧发布约定且具有破坏性；
- `list_operation`：直接使用 Python `set` 即可；
- `copy_surface_create_geo`：旧实现存在未定义变量，配套自动权重流程未完成；
- `create_logging`：使用 Python 标准 `logging`；
- `batch_Constraints_modle` / `batch_Constraints_joint`：正式 Core + Controller System 已可组合完成，不保留黑盒 Workflow；
- `create_dynamic_curve_driven`：旧 nHair / Joint / Spline IK 大流程不迁移，未来 Hair System 从零设计。

## 其它 Legacy Core 迁移

旧 Core 中的有效能力也已经完成整理：

- `connectionUtils.py` -> `core.connection_utils`
- `vectorUtils.py` Matrix 部分 -> `core.matrix_utils`
- `fileUtils.py` -> `core.file_utils` / `core.scene_io_utils` / `core.animation_io_utils`
- `controlUtils.py` Shape 能力 -> `core.control_shape_utils`
- `weightsUtils.py` 有效 Skin 能力 -> `core.skin_utils`
- `controlUtils.py` 中剩余 Ribbon / IK Spine / IK Curve Rig 参考 -> `legacy_reference/rigging/controlUtils.py`
- AdvancedSkeleton / MetaHuman 参考 -> `legacy_reference/integrations/`

## 最终状态

`legacy_reference/core/` 现在只保存这份迁移记录，不再是 Python Package，也不再包含历史 Core 实现。

需要新功能时，应按职责进入 `core/`、`tools/` 或 `systems/`，不要重新创建万能 Utils 类。
