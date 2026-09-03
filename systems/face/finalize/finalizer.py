# coding=utf-8
u"""
Face Rig Step 04 - Finalize
===========================

Face Workflow 的 Step 04 正式入口。

职责：
    1. 验证 Step 01 / 02 / 03 已经完成；
    2. 验证 Face Rig 关键层级仍然完整，不在 Finalize 阶段偷偷补建绑定结构；
    3. 收集 Face Controller，并确保全部加入 Face Controller Set；
    4. 应用 Step 04 最终显示状态；
    5. 再次验证 Controller Set 和 Visibility；
    6. 成功后把 Step 04 标记完成，并保持 Current Face Step = 04；
    7. Finalize 修改放在单个 Maya Undo Chunk 中，失败时回滚本次整理。

设计边界：
    - Finalize 不重新创建 Joint / Controller / Matrix / Deformer；
    - Finalize 不修改 Skin / BlendShape / Zip Lip 等绑定算法；
    - Finalize 不承担文件 Export / Publish，发布流程后续单独扩展；
    - Finalize 允许重复执行，重复执行只重新验收和整理最终状态；
    - Controller Set 使用 core.scene_utils.ensure_object_set()；
    - Workflow State 统一使用 FaceBase 的 Step API。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import scene_utils
from .. import config
from ..face_base import FaceBase


class FaceFinalizer(FaceBase):
    u"""统一执行 Face Workflow Step 04 最终验收和场景整理。"""

    required_step_values = [
        1,
        2,
        3,
    ]

    hierarchy_attr_names = [
        "face_master_grp",
        "face_model_grp",
        "face_guide_grp",
        "face_ctrl_grp",
        "face_jnt_grp",
        "face_rig_nodes_grp",
        "face_pos_driver_grp",
    ]

    def __init__(self):
        u"""初始化 Step 04 Finalize 状态。"""
        super(FaceFinalizer, self).__init__(
            side="md",
            part="face",
            index=1
        )

        self.step_value = 4
        self.controller_nodes = []
        self.controller_set = None
        self.visibility_state = {}
        self.validation_result = None

    # =========================================================================
    # Module Lifecycle
    # =========================================================================

    def collect_inputs(self):
        u"""
        检查 Finalize 所依赖的 Workflow 状态。

        Returns:
            bool:
                Step 01 / 02 / 03 都完成时返回 True。

        Raises:
            RuntimeError:
                Face Config 不存在或任一前置 Step 未完成时抛出。
        """
        if not self.config_node_exists():
            raise RuntimeError(
                u"没有找到 Face Config，请先完成 Face Setup。"
            )

        incomplete_steps = []

        for step_value in self.required_step_values:
            if self.is_step_completed(
                    step_value=step_value
            ):
                continue

            incomplete_steps.append(
                step_value
            )

        if incomplete_steps:
            raise RuntimeError(
                u"Face Finalize 前必须先完成 Step：{}".format(
                    incomplete_steps
                )
            )

        return True

    def prepare_data(self):
        u"""
        解析现有 Face Hierarchy 并收集正式 Controller。

        Finalize 只验证已有结构，不调用 ensure_hierarchy() 自动补建缺失 Group，
        避免把 Step 03 之后被误删的 Rig 节点伪装成正常状态。

        Returns:
            bool:
                层级和 Controller 收集完成时返回 True。
        """
        self.resolve_existing_hierarchy()
        self.controller_nodes = self.collect_face_controllers()

        if not self.controller_nodes:
            raise RuntimeError(
                u"Face Controller Group 下没有找到任何正式 Controller，不能完成 Finalize。"
            )

        return True

    def process_data(self):
        u"""
        整理 Controller Set，并应用 Step 04 最终显示状态。

        Returns:
            bool:
                Controller Set 和 Visibility 整理完成时返回 True。
        """
        self.controller_set = self.ensure_controller_set()
        self.visibility_state = self.apply_final_visibility()
        return True

    def finalize_step(self):
        u"""
        验证最终状态，并写入 Step 04 Workflow 完成状态。

        Returns:
            bool:
                Step 04 成功完成时返回 True。
        """
        self.validation_result = self.validate_results()

        self.set_step_completed(
            completed=True
        )
        self.set_current_step_value(
            4
        )
        self.organize_config_attributes()
        return True

    def run_step(self):
        u"""
        在单个 Maya Undo Chunk 中执行完整 Step 04。

        Returns:
            bool:
                Finalize 全部通过时返回 True。

        Raises:
            Exception:
                任一阶段失败时，在已经修改场景的情况下回滚本次 Finalize，
                然后继续向上抛出原异常。
        """
        scene_modified = False

        scene_utils.open_undo_chunk(
            chunk_name="FaceFinalizeStep04"
        )

        try:
            self.collect_inputs()
            self.prepare_data()

            # 从 process_data() 开始会修改 Set / Visibility。
            scene_modified = True
            self.process_data()
            self.finalize_step()
        except Exception:
            scene_utils.close_undo_chunk()

            if scene_modified:
                try:
                    cmds.undo()
                except Exception:
                    pass

            self.validation_result = None
            raise

        scene_utils.close_undo_chunk()
        return True

    # =========================================================================
    # Hierarchy
    # =========================================================================

    def resolve_existing_hierarchy(self):
        u"""
        验证并缓存当前 Scene 中真实的 Face Hierarchy Long Path。

        Returns:
            dict:
                Key 为 FaceBase Group Attribute，Value 为真实 Maya 节点路径。
        """
        resolved_groups = {}

        for attr_name in self.hierarchy_attr_names:
            group_node = getattr(
                self,
                attr_name,
                None
            )

            if not group_node:
                raise RuntimeError(
                    u"Face Finalize 缺少层级配置：{}".format(
                        attr_name
                    )
                )

            scene_utils.validate_node(
                group_node,
                label=u"Face Finalize Group"
            )
            long_name = scene_utils.get_long_name(
                group_node
            )

            setattr(
                self,
                attr_name,
                long_name
            )
            resolved_groups[attr_name] = long_name

        return resolved_groups

    # =========================================================================
    # Controller / Set
    # =========================================================================

    @staticmethod
    def get_node_base_name(node):
        u"""返回去掉 DAG Path 和 Maya Namespace 的节点基础名称。"""
        short_name = str(node).rsplit(
            "|",
            1
        )[-1]

        return short_name.rsplit(
            ":",
            1
        )[-1]

    def collect_face_controllers(self):
        u"""
        收集 Face Controller Group 下全部正式 ``ctrl_`` Transform。

        Returns:
            list[str]:
                排序后的 Controller Long Path 列表。
        """
        descendants = cmds.listRelatives(
            self.face_ctrl_grp,
            allDescendents=True,
            type="transform",
            fullPath=True
        ) or []

        controllers = []

        for node in descendants:
            base_name = self.get_node_base_name(
                node
            )

            if not base_name.startswith(
                    "ctrl_"
            ):
                continue

            long_name = scene_utils.get_long_name(
                node
            )

            if long_name in controllers:
                continue

            controllers.append(
                long_name
            )

        controllers.sort()
        return controllers

    def ensure_controller_set(self):
        u"""
        创建或复用 Face Controller Set，并补齐全部 Controller 成员。

        Returns:
            str:
                Maya Object Set 名称。
        """
        return scene_utils.ensure_object_set(
            set_name=config.face_ctrl_set,
            objects=self.controller_nodes
        )

    # =========================================================================
    # Visibility
    # =========================================================================

    def get_visibility_group_map(self):
        u"""返回 Config Visibility Key 到当前真实 Group Path 的映射。"""
        return {
            "face_model_grp": self.face_model_grp,
            "face_guide_grp": self.face_guide_grp,
            "face_ctrl_grp": self.face_ctrl_grp,
            "face_jnt_grp": self.face_jnt_grp,
            "face_rig_nodes_grp": self.face_rig_nodes_grp,
            "face_pos_driver_grp": self.face_pos_driver_grp,
        }

    def apply_final_visibility(self):
        u"""
        应用 config.py 中 Step 04 的最终显示规则。

        Returns:
            dict:
                实际写入的 Visibility 状态。
        """
        visibility_rules = config.face_step_visibility_rules.get(
            4,
            {}
        )
        group_map = self.get_visibility_group_map()
        visibility_state = {}

        for group_key in group_map:
            if group_key not in visibility_rules:
                continue

            group_node = group_map.get(
                group_key
            )
            visible = bool(
                visibility_rules.get(
                    group_key
                )
            )
            visibility_plug = "{}.visibility".format(
                group_node
            )

            if not cmds.objExists(
                    visibility_plug
            ):
                raise RuntimeError(
                    u"Face Finalize 找不到 Visibility：{}".format(
                        visibility_plug
                    )
                )

            cmds.setAttr(
                visibility_plug,
                visible
            )
            visibility_state[group_key] = visible

        return visibility_state

    # =========================================================================
    # Validation
    # =========================================================================

    def validate_controller_set(self):
        u"""验证 Face Controller Set 存在且包含全部 Controller。"""
        scene_utils.validate_node(
            self.controller_set,
            label=u"Face Controller Set"
        )

        if cmds.nodeType(
                self.controller_set
        ) != "objectSet":
            raise RuntimeError(
                u"Face Controller Set 不是 objectSet：{}".format(
                    self.controller_set
                )
            )

        missing_members = []

        for controller in self.controller_nodes:
            is_member = cmds.sets(
                controller,
                isMember=self.controller_set
            )

            if is_member:
                continue

            missing_members.append(
                controller
            )

        if missing_members:
            raise RuntimeError(
                u"Face Controller Set 缺少 Controller：{}".format(
                    missing_members
                )
            )

        return True

    def validate_visibility(self):
        u"""
        验证当前 Group Visibility 与 Step 04 Config 完全一致。

        Returns:
            dict:
                当前实际 Visibility 状态。
        """
        visibility_rules = config.face_step_visibility_rules.get(
            4,
            {}
        )
        group_map = self.get_visibility_group_map()
        actual_state = {}

        for group_key in group_map:
            if group_key not in visibility_rules:
                continue

            group_node = group_map.get(
                group_key
            )
            expected_visible = bool(
                visibility_rules.get(
                    group_key
                )
            )
            actual_visible = bool(
                cmds.getAttr(
                    "{}.visibility".format(
                        group_node
                    )
                )
            )
            actual_state[group_key] = actual_visible

            if actual_visible == expected_visible:
                continue

            raise RuntimeError(
                u"Face Finalize 显示状态错误：{} expected={} actual={}".format(
                    group_node,
                    expected_visible,
                    actual_visible
                )
            )

        return actual_state

    def validate_results(self):
        u"""
        验证 Finalize 后的关键结果并返回精简摘要。

        Returns:
            dict:
                Controller、Set 和 Visibility 验收摘要。
        """
        if not self.controller_nodes:
            raise RuntimeError(
                u"Face Finalize Controller 数量不能为 0。"
            )

        self.validate_controller_set()
        actual_visibility = self.validate_visibility()

        return {
            "controller_set": self.controller_set,
            "controller_count": len(
                self.controller_nodes
            ),
            "controllers": list(
                self.controller_nodes
            ),
            "visibility": actual_visibility,
        }


def finalize_face():
    u"""
    执行完整 Face Workflow Step 04，并返回公开结果。

    Returns:
        dict:
            Finalizer、Controller Set、Controller 数量、Visibility 和 Workflow 状态。
    """
    finalizer = FaceFinalizer()
    finalizer.run_step()

    return {
        "finalizer": finalizer,
        "controller_set": finalizer.controller_set,
        "controller_count": len(
            finalizer.controller_nodes
        ),
        "controllers": list(
            finalizer.controller_nodes
        ),
        "validation": finalizer.validation_result,
        "step_04_completed": finalizer.is_step_completed(
            step_value=4
        ),
        "current_step": finalizer.get_current_step_value(),
    }


__all__ = [
    "FaceFinalizer",
    "finalize_face",
]
