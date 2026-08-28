# coding=utf-8
u"""
关节重采样工具

兼容 Maya 2023 / PySide2。
"""

from __future__ import print_function

import maya.cmds as cmds

from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QSpinBox
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QVBoxLayout

from ....core import qtUtils


_window = None


class JointResamplingDialog(QDialog):

    def __init__(self, parent=None):

        if parent is None:
            parent = qtUtils.get_maya_window()

        super(JointResamplingDialog, self).__init__(parent)

        self.setWindowTitle("关节重采样工具")
        self.setMinimumWidth(360)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        self.start_label = QLabel("起始关节:")
        self.start_line = QLineEdit()
        self.start_line.setReadOnly(True)
        self.start_pick_btn = QPushButton("拾取")

        self.end_label = QLabel("末端关节:")
        self.end_line = QLineEdit()
        self.end_line.setReadOnly(True)
        self.end_pick_btn = QPushButton("拾取")

        self.joint_number_label = QLabel("中间关节数量:")
        self.joint_number_spin = QSpinBox()
        self.joint_number_spin.setMinimum(1)
        self.joint_number_spin.setMaximum(100)
        self.joint_number_spin.setValue(2)

        self.resample_btn = QPushButton("重新采样")

    def create_layouts(self):

        start_layout = QHBoxLayout()
        start_layout.addWidget(self.start_label)
        start_layout.addWidget(self.start_line)
        start_layout.addWidget(self.start_pick_btn)

        end_layout = QHBoxLayout()
        end_layout.addWidget(self.end_label)
        end_layout.addWidget(self.end_line)
        end_layout.addWidget(self.end_pick_btn)

        number_layout = QHBoxLayout()
        number_layout.addWidget(self.joint_number_label)
        number_layout.addWidget(self.joint_number_spin)
        number_layout.addStretch()

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(start_layout)
        main_layout.addLayout(end_layout)
        main_layout.addLayout(number_layout)
        main_layout.addWidget(self.resample_btn)

    def create_connections(self):

        self.start_pick_btn.clicked.connect(
            self.pick_start_joint
        )

        self.end_pick_btn.clicked.connect(
            self.pick_end_joint
        )

        self.resample_btn.clicked.connect(
            self.resample
        )

    def pick_start_joint(self):

        joints = cmds.ls(
            selection=True,
            type="joint",
        )

        if len(joints) != 1:
            cmds.warning(
                "请只选择一个关节作为起始关节。"
            )
            return

        self.start_line.setText(joints[0])

    def pick_end_joint(self):

        joints = cmds.ls(
            selection=True,
            type="joint",
        )

        if len(joints) != 1:
            cmds.warning(
                "请只选择一个关节作为末端关节。"
            )
            return

        self.end_line.setText(joints[0])

    def resample(self):

        start_joint = self.start_line.text()
        end_joint = self.end_line.text()
        joint_number = self.joint_number_spin.value()

        if not start_joint:
            cmds.warning("没有指定起始关节。")
            return

        if not end_joint:
            cmds.warning("没有指定末端关节。")
            return

        if not cmds.objExists(start_joint):
            cmds.warning(
                "起始关节不存在: {}".format(
                    start_joint
                )
            )
            return

        if not cmds.objExists(end_joint):
            cmds.warning(
                "末端关节不存在: {}".format(
                    end_joint
                )
            )
            return

        resample_joint(
            start_joint,
            end_joint,
            joint_number,
        )


def resample_joint(start_joint, end_joint, joint_number):

    if joint_number < 1:
        cmds.warning(
            "关节数量必须大于等于 1。"
        )
        return []

    start_position = cmds.xform(
        start_joint,
        query=True,
        worldSpace=True,
        translation=True,
    )

    end_position = cmds.xform(
        end_joint,
        query=True,
        worldSpace=True,
        translation=True,
    )

    created_joints = []
    previous_joint = start_joint

    for index in range(joint_number):

        ratio = float(index + 1) / float(joint_number + 1)

        position = []

        for axis_index in range(3):

            value = (
                start_position[axis_index]
                + (
                    end_position[axis_index]
                    - start_position[axis_index]
                )
                * ratio
            )

            position.append(value)

        cmds.select(clear=True)

        new_joint = cmds.joint(
            name="{}_resamp_{:03d}".format(
                start_joint,
                index + 1,
            ),
            position=position,
        )

        cmds.parent(
            new_joint,
            previous_joint,
        )

        created_joints.append(new_joint)
        previous_joint = new_joint

    cmds.parent(
        end_joint,
        previous_joint,
    )

    return created_joints


def main():
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = JointResamplingDialog()
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window
