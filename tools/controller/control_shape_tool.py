# coding=utf-8
u"""
Control Shape Tool
==================

Maya Controller Shape 图库与编辑工具。

模块职责
--------
1. 展示正式 Controller Shape 资源目录；
2. 收集 Maya Selection 和 UI 参数；
3. 调用 ``core.control_shape_utils`` 执行 Shape 读写和编辑；
4. 管理 Shape 图库交互；
5. 提供在 Maya Script Editor 中可以直接显示的 ``main()`` 入口。

主要公开类型 / 方法
------------------
ShapeListWidget
    Controller Shape JSON 图库控件；负责浏览、应用、上传和删除 Shape。

ColorListWidget
    Maya Index Color 选择控件。

ControlShapeTool
    Controller Shape 图库主窗口。

main()
    创建或恢复主窗口，立即显示并返回 QWidget。

底层边界
--------
Curve Shape 数据读写、CV 编辑、颜色、缩放和镜像统一放在 ``core/control_shape_utils.py``。
本文件只负责 UI 和用户交互，不复制底层 Shape 算法。

直接运行
--------
Maya Python Script Editor：

    from muziToolset.tools.controller import control_shape_tool

    window = control_shape_tool.main()

窗口生命周期
------------
独立运行时通过 ``ui.window_utils`` 保存强引用；从 MuziTools 主工具箱打开时，返回的 QWidget 还会继续
交给 ``app.window_manager`` 做 Maya Parent、Window Flags 和应用级窗口管理。
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
    from PySide2.QtWidgets import QDoubleSpinBox
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QInputDialog
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QListWidget
    from PySide2.QtWidgets import QListWidgetItem
    from PySide2.QtWidgets import QMenu
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtCore import QSize
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QColor
    from PySide6.QtGui import QIcon
    from PySide6.QtGui import QPixmap
    from PySide6.QtWidgets import QCheckBox
    from PySide6.QtWidgets import QDoubleSpinBox
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QInputDialog
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QListWidget
    from PySide6.QtWidgets import QListWidgetItem
    from PySide6.QtWidgets import QMenu
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...core import control_shape_utils
from ...ui import theme
from ...ui import window_utils
from ...core import scene_utils


index_rgb_map = [
    (0.5, 0.5, 0.5),
    (0.0, 0.0, 0.0),
    (0.247, 0.247, 0.247),
    (0.498, 0.498, 0.498),
    (0.608, 0.0, 0.157),
    (0.0, 0.16, 0.376),
    (0.0, 0.0, 1.0),
    (0.0, 0.275, 0.094),
    (0.149, 0.0, 0.263),
    (0.78, 0.0, 0.78),
    (0.537, 0.278, 0.2),
    (0.243, 0.133, 0.121),
    (0.6, 0.145, 0.0),
    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.2549, 0.6),
    (1.0, 1.0, 1.0),
    (1.0, 1.0, 0.0),
    (0.388, 0.863, 1.0),
    (0.263, 1.0, 0.639),
    (1.0, 0.686, 0.686),
    (0.89, 0.674, 0.474),
    (1.0, 1.0, 0.388),
    (0.0, 0.6, 0.329),
    (0.627, 0.411, 0.188),
    (0.619, 0.627, 0.188),
    (0.408, 0.631, 0.188),
    (0.188, 0.631, 0.365),
    (0.188, 0.627, 0.627),
    (0.188, 0.403, 0.627),
    (0.434, 0.188, 0.627),
    (0.627, 0.188, 0.411),
]


class ShapeListWidget(QListWidget):
    """Controller Shape JSON 图库。"""

    def __init__(self, parent=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        # -------------------------------------------------------------------------
        # Step 01：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        super(ShapeListWidget, self).__init__(parent)

        self.setMovement(QListWidget.Static)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        # -------------------------------------------------------------------------
        # Step 02：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(82, 82))
        self.setGridSize(QSize(124, 112))
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.setResizeMode(QListWidget.Adjust)
        self.setSpacing(4)
        self.setMinimumHeight(300)

        # -------------------------------------------------------------------------
        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.create_menu()
        self.create_connections()
        # -------------------------------------------------------------------------
        # Step 05：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        self.refresh()

    def create_menu(self):
        u"""
        创建 Shape 图库右键菜单。
        """
        self.menu = QMenu(self)
        self.menu.addAction(
            u"应用 Shape",
            self.apply_selected_shape
        )
        self.menu.addSeparator()
        self.menu.addAction(
            u"上传当前控制器",
            self.upload_control
        )
        self.menu.addAction(
            u"删除图库 Shape",
            self.delete_shape_files
        )

    def create_connections(self):
        u"""
        连接 Shape 图库信号。
        """
        self.itemDoubleClicked.connect(
            self.apply_item_shape
        )

    def contextMenuEvent(self, event):
        u"""
        执行 `contextMenuEvent` 对应的 Maya 工具操作。

        Args:
            event (QtCore.QEvent | object):
                Qt Event 回调传入的事件对象。
        """

        self.menu.exec_(event.globalPos())

    def refresh(self):
        u"""
        重新扫描 Controller Shape 资源目录。
        """
        # -------------------------------------------------------------------------
        # Step 01：清理当前阶段不再需要的数据或场景状态
        # -------------------------------------------------------------------------
        self.clear()

        library_dir = control_shape_utils.get_library_dir()

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not os.path.isdir(library_dir):
            os.makedirs(library_dir)

        file_names = os.listdir(library_dir)
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        shape_names = []

        for file_name in file_names:
            shape_name, extension = os.path.splitext(file_name)

            if extension.lower() != ".json":
                continue

            shape_names.append(shape_name)

        # -------------------------------------------------------------------------
        # Step 04：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        shape_names.sort()

        # -------------------------------------------------------------------------
        # Step 05：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for shape_name in shape_names:
            jpg_file = os.path.join(
                library_dir,
                "{}.jpg".format(shape_name)
            )
            png_file = os.path.join(
                library_dir,
                "{}.png".format(shape_name)
            )

            icon_file = None

            if os.path.isfile(jpg_file):
                icon_file = jpg_file
            elif os.path.isfile(png_file):
                icon_file = png_file

            if icon_file:
                item = QListWidgetItem(
                    QIcon(icon_file),
                    shape_name,
                    self
                )
            else:
                item = QListWidgetItem(
                    shape_name,
                    self
                )

            item.setToolTip(shape_name)
            item.setTextAlignment(Qt.AlignHCenter)

    def apply_item_shape(self, item):
        u"""
        双击图库项目时应用 Shape。

        Args:
            item (str | object):
                当前查询、吸附或 UI 操作使用的 Maya Item / 数据项。
        """
        self.apply_shape_name(item.text())

    def apply_selected_shape(self):
        u"""
        应用当前第一个选中的图库 Shape。
        """
        items = self.selectedItems()

        if not items:
            cmds.warning(u"请先在图库中选择一个 Shape。")
            return

        self.apply_shape_name(items[0].text())

    @staticmethod
    def apply_shape_name(shape_name):
        u"""
        把指定 Shape 应用到选择控制器，或创建新控制器。

        Args:
            shape_name (str):
                `shape_name` 对应的 Maya 节点或资源名称。
        """
        try:
            shape_data = control_shape_utils.load_shape_data(
                shape_name
            )
        except Exception as error:
            cmds.warning(str(error))
            return

        transforms = control_shape_utils.get_selected_curve_transforms()

        scene_utils.open_undo_chunk("MuziApplyControlShape")

        try:
            if transforms:
                for transform in transforms:
                    control_shape_utils.apply_shape_data(
                        transform,
                        shape_data
                    )
            else:
                transform = cmds.createNode(
                    "transform",
                    name="ctrl_{}".format(shape_name)
                )
                control_shape_utils.apply_shape_data(
                    transform,
                    shape_data
                )
                cmds.select(
                    transform,
                    replace=True
                )
        except Exception as error:
            cmds.warning(str(error))
        finally:
            scene_utils.close_undo_chunk()

    def upload_control(self):
        u"""
        把当前一个 Curve Controller 保存进图库。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        transforms = control_shape_utils.get_selected_curve_transforms()

        if len(transforms) != 1:
            cmds.warning(
                u"上传 Shape 时请只选择一个 Curve 控制器。"
            )
            return

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        default_name = transforms[0].split("|")[-1]

        shape_name, accepted = QInputDialog.getText(
            self,
            u"上传控制器 Shape",
            u"Shape 名称:",
            text=default_name
        )

        if not accepted:
            return

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        shape_name = shape_name.strip()

        if not shape_name:
            return

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        invalid_characters = [
            "/",
            "\\",
            ":",
            "*",
            "?",
            '"',
            "<",
            ">",
            "|",
        ]

        for character in invalid_characters:
            if character in shape_name:
                cmds.warning(
                    u"Shape 名称包含非法字符：{}".format(
                        character
                    )
                )
                return

        # -------------------------------------------------------------------------
        # Step 05：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            file_path = control_shape_utils.save_shape_data(
                shape_name,
                transforms[0]
            )
            self.refresh()
            print(
                u"[Control Shape] 已保存：{}".format(
                    file_path
                )
            )
        except Exception as error:
            cmds.warning(str(error))

    def delete_shape_files(self):
        u"""
        删除选中 Shape 对应的 JSON 和缩略图。
        """
        items = self.selectedItems()

        if not items:
            cmds.warning(
                u"请选择需要删除的图库 Shape。"
            )
            return

        for item in items:
            shape_name = item.text()

            try:
                control_shape_utils.delete_shape_data(
                    shape_name,
                    delete_previews=True
                )
            except OSError as error:
                cmds.warning(str(error))

        self.refresh()


class ColorListWidget(QListWidget):
    """Maya Index Color 选择器。"""

    def __init__(self, parent=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        super(ColorListWidget, self).__init__(parent)

        self.setMovement(QListWidget.Static)
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(30, 30))
        self.setGridSize(QSize(48, 48))
        self.setResizeMode(QListWidget.Adjust)
        self.setMaximumHeight(146)

        self.create_items()
        self.itemClicked.connect(self.apply_color)

    def create_items(self):
        u"""
        创建 Maya Index Color 项目。
        """
        color_index = 0

        for rgb in index_rgb_map:
            pixmap = QPixmap(28, 28)
            pixmap.fill(
                QColor.fromRgbF(
                    rgb[0],
                    rgb[1],
                    rgb[2]
                )
            )

            item = QListWidgetItem(
                QIcon(pixmap),
                str(color_index),
                self
            )
            item.setData(
                Qt.UserRole,
                color_index
            )

            color_index += 1

    @staticmethod
    def apply_color(item):
        u"""
        把 Index Color 应用到选择控制器 Shape。

        Args:
            item (str | object):
                当前查询、吸附或 UI 操作使用的 Maya Item / 数据项。
        """
        color_index = item.data(Qt.UserRole)
        transforms = control_shape_utils.get_selected_curve_transforms()

        if not transforms:
            cmds.warning(u"请先选择 Curve 控制器。")
            return

        for transform in transforms:
            control_shape_utils.set_shape_color(
                transform,
                color_index
            )


class ControlShapeTool(QWidget):
    """Controller Shape 图库主窗口。"""

    def __init__(self, parent=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        super(ControlShapeTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"控制器 Shape 图库",
            minimum_width=620
        )
        self.resize(660, 820)

    def create_widgets(self):
        u"""
        创建窗口控件。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.title_label = theme.make_title(
            u"控制器 Shape 图库"
        )
        self.subtitle_label = theme.make_subtitle(
            u"统一管理 Controller Shape、颜色和 CV 级别编辑。双击图库项目可直接应用。"
        )

        self.library_path_label = QLabel(
            control_shape_utils.get_library_dir()
        )
        self.library_path_label.setWordWrap(True)
        theme.set_role(
            self.library_path_label,
            "muted"
        )

        self.shape_list = ShapeListWidget(self)
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.color_list = ColorListWidget(self)

        self.rotate_spin = QDoubleSpinBox()
        self.rotate_spin.setRange(
            -3600.0,
            3600.0
        )
        self.rotate_spin.setValue(90.0)

        self.rotate_x_check = QCheckBox("X")
        self.rotate_y_check = QCheckBox("Y")
        self.rotate_z_check = QCheckBox("Z")
        # -------------------------------------------------------------------------
        # Step 03：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self.rotate_x_check.setChecked(True)

        self.rotate_button = QPushButton(
            u"旋转 Shape"
        )

        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(
            0.001,
            1000.0
        )
        self.scale_spin.setDecimals(3)
        self.scale_spin.setValue(1.0)

        self.scale_button = QPushButton(
            u"缩放 Shape"
        )

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.mirror_x_button = QPushButton(u"镜像 X")
        self.mirror_y_button = QPushButton(u"镜像 Y")
        self.mirror_z_button = QPushButton(u"镜像 Z")

        self.replace_button = QPushButton(
            u"用最后选择替换前面 Shape"
        )
        theme.style_primary(self.replace_button)

        self.refresh_button = QPushButton(
            u"刷新 Shape 图库"
        )
        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.style_ghost(self.refresh_button)

    def create_layouts(self):
        u"""
        创建统一 Card 布局。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            16,
            16,
            16,
            16
        )
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        library_card, library_layout = theme.make_card(self)
        library_layout.addWidget(
            theme.make_section_title(u"Shape Library")
        )
        library_layout.addWidget(self.library_path_label)
        library_layout.addWidget(self.shape_list)

        color_card, color_layout = theme.make_card(self)
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        color_layout.addWidget(
            theme.make_section_title(u"Maya Index Color")
        )
        color_layout.addWidget(self.color_list)

        edit_card, edit_layout = theme.make_card(self)
        edit_layout.addWidget(
            theme.make_section_title(u"Shape 编辑")
        )

        rotate_layout = QHBoxLayout()
        rotate_layout.setContentsMargins(0, 0, 0, 0)
        rotate_layout.addWidget(QLabel(u"旋转角度"))
        rotate_layout.addWidget(self.rotate_spin)
        rotate_layout.addWidget(self.rotate_x_check)
        rotate_layout.addWidget(self.rotate_y_check)
        rotate_layout.addWidget(self.rotate_z_check)
        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        rotate_layout.addWidget(self.rotate_button)
        edit_layout.addLayout(rotate_layout)

        scale_layout = QHBoxLayout()
        scale_layout.setContentsMargins(0, 0, 0, 0)
        scale_layout.addWidget(QLabel(u"缩放倍数"))
        scale_layout.addWidget(self.scale_spin)
        scale_layout.addWidget(self.scale_button)
        edit_layout.addLayout(scale_layout)

        mirror_layout = QGridLayout()
        mirror_layout.setHorizontalSpacing(8)
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        mirror_layout.setVerticalSpacing(8)
        mirror_layout.addWidget(self.mirror_x_button, 0, 0)
        mirror_layout.addWidget(self.mirror_y_button, 0, 1)
        mirror_layout.addWidget(self.mirror_z_button, 0, 2)
        mirror_layout.addWidget(self.replace_button, 1, 0, 1, 3)
        mirror_layout.addWidget(self.refresh_button, 2, 0, 1, 3)
        edit_layout.addLayout(mirror_layout)

        main_layout.addWidget(library_card)
        main_layout.addWidget(color_card)
        main_layout.addWidget(edit_card)
        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        main_layout.addStretch(1)

    def create_connections(self):
        u"""
        连接窗口信号。
        """
        self.rotate_button.clicked.connect(
            self.rotate_shapes
        )
        self.scale_button.clicked.connect(
            self.scale_shapes
        )
        self.mirror_x_button.clicked.connect(
            self.mirror_x_shapes
        )
        self.mirror_y_button.clicked.connect(
            self.mirror_y_shapes
        )
        self.mirror_z_button.clicked.connect(
            self.mirror_z_shapes
        )
        self.replace_button.clicked.connect(
            self.replace_shapes
        )
        self.refresh_button.clicked.connect(
            self.shape_list.refresh
        )

    def rotate_shapes(self):
        u"""
        旋转选择控制器的 Shape CV。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        transforms = control_shape_utils.get_selected_curve_transforms()

        if not transforms:
            cmds.warning(u"请先选择 Curve 控制器。")
            return

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        angle = self.rotate_spin.value()
        rotate_x = 0.0
        rotate_y = 0.0
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        rotate_z = 0.0

        if self.rotate_x_check.isChecked():
            rotate_x = angle

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if self.rotate_y_check.isChecked():
            rotate_y = angle

        if self.rotate_z_check.isChecked():
            rotate_z = angle

        # -------------------------------------------------------------------------
        # Step 05：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for transform in transforms:
            control_shape_utils.rotate_shape(
                transform,
                rotate_x=rotate_x,
                rotate_y=rotate_y,
                rotate_z=rotate_z
            )

    def scale_shapes(self):
        u"""
        统一缩放选择控制器的 Shape CV。
        """
        transforms = control_shape_utils.get_selected_curve_transforms()

        if not transforms:
            cmds.warning(u"请先选择 Curve 控制器。")
            return

        scale_value = self.scale_spin.value()

        for transform in transforms:
            control_shape_utils.scale_shape(
                transform,
                scale_value
            )

    def mirror_x_shapes(self):
        u"""
        执行 `mirror_x_shapes` 对应的 Maya 工具操作。
        """

        self.mirror_shapes("x")

    def mirror_y_shapes(self):
        u"""
        执行 `mirror_y_shapes` 对应的 Maya 工具操作。
        """

        self.mirror_shapes("y")

    def mirror_z_shapes(self):
        u"""
        执行 `mirror_z_shapes` 对应的 Maya 工具操作。
        """

        self.mirror_shapes("z")

    def mirror_shapes(self, axis):
        u"""
        沿给定轴镜像选择控制器的 Shape CV。

        Args:
            axis (str):
                操作使用的轴向标记。
        """
        transforms = control_shape_utils.get_selected_curve_transforms()

        if not transforms:
            cmds.warning(u"请先选择 Curve 控制器。")
            return

        for transform in transforms:
            control_shape_utils.mirror_shape(
                transform,
                axis=axis
            )

    @staticmethod
    def replace_shapes():
        u"""
        用最后选择控制器的 Shape 替换前面选择对象。
        """
        transforms = control_shape_utils.get_selected_curve_transforms()

        if len(transforms) < 2:
            cmds.warning(
                u"至少选择两个控制器，最后选择的对象作为 Shape 来源。"
            )
            return

        source = transforms[-1]
        targets = transforms[:-1]
        source_data = control_shape_utils.get_shape_data(source)

        if not source_data:
            cmds.warning(
                u"Shape 来源没有 NURBS Curve Shape。"
            )
            return

        scene_utils.open_undo_chunk("MuziReplaceControlShapes")

        try:
            for target in targets:
                control_shape_utils.apply_shape_data(
                    target,
                    source_data
                )
        finally:
            scene_utils.close_undo_chunk()


def main():
    u"""
    创建或恢复 Controller Shape 工具，并立即显示。

    直接从 Maya Script Editor 调用时无需额外执行 ``window.show()``。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return window_utils.show_window(
        "tools.controller.control_shape_tool",
        ControlShapeTool
    )


if __name__ == "__main__":
    main()
