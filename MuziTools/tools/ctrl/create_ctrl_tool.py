# coding=utf-8
u"""
Control Creator
===============

Maya 2023 / PySide2 控制器创建工具。

本模块与 ``control_shape_tool`` 共用同一套 JSON Shape 数据，创建过程只使用
``maya.cmds``，不再依赖 ``core.controlUtils`` 的 PyMel 对象。
"""

from __future__ import print_function

import os

import maya.cmds as cmds

from PySide2.QtCore import QSize
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor
from PySide2.QtGui import QIcon
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QButtonGroup
from PySide2.QtWidgets import QCheckBox
from PySide2.QtWidgets import QComboBox
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QDoubleSpinBox
from PySide2.QtWidgets import QFrame
from PySide2.QtWidgets import QGridLayout
from PySide2.QtWidgets import QGroupBox
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QScrollArea
from PySide2.QtWidgets import QSlider
from PySide2.QtWidgets import QSpinBox
from PySide2.QtWidgets import QToolButton
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget

from ....core import qtUtils
from . import control_shape_tool


_window = None


MAYA_COLORS = {
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


AXIS_ROTATION = {
    "X+": (90.0, 0.0, 0.0),
    "X-": (-90.0, 0.0, 0.0),
    "Y+": (0.0, 90.0, 0.0),
    "Y-": (0.0, -90.0, 0.0),
    "Z+": (0.0, 0.0, 90.0),
    "Z-": (0.0, 0.0, -90.0),
}


def _short_name(node):
    return node.split("|")[-1].replace(":", "_")


def _safe_control_name(name):
    clean_name = name.replace("|", "_").replace(":", "_").strip()

    if not clean_name:
        clean_name = "ctrl_new_001"

    if not clean_name.startswith("ctrl_"):
        clean_name = "ctrl_" + clean_name

    return clean_name


def _name_from_target(target):
    short_name = _short_name(target)

    if short_name.startswith("jnt_"):
        return short_name.replace("jnt_", "ctrl_", 1)

    if short_name.startswith("bpjnt_"):
        return short_name.replace("bpjnt_", "ctrl_", 1)

    return _safe_control_name(short_name)


def _next_available_name(name):
    if not cmds.objExists(name):
        return name

    index = 1
    while True:
        candidate = "{}_{:03d}".format(name, index)
        if not cmds.objExists(candidate):
            return candidate
        index += 1


def _replace_ctrl_prefix(name, prefix):
    if name.startswith("ctrl_"):
        return name.replace("ctrl_", prefix + "_", 1)

    return "{}_{}".format(prefix, name)


def _curve_shapes(transform):
    return cmds.listRelatives(
        transform,
        shapes=True,
        noIntermediate=True,
        fullPath=True,
        type="nurbsCurve"
    ) or []


def _shape_cvs(transform):
    cvs = []
    shapes = _curve_shapes(transform)

    for shape in shapes:
        shape_cvs = cmds.ls(shape + ".cv[*]", flatten=True) or []
        for cv in shape_cvs:
            cvs.append(cv)

    return cvs


def _set_shape_color(transform, color_index):
    shapes = _curve_shapes(transform)

    for shape in shapes:
        cmds.setAttr(shape + ".overrideEnabled", 1)
        cmds.setAttr(shape + ".overrideRGBColors", 0)
        cmds.setAttr(shape + ".overrideColor", int(color_index))


def _transform_shape(transform, radius, axis, rotate_x=0.0):
    cvs = _shape_cvs(transform)
    if not cvs:
        return

    cmds.scale(
        radius,
        radius,
        radius,
        cvs,
        relative=True,
        objectSpace=True
    )

    axis_rotation = AXIS_ROTATION.get(axis, (0.0, 0.0, 0.0))
    rotate_x_value = axis_rotation[0] + float(rotate_x)

    cmds.rotate(
        rotate_x_value,
        axis_rotation[1],
        axis_rotation[2],
        cvs,
        relative=True,
        objectSpace=True
    )


def _add_to_control_set(control):
    set_name = "ctrl_set"

    if not cmds.objExists(set_name):
        cmds.sets(name=set_name, empty=True)

    cmds.sets(control, add=set_name)


def _hierarchy_targets(root):
    """按父到子的顺序返回 Transform / Joint 层级。"""
    result = []

    def walk(node):
        if node in result:
            return

        node_type = cmds.nodeType(node)
        if node_type not in ("transform", "joint"):
            return

        result.append(node)

        children = cmds.listRelatives(
            node,
            children=True,
            fullPath=True
        ) or []

        for child in children:
            child_type = cmds.nodeType(child)
            if child_type in ("transform", "joint"):
                walk(child)

    walk(root)
    return result


def create_controller(
        name,
        shape="circle",
        radius=1.0,
        axis="Y+",
        target=None,
        parent=None,
        color=6,
        rotate_x=0.0,
        create_sub_control=True,
        create_extra_groups=True,
        add_to_set=True
):
    """
    创建标准绑定控制器。

    层级：
        zero
          driven
            space
              connect
                offset
                  ctrl
                    ctrlSub
                    output

    Returns:
        dict: 创建结果。
    """
    control_name = _safe_control_name(name)
    control_name = _next_available_name(control_name)

    shape_data = control_shape_tool.load_shape_data(shape)

    control = cmds.createNode("transform", name=control_name)
    control_shape_tool.apply_shape_data(control, shape_data)
    _transform_shape(
        control,
        radius=radius,
        axis=axis,
        rotate_x=rotate_x
    )
    _set_shape_color(control, color)

    groups = {}
    top_group = control

    if create_extra_groups:
        group_order = [
            "offset",
            "connect",
            "space",
            "driven",
            "zero",
        ]

        current_child = control
        for group_type in group_order:
            group_name = _replace_ctrl_prefix(
                control_name,
                group_type
            )
            group_name = _next_available_name(group_name)
            group = cmds.createNode("transform", name=group_name)
            cmds.parent(current_child, group)
            groups[group_type] = group
            current_child = group

        top_group = groups["zero"]

    sub_control = None
    if create_sub_control:
        sub_name = control_name + "Sub"
        sub_name = _next_available_name(sub_name)
        sub_control = cmds.createNode("transform", name=sub_name)
        control_shape_tool.apply_shape_data(sub_control, shape_data)
        _transform_shape(
            sub_control,
            radius=radius * 0.7,
            axis=axis,
            rotate_x=rotate_x
        )

        sub_color = min(int(color) + 1, 31)
        _set_shape_color(sub_control, sub_color)
        cmds.parent(sub_control, control)

        if not cmds.attributeQuery(
                "subCtrlVis",
                node=control,
                exists=True
        ):
            cmds.addAttr(
                control,
                longName="subCtrlVis",
                attributeType="bool",
                defaultValue=0
            )
            cmds.setAttr(
                control + ".subCtrlVis",
                channelBox=True
            )

        cmds.connectAttr(
            control + ".subCtrlVis",
            sub_control + ".visibility",
            force=True
        )

    output_name = _replace_ctrl_prefix(control_name, "output")
    output_name = _next_available_name(output_name)
    output = cmds.createNode(
        "transform",
        name=output_name,
        parent=control
    )

    driver = control
    if sub_control is not None:
        driver = sub_control

    connection_attrs = [
        "translate",
        "rotate",
        "scale",
        "rotateOrder",
    ]

    for attr in connection_attrs:
        cmds.connectAttr(
            "{}.{}".format(driver, attr),
            "{}.{}".format(output, attr),
            force=True
        )

    if target is not None:
        if not cmds.objExists(target):
            raise RuntimeError(u"吸附目标不存在：{}".format(target))

        cmds.matchTransform(
            top_group,
            target,
            position=True,
            rotation=True
        )

    if parent is not None:
        if not cmds.objExists(parent):
            raise RuntimeError(u"父节点不存在：{}".format(parent))
        cmds.parent(top_group, parent)

    if add_to_set:
        _add_to_control_set(control)

    result = {
        "control": control,
        "sub_control": sub_control,
        "output": output,
        "top_group": top_group,
        "groups": groups,
    }

    return result


class ControlButton(QToolButton):
    """Shape 单选按钮。"""

    def __init__(self, shape_name, parent=None):
        super(ControlButton, self).__init__(parent)

        self.shape_name = shape_name
        self.setCheckable(True)
        self.setFixedSize(105, 92)
        self.setToolTip(shape_name)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setIconSize(QSize(64, 64))

        jpg_path = os.path.join(
            control_shape_tool.get_library_dir(),
            "{}.jpg".format(shape_name)
        )

        if os.path.isfile(jpg_path):
            pixmap = QPixmap(jpg_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    64,
                    64,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.setIcon(QIcon(pixmap))

        display_name = shape_name
        if len(display_name) > 13:
            display_name = display_name[:12] + u"…"

        self.setText(display_name)


class ColorPreviewLabel(QLabel):
    def __init__(self, parent=None):
        super(ColorPreviewLabel, self).__init__(parent)
        self.setFixedSize(32, 32)
        self.setFrameShape(QFrame.StyledPanel)
        self.set_color(6)

    def set_color(self, index):
        rgb = MAYA_COLORS.get(index, (0.5, 0.5, 0.5))
        red = int(rgb[0] * 255)
        green = int(rgb[1] * 255)
        blue = int(rgb[2] * 255)

        self.setStyleSheet(
            "background-color: rgb({}, {}, {}); border: 1px solid #777;".format(
                red,
                green,
                blue
            )
        )
        self.setToolTip("Color Index: {}".format(index))


class ControlCreatorDialog(QDialog):
    """控制器创建界面。"""

    AXIS_LIST = ["X+", "X-", "Y+", "Y-", "Z+", "Z-"]

    def __init__(self, parent=None):
        if parent is None:
            parent = qtUtils.get_maya_window()

        super(ControlCreatorDialog, self).__init__(parent)

        self.setWindowTitle(u"Control Creator")
        self.resize(560, 720)

        self.current_shape = None
        self.shape_buttons = []
        self.shape_group = None

        self._create_widgets()
        self._create_layouts()
        self._create_connections()
        self._load_shapes()

    def _create_widgets(self):
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(u"搜索 Shape...")

        self.shape_scroll = QScrollArea()
        self.shape_scroll.setWidgetResizable(True)
        self.shape_scroll.setFrameShape(QFrame.NoFrame)

        self.shapes_widget = QWidget()
        self.shapes_layout = QGridLayout(self.shapes_widget)
        self.shapes_layout.setContentsMargins(4, 4, 4, 4)
        self.shapes_layout.setSpacing(6)
        self.shape_scroll.setWidget(self.shapes_widget)

        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.01, 1000.0)
        self.scale_spin.setDecimals(3)
        self.scale_spin.setValue(2.0)
        self.scale_spin.setSingleStep(0.25)

        self.axis_combo = QComboBox()
        self.axis_combo.addItems(self.AXIS_LIST)
        self.axis_combo.setCurrentText("Y+")

        self.rotate_x_spin = QDoubleSpinBox()
        self.rotate_x_spin.setRange(-3600.0, 3600.0)
        self.rotate_x_spin.setValue(0.0)

        self.match_combo = QComboBox()
        self.match_combo.addItems([
            u"选择物体",
            u"选择层级",
            u"原点",
        ])

        self.color_slider = QSlider(Qt.Horizontal)
        self.color_slider.setRange(0, 31)
        self.color_slider.setValue(6)

        self.color_spin = QSpinBox()
        self.color_spin.setRange(0, 31)
        self.color_spin.setValue(6)
        self.color_preview = ColorPreviewLabel()

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText(
            u"留空时根据目标名称自动生成 ctrl_*"
        )

        self.sub_control_check = QCheckBox(u"创建次级控制器")
        self.sub_control_check.setChecked(True)

        self.extra_groups_check = QCheckBox(u"创建标准层级组")
        self.extra_groups_check.setChecked(True)

        self.add_set_check = QCheckBox(u"加入 ctrl_set")
        self.add_set_check.setChecked(True)

        self.create_btn = QPushButton(u"创建控制器")
        self.refresh_btn = QPushButton(u"刷新 Shape 图库")

    def _create_layouts(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(self.search_edit)
        main_layout.addWidget(self.shape_scroll, 1)

        params_group = QGroupBox(u"创建参数")
        params_layout = QGridLayout(params_group)
        params_layout.addWidget(QLabel(u"大小:"), 0, 0)
        params_layout.addWidget(self.scale_spin, 0, 1)
        params_layout.addWidget(QLabel(u"轴向:"), 0, 2)
        params_layout.addWidget(self.axis_combo, 0, 3)
        params_layout.addWidget(QLabel(u"额外旋转 X:"), 1, 0)
        params_layout.addWidget(self.rotate_x_spin, 1, 1)
        params_layout.addWidget(QLabel(u"创建模式:"), 1, 2)
        params_layout.addWidget(self.match_combo, 1, 3)
        main_layout.addWidget(params_group)

        color_group = QGroupBox(u"颜色")
        color_layout = QHBoxLayout(color_group)
        color_layout.addWidget(self.color_slider, 1)
        color_layout.addWidget(self.color_spin)
        color_layout.addWidget(self.color_preview)
        main_layout.addWidget(color_group)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel(u"名称:"))
        name_layout.addWidget(self.name_edit, 1)
        main_layout.addLayout(name_layout)

        option_layout = QHBoxLayout()
        option_layout.addWidget(self.sub_control_check)
        option_layout.addWidget(self.extra_groups_check)
        option_layout.addWidget(self.add_set_check)
        main_layout.addLayout(option_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.create_btn, 1)
        main_layout.addLayout(button_layout)

    def _create_connections(self):
        self.search_edit.textChanged.connect(self._filter_shapes)
        self.color_slider.valueChanged.connect(self._sync_color)
        self.color_spin.valueChanged.connect(self._sync_color)
        self.create_btn.clicked.connect(self.create_controls)
        self.refresh_btn.clicked.connect(self._load_shapes)

    def _load_shapes(self):
        while self.shapes_layout.count():
            item = self.shapes_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.shape_buttons = []
        self.current_shape = None
        self.shape_group = QButtonGroup(self)
        self.shape_group.setExclusive(True)

        library_dir = control_shape_tool.get_library_dir()
        file_names = os.listdir(library_dir) if os.path.isdir(library_dir) else []
        shape_names = []

        for file_name in file_names:
            name, extension = os.path.splitext(file_name)
            if extension.lower() == ".json":
                shape_names.append(name)

        shape_names.sort()

        columns = 4
        index = 0
        for shape_name in shape_names:
            button = ControlButton(shape_name, self)
            self.shape_group.addButton(button)
            self.shapes_layout.addWidget(
                button,
                index // columns,
                index % columns
            )
            self.shape_buttons.append(button)
            index += 1

        self.shape_group.buttonClicked.connect(self._shape_selected)

        if self.shape_buttons:
            self.shape_buttons[0].setChecked(True)
            self.current_shape = self.shape_buttons[0].shape_name

    def _shape_selected(self, button):
        if button.isChecked():
            self.current_shape = button.shape_name

    def _filter_shapes(self, text):
        search_text = text.lower().strip()

        for button in self.shape_buttons:
            visible = search_text in button.shape_name.lower()
            button.setVisible(visible)

    def _sync_color(self, value):
        self.color_slider.blockSignals(True)
        self.color_spin.blockSignals(True)
        self.color_slider.setValue(value)
        self.color_spin.setValue(value)
        self.color_slider.blockSignals(False)
        self.color_spin.blockSignals(False)
        self.color_preview.set_color(value)

    def _targets_from_mode(self):
        mode = self.match_combo.currentText()

        if mode == u"原点":
            return []

        selections = cmds.ls(selection=True, long=True) or []
        if not selections:
            return []

        targets = []

        if mode == u"选择物体":
            for selection in selections:
                if selection not in targets:
                    targets.append(selection)
            return targets

        for selection in selections:
            hierarchy_nodes = _hierarchy_targets(selection)
            for node in hierarchy_nodes:
                if node not in targets:
                    targets.append(node)

        return targets

    def _requested_name(self, target, index, total):
        typed_name = self.name_edit.text().strip()

        if typed_name:
            if total == 1:
                return _safe_control_name(typed_name)

            return _safe_control_name(
                "{}_{:03d}".format(typed_name, index + 1)
            )

        if target is not None:
            return _name_from_target(target)

        return "ctrl_new_001"

    def create_controls(self):
        if not self.current_shape:
            cmds.warning(u"请先选择控制器 Shape。")
            return

        targets = self._targets_from_mode()
        mode = self.match_combo.currentText()

        if mode != u"原点" and not targets:
            cmds.warning(u"当前创建模式需要先选择目标物体。")
            return

        if mode == u"原点":
            targets = [None]

        created_controls = []
        target_control_map = {}

        cmds.undoInfo(openChunk=True, chunkName="MuziCreateControls")
        try:
            total = len(targets)
            index = 0

            while index < total:
                target = targets[index]
                control_name = self._requested_name(
                    target,
                    index,
                    total
                )

                parent_control = None

                if mode == u"选择层级" and target is not None:
                    parent_nodes = cmds.listRelatives(
                        target,
                        parent=True,
                        fullPath=True
                    ) or []

                    if parent_nodes:
                        parent_target = parent_nodes[0]
                        parent_control = target_control_map.get(parent_target)

                result = create_controller(
                    name=control_name,
                    shape=self.current_shape,
                    radius=self.scale_spin.value(),
                    axis=self.axis_combo.currentText(),
                    target=target,
                    parent=parent_control,
                    color=self.color_spin.value(),
                    rotate_x=self.rotate_x_spin.value(),
                    create_sub_control=self.sub_control_check.isChecked(),
                    create_extra_groups=self.extra_groups_check.isChecked(),
                    add_to_set=self.add_set_check.isChecked()
                )

                control = result["control"]
                created_controls.append(control)

                if target is not None:
                    target_control_map[target] = control

                index += 1

        except Exception as error:
            cmds.warning(u"创建控制器失败：{}".format(error))
        finally:
            cmds.undoInfo(closeChunk=True)

        if created_controls:
            cmds.select(created_controls, replace=True)
            print(
                u"[Control Creator] 已创建 {} 个控制器。".format(
                    len(created_controls)
                )
            )


def main():
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = ControlCreatorDialog()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window


if __name__ == "__main__":
    main()
