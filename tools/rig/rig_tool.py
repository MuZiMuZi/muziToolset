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

架构边界：
    - Animation 清理统一调用 core.animation_utils；
    - Constraint 创建统一调用 core.constraint_utils；
    - DAG Parent / Descendant / Parent Group 统一调用 core.hierarchy_utils；
    - 单 Joint 能力统一调用 core.joint_utils；
    - Joint Chain 查询统一调用 core.joint_chain_utils；
    - Point / Vector Math 统一调用 core.math_utils；
    - DAG Short / Long Name 统一调用 core.rename_utils / scene_utils；
    - Selection / Node 创建 / Undo 统一调用 core.scene_utils；
    - World Position 统一调用 core.transform_utils；
    - Rig Naming 统一调用 systems.rig_base.RigBase；
    - Controller 创建统一调用 systems.ctrl_base；
    - Snap 算法统一调用 core.snap_utils；
    - 子窗口统一交给 app.window_manager；
    - 本文件只保留 Rig Tool UI、RP IK / Pole Vector 业务和工作流组装。
"""

from __future__ import print_function

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
from ...core import animation_utils
from ...core import attr_utils
from ...core import constraint_utils
from ...core import hierarchy_utils
from ...core import joint_chain_utils
from ...core import joint_utils
from ...core import math_utils
from ...core import rename_utils
from ...core import scene_utils
from ...core import snap_utils
from ...core import transform_utils
from ...systems import ctrl_base
from ...systems.rig_base import RigBase
from ...ui import theme
from ...ui import window_utils
from ...ui.widgets import MayaObjectPicker
from ..controller import create_ctrl_tool
from ..controller import create_fk_ctrl_tool
from ..joint import joint_tool
from . import skirt_ctrl_tool


# =============================================================================
# IK Workflow
# =============================================================================

def get_pole_vector_position(
        start_joint,
        middle_joint,
        end_joint
):
    u"""
    计算三关节链 Pole Vector 推荐世界位置。

    Args:
        start_joint (str):
            RP IK Chain 的起始 Joint。
        middle_joint (str):
            RP IK Chain 中用于确定弯曲平面的中间 Joint。
        end_joint (str):
            RP IK Chain 的末端 Joint。

    Returns:
        list:
        推荐的 Pole Vector 世界坐标 [x, y, z]。
    """
    start_position = transform_utils.get_world_translation(
        start_joint
    )
    middle_position = transform_utils.get_world_translation(
        middle_joint
    )
    end_position = transform_utils.get_world_translation(
        end_joint
    )

    start_to_end = math_utils.subtract_vector3(
        end_position,
        start_position
    )
    start_to_middle = math_utils.subtract_vector3(
        middle_position,
        start_position
    )

    line_length = math_utils.length_vector3(
        start_to_end
    )

    if line_length <= 0.000001:
        return middle_position

    line_direction = math_utils.normalize_vector3(
        start_to_end
    )
    projection_length = math_utils.dot_vector3(
        start_to_middle,
        line_direction
    )
    projection = math_utils.add_vector3(
        start_position,
        math_utils.multiply_vector3(
            line_direction,
            projection_length
        )
    )

    pole_direction = math_utils.subtract_vector3(
        middle_position,
        projection
    )
    pole_direction = math_utils.normalize_vector3(
        pole_direction
    )

    if math_utils.length_vector3(pole_direction) <= 0.000001:
        pole_direction = [
            0.0,
            0.0,
            1.0,
        ]

    start_segment_length = math_utils.distance_between_points(
        start_position,
        middle_position
    )
    end_segment_length = math_utils.distance_between_points(
        middle_position,
        end_position
    )
    chain_length = start_segment_length + end_segment_length

    return math_utils.add_vector3(
        middle_position,
        math_utils.multiply_vector3(
            pole_direction,
            chain_length * 0.75
        )
    )


@scene_utils.undo_chunk
def create_ik_rig(start_joint, end_joint):
    u"""
    创建基础 RP IK、End Controller 和 Pole Vector Controller。

    Args:
        start_joint (str):
            RP IK Chain 的起始 Joint。
        end_joint (str):
            RP IK Chain 的末端 Joint。

    Returns:
        dict:
        返回 Rig Group、IK Handle、Effector、End Controller 和可选 Pole Controller。

    Raises:
        RuntimeError:
        Joint 输入无效、两端不属于同一子 Joint Chain 或 Chain 长度不足时抛出。
    """
    joint_utils.Joint(
        start_joint
    )
    joint_utils.Joint(
        end_joint
    )

    start_joint = scene_utils.get_long_name(
        start_joint
    )
    end_joint = scene_utils.get_long_name(
        end_joint
    )

    joint_path = joint_chain_utils.get_joint_path(
        start_joint,
        end_joint
    )

    if not joint_path:
        raise RuntimeError(
            u"起始 Joint 和末端 Joint 不在同一条子 Joint Chain 上。"
        )

    if len(joint_path) < 2:
        raise RuntimeError(
            u"RP IK 至少需要两个 Joint。"
        )

    start_joint_short_name = rename_utils.get_short_name(
        start_joint
    )
    rig_side = "md"
    rig_part_source = start_joint_short_name

    try:
        start_joint_name = RigBase(
            name=start_joint_short_name
        )

        if start_joint_name.part:
            rig_side = start_joint_name.side
            rig_part_source = start_joint_name.part
    except (IndexError, TypeError, ValueError):
        if rig_part_source.startswith("jnt_"):
            rig_part_source = rig_part_source[4:]

    rig_part = rename_utils.get_name_token(
        rig_part_source,
        fallback="ik"
    )

    rig_identity = RigBase(
        side=rig_side,
        part=rig_part,
        index=1
    )

    rig_group_name = rig_identity.create_name(
        type="grp",
        function="ik"
    )
    ik_handle_name = rig_identity.create_name(
        type="ikh",
        function="ik"
    )
    end_control_name = rig_identity.create_name(
        type="ctrl",
        function="ik"
    )
    pole_control_name = rig_identity.create_name(
        type="ctrl",
        function="pv"
    )

    scene_utils.ensure_nodes_available(
        [
            rig_group_name,
            ik_handle_name,
        ],
        label=u"IK Rig 节点"
    )

    rig_group = scene_utils.create_node(
        "transform",
        rig_group_name
    )

    rig_group_attrs = attr_utils.Attr(
        rig_group
    )
    rig_group_attrs.set_value(
        "muziRigType",
        "ik",
        attr_type="string",
        lock=False,
        keyable=False,
        channel_box=False
    )

    ik_handle_result = cmds.ikHandle(
        startJoint=start_joint,
        endEffector=end_joint,
        solver="ikRPsolver",
        name=ik_handle_name
    )

    ik_handle = ik_handle_result[0]
    effector = ik_handle_result[1]
    ik_handle = hierarchy_utils.parent(
        ik_handle,
        rig_group
    )

    start_position = transform_utils.get_world_translation(
        start_joint
    )
    end_position = transform_utils.get_world_translation(
        end_joint
    )
    chain_size = math_utils.distance_between_points(
        start_position,
        end_position
    )
    control_radius = max(
        chain_size * 0.15,
        0.5
    )

    end_control_result = ctrl_base.create_ctrl(
        name=end_control_name,
        shape="circle",
        radius=control_radius,
        axis="Y+",
        target_node=end_joint,
        parent_node=rig_group,
        color=17,
        create_sub_ctrl=False,
        add_to_set=True
    )

    end_control = end_control_result["ctrl_node"]

    constraint_utils.create_constraint(
        driver_objects=end_control,
        driven_object=ik_handle,
        constraint_type="pointConstraint",
        maintain_offset=False
    )
    constraint_utils.create_constraint(
        driver_objects=end_control,
        driven_object=end_joint,
        constraint_type="orientConstraint",
        maintain_offset=True
    )

    pole_control = None

    if len(joint_path) >= 3:
        middle_index = int(
            len(joint_path) / 2
        )
        middle_joint = joint_path[middle_index]
        pole_position = get_pole_vector_position(
            start_joint,
            middle_joint,
            end_joint
        )

        pole_result = ctrl_base.create_ctrl(
            name=pole_control_name,
            shape="circle",
            radius=max(
                control_radius * 0.65,
                0.3
            ),
            axis="Y+",
            target_node=middle_joint,
            parent_node=rig_group,
            color=17,
            create_sub_ctrl=False,
            add_to_set=True
        )

        pole_control = pole_result["ctrl_node"]
        pole_top_group = pole_result["top_grp"]

        transform_utils.set_world_translation(
            pole_top_group,
            pole_position
        )
        constraint_utils.create_pole_vector_constraint(
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


# =============================================================================
# Rig Module / Scene Query
# =============================================================================

def find_rig_root(node):
    u"""
    沿父层级查找带 muziRigType 的 Rig Module Root。

    Args:
        node (str):
            需要向上查询所属 Rig Module 的 Maya Node。

    Returns:
        str | None:
        找到时返回 Rig Module Root；没有标记节点时返回 None。
    """
    try:
        current_node = scene_utils.get_long_name(
            node
        )
    except RuntimeError:
        return None

    while current_node:
        node_attrs = attr_utils.Attr(
            current_node
        )

        if node_attrs.attr_exists(
                "muziRigType"
        ):
            return current_node

        current_node = hierarchy_utils.get_parent(
            current_node,
            full_path=True
        )

    return None


def get_duplicate_map():
    u"""
    按短名称收集场景重名 DAG 节点。

    Returns:
        dict:
        Key 为重复 Short Name，Value 为对应的 Long DAG Path 列表。
    """
    nodes = cmds.ls(
        long=True,
        dagObjects=True
    ) or []

    name_map = {}

    for node in nodes:
        short_name = rename_utils.get_short_name(
            node
        )

        if short_name not in name_map:
            name_map[short_name] = []

        name_map[short_name].append(
            node
        )

    duplicates = {}

    for short_name in name_map:
        matches = name_map[short_name]

        if len(matches) > 1:
            duplicates[short_name] = matches

    return duplicates


# =============================================================================
# UI
# =============================================================================

class RigTool(QWidget):
    u"""通用 Rig 主工具面板。"""

    def __init__(self, parent=None):
        u"""
        初始化 Rig Tool 窗口及其控件、布局和信号连接。

        Args:
            parent (QWidget | None):
                可选 Qt Parent Widget。
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
        self.resize(
            640,
            760
        )

    def create_widgets(self):
        u"""
        创建界面控件。
        """
        self.title_label = theme.make_title(
            u"Rig 工具"
        )
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
        theme.style_primary(
            self.create_ik_button
        )

        self.delete_rig_button = QPushButton(u"删除选择 Rig Module")
        theme.style_danger(
            self.delete_rig_button
        )

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
        root_layout = QVBoxLayout(
            self
        )
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

        utility_layout.addLayout(
            utility_grid
        )

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
        self.create_fk_button.clicked.connect(self.open_fk_tool)
        self.open_control_creator_button.clicked.connect(self.open_control_creator)
        self.open_joint_tool_button.clicked.connect(self.open_joint_tool)
        self.open_skirt_tool_button.clicked.connect(self.open_skirt_tool)
        self.create_ik_button.clicked.connect(self.create_ik)
        self.delete_rig_button.clicked.connect(self.delete_selected_rig)
        self.clear_keys_button.clicked.connect(self.clear_keys)
        self.reset_attrs_button.clicked.connect(self.reset_attributes)
        self.batch_constraint_button.clicked.connect(self.batch_parent_constraint)
        self.create_default_groups_button.clicked.connect(self.create_default_groups)
        self.add_zero_group_button.clicked.connect(self.add_zero_groups)
        self.select_children_button.clicked.connect(self.select_children)
        self.snap_button.clicked.connect(self.snap_last_to_center)
        self.print_duplicates_button.clicked.connect(self.print_duplicate_nodes)
        self.rename_duplicates_button.clicked.connect(self.rename_duplicate_nodes)

    @staticmethod
    def open_tool(tool_key, tool_module):
        u"""
        通过统一 Window Manager 执行或打开专项工具。

        Args:
            tool_key (str):
                Window Manager 使用的 Rig Tool Key。
            tool_module (object):
                提供 main() 入口的 Tool Module。

        Returns:
            object:
            Window Manager 返回的 Tool 执行结果或窗口对象。
        """
        return window_manager.show_tool(
            "rig/{}".format(tool_key),
            tool_module.main
        )

    def open_fk_tool(self):
        u"""
        打开 FK Controller Tool。

        Returns:
            object:
            Window Manager 返回的 FK Controller Tool 窗口或执行结果。
        """
        return self.open_tool(
            "fk_controller",
            create_fk_ctrl_tool
        )

    def open_control_creator(self):
        u"""
        打开 Controller Creator。

        Returns:
            object:
            Window Manager 返回的 Controller Creator 窗口或执行结果。
        """
        return self.open_tool(
            "controller_creator",
            create_ctrl_tool
        )

    def open_joint_tool(self):
        u"""
        打开 Joint Tool。

        Returns:
            object:
            Window Manager 返回的 Joint Tool 窗口或执行结果。
        """
        return self.open_tool(
            "joint_tool",
            joint_tool
        )

    def open_skirt_tool(self):
        u"""
        打开 Skirt Rig Tool。

        Returns:
            object:
            Window Manager 返回的 Skirt Rig Tool 窗口或执行结果。
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
            cmds.warning(
                u"请先拾取 IK 起始和末端 Joint。"
            )
            return

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
            cmds.warning(
                str(error)
            )

    @staticmethod
    def delete_selected_rig():
        u"""
        删除选择节点所属的 Muzi Rig Module。
        """
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )
        rig_roots = []

        for node in selections:
            rig_root = find_rig_root(
                node
            )

            if not rig_root:
                continue

            if rig_root in rig_roots:
                continue

            rig_roots.append(
                rig_root
            )

        if not rig_roots:
            cmds.warning(
                u"选择中未找到带 muziRigType 的 Rig Module。"
            )
            return

        cmds.delete(
            rig_roots
        )

    @staticmethod
    def clear_keys():
        u"""
        删除选择对象关键帧；没有选择时清理场景 AnimCurve。
        """
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )
        target_nodes = selections

        if not target_nodes:
            target_nodes = None

        animation_utils.clear_animation_keys(
            nodes=target_nodes
        )

    @staticmethod
    @scene_utils.undo_chunk
    def reset_attributes():
        u"""
        把选择对象可设置的 Keyable Attribute 恢复 Attribute Default。
        """
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        if not selections:
            cmds.warning(
                u"请先选择需要重置的对象。"
            )
            return

        for node in selections:
            attrs = cmds.listAttr(
                node,
                keyable=True
            ) or []

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

    @staticmethod
    @scene_utils.undo_chunk
    def batch_parent_constraint():
        u"""
        按 driver/driven 成对顺序批量创建 Parent Constraint。
        """
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        if len(selections) < 2:
            cmds.warning(
                u"请按 driver1, driven1, driver2, driven2... 顺序选择偶数个对象。"
            )
            return

        if len(selections) % 2 != 0:
            cmds.warning(
                u"请按 driver1, driven1, driver2, driven2... 顺序选择偶数个对象。"
            )
            return

        selection_index = 0

        while selection_index < len(selections):
            driver = selections[selection_index]
            driven = selections[selection_index + 1]

            constraint_utils.create_constraint(
                driver_objects=driver,
                driven_object=driven,
                constraint_type="parentConstraint",
                maintain_offset=True
            )

            selection_index += 2

    @staticmethod
    @scene_utils.undo_chunk
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
                created_groups[group_name] = scene_utils.get_long_name(
                    group_name
                )
                continue

            created_groups[group_name] = hierarchy_utils.ensure_group(
                group_name
            )

        child_names = [
            "geo_grp",
            "skeleton_grp",
            "controls_grp",
            "noTouch_grp",
        ]

        for child_name in child_names:
            child_group = created_groups[child_name]
            parent_node = hierarchy_utils.get_parent(
                child_group,
                full_path=True
            )

            if parent_node is not None:
                continue

            child_group = hierarchy_utils.parent(
                child_group,
                created_groups["rig_grp"]
            )
            created_groups[child_name] = child_group

        cmds.setAttr(
            created_groups["noTouch_grp"] + ".visibility",
            0
        )
        cmds.select(
            created_groups["rig_grp"],
            replace=True
        )

    @staticmethod
    @scene_utils.undo_chunk
    def add_zero_groups():
        u"""
        为选择对象创建匹配 Transform 的 Zero Group。
        """
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        if not selections:
            cmds.warning(
                u"请先选择需要添加 Zero Group 的对象。"
            )
            return

        created_groups = []

        for node in selections:
            short_name = rename_utils.get_short_name(
                node
            )
            zero_name = None

            try:
                rig_name = RigBase(
                    name=short_name
                )

                if rig_name.name:
                    zero_name = rig_name.create_name(
                        type="zero"
                    )
            except (IndexError, TypeError, ValueError):
                pass

            if not zero_name:
                zero_name = "zero_{}".format(
                    rename_utils.get_name_token(
                        short_name,
                        fallback="node"
                    )
                )

            if cmds.objExists(zero_name):
                cmds.warning(
                    u"Zero Group 已存在，跳过：{}".format(
                        zero_name
                    )
                )
                continue

            zero_group = hierarchy_utils.insert_parent_group(
                node=node,
                group_name=zero_name,
                match_rotation=True
            )
            created_groups.append(
                zero_group
            )

        if created_groups:
            cmds.select(
                created_groups,
                replace=True
            )

    @staticmethod
    def select_children():
        u"""
        选择当前对象全部后代 DAG 节点。
        """
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        if not selections:
            cmds.warning(
                u"请先选择父对象。"
            )
            return

        result = []

        for node in selections:
            descendants = hierarchy_utils.get_descendants(
                node,
                full_path=True
            )

            for descendant in descendants:
                if descendant in result:
                    continue

                result.append(
                    descendant
                )

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
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        if len(selections) < 2:
            cmds.warning(
                u"至少选择两个对象，最后一个作为被吸附对象。"
            )
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
            cmds.warning(
                str(error)
            )

    @staticmethod
    def print_duplicate_nodes():
        u"""
        打印重名 DAG 节点。
        """
        duplicates = get_duplicate_map()

        if not duplicates:
            print(
                u"[Rig Tool] 场景中没有重名 DAG 节点。"
            )
            return

        short_names = []

        for short_name in duplicates:
            short_names.append(
                short_name
            )

        short_names.sort()

        print(
            u"[Rig Tool] 重名 DAG 节点："
        )

        for short_name in short_names:
            print(
                u"  {}".format(
                    short_name
                )
            )

            for node in duplicates[short_name]:
                print(
                    u"    {}".format(
                        node
                    )
                )

    @staticmethod
    @scene_utils.undo_chunk
    def rename_duplicate_nodes():
        u"""
        给重名 DAG 节点追加递增编号。
        """
        duplicates = get_duplicate_map()

        if not duplicates:
            print(
                u"[Rig Tool] 场景中没有重名 DAG 节点。"
            )
            return

        short_names = []

        for short_name in duplicates:
            short_names.append(
                short_name
            )

        short_names.sort()

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

                rename_utils.rename_node(
                    node,
                    new_name
                )
                match_index += 1


def main():
    u"""
    显示并返回 Rig Tool。

    Returns:
        QWidget:
        当前显示的 Rig Tool 窗口实例。
    """
    return window_utils.show_window(
        "tools.rig.rig_tool",
        RigTool
    )


__all__ = [
    "RigTool",
    "create_ik_rig",
    "get_pole_vector_position",
    "find_rig_root",
    "main",
]
