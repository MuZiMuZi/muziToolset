# pipelineUtils Migration Map

`legacy_reference/core/pipelineUtils.py` 是早期的综合工具类，包含场景、动画、约束、Curve、Surface、Face、Controller、Hair 等多种职责。

正式代码不再恢复 `Pipeline` 万能类。旧函数按职责迁入独立 Core 模块或完整 Rig System。

## 状态说明

- ✅ **已迁移**：已有正式替代 API。
- ♻️ **已有替代**：功能已经被正式模块覆盖，不再重复迁移。
- 🧩 **迁入 System**：属于完整 Rig Workflow，不放回 Core。
- 🗑 **淘汰**：旧实现不再保留为正式 API；未来如需要，应重新设计。

## 通用 Core

| 旧 Pipeline 方法 | 状态 | 正式位置 | 说明 |
| --- | --- | --- | --- |
| `clear_keys` | ✅ | `core.animation_utils.clear_animation_keys` | 支持全场景或指定节点。 |
| `reset_control` | ✅ | `core.animation_utils.reset_controls` | 只重置标准 TRS；Rig 自定义属性由对应 System 管理。 |
| `distence_between` | ✅ | `core.transform_utils.distance_between` | 修正旧拼写错误。 |
| `move` | ✅ | `core.transform_utils.move_relative` | 明确相对移动和空间参数。 |
| `make_undo` | ✅ | `core.scene_utils.undo_chunk` | 使用 try/finally 保证关闭 Undo Chunk。 |
| `create_node` | ✅ | `core.scene_utils.create_node` | 可匹配 Transform、指定 Parent。 |
| `get_selected_type` | ✅ | `core.scene_utils.get_selected_nodes` / `require_selected_nodes` | 不再把选择检查和 warning 写死在一个函数里。 |
| `create_native_script_job` | ✅ | `core.scene_utils.create_native_event_callback` | 改用 `maya.api.OpenMaya`。 |
| `create_set` | ✅ | `core.scene_utils.ensure_object_set` | 支持复用 Set 和父 Set。 |
| `create_constraint` | ✅ | `core.constraint_utils.create_constraint` | Driver / Driven 参数明确。 |
| `create_constraints` | ✅ | `core.constraint_utils.create_constraints` | 支持一组 Driver 批量约束多个 Driven。 |
| `select_constraints` | ✅ | `core.constraint_utils.get_constraints` | 选择行为留在 UI，Core 只查询。 |
| `delete_constraints` | ✅ | `core.constraint_utils.delete_constraints` | 返回实际删除节点。 |
| `get_percentages` | ✅ | `core.curve_utils.get_even_percentages` | 对非法 sample count 明确报错。 |
| `get_dag_path` | ✅ | `core.curve_utils.get_dag_path` | Maya API 2.0。 |
| `get_point_on_curve` | ✅ | `core.curve_utils.sample_curve_by_length` | 返回普通 Python 坐标和 tangent 数据。 |
| Curve Parameter Sync | ✅ | `core.curve_utils.parameter_to_length_percentage` / `length_percentage_to_parameter` | 多条 Curve 不再直接共享 raw parameter。 |
| Curve Attachment | ✅ | `core.curve_utils.create_point_on_curve_attachment` | Parent 下自动做 World -> Local Matrix 转换。 |
| `create_curve_on_joints` | ✅ | `core.curve_utils.create_curve_from_nodes` | 不再限定输入一定是 Joint。 |
| `create_curve_on_polyToCurve` | ✅ | `core.curve_utils.create_curve_from_selected_edges` | 明确要求 Polygon Edge Selection。 |
| `get_curve_number` | ✅ | `core.curve_utils.get_curve_cv_count` | 直接读取 CV，不使用 spans + degree 推算。 |
| `create_surface_on_curve` | ✅ | `core.surface_utils.create_surface_from_curve` | 不再移动或删除原始 Curve。 |
| `create_joint_follicle_on_surface` | 部分 ✅ | `core.surface_utils.create_follicle` / `create_even_follicles` | Core 只负责 Follicle；Joint / Ctrl / Set 由上层 System 创建。 |
| `duplicate_model` | ♻️ | `core.mesh_utils.duplicate_model` | 已经有正式实现。 |
| Skin Weight Copy | ♻️ | `core.skin_utils` | 不再从 Pipeline 提供第二套入口。 |

## Joint / Curve Rig

| 旧 Pipeline 方法 | 状态 | 正式方向 | 说明 |
| --- | --- | --- | --- |
| `create_joints_on_curve` | ♻️ | `core.jointUtils.JointCurve` + `core.curve_utils` | Joint 创建属于 Joint 模块，等距采样属于 Curve Core。 |
| `create_eyelid_joints_on_curve` | ✅ | `systems.face.eyelid` | 重构为眼皮 / 眼袋共用的放射状 Joint Builder。 |
| `attach_joints_on_curve` | ✅ | `systems.face.curve_attachment.attach_joints_to_curves` | Drive / Aim / Up Curve 使用统一弧长百分比同步。 |
| `create_doble_constraint` | ✅ | `systems.controller.create_parent_space_blend` | 重构为标准 Controller Parent Space / Follow Blend，并使用真实 Constraint Weight Alias。 |

## Face

| 旧 Pipeline 方法 | 状态 | 正式方向 | 说明 |
| --- | --- | --- | --- |
| `create_zip_lip` | ✅ | `systems.face.lip.build_zip_lip` | 已重构为 Matrix Zip Lip，不再使用每 Joint ParentConstraint 做闭合混合。 |
| `add_face_tag` | 🗑 | 不迁移 | `isFace` 是旧发布约定，当前 Face Rig 不依赖。以后如果做 Publish，应重新设计 metadata。 |
| `remove_non_face_objs` | 🗑 | 不迁移 | 会直接删除未标记 Transform，破坏性过高，不允许成为通用 Core API。 |

## Controller / Rig Workflow

| 旧 Pipeline 方法 | 状态 | 正式方向 | 说明 |
| --- | --- | --- | --- |
| `batch_Constraints_modle` | ♻️ / 🗑 | `systems.controller` + `core.skin_utils` + `core.constraint_utils` | 旧函数重复创建 Joint、Skin、Controller、Hierarchy、Constraint；正式模块已可组合完成，不保留一键黑盒 API。 |
| `batch_Constraints_joint` | ♻️ / 🗑 | `systems.controller` + `core.constraint_utils` | 标准 Controller Builder 已覆盖层级和输出节点，不保留旧重复实现。 |

## Hair / Dynamics

| 旧 Pipeline 方法 | 状态 | 正式方向 | 说明 |
| --- | --- | --- | --- |
| `create_dynamic_curve_driven` | 🗑 | Future `systems/hair` 重写 | 旧实现同时操作 MakeCurvesDynamic、Joint、Spline IK、Set、Hierarchy，并包含旧调用问题；未来 Hair System 从零设计，不复制旧实现。 |

## 淘汰

| 旧 Pipeline 方法 | 状态 | 说明 |
| --- | --- | --- |
| `list_operation` | 🗑 | 只是 Python `set` 运算，没有必要维护 Maya 专用 API。 |
| `copy_surface_create_geo` | 🗑 | 旧实现包含未定义的 `self.geo` / `geo`，且对应的自动权重流程本身未完成。 |
| `create_logging` | 🗑 | Python 标准 `logging` 足够；如以后需要项目日志系统，应单独设计。 |

## 其它 Legacy Core 已完成迁移

本轮额外完成：

- `connectionUtils.py` -> `core.connection_utils`
- `vectorUtils.py` Matrix 部分 -> `core.matrix_utils`
- `fileUtils.py` -> `core.file_utils` + `core.scene_io_utils` + `core.animation_io_utils`
- `controlUtils.py` Shape 能力 -> `core.control_shape_utils`
- `pipelineUtils.create_doble_constraint` -> `systems.controller.space_blend`
- `weightsUtils.py` 的有效 Skin IO / Copy 能力 -> `core.skin_utils`

## legacy pipelineUtils.py 删除条件

目前通用能力和有价值的 Face / Controller 算法已经完成迁移，剩余旧 Workflow 也已经明确淘汰或决定未来从零重写。

正式运行代码不允许 import `legacy_reference.core.pipelineUtils`。

在删除 `legacy_reference/core/pipelineUtils.py` 前，只保留最后一个验证门槛：

1. Maya 2023 `muziToolset.pipeline_smoke_test()` 新版 9 项全部通过；
2. Maya 2023 `muziToolset.controller_component_smoke_test()` 通过；
3. Face Component Smoke Test 如继续用于 Face System 验证，也应保持通过。

验证通过后即可删除旧 `pipelineUtils.py`，不再保留第二套实现。
