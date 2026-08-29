# coding=utf-8
u"""
约束工具
========

功能：
    - Parent / Point / Orient / Scale / Aim / Pole Vector Constraint；
    - 多对一 / 一对多选择模式；
    - 查询和删除关联约束节点。

结构：
    UI 只负责选择模式、按钮事件和反馈；
    Maya Constraint 场景操作统一由 core.constraint_utils 负责。
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
from ...ui import theme as ui_theme


class ConstraintTool(QWidget):
    """Maya 常用约束工具窗口。"""

    def __init__(self, parent=None):
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
        """创建窗口中使用的所有部件。"""
        self.title_label = ui_theme.make_title(u"约束工具")
        self.subtitle_label = ui_theme.make_subtitle(
            u"统一创建常用 Constraint，并管理选择对象已有的约束节点。"
        )

        self.mult_to_one_radio = QRadioButton(u"多对一")
        self.mult_to_one_radio.setToolTip(
            u"前面的选择物体驱动最后一个选择物体"
        )
        self.mult_to_one_radio.setChecked(True)

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
            u"选择关联约束"
        )
        self.delete_constraint_button = QPushButton(
            QIcon(":delete.png"),
            u"删除关联约束"
        )
        ui_theme.style_danger(self.delete_constraint_button)

    def create_layouts(self):
        """创建 Card 布局。"""
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
            u"对当前选择对象查询或删除已连接的 Constraint 节点。"
        )
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
        main_layout.addStretch(1)

    def create_connections(self):
        """连接所有按钮事件。"""
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
        """根据当前模式拆分 Driver / Driven。"""
        selected_objects = cmds.ls(
            selection=True,
            long=True
        )

        if selected_objects is None:
            selected_objects = []

        if len(selected_objects) < 2:
            cmds.warning(u"请至少选择两个物体。")
            return [], []

        driver_objects = []
        driven_objects = []

        if self.mult_to_one_radio.isChecked():
            last_index = len(selected_objects) - 1
            index = 0

            while index < last_index:
                driver_objects.append(
                    selected_objects[index]
                )
                index += 1

            driven_objects.append(
                selected_objects[-1]
            )
        else:
            driver_objects.append(
                selected_objects[0]
            )

            index = 1
            while index < len(selected_objects):
                driven_objects.append(
                    selected_objects[index]
                )
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
        """收集 UI 参数并调用 Core 创建标准约束。"""
        driver_objects, driven_objects = self.get_driver_and_driven_objects()

        if not driver_objects or not driven_objects:
            return

        maintain_offset = self.maintain_offset_checkbox.isChecked()

        cmds.undoInfo(
            openChunk=True,
            chunkName=chunk_name
        )

        try:
            constraint_utils.create_constraints(
                driver_objects=driver_objects,
                driven_objects=driven_objects,
                constraint_type=constraint_type,
                maintain_offset=maintain_offset
            )
        except RuntimeError as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(
                closeChunk=True
            )

    def clicked_parent_constraint_button(self):
        self.create_standard_constraint(
            "parentConstraint",
            "MuziParentConstraint"
        )

    def clicked_point_constraint_button(self):
        self.create_standard_constraint(
            "pointConstraint",
            "MuziPointConstraint"
        )

    def clicked_orient_constraint_button(self):
        self.create_standard_constraint(
            "orientConstraint",
            "MuziOrientConstraint"
        )

    def clicked_scale_constraint_button(self):
        self.create_standard_constraint(
            "scaleConstraint",
            "MuziScaleConstraint"
        )

    def clicked_aim_constraint_button(self):
        self.create_standard_constraint(
            "aimConstraint",
            "MuziAimConstraint"
        )

    def clicked_pole_vector_constraint_button(self):
        """创建 Pole Vector Constraint。"""
        selected_objects = cmds.ls(
            selection=True,
            long=True
        )

        if selected_objects is None:
            selected_objects = []

        if len(selected_objects) != 2:
            cmds.warning(
                u"Pole Vector 需要恰好选择两个物体：控制器 -> IK Handle。"
            )
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziPoleVectorConstraint"
        )

        try:
            constraint_utils.create_pole_vector_constraint(
                driver_object=selected_objects[0],
                ik_handle=selected_objects[1]
            )
        except RuntimeError as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(
                closeChunk=True
            )

    # =========================================================================
    # Manage
    # =========================================================================

    @staticmethod
    def get_constraints_from_objects(selected_objects):
        """从 Core 查询对象关联的约束节点。"""
        return constraint_utils.get_constraints(
            selected_objects
        )

    def clicked_select_constraint_button(self):
        """选择当前对象关联的所有约束节点。"""
        selected_objects = cmds.ls(
            selection=True,
            long=True
        )

        if selected_objects is None:
            selected_objects = []

        if not selected_objects:
            cmds.warning(u"请先选择需要查询约束的物体。")
            return

        constraint_nodes = self.get_constraints_from_objects(
            selected_objects
        )

        if not constraint_nodes:
            cmds.warning(u"没有找到约束节点。")
            return

        cmds.select(
            constraint_nodes,
            replace=True
        )

    def clicked_delete_constraint_button(self):
        """删除当前对象关联的所有约束节点。"""
        selected_objects = cmds.ls(
            selection=True,
            long=True
        )

        if selected_objects is None:
            selected_objects = []

        if not selected_objects:
            cmds.warning(u"请先选择需要删除约束的物体。")
            return

        constraint_nodes = self.get_constraints_from_objects(
            selected_objects
        )

        if not constraint_nodes:
            cmds.warning(u"没有找到需要删除的约束节点。")
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziDeleteConstraints"
        )

        try:
            constraint_utils.delete_constraints(
                selected_objects
            )
        finally:
            cmds.undoInfo(
                closeChunk=True
            )


def main():
    """创建约束工具并返回 QWidget。"""
    window = ConstraintTool()
    return window


__all__ = [
    "ConstraintTool",
    "main",
]
