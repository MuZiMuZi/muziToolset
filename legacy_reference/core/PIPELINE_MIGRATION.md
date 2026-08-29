# pipelineUtils Migration Map

`legacy_reference/core/pipelineUtils.py` 是早期的综合工具类，包含场景、动画、约束、Curve、Surface、Face、Controller、Hair 等多种职责。

正式代码不再恢复 `Pipeline` 万能类。旧函数按职责迁入独立 Core 模块或完整 Rig System。

## 状态说明

- ✅ **已迁移**：已有正式替代 API。
- ♻️ **已有替代**：功能已经被正式模块覆盖，不再重复迁移。
- 🧩 **迁入 System**：属于完整 Rig Workflow，不能放回 Core。
- ⏸ **暂缓**：当前正式工具没有调用，保留旧实现供后续判断。
- 🗑 **淘汰**：不建议继续保留为正式 API。

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
| `create_joints_on_curve` | ♻️ / 重构中 | `core.jointUtils.JointCurve` + `core.curve_utils` | Joint 创建属于 Joint 模块，等距采样属于 Curve Core。 |
| `create_eyelid_joints_on_curve` | ✅ | `systems.face.eyelid` | 重构为眼皮 / 眼袋共用的放射状 Joint Builder。 |
| `attach_joints_on_curve` | ✅ | `systems.face.curve_attachment.attach_joints_to_curves` | Drive / Aim / Up Curve 使用统一弧长百分比同步。 |
| `create_doble_constraint` | 🧩 | Controller / Rig System | 依赖 zero / driven / ctrl 特定层级约定。 |

## Face

| 旧 Pipeline 方法 | 状态 | 正式方向 | 说明 |
| --- | --- | --- | --- |
| `add_face_tag` | ⏸ | Face Publish / Export System | 当前 Face Rig 不依赖 `isFace` Tag。 |
| `remove_non_face_objs` | ⏸ | Face Publish / Export System | 具有破坏性，不允许作为普通 Core API。 |
| `create_zip_lip` | ✅ | `systems.face.lip.build_zip_lip` | 已重构为 Matrix Zip Lip，不再使用每 Joint ParentConstraint 做闭合混合。 |

## Controller / Rig Workflow

| 旧 Pipeline 方法 | 状态 | 正式方向 | 说明 |
| --- | --- | --- | --- |
| `batch_Constraints_modle` | 🧩 | Controller / Rig System | 同时创建 Joint、Skin、Controller、Hierarchy、Constraint，职责过重。 |
| `batch_Constraints_joint` | 🧩 | Controller / Rig System | 同上。 |

## Hair / Dynamics

| 旧 Pipeline 方法 | 状态 | 正式方向 | 说明 |
| --- | --- | --- | --- |
| `create_dynamic_curve_driven` | 🧩 | Future Hair System | 同时创建 nHair、Joint、Spline IK、Set 和 Rig Group，不属于 Core。 |

## 暂缓 / 淘汰

| 旧 Pipeline 方法 | 状态 | 说明 |
| --- | --- | --- |
| `list_operation` | 🗑 | 只是 Python `set` 运算，没有必要维护 Maya 专用 API。 |
| `copy_surface_create_geo` | ⏸ | 依赖当前 Face Component Selection 的交互建模操作，当前正式系统没有调用。 |
| `create_logging` | 🗑 / 暂缓 | Python 标准 `logging` 足够；如以后需要项目日志系统，应单独设计。 |

## 删除 legacy pipelineUtils.py 的条件

只有以下条件全部满足后，才删除 `legacy_reference/core/pipelineUtils.py`：

1. 通用 Core 功能全部有正式替代；
2. Face Zip Lip、Eyelid、Curve Attachment 等有价值算法已经迁入对应 System 或明确淘汰；
3. Dynamic Hair、批量 Controller Rig 等完整 Workflow 已经迁移或确认不再保留；
4. 全仓库正式运行代码搜索 `pipelineUtils` 为 0；
5. Maya 2023 Smoke Test、Functional Smoke Test 与新 Face Component Smoke Test 通过。

在此之前，旧文件只作为历史算法参考，不允许正式代码 import。
