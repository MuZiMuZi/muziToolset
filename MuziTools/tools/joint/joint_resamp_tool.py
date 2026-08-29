# coding=utf-8
u"""
关节重采样工具
==============

功能：
    在起始关节和末端关节之间按世界空间位置均匀插入指定数量的新关节。

说明：
    - Maya 2023 优先使用 PySide2。
    - 不依赖 pymel。
    - main() 只创建并返回窗口，由 window_manager 负责显示和生命周期。
    - 当前工具只负责插入新关节，不主动删除旧的中间关节，避免误删分支骨骼。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QSpinBox
    from PySide2.QtWidgets import QVBoxLayout
except ImportError:
    from PySide6.QtWidgets import QDialog
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QSpinBox
    from PySide6.QtWidgets import QVBoxLayout


class JointResamplingDialog(QDialog):
    """关节重采样窗口。"""

    def __init__(self, parent=None):
        super(JointResamplingDialog, self).__init__(parent)

        self.setWindowTitle(u"关节重采样工具")
        self.setMinimumWidth(380)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """创建界面部件。"""

        self.start_joint_label = QLabel(u"起始关节：")
        self.start_joint_line = QLineEdit()
        self.start_joint_line.setReadOnly(True)
        self.start_joint_button = QPushButton(u"拾取")

        self.end_joint_label = QLabel(u"末端关节：")
        self.end_joint_line = QLineEdit()
        self.end_joint_line.setReadOnly(True)
        self.end_joint_button = QPushButton(u"拾取")

        self.joint_number_label = QLabel(u"插入关节数量：")
        self.joint_number_spin = QSpinBox()
        self.joint_number_spin.setMinimum(1)
        self.joint_number_spin.setMaximum(100)
        self.joint_number_spin.setValue(2)

        self.resample_button = QPushButton(u"重新采样")
        self.resample_button.setToolTip(
            u"在起始和末端关节之间均匀插入新关节"
        )

    def create_layouts(self):
        """创建界面布局。"""

        self.start_joint_layout = QHBoxLayout()
        self.start_joint_layout.addWidget(self.start_joint_label)
        self.start_joint_layout.addWidget(self.start_joint_line)
        self.start_joint_layout.addWidget(self.start_joint_button)

        self.end_joint_layout = QHBoxLayout()
        self.end_joint_layout.addWidget(self.end_joint_label)
        self.end_joint_layout.addWidget(self.end_joint_line)
        self.end_joint_layout.addWidget(self.end_joint_button)

        self.joint_number_layout = QHBoxLayout()
        self.joint_number_layout.addWidget(self.joint_number_label)
        self.joint_number_layout.addWidget(self.joint_number_spin)
        self.joint_number_layout.addStretch()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.start_joint_layout)
        self.main_layout.addLayout(self.end_joint_layout)
        self.main_layout.addLayout(self.joint_number_layout)
        self.main_layout.addWidget(self.resample_button)

    def create_connections(self):
        """连接界面事件。"""

        self.start_joint_button.clicked.connect(
            self.pick_start_joint
        )
        self.end_joint_button.clicked.connect(
            self.pick_end_joint
        )
        self.resample_button.clicked.connect(
            self.resample
        )

    def get_single_selected_joint(self):
        """读取当前唯一选择的 Joint。"""

        selected_joints = cmds.ls(
            selection=True,
            type="joint",
            long=True
        )

        if selected_joints is None:
            selected_joints = []

        if len(selected_joints) != 1:
            cmds.warning(u"请只选择一个 Joint。")
            return None

        return selected_joints[0]

    def pick_start_joint(self):
        """拾取起始关节。"""

        selected_joint = self.get_single_selected_joint()

        if selected_joint is None:
            return

        self.start_joint_line.setText(selected_joint)

    def pick_end_joint(self):
        """拾取末端关节。"""

        selected_joint = self.get_single_selected_joint()

        if selected_joint is None:
            return

        self.end_joint_line.setText(selected_joint)

    def resample(self):
        """根据界面参数执行关节插入。"""

        start_joint = self.start_joint_line.text().strip()
        end_joint = self.end_joint_line.text().strip()
        joint_number = self.joint_number_spin.value()

        if not start_joint:
            cmds.warning(u"没有指定起始关节。")
            return

        if not end_joint:
            cmds.warning(u"没有指定末端关节。")
            return

        created_joints = resample_joint(
            start_joint=start_joint,
            end_joint=end_joint,
            joint_number=joint_number
        )

        if created_joints:
            cmds.select(
                created_joints,
                replace=True
            )


def get_short_name(node):
    """获取节点短名称，用于生成新 Joint 名称。"""

    if "|" in node:
        return node.rsplit("|", 1)[-1]

    return node


def validate_joint(joint, label):
    """检查节点是否存在并且是 Joint。"""

    if not joint:
        cmds.warning(u"{}不能为空。".format(label))
        return False

    if not cmds.objExists(joint):
        cmds.warning(u"{}不存在：{}".format(label, joint))
        return False

    if cmds.nodeType(joint) != "joint":
        cmds.warning(u"{}不是 Joint：{}".format(label, joint))
        return False

    return True


def resample_joint(start_joint, end_joint, joint_number):
    """
    在两个 Joint 之间插入指定数量的新 Joint。

    新关节会依次组成：
        start_joint
            -> new_joint_001
                -> new_joint_002
                    -> end_joint

    这个函数不会删除起始和末端之间可能已经存在的其它分支节点。
    """

    if not validate_joint(start_joint, u"起始关节"):
        return []

    if not validate_joint(end_joint, u"末端关节"):
        return []

    if start_joint == end_joint:
        cmds.warning(u"起始关节和末端关节不能是同一个 Joint。")
        return []

    if joint_number < 1:
        cmds.warning(u"插入关节数量必须大于等于 1。")
        return []

    start_position = cmds.xform(
        start_joint,
        query=True,
        worldSpace=True,
        translation=True
    )
    end_position = cmds.xform(
        end_joint,
        query=True,
        worldSpace=True,
        translation=True
    )

    start_short_name = get_short_name(start_joint)
    created_joints = []
    previous_joint = start_joint

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziJointResampling"
    )

    try:
        index = 0

        while index < joint_number:
            ratio = float(index + 1) / float(joint_number + 1)
            position = []

            axis_index = 0

            while axis_index < 3:
                start_value = start_position[axis_index]
                end_value = end_position[axis_index]
                value = start_value + ((end_value - start_value) * ratio)
                position.append(value)
                axis_index += 1

            new_joint_name = "{}_resamp_{:03d}".format(
                start_short_name,
                index + 1
            )

            cmds.select(clear=True)
            new_joint = cmds.joint(
                name=new_joint_name,
                position=position
            )

            new_joint = cmds.parent(
                new_joint,
                previous_joint
            )[0]

            created_joints.append(new_joint)
            previous_joint = new_joint
            index += 1

        # 把末端 Joint 接到最后一个新 Joint 下。
        # Maya parent 默认保持当前世界空间位置，所以不会把末端吸回局部原点。
        cmds.parent(
            end_joint,
            previous_joint
        )
    except RuntimeError as error:
        cmds.warning(str(error))
        return []
    finally:
        cmds.undoInfo(closeChunk=True)

    return created_joints


def main():
    """创建关节重采样窗口并返回 QDialog。"""
    window = JointResamplingDialog()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
