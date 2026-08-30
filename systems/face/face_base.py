# coding=utf-8
u"""
Face Rig 公共基础类
==================

所有 Face Rig Step 的公共业务底座。

负责：
    1. 保存 Face Rig 公共命名和层级配置；
    2. 确保 Face Rig 基础层级存在；
    3. 定义 Step 01 公共 Setup 数据；
    4. 统一管理 Face Step 完成状态。

重要边界：
    - Config Network Node 的创建、Message 引用、Value 读写由 core.config_utils.ConfigNode 负责；
    - Maya Model 有效性由 core.mesh_utils 负责；
    - Maya DAG 层级操作由 core.hierarchy_utils 负责；
    - FaceBase 只保留 Face System 自己的业务语义。
"""

from __future__ import print_function

from ...core import config_utils
from ...core import hierarchy_utils
from ...core import mesh_utils
from . import config


class FaceBase(object):
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

    def __init__(self):
        u"""初始化 Face Rig 公共配置。"""
        # ------------------------------------------------------------
        # 当前子类对应的 Step。
        # ------------------------------------------------------------
        self.step_value = None

        # ------------------------------------------------------------
        # Face Rig 基础配置。
        # ------------------------------------------------------------
        self.face_side = config.face_side
        self.face_center_axis = config.face_center_axis

        # ------------------------------------------------------------
        # 通用 Config Node 代理。
        # ------------------------------------------------------------
        self.config_node = config.config_node
        self.config_data = config_utils.ConfigNode(
            self.config_node
        )

        # ------------------------------------------------------------
        # Face Rig 主层级。
        # ------------------------------------------------------------
        self.face_master_grp = config.face_master_grp
        self.face_model_grp = config.face_model_grp

        # ------------------------------------------------------------
        # Face Rig 功能组。
        # ------------------------------------------------------------
        self.face_guide_grp = config.face_guide_grp
        self.face_ctrl_grp = config.face_ctrl_grp
        self.face_jnt_grp = config.face_jnt_grp
        self.face_rig_nodes_grp = config.face_rig_nodes_grp
        self.face_pos_driver_grp = config.face_pos_driver_grp

        # ------------------------------------------------------------
        # 模型工作层。
        # ------------------------------------------------------------
        self.face_tweak_grp = config.face_tweak_grp
        self.face_stretch_grp = config.face_stretch_grp
        self.face_deform_grp = config.face_deform_grp

        # ------------------------------------------------------------
        # 层级列表。
        # ------------------------------------------------------------
        self.type_groups = config.type_grp_list
        self.model_groups = config.model_grp_list

        # ------------------------------------------------------------
        # Step 01 公共输入数据。
        # ------------------------------------------------------------
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
    # Config Node - Compatibility / Face API
    # =========================================================================

    def ensure_config_node(self):
        u"""
        确保 Face Config 存在。

        通用 Network Config 行为已经下沉到 core.config_utils.ConfigNode。
        本方法作为 Face API 兼容入口保留。
        """
        config_node = self.config_data.ensure()
        self.config_node = config_node
        return config_node

    def config_node_exists(self):
        u"""检查 Face Config Network Node 是否有效。"""
        return self.config_data.exists()

    def get_config_attr(self):
        u"""
        返回 Config 的底层 Attr 对象。

        新代码优先使用 get_config_message / get_config_value 等语义化接口。
        """
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
    # Setup Data
    # =========================================================================

    def refresh_setup_data(self):
        u"""
        从 Config Node 重新读取 Step 01 的最新数据。

        Step 01 可以重复执行，因此后续 Step 在执行前应该刷新数据。
        """
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
        u"""
        检查后续 Face Step 所依赖的 Step 01 公共数据。

        这里只定义 Face 业务要求：Head 必填、其它模型可选、必要时要求 Mouth Joint Number。
        “模型是否存在 / 名称是否唯一 / 是否为 Transform”统一由 mesh_utils 负责。
        """
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
