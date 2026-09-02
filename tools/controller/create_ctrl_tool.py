# coding=utf-8
u"""
Control Creator
===============

控制器创建工具 UI。

边界：
    - Controller Shape 数据来自 resources/controller_shapes；
    - Rig Name 统一使用实例化的 systems.rig_base.RigBase；
    - Controller Hierarchy 统一使用 systems.ctrl_base.create_ctrl；
    - 标准 zero / driven / space / connect / offset / ctrl / output 层级固定创建；
    - UI 不重复实现 Controller 构建算法。
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
from ...core import rename_utils
from ...core import scene_utils
from ...systems import ctrl_base
from ...systems.rig_base import RigBase
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
    u"""Controller Creator 主窗口。"""

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
        self.resize(
            660,
            760
        )

    # =========================================================================
    # UI
    # =========================================================================

    def create_widgets(self):
        u"""创建界面控件。"""
        self.title_label = theme.make_title(
            u"创建控制器"
        )
        self.subtitle_label = theme.make_subtitle(
            u"统一使用 RigBase Identity 命名和 CtrlBase 标准控制器层级。"
        )

        self.shape_search_line = QLineEdit()
        self.shape_search_line.setPlaceholderText(
            u"搜索 Shape..."
        )
        theme.style_search(
            self.shape_search_line
        )

        self.shape_list = QListWidget()
        self.shape_list.setViewMode(
            QListWidget.IconMode
        )
        self.shape_list.setResizeMode(
            QListWidget.Adjust
        )
        self.shape_list.setMovement(
            QListWidget.Static
        )
        self.shape_list.setSelectionMode(
            QListWidget.SingleSelection
        )
        self.shape_list.setIconSize(
            QSize(72, 72)
        )
        self.shape_list.setGridSize(
            QSize(132, 118)
        )
        self.shape_list.setSpacing(
            4
        )
        self.shape_list.setMinimumHeight(
            310
        )
        self.shape_list.setWordWrap(
            True
        )
        self.shape_list.setUniformItemSizes(
            True
        )
        self.shape_list.setWrapping(
            True
        )
        self.shape_list.setFlow(
            QListView.LeftToRight
        )

        self.radius_spin = QDoubleSpinBox()
        self.radius_spin.setDecimals(3)
        self.radius_spin.setRange(0.001, 10000.0)
        self.radius_spin.setValue(2.0)
        self.radius_spin.setSingleStep(0.1)

        self.axis_combo = QComboBox()

        for axis in axis_list:
            self.axis_combo.addItem(
                axis
            )

        self.axis_combo.setCurrentText(
            "Y+"
        )

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
            u"标准名称，例如 ctrl_md_hand_main_001；留空自动生成"
        )

        self.create_sub_checkbox = QCheckBox(
            u"创建次级控制器"
        )
        self.create_sub_checkbox.setChecked(
            True
        )

        self.add_set_checkbox = QCheckBox(
            u"加入 ctrl_set"
        )
        self.add_set_checkbox.setChecked(
            True
        )

        self.refresh_button = QPushButton(
            u"刷新 Shape 图库"
        )
        theme.style_ghost(
            self.refresh_button
        )

        self.create_button = QPushButton(
            u"创建控制器"
        )
        theme.style_primary(
            self.create_button
        )

        self.status_label = QLabel(
            u"准备就绪"
        )
        theme.set_role(
            self.status_label,
            "muted"
        )

    def create_layouts(self):
        u"""创建窗口布局。"""
        main_layout = QVBoxLayout(
            self
        )
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

        standard_hint = QLabel(
            u"CtrlBase 固定创建 zero → driven → space → connect → offset → ctrl → output。"
        )
        standard_hint.setWordWrap(
            True
        )
        theme.set_role(
            standard_hint,
            "muted"
        )
        hierarchy_layout.addWidget(
            standard_hint
        )

        option_layout = QHBoxLayout()
        option_layout.setContentsMargins(0, 0, 0, 0)
        option_layout.addWidget(self.create_sub_checkbox)
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
        u"""连接 UI Signal。"""
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

    # =========================================================================
    # Shape Library
    # =========================================================================

    def refresh_shape_library(self):
        u"""重新读取正式 Controller Shape 资源目录。"""
        self.shape_list.clear()

        if not os.path.isdir(controller_shapes_dir):
            self.status_label.setText(
                u"Shape 资源目录不存在"
            )
            return

        file_names = os.listdir(
            controller_shapes_dir
        )
        shape_names = []

        for file_name in file_names:
            shape_name, extension = os.path.splitext(
                file_name
            )

            if extension.lower() != ".json":
                continue

            if shape_name not in shape_names:
                shape_names.append(
                    shape_name
                )

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

                pixmap = QPixmap(
                    preview_path
                )

                if not pixmap.isNull():
                    icon = QIcon(
                        pixmap
                    )

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
            u"已加载 {} 个 Shape".format(
                self.shape_list.count()
            )
        )

    def filter_shape_library(self, text_value):
        u"""根据搜索文字过滤 Shape。"""
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
        u"""返回当前选中的 Shape 名称。"""
        selected_items = self.shape_list.selectedItems()

        if not selected_items:
            return None

        return selected_items[0].data(
            Qt.UserRole
        )

    # =========================================================================
    # Color
    # =========================================================================

    def update_color_preview(self):
        u"""刷新 Maya Index Color 预览块。"""
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
            u"border-radius: 6px;".format(
                color.name()
            )
        )

    # =========================================================================
    # Target / Naming
    # =========================================================================

    def get_create_targets(self):
        u"""根据当前创建模式返回 Target List。"""
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
            cmds.warning(
                u"当前创建模式需要先选择 Maya 对象。"
            )
            return []

        if mode == "selection":
            return selections

        targets = []

        for root in selections:
            if root not in targets:
                targets.append(
                    root
                )

            descendants = cmds.listRelatives(
                root,
                allDescendents=True,
                fullPath=True
            )

            if descendants is None:
                descendants = []

            descendants.reverse()

            for descendant in descendants:
                node_type = cmds.nodeType(
                    descendant
                )

                if node_type not in [
                    "transform",
                    "joint",
                ]:
                    continue

                if descendant not in targets:
                    targets.append(
                        descendant
                    )

        return targets

    @staticmethod
    def _clean_part(text):
        u"""把任意 Tool 输入整理成可用于 RigBase part 的字符串。"""
        text = str(text).strip().lower()
        text = text.replace("|", "_")
        text = text.replace(":", "_")
        text = text.replace(" ", "_")
        text = text.replace("-", "_")

        while "__" in text:
            text = text.replace("__", "_")

        text = text.strip("_")

        if not text:
            text = "new"

        return text

    @staticmethod
    def _create_control_name(
            side,
            part,
            function,
            index
    ):
        u"""根据一个明确 Rig Identity 创建 Controller Name。"""
        rig_object = RigBase(
            side=side,
            part=part,
            index=index
        )

        return rig_object.create_name(
            node_type="ctrl",
            function=function
        )

    def get_control_name(self, target, target_index, target_count):
        u"""使用 RigBase Identity 生成当前 Controller 的正式名称。"""
        custom_name = self.name_line.text().strip()

        if custom_name:
            if RigBase.validate_name(custom_name):
                fields = RigBase.parse_name(
                    custom_name
                )
                index = fields["index"]

                if target_count > 1:
                    index = target_index + 1

                return self._create_control_name(
                    side=fields["side"],
                    part=fields["part"],
                    function=fields["function"],
                    index=index
                )

            return self._create_control_name(
                side="md",
                part=self._clean_part(custom_name),
                function="main",
                index=target_index + 1
            )

        if target is None:
            return self._create_control_name(
                side="md",
                part="new",
                function="main",
                index=target_index + 1
            )

        target_name = rename_utils.get_short_name(
            target
        )

        if RigBase.validate_name(target_name):
            fields = RigBase.parse_name(
                target_name
            )
            return self._create_control_name(
                side=fields["side"],
                part=fields["part"],
                function=fields["function"],
                index=fields["index"]
            )

        return self._create_control_name(
            side="md",
            part=self._clean_part(target_name),
            function="main",
            index=target_index + 1
        )

    # =========================================================================
    # Create
    # =========================================================================

    def create_controls(self):
        u"""根据 UI 参数调用 ctrl_base.create_ctrl()。"""
        shape_name = self.selected_shape_name()

        if not shape_name:
            cmds.warning(
                u"请先选择一个 Controller Shape。"
            )
            return

        targets = self.get_create_targets()

        if not targets:
            return

        radius = self.radius_spin.value()
        axis = self.axis_combo.currentText()
        rotate_x = self.rotate_x_spin.value()
        color = self.color_spin.value()
        create_sub_ctrl = self.create_sub_checkbox.isChecked()
        add_to_set = self.add_set_checkbox.isChecked()

        created_controls = []

        scene_utils.open_undo_chunk(
            "MuziCreateControllers"
        )

        try:
            target_index = 0
            target_count = len(targets)

            for target in targets:
                ctrl_name = self.get_control_name(
                    target,
                    target_index,
                    target_count
                )

                result = ctrl_base.create_ctrl(
                    name=ctrl_name,
                    shape=shape_name,
                    radius=radius,
                    axis=axis,
                    target_node=target,
                    color=color,
                    rotate_x=rotate_x,
                    create_sub_ctrl=create_sub_ctrl,
                    add_to_set=add_to_set
                )

                created_controls.append(
                    result["ctrl_node"]
                )
                target_index += 1

        except Exception as error:
            cmds.warning(
                str(error)
            )
            self.status_label.setText(
                u"创建失败"
            )
            return

        finally:
            scene_utils.close_undo_chunk()

        if created_controls:
            cmds.select(
                created_controls,
                replace=True
            )

        self.status_label.setText(
            u"已创建 {} 个控制器".format(
                len(created_controls)
            )
        )


def main():
    u"""显示并返回 Control Creator 窗口。"""
    return window_utils.show_window(
        "tools.controller.create_ctrl_tool",
        ControlCreatorDialog
    )


__all__ = [
    "ControlCreatorDialog",
    "main",
]
