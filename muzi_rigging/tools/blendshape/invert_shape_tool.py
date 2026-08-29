# coding=utf-8
u"""
Invert Shape Tool
=================

为蒙皮后的模型计算可用于 BlendShape 的反算修型。
使用 Maya 原生 ``cmds.invertShape``。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
except ImportError:
    from PySide6.QtWidgets import QDialog
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout

from ... import ui_theme


def _short_name(node):
    """返回节点短名称。"""
    return node.split("|")[-1].replace(":", "_")


def _mesh_shape(node):
    """返回 Transform 或 Mesh 对应的可见 Mesh Shape。"""
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
    )

    if shapes is None:
        shapes = []

    if shapes:
        return shapes[0]

    return None


def _vertex_count(node):
    """返回 Mesh 顶点数量。"""
    shape = _mesh_shape(node)

    if not shape:
        return None

    return cmds.polyEvaluate(
        shape,
        vertex=True
    )


def invert_shapes(base_mesh, corrective_meshes):
    """批量执行 invertShape。"""
    if not _mesh_shape(base_mesh):
        raise RuntimeError(
            u"基础模型不是有效 Mesh：{}".format(base_mesh)
        )

    base_vertex_count = _vertex_count(base_mesh)
    results = []

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziInvertShapes"
    )

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

            inverted = cmds.rename(
                inverted,
                target_name
            )
            results.append(inverted)
    finally:
        cmds.undoInfo(closeChunk=True)

    return results


class InvertShapeTool(QDialog):
    """Invert Shape 批处理窗口。"""

    def __init__(self, parent=None):
        super(InvertShapeTool, self).__init__(parent)

        self.corrective_meshes = []

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        ui_theme.style_window(
            self,
            title=u"Invert Shape",
            minimum_width=540
        )
        self.resize(560, 390)

    # -------------------------------------------------------------------------
    # UI
    # -------------------------------------------------------------------------

    def create_widgets(self):
        """创建界面部件。"""
        self.title_label = ui_theme.make_title(u"Invert Shape")
        self.subtitle_label = ui_theme.make_subtitle(
            u"把蒙皮后模型上的修型反算为可用于 BlendShape 的 Corrective Shape。"
        )

        self.base_label = QLabel(u"基础模型")
        self.base_line = QLineEdit()
        self.base_line.setReadOnly(True)
        self.base_line.setPlaceholderText(u"选择蒙皮后的基础 Mesh")
        self.base_pick_button = QPushButton(u"拾取")

        self.corrective_label = QLabel(u"修型模型")
        self.corrective_line = QLineEdit()
        self.corrective_line.setReadOnly(True)
        self.corrective_line.setPlaceholderText(u"选择一个或多个 Corrective Mesh")
        self.corrective_pick_button = QPushButton(u"拾取多个")

        self.selection_count_label = QLabel(u"尚未拾取修型")
        ui_theme.set_role(self.selection_count_label, "muted")

        self.topology_info_label = QLabel(
            u"基础模型和修型模型必须具有相同的顶点数量；不匹配的模型会自动跳过。"
        )
        self.topology_info_label.setWordWrap(True)
        ui_theme.set_role(self.topology_info_label, "muted")

        self.execute_button = QPushButton(u"计算 Invert Shape")
        ui_theme.style_primary(self.execute_button)

    def create_layouts(self):
        """创建 Silicon Card 布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        source_card, source_layout = ui_theme.make_card(self)
        source_layout.addWidget(
            ui_theme.make_section_title(u"输入模型")
        )

        base_layout = QHBoxLayout()
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.addWidget(self.base_label)
        base_layout.addWidget(self.base_line, 1)
        base_layout.addWidget(self.base_pick_button)
        source_layout.addLayout(base_layout)

        corrective_layout = QHBoxLayout()
        corrective_layout.setContentsMargins(0, 0, 0, 0)
        corrective_layout.addWidget(self.corrective_label)
        corrective_layout.addWidget(self.corrective_line, 1)
        corrective_layout.addWidget(self.corrective_pick_button)
        source_layout.addLayout(corrective_layout)
        source_layout.addWidget(self.selection_count_label)

        execute_card, execute_layout = ui_theme.make_card(self)
        execute_layout.addWidget(
            ui_theme.make_section_title(u"反算")
        )
        execute_layout.addWidget(self.topology_info_label)
        execute_layout.addWidget(self.execute_button)

        main_layout.addWidget(source_card)
        main_layout.addWidget(execute_card)
        main_layout.addStretch(1)

    def create_connections(self):
        """连接界面信号。"""
        self.base_pick_button.clicked.connect(self.pick_base)
        self.corrective_pick_button.clicked.connect(
            self.pick_correctives
        )
        self.execute_button.clicked.connect(self.execute)

    # -------------------------------------------------------------------------
    # 选择
    # -------------------------------------------------------------------------

    def pick_base(self):
        """拾取唯一基础 Mesh。"""
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if len(selections) != 1:
            cmds.warning(u"基础模型请只选择一个 Mesh。")
            return

        if not _mesh_shape(selections[0]):
            cmds.warning(u"选择对象不是 Mesh。")
            return

        self.base_line.setText(selections[0])

    def pick_correctives(self):
        """拾取多个 Corrective Mesh。"""
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

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
        self.selection_count_label.setText(
            u"已拾取 {} 个修型模型".format(len(valid_meshes))
        )

    # -------------------------------------------------------------------------
    # 执行
    # -------------------------------------------------------------------------

    def execute(self):
        """执行批量 Invert Shape。"""
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
                cmds.select(
                    results,
                    replace=True
                )
                print(
                    u"[Invert Shape] 已生成 {} 个反算修型。".format(
                        len(results)
                    )
                )
            else:
                cmds.warning(u"没有生成任何 Invert Shape。")
        except Exception as error:
            cmds.warning(str(error))


def main():
    """创建 Invert Shape 窗口。"""
    window = InvertShapeTool()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
