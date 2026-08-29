# coding=utf-8
u"""
约束工具
========

功能：
    1. 父子约束
    2. 点约束
    3. 方向约束
    4. 缩放约束
    5. 目标约束
    6. 极向量约束
    7. 选择物体关联的约束节点
    8. 删除物体关联的约束节点

约束模式：
    多对一：
        前面的选择物体作为驱动者，最后一个选择物体作为被驱动者。

    一对多：
        第一个选择物体作为驱动者，其余选择物体作为被驱动者。

说明：
    - Maya 2023 优先使用 PySide2。
    - Maya 场景操作统一使用 maya.cmds。
    - main() 只创建并返回 QWidget，由 window_manager 统一管理窗口。
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


class ConstraintTool(QWidget):
    """Maya 常用约束工具窗口。"""

    def __init__(self, parent=None):
        super(ConstraintTool, self).__init__(parent)

        self.window_name = "ConstraintTool"
        self.window_title = u"Constraint Tool（约束工具）"

        self.setWindowTitle(self.window_title)
        self.setMinimumWidth(360)

        self.constraint_types = [
            "parentConstraint",
            "pointConstraint",
            "orientConstraint",
            "scaleConstraint",
            "aimConstraint",
            "poleVectorConstraint",
        ]

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    # -------------------------------------------------------------------------
    # 创建界面
    # -------------------------------------------------------------------------

    def create_widgets(self):
        """创建窗口中使用的所有部件。"""

        self.title_label = QLabel(
            u"---------------- 约束工具 ----------------"
        )
        self.title_label.setStyleSheet(
            u"color: rgb(169, 255, 175);"
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

        self.parent_constraint_button = QPushButton(
            QIcon(":parentConstraint.png"),
            u"父子约束"
        )
        self.point_constraint_button = QPushButton(
            QIcon(":posConstraint.png"),
            u"点约束"
        )
        self.orient_constraint_button = QPushButton(
            QIcon(":orientConstraint.png"),
            u"方向约束"
        )
        self.scale_constraint_button = QPushButton(
            QIcon(":scaleConstraint.png"),
            u"缩放约束"
        )
        self.aim_constraint_button = QPushButton(
            QIcon(":aimConstraint.png"),
            u"目标约束"
        )
        self.pole_vector_constraint_button = QPushButton(
            QIcon(":poleVectorConstraint.png"),
            u"极向量约束"
        )

        self.select_constraint_button = QPushButton(
            QIcon(":menuIconModify.png"),
            u"选择约束"
        )
        self.select_constraint_button.setToolTip(
            u"选择当前物体关联的所有约束节点"
        )

        self.delete_constraint_button = QPushButton(
            QIcon(":delete.png"),
            u"删除约束"
        )
        self.delete_constraint_button.setToolTip(
            u"删除当前物体关联的所有约束节点"
        )

        self.constraint_buttons = [
            self.parent_constraint_button,
            self.point_constraint_button,
            self.orient_constraint_button,
            self.scale_constraint_button,
            self.aim_constraint_button,
            self.pole_vector_constraint_button,
            self.select_constraint_button,
            self.delete_constraint_button,
        ]

    def create_layouts(self):
        """创建窗口布局。"""

        self.mode_layout = QHBoxLayout()
        self.mode_layout.addWidget(self.mult_to_one_radio)
        self.mode_layout.addWidget(self.one_to_mult_radio)
        self.mode_layout.addStretch()
        self.mode_layout.addWidget(self.maintain_offset_checkbox)

        self.constraint_layout = QGridLayout()

        row = 0
        column = 0

        for button in self.constraint_buttons:
            self.constraint_layout.addWidget(
                button,
                row,
                column
            )

            column += 1

            if column >= 2:
                column = 0
                row += 1

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.mode_layout)
        self.main_layout.addLayout(self.constraint_layout)
        self.main_layout.addStretch()

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

    # -------------------------------------------------------------------------
    # 选择数据
    # -------------------------------------------------------------------------

    def get_driver_and_driven_objects(self):
        """
        根据当前约束模式，把 Maya 选择拆分成驱动者和被驱动者。

        Returns:
            tuple:
                driver_objects (list)
                driven_objects (list)
        """

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

    # -------------------------------------------------------------------------
    # 创建约束
    # -------------------------------------------------------------------------

    def create_standard_constraint(self, constraint_command, chunk_name):
        """
        创建支持多目标的标准约束。

        parent / point / orient / scale / aim 的选择逻辑完全一致，
        因此只把共同流程集中在这里；具体按钮仍然保留独立函数，便于阅读。
        """

        driver_objects, driven_objects = self.get_driver_and_driven_objects()

        if not driver_objects or not driven_objects:
            return

        maintain_offset = self.maintain_offset_checkbox.isChecked()

        cmds.undoInfo(
            openChunk=True,
            chunkName=chunk_name
        )

        try:
            for driven_object in driven_objects:
                try:
                    constraint_command(
                        driver_objects,
                        driven_object,
                        maintainOffset=maintain_offset
                    )
                except RuntimeError as error:
                    cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    def clicked_parent_constraint_button(self):
        """创建父子约束。"""
        self.create_standard_constraint(
            cmds.parentConstraint,
            "MuziParentConstraint"
        )

    def clicked_point_constraint_button(self):
        """创建点约束。"""
        self.create_standard_constraint(
            cmds.pointConstraint,
            "MuziPointConstraint"
        )

    def clicked_orient_constraint_button(self):
        """创建方向约束。"""
        self.create_standard_constraint(
            cmds.orientConstraint,
            "MuziOrientConstraint"
        )

    def clicked_scale_constraint_button(self):
        """创建缩放约束。"""
        self.create_standard_constraint(
            cmds.scaleConstraint,
            "MuziScaleConstraint"
        )

    def clicked_aim_constraint_button(self):
        """
        创建目标约束。

        旧工具这里调用 performAimConstraint MEL，导致它不遵循工具中的
        多对一 / 一对多和保持偏移选项。现在统一使用 maya.cmds.aimConstraint。
        """
        self.create_standard_constraint(
            cmds.aimConstraint,
            "MuziAimConstraint"
        )

    def clicked_pole_vector_constraint_button(self):
        """创建极向量约束。极向量约束要求恰好选择两个物体。"""

        selected_objects = cmds.ls(
            selection=True,
            long=True
        )

        if selected_objects is None:
            selected_objects = []

        if len(selected_objects) != 2:
            cmds.warning(
                u"极向量约束需要恰好选择两个物体：控制器 -> IK Handle。"
            )
            return

        driver_object = selected_objects[0]
        ik_handle = selected_objects[1]

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziPoleVectorConstraint"
        )

        try:
            cmds.poleVectorConstraint(
                driver_object,
                ik_handle
            )
        except RuntimeError as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    # -------------------------------------------------------------------------
    # 查询约束
    # -------------------------------------------------------------------------

    def get_constraints_from_objects(self, selected_objects):
        """收集选择物体关联的约束节点，并保持稳定顺序去重。"""

        constraint_nodes = []

        for selected_object in selected_objects:
            for constraint_type in self.constraint_types:
                connected_nodes = cmds.listConnections(
                    selected_object,
                    type=constraint_type
                )

                if connected_nodes is None:
                    connected_nodes = []

                for connected_node in connected_nodes:
                    if connected_node in constraint_nodes:
                        continue

                    constraint_nodes.append(connected_node)

        return constraint_nodes

    def clicked_select_constraint_button(self):
        """选择当前选择物体关联的所有约束节点。"""

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

        print(
            u"[ConstraintTool] 已选择 {} 个约束节点。".format(
                len(constraint_nodes)
            )
        )

    def clicked_delete_constraint_button(self):
        """删除当前选择物体关联的所有约束节点。"""

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

        deleted_count = 0

        try:
            for constraint_node in constraint_nodes:
                if not cmds.objExists(constraint_node):
                    continue

                cmds.delete(constraint_node)
                deleted_count += 1
        finally:
            cmds.undoInfo(closeChunk=True)

        print(
            u"[ConstraintTool] 已删除 {} 个约束节点。".format(
                deleted_count
            )
        )


# 旧类名兼容。
Constraint_Tool = ConstraintTool


def main():
    """创建约束工具并返回 QWidget。"""
    window = ConstraintTool()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
