# coding=utf-8
u"""
Face Rig 公共基础类
==================

所有 Face Rig Step 的公共业务底座。

负责：
    1. 保存 Face Rig 公共命名和层级配置；
    2. 确保 Face Rig 基础层级存在；
    3. 定义 Step 01 公共 Setup 数据；
    4. 统一管理 Face Step 完成状态和当前 Workflow Step；
    5. 统一整理 Face Config Network Node 的 Step 属性分区；
    6. 继承 systems.common.StepBase 的统一 Step 生命周期。

重要边界：
    - Step 生命周期由 systems.common.StepBase 负责；
    - Config Network Node 的创建、Message 引用、Value 读写由 core.config_utils.ConfigNode 负责；
    - Maya Model 有效性由 core.mesh_utils 负责；
    - Maya DAG 层级操作由 core.hierarchy_utils 负责；
    - FaceBase 只保留 Face System 自己的公共业务语义；
    - 只维护当前正式 Config Schema，不处理历史场景迁移。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import config_utils
from ...core import hierarchy_utils
from ...core import mesh_utils
from ..common import StepBase
from . import config


class FaceBase(StepBase):
    u"""所有 Face Rig Step 共用的基础类。"""

    setup_message_attr_names = [
        "face_head_model",
        "face_lf_eye_model",
        "face_rt_eye_model",
        "upper_teech_model",
        "lower_teech_model",
        "face_tongue_model",
        "face_gum_model",
    ]

    setup_value_attr_names = [
        "mouth_jnt_number",
    ]

    last_step_value = 4
    current_step_attr_name = "face_current_step"
    workflow_section_attr_name = "face_workflow_section"

    current_step_enum_name = (
        "Not Started:"
        "Step 01 Setup:"
        "Step 02 Guide:"
        "Step 03 Build:"
        "Step 04 Finalize"
    )

    step_section_attr_names = {
        1: "step_01_setup_section",
        2: "step_02_guide_section",
        3: "step_03_build_section",
        4: "step_04_finalize_section",
    }

    step_section_nice_names = {
        1: "---------- STEP 01 SETUP ----------",
        2: "---------- STEP 02 GUIDE ----------",
        3: "---------- STEP 03 BUILD ----------",
        4: "---------- STEP 04 FINALIZE ----------",
    }

    step_config_attr_names = {
        1: [
            "face_head_model",
            "face_lf_eye_model",
            "face_rt_eye_model",
            "upper_teech_model",
            "lower_teech_model",
            "face_tongue_model",
            "face_gum_model",
            "mouth_jnt_number",
            "step_01_completed",
        ],
        2: list(
            config.face_step_02_config_attr_names
        ),
        3: [
            "step_03_completed",
        ],
        4: [
            "step_04_completed",
        ],
    }

    def __init__(self):
        u"""初始化 Face Rig 公共配置。"""
        self.step_value = None

        self.face_side = config.face_side
        self.face_center_axis = config.face_center_axis

        self.config_node = config.config_node
        self.config_data = config_utils.ConfigNode(
            self.config_node
        )

        self.face_master_grp = config.face_master_grp
        self.face_model_grp = config.face_model_grp

        self.face_guide_grp = config.face_guide_grp
        self.face_ctrl_grp = config.face_ctrl_grp
        self.face_jnt_grp = config.face_jnt_grp
        self.face_rig_nodes_grp = config.face_rig_nodes_grp
        self.face_pos_driver_grp = config.face_pos_driver_grp

        self.face_tweak_grp = config.face_tweak_grp
        self.face_stretch_grp = config.face_stretch_grp
        self.face_deform_grp = config.face_deform_grp

        self.type_groups = config.type_grp_list
        self.model_groups = config.model_grp_list

        self.face_head_model = None
        self.face_lf_eye_model = None
        self.face_rt_eye_model = None
        self.upper_teech_model = None
        self.lower_teech_model = None
        self.face_tongue_model = None
        self.face_gum_model = None
        self.mouth_jnt_number = None

    # =========================================================================
    # Hierarchy
    # =========================================================================

    def ensure_hierarchy(self):
        u"""确保 Face Rig 基础层级存在。"""
        hierarchy_utils.Hierarchy.create_grp(
            self.face_master_grp
        )

        hierarchy_utils.Hierarchy.create_grp(
            self.face_model_grp,
            parent=self.face_master_grp
        )

        for group_name in self.type_groups:
            hierarchy_utils.Hierarchy.create_grp(
                group_name,
                parent=self.face_master_grp
            )

        for group_name in self.model_groups:
            hierarchy_utils.Hierarchy.create_grp(
                group_name,
                parent=self.face_model_grp
            )

        return True

    # =========================================================================
    # Config Node / Face API
    # =========================================================================

    def ensure_config_node(self):
        u"""确保 Face Config 存在。"""
        config_node = self.config_data.ensure()
        self.config_node = config_node
        return config_node

    def config_node_exists(self):
        u"""检查 Face Config Network Node 是否有效。"""
        return self.config_data.exists()

    def get_config_attr(self):
        u"""返回 Config 的底层 Attr 对象。"""
        return self.config_data.get_attr()

    def get_config_message(self, attr_name):
        u"""读取 Face Config 中保存的 Maya 节点 Message 引用。"""
        return self.config_data.get_message(
            attr_name
        )

    def get_config_value(self, attr_name):
        u"""读取 Face Config 中保存的普通属性值。"""
        return self.config_data.get_value(
            attr_name
        )

    def set_config_messages(
            self,
            attrs_dict,
            force=True,
            clear_empty=True
    ):
        u"""批量保存 Maya 节点引用到 Face Config。"""
        result = self.config_data.set_messages(
            attrs_dict=attrs_dict,
            force=force,
            clear_empty=clear_empty
        )

        self.config_node = self.config_data.node
        return result

    def set_config_values(
            self,
            attrs_dict,
            attr_types=None,
            lock=False,
            hide=False
    ):
        u"""批量保存普通数值 / 字符串配置到 Face Config。"""
        result = self.config_data.set_values(
            attrs_dict=attrs_dict,
            attr_types=attr_types,
            lock=lock,
            hide=hide
        )

        self.config_node = self.config_data.node
        return result

    # =========================================================================
    # Config Layout / Workflow State
    # =========================================================================

    def ensure_config_layout(self):
        u"""创建当前正式 Face Config Workflow / Step 分隔属性。"""
        self.ensure_config_node()
        config_attr = self.get_config_attr()

        config_attr.add_attr(
            self.workflow_section_attr_name,
            attr_type="enum",
            lock=True,
            hide=True,
            default_value=0,
            enum_name="--------------------",
            niceName="========== FACE WORKFLOW =========="
        )

        if not config_attr.attr_exists(
                self.current_step_attr_name
        ):
            config_attr.add_attr(
                self.current_step_attr_name,
                attr_type="enum",
                lock=True,
                hide=True,
                default_value=1,
                enum_name=self.current_step_enum_name,
                niceName="Current Face Step"
            )

        step_value = 1

        while step_value <= self.last_step_value:
            section_attr_name = self.step_section_attr_names.get(
                step_value
            )
            section_nice_name = self.step_section_nice_names.get(
                step_value
            )

            config_attr.add_attr(
                section_attr_name,
                attr_type="enum",
                lock=True,
                hide=True,
                default_value=0,
                enum_name="--------------------",
                niceName=section_nice_name
            )

            step_value += 1

        self.organize_config_attributes()
        return True

    def get_config_attribute_order(self):
        u"""返回 Face Config 在 Attribute Editor 中推荐的动态属性顺序。"""
        attr_names = [
            self.workflow_section_attr_name,
            self.current_step_attr_name,
        ]

        step_value = 1

        while step_value <= self.last_step_value:
            section_attr_name = self.step_section_attr_names.get(
                step_value
            )
            attr_names.append(
                section_attr_name
            )

            step_attr_names = self.step_config_attr_names.get(
                step_value,
                []
            )

            for attr_name in step_attr_names:
                attr_names.append(
                    attr_name
                )

            step_value += 1

        return attr_names

    def organize_config_attributes(self):
        u"""按 Workflow Step 重新排序 Config Node 的 User Defined Attribute。"""
        if not self.config_node_exists():
            return []

        ordered_attrs = self.get_config_attribute_order()
        reordered_attrs = []

        for attr_name in ordered_attrs:
            plug = "{}.{}".format(
                self.config_node,
                attr_name
            )

            if not cmds.objExists(plug):
                continue

            try:
                cmds.reorderAttr(
                    plug,
                    back=True
                )
            except Exception:
                continue

            reordered_attrs.append(
                attr_name
            )

        return reordered_attrs

    def get_current_step_value(self):
        u"""读取当前 Face Workflow Step；没有 Config 时从 Step 01 开始。"""
        if not self.config_node_exists():
            return 1

        current_step_value = self.get_config_value(
            self.current_step_attr_name
        )

        if not isinstance(current_step_value, int):
            return 1

        if current_step_value < 1:
            return 1

        if current_step_value > self.last_step_value:
            return self.last_step_value

        return current_step_value

    def set_current_step_value(self, step_value):
        u"""把当前 Face Workflow Step 保存到 Config Node。"""
        if not isinstance(step_value, int):
            raise TypeError(
                u"Current Face Step 必须是整数。"
            )

        if step_value < 1 or step_value > self.last_step_value:
            raise ValueError(
                u"Current Face Step 必须在 1～{}。".format(
                    self.last_step_value
                )
            )

        self.ensure_config_layout()
        config_attr = self.get_config_attr()

        config_attr.set_attr_value(
            attr=self.current_step_attr_name,
            value=step_value,
            attr_type="enum",
            lock=True,
            hide=True,
            enum_name=self.current_step_enum_name
        )

        self.organize_config_attributes()
        return step_value

    # =========================================================================
    # Setup Data
    # =========================================================================

    def refresh_setup_data(self):
        u"""从 Config Node 重新读取 Step 01 的最新数据。"""
        message_data = self.config_data.get_messages(
            self.setup_message_attr_names
        )

        for attr_name in self.setup_message_attr_names:
            setattr(
                self,
                attr_name,
                message_data.get(attr_name)
            )

        value_data = self.config_data.get_values(
            self.setup_value_attr_names
        )

        for attr_name in self.setup_value_attr_names:
            setattr(
                self,
                attr_name,
                value_data.get(attr_name)
            )

        return self.get_setup_data(
            refresh=False
        )

    def get_setup_data(self, refresh=False):
        u"""返回 Step 01 公共输入数据字典。"""
        if refresh:
            self.refresh_setup_data()

        setup_data = {}

        for attr_name in self.setup_message_attr_names:
            setup_data[attr_name] = getattr(
                self,
                attr_name,
                None
            )

        for attr_name in self.setup_value_attr_names:
            setup_data[attr_name] = getattr(
                self,
                attr_name,
                None
            )

        return setup_data

    def validate_setup_config(
            self,
            require_mouth_jnt_number=True
    ):
        u"""检查后续 Face Step 所依赖的 Step 01 公共数据。"""
        if not self.config_node_exists():
            raise RuntimeError(
                u"没有找到 Face Config，请先完成 Face Setup。"
            )

        self.refresh_setup_data()

        if not self.face_head_model:
            raise RuntimeError(
                u"没有读取到 Face Head Model，请先完成 Face Setup。"
            )

        mesh_utils.validate_model_transform(
            self.face_head_model,
            label=u"Face Head Model"
        )

        optional_models = [
            self.face_lf_eye_model,
            self.face_rt_eye_model,
            self.upper_teech_model,
            self.lower_teech_model,
            self.face_tongue_model,
            self.face_gum_model,
        ]

        for model in optional_models:
            if not model:
                continue

            mesh_utils.validate_model_transform(
                model,
                label=u"Face Setup Model"
            )

        if require_mouth_jnt_number:
            if self.mouth_jnt_number is None:
                raise RuntimeError(
                    u"没有读取到嘴唇 Joint 数量，请先完成 Face Setup。"
                )

        return True

    # =========================================================================
    # Step State
    # =========================================================================

    @staticmethod
    def get_step_completed_attr_name(step_value):
        u"""根据 Step 编号生成 Config 完成状态属性名称。"""
        if not isinstance(step_value, int):
            raise TypeError(
                u"Step 编号必须是整数。"
            )

        if step_value < 1:
            raise ValueError(
                u"Step 编号不能小于 1。"
            )

        return "step_{:02d}_completed".format(
            step_value
        )

    def resolve_step_value(self, step_value=None):
        u"""获取当前操作使用的 Step 编号。"""
        if step_value is None:
            step_value = self.step_value

        if step_value is None:
            raise RuntimeError(
                u"当前 Face 类没有设置 step_value。"
            )

        if not isinstance(step_value, int):
            raise TypeError(
                u"Step 编号必须是整数。"
            )

        return step_value

    def set_step_completed(
            self,
            step_value=None,
            completed=True
    ):
        u"""写入某个 Face Step 的完成状态。"""
        step_value = self.resolve_step_value(
            step_value
        )
        attr_name = self.get_step_completed_attr_name(
            step_value
        )

        self.set_config_values(
            attrs_dict={
                attr_name: bool(completed),
            },
            attr_types={
                attr_name: "bool",
            },
            lock=False,
            hide=True
        )

        return bool(completed)

    def is_step_completed(self, step_value=None):
        u"""读取某个 Face Step 是否已经完成。"""
        step_value = self.resolve_step_value(
            step_value
        )
        attr_name = self.get_step_completed_attr_name(
            step_value
        )
        value = self.get_config_value(
            attr_name
        )

        if value is None:
            return False

        return bool(value)

    def invalidate_later_steps(
            self,
            step_value=None,
            last_step=4
    ):
        u"""将当前 Step 之后的完成状态全部设为 False。"""
        step_value = self.resolve_step_value(
            step_value
        )

        if not isinstance(last_step, int):
            raise TypeError(
                u"last_step 必须是整数。"
            )

        if last_step <= step_value:
            return []

        invalidated_steps = []
        current_step = step_value + 1

        while current_step <= last_step:
            self.set_step_completed(
                step_value=current_step,
                completed=False
            )
            invalidated_steps.append(
                current_step
            )
            current_step += 1

        return invalidated_steps

    def get_step_status(self, last_step=4):
        u"""返回 Face Wizard 各 Step 的完成状态。"""
        if not isinstance(last_step, int):
            raise TypeError(
                u"last_step 必须是整数。"
            )

        status = {}
        current_step = 1

        while current_step <= last_step:
            status[current_step] = self.is_step_completed(
                step_value=current_step
            )
            current_step += 1

        return status


__all__ = [
    "FaceBase",
]
