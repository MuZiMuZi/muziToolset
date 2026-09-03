# coding=utf-8
u"""
Constraint Tool
===============

Maya 常用约束工具窗口。

模块职责
--------
1. Parent / Point / Orient / Scale / Aim / Pole Vector Constraint；
2. 支持多对一 / 一对多 Selection 模式；
3. 查询和删除当前选择 Driven 对象上的 Constraint；
4. Selection、批量创建和删除决策由 Tool 负责，单个 Constraint 创建 / 查询复用 ``core.constraint_utils``；
5. 提供可在 Maya Script Editor 中直接显示的 ``main()``。

主要公开类型 / 方法
------------------
ConstraintTool
    约束工具主窗口。

ConstraintTool.get_driver_and_driven_objects()
    根据 UI 模式拆分 Driver / Driven。

ConstraintTool.create_standard_constraint(...)
    按 UI Selection Workflow 循环调用 Core 创建单个标准约束。

ConstraintTool.clicked_pole_vector_constraint_button()
    创建 Pole Vector Constraint。

ConstraintTool.clicked_select_constraint_button()
ConstraintTool.clicked_delete_constraint_button()
    查询 / 删除真正驱动当前选择对象的 Constraint。

main()
    创建或恢复窗口，立即显示并返回 QWidget。

直接运行
--------

    from muziToolset.tools.basic import constraint_tool

    window = constraint_tool.main()

设计边界
--------
本文件负责 Selection、批量 Workflow 和删除意图；
实际 Maya Constraint 创建与 Driven 侧查询统一复用 ``core.constraint_utils``。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QCheckBox
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QRadioButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import QCheckBox
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QRadioButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...core import constraint_utils
from ...core import scene_utils
from ...ui import theme as ui_theme
from ...ui import window_utils


class ConstraintTool(QWidget):
    """Maya 常用约束工具窗口。"""

    def __init__(self, parent=None):
        u"""
        初始化当前对象，并准备运行时需要的状态和成员。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        super(ConstraintTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        ui_theme.style_window(
            self,
            title=u"约束工具",
            minimum_width=520
        )
        self.resize(540, 460)

    # =========================================================================
    # UI
    # =========================================================================

    def create_widgets(self):
        u"""
        创建窗口中使用的所有部件。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.title_label = ui_theme.make_title(u"约束工具")
        self.subtitle_label = ui_theme.make_subtitle(
            u"统一创建常用 Constraint，并管理选择对象真正接收的约束节点。"
        )

        self.mult_to_one_radio = QRadioButton(u"多对一")
        self.mult_to_one_radio.setToolTip(
            u"前面的选择物体驱动最后一个选择物体"
        )
        self.mult_to_one_radio.setChecked(True)

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.one_to_mult_radio = QRadioButton(u"一对多")
        self.one_to_mult_radio.setToolTip(
            u"第一个选择物体驱动后面的所有选择物体"
        )

        self.maintain_offset_checkbox = QCheckBox(u"保持偏移")
        self.maintain_offset_checkbox.setChecked(True)

        self.mode_info_label = QLabel(
            u"多对一：前面选择作为 Driver，最后一个作为 Driven。\n"
            u"一对多：第一个作为 Driver，其余对象作为 Driven。"
        )
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.mode_info_label.setWordWrap(True)
        ui_theme.set_role(self.mode_info_label, "muted")

        self.parent_constraint_button = QPushButton(
            QIcon(":parentConstraint.png"),
            u"Parent"
        )
        self.point_constraint_button = QPushButton(
            QIcon(":posConstraint.png"),
            u"Point"
        )
        self.orient_constraint_button = QPushButton(
            QIcon(":orientConstraint.png"),
            u"Orient"
        )
        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.scale_constraint_button = QPushButton(
            QIcon(":scaleConstraint.png"),
            u"Scale"
        )
        self.aim_constraint_button = QPushButton(
            QIcon(":aimConstraint.png"),
            u"Aim"
        )
        self.pole_vector_constraint_button = QPushButton(
            QIcon(":poleVectorConstraint.png"),
            u"Pole Vector"
        )

        self.select_constraint_button = QPushButton(
            QIcon(":menuIconModify.png"),
            u"选择对象约束"
        )
        self.delete_constraint_button = QPushButton(
            QIcon(":delete.png"),
            u"删除对象约束"
        )
        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        ui_theme.style_danger(self.delete_constraint_button)

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

        mode_card, mode_layout = ui_theme.make_card(self)
        mode_layout.addWidget(
            ui_theme.make_section_title(u"选择模式")
        )
        mode_layout.addWidget(self.mode_info_label)

        mode_row = QHBoxLayout()
        mode_row.setContentsMargins(0, 0, 0, 0)
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        mode_row.addWidget(self.mult_to_one_radio)
        mode_row.addWidget(self.one_to_mult_radio)
        mode_row.addStretch(1)
        mode_row.addWidget(self.maintain_offset_checkbox)
        mode_layout.addLayout(mode_row)

        create_card, create_layout = ui_theme.make_card(self)
        create_layout.addWidget(
            ui_theme.make_section_title(u"创建约束")
        )

        constraint_grid = QGridLayout()
        constraint_grid.setHorizontalSpacing(8)
        constraint_grid.setVerticalSpacing(8)
        constraint_grid.addWidget(self.parent_constraint_button, 0, 0)
        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        constraint_grid.addWidget(self.point_constraint_button, 0, 1)
        constraint_grid.addWidget(self.orient_constraint_button, 0, 2)
        constraint_grid.addWidget(self.scale_constraint_button, 1, 0)
        constraint_grid.addWidget(self.aim_constraint_button, 1, 1)
        constraint_grid.addWidget(self.pole_vector_constraint_button, 1, 2)
        create_layout.addLayout(constraint_grid)

        manage_card, manage_layout = ui_theme.make_card(self)
        manage_layout.addWidget(
            ui_theme.make_section_title(u"约束管理")
        )

        manage_info_label = QLabel(
            u"只管理真正驱动当前选择对象的 Constraint；仅作为 Driver 的对象不会被匹配。"
        )
        manage_info_label.setWordWrap(True)
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        ui_theme.set_role(manage_info_label, "muted")
        manage_layout.addWidget(manage_info_label)

        manage_row = QHBoxLayout()
        manage_row.setContentsMargins(0, 0, 0, 0)
        manage_row.addWidget(self.select_constraint_button)
        manage_row.addWidget(self.delete_constraint_button)
        manage_layout.addLayout(manage_row)

        main_layout.addWidget(mode_card)
        main_layout.addWidget(create_card)
        main_layout.addWidget(manage_card)
        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        main_layout.addStretch(1)

    def create_connections(self):
        u"""
        连接所有按钮事件。
        """
        self.parent_constraint_button.clicked.connect(
            self.clicked_parent_constraint_button
        )
        self.point_constraint_button.clicked.connect(
            self.clicked_point_constraint_button
        )
        self.orient_constraint_button.clicked.connect(
            self.clicked_orient_constraint_button
        )
        self.scale_constraint_button.clicked.connect(
            self.clicked_scale_constraint_button
        )
        self.aim_constraint_button.clicked.connect(
            self.clicked_aim_constraint_button
        )
        self.pole_vector_constraint_button.clicked.connect(
            self.clicked_pole_vector_constraint_button
        )
        self.select_constraint_button.clicked.connect(
            self.clicked_select_constraint_button
        )
        self.delete_constraint_button.clicked.connect(
            self.clicked_delete_constraint_button
        )

    # =========================================================================
    # Selection
    # =========================================================================

    def get_driver_and_driven_objects(self):
        u"""
        根据当前模式拆分 Driver / Driven。

        Returns:
            tuple:
            按当前 API 约定组织的结果元组。
        """
        selected_objects = cmds.ls(
            selection=True,
            long=True
        ) or []

        if len(selected_objects) < 2:
            cmds.warning(u"请至少选择两个物体。")
            return [], []

        driver_objects = []
        driven_objects = []

        if self.mult_to_one_radio.isChecked():
            last_index = len(selected_objects) - 1
            index = 0

            while index < last_index:
                driver_objects.append(selected_objects[index])
                index += 1

            driven_objects.append(selected_objects[-1])
        else:
            driver_objects.append(selected_objects[0])

            index = 1

            while index < len(selected_objects):
                driven_objects.append(selected_objects[index])
                index += 1

        return driver_objects, driven_objects

    # =========================================================================
    # Create
    # =========================================================================

    def create_standard_constraint(
            self,
            constraint_type,
            chunk_name
    ):
        u"""
        收集 UI 参数并按 Driven 循环调用 Core 创建标准约束。

        Args:
            constraint_type (str):
                Maya Constraint 类型，例如 parentConstraint、pointConstraint、orientConstraint、scaleConstraint 或 aimConstraint。
            chunk_name (str):
                当前按钮操作使用的 Maya Undo Chunk 名称。
        """
        driver_objects, driven_objects = self.get_driver_and_driven_objects()

        if not driver_objects or not driven_objects:
            return

        maintain_offset = self.maintain_offset_checkbox.isChecked()

        scene_utils.open_undo_chunk(chunk_name)

        try:
            for driven_object in driven_objects:
                constraint_utils.create_constraint(
                    driver_objects=driver_objects,
                    driven_object=driven_object,
                    constraint_type=constraint_type,
                    maintain_offset=maintain_offset
                )
        except (RuntimeError, ValueError) as error:
            cmds.warning(str(error))
        finally:
            scene_utils.close_undo_chunk()

    def clicked_parent_constraint_button(self):
        u"""
        创建 Parent Constraint。
        """
        self.create_standard_constraint(
            "parentConstraint",
            "MuziParentConstraint"
        )

    def clicked_point_constraint_button(self):
        u"""
        创建 Point Constraint。
        """
        self.create_standard_constraint(
            "pointConstraint",
            "MuziPointConstraint"
        )

    def clicked_orient_constraint_button(self):
        u"""
        创建 Orient Constraint。
        """
        self.create_standard_constraint(
            "orientConstraint",
            "MuziOrientConstraint"
        )

    def clicked_scale_constraint_button(self):
        u"""
        创建 Scale Constraint。
        """
        self.create_standard_constraint(
            "scaleConstraint",
            "MuziScaleConstraint"
        )

    def clicked_aim_constraint_button(self):
        u"""
        创建 Aim Constraint。
        """
        self.create_standard_constraint(
            "aimConstraint",
            "MuziAimConstraint"
        )

    def clicked_pole_vector_constraint_button(self):
        u"""
        创建 Pole Vector Constraint。
        """
        selected_objects = cmds.ls(
            selection=True,
            long=True
        ) or []

        if len(selected_objects) != 2:
            cmds.warning(
                u"Pole Vector 需要恰好选择两个物体：控制器 -> IK Handle。"
            )
            return

        scene_utils.open_undo_chunk("MuziPoleVectorConstraint")

        try:
            constraint_utils.create_pole_vector_constraint(
                driver_object=selected_objects[0],
                ik_handle=selected_objects[1]
            )
        except RuntimeError as error:
            cmds.warning(str(error))
        finally:
            scene_utils.close_undo_chunk()

    # =========================================================================
    # Manage
    # =========================================================================

    @staticmethod
    def get_constraints_from_objects(selected_objects):
        u"""
        从 Core 查询真正驱动输入对象的 Constraint 节点。

        Args:
            selected_objects (str | list[str]):
                需要作为 Driven 查询 Constraint 的 Maya 节点。

        Returns:
            list[str]:
            真正向这些对象输出驱动结果的 Constraint 节点。
        """
        return constraint_utils.get_constraints(
            selected_objects
        )

    def clicked_select_constraint_button(self):
        u"""
        选择真正驱动当前选择对象的所有 Constraint 节点。
        """
        selected_objects = cmds.ls(
            selection=True,
            long=True
        ) or []

        if not selected_objects:
            cmds.warning(u"请先选择需要查询约束的 Driven 对象。")
            return

        constraint_nodes = self.get_constraints_from_objects(
            selected_objects
        )

        if not constraint_nodes:
            cmds.warning(u"没有找到驱动所选对象的 Constraint 节点。")
            return

        cmds.select(
            constraint_nodes,
            replace=True
        )

    def clicked_delete_constraint_button(self):
        u"""
        删除真正驱动当前选择对象的所有 Constraint 节点。
        """
        selected_objects = cmds.ls(
            selection=True,
            long=True
        ) or []

        if not selected_objects:
            cmds.warning(u"请先选择需要删除约束的 Driven 对象。")
            return

        constraint_nodes = self.get_constraints_from_objects(
            selected_objects
        )

        if not constraint_nodes:
            cmds.warning(u"没有找到需要删除的 Constraint 节点。")
            return

        scene_utils.open_undo_chunk("MuziDeleteConstraints")

        try:
            cmds.delete(
                constraint_nodes
            )
        finally:
            scene_utils.close_undo_chunk()


def main():
    u"""
    创建或恢复 Constraint Tool，立即显示并返回 QWidget。

    Returns:
        object:
        当前工具入口创建并显示的窗口或执行结果。
    """
    return window_utils.show_window(
        "tools.basic.constraint_tool",
        ConstraintTool
    )


__all__ = [
    "ConstraintTool",
    "main",
]
