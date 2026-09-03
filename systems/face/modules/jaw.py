# coding=utf-8
u"""
Jaw Module
==========

下巴绑定模块。

新架构流程：

    setup
        ↓
    guide
        ↓
    joint
        ↓
    control
        ↓
    connect
        ↓
    deform
        ↓
    finalize

本模块参考旧 ``legacy_reference/bind/subject/face_subject/jaw.py`` 的绑定思路，
但不再导入旧 bpjnt 文件，也不再使用字符串 replace() 推导节点名称。

保留的旧算法：
    Jaw Controller 旋转时，根据 rotateY 自动产生可调节的 X / Z 位移，
    用于制作张嘴时下巴同时前后 / 上下移动的夸张效果。

新的实现方式：
    - Guide 使用当前 Face Guide Template；
    - Joint 使用 core.joint_utils 程序创建；
    - Controller 使用 systems.ctrl_base；
    - Plug 连接使用 core.connection_utils；
    - Attribute 使用 core.attr_utils；
    - Constraint 使用 core.constraint_utils；
    - Naming 使用 RigBase / FaceBase；
    - 只在 Build 前检查已有 Scene Node，不重复验证内部 Rig Name。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import attr_utils
from ....core import connection_utils
from ....core import constraint_utils
from ....core import hierarchy_utils
from ....core import joint_utils
from ....core import matrix_utils
from ....core import scene_utils
from ....core import transform_utils
from ... import ctrl_base
from .. import config
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class JawModule(FaceModuleBase):
    u"""根据 Jaw Guide 创建 Joint、Controller 和 Jaw Open 自动位移效果。"""

    def __init__(self):
        u"""初始化 Jaw Module 的输入、名称、设置和构建结果。"""
        super(JawModule, self).__init__(
            side="md",
            part="jaw",
            index=1
        )

        self.face_guide = FaceGuide()

        # Guide
        self.jaw_start_guide_name = None
        self.jaw_end_guide_name = None
        self.jaw_start_guide = None
        self.jaw_end_guide = None

        # Controller Settings
        self.controller_global_scale = 1.0
        self.controller_color = 17
        self.controller_size = 1.0
        self.controller_radius = 1.0

        # Naming
        self.jaw_start_joint_name = None
        self.jaw_end_joint_name = None
        self.jaw_ctrl_name = None
        self.jaw_matrix_name = None

        self.jaw_open_driver_zero_name = None
        self.jaw_offset_driver_name = None
        self.jaw_ctrl_driver_name = None
        self.jaw_sub_driver_name = None
        self.jaw_open_reader_zero_name = None
        self.jaw_open_reader_name = None
        self.jaw_open_constraint_name = None
        self.jaw_open_multiply_name = None

        # Build Result
        self.jaw_start_joint = None
        self.jaw_end_joint = None
        self.jaw_ctrl_dict = None
        self.jaw_ctrl = None
        self.jaw_sub_ctrl = None
        self.jaw_output = None
        self.jaw_matrix_node = None

        self.jaw_open_driver_zero = None
        self.jaw_offset_driver = None
        self.jaw_ctrl_driver = None
        self.jaw_sub_driver = None
        self.jaw_open_reader_zero = None
        self.jaw_open_reader = None
        self.jaw_open_constraint = None
        self.jaw_open_multiply = None

    # =========================================================================
    # 01. Setup
    # =========================================================================

    def setup(self):
        u"""
        准备 Jaw 参数、标准名称、Face 公共层级和 Build 前 Scene State。

        Returns:
            bool:
                参数准备和 Scene Preflight 完成后返回 True。
        """
        # -------------------------------------------------------------------------
        # Step 01：确认 Face Setup 已经完成，并确保正式 Face 层级存在
        # -------------------------------------------------------------------------
        self.validate_setup_config(
            require_mouth_jnt_number=False
        )
        self.ensure_hierarchy()

        # -------------------------------------------------------------------------
        # Step 02：读取统一 Controller Settings，不在 Jaw Module 写第二套配置
        # -------------------------------------------------------------------------
        controller_settings = self.face_guide.load_controller_settings()

        self.controller_global_scale = controller_settings.get(
            config.face_controller_global_scale_attr,
            1.0
        )
        self.controller_color = controller_settings.get(
            config.face_controller_color_attr_names["md"],
            17
        )
        self.controller_size = controller_settings.get(
            config.face_controller_size_attr_names["jaw"],
            1.0
        )
        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        if self.controller_radius <= 0.0:
            raise ValueError(
                u"Jaw Controller Radius 必须大于 0。"
            )

        # -------------------------------------------------------------------------
        # Step 03：集中准备 Jaw 全部确定性名称，后续阶段只使用保存后的名称
        # -------------------------------------------------------------------------
        self._prepare_names()

        # -------------------------------------------------------------------------
        # Step 04：只检查 Rebuild Scene State，不重复验证内部 Naming 格式
        # -------------------------------------------------------------------------
        self._validate_build_nodes_available()

        return True

    # =========================================================================
    # 02. Guide
    # =========================================================================

    def guide(self):
        u"""
        从当前 Face Guide Template 读取 Jaw Start / End Guide。

        Returns:
            list[str]:
                按 Start、End 顺序返回两个 Jaw Guide。
        """
        # -------------------------------------------------------------------------
        # Step 01：根据当前正式 Naming 生成 Jaw Guide 名称
        # -------------------------------------------------------------------------
        self.jaw_start_guide_name = self.create_name(
            type="loc",
            part="jaw_start",
            function="guide"
        )
        self.jaw_end_guide_name = self.create_name(
            type="loc",
            part="jaw_end",
            function="guide"
        )

        # -------------------------------------------------------------------------
        # Step 02：从 FaceGuide 查询真实 Maya 节点；Guide 缺失时直接阻止 Build
        # -------------------------------------------------------------------------
        self.jaw_start_guide = self.face_guide.get_guide_node(
            self.jaw_start_guide_name,
            required=True
        )
        self.jaw_end_guide = self.face_guide.get_guide_node(
            self.jaw_end_guide_name,
            required=True
        )

        return [
            self.jaw_start_guide,
            self.jaw_end_guide,
        ]

    # =========================================================================
    # 03. Joint
    # =========================================================================

    def joint(self):
        u"""
        根据 Jaw Start / End Guide 创建两节 Jaw Bind Joint Chain。

        Returns:
            list[str]:
                Jaw Start Joint 与 Jaw End Joint。
        """
        joint_radius = self.controller_radius * 0.25

        # -------------------------------------------------------------------------
        # Step 01：在 Jaw Start Guide 创建主 Jaw Joint，并挂到 Face Joint Group
        # -------------------------------------------------------------------------
        self.jaw_start_joint = joint_utils.Joint.create_at_object(
            obj=self.jaw_start_guide,
            name=self.jaw_start_joint_name,
            parent=self.face_jnt_grp,
            match_rotation=True,
            radius=joint_radius
        )

        # -------------------------------------------------------------------------
        # Step 02：在 Jaw End Guide 创建 End Joint，并建立明确 Joint Chain
        # -------------------------------------------------------------------------
        self.jaw_end_joint = joint_utils.Joint.create_at_object(
            obj=self.jaw_end_guide,
            name=self.jaw_end_joint_name,
            parent=self.jaw_start_joint,
            match_rotation=True,
            radius=joint_radius
        )

        self.module_dict["jaw_start_joint"] = self.jaw_start_joint
        self.module_dict["jaw_end_joint"] = self.jaw_end_joint

        return [
            self.jaw_start_joint,
            self.jaw_end_joint,
        ]

    # =========================================================================
    # 04. Control
    # =========================================================================

    def control(self):
        u"""
        创建 Jaw Main Controller 与 Sub Controller。

        Returns:
            dict:
                ctrl_base.create_ctrl() 返回的完整 Jaw Controller Dict。
        """
        # -------------------------------------------------------------------------
        # Step 01：使用统一 CtrlBase 创建完整标准 Controller 层级
        # -------------------------------------------------------------------------
        self.jaw_ctrl_dict = ctrl_base.create_ctrl(
            name=self.jaw_ctrl_name,
            shape="circle",
            radius=self.controller_radius,
            color=self.controller_color,
            axis="Z+",
            target_node=self.jaw_start_guide,
            parent_node=self.face_ctrl_grp,
            create_sub_ctrl=True,
            add_to_set=True,
            ctrl_set=config.face_ctrl_set
        )

        # -------------------------------------------------------------------------
        # Step 02：保存明确业务变量，后续代码不反复从 Dict 临时猜节点用途
        # -------------------------------------------------------------------------
        self.jaw_ctrl = self.jaw_ctrl_dict["ctrl_node"]
        self.jaw_sub_ctrl = self.jaw_ctrl_dict["sub_ctrl_node"]
        self.jaw_output = self.jaw_ctrl_dict["output_node"]

        self.module_dict["jaw_ctrl_dict"] = self.jaw_ctrl_dict
        self.module_dict["jaw_ctrl"] = self.jaw_ctrl
        self.module_dict["jaw_sub_ctrl"] = self.jaw_sub_ctrl
        self.module_dict["jaw_output"] = self.jaw_output

        return self.jaw_ctrl_dict

    # =========================================================================
    # 05. Connect
    # =========================================================================

    def connect(self):
        u"""
        使用 Jaw Controller Output 驱动 Jaw Start Joint。

        Returns:
            str:
                创建出的 Parent Matrix Constraint 节点。
        """
        # -------------------------------------------------------------------------
        # Step 01：Controller 最终 Output 作为唯一 Rig Driver
        # -------------------------------------------------------------------------
        self.jaw_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.jaw_output,
            driven=self.jaw_start_joint,
            maintain_offset=False,
            name=self.jaw_matrix_name
        )

        self.module_dict["jaw_matrix"] = self.jaw_matrix_node
        return self.jaw_matrix_node

    # =========================================================================
    # 06. Deform / Special Effect
    # =========================================================================

    def deform(self):
        u"""
        创建 Jaw Open 自动位移效果。

        旧 Bind 的核心思路被保留：
        不能直接把 Jaw Ctrl 的 rotateY 回接到它自己的祖先 Connect Group，
        否则容易产生 Maya Evaluation Cycle。

        新实现创建一套独立 Rotation Driver Chain，复制 Offset / Ctrl / SubCtrl
        的局部旋转，再通过 Orient Constraint 读取累计旋转，最后把 rotateY
        乘以 Animator 可调属性，输出到 Jaw Connect Group 的 translateX / Z。

        Returns:
            dict:
                Jaw Open Driver Network 的主要节点。
        """
        jaw_grp_dict = self.jaw_ctrl_dict["grp_dict"]
        jaw_offset_grp = jaw_grp_dict["offset"]
        jaw_connect_grp = jaw_grp_dict["connect"]

        # -------------------------------------------------------------------------
        # Step 01：创建与 Jaw Rest Orientation 对齐的独立 Rotation Driver Root
        # -------------------------------------------------------------------------
        self.jaw_open_driver_zero = cmds.createNode(
            "transform",
            name=self.jaw_open_driver_zero_name,
            parent=self.face_rig_nodes_grp
        )
        self._match_world_transform(
            self.jaw_start_joint,
            self.jaw_open_driver_zero
        )

        # -------------------------------------------------------------------------
        # Step 02：复制 Offset / Ctrl / SubCtrl 的局部 Rotation，形成独立累计旋转链
        # -------------------------------------------------------------------------
        source_nodes = [
            ("offset", jaw_offset_grp, self.jaw_offset_driver_name),
            ("ctrl", self.jaw_ctrl, self.jaw_ctrl_driver_name),
            ("sub", self.jaw_sub_ctrl, self.jaw_sub_driver_name),
        ]

        driver_parent = self.jaw_open_driver_zero
        created_driver_nodes = {}

        for source_label, source_node, driver_name in source_nodes:
            if source_node is None:
                continue

            driver_node = cmds.createNode(
                "transform",
                name=driver_name,
                parent=driver_parent
            )

            connection_utils.connect_plugs(
                source_node + ".rotate",
                driver_node + ".rotate"
            )
            connection_utils.connect_plugs(
                source_node + ".rotateOrder",
                driver_node + ".rotateOrder"
            )

            created_driver_nodes[source_label] = driver_node
            driver_parent = driver_node

        self.jaw_offset_driver = created_driver_nodes.get("offset")
        self.jaw_ctrl_driver = created_driver_nodes.get("ctrl")
        self.jaw_sub_driver = created_driver_nodes.get("sub")

        # -------------------------------------------------------------------------
        # Step 03：创建与 Jaw Rest Orientation 对齐的 Rotation Reader Locator
        # -------------------------------------------------------------------------
        self.jaw_open_reader_zero = cmds.createNode(
            "transform",
            name=self.jaw_open_reader_zero_name,
            parent=self.face_rig_nodes_grp
        )
        self._match_world_transform(
            self.jaw_start_joint,
            self.jaw_open_reader_zero
        )

        jaw_open_reader_list = cmds.spaceLocator(
            name=self.jaw_open_reader_name
        )
        self.jaw_open_reader = jaw_open_reader_list[0]
        self.jaw_open_reader = hierarchy_utils.parent(
            self.jaw_open_reader,
            self.jaw_open_reader_zero
        )

        cmds.setAttr(self.jaw_open_reader + ".translate", 0.0, 0.0, 0.0)
        cmds.setAttr(self.jaw_open_reader + ".rotate", 0.0, 0.0, 0.0)

        constraint_node_list = constraint_utils.create_constraint(
            driver_objects=driver_parent,
            driven_object=self.jaw_open_reader,
            constraint_type="orientConstraint",
            maintain_offset=False,
            name=self.jaw_open_constraint_name
        )

        if not constraint_node_list:
            raise RuntimeError(
                u"Jaw Open Rotation Reader Constraint 创建失败。"
            )

        self.jaw_open_constraint = constraint_node_list[0]

        # -------------------------------------------------------------------------
        # Step 04：在 Jaw Ctrl 创建动画师可调 X / Z 位移倍率
        # -------------------------------------------------------------------------
        jaw_ctrl_attr = attr_utils.Attr(
            self.jaw_ctrl
        )
        jaw_offset_x_plug = jaw_ctrl_attr.add_attr(
            "offset_X",
            attr_type="double",
            lock=False,
            hide=False,
            default_value=0.01,
            min_value=-0.05,
            max_value=0.05,
            keyable=True,
            channel_box=True
        )
        jaw_offset_z_plug = jaw_ctrl_attr.add_attr(
            "offset_Z",
            attr_type="double",
            lock=False,
            hide=False,
            default_value=0.01,
            min_value=-0.05,
            max_value=0.05,
            keyable=True,
            channel_box=True
        )

        # -------------------------------------------------------------------------
        # Step 05：用 multiplyDivide 把累计 rotateY 转换成 Jaw Connect 位移
        # -------------------------------------------------------------------------
        self.jaw_open_multiply = cmds.createNode(
            "multiplyDivide",
            name=self.jaw_open_multiply_name
        )

        connection_utils.connect_plugs(
            self.jaw_open_reader + ".rotateY",
            self.jaw_open_multiply + ".input1X"
        )
        connection_utils.connect_plugs(
            self.jaw_open_reader + ".rotateY",
            self.jaw_open_multiply + ".input1Z"
        )
        connection_utils.connect_plugs(
            jaw_offset_x_plug,
            self.jaw_open_multiply + ".input2X"
        )
        connection_utils.connect_plugs(
            jaw_offset_z_plug,
            self.jaw_open_multiply + ".input2Z"
        )
        connection_utils.connect_plugs(
            self.jaw_open_multiply + ".outputX",
            jaw_connect_grp + ".translateX"
        )
        connection_utils.connect_plugs(
            self.jaw_open_multiply + ".outputZ",
            jaw_connect_grp + ".translateZ"
        )

        jaw_open_dict = {
            "driver_zero": self.jaw_open_driver_zero,
            "offset_driver": self.jaw_offset_driver,
            "ctrl_driver": self.jaw_ctrl_driver,
            "sub_driver": self.jaw_sub_driver,
            "reader_zero": self.jaw_open_reader_zero,
            "reader": self.jaw_open_reader,
            "constraint": self.jaw_open_constraint,
            "multiply": self.jaw_open_multiply,
        }
        self.module_dict["jaw_open_dict"] = jaw_open_dict

        return jaw_open_dict

    # =========================================================================
    # 07. Finalize
    # =========================================================================

    def finalize(self):
        u"""
        验证 Jaw Module 最终节点，并返回统一 Module Dict。

        Returns:
            bool:
                所有关键 Build Node 存在时返回 True。
        """
        required_nodes = [
            self.jaw_start_joint,
            self.jaw_end_joint,
            self.jaw_ctrl,
            self.jaw_output,
            self.jaw_matrix_node,
            self.jaw_open_driver_zero,
            self.jaw_open_reader,
            self.jaw_open_constraint,
            self.jaw_open_multiply,
        ]

        # -------------------------------------------------------------------------
        # Step 01：最终只验证真实 Scene State，不重新验证内部名称格式
        # -------------------------------------------------------------------------
        for node in required_nodes:
            if not node:
                raise RuntimeError(
                    u"Jaw Module 构建结果不完整。"
                )

            scene_utils.validate_node(
                node,
                label=u"Jaw Module Build Node"
            )

        self.module_dict["built"] = True
        return True

    # =========================================================================
    # Naming / Scene State
    # =========================================================================

    def _prepare_names(self):
        u"""集中准备 Jaw Module 的全部标准 Rig Name。"""
        # -------------------------------------------------------------------------
        # Step 01：Joint / Controller / Matrix
        # -------------------------------------------------------------------------
        self.jaw_start_joint_name = self.create_name(
            type="jnt",
            part="jaw_start",
            function="bind"
        )
        self.jaw_end_joint_name = self.create_name(
            type="jnt",
            part="jaw_end",
            function="bind"
        )
        self.jaw_ctrl_name = self.create_name(
            type="ctrl",
            part="jaw",
            function="bind"
        )
        self.jaw_matrix_name = self.create_name(
            type="mult",
            part="jaw",
            function="parent"
        )

        # -------------------------------------------------------------------------
        # Step 02：Jaw Open Rotation Driver
        # -------------------------------------------------------------------------
        self.jaw_open_driver_zero_name = self.create_name(
            type="zero",
            part="jaw_open",
            function="driver"
        )
        self.jaw_offset_driver_name = self.create_name(
            type="grp",
            part="jaw_offset",
            function="driver"
        )
        self.jaw_ctrl_driver_name = self.create_name(
            type="grp",
            part="jaw_ctrl",
            function="driver"
        )
        self.jaw_sub_driver_name = self.create_name(
            type="grp",
            part="jaw_sub",
            function="driver"
        )

        # -------------------------------------------------------------------------
        # Step 03：Jaw Open Rotation Reader / Math
        # -------------------------------------------------------------------------
        self.jaw_open_reader_zero_name = self.create_name(
            type="zero",
            part="jaw_open",
            function="reader"
        )
        self.jaw_open_reader_name = self.create_name(
            type="loc",
            part="jaw_open",
            function="reader"
        )
        self.jaw_open_constraint_name = self.create_name(
            type="cns",
            part="jaw_open",
            function="reader"
        )
        self.jaw_open_multiply_name = self.create_name(
            type="mult",
            part="jaw_open",
            function="driver"
        )

        return True

    def _validate_build_nodes_available(self):
        u"""检查上一次 Jaw Build 的确定性节点是否仍存在。"""
        expected_nodes = [
            self.jaw_start_joint_name,
            self.jaw_end_joint_name,
            self.jaw_matrix_name,
            self.jaw_open_driver_zero_name,
            self.jaw_offset_driver_name,
            self.jaw_ctrl_driver_name,
            self.jaw_sub_driver_name,
            self.jaw_open_reader_zero_name,
            self.jaw_open_reader_name,
            self.jaw_open_constraint_name,
            self.jaw_open_multiply_name,
        ]

        jaw_ctrl_hierarchy_names = ctrl_base.get_ctrl_hierarchy_names(
            self.jaw_ctrl_name,
            create_sub_ctrl=True
        )

        for hierarchy_key in jaw_ctrl_hierarchy_names:
            hierarchy_name = jaw_ctrl_hierarchy_names[hierarchy_key]

            if hierarchy_name is None:
                continue

            expected_nodes.append(
                hierarchy_name
            )

        scene_utils.ensure_nodes_available(
            expected_nodes,
            label=u"Jaw Module Build Node"
        )
        return True

    @staticmethod
    def _match_world_transform(source_node, target_node):
        u"""
        把 Target 的世界位置和旋转匹配到 Source。

        Args:
            source_node (str):
                提供 World Transform 的 Maya 节点。
            target_node (str):
                接收 World Transform 的 Maya 节点。

        Returns:
            str:
                完成匹配后的 Target 节点。
        """
        source_translation = transform_utils.get_world_translation(
            source_node
        )
        source_rotation = transform_utils.get_world_rotation(
            source_node
        )

        transform_utils.set_world_translation(
            target_node,
            source_translation
        )
        transform_utils.set_world_rotation(
            target_node,
            source_rotation
        )
        return target_node


def build_jaw():
    u"""
    构建 Jaw Module，并返回统一模块结果字典。

    Returns:
        dict:
            JawModule.build() 的完整公开结果。
    """
    jaw_module = JawModule()
    jaw_module_dict = jaw_module.build()
    return jaw_module_dict


__all__ = [
    "JawModule",
    "build_jaw",
]
