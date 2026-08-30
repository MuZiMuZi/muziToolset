# coding=utf-8
u"""
Face Rig 公共基础类
==================

所有 Face Rig Step 的公共底座。

负责：
    1. 保存 Face Rig 公共配置和层级名称；
    2. 确保 Face Rig 基础层级存在；
    3. 确保 Face Config Network Node 存在；
    4. 统一读写 Config Message / Value；
    5. 统一读取 Step 01 保存的 Face Setup 数据；
    6. 统一管理 Step 完成状态。

边界：
    - 这里只放多个 Face Step 都会复用的能力；
    - Guide 模板、Guide 查询、Guide 镜像属于 FaceGuide；
    - Joint / Curve / Controller 构建属于各自 Builder；
    - 通用 Maya DAG / 文件 / 属性能力继续放在 core。

说明：
    正式系统代码不在模块 import 时主动 reload 依赖。
    热重载由开发阶段的专用入口负责，避免 Maya 中出现旧类实例和新模块混用。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import attr_utils
from ...core import hierarchy_utils
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
        # ------------------------------------------------------------
        # 当前子类对应的 Step。
        # FaceBase 本身没有 Step，具体子类负责设置。
        # ------------------------------------------------------------
        u"""
        执行 `__init__` 对应的 Maya 工具操作。
        """

        self.step_value = None

        # ------------------------------------------------------------
        # Face Rig 基础配置
        # ------------------------------------------------------------
        self.face_side = config.face_side
        self.face_center_axis = config.face_center_axis

        # ------------------------------------------------------------
        # Config Node
        # ------------------------------------------------------------
        self.config_node = config.config_node

        # ------------------------------------------------------------
        # Face Rig 主层级
        # ------------------------------------------------------------
        self.face_master_grp = config.face_master_grp
        self.face_model_grp = config.face_model_grp

        # ------------------------------------------------------------
        # Face Rig 功能组
        # ------------------------------------------------------------
        self.face_guide_grp = config.face_guide_grp
        self.face_ctrl_grp = config.face_ctrl_grp
        self.face_jnt_grp = config.face_jnt_grp
        self.face_rig_nodes_grp = config.face_rig_nodes_grp
        self.face_pos_driver_grp = config.face_pos_driver_grp

        # ------------------------------------------------------------
        # 模型工作层
        # ------------------------------------------------------------
        self.face_tweak_grp = config.face_tweak_grp
        self.face_stretch_grp = config.face_stretch_grp
        self.face_deform_grp = config.face_deform_grp

        # ------------------------------------------------------------
        # 层级列表
        # ------------------------------------------------------------
        self.type_groups = config.type_grp_list
        self.model_groups = config.model_grp_list

        # ------------------------------------------------------------
        # Step 01 公共输入数据。
        # 不在 Base 初始化时强制读取 Config，避免 Step 01 首次运行时
        # Config 尚未创建而产生无意义的读取。
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
        u"""
        确保 Face Rig 基础层级存在。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        if not cmds.objExists(self.face_master_grp):
            hierarchy_utils.Hierarchy.create_grp(
                self.face_master_grp
            )

        if not cmds.objExists(self.face_model_grp):
            hierarchy_utils.Hierarchy.create_grp(
                self.face_model_grp,
                parent=self.face_master_grp
            )

        for group_name in self.type_groups:
            if cmds.objExists(group_name):
                continue

            hierarchy_utils.Hierarchy.create_grp(
                group_name,
                parent=self.face_master_grp
            )

        for group_name in self.model_groups:
            if cmds.objExists(group_name):
                continue

            hierarchy_utils.Hierarchy.create_grp(
                group_name,
                parent=self.face_model_grp
            )

        return True

    # =========================================================================
    # Config Node
    # =========================================================================

    def ensure_config_node(self):
        u"""
        确保 Face Rig Config Network Node 存在。

        Returns:
            object:
            方法执行后的结果数据。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if cmds.objExists(self.config_node):
            node_type = cmds.nodeType(
                self.config_node
            )

            if node_type != "network":
                raise RuntimeError(
                    u"Config 节点名称已经被其他类型节点占用: {0}，"
                    u"当前节点类型为: {1}".format(
                        self.config_node,
                        node_type
                    )
                )

            return self.config_node

        config_node = cmds.createNode(
            "network",
            name=self.config_node
        )

        self.config_node = config_node
        return config_node

    def config_node_exists(self):
        u"""
        检查 Face Rig Config Node 是否存在。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        if not cmds.objExists(self.config_node):
            return False

        if cmds.nodeType(self.config_node) != "network":
            return False

        return True

    # =========================================================================
    # Config Attr - Read
    # =========================================================================

    def get_config_attr(self):
        u"""
        获取 Face Rig Config 节点的 Attr 操作对象。

        Returns:
            object:
            方法执行后的结果数据。
        """
        config_attr = attr_utils.Attr(
            self.config_node
        )
        return config_attr

    def get_config_message(self, attr_name):
        u"""
        读取 Config Node 中保存的 Maya 节点 Message。

        Args:
            attr_name (str):
                `attr_name` 对应的 Maya 节点或资源名称。

        Returns:
            object | None:
            方法执行后的结果数据。
        """
        if not self.config_node_exists():
            return None

        config_attr = self.get_config_attr()
        node = config_attr.get_message(
            attr_name
        )
        return node

    def get_config_value(self, attr_name):
        u"""
        读取 Config Node 中保存的普通属性值。

        Args:
            attr_name (str):
                `attr_name` 对应的 Maya 节点或资源名称。

        Returns:
            object | None:
            方法执行后的结果数据。
        """
        if not self.config_node_exists():
            return None

        config_attr = self.get_config_attr()
        value = config_attr.get_attr_value(
            attr_name
        )
        return value

    # =========================================================================
    # Config Attr - Write
    # =========================================================================

    def set_config_messages(
            self,
            attrs_dict,
            force=True,
            clear_empty=True
    ):
        u"""
        批量保存 Maya 节点引用到 Face Config。

        节点引用统一使用 Message，而不是保存节点名称字符串。
        这样场景中对象改名后，Config 仍然能够找到正确节点。

        Args:
            attrs_dict (dict):
                `attrs_dict` 对应的配置或映射字典。
            force (bool):
                是否强制覆盖已有连接、状态或结果。
            clear_empty (bool):
                是否启用 `clear_empty` 对应的处理。

        Returns:
            object:
            方法执行后的结果数据。
        """
        self.ensure_config_node()

        config_attr = self.get_config_attr()
        result = config_attr.connect_messages(
            attrs_dict=attrs_dict,
            force=force,
            clear_empty=clear_empty
        )

        return result

    def set_config_values(
            self,
            attrs_dict,
            attr_types=None,
            lock=False,
            hide=False
    ):
        u"""
        批量保存普通数值 / 字符串配置到 Face Config。

        Args:
            attrs_dict (dict):
                `attrs_dict` 对应的配置或映射字典。
            attr_types (object):
                `attr_types` 对应的输入数据。
            lock (bool):
                是否启用 `lock` 对应的处理。
            hide (bool):
                是否启用 `hide` 对应的处理。

        Returns:
            object:
            方法执行后的结果数据。
        """
        self.ensure_config_node()

        if attr_types is None:
            attr_types = {}

        config_attr = self.get_config_attr()
        result = config_attr.set_attr_values(
            attrs_dict=attrs_dict,
            attr_types=attr_types,
            lock=lock,
            hide=hide
        )

        return result

    # =========================================================================
    # Setup Data
    # =========================================================================

    def refresh_setup_data(self):
        u"""
        从 Config Node 重新读取 Step 01 的最新数据。

        Step 01 可以重复 Build，因此后续 Step 在执行前应该刷新数据，
        不依赖对象初始化时缓存下来的旧值。

        Returns:
            object:
            方法执行后的结果数据。
        """
        for attr_name in self.setup_message_attr_names:
            node = self.get_config_message(
                attr_name
            )
            setattr(
                self,
                attr_name,
                node
            )

        for attr_name in self.setup_value_attr_names:
            value = self.get_config_value(
                attr_name
            )
            setattr(
                self,
                attr_name,
                value
            )

        return self.get_setup_data(
            refresh=False
        )

    def get_setup_data(self, refresh=False):
        u"""
        返回 Step 01 公共输入数据字典。

        Args:
            refresh (bool):
                是否启用 `refresh` 对应的处理。

        Returns:
            object:
            方法执行后的结果数据。
        """
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

        更具体的业务条件仍由各 Step 自己负责，避免 FaceBase
        知道 Lip / Brow / Eyelid 等组件的实现细节。

        Args:
            require_mouth_jnt_number (bool):
                是否启用 `require_mouth_jnt_number` 对应的处理。

        Returns:
            bool:
            方法执行后的结果数据。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
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

        if not cmds.objExists(self.face_head_model):
            raise RuntimeError(
                u"Face Head Model 已经不存在于当前场景中: {}".format(
                    self.face_head_model
                )
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

            if cmds.objExists(model):
                continue

            raise RuntimeError(
                u"Face Setup 中保存的模型已经不存在: {}".format(
                    model
                )
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
        u"""
        根据 Step 编号生成 Config 中的完成状态属性名称。

        Args:
            step_value (int):
                `step_value` 对应的整数参数。

        Returns:
            object:
            方法执行后的结果数据。

        Raises:
            TypeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if not isinstance(step_value, int):
            raise TypeError(
                u"Step 编号必须是整数。"
            )

        if step_value < 1:
            raise ValueError(
                u"Step 编号不能小于 1。"
            )

        attr_name = "step_{:02d}_completed".format(
            step_value
        )
        return attr_name

    def resolve_step_value(self, step_value=None):
        u"""
        获取当前操作使用的 Step 编号。

        Args:
            step_value (int):
                `step_value` 对应的整数参数。

        Returns:
            object:
            方法执行后的结果数据。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
            TypeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
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
        u"""
        写入某个 Face Step 的完成状态。

        Args:
            step_value (int):
                `step_value` 对应的整数参数。
            completed (bool):
                是否启用 `completed` 对应的处理。

        Returns:
            object:
            方法执行后的结果数据。
        """
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
        u"""
        读取某个 Face Step 是否已经完成。

        Args:
            step_value (int):
                `step_value` 对应的整数参数。

        Returns:
            object | bool:
            方法执行后的结果数据。
        """
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
        u"""
        将当前 Step 之后的完成状态全部设为 False。

        例如重新 Build Step 01 后，Step 02～04 的旧结果已经不能保证
        继续有效，因此统一标记为未完成。

        Args:
            step_value (int):
                `step_value` 对应的整数参数。
            last_step (int):
                `last_step` 对应的整数参数。

        Returns:
            object | list:
            方法执行后的结果数据。

        Raises:
            TypeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
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
        u"""
        返回 Face Wizard 各 Step 的完成状态。

        Args:
            last_step (int):
                `last_step` 对应的整数参数。

        Returns:
            object:
            方法执行后的结果数据。

        Raises:
            TypeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
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
