# coding=utf-8
u"""
Invert Shape Tool
=================

为蒙皮后的模型计算可用于 BlendShape 的反算修型（corrective shape）。
使用 Maya 原生 ``cmds.invertShape``。
"""

from __future__ import print_function

import maya.cmds as cmds

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QVBoxLayout

from ....core import qtUtils


_window = None


def _short_name(node):
    return node.split("|")[-1].replace(":", "_")


def _mesh_shape(node):
    if not node or not cmds.objExists(node):
        return None

    if cmds.nodeType(node) == "mesh":
        return node

    shapes = cmds.listRelatives(
        node,
        shapes=True,
        noIntermediate=True,
        fullPath=True,
        type="mesh"
    ) or []

    if shapes:
        return shapes[0]

    return None


def _vertex_count(node):
    shape = _mesh_shape(node)
    if not shape:
        return None

    return cmds.polyEvaluate(shape, vertex=True)


def invert_shapes(base_mesh, corrective_meshes):
    """批量执行 invertShape。"""
    if not _mesh_shape(base_mesh):
        raise RuntimeError(u"基础模型不是有效 Mesh：{}".format(base_mesh))

    base_vertex_count = _vertex_count(base_mesh)
    results = []

    cmds.undoInfo(openChunk=True, chunkName="MuziInvertShapes")
    try:
        for corrective in corrective_meshes:
            if not corrective or not cmds.objExists(corrective):
                continue

            if not _mesh_shape(corrective):
                cmds.warning(u"跳过非 Mesh：{}".format(corrective))
                continue

            corrective_vertex_count = _vertex_count(corrective)
            if corrective_vertex_count != base_vertex_count:
                cmds.warning(
                    u"拓扑点数不一致，跳过 {}：base={} / corrective={}".format(
                        corrective,
                        base_vertex_count,
                        corrective_vertex_count
                    )
                )
                continue

            inverted = cmds.invertShape(
                base_mesh,
                corrective
            )

            if isinstance(inverted, (list, tuple)):
                inverted = inverted[0]

            target_name = "{}_invert_geo".format(
                _short_name(corrective)
            )

            if cmds.objExists(target_name):
                suffix = 1
                while cmds.objExists(
                        "{}_{:03d}".format(target_name, suffix)
                ):
                    suffix += 1
                target_name = "{}_{:03d}".format(
                    target_name,
                    suffix
                )

            inverted = cmds.rename(inverted, target_name)
            results.append(inverted)
    finally:
        cmds.undoInfo(closeChunk=True)

    return results


class InvertShapeTool(QDialog):
    """Invert Shape 批处理窗口。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = qtUtils.get_maya_window()

        super(InvertShapeTool, self).__init__(parent)
        self.setWindowTitle(u"Invert Shape Tool")
        self.setMinimumWidth(430)

        self.base_line = QLineEdit()
        self.base_line.setReadOnly(True)
        self.base_pick_btn = QPushButton(u"拾取")

        self.corrective_line = QLineEdit()
        self.corrective_line.setReadOnly(True)
        self.corrective_pick_btn = QPushButton(u"拾取多个")

        self.execute_btn = QPushButton(u"计算 Invert Shape")

        self.corrective_meshes = []

        self._create_layout()
        self._create_connections()

    def _create_layout(self):
        main_layout = QVBoxLayout(self)

        base_layout = QHBoxLayout()
        base_layout.addWidget(QLabel(u"蒙皮基础模型:"))
        base_layout.addWidget(self.base_line, 1)
        base_layout.addWidget(self.base_pick_btn)
        main_layout.addLayout(base_layout)

        corrective_layout = QHBoxLayout()
        corrective_layout.addWidget(QLabel(u"修型模型:"))
        corrective_layout.addWidget(self.corrective_line, 1)
        corrective_layout.addWidget(self.corrective_pick_btn)
        main_layout.addLayout(corrective_layout)

        main_layout.addWidget(self.execute_btn)

    def _create_connections(self):
        self.base_pick_btn.clicked.connect(self.pick_base)
        self.corrective_pick_btn.clicked.connect(self.pick_correctives)
        self.execute_btn.clicked.connect(self.execute)

    def pick_base(self):
        selections = cmds.ls(selection=True, long=True) or []
        if len(selections) != 1:
            cmds.warning(u"基础模型请只选择一个 Mesh。")
            return

        if not _mesh_shape(selections[0]):
            cmds.warning(u"选择对象不是 Mesh。")
            return

        self.base_line.setText(selections[0])

    def pick_correctives(self):
        selections = cmds.ls(selection=True, long=True) or []
        if not selections:
            cmds.warning(u"请选择一个或多个修型 Mesh。")
            return

        valid_meshes = []
        for node in selections:
            if _mesh_shape(node):
                valid_meshes.append(node)

        if not valid_meshes:
            cmds.warning(u"选择中没有有效 Mesh。")
            return

        self.corrective_meshes = valid_meshes

        display_names = []
        for node in valid_meshes:
            display_names.append(_short_name(node))

        self.corrective_line.setText(
            ", ".join(display_names)
        )

    def execute(self):
        base_mesh = self.base_line.text().strip()

        if not base_mesh:
            cmds.warning(u"请先拾取蒙皮基础模型。")
            return

        if not self.corrective_meshes:
            cmds.warning(u"请先拾取修型模型。")
            return

        try:
            results = invert_shapes(
                base_mesh,
                self.corrective_meshes
            )

            if results:
                cmds.select(results, replace=True)
                print(
                    u"[Invert Shape] 已生成 {} 个反算修型。".format(
                        len(results)
                    )
                )
            else:
                cmds.warning(u"没有生成任何 Invert Shape。")
        except Exception as error:
            cmds.warning(str(error))


# 旧类名兼容。
shape_Tool = InvertShapeTool


def main():
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = InvertShapeTool()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window


if __name__ == "__main__":
    main()
