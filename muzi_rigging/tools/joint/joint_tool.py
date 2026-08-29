# coding=utf-8
u"""
Joint Tool
==========

Maya 2023+ 关节工具面板。

职责：
    1. Joint 显示与轴向管理；
    2. Maya 原生 Joint / IK / Skin 选项入口；
    3. Joint 创建、链整理和 Curve / Edge 转 Joint；
    4. Segment Scale Compensate 与 Joint Orient 管理；
    5. 关节链 Curve、批量 Parent Constraint；
    6. Skin Weight 复制入口。

架构：
    - Joint 算法调用 core.jointUtils；
    - Skin 算法调用 core.skin_utils；
    - 子工具窗口统一交给 app.window_manager；
    - 本文件只负责 UI、参数收集和执行入口。
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
from ...core import jointUtils
from ...core import skin_utils
from ...ui import theme
from . import joint_resamp_tool


class JointTool(QWidget):
    """木子绑定工具集 Joint 工具。"""

    def __init__(self, parent=None):
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
        """创建窗口控件。"""
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
        self.show_axis_hierarchy_button = QPushButton(u"显示轴向 · 层级")
        self.hide_axis_hierarchy_button = QPushButton(u"隐藏轴向 · 层级")
        self.show_axis_all_button = QPushButton(u"显示轴向 · 全部")
        self.hide_axis_all_button = QPushButton(u"隐藏轴向 · 全部")

        self.orient_options_button = QPushButton(u"Joint Orient Options")
        self.mirror_options_button = QPushButton(u"Mirror Joint Options")
        self.ik_handle_options_button = QPushButton(u"IK Handle Options")
        self.ik_spline_options_button = QPushButton(u"IK Spline Options")

        self.create_snap_joint_button = QPushButton(u"按选择创建 Joint")
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
        theme.style_primary(self.copy_skin_button)

    def create_layouts(self):
        """创建滚动 Card 布局。"""
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
        display_layout.addWidget(
            theme.make_section_title(u"Joint 显示")
        )

        radius_layout = QHBoxLayout()
        radius_layout.setContentsMargins(0, 0, 0, 0)
        radius_layout.addWidget(QLabel(u"全局 Joint Radius"))
        radius_layout.addWidget(self.joint_size_spinbox)
        radius_layout.addStretch(1)
        display_layout.addLayout(radius_layout)

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
        maya_layout.addWidget(
            theme.make_section_title(u"Maya Joint / IK")
        )

        maya_grid = QGridLayout()
        maya_grid.setHorizontalSpacing(8)
        maya_grid.setVerticalSpacing(8)
        maya_grid.addWidget(self.orient_options_button, 0, 0)
        maya_grid.addWidget(self.mirror_options_button, 0, 1)
        maya_grid.addWidget(self.ik_handle_options_button, 1, 0)
        maya_grid.addWidget(self.ik_spline_options_button, 1, 1)
        maya_layout.addLayout(maya_grid)

        create_card, create_layout = theme.make_card(scroll_widget)
        create_layout.addWidget(
            theme.make_section_title(u"Joint 创建与编辑")
        )

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
        create_layout.addLayout(create_grid)

        skin_card, skin_layout = theme.make_card(scroll_widget)
        skin_layout.addWidget(
            theme.make_section_title(u"Skin")
        )

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
        root_layout.addWidget(scroll_area, 1)

    def create_connections(self):
        """连接界面信号。"""
        self.joint_size_spinbox.valueChanged.connect(
            self.set_joint_size
        )

        self.show_axis_selected_button.clicked.connect(
            self.show_axis_selected
        )
        self.hide_axis_selected_button.clicked.connect(
            self.hide_axis_selected
        )
        self.show_axis_hierarchy_button.clicked.connect(
            self.show_axis_hierarchy
        )
        self.hide_axis_hierarchy_button.clicked.connect(
            self.hide_axis_hierarchy
        )
        self.show_axis_all_button.clicked.connect(
            self.show_axis_all
        )
        self.hide_axis_all_button.clicked.connect(
            self.hide_axis_all
        )

        self.orient_options_button.clicked.connect(
            self.open_orient_options
        )
        self.mirror_options_button.clicked.connect(
            self.open_mirror_options
        )
        self.ik_handle_options_button.clicked.connect(
            self.open_ik_handle_options
        )
        self.ik_spline_options_button.clicked.connect(
            self.open_ik_spline_options
        )

        self.create_snap_joint_button.clicked.connect(
            self.create_snap_joints
        )
        self.create_child_joint_button.clicked.connect(
            self.create_child_joints
        )
        self.resample_joint_button.clicked.connect(
            self.open_resample_tool
        )
        self.parent_chain_button.clicked.connect(
            self.parent_selected_chain
        )
        self.curve_chain_button.clicked.connect(
            self.create_joints_on_curves
        )
        self.edge_chain_button.clicked.connect(
            self.create_joints_on_edges
        )
        self.enable_scale_compensate_button.clicked.connect(
            self.enable_scale_compensate
        )
        self.disable_scale_compensate_button.clicked.connect(
            self.disable_scale_compensate
        )
        self.show_orient_button.clicked.connect(
            self.show_orient
        )
        self.hide_orient_button.clicked.connect(
            self.hide_orient
        )
        self.clear_orient_button.clicked.connect(
            self.clear_joint_orient
        )
        self.create_curve_on_joints_button.clicked.connect(
            self.create_curve_on_joints
        )
        self.batch_parent_constraint_button.clicked.connect(
            self.batch_parent_constraint
        )

        self.bind_skin_options_button.clicked.connect(
            self.open_bind_skin_options
        )
        self.detach_skin_options_button.clicked.connect(
            self.open_detach_skin_options
        )
        self.paint_skin_options_button.clicked.connect(
            self.open_paint_skin_options
        )
        self.mirror_skin_options_button.clicked.connect(
            self.open_mirror_skin_options
        )
        self.copy_skin_button.clicked.connect(
            self.copy_skin_weights
        )

    # =========================================================================
    # Maya Option Windows
    # =========================================================================

    @staticmethod
    def open_orient_options():
        mel.eval("OrientJointOptions;")

    @staticmethod
    def open_mirror_options():
        mel.eval("MirrorJointOptions;")

    @staticmethod
    def open_ik_handle_options():
        mel.eval("IKHandleToolOptions;")

    @staticmethod
    def open_ik_spline_options():
        mel.eval("IKSplineHandleToolOptions;")

    @staticmethod
    def open_bind_skin_options():
        mel.eval("SmoothBindSkinOptions;")

    @staticmethod
    def open_detach_skin_options():
        mel.eval("DetachSkinOptions;")

    @staticmethod
    def open_paint_skin_options():
        mel.eval("ArtPaintSkinWeightsToolOptions;")

    @staticmethod
    def open_mirror_skin_options():
        mel.eval("MirrorSkinWeightsOptions;")

    # =========================================================================
    # Joint Display
    # =========================================================================

    @staticmethod
    def get_selected_joints():
        """返回当前选择 Joint。"""
        joints = cmds.ls(
            selection=True,
            type="joint",
            long=True
        )

        if joints is None:
            joints = []

        if not joints:
            cmds.warning(u"请先选择一个或以上的 Joint。")

        return joints

    def set_joint_size(self, value):
        """设置全场景 Joint Radius。"""
        jointUtils.Joint.set_all_radius(
            float(value)
        )

    def show_axis_selected(self):
        self.set_axis_visibility(
            visible=True,
            hierarchy=False,
            all_joints=False
        )

    def hide_axis_selected(self):
        self.set_axis_visibility(
            visible=False,
            hierarchy=False,
            all_joints=False
        )

    def show_axis_hierarchy(self):
        self.set_axis_visibility(
            visible=True,
            hierarchy=True,
            all_joints=False
        )

    def hide_axis_hierarchy(self):
        self.set_axis_visibility(
            visible=False,
            hierarchy=True,
            all_joints=False
        )

    def show_axis_all(self):
        self.set_axis_visibility(
            visible=True,
            hierarchy=False,
            all_joints=True
        )

    def hide_axis_all(self):
        self.set_axis_visibility(
            visible=False,
            hierarchy=False,
            all_joints=True
        )

    @staticmethod
    def set_axis_visibility(visible, hierarchy, all_joints):
        """设置 Joint Local Rotation Axis 显示。"""
        if all_joints:
            jointUtils.Joint.set_all_axis_visibility(
                visible=visible
            )
            return

        jointUtils.Joint.set_selected_axis_visibility(
            visible=visible,
            include_descendents=hierarchy
        )

    # =========================================================================
    # Joint Create / Edit
    # =========================================================================

    def create_snap_joints(self):
        """在当前选择位置创建 Joint。"""
        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziCreateSnapJoints"
        )

        try:
            joints = jointUtils.Joint.create_from_selection(
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
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    def create_child_joints(self):
        """为选择 Transform / Joint 创建子 Joint。"""
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(u"请选择一个或以上的 Transform / Joint。")
            return

        created_joints = []

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziCreateChildJoints"
        )

        try:
            for selected_object in selections:
                joint = jointUtils.Joint.create_child(
                    obj=selected_object,
                    radius=self.joint_size_spinbox.value()
                )
                created_joints.append(joint)
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

        if created_joints:
            cmds.select(
                created_joints,
                replace=True
            )

    @staticmethod
    def open_resample_tool():
        """通过统一 Window Manager 打开 Joint Resample。"""
        return window_manager.show_tool(
            "joint/joint_resample",
            joint_resamp_tool.main
        )

    @staticmethod
    def parent_selected_chain():
        """按照选择顺序把 Joint 组成父子链。"""
        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziParentJointChain"
        )

        try:
            jointUtils.JointChain.parent_selected_as_chain()
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    def create_joints_on_curves(self):
        """根据选择 Curve 的 CV 创建 Joint Chain。"""
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(u"请选择一条或多条 NURBS Curve。")
            return

        created_joints = []

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziCurveJointChain"
        )

        try:
            for curve in selections:
                result = jointUtils.JointCurve.create_joints_on_curve_points(
                    curve=curve,
                    parent_chain=True,
                    create_group=True,
                    radius=self.joint_size_spinbox.value()
                )

                joints = result.get("jnt_list") or []

                for joint in joints:
                    created_joints.append(joint)
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

        if created_joints:
            cmds.select(
                created_joints,
                replace=True
            )

    def create_joints_on_edges(self):
        """把连续 Polygon Edge 转 Curve 后创建 Joint Chain。"""
        selections = cmds.ls(
            selection=True,
            flatten=True
        )

        if selections is None:
            selections = []

        valid_edges = []

        for selected_item in selections:
            if ".e[" in selected_item:
                valid_edges.append(selected_item)

        if not valid_edges:
            cmds.warning(u"请选择连续的多边形边。")
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziEdgeJointChain"
        )

        try:
            cmds.select(
                valid_edges,
                replace=True
            )

            curve_result = cmds.polyToCurve(
                form=2,
                degree=3,
                conformToSmoothMeshPreview=1,
                constructionHistory=False
            )
            curve = curve_result[0]

            result = jointUtils.JointCurve.create_joints_on_curve_points(
                curve=curve,
                parent_chain=True,
                create_group=True,
                radius=self.joint_size_spinbox.value()
            )

            joints = result.get("jnt_list") or []

            if joints:
                cmds.select(
                    joints,
                    replace=True
                )
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    def enable_scale_compensate(self):
        self.set_scale_compensate(True)

    def disable_scale_compensate(self):
        self.set_scale_compensate(False)

    def set_scale_compensate(self, enabled):
        """设置选择 Joint 的 Segment Scale Compensate。"""
        joints = self.get_selected_joints()

        if not joints:
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziScaleCompensate"
        )

        try:
            for joint in joints:
                jointUtils.Joint(joint).set_scale_compensate(
                    enabled=enabled
                )
        finally:
            cmds.undoInfo(closeChunk=True)

    def show_orient(self):
        self.set_orient_visibility(True)

    def hide_orient(self):
        self.set_orient_visibility(False)

    def set_orient_visibility(self, visible):
        """显示或隐藏 Joint Orient。"""
        joints = self.get_selected_joints()

        if not joints:
            return

        for joint in joints:
            joint_handler = jointUtils.Joint(joint)

            if visible:
                joint_handler.show_orient()
            else:
                joint_handler.hide_orient()

    def clear_joint_orient(self):
        """清空选择 Joint 的 Joint Orient。"""
        joints = self.get_selected_joints()

        if not joints:
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziClearJointOrient"
        )

        try:
            for joint in joints:
                jointUtils.Joint(joint).clear_orient()
        finally:
            cmds.undoInfo(closeChunk=True)

    def create_curve_on_joints(self):
        """按照选择 Joint 世界位置创建 Curve。"""
        joints = self.get_selected_joints()

        if len(joints) < 2:
            cmds.warning(u"至少选择两个 Joint。")
            return

        positions = []

        for joint in joints:
            position = cmds.xform(
                joint,
                query=True,
                worldSpace=True,
                translation=True
            )
            positions.append(position)

        degree = 3

        if len(positions) < 4:
            degree = 1

        curve = cmds.curve(
            name="crv_joint_chain_001",
            degree=degree,
            point=positions
        )

        cmds.select(
            curve,
            replace=True
        )

    @staticmethod
    def batch_parent_constraint():
        """按照 driver/driven 成对顺序批量创建 Parent Constraint。"""
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if len(selections) < 2 or len(selections) % 2 != 0:
            cmds.warning(
                u"请按 driver1, driven1, driver2, driven2... 的顺序选择偶数个对象。"
            )
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziBatchParentConstraint"
        )

        try:
            selection_index = 0

            while selection_index < len(selections):
                driver = selections[selection_index]
                driven = selections[selection_index + 1]

                cmds.parentConstraint(
                    driver,
                    driven,
                    maintainOffset=True
                )

                selection_index += 2
        finally:
            cmds.undoInfo(closeChunk=True)

    # =========================================================================
    # Skin
    # =========================================================================

    @staticmethod
    def copy_skin_weights():
        """把第一个选择模型 Skin Weight 复制到后续选择模型。"""
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if len(selections) < 2:
            cmds.warning(u"请先选择源模型，再选择一个或多个目标模型。")
            return

        source_mesh = selections[0]
        target_meshes = selections[1:]

        try:
            result = skin_utils.copy_skin_weights(
                source=source_mesh,
                targets=target_meshes
            )
        except Exception as error:
            cmds.warning(str(error))
            return

        if result:
            print(
                u"[Joint Tool] 已复制 Skin Weight 到 {} 个目标。".format(
                    len(result)
                )
            )


def main():
    """创建并返回 Joint Tool。"""
    window = JointTool()
    return window


__all__ = [
    "JointTool",
    "main",
]
