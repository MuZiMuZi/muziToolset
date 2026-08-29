# coding=utf-8
u"""
Joint Tool
==========

Maya 2023 / PySide2 关节工具面板。

设计原则：
    1. UI 只负责交互，不再依赖旧的 ``Joint_Tool_main.py``。
    2. 关节基础能力统一调用 ``core.jointUtils`` 当前 API。
    3. 不引入 PyMel，避免 UI 因可选依赖缺失而无法启动。
    4. 关节重采样由 ``joint_resamp_tool`` 独立负责。
"""

from __future__ import print_function

import maya.cmds as cmds
import maya.mel as mel

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDoubleSpinBox
from PySide2.QtWidgets import QGridLayout
from PySide2.QtWidgets import QGroupBox
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QScrollArea
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget

from ....core import jointUtils
from ....core import qtUtils
from . import joint_resamp_tool


_window = None


class JointTool(QWidget):
    """木子工具集中的关节工具面板。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = qtUtils.get_maya_window()

        super(JointTool, self).__init__(parent)

        self.setWindowTitle(u"Joint Tool")
        self.setMinimumWidth(420)
        self.resize(460, 720)

        self._create_widgets()
        self._create_layouts()
        self._create_connections()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _create_widgets(self):
        self.joint_size_spin = QDoubleSpinBox()
        self.joint_size_spin.setDecimals(2)
        self.joint_size_spin.setRange(0.01, 100.0)
        self.joint_size_spin.setSingleStep(0.1)
        self.joint_size_spin.setValue(0.5)
        self.joint_size_spin.setToolTip(u"设置场景中所有关节的 radius。")

        self.show_axis_selected_btn = QPushButton(u"显示轴向 - 选择")
        self.hide_axis_selected_btn = QPushButton(u"隐藏轴向 - 选择")
        self.show_axis_hierarchy_btn = QPushButton(u"显示轴向 - 层级")
        self.hide_axis_hierarchy_btn = QPushButton(u"隐藏轴向 - 层级")
        self.show_axis_all_btn = QPushButton(u"显示轴向 - 全部")
        self.hide_axis_all_btn = QPushButton(u"隐藏轴向 - 全部")

        self.orient_options_btn = QPushButton(u"关节定向选项")
        self.mirror_options_btn = QPushButton(u"镜像关节选项")
        self.ik_handle_options_btn = QPushButton(u"IK Handle 选项")
        self.ik_spline_options_btn = QPushButton(u"IK Spline 选项")

        self.bind_skin_options_btn = QPushButton(u"绑定蒙皮选项")
        self.detach_skin_options_btn = QPushButton(u"解绑蒙皮选项")
        self.paint_skin_options_btn = QPushButton(u"绘制权重选项")
        self.mirror_skin_options_btn = QPushButton(u"镜像权重选项")
        self.copy_skin_btn = QPushButton(u"复制蒙皮权重")
        self.copy_skin_btn.setToolTip(
            u"先选择源模型，再选择一个或多个目标模型。"
        )

        self.create_snap_joint_btn = QPushButton(u"按选择创建关节")
        self.create_snap_joint_btn.setToolTip(
            u"在当前选择的物体或组件位置创建关节。"
        )

        self.create_child_joint_btn = QPushButton(u"创建子关节")
        self.create_child_joint_btn.setToolTip(
            u"在每个选中 Transform / Joint 下创建一个子关节。"
        )

        self.resample_joint_btn = QPushButton(u"关节链重采样")
        self.parent_chain_btn = QPushButton(u"按选择顺序组成关节链")
        self.curve_chain_btn = QPushButton(u"曲线 CV 创建关节链")
        self.edge_chain_btn = QPushButton(u"多边形边创建关节链")

        self.enable_scale_comp_btn = QPushButton(u"开启分段比例补偿")
        self.disable_scale_comp_btn = QPushButton(u"关闭分段比例补偿")

        self.show_orient_btn = QPushButton(u"显示 Joint Orient")
        self.hide_orient_btn = QPushButton(u"隐藏 Joint Orient")
        self.clear_orient_btn = QPushButton(u"归零 Joint Orient")

        self.create_curve_on_joints_btn = QPushButton(u"关节链创建曲线")
        self.batch_parent_constraint_btn = QPushButton(u"按顺序批量父子约束")
        self.batch_parent_constraint_btn.setToolTip(
            u"按 driver1, driven1, driver2, driven2... 的选择顺序创建父子约束。"
        )

    def _create_layouts(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(6, 6, 6, 6)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        display_group = QGroupBox(u"关节显示")
        display_layout = QGridLayout(display_group)
        display_layout.addWidget(self.joint_size_spin, 0, 0, 1, 2)
        display_layout.addWidget(self.show_axis_selected_btn, 1, 0)
        display_layout.addWidget(self.hide_axis_selected_btn, 1, 1)
        display_layout.addWidget(self.show_axis_hierarchy_btn, 2, 0)
        display_layout.addWidget(self.hide_axis_hierarchy_btn, 2, 1)
        display_layout.addWidget(self.show_axis_all_btn, 3, 0)
        display_layout.addWidget(self.hide_axis_all_btn, 3, 1)

        maya_group = QGroupBox(u"Maya 关节 / IK")
        maya_layout = QGridLayout(maya_group)
        maya_layout.addWidget(self.orient_options_btn, 0, 0)
        maya_layout.addWidget(self.mirror_options_btn, 0, 1)
        maya_layout.addWidget(self.ik_handle_options_btn, 1, 0)
        maya_layout.addWidget(self.ik_spline_options_btn, 1, 1)

        create_group = QGroupBox(u"关节创建与编辑")
        create_layout = QGridLayout(create_group)
        create_layout.addWidget(self.create_snap_joint_btn, 0, 0)
        create_layout.addWidget(self.create_child_joint_btn, 0, 1)
        create_layout.addWidget(self.resample_joint_btn, 1, 0)
        create_layout.addWidget(self.parent_chain_btn, 1, 1)
        create_layout.addWidget(self.curve_chain_btn, 2, 0)
        create_layout.addWidget(self.edge_chain_btn, 2, 1)
        create_layout.addWidget(self.enable_scale_comp_btn, 3, 0)
        create_layout.addWidget(self.disable_scale_comp_btn, 3, 1)
        create_layout.addWidget(self.show_orient_btn, 4, 0)
        create_layout.addWidget(self.hide_orient_btn, 4, 1)
        create_layout.addWidget(self.clear_orient_btn, 5, 0)
        create_layout.addWidget(self.create_curve_on_joints_btn, 5, 1)
        create_layout.addWidget(self.batch_parent_constraint_btn, 6, 0, 1, 2)

        skin_group = QGroupBox(u"蒙皮")
        skin_layout = QGridLayout(skin_group)
        skin_layout.addWidget(self.bind_skin_options_btn, 0, 0)
        skin_layout.addWidget(self.detach_skin_options_btn, 0, 1)
        skin_layout.addWidget(self.paint_skin_options_btn, 1, 0)
        skin_layout.addWidget(self.mirror_skin_options_btn, 1, 1)
        skin_layout.addWidget(self.copy_skin_btn, 2, 0, 1, 2)

        scroll_layout.addWidget(display_group)
        scroll_layout.addWidget(maya_group)
        scroll_layout.addWidget(create_group)
        scroll_layout.addWidget(skin_group)
        scroll_layout.addStretch(1)

        scroll_area.setWidget(scroll_widget)
        root_layout.addWidget(scroll_area)

    def _create_connections(self):
        self.joint_size_spin.valueChanged.connect(self.set_joint_size)

        self.show_axis_selected_btn.clicked.connect(
            lambda: self.set_axis_visibility(True, False, False)
        )
        self.hide_axis_selected_btn.clicked.connect(
            lambda: self.set_axis_visibility(False, False, False)
        )
        self.show_axis_hierarchy_btn.clicked.connect(
            lambda: self.set_axis_visibility(True, True, False)
        )
        self.hide_axis_hierarchy_btn.clicked.connect(
            lambda: self.set_axis_visibility(False, True, False)
        )
        self.show_axis_all_btn.clicked.connect(
            lambda: self.set_axis_visibility(True, False, True)
        )
        self.hide_axis_all_btn.clicked.connect(
            lambda: self.set_axis_visibility(False, False, True)
        )

        self.orient_options_btn.clicked.connect(
            lambda: mel.eval("OrientJointOptions;")
        )
        self.mirror_options_btn.clicked.connect(
            lambda: mel.eval("MirrorJointOptions;")
        )
        self.ik_handle_options_btn.clicked.connect(
            lambda: mel.eval("IKHandleToolOptions;")
        )
        self.ik_spline_options_btn.clicked.connect(
            lambda: mel.eval("IKSplineHandleToolOptions;")
        )

        self.bind_skin_options_btn.clicked.connect(
            lambda: mel.eval("SmoothBindSkinOptions;")
        )
        self.detach_skin_options_btn.clicked.connect(
            lambda: mel.eval("DetachSkinOptions;")
        )
        self.paint_skin_options_btn.clicked.connect(
            lambda: mel.eval("ArtPaintSkinWeightsToolOptions;")
        )
        self.mirror_skin_options_btn.clicked.connect(
            lambda: mel.eval("MirrorSkinWeightsOptions;")
        )
        self.copy_skin_btn.clicked.connect(self.copy_skin_weights)

        self.create_snap_joint_btn.clicked.connect(self.create_snap_joints)
        self.create_child_joint_btn.clicked.connect(self.create_child_joints)
        self.resample_joint_btn.clicked.connect(joint_resamp_tool.main)
        self.parent_chain_btn.clicked.connect(self.parent_selected_chain)
        self.curve_chain_btn.clicked.connect(self.create_joints_on_curves)
        self.edge_chain_btn.clicked.connect(self.create_joints_on_edges)
        self.enable_scale_comp_btn.clicked.connect(
            lambda: self.set_scale_compensate(True)
        )
        self.disable_scale_comp_btn.clicked.connect(
            lambda: self.set_scale_compensate(False)
        )
        self.show_orient_btn.clicked.connect(
            lambda: self.set_orient_visibility(True)
        )
        self.hide_orient_btn.clicked.connect(
            lambda: self.set_orient_visibility(False)
        )
        self.clear_orient_btn.clicked.connect(self.clear_joint_orient)
        self.create_curve_on_joints_btn.clicked.connect(
            self.create_curve_on_joints
        )
        self.batch_parent_constraint_btn.clicked.connect(
            self.batch_parent_constraint
        )

    # ------------------------------------------------------------------
    # Joint
    # ------------------------------------------------------------------

    @staticmethod
    def _selected_joints():
        joints = cmds.ls(selection=True, type="joint", long=True)
        if not joints:
            cmds.warning(u"请先选择一个或以上的 Joint。")
            return []
        return joints

    def set_joint_size(self, value):
        jointUtils.Joint.set_all_radius(float(value))

    def set_axis_visibility(self, visible, hierarchy, all_joints):
        if all_joints:
            jointUtils.Joint.set_all_axis_visibility(visible=visible)
            return

        jointUtils.Joint.set_selected_axis_visibility(
            visible=visible,
            include_descendents=hierarchy
        )

    def create_snap_joints(self):
        cmds.undoInfo(openChunk=True, chunkName="MuziCreateSnapJoints")
        try:
            joints = jointUtils.Joint.create_from_selection(
                name_prefix="jnt_snap",
                parent_chain=False,
                radius=self.joint_size_spin.value()
            )
            if joints:
                cmds.select(joints, replace=True)
        finally:
            cmds.undoInfo(closeChunk=True)

    def create_child_joints(self):
        selections = cmds.ls(selection=True, long=True)
        if not selections:
            cmds.warning(u"请选择一个或以上的 Transform / Joint。")
            return

        created_joints = []
        cmds.undoInfo(openChunk=True, chunkName="MuziCreateChildJoints")
        try:
            for obj in selections:
                joint = jointUtils.Joint.create_child(
                    obj=obj,
                    radius=self.joint_size_spin.value()
                )
                created_joints.append(joint)
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

        if created_joints:
            cmds.select(created_joints, replace=True)

    def parent_selected_chain(self):
        cmds.undoInfo(openChunk=True, chunkName="MuziParentJointChain")
        try:
            jointUtils.JointChain.parent_selected_as_chain()
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    def create_joints_on_curves(self):
        selections = cmds.ls(selection=True, long=True)
        if not selections:
            cmds.warning(u"请选择一条或多条 NURBS Curve。")
            return

        created_joints = []
        cmds.undoInfo(openChunk=True, chunkName="MuziCurveJointChain")
        try:
            for curve in selections:
                result = jointUtils.JointCurve.create_joints_on_curve_points(
                    curve=curve,
                    parent_chain=True,
                    create_group=True,
                    radius=self.joint_size_spin.value()
                )
                joints = result.get("jnt_list") or []
                for joint in joints:
                    created_joints.append(joint)
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

        if created_joints:
            cmds.select(created_joints, replace=True)

    def create_joints_on_edges(self):
        edges = cmds.ls(selection=True, flatten=True)
        if not edges:
            cmds.warning(u"请选择连续的多边形边。")
            return

        valid_edges = []
        for item in edges:
            if ".e[" in item:
                valid_edges.append(item)

        if not valid_edges:
            cmds.warning(u"当前选择中没有多边形边。")
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziEdgeJointChain")
        try:
            cmds.select(valid_edges, replace=True)
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
                radius=self.joint_size_spin.value()
            )
            joints = result.get("jnt_list") or []
            if joints:
                cmds.select(joints, replace=True)
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    def set_scale_compensate(self, enabled):
        joints = self._selected_joints()
        if not joints:
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziScaleCompensate")
        try:
            for joint in joints:
                jointUtils.Joint(joint).set_scale_compensate(enabled=enabled)
        finally:
            cmds.undoInfo(closeChunk=True)

    def set_orient_visibility(self, visible):
        joints = self._selected_joints()
        if not joints:
            return

        for joint in joints:
            joint_utils = jointUtils.Joint(joint)
            if visible:
                joint_utils.show_orient()
            else:
                joint_utils.hide_orient()

    def clear_joint_orient(self):
        joints = self._selected_joints()
        if not joints:
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziClearJointOrient")
        try:
            for joint in joints:
                jointUtils.Joint(joint).clear_orient()
        finally:
            cmds.undoInfo(closeChunk=True)

    def create_curve_on_joints(self):
        joints = self._selected_joints()
        if not joints:
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

        if len(positions) < 2:
            cmds.warning(u"至少选择两个关节。")
            return

        degree = 3
        if len(positions) < 4:
            degree = 1

        curve = cmds.curve(
            name="crv_jointChain_001",
            degree=degree,
            point=positions
        )
        cmds.select(curve, replace=True)

    def batch_parent_constraint(self):
        selections = cmds.ls(selection=True, long=True)
        if len(selections) < 2 or len(selections) % 2 != 0:
            cmds.warning(
                u"请按 driver1, driven1, driver2, driven2... 的顺序选择偶数个对象。"
            )
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziBatchParentConstraint")
        try:
            index = 0
            while index < len(selections):
                driver = selections[index]
                driven = selections[index + 1]
                cmds.parentConstraint(
                    driver,
                    driven,
                    maintainOffset=True
                )
                index += 2
        finally:
            cmds.undoInfo(closeChunk=True)

    # ------------------------------------------------------------------
    # Skin
    # ------------------------------------------------------------------

    @staticmethod
    def copy_skin_weights():
        selections = cmds.ls(selection=True, long=True)
        if len(selections) < 2:
            cmds.warning(u"请先选择源模型，再选择一个或多个目标模型。")
            return

        source_mesh = selections[0]
        target_meshes = selections[1:]
        source_skin = mel.eval(
            'findRelatedSkinCluster("{}")'.format(source_mesh)
        )

        if not source_skin:
            cmds.warning(u"源模型没有 SkinCluster：{}".format(source_mesh))
            return

        influences = cmds.skinCluster(
            source_skin,
            query=True,
            influence=True
        ) or []

        if not influences:
            cmds.warning(u"源 SkinCluster 没有影响关节。")
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziCopySkinWeights")
        try:
            for target_mesh in target_meshes:
                target_skin = mel.eval(
                    'findRelatedSkinCluster("{}")'.format(target_mesh)
                )

                if target_skin:
                    cmds.delete(target_skin)

                target_skin = cmds.skinCluster(
                    influences,
                    target_mesh,
                    toSelectedBones=True,
                    normalizeWeights=1
                )[0]

                cmds.copySkinWeights(
                    sourceSkin=source_skin,
                    destinationSkin=target_skin,
                    noMirror=True,
                    surfaceAssociation="closestPoint",
                    influenceAssociation=["label", "oneToOne", "closestJoint"]
                )
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)


def main():
    """显示关节工具窗口。"""
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = JointTool()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window
