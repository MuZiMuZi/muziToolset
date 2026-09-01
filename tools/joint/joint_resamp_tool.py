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

架构边界
--------
- Joint 类型校验统一复用 ``core.joint_utils``；
- DAG Short Name 统一复用 ``core.rename_utils``；
- DAG Parent 查询统一复用 ``core.hierarchy_utils``；
- World Position 统一复用 ``core.transform_utils``；
- Long DAG Path 与 Undo Chunk 统一复用 ``core.scene_utils``；
- Tool 只保留“直接父子安全检查 + 线性重采样 + UI”工作流。

安全规则
--------
- End Joint 必须是 Start Joint 的直接子 Joint；
- 不跨越已有中间 Joint 重建层级；
- 创建失败时删除本轮创建节点；
- 整个创建过程是一个 Maya Undo Chunk。
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
            parent (QWidget | None):
                Qt 父窗口。
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

        # 调用参数化重采样函数，UI 不直接实现 Joint 构建算法。
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
    使用 Joint Core 检查节点是否存在并且是 Joint。

    Args:
        joint (str):
            需要检查的 Maya Joint。
        label (str):
            Warning 中展示的输入名称。

    Returns:
        bool:
        合法 Joint 返回 True，否则 Warning 并返回 False。
    """
    if not joint:
        cmds.warning(
            u"{}不能为空。".format(label)
        )
        return False

    try:
        # 构造 Joint Core 对象，让 Joint 类型规则只维护在 core.joint_utils。
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
            父 Joint。
        end_joint (str):
            需要检查的 Child Joint。

    Returns:
        bool:
        End 是 Start 的直接子级时返回 True。
    """
    # 使用 Scene Core 把 Start 解析成唯一 Long Path，避免重名 DAG 误判。
    try:
        start_long_name = scene_utils.get_long_name(
            start_joint
        )
    except RuntimeError:
        return False

    # 使用 Hierarchy Core 查询 End 的直接 Parent。
    parent_node = hierarchy_utils.get_parent(
        end_joint,
        full_path=True
    )

    if parent_node is None:
        return False

    return parent_node == start_long_name


def get_interpolated_position(start_position, end_position, ratio):
    u"""
    计算两个三维位置之间的线性插值位置。

    Args:
        start_position (list[float] | tuple[float, float, float]):
            起始世界位置。
        end_position (list[float] | tuple[float, float, float]):
            结束世界位置。
        ratio (float):
            0.0～1.0 插值比例。

    Returns:
        list[float]:
        插值后的 XYZ 世界位置。
    """
    position = []

    for axis_index in range(3):
        start_value = start_position[axis_index]
        end_value = end_position[axis_index]

        value = start_value + (
            (end_value - start_value) * ratio
        )

        position.append(
            value
        )

    return position


@scene_utils.undo_chunk
def resample_joint(start_joint, end_joint, joint_number):
    u"""
    在直接父子 Joint 之间插入指定数量的新 Joint。

    执行步骤：
        1. 验证 Start / End 和直接父子关系；
        2. 记录两端世界位置；
        3. 临时把 End 放到 World；
        4. 按等比例位置依次创建并 Parent 新 Joint；
        5. 把 End 接回新 Chain 末端；
        6. 失败时删除新节点并恢复原始 Parent。

    Args:
        start_joint (str):
            起始父 Joint。
        end_joint (str):
            末端直接子 Joint。
        joint_number (int):
            需要插入的新 Joint 数量。

    Returns:
        list[str]:
        成功创建的中间 Joint；失败返回空列表。
    """
    # 检查 Start / End 都是有效 Joint。
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

    joint_number = int(
        joint_number
    )

    if joint_number < 1:
        cmds.warning(
            u"插入 Joint 数量必须大于等于 1。"
        )
        return []

    # 安全模式只允许重采样一段直接父子 Joint。
    if not is_direct_child_joint(
            start_joint,
            end_joint
    ):
        cmds.warning(
            u"安全模式只允许直接父子 Joint。当前末端 Joint 不是起始 Joint 的直接子级。"
        )
        return []

    # 使用 Transform Core 记录两端世界位置。
    start_position = transform_utils.get_world_translation(
        start_joint
    )
    end_position = transform_utils.get_world_translation(
        end_joint
    )

    # 使用统一 Short Name API 生成新 Joint 名称。
    start_short_name = rename_utils.get_short_name(
        start_joint
    )

    created_joints = []
    previous_joint = start_joint
    success = False

    try:
        # 临时把 End 放到 World，避免插入新 Chain 时形成错误层级。
        end_joint = hierarchy_utils.parent(
            end_joint,
            None
        )

        # 按等比例位置创建 Joint，并逐个组成 Chain。
        for joint_index in range(joint_number):
            ratio = float(joint_index + 1) / float(
                joint_number + 1
            )

            # 计算当前中间 Joint 的世界位置。
            position = get_interpolated_position(
                start_position,
                end_position,
                ratio
            )

            new_joint_name = "{}_resamp_{:03d}".format(
                start_short_name,
                joint_index + 1
            )

            # 使用 Joint Core 创建新 Joint，不在 Tool 内维护另一套 Joint 创建逻辑。
            new_joint = joint_utils.Joint.create(
                name=new_joint_name,
                position=position,
                parent=previous_joint
            )

            created_joints.append(
                new_joint
            )
            previous_joint = new_joint

        # 把原 End Joint 接回新 Chain 尾端。
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
            # 删除本轮创建的中间 Joint。
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

            # 尽量恢复 Start -> End 的原始直接父子关系。
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

    return created_joints


def main():
    u"""
    创建或恢复 Joint Resample Tool，立即显示并返回 QWidget。

    Returns:
        QWidget:
        Joint Resample 窗口。
    """
    return window_utils.show_window(
        "tools.joint.joint_resamp_tool",
        JointResamplingTool
    )


if __name__ == "__main__":
    main()
