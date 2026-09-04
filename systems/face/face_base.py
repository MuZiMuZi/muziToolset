# coding=utf-8
u"""
Face Rig 公共基础类
==================

所有 Face Rig Workflow / Module 的公共业务底座。

负责：
    1. 把 Face Rig Object Identity 接入 RigBase；
    2. 保存 Face Rig 公共命名和层级配置；
    3. 确保 Face Rig 基础层级存在；
    4. 定义 Step 01 公共 Setup 数据；
    5. 统一管理 Face Step 完成状态和当前 Workflow Step；
    6. 统一整理 Face Config Network Node 的 Step 属性分区。

重要边界：
    - Rig Object Identity / Naming 由 systems.rig_base.RigBase 负责；
    - Module 四阶段生命周期由 systems.module_base.ModuleBase 负责；
    - 标准 Rig 的 Jnt / Controller / Connection 三阶段构建由 RigModuleBase 负责；
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
from ..module_base import RigModuleBase
from . import config


class FaceBase(RigModuleBase):
    u"""所有 Face Rig Workflow / Module 共用的基础类。"""

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

    def __init__(
            self,
            side=None,
            part=None,
            index=1
    ):
        u"""
        初始化 Face Rig 公共配置和当前 Rig Object Identity。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            part (str):
                Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。
            index (int):
                目标元素或节点的序号。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if side is None:
            side = config.face_side

        if part is None:
            part = config.face_part

        super(FaceBase, self).__init__(
            side=side,
            part=part,
            index=index
        )

        self.step_value = None

        self.face_side = config.face_side
        self.face_center_axis = config.face_center_axis

        self.config_node = config.config_node
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.config_data = config_utils.ConfigNode(
            self.config_node
        )

        self.face_master_grp = config.face_master_grp
        self.face_model_grp = config.face_model_grp

        self.face_guide_grp = config.face_guide_grp
        self.face_ctrl_grp = config.face_ctrl_grp
        self.face_jnt_grp = config.face_jnt_grp
        self.face_rig_nodes_grp = config.face_rig_nodes_grp
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.face_pos_driver_grp = config.face_pos_driver_grp

        self.face_tweak_grp = config.face_tweak_grp
        self.face_stretch_grp = config.face_stretch_grp
        self.face_deform_grp = config.face_deform_grp

        self.type_groups = config.type_grp_list
        self.model_groups = config.model_grp_list

        self.face_head_model = None
        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.face_lf_eye_model = None
        self.face_rt_eye_model = None
        self.upper_teech_model = None
        self.lower_teech_model = None
        self.face_tongue_model = None
        self.face_gum_model = None
        # -------------------------------------------------------------------------
        # Step 05：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.mouth_jnt_number = None

    # =========================================================================
    # Hierarchy
    # =========================================================================

    def ensure_hierarchy(self):
        u"""
        确保 Face Rig 基础 Group 存在，并保存 Maya 返回的真实 DAG Long Path。

        Config 只负责提供标准节点名称。真正创建或查询 Maya Group 后，必须把
        ``hierarchy_utils.ensure_group()`` 返回的唯一 Long Path 写回当前实例，
        这样 Namespace、同名 DAG 和 Rebuild 场景都继续使用真实场景节点。

        Returns:
            bool:
            Face 基础层级全部存在、Parent 正确，并完成真实路径缓存后返回 True。
        """
        # -------------------------------------------------------------------------
        # Step 01：创建 Face Master，并保存 Maya 实际返回的唯一 Long Path
        # -------------------------------------------------------------------------
        self.face_master_grp = hierarchy_utils.ensure_group(
            self.face_master_grp
        )

        # -------------------------------------------------------------------------
        # Step 02：创建 Model 主组，并挂到 Face Master 下
        # -------------------------------------------------------------------------
        self.face_model_grp = hierarchy_utils.ensure_group(
            self.face_model_grp,
            parent_node=self.face_master_grp
        )

        # -------------------------------------------------------------------------
        # Step 03：创建 Face 类型层级，并逐项保存真实场景路径
        # -------------------------------------------------------------------------
        self.face_guide_grp = hierarchy_utils.ensure_group(
            self.face_guide_grp,
            parent_node=self.face_master_grp
        )
        self.face_ctrl_grp = hierarchy_utils.ensure_group(
            self.face_ctrl_grp,
            parent_node=self.face_master_grp
        )
        self.face_jnt_grp = hierarchy_utils.ensure_group(
            self.face_jnt_grp,
            parent_node=self.face_master_grp
        )
        self.face_rig_nodes_grp = hierarchy_utils.ensure_group(
            self.face_rig_nodes_grp,
            parent_node=self.face_master_grp
        )
        self.face_pos_driver_grp = hierarchy_utils.ensure_group(
            self.face_pos_driver_grp,
            parent_node=self.face_master_grp
        )

        # -------------------------------------------------------------------------
        # Step 04：创建 Head Work Model 层级，并保存真实场景路径
        # -------------------------------------------------------------------------
        self.face_tweak_grp = hierarchy_utils.ensure_group(
            self.face_tweak_grp,
            parent_node=self.face_model_grp
        )
        self.face_stretch_grp = hierarchy_utils.ensure_group(
            self.face_stretch_grp,
            parent_node=self.face_model_grp
        )
        self.face_deform_grp = hierarchy_utils.ensure_group(
            self.face_deform_grp,
            parent_node=self.face_model_grp
        )

        # -------------------------------------------------------------------------
        # Step 05：刷新公共 Group 列表，后续 Module 统一复用真实 Long Path
        # -------------------------------------------------------------------------
        self.type_groups = [
            self.face_guide_grp,
            self.face_ctrl_grp,
            self.face_jnt_grp,
            self.face_rig_nodes_grp,
            self.face_pos_driver_grp,
        ]
        self.model_groups = [
            self.face_tweak_grp,
            self.face_stretch_grp,
            self.face_deform_grp,
        ]

        return True

    # =========================================================================
    # Config Node / Face API
    # =========================================================================

    def ensure_config_node(self):
        u"""
        确保 Face Config 存在。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        config_node = self.config_data.ensure()
        self.config_node = config_node
        return config_node

    def config_node_exists(self):
        u"""
        检查 Face Config Network Node 是否有效。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        return self.config_data.exists()

    def get_config_attr(self):
        u"""
        返回 Config 的底层 Attr 对象。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        return self.config_data.get_attr()

    def get_config_message(self, attr_name):
        u"""
        读取 Face Config 中保存的 Maya 节点 Message 引用。

        Args:
            attr_name (str):
                `attr_name` 对应的 Maya 节点或资源名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        return self.config_data.get_message(
            attr_name
        )

    def get_config_value(self, attr_name):
        u"""
        读取 Face Config 中保存的普通属性值。

        Args:
            attr_name (str):
                `attr_name` 对应的 Maya 节点或资源名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        return self.config_data.get_value(
            attr_name
        )

    def set_config_messages(
            self,
            attrs_dict,
            force=True,
            clear_empty=True
    ):
        u"""
        批量保存 Maya 节点引用到 Face Config。

        Args:
            attrs_dict (dict):
                Attribute 名称到 Value / Config 数据的批量映射。
            force (bool):
                是否强制覆盖已有连接、状态或结果。
            clear_empty (bool):
                批量保存 Message / Config 时，空值是否主动断开旧连接。

        Returns:
            object:
            完成设置或应用后的目标对象 / 状态结果。
        """
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
        u"""
        批量保存普通数值 / 字符串配置到 Face Config。

        Args:
            attrs_dict (dict):
                Attribute 名称到 Value / Config 数据的批量映射。
            attr_types (dict | None):
                Attribute 名称到 Maya Attribute Type 的映射；未指定的属性由调用方默认规则处理。
            lock (bool):
                是否 Lock 对应 Maya Channel / Attribute。
            hide (bool):
                是否从 Channel Box 隐藏对应 Maya Attribute。

        Returns:
            object:
            完成设置或应用后的目标对象 / 状态结果。
        """
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
        u"""
        创建当前正式 Face Config Workflow / Step 分隔属性。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.ensure_config_node()
        config_attr = self.get_config_attr()

        # -------------------------------------------------------------------------
        # Step 02：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 04：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        self.organize_config_attributes()
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def get_config_attribute_order(self):
        u"""
        返回 Face Config 在 Attribute Editor 中推荐的动态属性顺序。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
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
        u"""
        按 Workflow Step 重新排序 Config Node 的 User Defined Attribute。

        Returns:
            object | list:
            按当前 API 约定顺序返回的结果列表。
        """
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
        u"""
        读取当前 Face Workflow Step；没有 Config 时从 Step 01 开始。

        Returns:
            object | int:
            当前查询得到的整数值。
        """
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
        u"""
        把当前 Face Workflow Step 保存到 Config Node。

        Args:
            step_value (int):
                Face Wizard / Build Pipeline 当前 Step 编号。

        Returns:
            object:
            完成设置或应用后的目标对象 / 状态结果。

        Raises:
            TypeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not isinstance(step_value, int):
            raise TypeError(
                u"Current Face Step 必须是整数。"
            )

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if step_value < 1 or step_value > self.last_step_value:
            raise ValueError(
                u"Current Face Step 必须在 1～{}。".format(
                    self.last_step_value
                )
            )

        self.ensure_config_layout()
        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        config_attr = self.get_config_attr()

        config_attr.set_attr_value(
            attr=self.current_step_attr_name,
            value=step_value,
            attr_type="enum",
            lock=True,
            hide=True,
            enum_name=self.current_step_enum_name
        )

        # -------------------------------------------------------------------------
        # Step 04：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        self.organize_config_attributes()
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return step_value

    # =========================================================================
    # Setup Data
    # =========================================================================

    def refresh_setup_data(self):
        u"""
        从 Config Node 重新读取 Step 01 的最新数据。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
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
        u"""
        返回 Step 01 公共输入数据字典。

        Args:
            refresh (bool):
                读取数据前是否先从 Maya Scene / Config 重新刷新缓存。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
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

        Args:
            require_mouth_jnt_number (bool):
                当前构建、采样或查询过程使用的元素数量。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not self.config_node_exists():
            raise RuntimeError(
                u"没有找到 Face Config，请先完成 Face Setup。"
            )

        self.refresh_setup_data()

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not self.face_head_model:
            raise RuntimeError(
                u"没有读取到 Face Head Model，请先完成 Face Setup。"
            )

        mesh_utils.validate_model_transform(
            self.face_head_model,
            label=u"Face Head Model"
        )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if require_mouth_jnt_number:
            if self.mouth_jnt_number is None:
                raise RuntimeError(
                    u"没有读取到嘴唇 Jnt 数量，请先完成 Face Setup。"
                )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    # =========================================================================
    # Step State
    # =========================================================================

    @staticmethod
    def get_step_completed_attr_name(step_value):
        u"""
        根据 Step 编号生成 Config 完成状态属性名称。

        Args:
            step_value (int):
                Face Wizard / Build Pipeline 当前 Step 编号。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

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

        return "step_{:02d}_completed".format(
            step_value
        )

    def resolve_step_value(self, step_value=None):
        u"""
        获取当前操作使用的 Step 编号。

        Args:
            step_value (int):
                Face Wizard / Build Pipeline 当前 Step 编号。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

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
                Face Wizard / Build Pipeline 当前 Step 编号。
            completed (bool):
                当前 Face Wizard / Build Step 是否标记为已完成。

        Returns:
            object:
            完成设置或应用后的目标对象 / 状态结果。
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
                Face Wizard / Build Pipeline 当前 Step 编号。

        Returns:
            object | bool:
            条件成立时返回 True，否则返回 False。
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

        Args:
            step_value (int):
                Face Wizard / Build Pipeline 当前 Step 编号。
            last_step (int):
                Step 状态查询或失效处理时的最后一个 Step 编号。

        Returns:
            object | list:
            按当前 API 约定顺序返回的结果列表。

        Raises:
            TypeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        step_value = self.resolve_step_value(
            step_value
        )

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not isinstance(last_step, int):
            raise TypeError(
                u"last_step 必须是整数。"
            )

        if last_step <= step_value:
            return []

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        invalidated_steps = []
        current_step = step_value + 1

        # -------------------------------------------------------------------------
        # Step 04：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        while current_step <= last_step:
            self.set_step_completed(
                step_value=current_step,
                completed=False
            )
            invalidated_steps.append(
                current_step
            )
            current_step += 1

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return invalidated_steps

    def get_step_status(self, last_step=4):
        u"""
        返回 Face Wizard 各 Step 的完成状态。

        Args:
            last_step (int):
                Step 状态查询或失效处理时的最后一个 Step 编号。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

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
