# -*- coding: utf-8 -*-
"""
set_ctrl_tool.py
控制器编辑工具（Maya 2023 / PySide2）

功能：
- 从 controlUtils 对应的 tools/image 目录读取控制器形状缩略图
- 给当前选中的控制器应用形状、颜色和大小
- 按 X / Y / Z 轴旋转控制器形状
- 镜像控制器形状、在多个控制器之间替换形状
- 上传当前控制器形状、删除形状库中的预设

使用方法：
    from MuziTools.tools.ctrl import set_ctrl_tool
    set_ctrl_tool.main()
"""

from __future__ import print_function

import os
from contextlib import contextmanager
from importlib import reload

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds

try:
    from ....core import controlUtils
except ImportError:
    raise ImportError(u"无法导入 controlUtils，请确保该工具通过 MuziTools 包运行")

reload(controlUtils)


# Maya overrideColor 0-31 颜色表（RGB）。
MAYA_COLORS = {
    0: (0.467, 0.467, 0.467), 1: (0.000, 0.000, 0.000),
    2: (0.200, 0.200, 0.200), 3: (0.600, 0.600, 0.600),
    4: (0.800, 0.000, 0.000), 5: (0.000, 0.000, 0.400),
    6: (0.000, 0.000, 1.000), 7: (0.000, 0.400, 0.000),
    8: (0.200, 0.000, 0.400), 9: (0.800, 0.400, 0.000),
    10: (0.600, 0.400, 0.200), 11: (0.400, 0.200, 0.000),
    12: (1.000, 1.000, 0.000), 13: (1.000, 0.000, 0.000),
    14: (0.000, 1.000, 0.000), 15: (0.000, 1.000, 1.000),
    16: (1.000, 1.000, 1.000), 17: (1.000, 1.000, 0.000),
    18: (0.000, 0.800, 1.000), 19: (1.000, 0.600, 0.800),
    20: (1.000, 0.400, 0.400), 21: (0.600, 1.000, 0.400),
    22: (1.000, 0.800, 0.400), 23: (0.400, 0.600, 1.000),
    24: (1.000, 1.000, 1.000), 25: (1.000, 1.000, 0.800),
    26: (0.800, 1.000, 0.800), 27: (0.800, 1.000, 1.000),
    28: (1.000, 0.800, 1.000), 29: (1.000, 0.600, 0.600),
    30: (0.800, 1.000, 0.600), 31: (0.600, 0.800, 1.000),
}


def get_maya_main_window():
    """返回 Maya 主窗口，保证工具始终附着在 Maya 上。"""
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(int(ptr), QWidget)
    return None


def get_shape_library_path():
    """返回 tools/image 形状库目录。"""
    core_dir = os.path.dirname(os.path.abspath(controlUtils.__file__))
    return os.path.abspath(os.path.join(core_dir, os.pardir, "tools", "image"))


@contextmanager
def maya_undo_chunk(name):
    """把一次按钮操作包装成一个 Maya Undo 步骤。"""
    cmds.undoInfo(openChunk=True, chunkName=name)
    try:
        yield
    finally:
        cmds.undoInfo(closeChunk=True)


class ControlShapeButton(QToolButton):
    """形状选择按钮：缩略图在上，形状名称在下。"""

    def __init__(self, shape_name, parent=None):
        super(ControlShapeButton, self).__init__(parent)
        self.shape_name = shape_name
        self.setCheckable(True)
        self.setFixedSize(110, 90)
        self.setToolTip(shape_name)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setIconSize(QSize(64, 64))
        self.setStyleSheet("""
            QToolButton {
                background-color: #2b2b2b;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                color: #aaaaaa;
                font-size: 10px;
                padding: 4px;
            }
            QToolButton:hover {
                background-color: #353535;
                border-color: #5a5a5a;
            }
            QToolButton:checked {
                background-color: #3a3a3a;
                border-color: #00a8ff;
                color: #ffffff;
            }
        """)
        self._load_thumbnail()

    def _load_thumbnail(self):
        jpg_path = os.path.join(
            get_shape_library_path(), "{}.jpg".format(self.shape_name)
        )
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)

        if os.path.exists(jpg_path):
            thumbnail = QPixmap(jpg_path)
            if not thumbnail.isNull():
                pixmap = thumbnail.scaled(
                    64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )

        self.setIcon(QIcon(pixmap))
        display_name = self.shape_name
        if len(display_name) > 12:
            display_name = display_name[:11] + u"…"
        self.setText(display_name)


class ColorPreviewLabel(QLabel):
    """Maya 颜色索引预览方块。"""

    def __init__(self, parent=None):
        super(ColorPreviewLabel, self).__init__(parent)
        self.setFixedSize(32, 32)
        self.setFrameShape(QFrame.StyledPanel)
        self.set_color(6)

    def set_color(self, color_index):
        rgb = MAYA_COLORS.get(int(color_index), (0.5, 0.5, 0.5))
        r, g, b = [int(channel * 255) for channel in rgb]
        self.setStyleSheet(
            "background-color: rgb({}, {}, {}); "
            "border: 2px solid #ffffff; border-radius: 4px;".format(r, g, b)
        )
        self.setToolTip("Color Index: {}".format(color_index))


class ControlSetterUI(QDialog):
    """控制器形状和显示属性编辑窗口。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = get_maya_main_window()
        super(ControlSetterUI, self).__init__(parent)

        self.setWindowTitle("CONTROL SETTER")
        self.setMinimumSize(500, 650)
        self.resize(520, 720)
        self.setWindowFlags(Qt.Window)

        self.current_shape = None
        self.shape_buttons = []
        self.shape_group = None

        self.create_widgets()
        self._load_shapes()
        self.create_connections()

    # ------------------------------------------------------------------ UI
    def create_widgets(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Shape Search:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(u"输入形状名称进行筛选")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.setStyleSheet(self._line_edit_style())
        self.refresh_shapes_btn = QPushButton(u"刷新")
        self.refresh_shapes_btn.setFixedWidth(60)
        search_layout.addWidget(self.search_edit, 1)
        search_layout.addWidget(self.refresh_shapes_btn)
        main_layout.addLayout(search_layout)

        shape_scroll = QScrollArea()
        shape_scroll.setWidgetResizable(True)
        shape_scroll.setFrameShape(QFrame.NoFrame)
        shape_scroll.setStyleSheet("QScrollArea { background-color: transparent; }")

        self.shapes_widget = QWidget()
        self.shapes_layout = QGridLayout(self.shapes_widget)
        self.shapes_layout.setSpacing(8)
        self.shapes_layout.setContentsMargins(4, 4, 4, 4)
        shape_scroll.setWidget(self.shapes_widget)
        main_layout.addWidget(shape_scroll, 1)

        shape_action_layout = QHBoxLayout()
        self.apply_shape_btn = QPushButton(u"应用所选形状")
        self.upload_shape_btn = QPushButton(u"上传当前控制器")
        self.delete_shape_btn = QPushButton(u"删除所选预设")
        shape_action_layout.addWidget(self.apply_shape_btn)
        shape_action_layout.addWidget(self.upload_shape_btn)
        shape_action_layout.addWidget(self.delete_shape_btn)
        main_layout.addLayout(shape_action_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #3d3d3d;")
        main_layout.addWidget(line)

        color_group = QGroupBox("Color Override")
        color_group.setStyleSheet(self._group_style())
        color_layout = QHBoxLayout(color_group)
        color_layout.setSpacing(10)

        self.color_slider = QSlider(Qt.Horizontal)
        self.color_slider.setRange(0, 31)
        self.color_slider.setValue(6)
        self.color_slider.setTickPosition(QSlider.TicksBelow)
        self.color_slider.setTickInterval(1)
        self.color_slider.setStyleSheet(self._slider_style())

        self.color_spin = QSpinBox()
        self.color_spin.setRange(0, 31)
        self.color_spin.setValue(6)
        self.color_spin.setFixedWidth(50)
        self.color_spin.setStyleSheet(self._spin_style())

        self.color_preview = ColorPreviewLabel()
        self.apply_color_btn = QPushButton(u"应用颜色")

        color_layout.addWidget(QLabel("Index:"))
        color_layout.addWidget(self.color_slider, 1)
        color_layout.addWidget(self.color_spin)
        color_layout.addWidget(self.color_preview)
        color_layout.addWidget(self.apply_color_btn)
        main_layout.addWidget(color_group)

        transform_group = QGroupBox("Shape Transform")
        transform_group.setStyleSheet(self._group_style())
        transform_layout = QGridLayout(transform_group)
        transform_layout.setSpacing(8)

        transform_layout.addWidget(QLabel(u"缩放百分比:"), 0, 0)
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(1.0, 1000.0)
        self.scale_spin.setDecimals(2)
        self.scale_spin.setValue(100.0)
        self.scale_spin.setSingleStep(10.0)
        self.scale_spin.setSuffix(" %")
        self.scale_spin.setStyleSheet(self._spin_style())
        transform_layout.addWidget(self.scale_spin, 0, 1)
        self.apply_scale_btn = QPushButton(u"缩放")
        transform_layout.addWidget(self.apply_scale_btn, 0, 2)

        transform_layout.addWidget(QLabel(u"旋转角度:"), 1, 0)
        self.rotate_spin = QDoubleSpinBox()
        self.rotate_spin.setRange(-360.0, 360.0)
        self.rotate_spin.setDecimals(2)
        self.rotate_spin.setValue(90.0)
        self.rotate_spin.setSingleStep(15.0)
        self.rotate_spin.setSuffix(u"°")
        self.rotate_spin.setStyleSheet(self._spin_style())
        transform_layout.addWidget(self.rotate_spin, 1, 1)

        axis_layout = QHBoxLayout()
        self.rotate_x_check = QCheckBox("X")
        self.rotate_y_check = QCheckBox("Y")
        self.rotate_z_check = QCheckBox("Z")
        self.rotate_x_check.setChecked(True)
        axis_layout.addWidget(self.rotate_x_check)
        axis_layout.addWidget(self.rotate_y_check)
        axis_layout.addWidget(self.rotate_z_check)
        transform_layout.addLayout(axis_layout, 1, 2)

        self.apply_rotate_btn = QPushButton(u"旋转")
        transform_layout.addWidget(self.apply_rotate_btn, 1, 3)
        main_layout.addWidget(transform_group)

        other_layout = QHBoxLayout()
        self.mirror_btn = QPushButton(u"镜像形状")
        self.replace_btn = QPushButton(u"替换形状")
        self.replace_btn.setToolTip(
            u"至少选择两个控制器：最后选择的控制器作为形状来源"
        )
        other_layout.addWidget(self.mirror_btn)
        other_layout.addWidget(self.replace_btn)
        main_layout.addLayout(other_layout)

        self.setStyleSheet("""
            QDialog { background-color: #1e1e1e; }
            QWidget { color: #aaaaaa; font-size: 11px; }
            QPushButton {
                background-color: #353535;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                color: #dddddd;
                padding: 6px 10px;
            }
            QPushButton:hover { background-color: #454545; border-color: #00a8ff; }
            QPushButton:pressed { background-color: #252525; }
            QCheckBox { spacing: 5px; }
        """)
        self.apply_shape_btn.setStyleSheet(self._primary_button_style())

    def create_connections(self):
        """集中连接界面信号，保持和 create_ctrl_tool 相同的组织方式。"""
        self.search_edit.textChanged.connect(self._filter_shapes)
        self.refresh_shapes_btn.clicked.connect(self._load_shapes)

        self.apply_shape_btn.clicked.connect(self.apply_selected_shape)
        self.upload_shape_btn.clicked.connect(self.upload_selected_controls)
        self.delete_shape_btn.clicked.connect(self.delete_selected_shape)

        self.color_slider.valueChanged.connect(self._on_color_changed)
        self.color_spin.valueChanged.connect(self._on_color_changed)
        self.apply_color_btn.clicked.connect(self.apply_selected_color)

        self.apply_scale_btn.clicked.connect(self.scale_selected_controls)
        self.apply_rotate_btn.clicked.connect(self.rotate_selected_controls)
        self.mirror_btn.clicked.connect(self.mirror_selected_controls)
        self.replace_btn.clicked.connect(self.replace_selected_controls)

    # --------------------------------------------------------------- Shapes
    def _load_shapes(self):
        """重新读取 JSON 形状文件并生成网格按钮。"""
        while self.shapes_layout.count():
            layout_item = self.shapes_layout.takeAt(0)
            widget = layout_item.widget()
            if widget is not None:
                widget.deleteLater()

        self.current_shape = None
        self.shape_buttons = []
        self.shape_group = QButtonGroup(self)
        self.shape_group.setExclusive(True)

        shape_dir = get_shape_library_path()
        shape_names = []
        if os.path.isdir(shape_dir):
            shape_names = sorted(
                os.path.splitext(file_name)[0]
                for file_name in os.listdir(shape_dir)
                if file_name.lower().endswith(".json")
            )

        columns = 4
        for index, shape_name in enumerate(shape_names):
            button = ControlShapeButton(shape_name)
            self.shape_group.addButton(button)
            self.shapes_layout.addWidget(button, index // columns, index % columns)
            self.shape_buttons.append(button)

        if shape_names:
            self.shape_group.buttonClicked.connect(self._on_shape_selected)
        else:
            empty_label = QLabel(u"没有找到控制器形状，请检查 tools/image 目录。")
            empty_label.setAlignment(Qt.AlignCenter)
            self.shapes_layout.addWidget(empty_label, 0, 0, 1, columns)

        self._filter_shapes(self.search_edit.text())

    def _on_shape_selected(self, button):
        self.current_shape = button.shape_name if button.isChecked() else None

    def _filter_shapes(self, text):
        keyword = text.strip().lower()
        for button in self.shape_buttons:
            button.setVisible(keyword in button.shape_name.lower())

    # ------------------------------------------------------------ UI Values
    def _on_color_changed(self, value):
        self.color_slider.blockSignals(True)
        self.color_spin.blockSignals(True)
        self.color_slider.setValue(value)
        self.color_spin.setValue(value)
        self.color_slider.blockSignals(False)
        self.color_spin.blockSignals(False)
        self.color_preview.set_color(value)

    @staticmethod
    def _selected_controls(minimum=1):
        """获取 controlUtils 控制器对象，并统一处理空选择。"""
        try:
            controls = list(controlUtils.Control.selected() or [])
        except Exception as exc:
            cmds.warning(u"【Control Setter】读取选中控制器失败: {}".format(exc))
            return []

        if len(controls) < minimum:
            if minimum == 1:
                cmds.warning(u"【Control Setter】请先选择至少一个控制器。")
            else:
                cmds.warning(
                    u"【Control Setter】请至少选择 {} 个控制器。".format(minimum)
                )
            return []
        return controls

    # --------------------------------------------------------------- Actions
    def apply_selected_shape(self):
        if not self.current_shape:
            cmds.warning(u"【Control Setter】请先选择一个形状预设。")
            return
        controls = self._selected_controls()
        if not controls:
            return

        try:
            with maya_undo_chunk("ControlSetter_ApplyShape"):
                radius = controlUtils.Control.get_soft_radius()
                controlUtils.Control.set_selected(s=self.current_shape, r=radius)
            cmds.warning(
                u"【Control Setter】已为 {} 个控制器应用形状 {}。".format(
                    len(controls), self.current_shape
                )
            )
        except Exception as exc:
            cmds.warning(u"【Control Setter】应用形状失败: {}".format(exc))

    def apply_selected_color(self):
        controls = self._selected_controls()
        if not controls:
            return

        color_index = self.color_spin.value()
        try:
            with maya_undo_chunk("ControlSetter_ApplyColor"):
                controlUtils.Control.set_selected(c=color_index)
            cmds.warning(
                u"【Control Setter】已为 {} 个控制器应用颜色 {}。".format(
                    len(controls), color_index
                )
            )
        except Exception as exc:
            cmds.warning(u"【Control Setter】设置颜色失败: {}".format(exc))

    def scale_selected_controls(self):
        controls = self._selected_controls()
        if not controls:
            return

        scale_factor = self.scale_spin.value() / 100.0
        success_count = 0
        try:
            with maya_undo_chunk("ControlSetter_ScaleShape"):
                for control in controls:
                    current_radius = float(control.get_radius())
                    control.set_radius(r=current_radius * scale_factor)
                    success_count += 1
            cmds.warning(
                u"【Control Setter】已按 {}% 缩放 {} 个控制器。".format(
                    self.scale_spin.value(), success_count
                )
            )
        except Exception as exc:
            cmds.warning(u"【Control Setter】缩放控制器失败: {}".format(exc))


    def rotate_selected_controls (self) :
        """
        旋转当前选择控制器的 Shape。
        """

        controls = self._selected_controls ()

        if not controls :
            return

        # ------------------------------------------------------------
        # 获取界面中勾选的旋转轴
        # ------------------------------------------------------------

        rotate_x = self.rotate_x_check.isChecked ()
        rotate_y = self.rotate_y_check.isChecked ()
        rotate_z = self.rotate_z_check.isChecked ()

        # ------------------------------------------------------------
        # 至少需要选择一个旋转轴
        # ------------------------------------------------------------

        if not any ((rotate_x , rotate_y , rotate_z)) :
            cmds.warning (
                u"【Control Setter】请至少勾选一个旋转轴。"
            )

            return

        # ------------------------------------------------------------
        # 获取旋转角度
        # ------------------------------------------------------------

        angle = self.rotate_spin.value ()

        # ------------------------------------------------------------
        # 根据勾选状态计算 XYZ 旋转值
        # ------------------------------------------------------------

        rotate_value_x = 0
        rotate_value_y = 0
        rotate_value_z = 0

        if rotate_x :
            rotate_value_x = angle

        if rotate_y :
            rotate_value_y = angle

        if rotate_z :
            rotate_value_z = angle

        # ------------------------------------------------------------
        # 旋转控制器 Shape
        # ------------------------------------------------------------

        try :

            with maya_undo_chunk (
                    "ControlSetter_RotateShape"
            ) :

                for control in controls :
                    control.set_rotate (
                        rx = rotate_value_x ,
                        ry = rotate_value_y ,
                        rz = rotate_value_z
                    )

            cmds.warning (
                u"【Control Setter】已旋转 {} 个控制器。".format (
                    len (controls)
                )
            )

        except Exception as exc :

            cmds.warning (
                u"【Control Setter】旋转控制器失败: {}".format (
                    exc
                )
            )

    def mirror_selected_controls(self):
        controls = self._selected_controls()
        if not controls:
            return
        try:
            with maya_undo_chunk("ControlSetter_MirrorShape"):
                controlUtils.Control.mirror_selected()
            cmds.warning(
                u"【Control Setter】已镜像 {} 个控制器。".format(len(controls))
            )
        except Exception as exc:
            cmds.warning(u"【Control Setter】镜像控制器失败: {}".format(exc))

    def replace_selected_controls(self):
        controls = self._selected_controls(minimum=2)
        if not controls:
            return

        source_control = controls[-1]
        target_controls = controls[:-1]
        try:
            with maya_undo_chunk("ControlSetter_ReplaceShape"):
                source_shape = source_control.get_shape()
                for control in target_controls:
                    control.set_shape(source_shape)
            cmds.warning(
                u"【Control Setter】已用最后选择的控制器替换 {} 个形状。".format(
                    len(target_controls)
                )
            )
        except Exception as exc:
            cmds.warning(u"【Control Setter】替换形状失败: {}".format(exc))

    def upload_selected_controls(self):
        controls = self._selected_controls()
        if not controls:
            return

        try:
            with maya_undo_chunk("ControlSetter_UploadShape"):
                for control in controls:
                    control.upload()
            self._load_shapes()
            cmds.warning(
                u"【Control Setter】已上传 {} 个控制器形状。".format(len(controls))
            )
        except Exception as exc:
            cmds.warning(u"【Control Setter】上传控制器失败: {}".format(exc))

    def delete_selected_shape(self):
        if not self.current_shape:
            cmds.warning(u"【Control Setter】请先选择要删除的形状预设。")
            return

        result = QMessageBox.question(
            self,
            u"删除形状预设",
            u"确定删除形状预设“{}”吗？\n此操作会删除对应的 JSON 和缩略图文件。".format(
                self.current_shape
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if result != QMessageBox.Yes:
            return

        shape_name = self.current_shape
        try:
            controlUtils.Control.delete_shapes(shape_name)
            self._load_shapes()
            cmds.warning(u"【Control Setter】已删除形状预设 {}。".format(shape_name))
        except Exception as exc:
            cmds.warning(u"【Control Setter】删除形状预设失败: {}".format(exc))

    # --------------------------------------------------------------- Styles
    @staticmethod
    def _line_edit_style():
        return """
            QLineEdit {
                background-color: #2b2b2b;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: #cccccc;
                padding: 4px 8px;
            }
            QLineEdit:focus { border-color: #00a8ff; }
        """

    @staticmethod
    def _spin_style():
        return """
            QDoubleSpinBox, QSpinBox {
                background-color: #2b2b2b;
                border: 1px solid #3d3d3d;
                color: #cccccc;
                padding: 2px;
                border-radius: 3px;
            }
            QDoubleSpinBox::up-button, QSpinBox::up-button { width: 14px; }
            QDoubleSpinBox::down-button, QSpinBox::down-button { width: 14px; }
        """

    @staticmethod
    def _group_style():
        return """
            QGroupBox {
                color: #aaaaaa;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
            }
        """

    @staticmethod
    def _slider_style():
        return """
            QSlider::groove:horizontal {
                height: 6px;
                background: #3d3d3d;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #00a8ff;
                width: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #00a8ff;
                border-radius: 3px;
            }
        """

    @staticmethod
    def _primary_button_style():
        return """
            QPushButton {
                background-color: #00a8ff;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0090e0; }
            QPushButton:pressed { background-color: #0078c0; }
        """


# 保留旧类名，避免其他脚本仍然通过 ControlsWidget 调用时失效。
ControlsWidget = ControlSetterUI


control_window = None


def main():
    """关闭旧窗口并显示新的控制器编辑窗口。"""
    global control_window
    if control_window is not None:
        try:
            control_window.close()
            control_window.deleteLater()
        except Exception:
            pass

    control_window = ControlSetterUI()
    control_window.show()
    return control_window


if __name__ == "__main__":
    main()
