# coding=utf-8
u"""
Joint Resample Tool
===================

在一对直接父子 Joint 之间均匀插入指定数量的新 Joint。

模块职责
--------
1. 提供 Start Joint / End Joint Picker 和插入数量参数；
2. 校验只处理直接父子 Joint；
3. 使用 Core 三维插值在两端之间插入新 Joint；
4. 创建失败时清理本轮新节点并尽量恢复原父子关系；
5. 提供可在 Maya Script Editor 中直接显示的 ``main()``。

架构边界
--------
- Joint 类型校验统一复用 ``core.joint_utils``；
- 三维插值统一复用 ``core.math_utils``；
- DAG Short Name 统一复用 ``core.rename_utils``；
- DAG Parent 查询统一复用 ``core.hierarchy_utils``；
- World Position 统一复用 ``core.transform_utils``；
- Long DAG Path 与 Undo Chunk 统一复用 ``core.scene_utils``；
- Tool 只保留“直接父子安全检查 + UI / Warning”工作流。
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

from ...core import hierarchy_utils
from ...core import joint_utils
from ...core import math_utils
from ...core import rename_utils
from ...core import scene_utils
from ...core import transform_utils
from ...ui import theme
from ...ui import window_utils
from ...ui.widgets import MayaObjectPicker


class JointResamplingTool(QWidget):
    """Joint Resample 窗口。"""

    def __init__(self, parent=None):
        u"""
        创建 Joint Resample 窗口。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """
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
        u"""
        创建界面控件。
        """
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
        u"""
        创建 Card 布局。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        number_layout = QHBoxLayout()
        number_layout.setContentsMargins(0, 0, 0, 0)
        number_layout.addWidget(QLabel(u"插入数量"))
        number_layout.addWidget(self.joint_number_spinbox)
        number_layout.addStretch(1)

        # -------------------------------------------------------------------------
        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        parameter_layout.addLayout(number_layout)
        parameter_layout.addWidget(self.safety_label)
        parameter_layout.addWidget(self.resample_button)

        main_layout.addWidget(range_card)
        main_layout.addWidget(parameter_card)
        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        main_layout.addStretch(1)

    def create_connections(self):
        u"""
        连接界面信号。
        """
        self.resample_button.clicked.connect(
            self.resample
        )

    def resample(self):
        u"""
        读取当前 UI 参数并执行 Joint Resample。
        """
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


def validate_joint(joint, label):
    u"""
    使用 Joint Core 校验，并把异常转换成 Tool Warning。

    Args:
        joint (str):
            需要处理的 Maya Joint 节点名称。
        label (str):
            UI、Rig Node 或日志中展示的简短 Label。

    Returns:
        bool:
        当前操作成功或目标状态满足要求时返回 True，否则返回 False。
    """
    if not joint:
        cmds.warning(
            u"{}不能为空。".format(label)
        )
        return False

    try:
        joint_utils.Joint(
            joint
        )
    except RuntimeError as error:
        cmds.warning(
            u"{}无效：{}".format(
                label,
                error
            )
        )
        return False

    return True


def is_direct_child_joint(start_joint, end_joint):
    u"""
    检查 end_joint 是否是 start_joint 的直接子 Joint。

    Args:
        start_joint (str):
            当前 Rig 计算或构建使用的 Maya Joint 节点。
        end_joint (str):
            当前 Rig 计算或构建使用的 Maya Joint 节点。

    Returns:
        object | bool:
        条件成立时返回 True，否则返回 False。
    """
    try:
        start_long_name = scene_utils.get_long_name(
            start_joint
        )
    except RuntimeError:
        return False

    parent_node = hierarchy_utils.get_parent(
        end_joint,
        full_path=True
    )

    if parent_node is None:
        return False

    return parent_node == start_long_name


@scene_utils.undo_chunk
def resample_joint(start_joint, end_joint, joint_number):
    u"""
    在直接父子 Joint 之间插入指定数量的新 Joint。

    Args:
        start_joint (str):
            当前 Rig 计算或构建使用的 Maya Joint 节点。
        end_joint (str):
            当前 Rig 计算或构建使用的 Maya Joint 节点。
        joint_number (int):
            当前构建、采样或查询过程使用的元素数量。

    Returns:
        object | list:
        按当前 API 约定顺序返回的结果列表。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not validate_joint(
            start_joint,
            u"起始 Joint"
    ):
        return []

    if not validate_joint(
            end_joint,
            u"末端 Joint"
    ):
        return []

    if start_joint == end_joint:
        cmds.warning(
            u"起始 Joint 和末端 Joint 不能相同。"
        )
        return []

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    joint_number = int(
        joint_number
    )

    if joint_number < 1:
        cmds.warning(
            u"插入 Joint 数量必须大于等于 1。"
        )
        return []

    if not is_direct_child_joint(
            start_joint,
            end_joint
    ):
        cmds.warning(
            u"安全模式只允许直接父子 Joint。当前末端 Joint 不是起始 Joint 的直接子级。"
        )
        return []

    start_position = transform_utils.get_world_translation(
        start_joint
    )
    # -------------------------------------------------------------------------
    # Step 03：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    end_position = transform_utils.get_world_translation(
        end_joint
    )
    start_short_name = rename_utils.get_short_name(
        start_joint
    )

    created_joints = []
    previous_joint = start_joint
    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    success = False

    try:
        end_joint = hierarchy_utils.parent(
            end_joint,
            None
        )

        joint_index = 0

        while joint_index < joint_number:
            ratio = float(joint_index + 1) / float(
                joint_number + 1
            )
            position = math_utils.lerp_point3(
                start_position,
                end_position,
                ratio
            )
            new_joint_name = "{}_resamp_{:03d}".format(
                start_short_name,
                joint_index + 1
            )

            new_joint = joint_utils.Joint.create(
                name=new_joint_name,
                position=position,
                parent=previous_joint
            )

            created_joints.append(
                new_joint
            )
            previous_joint = new_joint
            joint_index += 1

        end_joint = hierarchy_utils.parent(
            end_joint,
            previous_joint
        )
        success = True

    except Exception as error:
        cmds.warning(
            str(error)
        )

    finally:
        if not success:
            delete_joints = []

            for created_joint in created_joints:
                if cmds.objExists(created_joint):
                    delete_joints.append(
                        created_joint
                    )

            if delete_joints:
                try:
                    cmds.delete(
                        delete_joints
                    )
                except Exception:
                    pass

            if cmds.objExists(end_joint):
                if cmds.objExists(start_joint):
                    try:
                        current_parent = hierarchy_utils.get_parent(
                            end_joint,
                            full_path=True
                        )

                        if current_parent is None:
                            end_joint = hierarchy_utils.parent(
                                end_joint,
                                start_joint
                            )
                    except Exception:
                        pass

    if not success:
        return []

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return created_joints


def main():
    u"""
    创建或恢复 Joint Resample Tool，立即显示并返回 QWidget。

    Returns:
        object:
        当前工具入口创建并显示的窗口或执行结果。
    """
    return window_utils.show_window(
        "tools.joint.joint_resamp_tool",
        JointResamplingTool
    )


if __name__ == "__main__":
    main()
