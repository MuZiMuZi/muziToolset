# coding=utf-8
u"""
Control Creator
===============

Maya 2023 / PySide2 控制器创建工具。

功能：
    1. 从 MuziTools/image 读取控制器 Shape JSON；
    2. 使用缩略图图库选择 Shape；
    3. 设置大小、轴向、额外 X 旋转与 Maya Color Index；
    4. 根据当前选择物体、选择层级或世界原点创建控制器；
    5. 可创建标准 zero / driven / space / connect / offset 层级；
    6. 可创建次级控制器和 output 节点；
    7. 可自动加入 ctrl_set。

说明：
    - 场景操作统一使用 maya.cmds，不使用 pymel。
    - Shape 图库使用 QListWidget IconMode，图片和名称分离显示，避免文字与缩略图重叠。
    - main() 只创建并返回窗口，由 MuziTools.window_manager 负责显示和生命周期。
"""

from __future__ import print_function

import os

import maya.cmds as cmds

try:
    from PySide2.QtCore import QSize
    from PySide2.QtCore import Qt
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
    from PySide2.QtWidgets import QSlider
    from PySide2.QtWidgets import QSpinBox
    from PySide2.QtWidgets import QVBoxLayout
except ImportError:
    from PySide6.QtCore import QSize
    from PySide6.QtCore import Qt
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
    from PySide6.QtWidgets import QSlider
    from PySide6.QtWidgets import QSpinBox
    from PySide6.QtWidgets import QVBoxLayout

from ... import ui_theme
from . import control_shape_tool


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


axis_rotation = {
    "X+": (90.0, 0.0, 0.0),
    "X-": (-90.0, 0.0, 0.0),
    "Y+": (0.0, 90.0, 0.0),
    "Y-": (0.0, -90.0, 0.0),
    "Z+": (0.0, 0.0, 90.0),
    "Z-": (0.0, 0.0, -90.0),
}


axis_list = [
    "X+",
    "X-",
    "Y+",
    "Y-",
    "Z+",
    "Z-",
]


def _short_name(node):
    """获取 DAG 节点短名称。"""
    return node.split("|")[-1].replace(":", "_")


def _safe_control_name(name):
    """整理控制器名称并确保带 ctrl_ 前缀。"""
    clean_name = name.replace("|", "_").replace(":", "_").strip()

    if not clean_name:
        clean_name = "ctrl_new_001"

    if not clean_name.startswith("ctrl_"):
        clean_name = "ctrl_" + clean_name

    return clean_name


def _name_from_target(target):
    """根据驱动目标名称生成控制器名称。"""
    short_name = _short_name(target)

    if short_name.startswith("jnt_"):
        return short_name.replace("jnt_", "ctrl_", 1)

    if short_name.startswith("bpjnt_"):
        return short_name.replace("bpjnt_", "ctrl_", 1)

    return _safe_control_name(short_name)


def _next_available_name(name):
    """返回场景中未被占用的节点名称。"""
    if not cmds.objExists(name):
        return name

    index = 1

    while True:
        candidate = "{}_{:03d}".format(name, index)

        if not cmds.objExists(candidate):
            return candidate

        index += 1


def _replace_ctrl_prefix(name, prefix):
    """把 ctrl_ 前缀替换成指定层级前缀。"""
    if name.startswith("ctrl_"):
        return name.replace("ctrl_", prefix + "_", 1)

    return "{}_{}".format(prefix, name)


def _curve_shapes(transform):
    """获取控制器 Transform 下的 NurbsCurve Shape。"""
    shapes = cmds.listRelatives(
        transform,
        shapes=True,
        noIntermediate=True,
        fullPath=True,
        type="nurbsCurve"
    )

    if shapes is None:
        shapes = []

    return shapes


def _shape_cvs(transform):
    """获取控制器全部 CV。"""
    cvs = []
    shapes = _curve_shapes(transform)

    for shape in shapes:
        shape_cvs = cmds.ls(
            shape + ".cv[*]",
            flatten=True
        )

        if shape_cvs is None:
            shape_cvs = []

        for cv in shape_cvs:
            cvs.append(cv)

    return cvs


def _set_shape_color(transform, color_index):
    """设置控制器 Shape 的 Maya Index Color。"""
    shapes = _curve_shapes(transform)

    for shape in shapes:
        cmds.setAttr(shape + ".overrideEnabled", 1)
        cmds.setAttr(shape + ".overrideRGBColors", 0)
        cmds.setAttr(shape + ".overrideColor", int(color_index))


def _transform_shape(transform, radius, axis, rotate_x=0.0):
    """直接修改 CV，实现 Shape 大小和轴向变换。"""
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

    rotation_value = axis_rotation.get(
        axis,
        (0.0, 0.0, 0.0)
    )

    rotate_x_value = rotation_value[0] + float(rotate_x)

    cmds.rotate(
        rotate_x_value,
        rotation_value[1],
        rotation_value[2],
        cvs,
        relative=True,
        objectSpace=True
    )


def _add_to_control_set(control):
    """把控制器添加到 ctrl_set。"""
    set_name = "ctrl_set"

    if not cmds.objExists(set_name):
        cmds.sets(
            name=set_name,
            empty=True
        )

    cmds.sets(
        control,
        add=set_name
    )


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
        )

        if children is None:
            children = []

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

    标准层级：
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

    control = cmds.createNode(
        "transform",
        name=control_name
    )

    control_shape_tool.apply_shape_data(
        control,
        shape_data
    )

    _transform_shape(
        control,
        radius=radius,
        axis=axis,
        rotate_x=rotate_x
    )

    _set_shape_color(
        control,
        color
    )

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

            group = cmds.createNode(
                "transform",
                name=group_name
            )

            cmds.parent(
                current_child,
                group
            )

            groups[group_type] = group
            current_child = group

        top_group = groups["zero"]

    sub_control = None

    if create_sub_control:
        sub_name = control_name + "Sub"
        sub_name = _next_available_name(sub_name)

        sub_control = cmds.createNode(
            "transform",
            name=sub_name
        )

        control_shape_tool.apply_shape_data(
            sub_control,
            shape_data
        )

        _transform_shape(
            sub_control,
            radius=radius * 0.7,
            axis=axis,
            rotate_x=rotate_x
        )

        sub_color = min(
            int(color) + 1,
            31
        )

        _set_shape_color(
            sub_control,
            sub_color
        )

        cmds.parent(
            sub_control,
            control
        )

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

    output_name = _replace_ctrl_prefix(
        control_name,
        "output"
    )
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
            raise RuntimeError(
                u"吸附目标不存在：{}".format(target)
            )

        cmds.matchTransform(
            top_group,
            target,
            position=True,
            rotation=True
        )

    if parent is not None:
        if not cmds.objExists(parent):
            raise RuntimeError(
                u"父节点不存在：{}".format(parent)
            )

        cmds.parent(
            top_group,
            parent
        )

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


class ColorPreviewLabel(QLabel):
    """显示当前 Maya Color Index 对应的颜色。"""

    def __init__(self, parent=None):
        super(ColorPreviewLabel, self).__init__(parent)
        self.setFixedSize(34, 34)
        self.set_color(6)

    def set_color(self, index):
        rgb = maya_colors.get(
            index,
            (0.5, 0.5, 0.5)
        )

        red = int(rgb[0] * 255)
        green = int(rgb[1] * 255)
        blue = int(rgb[2] * 255)

        self.setStyleSheet(
            u"background-color: rgb({}, {}, {}); "
            u"border: 1px solid {}; "
            u"border-radius: 7px;".format(
                red,
                green,
                blue,
                ui_theme.BORDER
            )
        )

        self.setToolTip(
            "Color Index: {}".format(index)
        )


class ControlCreatorDialog(QDialog):
    """控制器创建界面。"""

    def __init__(self, parent=None):
        super(ControlCreatorDialog, self).__init__(parent)

        self.current_shape = None

        ui_theme.style_window(
            self,
            title=u"Control Creator",
            minimum_width=620
        )

        self.resize(680, 820)
        self.setMinimumHeight(640)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.load_shapes()

    # -------------------------------------------------------------------------
    # 创建界面部件
    # -------------------------------------------------------------------------

    def create_widgets(self):
        self.title_label = ui_theme.make_title(
            u"Control Creator"
        )

        self.subtitle_label = ui_theme.make_subtitle(
            u"从 Shape 图库选择控制器外形，再设置大小、轴向、颜色和创建方式。"
        )

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(u"搜索 Shape...")
        self.search_edit.setClearButtonEnabled(True)

        # 使用 QListWidget 的 IconMode 作为 Shape Gallery。
        # Qt 会自动处理“缩略图在上、名称在下”的布局，不再依赖 ToolButton 的
        # TextUnderIcon，从根本上避免旧版图片和文字互相覆盖。
        self.shape_list = QListWidget()
        self.shape_list.setViewMode(QListView.IconMode)
        self.shape_list.setResizeMode(QListView.Adjust)
        self.shape_list.setMovement(QListView.Static)
        self.shape_list.setWrapping(True)
        self.shape_list.setWordWrap(False)
        self.shape_list.setUniformItemSizes(True)
        self.shape_list.setSpacing(8)
        self.shape_list.setIconSize(QSize(72, 72))
        self.shape_list.setGridSize(QSize(132, 118))
        self.shape_list.setMinimumHeight(330)
        self.shape_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )
        self.shape_list.setVerticalScrollMode(
            QListView.ScrollPerPixel
        )

        self.shape_count_label = QLabel()
        ui_theme.set_role(
            self.shape_count_label,
            "muted"
        )

        self.refresh_button = QPushButton(u"刷新图库")
        ui_theme.style_ghost(self.refresh_button)

        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.01, 1000.0)
        self.scale_spin.setDecimals(3)
        self.scale_spin.setValue(2.0)
        self.scale_spin.setSingleStep(0.25)

        self.axis_combo = QComboBox()

        for axis_name in axis_list:
            self.axis_combo.addItem(axis_name)

        self.axis_combo.setCurrentText("Y+")

        self.rotate_x_spin = QDoubleSpinBox()
        self.rotate_x_spin.setRange(-3600.0, 3600.0)
        self.rotate_x_spin.setDecimals(2)
        self.rotate_x_spin.setValue(0.0)

        self.match_combo = QComboBox()
        self.match_combo.addItem(u"选择物体")
        self.match_combo.addItem(u"选择层级")
        self.match_combo.addItem(u"原点")

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

        self.create_button = QPushButton(u"创建控制器")
        self.create_button.setMinimumHeight(38)
        ui_theme.style_primary(self.create_button)

        self.status_label = QLabel(u"请选择一个 Shape。")
        ui_theme.set_role(
            self.status_label,
            "muted"
        )

    # -------------------------------------------------------------------------
    # 创建布局
    # -------------------------------------------------------------------------

    def create_layouts(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        gallery_card, gallery_layout = ui_theme.make_card()
        gallery_layout.addWidget(
            ui_theme.make_section_title(u"Shape 图库")
        )
        gallery_layout.addWidget(self.search_edit)
        gallery_layout.addWidget(self.shape_list, 1)

        gallery_footer_layout = QHBoxLayout()
        gallery_footer_layout.setContentsMargins(0, 0, 0, 0)
        gallery_footer_layout.addWidget(self.shape_count_label)
        gallery_footer_layout.addStretch(1)
        gallery_footer_layout.addWidget(self.refresh_button)
        gallery_layout.addLayout(gallery_footer_layout)

        main_layout.addWidget(gallery_card, 1)

        parameter_card, parameter_layout = ui_theme.make_card()
        parameter_layout.addWidget(
            ui_theme.make_section_title(u"创建参数")
        )

        parameter_grid = QGridLayout()
        parameter_grid.setHorizontalSpacing(12)
        parameter_grid.setVerticalSpacing(8)

        parameter_grid.addWidget(QLabel(u"大小"), 0, 0)
        parameter_grid.addWidget(self.scale_spin, 0, 1)
        parameter_grid.addWidget(QLabel(u"轴向"), 0, 2)
        parameter_grid.addWidget(self.axis_combo, 0, 3)

        parameter_grid.addWidget(QLabel(u"额外旋转 X"), 1, 0)
        parameter_grid.addWidget(self.rotate_x_spin, 1, 1)
        parameter_grid.addWidget(QLabel(u"创建模式"), 1, 2)
        parameter_grid.addWidget(self.match_combo, 1, 3)

        parameter_grid.setColumnStretch(1, 1)
        parameter_grid.setColumnStretch(3, 1)
        parameter_layout.addLayout(parameter_grid)

        main_layout.addWidget(parameter_card)

        color_card, color_layout = ui_theme.make_card()
        color_layout.addWidget(
            ui_theme.make_section_title(u"颜色")
        )

        color_row_layout = QHBoxLayout()
        color_row_layout.setContentsMargins(0, 0, 0, 0)
        color_row_layout.addWidget(self.color_slider, 1)
        color_row_layout.addWidget(self.color_spin)
        color_row_layout.addWidget(self.color_preview)
        color_layout.addLayout(color_row_layout)

        main_layout.addWidget(color_card)

        option_card, option_layout = ui_theme.make_card()
        option_layout.addWidget(
            ui_theme.make_section_title(u"名称与层级")
        )

        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.addWidget(QLabel(u"名称"))
        name_layout.addWidget(self.name_edit, 1)
        option_layout.addLayout(name_layout)

        option_check_layout = QHBoxLayout()
        option_check_layout.setContentsMargins(0, 0, 0, 0)
        option_check_layout.addWidget(self.sub_control_check)
        option_check_layout.addWidget(self.extra_groups_check)
        option_check_layout.addWidget(self.add_set_check)
        option_check_layout.addStretch(1)
        option_layout.addLayout(option_check_layout)

        main_layout.addWidget(option_card)
        main_layout.addWidget(self.create_button)
        main_layout.addWidget(self.status_label)

    # -------------------------------------------------------------------------
    # 信号
    # -------------------------------------------------------------------------

    def create_connections(self):
        self.search_edit.textChanged.connect(
            self.filter_shapes
        )
        self.shape_list.currentItemChanged.connect(
            self.shape_selected
        )
        self.color_slider.valueChanged.connect(
            self.sync_color
        )
        self.color_spin.valueChanged.connect(
            self.sync_color
        )
        self.create_button.clicked.connect(
            self.create_controls
        )
        self.refresh_button.clicked.connect(
            self.load_shapes
        )

    # -------------------------------------------------------------------------
    # Shape Gallery
    # -------------------------------------------------------------------------

    def get_shape_names(self):
        """读取 Shape JSON 名称。"""
        library_dir = control_shape_tool.get_library_dir()
        file_names = []

        if os.path.isdir(library_dir):
            file_names = os.listdir(library_dir)

        shape_names = []

        for file_name in file_names:
            name, extension = os.path.splitext(file_name)

            if extension.lower() != ".json":
                continue

            if name not in shape_names:
                shape_names.append(name)

        shape_names.sort()
        return shape_names

    def create_shape_item(self, shape_name):
        """创建一个图库 Item。"""
        display_name = shape_name

        if len(display_name) > 18:
            display_name = display_name[:17] + u"…"

        item = QListWidgetItem(display_name)
        item.setData(Qt.UserRole, shape_name)
        item.setToolTip(shape_name)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignTop)
        item.setSizeHint(QSize(126, 112))

        jpg_path = os.path.join(
            control_shape_tool.get_library_dir(),
            "{}.jpg".format(shape_name)
        )

        if os.path.isfile(jpg_path):
            pixmap = QPixmap(jpg_path)

            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    72,
                    72,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                item.setIcon(QIcon(pixmap))

        return item

    def load_shapes(self):
        """重新读取并显示 Shape 图库。"""
        previous_shape = self.current_shape

        self.shape_list.blockSignals(True)
        self.shape_list.clear()
        self.current_shape = None

        shape_names = self.get_shape_names()
        selected_item = None

        for shape_name in shape_names:
            item = self.create_shape_item(shape_name)
            self.shape_list.addItem(item)

            if shape_name == previous_shape:
                selected_item = item

        if selected_item is None:
            if self.shape_list.count() > 0:
                selected_item = self.shape_list.item(0)

        if selected_item is not None:
            self.shape_list.setCurrentItem(selected_item)
            self.current_shape = selected_item.data(Qt.UserRole)

        self.shape_list.blockSignals(False)

        self.filter_shapes(
            self.search_edit.text()
        )

        self.update_shape_count()

        if self.current_shape:
            self.status_label.setText(
                u"当前 Shape：{}".format(self.current_shape)
            )
        else:
            self.status_label.setText(
                u"Shape 图库为空，请检查 MuziTools/image。"
            )

    def shape_selected(self, current_item, previous_item):
        """记录当前选择的 Shape。"""
        if current_item is None:
            return

        shape_name = current_item.data(Qt.UserRole)

        if not shape_name:
            return

        self.current_shape = shape_name
        self.status_label.setText(
            u"当前 Shape：{}".format(shape_name)
        )

    def filter_shapes(self, text):
        """按名称过滤图库。"""
        search_text = text.lower().strip()
        index = 0

        while index < self.shape_list.count():
            item = self.shape_list.item(index)
            shape_name = item.data(Qt.UserRole)

            if shape_name is None:
                shape_name = ""

            visible = search_text in shape_name.lower()
            item.setHidden(not visible)
            index += 1

        self.update_shape_count()

    def update_shape_count(self):
        """更新 Shape 数量提示。"""
        total_count = self.shape_list.count()
        visible_count = 0
        index = 0

        while index < total_count:
            item = self.shape_list.item(index)

            if not item.isHidden():
                visible_count += 1

            index += 1

        self.shape_count_label.setText(
            u"显示 {} / {} 个 Shape".format(
                visible_count,
                total_count
            )
        )

    # -------------------------------------------------------------------------
    # 参数
    # -------------------------------------------------------------------------

    def sync_color(self, value):
        """同步 Slider、SpinBox 和颜色预览。"""
        self.color_slider.blockSignals(True)
        self.color_spin.blockSignals(True)

        self.color_slider.setValue(value)
        self.color_spin.setValue(value)

        self.color_slider.blockSignals(False)
        self.color_spin.blockSignals(False)

        self.color_preview.set_color(value)

    def targets_from_mode(self):
        """根据创建模式获取目标列表。"""
        mode = self.match_combo.currentText()

        if mode == u"原点":
            return []

        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

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

    def requested_name(self, target, index, total):
        """计算当前控制器需要使用的名称。"""
        typed_name = self.name_edit.text().strip()

        if typed_name:
            if total == 1:
                return _safe_control_name(typed_name)

            numbered_name = "{}_{:03d}".format(
                typed_name,
                index + 1
            )

            return _safe_control_name(numbered_name)

        if target is not None:
            return _name_from_target(target)

        return "ctrl_new_001"

    # -------------------------------------------------------------------------
    # 创建控制器
    # -------------------------------------------------------------------------

    def create_controls(self):
        """根据界面参数创建控制器。"""
        if not self.current_shape:
            cmds.warning(u"请先选择控制器 Shape。")
            return

        targets = self.targets_from_mode()
        mode = self.match_combo.currentText()

        if mode != u"原点" and not targets:
            cmds.warning(u"当前创建模式需要先选择目标物体。")
            return

        if mode == u"原点":
            targets = [None]

        created_controls = []
        target_control_map = {}

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziCreateControls"
        )

        try:
            total = len(targets)
            index = 0

            while index < total:
                target = targets[index]

                control_name = self.requested_name(
                    target,
                    index,
                    total
                )

                parent_control = None

                if mode == u"选择层级":
                    if target is not None:
                        parent_nodes = cmds.listRelatives(
                            target,
                            parent=True,
                            fullPath=True
                        )

                        if parent_nodes is None:
                            parent_nodes = []

                        if parent_nodes:
                            parent_target = parent_nodes[0]
                            parent_control = target_control_map.get(
                                parent_target
                            )

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
            cmds.warning(
                u"创建控制器失败：{}".format(error)
            )
        finally:
            cmds.undoInfo(closeChunk=True)

        if not created_controls:
            self.status_label.setText(u"没有创建控制器。")
            return

        cmds.select(
            created_controls,
            replace=True
        )

        self.status_label.setText(
            u"已创建 {} 个控制器。".format(
                len(created_controls)
            )
        )

        print(
            u"[Control Creator] 已创建 {} 个控制器。".format(
                len(created_controls)
            )
        )


def main():
    """创建并返回 Control Creator 窗口。"""
    window = ControlCreatorDialog()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
