# coding=utf-8
u"""
关节重采样工具
==============

功能：
    在一对直接父子 Joint 之间均匀插入指定数量的新关节。

安全规则：
    - end_joint 必须是 start_joint 的直接子 Joint；
    - 不会跨越已有中间关节重建层级；
    - 创建失败时会尽量删除本次新建节点并恢复原父子关系。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QSpinBox
    from PySide2.QtWidgets import QVBoxLayout
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QDialog
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QSpinBox
    from PySide6.QtWidgets import QVBoxLayout

from ... import ui_theme


class JointResamplingDialog(QDialog):
    """关节重采样窗口。"""

    def __init__(self, parent=None):
        super(JointResamplingDialog, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        ui_theme.style_window(
            self,
            title=u"关节重采样",
            minimum_width=500
        )
        self.resize(520, 340)

    # -------------------------------------------------------------------------
    # UI
    # -------------------------------------------------------------------------

    def create_widgets(self):
        """创建界面部件。"""
        self.title_label = ui_theme.make_title(u"关节重采样")
        self.subtitle_label = ui_theme.make_subtitle(
            u"在一对直接父子 Joint 之间均匀插入新的中间关节。"
        )

        self.start_joint_label = QLabel(u"起始 Joint")
        self.start_joint_line = QLineEdit()
        self.start_joint_line.setReadOnly(True)
        self.start_joint_line.setPlaceholderText(u"选择父 Joint 后点击拾取")
        self.start_joint_button = QPushButton(u"拾取")

        self.end_joint_label = QLabel(u"末端 Joint")
        self.end_joint_line = QLineEdit()
        self.end_joint_line.setReadOnly(True)
        self.end_joint_line.setPlaceholderText(u"选择直接子 Joint 后点击拾取")
        self.end_joint_button = QPushButton(u"拾取")

        self.joint_number_label = QLabel(u"插入数量")
        self.joint_number_spin = QSpinBox()
        self.joint_number_spin.setMinimum(1)
        self.joint_number_spin.setMaximum(100)
        self.joint_number_spin.setValue(2)

        self.safety_label = QLabel(
            u"安全模式：只处理直接父子 Joint，不会跨越已有中间骨骼。"
        )
        self.safety_label.setWordWrap(True)
        ui_theme.set_role(self.safety_label, "muted")

        self.resample_button = QPushButton(u"插入关节")
        self.resample_button.setToolTip(
            u"在起始和末端 Joint 之间均匀插入新关节"
        )
        ui_theme.style_primary(self.resample_button)

    def create_layouts(self):
        """创建 Silicon Card 布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        joint_card, joint_card_layout = ui_theme.make_card(self)
        joint_card_layout.addWidget(
            ui_theme.make_section_title(u"关节范围")
        )

        start_layout = QHBoxLayout()
        start_layout.setContentsMargins(0, 0, 0, 0)
        start_layout.addWidget(self.start_joint_label)
        start_layout.addWidget(self.start_joint_line, 1)
        start_layout.addWidget(self.start_joint_button)
        joint_card_layout.addLayout(start_layout)

        end_layout = QHBoxLayout()
        end_layout.setContentsMargins(0, 0, 0, 0)
        end_layout.addWidget(self.end_joint_label)
        end_layout.addWidget(self.end_joint_line, 1)
        end_layout.addWidget(self.end_joint_button)
        joint_card_layout.addLayout(end_layout)

        parameter_card, parameter_layout = ui_theme.make_card(self)
        parameter_layout.addWidget(
            ui_theme.make_section_title(u"重采样参数")
        )

        number_layout = QHBoxLayout()
        number_layout.setContentsMargins(0, 0, 0, 0)
        number_layout.addWidget(self.joint_number_label)
        number_layout.addWidget(self.joint_number_spin)
        number_layout.addStretch(1)
        parameter_layout.addLayout(number_layout)
        parameter_layout.addWidget(self.safety_label)

        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.addStretch(1)
        action_layout.addWidget(self.resample_button)

        main_layout.addWidget(joint_card)
        main_layout.addWidget(parameter_card)
        main_layout.addLayout(action_layout)
        main_layout.addStretch(1)

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

    # -------------------------------------------------------------------------
    # 选择
    # -------------------------------------------------------------------------

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
        """拾取起始 Joint。"""
        selected_joint = self.get_single_selected_joint()

        if selected_joint is None:
            return

        self.start_joint_line.setText(selected_joint)

    def pick_end_joint(self):
        """拾取末端 Joint。"""
        selected_joint = self.get_single_selected_joint()

        if selected_joint is None:
            return

        self.end_joint_line.setText(selected_joint)

    # -------------------------------------------------------------------------
    # 执行
    # -------------------------------------------------------------------------

    def resample(self):
        """根据界面参数插入关节。"""
        start_joint = self.start_joint_line.text().strip()
        end_joint = self.end_joint_line.text().strip()
        joint_number = self.joint_number_spin.value()

        if not start_joint:
            cmds.warning(u"没有指定起始 Joint。")
            return

        if not end_joint:
            cmds.warning(u"没有指定末端 Joint。")
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
    """获取节点短名称。"""
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


def is_direct_child_joint(start_joint, end_joint):
    """检查 end_joint 是否是 start_joint 的直接子 Joint。"""
    parent_nodes = cmds.listRelatives(
        end_joint,
        parent=True,
        fullPath=True
    )

    if parent_nodes is None:
        parent_nodes = []

    if not parent_nodes:
        return False

    start_long_name = cmds.ls(
        start_joint,
        long=True
    )

    if not start_long_name:
        return False

    return parent_nodes[0] == start_long_name[0]


def get_interpolated_position(start_position, end_position, ratio):
    """计算两个三维位置之间的插值位置。"""
    position = []
    axis_index = 0

    while axis_index < 3:
        start_value = start_position[axis_index]
        end_value = end_position[axis_index]
        value = start_value + ((end_value - start_value) * ratio)
        position.append(value)
        axis_index += 1

    return position


def resample_joint(start_joint, end_joint, joint_number):
    """
    在直接父子 Joint 之间插入指定数量的新 Joint。

    Result::

        start_joint
            -> new_joint_001
                -> new_joint_002
                    -> end_joint
    """
    if not validate_joint(start_joint, u"起始 Joint"):
        return []

    if not validate_joint(end_joint, u"末端 Joint"):
        return []

    if start_joint == end_joint:
        cmds.warning(u"起始 Joint 和末端 Joint 不能相同。")
        return []

    if joint_number < 1:
        cmds.warning(u"插入关节数量必须大于等于 1。")
        return []

    if not is_direct_child_joint(start_joint, end_joint):
        cmds.warning(
            u"安全模式只允许直接父子 Joint。"
            u"当前末端 Joint 不是起始 Joint 的直接子级。"
        )
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
    success = False

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziJointResampling"
    )

    try:
        # 先把末端 Joint 临时放到世界层级，保持世界空间位置不变。
        cmds.parent(
            end_joint,
            world=True
        )

        index = 0

        while index < joint_number:
            ratio = float(index + 1) / float(joint_number + 1)
            position = get_interpolated_position(
                start_position,
                end_position,
                ratio
            )

            new_joint_name = "{}_resamp_{:03d}".format(
                start_short_name,
                index + 1
            )

            cmds.select(clear=True)
            new_joint = cmds.joint(
                name=new_joint_name,
                position=position
            )

            parent_result = cmds.parent(
                new_joint,
                previous_joint
            )
            new_joint = parent_result[0]

            created_joints.append(new_joint)
            previous_joint = new_joint
            index += 1

        cmds.parent(
            end_joint,
            previous_joint
        )
        success = True

    except RuntimeError as error:
        cmds.warning(str(error))

    finally:
        if not success:
            # 删除本次已创建节点。
            delete_joints = []

            for created_joint in created_joints:
                if cmds.objExists(created_joint):
                    delete_joints.append(created_joint)

            if delete_joints:
                try:
                    cmds.delete(delete_joints)
                except Exception:
                    pass

            # 尽量恢复原始父子关系。
            if cmds.objExists(end_joint) and cmds.objExists(start_joint):
                try:
                    current_parent = cmds.listRelatives(
                        end_joint,
                        parent=True,
                        fullPath=True
                    )

                    if not current_parent:
                        cmds.parent(
                            end_joint,
                            start_joint
                        )
                except Exception:
                    pass

        cmds.undoInfo(closeChunk=True)

    if not success:
        return []

    return created_joints


def main():
    """创建关节重采样窗口。"""
    window = JointResamplingDialog()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
