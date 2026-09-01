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
    - DAG Parent / Parent Group 统一调用 core.hierarchy_utils；
    - Joint 类型检查统一调用 core.joint_utils；
    - DAG Short / Long Name 统一调用 core.rename_utils / scene_utils；
    - Selection / Node 创建 / Undo 统一调用 core.scene_utils；
    - World Position 统一调用 core.transform_utils；
    - Controller 创建统一调用 systems.controller；
    - Snap 算法统一调用 core.snap_utils；
    - 子窗口统一交给 app.window_manager；
    - 本文件只保留 Rig Tool UI、RP IK / Pole Vector 业务和少量工作流组装。
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
from ...core import animation_utils
from ...core import constraint_utils
from ...core import hierarchy_utils
from ...core import joint_utils
from ...core import rename_utils
from ...core import scene_utils
from ...core import snap_utils
from ...core import transform_utils
from ...systems import controller as controller_system
from ...ui import theme
from ...ui import window_utils
from ...ui.widgets import MayaObjectPicker
from ..controller import create_ctrl_tool
from ..controller import create_fk_ctrl_tool
from ..joint import joint_tool
from . import skirt_ctrl_tool


# =============================================================================
# IK Math
# =============================================================================

def vector_subtract(vector_a, vector_b):
    u"""
    三维向量相减。

    Args:
        vector_a (list[float] | tuple[float, float, float]):
            第一个 XYZ Vector。
        vector_b (list[float] | tuple[float, float, float]):
            第二个 XYZ Vector。

    Returns:
        list[float]:
        vector_a - vector_b。
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
        vector_a (list[float] | tuple[float, float, float]):
            第一个 XYZ Vector。
        vector_b (list[float] | tuple[float, float, float]):
            第二个 XYZ Vector。

    Returns:
        list[float]:
        vector_a + vector_b。
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
        vector (list[float] | tuple[float, float, float]):
            XYZ Vector。
        value (float):
            标量。

    Returns:
        list[float]:
        缩放后的 Vector。
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
        vector (list[float] | tuple[float, float, float]):
            XYZ Vector。

    Returns:
        float:
        欧氏长度。
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
        vector (list[float] | tuple[float, float, float]):
            XYZ Vector。

    Returns:
        list[float]:
        单位向量；零长度时返回 [0, 0, 0]。
    """
    length = vector_length(
        vector
    )

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
        vector_a (list[float] | tuple[float, float, float]):
            第一个 XYZ Vector。
        vector_b (list[float] | tuple[float, float, float]):
            第二个 XYZ Vector。

    Returns:
        float:
        Dot Product。
    """
    return (
        vector_a[0] * vector_b[0]
        + vector_a[1] * vector_b[1]
        + vector_a[2] * vector_b[2]
    )


# =============================================================================
# IK Workflow
# =============================================================================

def get_joint_path(start_joint, end_joint):
    u"""
    返回 start_joint 到 end_joint 的 Joint 路径。

    Args:
        start_joint (str):
            起始 Joint。
        end_joint (str):
            末端 Joint。

    Returns:
        list[str] | None:
        从 Start 到 End 的 Joint Path；不存在时返回 None。
    """
    try:
        # 使用 Scene Core 把两端解析成唯一 DAG Long Path。
        start_joint = scene_utils.get_long_name(
            start_joint
        )
        end_joint = scene_utils.get_long_name(
            end_joint
        )
    except RuntimeError:
        return None

    if start_joint == end_joint:
        return [
            start_joint
        ]

    def walk(current_joint, current_path):
        # 使用 Hierarchy Core 获取当前 Joint 的直接 Child Joint。
        children = hierarchy_utils.get_children(
            current_joint,
            node_type="joint",
            full_path=True
        )

        for child_joint in children:
            child_path = []

            for path_joint in current_path:
                child_path.append(
                    path_joint
                )

            child_path.append(
                child_joint
            )

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
        start_joint (str):
            起始 Joint。
        middle_joint (str):
            中间 Joint。
        end_joint (str):
            末端 Joint。

    Returns:
        list[float]:
        推荐 Pole Vector 世界位置。
    """
    # 使用 Transform Core 读取三段 Joint 的世界位置。
    start_position = transform_utils.get_world_translation(
        start_joint
    )
    middle_position = transform_utils.get_world_translation(
        middle_joint
    )
    end_position = transform_utils.get_world_translation(
        end_joint
    )

    start_to_end = vector_subtract(
        end_position,
        start_position
    )
    start_to_middle = vector_subtract(
        middle_position,
        start_position
    )

    line_length = vector_length(
        start_to_end
    )

    if line_length <= 0.000001:
        return middle_position

    # 计算 Middle 在 Start -> End 直线上的投影点。
    line_direction = vector_normalize(
        start_to_end
    )
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

    # Middle 到投影点的方向就是 Pole Vector 方向。
    pole_direction = vector_subtract(
        middle_position,
        projection
    )
    pole_direction = vector_normalize(
        pole_direction
    )

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


@scene_utils.undo_chunk
def create_ik_rig(start_joint, end_joint):
    u"""
    创建基础 RP IK、End Controller 和 Pole Vector Controller。

    Args:
        start_joint (str):
            IK Chain 起始 Joint。
        end_joint (str):
            IK Chain 末端 Joint。

    Returns:
        dict:
        Rig Group、IK Handle、Effector、End Controller 和 Pole Controller。

    Raises:
        RuntimeError:
        输入 Joint 无效、Chain 不连续或 Rig 已存在时抛出。
    """
    # 使用 Joint Core 做领域类型检查。
    joint_utils.Joint(
        start_joint
    )
    joint_utils.Joint(
        end_joint
    )

    # 使用 Scene Core 解析唯一 DAG Long Path。
    start_joint = scene_utils.get_long_name(
        start_joint
    )
    end_joint = scene_utils.get_long_name(
        end_joint
    )

    # 解析 Start -> End 的连续 Joint Path。
    joint_path = get_joint_path(
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

    # 使用统一 Short Name API 生成当前 IK Module 名称。
    base_name = rename_utils.get_short_name(
        start_joint
    )

    if base_name.startswith("jnt_"):
        base_name = base_name[4:]

    rig_group_name = "rig_ik_{}_grp".format(
        base_name
    )

    if cmds.objExists(rig_group_name):
        raise RuntimeError(
            u"IK Rig 已存在：{}".format(
                rig_group_name
            )
        )

    # 使用 Scene Core 创建 IK Module Root。
    rig_group = scene_utils.create_node(
        "transform",
        rig_group_name
    )

    # muziRigType 是 Rig Module 的业务标记，因此由 Rig Tool 设置。
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

    # 创建 Maya RP IK Handle；IK Solver 本身属于当前 Rig Workflow。
    ik_handle_result = cmds.ikHandle(
        startJoint=start_joint,
        endEffector=end_joint,
        solver="ikRPsolver",
        name="ikh_{}".format(
            base_name
        )
    )

    ik_handle = ik_handle_result[0]
    effector = ik_handle_result[1]

    # 把 IK Handle 收进当前 Rig Module Root。
    ik_handle = hierarchy_utils.parent(
        ik_handle,
        rig_group
    )

    # 根据 IK Chain 世界长度计算 Controller 大小。
    start_position = transform_utils.get_world_translation(
        start_joint
    )
    end_position = transform_utils.get_world_translation(
        end_joint
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

    # 使用统一 Controller System 创建 IK End Controller。
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

    # 把 End Controller 顶层组收进当前 IK Module。
    end_top_group = hierarchy_utils.parent(
        end_top_group,
        rig_group
    )

    # End Controller 位置驱动 IK Handle。
    constraint_utils.create_constraint(
        driver_objects=end_control,
        driven_object=ik_handle,
        constraint_type="pointConstraint",
        maintain_offset=False
    )

    # End Controller 旋转驱动末端 Joint。
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

        # 根据 Joint Chain 几何关系计算稳定的 Pole Vector 推荐位置。
        pole_position = get_pole_vector_position(
            start_joint,
            middle_joint,
            end_joint
        )

        # 使用统一 Controller System 创建 Pole Vector Controller。
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

        # 把 Pole Controller 顶层组移动到计算得到的世界位置。
        transform_utils.set_world_translation(
            pole_top_group,
            pole_position
        )

        # 把 Pole Controller 收进当前 IK Module。
        pole_top_group = hierarchy_utils.parent(
            pole_top_group,
            rig_group
        )

        # 使用 Constraint Core 创建 Pole Vector Constraint。
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
            Rig Module 内任意 DAG 节点。

    Returns:
        str | None:
        Rig Module Root；找不到时返回 None。
    """
    try:
        # 使用 Scene Core 解析起始节点唯一 Long Path。
        current_node = scene_utils.get_long_name(
            node
        )
    except RuntimeError:
        return None

    while current_node:
        if cmds.attributeQuery(
                "muziRigType",
                node=current_node,
                exists=True
        ):
            return current_node

        # 使用 Hierarchy Core 向上查询直接 Parent。
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
        short_name -> Long Path List，仅包含重名项。
    """
    nodes = cmds.ls(
        long=True,
        dagObjects=True
    ) or []

    name_map = {}

    for node in nodes:
        # 使用 Rename Core 统一解析 DAG Short Name。
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
    """通用 Rig 主工具面板。"""

    def __init__(self, parent=None):
        u"""
        创建 Rig Tool 窗口。

        Args:
            parent (QWidget | None):
                Qt 父窗口。
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
            tool_key (str):
                Window Manager 唯一 Key。
            tool_module (module):
                已加载 Tool Module。

        Returns:
            object:
            Tool main() 返回值。
        """
        # 使用应用层统一 Window Manager 打开子工具。
        return window_manager.show_tool(
            "rig/{}".format(tool_key),
            tool_module.main
        )

    def open_fk_tool(self):
        u"""
        打开 FK Controller Tool。

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
        打开 Controller Creator。

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
        打开 Joint Tool。

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
        打开 Skirt Rig Tool。

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
            cmds.warning(
                u"请先拾取 IK 起始和末端 Joint。"
            )
            return

        try:
            # 调用参数化 IK Workflow；Undo 已由 create_ik_rig 统一管理。
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
            # 向上寻找当前选择所属 Rig Module Root。
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

        # 使用 Animation Core 统一删除目标 AnimCurve。
        animation_utils.clear_animation_keys(
            nodes=target_nodes
        )

    @staticmethod
    @scene_utils.undo_chunk
    def reset_attributes():
        u"""
        把选择对象可设置的 Keyable Attribute 恢复 Attribute Default。

        这里保留“所有 Keyable Attribute”语义，因为它比
        animation_utils.reset_transform_channels() 的标准 TRS Reset 更宽。
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

            # 使用 Constraint Core 创建当前 Driver -> Driven Parent Constraint。
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

        # 新 Group 通过 Hierarchy Core 创建；已有 Group 保留当前层级，避免工具擅自搬动用户节点。
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

            # 只处理当前还没有 Parent 的 Group，保持旧工具安全语义。
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
            # 使用 Rename Core 统一取得当前节点 Short Name。
            short_name = rename_utils.get_short_name(
                node
            )

            if short_name.startswith("ctrl_"):
                zero_name = short_name.replace(
                    "ctrl_",
                    "zero_",
                    1
                )
            else:
                zero_name = "zero_{}".format(
                    short_name
                )

            if cmds.objExists(zero_name):
                cmds.warning(
                    u"Zero Group 已存在，跳过：{}".format(
                        zero_name
                    )
                )
                continue

            # 使用 Hierarchy Core 插入 Zero Group，并保持原世界姿态 / Parent。
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

        # 当前操作需要所有 DAG 类型，不限制 Transform / Joint，因此直接使用 Maya DAG 查询。
        for node in selections:
            descendants = cmds.listRelatives(
                node,
                allDescendents=True,
                fullPath=True
            ) or []

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
            # 使用 Snap Core 计算参考对象平均位置 / 旋转并应用到 Target。
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

            # 保留第一个同名节点，只给后续重复项追加编号。
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
                    cmds.warning(
                        str(error)
                    )

                match_index += 1


def main():
    u"""
    显示并返回 Rig Tool。

    Returns:
        QWidget:
        Rig Tool 窗口。
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
