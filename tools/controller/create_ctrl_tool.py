# coding=utf-8
u"""
Control Creator
===============

控制器创建工具 UI。

模块职责
--------
1. 浏览 ``resources/controller_shapes`` 中的 Controller Shape；
2. 设置名称、大小、轴向、颜色和创建模式；
3. 把用户参数交给 ``systems.controller``；
4. 提供可以从 Maya Script Editor 直接调用的 ``main()`` 窗口入口；
5. 不在 UI 文件里重复维护 Controller 创建算法或窗口生命周期算法。

主要公开 API
------------
ControlCreatorDialog
    Controller Creator 的 PySide 主窗口。

main()
    创建或恢复 Control Creator 窗口，立即显示，并返回 QWidget。

直接运行示例
------------
在 Maya Python Script Editor 中：

    from muziToolset.tools.controller import create_ctrl_tool

    window = create_ctrl_tool.main()

窗口生命周期
------------
``main()`` 统一使用 ``ui.window_utils`` 保存强引用、恢复最小化窗口并激活已有实例。
主工具箱继续由 ``app.window_manager`` 负责应用级 Parent、Window Flags 和跨工具窗口管理。
"""

from __future__ import print_function

import os

import maya.cmds as cmds

try:
    from PySide2.QtCore import QSize
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QColor
    from PySide2.QtGui import QIcon
    from PySide2.QtGui import QPixmap
    from PySide2.QtWidgets import QCheckBox
    from PySide2.QtWidgets import QComboBox
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QDoubleSpinBox
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QListView
    from PySide2.QtWidgets import QListWidget
    from PySide2.QtWidgets import QListWidgetItem
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QSpinBox
    from PySide2.QtWidgets import QVBoxLayout
except ImportError:
    from PySide6.QtCore import QSize
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QColor
    from PySide6.QtGui import QIcon
    from PySide6.QtGui import QPixmap
    from PySide6.QtWidgets import QCheckBox
    from PySide6.QtWidgets import QComboBox
    from PySide6.QtWidgets import QDialog
    from PySide6.QtWidgets import QDoubleSpinBox
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QListView
    from PySide6.QtWidgets import QListWidget
    from PySide6.QtWidgets import QListWidgetItem
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QSpinBox
    from PySide6.QtWidgets import QVBoxLayout

from ...config import controller_shapes_dir
from ...systems import controller as controller_system
from ...ui import theme
from ...ui import window_utils


maya_colors = {
    0: (0.467, 0.467, 0.467),
    1: (0.000, 0.000, 0.000),
    2: (0.200, 0.200, 0.200),
    3: (0.600, 0.600, 0.600),
    4: (0.800, 0.000, 0.000),
    5: (0.000, 0.000, 0.400),
    6: (0.000, 0.000, 1.000),
    7: (0.000, 0.400, 0.000),
    8: (0.200, 0.000, 0.400),
    9: (0.800, 0.400, 0.000),
    10: (0.600, 0.400, 0.200),
    11: (0.400, 0.200, 0.000),
    12: (1.000, 1.000, 0.000),
    13: (1.000, 0.000, 0.000),
    14: (0.000, 1.000, 0.000),
    15: (0.000, 1.000, 1.000),
    16: (1.000, 1.000, 1.000),
    17: (1.000, 1.000, 0.000),
    18: (0.000, 0.800, 1.000),
    19: (1.000, 0.600, 0.800),
    20: (1.000, 0.400, 0.400),
    21: (0.600, 1.000, 0.400),
    22: (1.000, 0.800, 0.400),
    23: (0.400, 0.600, 1.000),
    24: (1.000, 1.000, 1.000),
    25: (1.000, 1.000, 0.800),
    26: (0.800, 1.000, 0.800),
    27: (0.800, 1.000, 1.000),
    28: (1.000, 0.800, 1.000),
    29: (1.000, 0.600, 0.600),
    30: (0.800, 1.000, 0.600),
    31: (0.600, 0.800, 1.000),
}


axis_list = [
    "X+",
    "X-",
    "Y+",
    "Y-",
    "Z+",
    "Z-",
]


class ControlCreatorDialog(QDialog):
    """控制器创建窗口。"""

    def __init__(self, parent=None):
        super(ControlCreatorDialog, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.refresh_shape_library()
        self.update_color_preview()

        theme.style_window(
            self,
            title=u"Control Creator",
            minimum_width=620
        )
        self.resize(660, 780)

    # -------------------------------------------------------------------------
    # UI
    # -------------------------------------------------------------------------

    def create_widgets(self):
        """创建界面控件。"""
        self.title_label = theme.make_title(u"创建控制器")
        self.subtitle_label = theme.make_subtitle(
            u"统一使用 Controller System 创建标准绑定控制器和层级。"
        )

        self.shape_search_line = QLineEdit()
        self.shape_search_line.setPlaceholderText(u"搜索 Shape...")
        theme.style_search(self.shape_search_line)

        self.shape_list = QListWidget()
        self.shape_list.setViewMode(QListWidget.IconMode)
        self.shape_list.setResizeMode(QListWidget.Adjust)
        self.shape_list.setMovement(QListWidget.Static)
        self.shape_list.setSelectionMode(QListWidget.SingleSelection)
        self.shape_list.setIconSize(QSize(72, 72))
        self.shape_list.setGridSize(QSize(132, 118))
        self.shape_list.setSpacing(4)
        self.shape_list.setMinimumHeight(310)
        self.shape_list.setWordWrap(True)
        self.shape_list.setUniformItemSizes(True)
        self.shape_list.setWrapping(True)
        self.shape_list.setFlow(QListView.LeftToRight)

        self.radius_spin = QDoubleSpinBox()
        self.radius_spin.setDecimals(3)
        self.radius_spin.setRange(0.001, 10000.0)
        self.radius_spin.setValue(2.0)
        self.radius_spin.setSingleStep(0.1)

        self.axis_combo = QComboBox()

        for axis in axis_list:
            self.axis_combo.addItem(axis)

        self.axis_combo.setCurrentText("Y+")

        self.rotate_x_spin = QDoubleSpinBox()
        self.rotate_x_spin.setDecimals(2)
        self.rotate_x_spin.setRange(-3600.0, 3600.0)
        self.rotate_x_spin.setValue(0.0)
        self.rotate_x_spin.setSingleStep(5.0)

        self.create_mode_combo = QComboBox()
        self.create_mode_combo.addItem(u"选择物体", "selection")
        self.create_mode_combo.addItem(u"选择层级", "hierarchy")
        self.create_mode_combo.addItem(u"世界原点", "world")

        self.color_spin = QSpinBox()
        self.color_spin.setRange(0, 31)
        self.color_spin.setValue(6)

        self.color_preview = QLabel()
        self.color_preview.setFixedSize(32, 32)

        self.name_line = QLineEdit()
        self.name_line.setPlaceholderText(
            u"留空时根据目标名称自动生成 ctrl_*"
        )

        self.create_sub_checkbox = QCheckBox(u"创建次级控制器")
        self.create_sub_checkbox.setChecked(True)

        self.create_groups_checkbox = QCheckBox(u"创建标准层级组")
        self.create_groups_checkbox.setChecked(True)

        self.add_set_checkbox = QCheckBox(u"加入 ctrl_set")
        self.add_set_checkbox.setChecked(True)

        self.refresh_button = QPushButton(u"刷新 Shape 图库")
        theme.style_ghost(self.refresh_button)

        self.create_button = QPushButton(u"创建控制器")
        theme.style_primary(self.create_button)

        self.status_label = QLabel(u"准备就绪")
        theme.set_role(self.status_label, "muted")

    def create_layouts(self):
        """创建窗口布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        shape_card, shape_layout = theme.make_card(self)
        shape_header_layout = QHBoxLayout()
        shape_header_layout.setContentsMargins(0, 0, 0, 0)
        shape_header_layout.addWidget(
            theme.make_section_title(u"Controller Shape")
        )
        shape_header_layout.addStretch(1)
        shape_header_layout.addWidget(self.refresh_button)
        shape_layout.addLayout(shape_header_layout)
        shape_layout.addWidget(self.shape_search_line)
        shape_layout.addWidget(self.shape_list)

        parameter_card, parameter_layout = theme.make_card(self)
        parameter_layout.addWidget(
            theme.make_section_title(u"创建参数")
        )

        parameter_grid = QGridLayout()
        parameter_grid.setHorizontalSpacing(12)
        parameter_grid.setVerticalSpacing(10)
        parameter_grid.addWidget(QLabel(u"大小"), 0, 0)
        parameter_grid.addWidget(self.radius_spin, 0, 1)
        parameter_grid.addWidget(QLabel(u"轴向"), 0, 2)
        parameter_grid.addWidget(self.axis_combo, 0, 3)
        parameter_grid.addWidget(QLabel(u"额外旋转 X"), 1, 0)
        parameter_grid.addWidget(self.rotate_x_spin, 1, 1)
        parameter_grid.addWidget(QLabel(u"创建模式"), 1, 2)
        parameter_grid.addWidget(self.create_mode_combo, 1, 3)
        parameter_grid.setColumnStretch(1, 1)
        parameter_grid.setColumnStretch(3, 1)
        parameter_layout.addLayout(parameter_grid)

        color_card, color_layout = theme.make_card(self)
        color_layout.addWidget(
            theme.make_section_title(u"颜色")
        )

        color_row = QHBoxLayout()
        color_row.setContentsMargins(0, 0, 0, 0)
        color_row.addWidget(QLabel(u"Maya Index Color"))
        color_row.addWidget(self.color_spin)
        color_row.addWidget(self.color_preview)
        color_row.addStretch(1)
        color_layout.addLayout(color_row)

        hierarchy_card, hierarchy_layout = theme.make_card(self)
        hierarchy_layout.addWidget(
            theme.make_section_title(u"命名与层级")
        )
        hierarchy_layout.addWidget(self.name_line)

        option_layout = QHBoxLayout()
        option_layout.setContentsMargins(0, 0, 0, 0)
        option_layout.addWidget(self.create_sub_checkbox)
        option_layout.addWidget(self.create_groups_checkbox)
        option_layout.addWidget(self.add_set_checkbox)
        hierarchy_layout.addLayout(option_layout)

        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.addWidget(self.status_label, 1)
        action_layout.addWidget(self.create_button)

        main_layout.addWidget(shape_card, 1)
        main_layout.addWidget(parameter_card)
        main_layout.addWidget(color_card)
        main_layout.addWidget(hierarchy_card)
        main_layout.addLayout(action_layout)

    def create_connections(self):
        """连接 UI 信号。"""
        self.shape_search_line.textChanged.connect(
            self.filter_shape_library
        )
        self.refresh_button.clicked.connect(
            self.refresh_shape_library
        )
        self.color_spin.valueChanged.connect(
            self.update_color_preview
        )
        self.create_button.clicked.connect(
            self.create_controls
        )

    # -------------------------------------------------------------------------
    # Shape Library
    # -------------------------------------------------------------------------

    def refresh_shape_library(self):
        """重新读取正式 Controller Shape 资源目录。"""
        self.shape_list.clear()

        if not os.path.isdir(controller_shapes_dir):
            self.status_label.setText(u"Shape 资源目录不存在")
            return

        file_names = os.listdir(controller_shapes_dir)
        shape_names = []

        for file_name in file_names:
            shape_name, extension = os.path.splitext(file_name)

            if extension.lower() != ".json":
                continue

            if shape_name not in shape_names:
                shape_names.append(shape_name)

        shape_names.sort()

        for shape_name in shape_names:
            icon = QIcon()

            preview_extensions = [
                ".jpg",
                ".png",
            ]

            for extension in preview_extensions:
                preview_path = os.path.join(
                    controller_shapes_dir,
                    shape_name + extension
                )

                if not os.path.isfile(preview_path):
                    continue

                pixmap = QPixmap(preview_path)

                if not pixmap.isNull():
                    icon = QIcon(pixmap)

                break

            item = QListWidgetItem()
            item.setText(shape_name)
            item.setIcon(icon)
            item.setData(Qt.UserRole, shape_name)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignTop)
            item.setToolTip(shape_name)
            self.shape_list.addItem(item)

        if self.shape_list.count() > 0:
            self.shape_list.setCurrentRow(0)

        self.filter_shape_library(
            self.shape_search_line.text()
        )
        self.status_label.setText(
            u"已加载 {} 个 Shape".format(self.shape_list.count())
        )

    def filter_shape_library(self, text_value):
        """根据搜索文字过滤 Shape。"""
        search_text = text_value.strip().lower()
        index = 0

        while index < self.shape_list.count():
            item = self.shape_list.item(index)
            shape_name = item.text().lower()
            hidden = False

            if search_text:
                if search_text not in shape_name:
                    hidden = True

            item.setHidden(hidden)
            index += 1

    def selected_shape_name(self):
        """返回当前选中的 Shape 名称。"""
        selected_items = self.shape_list.selectedItems()

        if not selected_items:
            return None

        return selected_items[0].data(Qt.UserRole)

    # -------------------------------------------------------------------------
    # Color
    # -------------------------------------------------------------------------

    def update_color_preview(self):
        """刷新 Maya Index Color 预览块。"""
        color_index = self.color_spin.value()
        rgb = maya_colors.get(
            color_index,
            (0.5, 0.5, 0.5)
        )

        color = QColor.fromRgbF(
            rgb[0],
            rgb[1],
            rgb[2]
        )

        self.color_preview.setStyleSheet(
            u"background-color: {}; border: 1px solid #DADCE0; "
            u"border-radius: 6px;".format(color.name())
        )

    # -------------------------------------------------------------------------
    # Target
    # -------------------------------------------------------------------------

    def get_create_targets(self):
        """根据当前创建模式返回需要创建控制器的目标列表。"""
        mode = self.create_mode_combo.currentData()

        if mode == "world":
            return [None]

        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(u"当前创建模式需要先选择 Maya 对象。")
            return []

        if mode == "selection":
            return selections

        targets = []

        for root in selections:
            if root not in targets:
                targets.append(root)

            descendants = cmds.listRelatives(
                root,
                allDescendents=True,
                fullPath=True
            )

            if descendants is None:
                descendants = []

            descendants.reverse()

            for descendant in descendants:
                node_type = cmds.nodeType(descendant)

                if node_type not in [
                    "transform",
                    "joint",
                ]:
                    continue

                if descendant not in targets:
                    targets.append(descendant)

        return targets

    def get_control_name(self, target, target_index, target_count):
        """根据用户输入和目标生成最终控制器名称。"""
        custom_name = self.name_line.text().strip()

        if not custom_name:
            if target is None:
                return "ctrl_new_001"

            return controller_system.get_control_name_from_target(target)

        if target_count <= 1:
            return custom_name

        return "{}_{:03d}".format(
            custom_name,
            target_index + 1
        )

    # -------------------------------------------------------------------------
    # Create
    # -------------------------------------------------------------------------

    def create_controls(self):
        """根据 UI 参数调用 Controller System。"""
        shape_name = self.selected_shape_name()

        if not shape_name:
            cmds.warning(u"请先选择一个 Controller Shape。")
            return

        targets = self.get_create_targets()

        if not targets:
            return

        radius = self.radius_spin.value()
        axis = self.axis_combo.currentText()
        rotate_x = self.rotate_x_spin.value()
        color = self.color_spin.value()
        create_sub_control = self.create_sub_checkbox.isChecked()
        create_extra_groups = self.create_groups_checkbox.isChecked()
        add_to_set = self.add_set_checkbox.isChecked()

        created_controls = []

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziCreateControllers"
        )

        try:
            target_index = 0
            target_count = len(targets)

            for target in targets:
                control_name = self.get_control_name(
                    target,
                    target_index,
                    target_count
                )

                result = controller_system.create_controller(
                    name=control_name,
                    shape=shape_name,
                    radius=radius,
                    axis=axis,
                    target=target,
                    color=color,
                    rotate_x=rotate_x,
                    create_sub_control=create_sub_control,
                    create_extra_groups=create_extra_groups,
                    add_to_set=add_to_set
                )

                created_controls.append(result["control"])
                target_index += 1

        except Exception as error:
            cmds.warning(str(error))
            self.status_label.setText(u"创建失败")
            return

        finally:
            cmds.undoInfo(closeChunk=True)

        if created_controls:
            cmds.select(
                created_controls,
                replace=True
            )

        self.status_label.setText(
            u"已创建 {} 个控制器".format(len(created_controls))
        )


def main():
    """显示并返回 Control Creator 窗口。"""
    return window_utils.show_window(
        "tools.controller.create_ctrl_tool",
        ControlCreatorDialog
    )


__all__ = [
    "ControlCreatorDialog",
    "main",
]
