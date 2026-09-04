# coding=utf-8
u"""
Joint Tool
==========

Maya 2023+ Joint 工具面板。

模块职责
--------
1. Joint Radius、Local Rotation Axis 与 Joint Orient Channel 显示管理；
2. Maya 原生 Joint / IK / Skin Options 入口；
3. Joint 创建、Child Joint、Joint Chain 和 Curve / Edge 转 Joint；
4. Segment Scale Compensate 管理；
5. Joint Chain Curve 与批量 Parent Constraint 辅助；
6. Skin Weight Copy 入口；
7. 提供可在 Maya Script Editor 中直接显示的 ``main()``。

架构边界
--------
- Selection / Scene Query 使用 ``core.scene_utils``；
- 单 Joint 能力使用 ``core.joint_utils``；
- 多 Joint / Curve CV -> Joint 使用 ``core.joint_chain_utils``；
- DAG Hierarchy 使用 ``core.hierarchy_utils``；
- Curve 创建使用 ``core.curve_utils``；
- Attribute Channel State 使用 ``core.attr_utils``；
- Constraint 使用 ``core.constraint_utils``；
- Skin 使用 ``core.skin_utils``；
- Tool 只保留 UI、Selection 语义、Warning 和命令编排；
- 不重新引入退休的 JointChain / JointCurve / Selection Compatibility 类。
"""

from __future__ import print_function

import maya.cmds as cmds
import maya.mel as mel

try:
    from PySide2.QtWidgets import QDoubleSpinBox
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QScrollArea
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QDoubleSpinBox
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QScrollArea
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...app import window_manager
from ...core import attr_utils
from ...core import constraint_utils
from ...core import curve_utils
from ...core import hierarchy_utils
from ...core import jnt_chain_utils
from ...core import jnt_utils
from ...core import rename_utils
from ...core import scene_utils
from ...core import skin_utils
from ...core import transform_utils
from ...ui import theme
from ...ui import window_utils
from . import joint_resamp_tool


class JointTool(QWidget):
    """木子绑定工具集 Joint 工具。"""

    def __init__(self, parent=None):
        u"""
        创建 Joint 工具窗口。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """
        super(JointTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"Joint 工具",
            minimum_width=560
        )
        self.resize(600, 780)

    # =========================================================================
    # UI
    # =========================================================================

    def create_widgets(self):
        u"""
        创建窗口控件。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.title_label = theme.make_title(u"Joint 工具")
        self.subtitle_label = theme.make_subtitle(
            u"集中处理 Joint 显示、创建、链编辑、Orient、IK 入口和常用 Skin 操作。"
        )

        self.joint_size_spinbox = QDoubleSpinBox()
        self.joint_size_spinbox.setDecimals(2)
        self.joint_size_spinbox.setRange(0.01, 100.0)
        self.joint_size_spinbox.setSingleStep(0.1)
        self.joint_size_spinbox.setValue(0.5)

        self.show_axis_selected_button = QPushButton(u"显示轴向 · 选择")
        self.hide_axis_selected_button = QPushButton(u"隐藏轴向 · 选择")
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.show_axis_hierarchy_button = QPushButton(u"显示轴向 · 层级")
        self.hide_axis_hierarchy_button = QPushButton(u"隐藏轴向 · 层级")
        self.show_axis_all_button = QPushButton(u"显示轴向 · 全部")
        self.hide_axis_all_button = QPushButton(u"隐藏轴向 · 全部")

        self.orient_options_button = QPushButton(u"Joint Orient Options")
        self.mirror_options_button = QPushButton(u"Mirror Joint Options")
        self.ik_handle_options_button = QPushButton(u"IK Handle Options")
        self.ik_spline_options_button = QPushButton(u"IK Spline Options")

        self.create_snap_joint_button = QPushButton(u"按选择创建 Joint")
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.create_child_joint_button = QPushButton(u"创建子 Joint")
        self.resample_joint_button = QPushButton(u"关节重采样")
        theme.style_primary(self.resample_joint_button)

        self.parent_chain_button = QPushButton(u"按选择顺序组成 Joint Chain")
        self.curve_chain_button = QPushButton(u"Curve CV 创建 Joint Chain")
        self.edge_chain_button = QPushButton(u"Polygon Edge 创建 Joint Chain")

        self.enable_scale_compensate_button = QPushButton(
            u"开启 Segment Scale Compensate"
        )
        self.disable_scale_compensate_button = QPushButton(
            u"关闭 Segment Scale Compensate"
        )

        self.show_orient_button = QPushButton(u"显示 Joint Orient")
        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.hide_orient_button = QPushButton(u"隐藏 Joint Orient")
        self.clear_orient_button = QPushButton(u"归零 Joint Orient")

        self.create_curve_on_joints_button = QPushButton(
            u"Joint Chain 创建 Curve"
        )
        self.batch_parent_constraint_button = QPushButton(
            u"按顺序批量 Parent Constraint"
        )

        self.bind_skin_options_button = QPushButton(u"Smooth Bind Options")
        self.detach_skin_options_button = QPushButton(u"Detach Skin Options")
        self.paint_skin_options_button = QPushButton(u"Paint Skin Weights")
        self.mirror_skin_options_button = QPushButton(u"Mirror Skin Weights")
        self.copy_skin_button = QPushButton(u"复制 Skin Weights")
        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.style_primary(self.copy_skin_button)

    def create_layouts(self):
        u"""
        创建滚动 Card 布局。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        root_layout.addWidget(self.title_label)
        root_layout.addWidget(self.subtitle_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 6, 0)
        scroll_layout.setSpacing(12)

        display_card, display_layout = theme.make_card(scroll_widget)
        display_layout.addWidget(theme.make_section_title(u"Joint 显示"))

        radius_layout = QHBoxLayout()
        radius_layout.setContentsMargins(0, 0, 0, 0)
        radius_layout.addWidget(QLabel(u"全局 Joint Radius"))
        radius_layout.addWidget(self.joint_size_spinbox)
        radius_layout.addStretch(1)
        display_layout.addLayout(radius_layout)

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        display_grid = QGridLayout()
        display_grid.setHorizontalSpacing(8)
        display_grid.setVerticalSpacing(8)
        display_grid.addWidget(self.show_axis_selected_button, 0, 0)
        display_grid.addWidget(self.hide_axis_selected_button, 0, 1)
        display_grid.addWidget(self.show_axis_hierarchy_button, 1, 0)
        display_grid.addWidget(self.hide_axis_hierarchy_button, 1, 1)
        display_grid.addWidget(self.show_axis_all_button, 2, 0)
        display_grid.addWidget(self.hide_axis_all_button, 2, 1)
        display_layout.addLayout(display_grid)

        maya_card, maya_layout = theme.make_card(scroll_widget)
        maya_layout.addWidget(theme.make_section_title(u"Maya Joint / IK"))

        maya_grid = QGridLayout()
        maya_grid.setHorizontalSpacing(8)
        maya_grid.setVerticalSpacing(8)
        maya_grid.addWidget(self.orient_options_button, 0, 0)
        maya_grid.addWidget(self.mirror_options_button, 0, 1)
        maya_grid.addWidget(self.ik_handle_options_button, 1, 0)
        maya_grid.addWidget(self.ik_spline_options_button, 1, 1)
        # -------------------------------------------------------------------------
        # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        maya_layout.addLayout(maya_grid)

        create_card, create_layout = theme.make_card(scroll_widget)
        create_layout.addWidget(theme.make_section_title(u"Joint 创建与编辑"))

        create_grid = QGridLayout()
        create_grid.setHorizontalSpacing(8)
        create_grid.setVerticalSpacing(8)
        create_grid.addWidget(self.create_snap_joint_button, 0, 0)
        create_grid.addWidget(self.create_child_joint_button, 0, 1)
        create_grid.addWidget(self.resample_joint_button, 1, 0)
        create_grid.addWidget(self.parent_chain_button, 1, 1)
        create_grid.addWidget(self.curve_chain_button, 2, 0)
        create_grid.addWidget(self.edge_chain_button, 2, 1)
        create_grid.addWidget(self.enable_scale_compensate_button, 3, 0)
        create_grid.addWidget(self.disable_scale_compensate_button, 3, 1)
        create_grid.addWidget(self.show_orient_button, 4, 0)
        create_grid.addWidget(self.hide_orient_button, 4, 1)
        create_grid.addWidget(self.clear_orient_button, 5, 0)
        create_grid.addWidget(self.create_curve_on_joints_button, 5, 1)
        create_grid.addWidget(
            self.batch_parent_constraint_button,
            6,
            0,
            1,
            2
        )
        # -------------------------------------------------------------------------
        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        create_layout.addLayout(create_grid)

        skin_card, skin_layout = theme.make_card(scroll_widget)
        skin_layout.addWidget(theme.make_section_title(u"Skin"))

        skin_grid = QGridLayout()
        skin_grid.setHorizontalSpacing(8)
        skin_grid.setVerticalSpacing(8)
        skin_grid.addWidget(self.bind_skin_options_button, 0, 0)
        skin_grid.addWidget(self.detach_skin_options_button, 0, 1)
        skin_grid.addWidget(self.paint_skin_options_button, 1, 0)
        skin_grid.addWidget(self.mirror_skin_options_button, 1, 1)
        skin_grid.addWidget(self.copy_skin_button, 2, 0, 1, 2)
        skin_layout.addLayout(skin_grid)

        scroll_layout.addWidget(display_card)
        scroll_layout.addWidget(maya_card)
        scroll_layout.addWidget(create_card)
        scroll_layout.addWidget(skin_card)
        scroll_layout.addStretch(1)

        scroll_area.setWidget(scroll_widget)
        # -------------------------------------------------------------------------
        # Step 05：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        root_layout.addWidget(scroll_area, 1)

    def create_connections(self):
        u"""
        连接界面信号。
        """
        # -------------------------------------------------------------------------
        # Step 01：建立当前阶段需要的层级、连接或驱动关系
        # -------------------------------------------------------------------------
        self.joint_size_spinbox.valueChanged.connect(self.set_joint_size)
        self.show_axis_selected_button.clicked.connect(self.show_axis_selected)
        self.hide_axis_selected_button.clicked.connect(self.hide_axis_selected)
        self.show_axis_hierarchy_button.clicked.connect(self.show_axis_hierarchy)
        self.hide_axis_hierarchy_button.clicked.connect(self.hide_axis_hierarchy)
        self.show_axis_all_button.clicked.connect(self.show_axis_all)
        self.hide_axis_all_button.clicked.connect(self.hide_axis_all)
        # -------------------------------------------------------------------------
        # Step 02：建立当前阶段需要的层级、连接或驱动关系
        # -------------------------------------------------------------------------
        self.orient_options_button.clicked.connect(self.open_orient_options)
        self.mirror_options_button.clicked.connect(self.open_mirror_options)
        self.ik_handle_options_button.clicked.connect(self.open_ik_handle_options)
        self.ik_spline_options_button.clicked.connect(self.open_ik_spline_options)
        self.create_snap_joint_button.clicked.connect(self.create_snap_joints)
        self.create_child_joint_button.clicked.connect(self.create_child_joints)
        self.resample_joint_button.clicked.connect(self.open_resample_tool)
        # -------------------------------------------------------------------------
        # Step 03：建立当前阶段需要的层级、连接或驱动关系
        # -------------------------------------------------------------------------
        self.parent_chain_button.clicked.connect(self.parent_selected_chain)
        self.curve_chain_button.clicked.connect(self.create_joints_on_curves)
        self.edge_chain_button.clicked.connect(self.create_joints_on_edges)
        self.enable_scale_compensate_button.clicked.connect(self.enable_scale_compensate)
        self.disable_scale_compensate_button.clicked.connect(self.disable_scale_compensate)
        self.show_orient_button.clicked.connect(self.show_orient)
        self.hide_orient_button.clicked.connect(self.hide_orient)
        # -------------------------------------------------------------------------
        # Step 04：建立当前阶段需要的层级、连接或驱动关系
        # -------------------------------------------------------------------------
        self.clear_orient_button.clicked.connect(self.clear_joint_orient)
        self.create_curve_on_joints_button.clicked.connect(self.create_curve_on_joints)
        self.batch_parent_constraint_button.clicked.connect(self.batch_parent_constraint)
        self.bind_skin_options_button.clicked.connect(self.open_bind_skin_options)
        self.detach_skin_options_button.clicked.connect(self.open_detach_skin_options)
        self.paint_skin_options_button.clicked.connect(self.open_paint_skin_options)
        self.mirror_skin_options_button.clicked.connect(self.open_mirror_skin_options)
        # -------------------------------------------------------------------------
        # Step 05：建立当前阶段需要的层级、连接或驱动关系
        # -------------------------------------------------------------------------
        self.copy_skin_button.clicked.connect(self.copy_skin_weights)

    # =========================================================================
    # Maya Option Windows
    # =========================================================================

    @staticmethod
    def open_orient_options():
        u"""
        打开 Maya Joint Orient Options。
        """
        mel.eval("OrientJointOptions;")

    @staticmethod
    def open_mirror_options():
        u"""
        打开 Maya Mirror Joint Options。
        """
        mel.eval("MirrorJointOptions;")

    @staticmethod
    def open_ik_handle_options():
        u"""
        打开 Maya IK Handle Options。
        """
        mel.eval("IKHandleToolOptions;")

    @staticmethod
    def open_ik_spline_options():
        u"""
        打开 Maya IK Spline Options。
        """
        mel.eval("IKSplineHandleToolOptions;")

    @staticmethod
    def open_bind_skin_options():
        u"""
        打开 Maya Smooth Bind Skin Options。
        """
        mel.eval("SmoothBindSkinOptions;")

    @staticmethod
    def open_detach_skin_options():
        u"""
        打开 Maya Detach Skin Options。
        """
        mel.eval("DetachSkinOptions;")

    @staticmethod
    def open_paint_skin_options():
        u"""
        打开 Maya Paint Skin Weights。
        """
        mel.eval("ArtPaintSkinWeightsToolOptions;")

    @staticmethod
    def open_mirror_skin_options():
        u"""
        打开 Maya Mirror Skin Weights Options。
        """
        mel.eval("MirrorSkinWeightsOptions;")

    # =========================================================================
    # Selection
    # =========================================================================

    @staticmethod
    def get_selected_joints():
        u"""
        返回当前选择 Joint；空选择时显示 Tool Warning。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        joints = scene_utils.get_selected_nodes(
            node_type="joint",
            long=True,
            flatten=True
        )

        if not joints:
            cmds.warning(
                u"请先选择一个或以上的 Joint。"
            )

        return joints

    # =========================================================================
    # Joint Display
    # =========================================================================

    def set_joint_size(self, value):
        u"""
        设置全场景 Joint Radius。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """
        joints = scene_utils.get_nodes_by_type(
            "joint",
            long=True
        )

        for joint in joints:
            joint_utils.Joint(
                joint
            ).set_radius(
                float(value)
            )

    def show_axis_selected(self):
        u"""
        执行当前 API 的主要处理流程。
        """

        self.set_axis_visibility(True, False, False)

    def hide_axis_selected(self):
        u"""
        执行当前 API 的主要处理流程。
        """

        self.set_axis_visibility(False, False, False)

    def show_axis_hierarchy(self):
        u"""
        执行当前 API 的主要处理流程。
        """

        self.set_axis_visibility(True, True, False)

    def hide_axis_hierarchy(self):
        u"""
        执行当前 API 的主要处理流程。
        """

        self.set_axis_visibility(False, True, False)

    def show_axis_all(self):
        u"""
        执行当前 API 的主要处理流程。
        """

        self.set_axis_visibility(True, False, True)

    def hide_axis_all(self):
        u"""
        执行当前 API 的主要处理流程。
        """

        self.set_axis_visibility(False, False, True)

    @staticmethod
    def set_axis_visibility(visible, hierarchy, all_joints):
        u"""
        设置选择、选择层级或场景全部 Joint 的 Local Rotation Axis。

        Args:
            visible (bool):
                Joint / Guide / UI 元素是否保持可见。
            hierarchy (bool | str):
                Joint Tool 当前是否按 Skeleton Hierarchy 工作，或用于指定层级范围。
            all_joints (str | list[str]):
                当前 Joint Tool 已解析出的完整 Joint 列表。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        process_joints = []

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if all_joints:
            process_joints = scene_utils.get_nodes_by_type(
                "joint",
                long=True
            )
        else:
            selected_joints = JointTool.get_selected_joints()

            if not selected_joints:
                return

            for selected_joint in selected_joints:
                if hierarchy:
                    hierarchy_joints = hierarchy_utils.get_descendants(
                        selected_joint,
                        node_type="joint",
                        include_root=True,
                        full_path=True
                    )

                    for hierarchy_joint in hierarchy_joints:
                        if hierarchy_joint not in process_joints:
                            process_joints.append(
                                hierarchy_joint
                            )
                else:
                    if selected_joint not in process_joints:
                        process_joints.append(
                            selected_joint
                        )

        # -------------------------------------------------------------------------
        # Step 03：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for joint in process_joints:
            joint_object = joint_utils.Joint(
                joint
            )

            if visible:
                joint_object.show_axis()
            else:
                joint_object.hide_axis()

    # =========================================================================
    # Joint Create / Edit
    # =========================================================================

    def create_snap_joints(self):
        u"""
        在当前选择的 Object / Component 世界位置创建 Joint。
        """
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        if not selections:
            cmds.warning(
                u"请选择一个或以上的物体或组件。"
            )
            return

        scene_utils.open_undo_chunk(
            "MuziCreateSnapJoints"
        )

        try:
            joints = joint_chain_utils.create_joints_at_items(
                items=selections,
                name_prefix="jnt_snap",
                parent_chain=False,
                radius=self.joint_size_spinbox.value()
            )

            if joints:
                cmds.select(
                    joints,
                    replace=True
                )
        except Exception as error:
            cmds.warning(
                str(error)
            )
        finally:
            scene_utils.close_undo_chunk()

    def create_child_joints(self):
        u"""
        为当前选择的 Transform / Joint 创建同姿态 Child Joint。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not selections:
            cmds.warning(
                u"请选择一个或以上的 Transform / Joint。"
            )
            return

        created_joints = []

        # -------------------------------------------------------------------------
        # Step 03：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        scene_utils.open_undo_chunk(
            "MuziCreateChildJoints"
        )

        # -------------------------------------------------------------------------
        # Step 04：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            for selected_object in selections:
                transform_utils.validate_transform(
                    selected_object
                )
                short_name = rename_utils.get_short_name(
                    selected_object
                )
                child_name = "{}_child".format(
                    short_name
                )

                if not child_name.startswith("jnt_"):
                    child_name = "jnt_{}".format(
                        child_name
                    )

                joint = jnt_utils.Joint.create_at_object(
                    obj=selected_object,
                    name=child_name,
                    parent=selected_object,
                    match_rotation=True,
                    radius=self.joint_size_spinbox.value()
                )
                created_joints.append(
                    joint
                )
        except Exception as error:
            cmds.warning(
                str(error)
            )
        finally:
            scene_utils.close_undo_chunk()

        # -------------------------------------------------------------------------
        # Step 05：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if created_joints:
            cmds.select(
                created_joints,
                replace=True
            )

    @staticmethod
    def open_resample_tool():
        u"""
        通过统一 Window Manager 打开 Joint Resample。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        return window_manager.show_tool(
            "joint/joint_resample",
            joint_resamp_tool.main
        )

    @staticmethod
    def parent_selected_chain():
        u"""
        按照当前 Joint Selection 顺序组成父子链。
        """
        joints = JointTool.get_selected_joints()

        if not joints:
            return

        scene_utils.open_undo_chunk(
            "MuziParentJointChain"
        )

        try:
            joint_chain_utils.parent_joints_as_chain(
                joints
            )
        except Exception as error:
            cmds.warning(
                str(error)
            )
        finally:
            scene_utils.close_undo_chunk()

    def create_joints_on_curves(self):
        u"""
        根据选择 Curve 的 CV 创建 Joint Chain。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not selections:
            cmds.warning(
                u"请选择一条或多条 NURBS Curve。"
            )
            return

        created_joints = []

        # -------------------------------------------------------------------------
        # Step 03：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        scene_utils.open_undo_chunk(
            "MuziCurveJointChain"
        )

        # -------------------------------------------------------------------------
        # Step 04：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            for curve in selections:
                result = joint_chain_utils.create_joints_on_curve_cvs(
                    curve=curve,
                    parent_chain=True,
                    create_group=True,
                    radius=self.joint_size_spinbox.value()
                )
                joints = result.get(
                    "jnt_list"
                ) or []

                for joint in joints:
                    created_joints.append(
                        joint
                    )
        except Exception as error:
            cmds.warning(
                str(error)
            )
        finally:
            scene_utils.close_undo_chunk()

        # -------------------------------------------------------------------------
        # Step 05：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if created_joints:
            cmds.select(
                created_joints,
                replace=True
            )

    def create_joints_on_edges(self):
        u"""
        把当前 Polygon Edge Selection 转 Curve 后创建 Joint Chain。
        """
        scene_utils.open_undo_chunk(
            "MuziEdgeJointChain"
        )

        try:
            curve = curve_utils.create_curve_from_selected_edges(
                name="crv_edge_joint_chain_001",
                degree=3,
                form=2
            )
            result = joint_chain_utils.create_joints_on_curve_cvs(
                curve=curve,
                parent_chain=True,
                create_group=True,
                radius=self.joint_size_spinbox.value()
            )
            joints = result.get(
                "jnt_list"
            ) or []

            if joints:
                cmds.select(
                    joints,
                    replace=True
                )
        except Exception as error:
            cmds.warning(
                str(error)
            )
        finally:
            scene_utils.close_undo_chunk()

    def enable_scale_compensate(self):
        u"""
        执行当前 API 的主要处理流程。
        """

        self.set_scale_compensate(True)

    def disable_scale_compensate(self):
        u"""
        执行当前 API 的主要处理流程。
        """

        self.set_scale_compensate(False)

    def set_scale_compensate(self, enabled):
        u"""
        设置选择 Joint 的 Segment Scale Compensate。

        Args:
            enabled (bool):
                当前 UI 控件或 Rig 功能是否启用。
        """
        joints = self.get_selected_joints()

        if not joints:
            return

        scene_utils.open_undo_chunk(
            "MuziScaleCompensate"
        )

        try:
            for joint in joints:
                joint_utils.Joint(
                    joint
                ).set_scale_compensate(
                    enabled=enabled
                )
        finally:
            scene_utils.close_undo_chunk()

    def show_orient(self):
        u"""
        执行当前 API 的主要处理流程。
        """

        self.set_orient_visibility(True)

    def hide_orient(self):
        u"""
        执行当前 API 的主要处理流程。
        """

        self.set_orient_visibility(False)

    def set_orient_visibility(self, visible):
        u"""
        显示或隐藏选择 Joint 的 jointOrient Channel。

        Args:
            visible (bool):
                Joint / Guide / UI 元素是否保持可见。
        """
        joints = self.get_selected_joints()

        if not joints:
            return

        orient_attrs = [
            "jointOrientX",
            "jointOrientY",
            "jointOrientZ",
        ]

        for joint in joints:
            joint_attr = attr_utils.Attr(
                joint
            )
            joint_attr.set_attrs_state(
                orient_attrs,
                keyable=visible
            )

    def clear_joint_orient(self):
        u"""
        清空选择 Joint 的 jointOrientXYZ。
        """
        joints = self.get_selected_joints()

        if not joints:
            return

        scene_utils.open_undo_chunk(
            "MuziClearJointOrient"
        )

        try:
            for joint in joints:
                joint_utils.Joint(
                    joint
                ).clear_joint_orient()
        finally:
            scene_utils.close_undo_chunk()

    def create_curve_on_joints(self):
        u"""
        按照选择 Joint 世界位置创建 Curve。
        """
        joints = self.get_selected_joints()

        if len(joints) < 2:
            cmds.warning(
                u"至少选择两个 Joint。"
            )
            return

        degree = 3

        if len(joints) < 4:
            degree = 1

        try:
            curve = curve_utils.create_curve_from_nodes(
                nodes=joints,
                name="crv_joint_chain_001",
                degree=degree
            )
        except Exception as error:
            cmds.warning(
                str(error)
            )
            return

        cmds.select(
            curve,
            replace=True
        )

    @staticmethod
    def batch_parent_constraint():
        u"""
        按照 driver/driven 成对顺序批量创建 Parent Constraint。
        """
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        if len(selections) < 2 or len(selections) % 2 != 0:
            cmds.warning(
                u"请按 driver1, driven1, driver2, driven2... 的顺序选择偶数个对象。"
            )
            return

        scene_utils.open_undo_chunk(
            "MuziBatchParentConstraint"
        )

        try:
            selection_index = 0

            while selection_index < len(selections):
                driver = selections[selection_index]
                driven = selections[selection_index + 1]

                constraint_utils.create_constraint(
                    driver_objects=driver,
                    driven_object=driven,
                    constraint_type="parentConstraint",
                    maintain_offset=True
                )

                selection_index += 2
        finally:
            scene_utils.close_undo_chunk()

    # =========================================================================
    # Skin
    # =========================================================================

    @staticmethod
    def copy_skin_weights():
        u"""
        把第一个选择模型 Skin Weight 复制到后续选择模型。
        """
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        if len(selections) < 2:
            cmds.warning(
                u"请先选择源模型，再选择一个或多个目标模型。"
            )
            return

        source_mesh = selections[0]
        target_meshes = selections[1:]

        try:
            result = skin_utils.copy_skin_weights(
                source=source_mesh,
                targets=target_meshes
            )
        except Exception as error:
            cmds.warning(
                str(error)
            )
            return

        if result:
            print(
                u"[Joint Tool] 已复制 Skin Weight 到 {} 个目标。".format(
                    len(result)
                )
            )


def main():
    u"""
    创建或恢复 Joint Tool，立即显示并返回 QWidget。

    Returns:
        object:
        当前工具入口创建并显示的窗口或执行结果。
    """
    return window_utils.show_window(
        "tools.joint.joint_tool",
        JointTool
    )


__all__ = [
    "JointTool",
    "main",
]
