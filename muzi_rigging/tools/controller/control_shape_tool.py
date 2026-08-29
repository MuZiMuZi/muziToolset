# coding=utf-8
u"""
Control Shape Tool
==================

Maya Controller Shape 图库与编辑工具。

职责：
    1. 从正式资源目录读取 Controller Shape JSON / 缩略图；
    2. 把 Shape 应用到当前控制器；
    3. 上传、删除和刷新 Shape 数据；
    4. 修改 Maya Index Color；
    5. 旋转、缩放、镜像和替换 Curve Shape。

说明：
    - 场景操作统一使用 maya.cmds；
    - 不依赖 PyMel；
    - 不自己保存全局窗口引用；
    - main() 只创建并返回 QWidget，由 app.window_manager 统一管理生命周期。
"""

from __future__ import print_function

import json
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

from ... import config
from ...ui import theme


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


def get_library_dir():
    """返回正式 Controller Shape 资源目录。"""
    return config.controller_shapes_dir


def get_curve_shapes(transform):
    """返回 Transform 下全部非 Intermediate NURBS Curve Shape。"""
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


def get_selected_curve_transforms():
    """返回 Maya 当前选择中的 Curve Transform。"""
    selections = cmds.ls(
        selection=True,
        long=True,
        objectsOnly=True
    )

    if selections is None:
        selections = []

    transforms = []

    for selected_node in selections:
        node = selected_node
        node_type = cmds.nodeType(node)

        if node_type == "nurbsCurve":
            parent_nodes = cmds.listRelatives(
                node,
                parent=True,
                fullPath=True
            )

            if parent_nodes:
                node = parent_nodes[0]

        if cmds.nodeType(node) != "transform":
            continue

        curve_shapes = get_curve_shapes(node)

        if not curve_shapes:
            continue

        if node not in transforms:
            transforms.append(node)

    return transforms


def get_shape_data_from_transform(transform):
    """把控制器 Transform 的全部 Curve Shape 转成可保存 JSON 数据。"""
    result = []
    curve_shapes = get_curve_shapes(transform)

    for curve_shape in curve_shapes:
        degree = cmds.getAttr(
            curve_shape + ".degree"
        )
        form = cmds.getAttr(
            curve_shape + ".form"
        )
        periodic = form == 2

        cvs = cmds.ls(
            curve_shape + ".cv[*]",
            flatten=True
        )

        if cvs is None:
            cvs = []

        points = []

        for cv in cvs:
            position = cmds.xform(
                cv,
                query=True,
                objectSpace=True,
                translation=True
            )

            for value in position:
                points.append(value)

        knot_count = cmds.getAttr(
            curve_shape + ".knots",
            size=True
        )

        knots = []

        for knot_index in range(knot_count):
            knot_value = cmds.getAttr(
                "{}.knots[{}]".format(
                    curve_shape,
                    knot_index
                )
            )
            knots.append(knot_value)

        shape_data = {
            "points": points,
            "degree": degree,
            "periodic": periodic,
            "knot": knots,
        }
        result.append(shape_data)

    return result


def create_temp_curve(shape_data):
    """根据单个 Shape 数据创建临时 Curve Transform。"""
    points_flat = shape_data.get("points") or []
    degree = int(shape_data.get("degree", 1))
    periodic = bool(shape_data.get("periodic", False))
    knots = shape_data.get("knot") or []

    points = []
    point_index = 0

    while point_index + 2 < len(points_flat):
        point = [
            points_flat[point_index],
            points_flat[point_index + 1],
            points_flat[point_index + 2],
        ]
        points.append(point)
        point_index += 3

    if not points:
        raise RuntimeError(u"Shape 数据没有有效 CV 点。")

    if periodic:
        extra_points = []

        for extra_index in range(degree):
            if extra_index >= len(points):
                break

            extra_points.append(points[extra_index])

        for point in extra_points:
            points.append(point)

    create_kwargs = {
        "degree": degree,
        "point": points,
        "periodic": periodic,
    }

    if knots:
        create_kwargs["knot"] = knots

    temp_curve = cmds.curve(**create_kwargs)
    return temp_curve


def apply_shape_data(transform, shape_data_list):
    """使用 Shape JSON 数据替换 Transform 下现有 Curve Shape。"""
    if not cmds.objExists(transform):
        raise RuntimeError(
            u"控制器不存在：{}".format(transform)
        )

    old_shapes = get_curve_shapes(transform)

    if old_shapes:
        cmds.delete(old_shapes)

    short_name = transform.split("|")[-1]
    shape_index = 0

    for shape_data in shape_data_list:
        temp_curve = create_temp_curve(shape_data)
        temp_shapes = get_curve_shapes(temp_curve)

        if not temp_shapes:
            cmds.delete(temp_curve)
            continue

        temp_shape = temp_shapes[0]

        cmds.parent(
            temp_shape,
            transform,
            shape=True,
            relative=True
        )

        new_shape_name = "{}Shape".format(short_name)

        if shape_index > 0:
            new_shape_name = "{}Shape{}".format(
                short_name,
                shape_index + 1
            )

        cmds.rename(
            temp_shape,
            new_shape_name
        )
        cmds.delete(temp_curve)
        shape_index += 1

    return transform


def load_shape_data(shape_name):
    """从 Controller Shape 资源目录读取 JSON。"""
    file_path = os.path.join(
        get_library_dir(),
        "{}.json".format(shape_name)
    )

    if not os.path.isfile(file_path):
        raise RuntimeError(
            u"控制器 Shape 文件不存在：{}".format(file_path)
        )

    with open(file_path, "r") as file_object:
        data = json.load(file_object)

    return data


def save_shape_data(shape_name, transform):
    """把控制器 Curve Shape 保存为 JSON。"""
    if not shape_name:
        raise RuntimeError(u"Shape 名称不能为空。")

    data = get_shape_data_from_transform(transform)

    if not data:
        raise RuntimeError(
            u"所选对象没有 NURBS Curve Shape。"
        )

    library_dir = get_library_dir()

    if not os.path.isdir(library_dir):
        os.makedirs(library_dir)

    file_path = os.path.join(
        library_dir,
        "{}.json".format(shape_name)
    )

    with open(file_path, "w") as file_object:
        json.dump(
            data,
            file_object,
            ensure_ascii=False,
            indent=4
        )

    return file_path


class ShapeListWidget(QListWidget):
    """Controller Shape JSON 图库。"""

    def __init__(self, parent=None):
        super(ShapeListWidget, self).__init__(parent)

        self.setMovement(QListWidget.Static)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(82, 82))
        self.setGridSize(QSize(124, 112))
        self.setResizeMode(QListWidget.Adjust)
        self.setSpacing(4)
        self.setMinimumHeight(300)

        self.create_menu()
        self.create_connections()
        self.refresh()

    def create_menu(self):
        """创建 Shape 图库右键菜单。"""
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
        """连接 Shape 图库信号。"""
        self.itemDoubleClicked.connect(
            self.apply_item_shape
        )

    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())

    def refresh(self):
        """重新扫描 Controller Shape 资源目录。"""
        self.clear()

        library_dir = get_library_dir()

        if not os.path.isdir(library_dir):
            os.makedirs(library_dir)

        file_names = os.listdir(library_dir)
        json_names = []

        for file_name in file_names:
            shape_name, extension = os.path.splitext(file_name)

            if extension.lower() != ".json":
                continue

            json_names.append(shape_name)

        json_names.sort()

        for shape_name in json_names:
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
        """双击图库项目时应用 Shape。"""
        self.apply_shape_name(item.text())

    def apply_selected_shape(self):
        """应用当前第一个选中的图库 Shape。"""
        items = self.selectedItems()

        if not items:
            cmds.warning(u"请先在图库中选择一个 Shape。")
            return

        self.apply_shape_name(items[0].text())

    @staticmethod
    def apply_shape_name(shape_name):
        """把指定 Shape 应用到选择控制器，或创建新控制器。"""
        data = load_shape_data(shape_name)
        transforms = get_selected_curve_transforms()

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziApplyControlShape"
        )

        try:
            if transforms:
                for transform in transforms:
                    apply_shape_data(
                        transform,
                        data
                    )
            else:
                transform = cmds.createNode(
                    "transform",
                    name="ctrl_{}".format(shape_name)
                )
                apply_shape_data(
                    transform,
                    data
                )
                cmds.select(
                    transform,
                    replace=True
                )
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    def upload_control(self):
        """把当前一个 Curve Controller 保存进图库。"""
        transforms = get_selected_curve_transforms()

        if len(transforms) != 1:
            cmds.warning(
                u"上传 Shape 时请只选择一个 Curve 控制器。"
            )
            return

        default_name = transforms[0].split("|")[-1]

        shape_name, accepted = QInputDialog.getText(
            self,
            u"上传控制器 Shape",
            u"Shape 名称:",
            text=default_name
        )

        if not accepted:
            return

        shape_name = shape_name.strip()

        if not shape_name:
            return

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

        try:
            file_path = save_shape_data(
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
        """删除选中 Shape 对应的 JSON 和缩略图。"""
        items = self.selectedItems()

        if not items:
            cmds.warning(
                u"请选择需要删除的图库 Shape。"
            )
            return

        library_dir = get_library_dir()

        for item in items:
            shape_name = item.text()
            extensions = [
                ".json",
                ".jpg",
                ".png",
            ]

            for extension in extensions:
                file_path = os.path.join(
                    library_dir,
                    shape_name + extension
                )

                if not os.path.isfile(file_path):
                    continue

                try:
                    os.remove(file_path)
                except OSError as error:
                    cmds.warning(str(error))

        self.refresh()


class ColorListWidget(QListWidget):
    """Maya Index Color 选择器。"""

    def __init__(self, parent=None):
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
        """创建 Maya Index Color 项目。"""
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
        """把 Index Color 应用到选择控制器 Shape。"""
        color_index = item.data(Qt.UserRole)
        transforms = get_selected_curve_transforms()

        if not transforms:
            cmds.warning(u"请先选择 Curve 控制器。")
            return

        for transform in transforms:
            curve_shapes = get_curve_shapes(transform)

            for curve_shape in curve_shapes:
                cmds.setAttr(
                    curve_shape + ".overrideEnabled",
                    1
                )
                cmds.setAttr(
                    curve_shape + ".overrideRGBColors",
                    0
                )
                cmds.setAttr(
                    curve_shape + ".overrideColor",
                    int(color_index)
                )


class ControlShapeTool(QWidget):
    """Controller Shape 图库主窗口。"""

    def __init__(self, parent=None):
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
        """创建窗口控件。"""
        self.title_label = theme.make_title(
            u"控制器 Shape 图库"
        )
        self.subtitle_label = theme.make_subtitle(
            u"统一管理 Controller Shape、颜色和 CV 级别编辑。双击图库项目可直接应用。"
        )

        self.library_path_label = QLabel(
            get_library_dir()
        )
        self.library_path_label.setWordWrap(True)
        theme.set_role(
            self.library_path_label,
            "muted"
        )

        self.shape_list = ShapeListWidget(self)
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
        theme.style_ghost(self.refresh_button)

    def create_layouts(self):
        """创建统一 Card 布局。"""
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
        main_layout.addStretch(1)

    def create_connections(self):
        """连接窗口信号。"""
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

    @staticmethod
    def get_selected_cvs():
        """返回当前选择控制器的全部 Curve CV。"""
        transforms = get_selected_curve_transforms()
        cvs = []

        for transform in transforms:
            curve_shapes = get_curve_shapes(transform)

            for curve_shape in curve_shapes:
                shape_cvs = cmds.ls(
                    curve_shape + ".cv[*]",
                    flatten=True
                )

                if shape_cvs is None:
                    shape_cvs = []

                for cv in shape_cvs:
                    cvs.append(cv)

        return cvs

    def rotate_shapes(self):
        """旋转选择控制器的 Shape CV。"""
        cvs = self.get_selected_cvs()

        if not cvs:
            cmds.warning(u"请先选择 Curve 控制器。")
            return

        angle = self.rotate_spin.value()
        rotate_x = 0.0
        rotate_y = 0.0
        rotate_z = 0.0

        if self.rotate_x_check.isChecked():
            rotate_x = angle

        if self.rotate_y_check.isChecked():
            rotate_y = angle

        if self.rotate_z_check.isChecked():
            rotate_z = angle

        cmds.rotate(
            rotate_x,
            rotate_y,
            rotate_z,
            cvs,
            relative=True,
            objectSpace=True
        )

    def scale_shapes(self):
        """统一缩放选择控制器的 Shape CV。"""
        cvs = self.get_selected_cvs()

        if not cvs:
            cmds.warning(u"请先选择 Curve 控制器。")
            return

        scale_value = self.scale_spin.value()

        cmds.scale(
            scale_value,
            scale_value,
            scale_value,
            cvs,
            relative=True,
            objectSpace=True
        )

    def mirror_x_shapes(self):
        self.mirror_shapes("x")

    def mirror_y_shapes(self):
        self.mirror_shapes("y")

    def mirror_z_shapes(self):
        self.mirror_shapes("z")

    def mirror_shapes(self, axis):
        """沿给定轴镜像选择控制器的 Shape CV。"""
        cvs = self.get_selected_cvs()

        if not cvs:
            cmds.warning(u"请先选择 Curve 控制器。")
            return

        scale_x = 1.0
        scale_y = 1.0
        scale_z = 1.0

        if axis == "x":
            scale_x = -1.0
        elif axis == "y":
            scale_y = -1.0
        elif axis == "z":
            scale_z = -1.0

        cmds.scale(
            scale_x,
            scale_y,
            scale_z,
            cvs,
            relative=True,
            objectSpace=True
        )

    @staticmethod
    def replace_shapes():
        """用最后选择控制器的 Shape 替换前面选择对象。"""
        transforms = get_selected_curve_transforms()

        if len(transforms) < 2:
            cmds.warning(
                u"至少选择两个控制器，最后选择的对象作为 Shape 来源。"
            )
            return

        source = transforms[-1]
        targets = transforms[:-1]
        source_data = get_shape_data_from_transform(source)

        if not source_data:
            cmds.warning(
                u"Shape 来源没有 NURBS Curve Shape。"
            )
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziReplaceControlShapes"
        )

        try:
            for target in targets:
                apply_shape_data(
                    target,
                    source_data
                )
        finally:
            cmds.undoInfo(closeChunk=True)


def main():
    """创建并返回 Controller Shape 工具。"""
    window = ControlShapeTool()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
