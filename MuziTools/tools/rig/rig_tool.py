# coding=utf-8
u"""
Rig Tool
========

Maya 2023 / PySide2 绑定工具入口。

目标：
    - 常用 Rig 操作用 maya.cmds 直接实现；
    - FK / Controller / Skirt 等复杂功能交给独立子工具；
    - 不在窗口启动阶段一次性导入大量旧 core 模块；
    - 避免一个可选依赖报错导致整个 Rig Tool 无法打开。
"""

from __future__ import print_function

import math

import maya.cmds as cmds

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout
from PySide2.QtWidgets import QGroupBox
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QScrollArea
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget

from ....core import qtUtils
from ..ctrl import create_ctrl_tool
from ..ctrl import create_fk_ctrl_tool
from ..joint import joint_tool
from . import skirt_ctrl_tool


_window = None


def _short_name(node):
    return node.split("|")[-1]


def _joint_path(start_joint, end_joint):
    """返回 start -> end 的关节路径。"""
    if start_joint == end_joint:
        return [start_joint]

    def walk(joint, path):
        children = cmds.listRelatives(
            joint,
            children=True,
            type="joint",
            fullPath=True
        ) or []

        for child in children:
            child_path = list(path)
            child_path.append(child)

            if child == end_joint:
                return child_path

            result = walk(child, child_path)
            if result:
                return result

        return None

    return walk(start_joint, [start_joint])


def _vector_sub(a, b):
    return [
        a[0] - b[0],
        a[1] - b[1],
        a[2] - b[2],
    ]


def _vector_add(a, b):
    return [
        a[0] + b[0],
        a[1] + b[1],
        a[2] + b[2],
    ]


def _vector_mul(vector, value):
    return [
        vector[0] * value,
        vector[1] * value,
        vector[2] * value,
    ]


def _vector_length(vector):
    return math.sqrt(
        vector[0] * vector[0]
        + vector[1] * vector[1]
        + vector[2] * vector[2]
    )


def _vector_normalize(vector):
    length = _vector_length(vector)
    if length <= 0.000001:
        return [0.0, 0.0, 0.0]

    return [
        vector[0] / length,
        vector[1] / length,
        vector[2] / length,
    ]


def _dot(a, b):
    return (
        a[0] * b[0]
        + a[1] * b[1]
        + a[2] * b[2]
    )


def _pole_vector_position(start_joint, middle_joint, end_joint):
    start_pos = cmds.xform(
        start_joint,
        query=True,
        worldSpace=True,
        translation=True
    )
    middle_pos = cmds.xform(
        middle_joint,
        query=True,
        worldSpace=True,
        translation=True
    )
    end_pos = cmds.xform(
        end_joint,
        query=True,
        worldSpace=True,
        translation=True
    )

    start_to_end = _vector_sub(end_pos, start_pos)
    start_to_middle = _vector_sub(middle_pos, start_pos)

    line_length = _vector_length(start_to_end)
    if line_length <= 0.000001:
        return middle_pos

    line_direction = _vector_normalize(start_to_end)
    projection_length = _dot(start_to_middle, line_direction)
    projection = _vector_add(
        start_pos,
        _vector_mul(line_direction, projection_length)
    )

    pole_direction = _vector_sub(middle_pos, projection)
    pole_direction = _vector_normalize(pole_direction)

    if _vector_length(pole_direction) <= 0.000001:
        pole_direction = [0.0, 0.0, 1.0]

    chain_length = (
        _vector_length(_vector_sub(middle_pos, start_pos))
        + _vector_length(_vector_sub(end_pos, middle_pos))
    )

    return _vector_add(
        middle_pos,
        _vector_mul(pole_direction, chain_length * 0.75)
    )


def create_ik_rig(start_joint, end_joint):
    """创建一个基础 RP IK + End Ctrl + Pole Vector Ctrl。"""
    if not cmds.objExists(start_joint):
        raise RuntimeError(u"IK 起始关节不存在：{}".format(start_joint))

    if not cmds.objExists(end_joint):
        raise RuntimeError(u"IK 末端关节不存在：{}".format(end_joint))

    path = _joint_path(start_joint, end_joint)
    if not path or len(path) < 2:
        raise RuntimeError(u"起始关节和末端关节不在同一条子关节链上。")

    base_name = _short_name(start_joint)
    if base_name.startswith("jnt_"):
        base_name = base_name[4:]

    rig_group_name = "rig_ik_{}_grp".format(base_name)
    if cmds.objExists(rig_group_name):
        raise RuntimeError(u"IK Rig 已存在：{}".format(rig_group_name))

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

    ik_handle_name = "ikh_{}".format(base_name)
    ik_handle, effector = cmds.ikHandle(
        startJoint=start_joint,
        endEffector=end_joint,
        solver="ikRPsolver",
        name=ik_handle_name
    )
    cmds.parent(ik_handle, rig_group)

    start_pos = cmds.xform(
        start_joint,
        query=True,
        worldSpace=True,
        translation=True
    )
    end_pos = cmds.xform(
        end_joint,
        query=True,
        worldSpace=True,
        translation=True
    )
    chain_size = _vector_length(_vector_sub(end_pos, start_pos))
    control_radius = max(chain_size * 0.15, 0.5)

    end_control_result = create_ctrl_tool.create_controller(
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
    cmds.parent(end_control_result["top_group"], rig_group)

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

    if len(path) >= 3:
        middle_index = int(len(path) / 2)
        middle_joint = path[middle_index]
        pole_position = _pole_vector_position(
            start_joint,
            middle_joint,
            end_joint
        )

        pole_result = create_ctrl_tool.create_controller(
            name="ctrl_{}_pv".format(base_name),
            shape="circle",
            radius=max(control_radius * 0.65, 0.3),
            axis="Y+",
            target=middle_joint,
            color=17,
            create_sub_control=False,
            create_extra_groups=True,
            add_to_set=True
        )
        pole_control = pole_result["control"]
        cmds.xform(
            pole_result["top_group"],
            worldSpace=True,
            translation=pole_position
        )
        cmds.parent(pole_result["top_group"], rig_group)
        cmds.poleVectorConstraint(pole_control, ik_handle)

    cmds.setAttr(ik_handle + ".visibility", 0)

    return {
        "group": rig_group,
        "ik_handle": ik_handle,
        "effector": effector,
        "end_control": end_control,
        "pole_control": pole_control,
    }


def _find_rig_root(node):
    current = node

    while current:
        if cmds.attributeQuery(
                "muziRigType",
                node=current,
                exists=True
        ):
            return current

        parents = cmds.listRelatives(
            current,
            parent=True,
            fullPath=True
        ) or []

        if not parents:
            break

        current = parents[0]

    return None


class RigTool(QWidget):
    """Rig 主工具面板。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = qtUtils.get_maya_window()

        super(RigTool, self).__init__(parent)
        self.setWindowTitle(u"Rig Tool - 木子绑定工具")
        self.resize(480, 720)

        self._create_widgets()
        self._create_layouts()
        self._create_connections()

    def _create_widgets(self):
        self.create_fk_btn = QPushButton(u"按选择创建 FK")
        self.open_control_creator_btn = QPushButton(u"打开控制器创建工具")
        self.open_joint_tool_btn = QPushButton(u"打开 Joint Tool")

        self.ik_start_line = QLineEdit()
        self.ik_start_line.setReadOnly(True)
        self.ik_start_pick_btn = QPushButton(u"拾取起始 Joint")

        self.ik_end_line = QLineEdit()
        self.ik_end_line.setReadOnly(True)
        self.ik_end_pick_btn = QPushButton(u"拾取末端 Joint")

        self.create_ik_btn = QPushButton(u"创建 RP IK Rig")
        self.delete_rig_btn = QPushButton(u"删除所选 Rig 模块")

        self.clear_keys_btn = QPushButton(u"删除关键帧")
        self.reset_attrs_btn = QPushButton(u"重置可动画属性")
        self.batch_constraint_btn = QPushButton(u"按顺序批量父子约束")
        self.create_default_groups_btn = QPushButton(u"创建默认绑定层级")
        self.add_zero_group_btn = QPushButton(u"为选择对象添加 Zero 组")
        self.select_children_btn = QPushButton(u"选择全部子物体")
        self.snap_btn = QPushButton(u"最后物体吸附到前面中心")
        self.print_duplicates_btn = QPushButton(u"检查重名节点")
        self.rename_duplicates_btn = QPushButton(u"重命名重复节点")
        self.skirt_tool_btn = QPushButton(u"裙子控制器工具")

    def _create_layouts(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(6, 6, 6, 6)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)

        fk_group = QGroupBox(u"FK / Controller")
        fk_layout = QGridLayout(fk_group)
        fk_layout.addWidget(self.create_fk_btn, 0, 0)
        fk_layout.addWidget(self.open_control_creator_btn, 0, 1)
        fk_layout.addWidget(self.open_joint_tool_btn, 1, 0, 1, 2)

        ik_group = QGroupBox(u"IK")
        ik_layout = QGridLayout(ik_group)
        ik_layout.addWidget(QLabel(u"起始:"), 0, 0)
        ik_layout.addWidget(self.ik_start_line, 0, 1)
        ik_layout.addWidget(self.ik_start_pick_btn, 0, 2)
        ik_layout.addWidget(QLabel(u"末端:"), 1, 0)
        ik_layout.addWidget(self.ik_end_line, 1, 1)
        ik_layout.addWidget(self.ik_end_pick_btn, 1, 2)
        ik_layout.addWidget(self.create_ik_btn, 2, 0, 1, 2)
        ik_layout.addWidget(self.delete_rig_btn, 2, 2)

        utility_group = QGroupBox(u"绑定小工具")
        utility_layout = QGridLayout(utility_group)
        utility_buttons = [
            self.clear_keys_btn,
            self.reset_attrs_btn,
            self.batch_constraint_btn,
            self.create_default_groups_btn,
            self.add_zero_group_btn,
            self.select_children_btn,
            self.snap_btn,
            self.print_duplicates_btn,
            self.rename_duplicates_btn,
            self.skirt_tool_btn,
        ]

        index = 0
        for button in utility_buttons:
            row = index // 2
            column = index % 2
            utility_layout.addWidget(button, row, column)
            index += 1

        content_layout.addWidget(fk_group)
        content_layout.addWidget(ik_group)
        content_layout.addWidget(utility_group)
        content_layout.addStretch(1)

        scroll.setWidget(content)
        root_layout.addWidget(scroll)

    def _create_connections(self):
        self.create_fk_btn.clicked.connect(create_fk_ctrl_tool.main)
        self.open_control_creator_btn.clicked.connect(create_ctrl_tool.main)
        self.open_joint_tool_btn.clicked.connect(joint_tool.main)

        self.ik_start_pick_btn.clicked.connect(
            lambda: self.pick_joint(self.ik_start_line)
        )
        self.ik_end_pick_btn.clicked.connect(
            lambda: self.pick_joint(self.ik_end_line)
        )
        self.create_ik_btn.clicked.connect(self.create_ik)
        self.delete_rig_btn.clicked.connect(self.delete_selected_rig)

        self.clear_keys_btn.clicked.connect(self.clear_keys)
        self.reset_attrs_btn.clicked.connect(self.reset_attributes)
        self.batch_constraint_btn.clicked.connect(self.batch_parent_constraint)
        self.create_default_groups_btn.clicked.connect(self.create_default_groups)
        self.add_zero_group_btn.clicked.connect(self.add_zero_groups)
        self.select_children_btn.clicked.connect(self.select_children)
        self.snap_btn.clicked.connect(self.snap_last_to_center)
        self.print_duplicates_btn.clicked.connect(self.print_duplicate_nodes)
        self.rename_duplicates_btn.clicked.connect(self.rename_duplicate_nodes)
        self.skirt_tool_btn.clicked.connect(skirt_ctrl_tool.main)

    @staticmethod
    def pick_joint(line_edit):
        joints = cmds.ls(selection=True, type="joint", long=True) or []
        if len(joints) != 1:
            cmds.warning(u"请只选择一个 Joint。")
            return

        line_edit.setText(joints[0])

    def create_ik(self):
        start_joint = self.ik_start_line.text().strip()
        end_joint = self.ik_end_line.text().strip()

        if not start_joint or not end_joint:
            cmds.warning(u"请先拾取 IK 起始和末端 Joint。")
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziCreateIkRig")
        try:
            result = create_ik_rig(start_joint, end_joint)
            cmds.select(result["group"], replace=True)
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    @staticmethod
    def delete_selected_rig():
        selections = cmds.ls(selection=True, long=True) or []
        if not selections:
            cmds.warning(u"请选择 Rig 模块组或模块中的节点。")
            return

        rig_roots = []
        for node in selections:
            rig_root = _find_rig_root(node)
            if rig_root and rig_root not in rig_roots:
                rig_roots.append(rig_root)

        if not rig_roots:
            cmds.warning(u"选择中未找到带 muziRigType 的 Rig 模块。")
            return

        cmds.delete(rig_roots)

    @staticmethod
    def clear_keys():
        selections = cmds.ls(selection=True, long=True) or []

        if selections:
            cmds.cutKey(selections, clear=True)
            return

        anim_curve_types = [
            "animCurveTA",
            "animCurveTL",
            "animCurveTT",
            "animCurveTU",
        ]
        anim_curves = []

        for node_type in anim_curve_types:
            nodes = cmds.ls(type=node_type) or []
            for node in nodes:
                anim_curves.append(node)

        if anim_curves:
            cmds.delete(anim_curves)

    @staticmethod
    def reset_attributes():
        selections = cmds.ls(selection=True, long=True) or []
        if not selections:
            cmds.warning(u"请先选择需要重置的对象。")
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziResetAttrs")
        try:
            for node in selections:
                attrs = cmds.listAttr(node, keyable=True) or []

                for attr in attrs:
                    plug = "{}.{}".format(node, attr)

                    if not cmds.getAttr(plug, settable=True):
                        continue

                    source = cmds.listConnections(
                        plug,
                        source=True,
                        destination=False,
                        plugs=True
                    ) or []

                    if source:
                        continue

                    defaults = cmds.attributeQuery(
                        attr,
                        node=node,
                        listDefault=True
                    )

                    if defaults:
                        try:
                            cmds.setAttr(plug, defaults[0])
                        except Exception:
                            pass
        finally:
            cmds.undoInfo(closeChunk=True)

    @staticmethod
    def batch_parent_constraint():
        selections = cmds.ls(selection=True, long=True) or []
        if len(selections) < 2 or len(selections) % 2 != 0:
            cmds.warning(
                u"请按 driver1, driven1, driver2, driven2... 顺序选择偶数个对象。"
            )
            return

        index = 0
        while index < len(selections):
            cmds.parentConstraint(
                selections[index],
                selections[index + 1],
                maintainOffset=True
            )
            index += 2

    @staticmethod
    def create_default_groups():
        group_names = [
            "rig_grp",
            "geo_grp",
            "skeleton_grp",
            "controls_grp",
            "noTouch_grp",
        ]

        created = {}
        for group_name in group_names:
            if cmds.objExists(group_name):
                created[group_name] = group_name
            else:
                created[group_name] = cmds.createNode(
                    "transform",
                    name=group_name
                )

        children = [
            created["geo_grp"],
            created["skeleton_grp"],
            created["controls_grp"],
            created["noTouch_grp"],
        ]

        for child in children:
            parents = cmds.listRelatives(child, parent=True) or []
            if not parents:
                cmds.parent(child, created["rig_grp"])

        cmds.setAttr(created["noTouch_grp"] + ".visibility", 0)
        cmds.select(created["rig_grp"], replace=True)

    @staticmethod
    def add_zero_groups():
        selections = cmds.ls(selection=True, long=True) or []
        if not selections:
            cmds.warning(u"请先选择需要添加 Zero 组的对象。")
            return

        created_groups = []

        for node in selections:
            short_name = _short_name(node)
            zero_name = "zero_{}".format(short_name)

            if short_name.startswith("ctrl_"):
                zero_name = short_name.replace("ctrl_", "zero_", 1)

            if cmds.objExists(zero_name):
                cmds.warning(u"Zero 组已存在，跳过：{}".format(zero_name))
                continue

            parent = cmds.listRelatives(
                node,
                parent=True,
                fullPath=True
            ) or []

            zero_group = cmds.createNode("transform", name=zero_name)
            cmds.matchTransform(
                zero_group,
                node,
                position=True,
                rotation=True,
                scale=True
            )

            if parent:
                cmds.parent(zero_group, parent[0])

            cmds.parent(node, zero_group)
            created_groups.append(zero_group)

        if created_groups:
            cmds.select(created_groups, replace=True)

    @staticmethod
    def select_children():
        selections = cmds.ls(selection=True, long=True) or []
        if not selections:
            cmds.warning(u"请先选择父对象。")
            return

        result = []
        for node in selections:
            descendants = cmds.listRelatives(
                node,
                allDescendents=True,
                fullPath=True
            ) or []

            for descendant in descendants:
                if descendant not in result:
                    result.append(descendant)

        if result:
            cmds.select(result, replace=True)

    @staticmethod
    def snap_last_to_center():
        selections = cmds.ls(selection=True, long=True) or []
        if len(selections) < 2:
            cmds.warning(u"至少选择两个对象，最后一个作为被吸附对象。")
            return

        references = selections[:-1]
        target = selections[-1]
        position_total = [0.0, 0.0, 0.0]
        rotation_total = [0.0, 0.0, 0.0]

        for reference in references:
            position = cmds.xform(
                reference,
                query=True,
                worldSpace=True,
                translation=True
            )
            rotation = cmds.xform(
                reference,
                query=True,
                worldSpace=True,
                rotation=True
            )

            axis = 0
            while axis < 3:
                position_total[axis] += position[axis]
                rotation_total[axis] += rotation[axis]
                axis += 1

        count = float(len(references))
        center_position = []
        center_rotation = []
        axis = 0
        while axis < 3:
            center_position.append(position_total[axis] / count)
            center_rotation.append(rotation_total[axis] / count)
            axis += 1

        cmds.xform(
            target,
            worldSpace=True,
            translation=center_position,
            rotation=center_rotation
        )

    @staticmethod
    def _duplicate_map():
        nodes = cmds.ls(long=True) or []
        name_map = {}

        for node in nodes:
            short_name = _short_name(node)
            if short_name not in name_map:
                name_map[short_name] = []
            name_map[short_name].append(node)

        duplicates = {}
        for short_name in name_map:
            matches = name_map[short_name]
            if len(matches) > 1:
                duplicates[short_name] = matches

        return duplicates

    @classmethod
    def print_duplicate_nodes(cls):
        duplicates = cls._duplicate_map()
        if not duplicates:
            print(u"[Rig Tool] 场景中没有重名节点。")
            return

        print(u"[Rig Tool] 重名节点：")
        for short_name in sorted(duplicates.keys()):
            print(u"  {}".format(short_name))
            for node in duplicates[short_name]:
                print(u"    {}".format(node))

    @classmethod
    def rename_duplicate_nodes(cls):
        duplicates = cls._duplicate_map()
        if not duplicates:
            print(u"[Rig Tool] 场景中没有重名节点。")
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziRenameDuplicates")
        try:
            for short_name in sorted(duplicates.keys()):
                matches = duplicates[short_name]
                index = 1

                while index < len(matches):
                    node = matches[index]
                    new_name = "{}_{:03d}".format(
                        short_name,
                        index
                    )

                    while cmds.objExists(new_name):
                        index += 1
                        new_name = "{}_{:03d}".format(
                            short_name,
                            index
                        )

                    try:
                        cmds.rename(node, new_name)
                    except Exception as error:
                        cmds.warning(str(error))

                    index += 1
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

    _window = RigTool()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window
