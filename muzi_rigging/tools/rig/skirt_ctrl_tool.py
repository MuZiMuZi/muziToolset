# coding=utf-8
u"""
Skirt Control Tool
==================

程序化裙子 FK 绑定工具。

工作流：
    1. 设置横向数量并生成 Up / Down 两条可编辑定位曲线；
    2. 每个横向采样点通过 pointOnCurveInfo 实时驱动 Blueprint Joint；
    3. 调整定位曲线贴合裙子；
    4. 设置纵向数量并生成纵向 Bind Joint 链与 FK 控制器。

兼容 Maya 2023 / PySide2，核心逻辑只使用 maya.cmds。
"""

from __future__ import print_function

import maya.cmds as cmds

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QSpinBox
from PySide2.QtWidgets import QVBoxLayout

from ....core import qtUtils
from ..ctrl import create_ctrl_tool


_window = None


def _safe_name(text):
    result = text.strip().replace(" ", "_").replace(":", "_")
    if not result:
        result = "skirt"
    return result


def _ensure_group(name, parent=None):
    if cmds.objExists(name):
        return name

    group = cmds.createNode("transform", name=name)

    if parent is not None:
        cmds.parent(group, parent)

    return group


def _world_position(node):
    return cmds.xform(
        node,
        query=True,
        worldSpace=True,
        translation=True
    )


def _lerp(a, b, ratio):
    return [
        a[0] + (b[0] - a[0]) * ratio,
        a[1] + (b[1] - a[1]) * ratio,
        a[2] + (b[2] - a[2]) * ratio,
    ]


class SkirtControlTool(QDialog):
    """裙子程序化绑定窗口。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = qtUtils.get_maya_window()

        super(SkirtControlTool, self).__init__(parent)
        self.setWindowTitle(u"裙子控制器工具")
        self.setMinimumWidth(360)

        self.name_line = QLineEdit("skirt")

        self.horizontal_spin = QSpinBox()
        self.horizontal_spin.setRange(3, 64)
        self.horizontal_spin.setValue(8)

        self.vertical_spin = QSpinBox()
        self.vertical_spin.setRange(2, 32)
        self.vertical_spin.setValue(4)

        self.setup_btn = QPushButton(u"01 生成 / 重建定位")
        self.build_btn = QPushButton(u"02 生成绑定")
        self.select_setup_btn = QPushButton(u"选择定位曲线")

        self._create_layout()
        self._create_connections()

    def _create_layout(self):
        main_layout = QVBoxLayout(self)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel(u"裙子名称:"))
        name_layout.addWidget(self.name_line)
        main_layout.addLayout(name_layout)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(QLabel(u"横向链数量:"))
        horizontal_layout.addWidget(self.horizontal_spin)
        main_layout.addLayout(horizontal_layout)

        vertical_layout = QHBoxLayout()
        vertical_layout.addWidget(QLabel(u"每条纵向关节数量:"))
        vertical_layout.addWidget(self.vertical_spin)
        main_layout.addLayout(vertical_layout)

        main_layout.addWidget(self.setup_btn)
        main_layout.addWidget(self.select_setup_btn)
        main_layout.addWidget(self.build_btn)

    def _create_connections(self):
        self.setup_btn.clicked.connect(self.create_setup)
        self.select_setup_btn.clicked.connect(self.select_setup_curves)
        self.build_btn.clicked.connect(self.build_rig)

    def _names(self):
        name = _safe_name(self.name_line.text())

        return {
            "name": name,
            "root": "grp_m_{}_001".format(name),
            "setup": "grp_m_{}Setup_001".format(name),
            "blueprint": "grp_m_{}Bpjnts_001".format(name),
            "controls": "grp_m_{}Ctrls_001".format(name),
            "joints": "grp_m_{}Jnts_001".format(name),
            "nodes": "grp_m_{}Nodes_001".format(name),
            "build": "grp_m_{}RigBuild_001".format(name),
            "up_curve": "crv_m_{}Up_001".format(name),
            "down_curve": "crv_m_{}Down_001".format(name),
        }

    def _create_root_groups(self):
        names = self._names()
        root = _ensure_group(names["root"])
        _ensure_group(names["setup"], root)
        _ensure_group(names["blueprint"], root)
        _ensure_group(names["controls"], root)
        _ensure_group(names["joints"], root)
        _ensure_group(names["nodes"], root)
        return names

    def _delete_setup_nodes(self, names):
        delete_nodes = []

        if cmds.objExists(names["setup"]):
            children = cmds.listRelatives(
                names["setup"],
                children=True,
                fullPath=True
            ) or []
            for child in children:
                delete_nodes.append(child)

        if cmds.objExists(names["blueprint"]):
            children = cmds.listRelatives(
                names["blueprint"],
                children=True,
                fullPath=True
            ) or []
            for child in children:
                delete_nodes.append(child)

        poci_nodes = cmds.ls(
            "poci_m_{}_*".format(names["name"]),
            type="pointOnCurveInfo"
        ) or []
        for node in poci_nodes:
            delete_nodes.append(node)

        if delete_nodes:
            cmds.delete(delete_nodes)

    def _create_setup_curve(self, name, y_value, radius, parent):
        curve = cmds.circle(
            name=name,
            center=(0.0, y_value, 0.0),
            normal=(0.0, 1.0, 0.0),
            radius=radius,
            degree=3,
            sections=max(self.horizontal_spin.value(), 4),
            constructionHistory=False
        )[0]
        cmds.parent(curve, parent)
        return curve

    def _create_curve_blueprints(self, curve, place, names):
        curve_shapes = cmds.listRelatives(
            curve,
            shapes=True,
            noIntermediate=True,
            fullPath=True,
            type="nurbsCurve"
        ) or []

        if not curve_shapes:
            raise RuntimeError(u"定位曲线没有 nurbsCurve Shape：{}".format(curve))

        curve_shape = curve_shapes[0]
        horizontal_count = self.horizontal_spin.value()

        for index in range(horizontal_count):
            point_group = cmds.createNode(
                "transform",
                name="grp_m_{}{}Point_{:03d}".format(
                    names["name"],
                    place,
                    index + 1
                ),
                parent=names["blueprint"]
            )

            poci = cmds.createNode(
                "pointOnCurveInfo",
                name="poci_m_{}{}_{:03d}".format(
                    names["name"],
                    place,
                    index + 1
                )
            )

            cmds.connectAttr(
                curve_shape + ".worldSpace[0]",
                poci + ".inputCurve",
                force=True
            )
            cmds.setAttr(poci + ".turnOnPercentage", 1)
            cmds.setAttr(
                poci + ".parameter",
                float(index) / float(horizontal_count)
            )
            cmds.connectAttr(
                poci + ".position",
                point_group + ".translate",
                force=True
            )

            joint = cmds.createNode(
                "joint",
                name="bpjnt_m_{}{}_hor{:03d}_001".format(
                    names["name"],
                    place,
                    index + 1
                ),
                parent=point_group
            )
            cmds.setAttr(joint + ".radius", 0.25)

    def create_setup(self):
        cmds.undoInfo(openChunk=True, chunkName="MuziSkirtSetup")
        try:
            names = self._create_root_groups()
            self._delete_setup_nodes(names)

            up_curve = self._create_setup_curve(
                names["up_curve"],
                y_value=5.0,
                radius=2.0,
                parent=names["setup"]
            )
            down_curve = self._create_setup_curve(
                names["down_curve"],
                y_value=0.0,
                radius=3.0,
                parent=names["setup"]
            )

            self._create_curve_blueprints(
                up_curve,
                "Up",
                names
            )
            self._create_curve_blueprints(
                down_curve,
                "Down",
                names
            )

            cmds.select([up_curve, down_curve], replace=True)
            print(
                u"[Skirt Tool] 已生成 {} 条纵向定位列。".format(
                    self.horizontal_spin.value()
                )
            )
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    def select_setup_curves(self):
        names = self._names()
        curves = []

        for key in ("up_curve", "down_curve"):
            curve = names[key]
            if cmds.objExists(curve):
                curves.append(curve)

        if not curves:
            cmds.warning(u"尚未生成定位曲线。")
            return

        cmds.select(curves, replace=True)

    def _delete_previous_build(self, names):
        if cmds.objExists(names["build"]):
            cmds.delete(names["build"])

        for group_key in ("controls", "joints"):
            group = names[group_key]
            if not cmds.objExists(group):
                continue

            children = cmds.listRelatives(
                group,
                children=True,
                fullPath=True
            ) or []

            if children:
                cmds.delete(children)

    def build_rig(self):
        names = self._create_root_groups()
        horizontal_count = self.horizontal_spin.value()
        vertical_count = self.vertical_spin.value()

        missing = []
        for index in range(horizontal_count):
            up_joint = "bpjnt_m_{}Up_hor{:03d}_001".format(
                names["name"],
                index + 1
            )
            down_joint = "bpjnt_m_{}Down_hor{:03d}_001".format(
                names["name"],
                index + 1
            )

            if not cmds.objExists(up_joint):
                missing.append(up_joint)
            if not cmds.objExists(down_joint):
                missing.append(down_joint)

        if missing:
            cmds.warning(u"定位数据不完整，请先点击“生成 / 重建定位”。")
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziBuildSkirtRig")
        try:
            self._delete_previous_build(names)
            build_group = cmds.createNode(
                "transform",
                name=names["build"],
                parent=names["root"]
            )

            created_controls = []

            for horizontal_index in range(horizontal_count):
                up_joint = "bpjnt_m_{}Up_hor{:03d}_001".format(
                    names["name"],
                    horizontal_index + 1
                )
                down_joint = "bpjnt_m_{}Down_hor{:03d}_001".format(
                    names["name"],
                    horizontal_index + 1
                )

                up_position = _world_position(up_joint)
                down_position = _world_position(down_joint)

                previous_joint = None
                previous_control = None

                for vertical_index in range(vertical_count):
                    if vertical_count == 1:
                        ratio = 0.0
                    else:
                        ratio = float(vertical_index) / float(vertical_count - 1)

                    position = _lerp(
                        up_position,
                        down_position,
                        ratio
                    )

                    joint_name = "jnt_m_{}_hor{:03d}_ver{:03d}".format(
                        names["name"],
                        horizontal_index + 1,
                        vertical_index + 1
                    )
                    joint = cmds.createNode(
                        "joint",
                        name=joint_name
                    )
                    cmds.xform(
                        joint,
                        worldSpace=True,
                        translation=position
                    )

                    if previous_joint is None:
                        cmds.parent(joint, names["joints"])
                    else:
                        cmds.parent(joint, previous_joint)

                    ctrl_name = "ctrl_m_{}_hor{:03d}_ver{:03d}".format(
                        names["name"],
                        horizontal_index + 1,
                        vertical_index + 1
                    )

                    parent_control = previous_control
                    if previous_control is None:
                        parent_control = names["controls"]

                    control_result = create_ctrl_tool.create_controller(
                        name=ctrl_name,
                        shape="circle",
                        radius=0.6,
                        axis="Y+",
                        target=joint,
                        parent=parent_control,
                        color=17,
                        create_sub_control=False,
                        create_extra_groups=True,
                        add_to_set=True
                    )
                    control = control_result["control"]

                    cmds.parentConstraint(
                        control,
                        joint,
                        maintainOffset=False
                    )

                    created_controls.append(control)
                    previous_joint = joint
                    previous_control = control

            cmds.addAttr(
                build_group,
                longName="horizontalCount",
                attributeType="long",
                defaultValue=horizontal_count
            )
            cmds.addAttr(
                build_group,
                longName="verticalCount",
                attributeType="long",
                defaultValue=vertical_count
            )

            if created_controls:
                cmds.select(created_controls, replace=True)

            print(
                u"[Skirt Tool] Build 完成：{} x {}。".format(
                    horizontal_count,
                    vertical_count
                )
            )
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)


def main():
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = SkirtControlTool()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window
