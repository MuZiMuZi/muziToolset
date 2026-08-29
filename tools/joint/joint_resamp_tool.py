# coding=utf-8
u"""
Joint Resample Tool
===================

在一对直接父子 Joint 之间均匀插入指定数量的新 Joint。

模块职责
--------
1. 提供 Start Joint / End Joint Picker 和插入数量参数；
2. 校验只处理直接父子 Joint；
3. 在两端世界位置之间做线性插值并插入新 Joint；
4. 创建失败时清理本轮新节点并尽量恢复原父子关系；
5. 提供可在 Maya Script Editor 中直接显示的 ``main()``。

主要公开方法
------------
validate_joint(joint, label)
    校验输入节点存在且为 Joint。

is_direct_child_joint(start_joint, end_joint)
    判断 End 是否为 Start 的直接 Child Joint。

get_interpolated_position(start_position, end_position, ratio)
    计算两点之间线性插值位置。

resample_joint(start_joint, end_joint, joint_number)
    安全插入中间 Joint。

JointResamplingTool
    参数和执行入口窗口。

main()
    创建或恢复窗口，立即显示并返回 QWidget。

安全规则
--------
- End Joint 必须是 Start Joint 的直接子 Joint；
- 不跨越已有中间 Joint 重建层级；
- 创建失败时删除本轮创建节点；
- 所有创建过程放在一个 Maya Undo Chunk 内。

直接运行
--------

    from muziToolset.tools.joint import joint_resamp_tool

    window = joint_resamp_tool.main()
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QSpinBox
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QSpinBox
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...ui import theme
from ...ui import window_utils
from ...ui.widgets import MayaObjectPicker


class JointResamplingTool(QWidget):
    """Joint Resample 窗口。"""

    def __init__(self, parent=None):
        super(JointResamplingTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"关节重采样",
            minimum_width=520
        )
        self.resize(540, 360)

    def create_widgets(self):
        """创建界面控件。"""
        self.title_label = theme.make_title(u"关节重采样")
        self.subtitle_label = theme.make_subtitle(
            u"在一对直接父子 Joint 之间均匀插入新的中间 Joint。"
        )

        self.start_joint_picker = MayaObjectPicker(
            label_text=u"起始 Joint",
            placeholder=u"选择父 Joint 后点击拾取",
            node_types=["joint"]
        )

        self.end_joint_picker = MayaObjectPicker(
            label_text=u"末端 Joint",
            placeholder=u"选择直接子 Joint 后点击拾取",
            node_types=["joint"]
        )

        self.joint_number_spinbox = QSpinBox()
        self.joint_number_spinbox.setMinimum(1)
        self.joint_number_spinbox.setMaximum(100)
        self.joint_number_spinbox.setValue(2)

        self.safety_label = QLabel(
            u"安全模式：只处理直接父子 Joint，不会跨越已有中间骨骼。"
        )
        self.safety_label.setWordWrap(True)
        theme.set_role(self.safety_label, "muted")

        self.resample_button = QPushButton(u"插入 Joint")
        theme.style_primary(self.resample_button)

    def create_layouts(self):
        """创建 Card 布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        range_card, range_layout = theme.make_card(self)
        range_layout.addWidget(
            theme.make_section_title(u"Joint 范围")
        )
        range_layout.addWidget(self.start_joint_picker)
        range_layout.addWidget(self.end_joint_picker)

        parameter_card, parameter_layout = theme.make_card(self)
        parameter_layout.addWidget(
            theme.make_section_title(u"插入参数")
        )

        number_layout = QHBoxLayout()
        number_layout.setContentsMargins(0, 0, 0, 0)
        number_layout.addWidget(QLabel(u"插入数量"))
        number_layout.addWidget(self.joint_number_spinbox)
        number_layout.addStretch(1)

        parameter_layout.addLayout(number_layout)
        parameter_layout.addWidget(self.safety_label)
        parameter_layout.addWidget(self.resample_button)

        main_layout.addWidget(range_card)
        main_layout.addWidget(parameter_card)
        main_layout.addStretch(1)

    def create_connections(self):
        """连接界面信号。"""
        self.resample_button.clicked.connect(
            self.resample
        )

    def resample(self):
        """读取当前 UI 参数并执行 Joint Resample。"""
        start_joint = self.start_joint_picker.get_value()
        end_joint = self.end_joint_picker.get_value()
        joint_number = self.joint_number_spinbox.value()

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
    """返回 Maya DAG 节点短名称。"""
    if "|" in node:
        return node.rsplit("|", 1)[-1]

    return node


def validate_joint(joint, label):
    """检查节点是否存在并且是 Joint。"""
    if not joint:
        cmds.warning(u"{}不能为空。".format(label))
        return False

    if not cmds.objExists(joint):
        cmds.warning(
            u"{}不存在：{}".format(
                label,
                joint
            )
        )
        return False

    if cmds.nodeType(joint) != "joint":
        cmds.warning(
            u"{}不是 Joint：{}".format(
                label,
                joint
            )
        )
        return False

    return True


def is_direct_child_joint(start_joint, end_joint):
    """检查 end_joint 是否是 start_joint 的直接子 Joint。"""
    parent_nodes = cmds.listRelatives(
        end_joint,
        parent=True,
        fullPath=True
    ) or []

    start_long_names = cmds.ls(
        start_joint,
        long=True
    ) or []

    if not parent_nodes or not start_long_names:
        return False

    return parent_nodes[0] == start_long_names[0]


def get_interpolated_position(start_position, end_position, ratio):
    """计算两个三维位置之间的线性插值位置。"""
    position = []

    for axis_index in range(3):
        start_value = start_position[axis_index]
        end_value = end_position[axis_index]
        value = start_value + (
            (end_value - start_value) * ratio
        )
        position.append(value)

    return position


def resample_joint(start_joint, end_joint, joint_number):
    """
    在直接父子 Joint 之间插入指定数量的新 Joint。

    执行步骤：
        1. 验证 Start / End 和直接父子关系；
        2. 记录两端世界位置；
        3. 临时把 End 放到 World；
        4. 按等比例位置依次创建并 Parent 新 Joint；
        5. 把 End 接回新 Chain 末端；
        6. 失败时删除新节点并恢复原始 Parent。
    """
    if not validate_joint(start_joint, u"起始 Joint"):
        return []

    if not validate_joint(end_joint, u"末端 Joint"):
        return []

    if start_joint == end_joint:
        cmds.warning(u"起始 Joint 和末端 Joint 不能相同。")
        return []

    if joint_number < 1:
        cmds.warning(u"插入 Joint 数量必须大于等于 1。")
        return []

    if not is_direct_child_joint(start_joint, end_joint):
        cmds.warning(
            u"安全模式只允许直接父子 Joint。当前末端 Joint 不是起始 Joint 的直接子级。"
        )
        return []

    # -------------------------------------------------------------------------
    # 步骤 1：记录两端世界位置。
    # -------------------------------------------------------------------------
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
        # ---------------------------------------------------------------------
        # 步骤 2：先把 End 暂时解除 Parent，避免创建新 Chain 时形成错误层级。
        # ---------------------------------------------------------------------
        cmds.parent(
            end_joint,
            world=True
        )

        # ---------------------------------------------------------------------
        # 步骤 3：按等比例位置创建 Joint，并逐个组成 Chain。
        # ---------------------------------------------------------------------
        for joint_index in range(joint_number):
            ratio = float(joint_index + 1) / float(
                joint_number + 1
            )

            position = get_interpolated_position(
                start_position,
                end_position,
                ratio
            )

            new_joint_name = "{}_resamp_{:03d}".format(
                start_short_name,
                joint_index + 1
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

        # ---------------------------------------------------------------------
        # 步骤 4：把原 End Joint 接到新 Chain 尾端。
        # ---------------------------------------------------------------------
        cmds.parent(
            end_joint,
            previous_joint
        )
        success = True

    except Exception as error:
        cmds.warning(str(error))

    finally:
        # ---------------------------------------------------------------------
        # 步骤 5：失败时清理本轮新节点并尽量恢复原始父子关系。
        # ---------------------------------------------------------------------
        if not success:
            delete_joints = []

            for created_joint in created_joints:
                if cmds.objExists(created_joint):
                    delete_joints.append(created_joint)

            if delete_joints:
                try:
                    cmds.delete(delete_joints)
                except Exception:
                    pass

            if cmds.objExists(end_joint) and cmds.objExists(start_joint):
                try:
                    current_parent = cmds.listRelatives(
                        end_joint,
                        parent=True,
                        fullPath=True
                    ) or []

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
    """创建或恢复 Joint Resample Tool，立即显示并返回 QWidget。"""
    return window_utils.show_window(
        "tools.joint.joint_resamp_tool",
        JointResamplingTool
    )


if __name__ == "__main__":
    main()
