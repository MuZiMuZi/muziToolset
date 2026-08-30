# coding=utf-8
u"""
Rig Tool
========

大型绑定工具集中的通用 Rig 工具入口。

职责：
    1. 启动 FK / Controller / Joint / Skirt 专项工具；
    2. 创建基础 RP IK Rig；
    3. 管理带 muziRigType 标记的 Rig Module；
    4. 提供常用 Rig 场景工具。

架构：
    - Controller 创建统一调用 systems.controller；
    - Snap 等通用算法统一调用 core；
    - 子窗口统一交给 app.window_manager；
    - 本文件只保留 Rig Tool UI 和少量模块级组装逻辑。
"""

from __future__ import print_function

import math

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QScrollArea
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QScrollArea
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...app import window_manager
from ...core import snap_utils
from ...systems import controller as controller_system
from ...ui import theme
from ...ui import window_utils
from ...ui.widgets import MayaObjectPicker
from ..controller import create_ctrl_tool
from ..controller import create_fk_ctrl_tool
from ..joint import joint_tool
from . import skirt_ctrl_tool


def get_short_name(node):
    u"""
    返回 DAG 节点短名称。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return node.split("|")[-1]


def get_long_name(node):
    u"""
    把 Maya DAG 节点统一解析成长路径。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object | None:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    if not node:
        return None

    matches = cmds.ls(
        node,
        long=True
    )

    if matches is None:
        matches = []

    if not matches:
        return None

    if len(matches) > 1:
        raise RuntimeError(
            u"节点名称不唯一，请使用完整 DAG 路径：{}".format(node)
        )

    return matches[0]


def vector_subtract(vector_a, vector_b):
    u"""
    三维向量相减。

    Args:
        vector_a (object):
            `vector_a` 对应的输入数据。
        vector_b (object):
            `vector_b` 对应的输入数据。

    Returns:
        list:
        方法执行后的结果数据。
    """
    return [
        vector_a[0] - vector_b[0],
        vector_a[1] - vector_b[1],
        vector_a[2] - vector_b[2],
    ]


def vector_add(vector_a, vector_b):
    u"""
    三维向量相加。

    Args:
        vector_a (object):
            `vector_a` 对应的输入数据。
        vector_b (object):
            `vector_b` 对应的输入数据。

    Returns:
        list:
        方法执行后的结果数据。
    """
    return [
        vector_a[0] + vector_b[0],
        vector_a[1] + vector_b[1],
        vector_a[2] + vector_b[2],
    ]


def vector_multiply(vector, value):
    u"""
    三维向量乘标量。

    Args:
        vector (object):
            `vector` 对应的输入数据。
        value (float):
            需要读取、写入或参与计算的数值。

    Returns:
        list:
        方法执行后的结果数据。
    """
    return [
        vector[0] * value,
        vector[1] * value,
        vector[2] * value,
    ]


def vector_length(vector):
    u"""
    返回三维向量长度。

    Args:
        vector (object):
            `vector` 对应的输入数据。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return math.sqrt(
        vector[0] * vector[0]
        + vector[1] * vector[1]
        + vector[2] * vector[2]
    )


def vector_normalize(vector):
    u"""
    返回单位向量。

    Args:
        vector (object):
            `vector` 对应的输入数据。

    Returns:
        list:
        方法执行后的结果数据。
    """
    length = vector_length(vector)

    if length <= 0.000001:
        return [0.0, 0.0, 0.0]

    return [
        vector[0] / length,
        vector[1] / length,
        vector[2] / length,
    ]


def dot_product(vector_a, vector_b):
    u"""
    返回三维向量点积。

    Args:
        vector_a (object):
            `vector_a` 对应的输入数据。
        vector_b (object):
            `vector_b` 对应的输入数据。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return (
        vector_a[0] * vector_b[0]
        + vector_a[1] * vector_b[1]
        + vector_a[2] * vector_b[2]
    )


def get_joint_path(start_joint, end_joint):
    u"""
    返回 start_joint 到 end_joint 的 Joint 路径。

    Args:
        start_joint (object):
            `start_joint` 对应的输入数据。
        end_joint (object):
            `end_joint` 对应的输入数据。

    Returns:
        object | None | list:
        方法执行后的结果数据。
    """
    start_joint = get_long_name(start_joint)
    end_joint = get_long_name(end_joint)

    if start_joint is None:
        return None

    if end_joint is None:
        return None

    if start_joint == end_joint:
        return [start_joint]

    def walk(current_joint, current_path):
        children = cmds.listRelatives(
            current_joint,
            children=True,
            type="joint",
            fullPath=True
        )

        if children is None:
            children = []

        for child_joint in children:
            child_path = []

            for path_joint in current_path:
                child_path.append(path_joint)

            child_path.append(child_joint)

            if child_joint == end_joint:
                return child_path

            result = walk(
                child_joint,
                child_path
            )

            if result:
                return result

        return None

    return walk(
        start_joint,
        [start_joint]
    )


def get_pole_vector_position(
        start_joint,
        middle_joint,
        end_joint
):
    u"""
    计算三关节链 Pole Vector 推荐位置。

    Args:
        start_joint (object):
            `start_joint` 对应的输入数据。
        middle_joint (object):
            `middle_joint` 对应的输入数据。
        end_joint (object):
            `end_joint` 对应的输入数据。

    Returns:
        object:
        方法执行后的结果数据。
    """
    start_position = cmds.xform(
        start_joint,
        query=True,
        worldSpace=True,
        translation=True
    )
    middle_position = cmds.xform(
        middle_joint,
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

    start_to_end = vector_subtract(
        end_position,
        start_position
    )
    start_to_middle = vector_subtract(
        middle_position,
        start_position
    )

    line_length = vector_length(start_to_end)

    if line_length <= 0.000001:
        return middle_position

    line_direction = vector_normalize(start_to_end)
    projection_length = dot_product(
        start_to_middle,
        line_direction
    )
    projection = vector_add(
        start_position,
        vector_multiply(
            line_direction,
            projection_length
        )
    )

    pole_direction = vector_subtract(
        middle_position,
        projection
    )
    pole_direction = vector_normalize(pole_direction)

    if vector_length(pole_direction) <= 0.000001:
        pole_direction = [0.0, 0.0, 1.0]

    chain_length = (
        vector_length(
            vector_subtract(
                middle_position,
                start_position
            )
        )
        + vector_length(
            vector_subtract(
                end_position,
                middle_position
            )
        )
    )

    return vector_add(
        middle_position,
        vector_multiply(
            pole_direction,
            chain_length * 0.75
        )
    )


def create_ik_rig(start_joint, end_joint):
    u"""
    创建基础 RP IK、End Controller 和 Pole Vector Controller。

    Args:
        start_joint (object):
            `start_joint` 对应的输入数据。
        end_joint (object):
            `end_joint` 对应的输入数据。

    Returns:
        dict:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    original_start_joint = start_joint
    original_end_joint = end_joint

    start_joint = get_long_name(start_joint)
    end_joint = get_long_name(end_joint)

    if start_joint is None:
        raise RuntimeError(
            u"IK 起始 Joint 不存在：{}".format(original_start_joint)
        )

    if end_joint is None:
        raise RuntimeError(
            u"IK 末端 Joint 不存在：{}".format(original_end_joint)
        )

    if cmds.nodeType(start_joint) != "joint":
        raise RuntimeError(u"IK 起始节点必须是 Joint。")

    if cmds.nodeType(end_joint) != "joint":
        raise RuntimeError(u"IK 末端节点必须是 Joint。")

    joint_path = get_joint_path(
        start_joint,
        end_joint
    )

    if not joint_path or len(joint_path) < 2:
        raise RuntimeError(
            u"起始 Joint 和末端 Joint 不在同一条子 Joint Chain 上。"
        )

    base_name = get_short_name(start_joint)

    if base_name.startswith("jnt_"):
        base_name = base_name[4:]

    rig_group_name = "rig_ik_{}_grp".format(base_name)

    if cmds.objExists(rig_group_name):
        raise RuntimeError(
            u"IK Rig 已存在：{}".format(rig_group_name)
        )

    rig_group = cmds.createNode(
        "transform",
        name=rig_group_name
    )

    cmds.addAttr(
        rig_group,
        longName="muziRigType",
        dataType="string"
    )
    cmds.setAttr(
        rig_group + ".muziRigType",
        "ik",
        type="string"
    )

    ik_handle_result = cmds.ikHandle(
        startJoint=start_joint,
        endEffector=end_joint,
        solver="ikRPsolver",
        name="ikh_{}".format(base_name)
    )

    ik_handle = ik_handle_result[0]
    effector = ik_handle_result[1]

    cmds.parent(
        ik_handle,
        rig_group
    )

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

    chain_size = vector_length(
        vector_subtract(
            end_position,
            start_position
        )
    )
    control_radius = max(
        chain_size * 0.15,
        0.5
    )

    end_control_result = controller_system.create_controller(
        name="ctrl_{}_ik".format(base_name),
        shape="circle",
        radius=control_radius,
        axis="Y+",
        target=end_joint,
        color=17,
        create_sub_control=False,
        create_extra_groups=True,
        add_to_set=True
    )

    end_control = end_control_result["control"]
    end_top_group = end_control_result["top_group"]

    cmds.parent(
        end_top_group,
        rig_group
    )

    cmds.pointConstraint(
        end_control,
        ik_handle,
        maintainOffset=False
    )
    cmds.orientConstraint(
        end_control,
        end_joint,
        maintainOffset=True
    )

    pole_control = None

    if len(joint_path) >= 3:
        middle_index = int(len(joint_path) / 2)
        middle_joint = joint_path[middle_index]
        pole_position = get_pole_vector_position(
            start_joint,
            middle_joint,
            end_joint
        )

        pole_result = controller_system.create_controller(
            name="ctrl_{}_pv".format(base_name),
            shape="circle",
            radius=max(
                control_radius * 0.65,
                0.3
            ),
            axis="Y+",
            target=middle_joint,
            color=17,
            create_sub_control=False,
            create_extra_groups=True,
            add_to_set=True
        )

        pole_control = pole_result["control"]
        pole_top_group = pole_result["top_group"]

        cmds.xform(
            pole_top_group,
            worldSpace=True,
            translation=pole_position
        )
        cmds.parent(
            pole_top_group,
            rig_group
        )
        cmds.poleVectorConstraint(
            pole_control,
            ik_handle
        )

    cmds.setAttr(
        ik_handle + ".visibility",
        0
    )

    return {
        "group": rig_group,
        "ik_handle": ik_handle,
        "effector": effector,
        "end_control": end_control,
        "pole_control": pole_control,
    }


def find_rig_root(node):
    u"""
    沿父层级查找带 muziRigType 的 Rig Module Root。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        None | object:
        方法执行后的结果数据。
    """
    current_node = get_long_name(node)

    while current_node:
        if cmds.attributeQuery(
                "muziRigType",
                node=current_node,
                exists=True
        ):
            return current_node

        parents = cmds.listRelatives(
            current_node,
            parent=True,
            fullPath=True
        )

        if parents is None:
            parents = []

        if not parents:
            break

        current_node = parents[0]

    return None


def get_duplicate_map():
    u"""
    按短名称收集场景重名 DAG 节点。

    Returns:
        object:
        方法执行后的结果数据。
    """
    nodes = cmds.ls(
        long=True,
        dagObjects=True
    )

    if nodes is None:
        nodes = []

    name_map = {}

    for node in nodes:
        short_name = get_short_name(node)

        if short_name not in name_map:
            name_map[short_name] = []

        name_map[short_name].append(node)

    duplicates = {}

    for short_name in name_map:
        matches = name_map[short_name]

        if len(matches) > 1:
            duplicates[short_name] = matches

    return duplicates


class RigTool(QWidget):
    """通用 Rig 主工具面板。"""

    def __init__(self, parent=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        super(RigTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"Rig 工具",
            minimum_width=600
        )
        self.resize(640, 760)

    def create_widgets(self):
        u"""
        创建界面控件。
        """
        self.title_label = theme.make_title(u"Rig 工具")
        self.subtitle_label = theme.make_subtitle(
            u"集中处理 Controller、FK、基础 IK、Rig Module 和常用绑定操作。"
        )

        self.create_fk_button = QPushButton(u"创建 FK Controller")
        self.open_control_creator_button = QPushButton(u"Controller Creator")
        self.open_joint_tool_button = QPushButton(u"Joint Tool")
        self.open_skirt_tool_button = QPushButton(u"Skirt Rig Tool")

        self.ik_start_picker = MayaObjectPicker(
            label_text=u"起始 Joint",
            placeholder=u"IK Chain 起始 Joint",
            node_types=["joint"]
        )
        self.ik_end_picker = MayaObjectPicker(
            label_text=u"末端 Joint",
            placeholder=u"IK Chain 末端 Joint",
            node_types=["joint"]
        )

        self.create_ik_button = QPushButton(u"创建 RP IK Rig")
        theme.style_primary(self.create_ik_button)

        self.delete_rig_button = QPushButton(u"删除选择 Rig Module")
        theme.style_danger(self.delete_rig_button)

        self.clear_keys_button = QPushButton(u"删除关键帧")
        self.reset_attrs_button = QPushButton(u"重置可动画属性")
        self.batch_constraint_button = QPushButton(u"批量 Parent Constraint")
        self.create_default_groups_button = QPushButton(u"创建默认 Rig 层级")
        self.add_zero_group_button = QPushButton(u"添加 Zero Group")
        self.select_children_button = QPushButton(u"选择全部子物体")
        self.snap_button = QPushButton(u"最后对象吸附到参考中心")
        self.print_duplicates_button = QPushButton(u"打印重名节点")
        self.rename_duplicates_button = QPushButton(u"重命名重复节点")

    def create_layouts(self):
        u"""
        创建 Card 布局。
        """
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        root_layout.addWidget(self.title_label)
        root_layout.addWidget(self.subtitle_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 6, 0)
        content_layout.setSpacing(12)

        launch_card, launch_layout = theme.make_card(content)
        launch_layout.addWidget(
            theme.make_section_title(u"专项工具")
        )

        launch_grid = QGridLayout()
        launch_grid.setHorizontalSpacing(8)
        launch_grid.setVerticalSpacing(8)
        launch_grid.addWidget(self.create_fk_button, 0, 0)
        launch_grid.addWidget(self.open_control_creator_button, 0, 1)
        launch_grid.addWidget(self.open_joint_tool_button, 1, 0)
        launch_grid.addWidget(self.open_skirt_tool_button, 1, 1)
        launch_layout.addLayout(launch_grid)

        ik_card, ik_layout = theme.make_card(content)
        ik_layout.addWidget(
            theme.make_section_title(u"RP IK")
        )
        ik_layout.addWidget(self.ik_start_picker)
        ik_layout.addWidget(self.ik_end_picker)

        ik_button_layout = QGridLayout()
        ik_button_layout.addWidget(self.create_ik_button, 0, 0)
        ik_button_layout.addWidget(self.delete_rig_button, 0, 1)
        ik_layout.addLayout(ik_button_layout)

        utility_card, utility_layout = theme.make_card(content)
        utility_layout.addWidget(
            theme.make_section_title(u"Rig Utility")
        )

        utility_grid = QGridLayout()
        utility_grid.setHorizontalSpacing(8)
        utility_grid.setVerticalSpacing(8)

        utility_buttons = [
            self.clear_keys_button,
            self.reset_attrs_button,
            self.batch_constraint_button,
            self.create_default_groups_button,
            self.add_zero_group_button,
            self.select_children_button,
            self.snap_button,
            self.print_duplicates_button,
            self.rename_duplicates_button,
        ]

        button_index = 0

        for button in utility_buttons:
            row = int(button_index / 2)
            column = button_index % 2
            utility_grid.addWidget(
                button,
                row,
                column
            )
            button_index += 1

        utility_layout.addLayout(utility_grid)

        content_layout.addWidget(launch_card)
        content_layout.addWidget(ik_card)
        content_layout.addWidget(utility_card)
        content_layout.addStretch(1)

        scroll_area.setWidget(content)
        root_layout.addWidget(scroll_area, 1)

    def create_connections(self):
        u"""
        连接界面信号。
        """
        self.create_fk_button.clicked.connect(
            self.open_fk_tool
        )
        self.open_control_creator_button.clicked.connect(
            self.open_control_creator
        )
        self.open_joint_tool_button.clicked.connect(
            self.open_joint_tool
        )
        self.open_skirt_tool_button.clicked.connect(
            self.open_skirt_tool
        )
        self.create_ik_button.clicked.connect(
            self.create_ik
        )
        self.delete_rig_button.clicked.connect(
            self.delete_selected_rig
        )
        self.clear_keys_button.clicked.connect(
            self.clear_keys
        )
        self.reset_attrs_button.clicked.connect(
            self.reset_attributes
        )
        self.batch_constraint_button.clicked.connect(
            self.batch_parent_constraint
        )
        self.create_default_groups_button.clicked.connect(
            self.create_default_groups
        )
        self.add_zero_group_button.clicked.connect(
            self.add_zero_groups
        )
        self.select_children_button.clicked.connect(
            self.select_children
        )
        self.snap_button.clicked.connect(
            self.snap_last_to_center
        )
        self.print_duplicates_button.clicked.connect(
            self.print_duplicate_nodes
        )
        self.rename_duplicates_button.clicked.connect(
            self.rename_duplicate_nodes
        )

    @staticmethod
    def open_tool(tool_key, tool_module):
        u"""
        通过统一 Window Manager 执行或打开专项工具。

        Args:
            tool_key (object):
                `tool_key` 对应的输入数据。
            tool_module (object):
                `tool_module` 对应的输入数据。

        Returns:
            object:
            方法执行后的结果数据。
        """
        return window_manager.show_tool(
            "rig/{}".format(tool_key),
            tool_module.main
        )

    def open_fk_tool(self):
        u"""
        执行 `open_fk_tool` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self.open_tool(
            "fk_controller",
            create_fk_ctrl_tool
        )

    def open_control_creator(self):
        u"""
        执行 `open_control_creator` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self.open_tool(
            "controller_creator",
            create_ctrl_tool
        )

    def open_joint_tool(self):
        u"""
        执行 `open_joint_tool` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self.open_tool(
            "joint_tool",
            joint_tool
        )

    def open_skirt_tool(self):
        u"""
        执行 `open_skirt_tool` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self.open_tool(
            "skirt_rig",
            skirt_ctrl_tool
        )

    def create_ik(self):
        u"""
        根据当前 Picker 创建基础 RP IK Rig。
        """
        start_joint = self.ik_start_picker.get_value()
        end_joint = self.ik_end_picker.get_value()

        if not start_joint or not end_joint:
            cmds.warning(u"请先拾取 IK 起始和末端 Joint。")
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziCreateIkRig"
        )

        try:
            result = create_ik_rig(
                start_joint,
                end_joint
            )
            cmds.select(
                result["group"],
                replace=True
            )
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    @staticmethod
    def delete_selected_rig():
        u"""
        删除选择节点所属的 Muzi Rig Module。
        """
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        rig_roots = []

        for node in selections:
            rig_root = find_rig_root(node)

            if rig_root and rig_root not in rig_roots:
                rig_roots.append(rig_root)

        if not rig_roots:
            cmds.warning(u"选择中未找到带 muziRigType 的 Rig Module。")
            return

        cmds.delete(rig_roots)

    @staticmethod
    def clear_keys():
        u"""
        删除选择对象关键帧；没有选择时清理场景 AnimCurve。
        """
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections:
            cmds.cutKey(
                selections,
                clear=True
            )
            return

        anim_curve_types = [
            "animCurveTA",
            "animCurveTL",
            "animCurveTT",
            "animCurveTU",
        ]
        anim_curves = []

        for node_type in anim_curve_types:
            nodes = cmds.ls(type=node_type)

            if nodes is None:
                nodes = []

            for node in nodes:
                anim_curves.append(node)

        if anim_curves:
            cmds.delete(anim_curves)

    @staticmethod
    def reset_attributes():
        u"""
        把选择对象可设置的 Keyable Attribute 恢复默认值。
        """
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(u"请先选择需要重置的对象。")
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziResetAttrs"
        )

        try:
            for node in selections:
                attrs = cmds.listAttr(
                    node,
                    keyable=True
                )

                if attrs is None:
                    attrs = []

                for attr_name in attrs:
                    plug = "{}.{}".format(
                        node,
                        attr_name
                    )

                    if not cmds.getAttr(
                            plug,
                            settable=True
                    ):
                        continue

                    source_connections = cmds.listConnections(
                        plug,
                        source=True,
                        destination=False,
                        plugs=True
                    )

                    if source_connections:
                        continue

                    defaults = cmds.attributeQuery(
                        attr_name,
                        node=node,
                        listDefault=True
                    )

                    if not defaults:
                        continue

                    try:
                        cmds.setAttr(
                            plug,
                            defaults[0]
                        )
                    except Exception:
                        pass
        finally:
            cmds.undoInfo(closeChunk=True)

    @staticmethod
    def batch_parent_constraint():
        u"""
        按 driver/driven 成对顺序批量创建 Parent Constraint。
        """
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if len(selections) < 2 or len(selections) % 2 != 0:
            cmds.warning(
                u"请按 driver1, driven1, driver2, driven2... 顺序选择偶数个对象。"
            )
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziRigBatchParentConstraint"
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

    @staticmethod
    def create_default_groups():
        u"""
        创建基础 Rig 层级。
        """
        group_names = [
            "rig_grp",
            "geo_grp",
            "skeleton_grp",
            "controls_grp",
            "noTouch_grp",
        ]
        created_groups = {}

        for group_name in group_names:
            if cmds.objExists(group_name):
                created_groups[group_name] = group_name
            else:
                created_groups[group_name] = cmds.createNode(
                    "transform",
                    name=group_name
                )

        child_names = [
            "geo_grp",
            "skeleton_grp",
            "controls_grp",
            "noTouch_grp",
        ]

        for child_name in child_names:
            child_group = created_groups[child_name]
            parents = cmds.listRelatives(
                child_group,
                parent=True
            )

            if not parents:
                cmds.parent(
                    child_group,
                    created_groups["rig_grp"]
                )

        cmds.setAttr(
            created_groups["noTouch_grp"] + ".visibility",
            0
        )
        cmds.select(
            created_groups["rig_grp"],
            replace=True
        )

    @staticmethod
    def add_zero_groups():
        u"""
        为选择对象创建匹配 Transform 的 Zero Group。
        """
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(u"请先选择需要添加 Zero Group 的对象。")
            return

        created_groups = []

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziAddZeroGroups"
        )

        try:
            for node in selections:
                short_name = get_short_name(node)

                if short_name.startswith("ctrl_"):
                    zero_name = short_name.replace(
                        "ctrl_",
                        "zero_",
                        1
                    )
                else:
                    zero_name = "zero_{}".format(short_name)

                if cmds.objExists(zero_name):
                    cmds.warning(
                        u"Zero Group 已存在，跳过：{}".format(zero_name)
                    )
                    continue

                parent_nodes = cmds.listRelatives(
                    node,
                    parent=True,
                    fullPath=True
                )

                if parent_nodes is None:
                    parent_nodes = []

                zero_group = cmds.createNode(
                    "transform",
                    name=zero_name
                )
                cmds.matchTransform(
                    zero_group,
                    node,
                    position=True,
                    rotation=True,
                    scale=True
                )

                if parent_nodes:
                    cmds.parent(
                        zero_group,
                        parent_nodes[0]
                    )

                cmds.parent(
                    node,
                    zero_group
                )
                created_groups.append(zero_group)
        finally:
            cmds.undoInfo(closeChunk=True)

        if created_groups:
            cmds.select(
                created_groups,
                replace=True
            )

    @staticmethod
    def select_children():
        u"""
        选择当前对象全部后代节点。
        """
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(u"请先选择父对象。")
            return

        result = []

        for node in selections:
            descendants = cmds.listRelatives(
                node,
                allDescendents=True,
                fullPath=True
            )

            if descendants is None:
                descendants = []

            for descendant in descendants:
                if descendant not in result:
                    result.append(descendant)

        if result:
            cmds.select(
                result,
                replace=True
            )

    @staticmethod
    def snap_last_to_center():
        u"""
        把最后选择对象吸附到前面参考项平均位置和旋转。
        """
        selections = cmds.ls(
            selection=True,
            long=True,
            flatten=True
        )

        if selections is None:
            selections = []

        if len(selections) < 2:
            cmds.warning(u"至少选择两个对象，最后一个作为被吸附对象。")
            return

        references = selections[:-1]
        target = selections[-1]

        try:
            snap_utils.snap_to_average(
                reference_items=references,
                target_item=target,
                include_rotation=True
            )
        except Exception as error:
            cmds.warning(str(error))

    @staticmethod
    def print_duplicate_nodes():
        u"""
        打印重名 DAG 节点。
        """
        duplicates = get_duplicate_map()

        if not duplicates:
            print(u"[Rig Tool] 场景中没有重名 DAG 节点。")
            return

        short_names = []

        for short_name in duplicates:
            short_names.append(short_name)

        short_names.sort()

        print(u"[Rig Tool] 重名 DAG 节点：")

        for short_name in short_names:
            print(u"  {}".format(short_name))

            for node in duplicates[short_name]:
                print(u"    {}".format(node))

    @staticmethod
    def rename_duplicate_nodes():
        u"""
        给重名 DAG 节点追加递增编号。
        """
        duplicates = get_duplicate_map()

        if not duplicates:
            print(u"[Rig Tool] 场景中没有重名 DAG 节点。")
            return

        short_names = []

        for short_name in duplicates:
            short_names.append(short_name)

        short_names.sort()

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziRenameDuplicates"
        )

        try:
            for short_name in short_names:
                matches = duplicates[short_name]
                match_index = 1

                while match_index < len(matches):
                    node = matches[match_index]
                    suffix_index = match_index
                    new_name = "{}_{:03d}".format(
                        short_name,
                        suffix_index
                    )

                    while cmds.objExists(new_name):
                        suffix_index += 1
                        new_name = "{}_{:03d}".format(
                            short_name,
                            suffix_index
                        )

                    try:
                        cmds.rename(
                            node,
                            new_name
                        )
                    except Exception as error:
                        cmds.warning(str(error))

                    match_index += 1
        finally:
            cmds.undoInfo(closeChunk=True)


def main():
    u"""
    显示并返回 Rig Tool。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return window_utils.show_window(
        "tools.rig.rig_tool",
        RigTool
    )


__all__ = [
    "RigTool",
    "create_ik_rig",
    "find_rig_root",
    "get_joint_path",
    "main",
]
