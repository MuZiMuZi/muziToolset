# coding=utf-8
u"""
Control Shape Tool
==================

Maya 2023 / PySide2 控制器 Shape 图库。

本模块直接使用 maya.cmds 处理 NURBS Curve Shape，不再依赖旧的
``Control_Tool_main.py`` 或 PyMel。
"""

from __future__ import print_function

import json
import os

import maya.cmds as cmds

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

from ....core import qtUtils


_window = None


INDEX_RGB_MAP = [
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
    """返回 MuziTools/image 目录。"""
    module_dir = os.path.dirname(os.path.abspath(__file__))
    tools_dir = os.path.dirname(module_dir)
    muzi_tools_dir = os.path.dirname(tools_dir)
    return os.path.join(muzi_tools_dir, "image")


def _curve_shapes(transform):
    shapes = cmds.listRelatives(
        transform,
        shapes=True,
        noIntermediate=True,
        fullPath=True,
        type="nurbsCurve"
    ) or []
    return shapes


def _selected_curve_transforms():
    selections = cmds.ls(selection=True, long=True, objectsOnly=True) or []
    transforms = []

    for node in selections:
        node_type = cmds.nodeType(node)

        if node_type == "nurbsCurve":
            parents = cmds.listRelatives(node, parent=True, fullPath=True) or []
            if parents:
                node = parents[0]

        if cmds.nodeType(node) != "transform":
            continue

        if not _curve_shapes(node):
            continue

        if node not in transforms:
            transforms.append(node)

    return transforms


def _shape_data_from_transform(transform):
    """把一个控制器 Transform 的全部 Curve Shape 转成 JSON 数据。"""
    result = []
    shapes = _curve_shapes(transform)

    for shape in shapes:
        degree = cmds.getAttr(shape + ".degree")
        form = cmds.getAttr(shape + ".form")
        periodic = form == 2

        cvs = cmds.ls(shape + ".cv[*]", flatten=True) or []
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

        knot_count = cmds.getAttr(shape + ".knots", size=True)
        knots = []
        for index in range(knot_count):
            knot_value = cmds.getAttr(
                "{}.knots[{}]".format(shape, index)
            )
            knots.append(knot_value)

        result.append({
            "points": points,
            "degree": degree,
            "periodic": periodic,
            "knot": knots,
        })

    return result


def _create_temp_curve(shape_data):
    points_flat = shape_data.get("points") or []
    degree = int(shape_data.get("degree", 1))
    periodic = bool(shape_data.get("periodic", False))
    knots = shape_data.get("knot") or []

    points = []
    index = 0
    while index < len(points_flat):
        point = [
            points_flat[index],
            points_flat[index + 1],
            points_flat[index + 2],
        ]
        points.append(point)
        index += 3

    if periodic:
        extra_points = []
        extra_index = 0
        while extra_index < degree:
            if extra_index < len(points):
                extra_points.append(points[extra_index])
            extra_index += 1

        for point in extra_points:
            points.append(point)

    kwargs = {
        "degree": degree,
        "point": points,
        "periodic": periodic,
    }

    if knots:
        kwargs["knot"] = knots

    return cmds.curve(**kwargs)


def apply_shape_data(transform, shape_data_list):
    """用给定 JSON 数据替换 Transform 下现有 Curve Shape。"""
    if not cmds.objExists(transform):
        raise RuntimeError(u"控制器不存在：{}".format(transform))

    old_shapes = _curve_shapes(transform)
    if old_shapes:
        cmds.delete(old_shapes)

    shape_index = 0
    for shape_data in shape_data_list:
        temp_curve = _create_temp_curve(shape_data)
        temp_shape = _curve_shapes(temp_curve)[0]

        cmds.parent(
            temp_shape,
            transform,
            shape=True,
            relative=True
        )

        short_name = transform.split("|")[-1]
        new_shape_name = "{}Shape".format(short_name)
        if shape_index > 0:
            new_shape_name = "{}Shape{}".format(
                short_name,
                shape_index + 1
            )

        cmds.rename(temp_shape, new_shape_name)
        cmds.delete(temp_curve)
        shape_index += 1

    return transform


def load_shape_data(shape_name):
    file_path = os.path.join(
        get_library_dir(),
        "{}.json".format(shape_name)
    )

    if not os.path.isfile(file_path):
        raise RuntimeError(u"控制器 Shape 文件不存在：{}".format(file_path))

    with open(file_path, "r") as file_obj:
        return json.load(file_obj)


def save_shape_data(shape_name, transform):
    if not shape_name:
        raise RuntimeError(u"Shape 名称不能为空。")

    data = _shape_data_from_transform(transform)
    if not data:
        raise RuntimeError(u"所选对象没有 NURBS Curve Shape。")

    file_path = os.path.join(
        get_library_dir(),
        "{}.json".format(shape_name)
    )

    with open(file_path, "w") as file_obj:
        json.dump(
            data,
            file_obj,
            ensure_ascii=False,
            indent=4
        )

    return file_path


class ShapeListWidget(QListWidget):
    """Shape JSON 图库。"""

    def __init__(self, parent=None):
        super(ShapeListWidget, self).__init__(parent)

        self.setMovement(QListWidget.Static)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(90, 90))
        self.setResizeMode(QListWidget.Adjust)
        self.setMinimumHeight(260)

        self.itemDoubleClicked.connect(self.apply_item_shape)

        self.menu = QMenu(self)
        self.menu.addAction(u"应用 Shape", self.apply_selected_shape)
        self.menu.addSeparator()
        self.menu.addAction(u"上传当前控制器", self.upload_control)
        self.menu.addAction(u"删除图库 Shape", self.delete_shape_files)

        self.refresh()

    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())

    def refresh(self):
        self.clear()

        library_dir = get_library_dir()
        if not os.path.isdir(library_dir):
            os.makedirs(library_dir)

        file_names = os.listdir(library_dir)
        json_names = []

        for file_name in file_names:
            name, extension = os.path.splitext(file_name)
            if extension.lower() != ".json":
                continue
            json_names.append(name)

        json_names.sort()

        for shape_name in json_names:
            jpg_file = os.path.join(
                library_dir,
                "{}.jpg".format(shape_name)
            )

            if os.path.isfile(jpg_file):
                item = QListWidgetItem(QIcon(jpg_file), shape_name, self)
            else:
                item = QListWidgetItem(shape_name, self)

            item.setToolTip(shape_name)

    def apply_item_shape(self, item):
        self._apply_shape_name(item.text())

    def apply_selected_shape(self):
        items = self.selectedItems()
        if not items:
            cmds.warning(u"请先在图库中选择一个 Shape。")
            return

        self._apply_shape_name(items[0].text())

    @staticmethod
    def _apply_shape_name(shape_name):
        data = load_shape_data(shape_name)
        transforms = _selected_curve_transforms()

        cmds.undoInfo(openChunk=True, chunkName="MuziApplyControlShape")
        try:
            if transforms:
                for transform in transforms:
                    apply_shape_data(transform, data)
            else:
                transform = cmds.createNode(
                    "transform",
                    name="ctrl_{}".format(shape_name)
                )
                apply_shape_data(transform, data)
                cmds.select(transform, replace=True)
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    def upload_control(self):
        transforms = _selected_curve_transforms()
        if len(transforms) != 1:
            cmds.warning(u"上传 Shape 时请只选择一个 Curve 控制器。")
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

        invalid_characters = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
        for character in invalid_characters:
            if character in shape_name:
                cmds.warning(u"Shape 名称包含非法字符：{}".format(character))
                return

        try:
            save_shape_data(shape_name, transforms[0])
            self.refresh()
            print(u"[Control Shape] 已保存：{}".format(shape_name))
        except Exception as error:
            cmds.warning(str(error))

    def delete_shape_files(self):
        items = self.selectedItems()
        if not items:
            cmds.warning(u"请选择需要删除的图库 Shape。")
            return

        library_dir = get_library_dir()

        for item in items:
            shape_name = item.text()
            extensions = [".json", ".jpg", ".png"]

            for extension in extensions:
                file_path = os.path.join(
                    library_dir,
                    shape_name + extension
                )

                if os.path.isfile(file_path):
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
        self.setIconSize(QSize(34, 34))
        self.setResizeMode(QListWidget.Adjust)
        self.setMaximumHeight(170)

        index = 0
        for rgb in INDEX_RGB_MAP:
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor.fromRgbF(rgb[0], rgb[1], rgb[2]))
            item = QListWidgetItem(QIcon(pixmap), str(index), self)
            item.setSizeHint(QSize(42, 42))
            item.setData(Qt.UserRole, index)
            index += 1

        self.itemClicked.connect(self.apply_color)

    @staticmethod
    def apply_color(item):
        color_index = item.data(Qt.UserRole)
        transforms = _selected_curve_transforms()

        if not transforms:
            cmds.warning(u"请先选择 Curve 控制器。")
            return

        for transform in transforms:
            shapes = _curve_shapes(transform)
            for shape in shapes:
                cmds.setAttr(shape + ".overrideEnabled", 1)
                cmds.setAttr(shape + ".overrideRGBColors", 0)
                cmds.setAttr(shape + ".overrideColor", int(color_index))


class ControlShapeTool(QWidget):
    """控制器 Shape 图库主窗口。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = qtUtils.get_maya_window()

        super(ControlShapeTool, self).__init__(parent)
        self.setWindowTitle(u"控制器 Shape 工具")
        self.resize(560, 700)

        self.shape_list = ShapeListWidget(self)
        self.color_list = ColorListWidget(self)

        self.rotate_spin = QDoubleSpinBox()
        self.rotate_spin.setRange(-3600.0, 3600.0)
        self.rotate_spin.setValue(90.0)

        self.rotate_x_check = QCheckBox("X")
        self.rotate_y_check = QCheckBox("Y")
        self.rotate_z_check = QCheckBox("Z")
        self.rotate_x_check.setChecked(True)

        self.rotate_btn = QPushButton(u"旋转 Shape")

        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.001, 1000.0)
        self.scale_spin.setDecimals(3)
        self.scale_spin.setValue(1.0)
        self.scale_btn = QPushButton(u"缩放 Shape")

        self.mirror_x_btn = QPushButton(u"镜像 X")
        self.mirror_y_btn = QPushButton(u"镜像 Y")
        self.mirror_z_btn = QPushButton(u"镜像 Z")
        self.replace_btn = QPushButton(u"用最后选择替换前面 Shape")
        self.refresh_btn = QPushButton(u"刷新图库")

        self._create_layout()
        self._create_connections()

    def _create_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel(u"Shape 图库（双击应用）"))
        main_layout.addWidget(self.shape_list)
        main_layout.addWidget(QLabel(u"Maya Index Color"))
        main_layout.addWidget(self.color_list)

        rotate_layout = QHBoxLayout()
        rotate_layout.addWidget(QLabel(u"角度:"))
        rotate_layout.addWidget(self.rotate_spin)
        rotate_layout.addWidget(self.rotate_x_check)
        rotate_layout.addWidget(self.rotate_y_check)
        rotate_layout.addWidget(self.rotate_z_check)
        rotate_layout.addWidget(self.rotate_btn)
        main_layout.addLayout(rotate_layout)

        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel(u"缩放倍数:"))
        scale_layout.addWidget(self.scale_spin)
        scale_layout.addWidget(self.scale_btn)
        main_layout.addLayout(scale_layout)

        mirror_layout = QGridLayout()
        mirror_layout.addWidget(self.mirror_x_btn, 0, 0)
        mirror_layout.addWidget(self.mirror_y_btn, 0, 1)
        mirror_layout.addWidget(self.mirror_z_btn, 0, 2)
        mirror_layout.addWidget(self.replace_btn, 1, 0, 1, 3)
        mirror_layout.addWidget(self.refresh_btn, 2, 0, 1, 3)
        main_layout.addLayout(mirror_layout)

    def _create_connections(self):
        self.rotate_btn.clicked.connect(self.rotate_shapes)
        self.scale_btn.clicked.connect(self.scale_shapes)
        self.mirror_x_btn.clicked.connect(lambda: self.mirror_shapes("x"))
        self.mirror_y_btn.clicked.connect(lambda: self.mirror_shapes("y"))
        self.mirror_z_btn.clicked.connect(lambda: self.mirror_shapes("z"))
        self.replace_btn.clicked.connect(self.replace_shapes)
        self.refresh_btn.clicked.connect(self.shape_list.refresh)

    @staticmethod
    def _selected_cvs():
        transforms = _selected_curve_transforms()
        cvs = []

        for transform in transforms:
            shapes = _curve_shapes(transform)
            for shape in shapes:
                shape_cvs = cmds.ls(shape + ".cv[*]", flatten=True) or []
                for cv in shape_cvs:
                    cvs.append(cv)

        return cvs

    def rotate_shapes(self):
        cvs = self._selected_cvs()
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
        cvs = self._selected_cvs()
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

    def mirror_shapes(self, axis):
        cvs = self._selected_cvs()
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
        transforms = _selected_curve_transforms()
        if len(transforms) < 2:
            cmds.warning(u"至少选择两个控制器，最后选择的对象作为 Shape 来源。")
            return

        source = transforms[-1]
        targets = transforms[:-1]
        source_data = _shape_data_from_transform(source)

        if not source_data:
            cmds.warning(u"Shape 来源没有 NURBS Curve Shape。")
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziReplaceControlShapes")
        try:
            for target in targets:
                apply_shape_data(target, source_data)
        finally:
            cmds.undoInfo(closeChunk=True)


def main():
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = ControlShapeTool()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window
