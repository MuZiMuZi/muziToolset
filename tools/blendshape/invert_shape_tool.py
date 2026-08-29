# coding=utf-8
u"""
Invert Shape Tool
=================

Corrective Shape 反算 UI。

实际 invertShape 逻辑统一维护在：
    muzi_rigging.core.blendshape_utils
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
except ImportError:
    from PySide6.QtWidgets import QDialog
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout

from ...core import blendshape_utils
from ...ui import theme
from ...ui.widgets import MayaObjectPicker


class InvertShapeTool(QDialog):
    """Invert Shape 批处理窗口。"""

    def __init__(self, parent=None):
        super(InvertShapeTool, self).__init__(parent)

        self.corrective_meshes = []

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"Invert Shape",
            minimum_width=560
        )
        self.resize(590, 410)

    def create_widgets(self):
        """创建界面控件。"""
        self.title_label = theme.make_title(u"Invert Shape")
        self.subtitle_label = theme.make_subtitle(
            u"把蒙皮后模型上的修型反算为可用于 BlendShape 的 Corrective Shape。"
        )

        self.base_picker = MayaObjectPicker(
            label_text=u"基础模型",
            placeholder=u"选择蒙皮后的基础 Mesh"
        )

        self.corrective_button = QPushButton(u"拾取当前选择为 Corrective Mesh")
        self.corrective_count_label = QLabel(u"尚未拾取修型")
        theme.set_role(self.corrective_count_label, "muted")

        self.topology_info_label = QLabel(
            u"基础模型与修型模型必须具有相同顶点数量；不匹配的修型会自动跳过。"
        )
        self.topology_info_label.setWordWrap(True)
        theme.set_role(self.topology_info_label, "muted")

        self.execute_button = QPushButton(u"计算 Invert Shape")
        theme.style_primary(self.execute_button)

        self.status_label = QLabel(u"准备就绪")
        theme.set_role(self.status_label, "muted")

    def create_layouts(self):
        """创建 Card 布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        source_card, source_layout = theme.make_card(self)
        source_layout.addWidget(
            theme.make_section_title(u"输入模型")
        )
        source_layout.addWidget(self.base_picker)
        source_layout.addWidget(self.corrective_button)
        source_layout.addWidget(self.corrective_count_label)

        execute_card, execute_layout = theme.make_card(self)
        execute_layout.addWidget(
            theme.make_section_title(u"反算")
        )
        execute_layout.addWidget(self.topology_info_label)
        execute_layout.addWidget(self.execute_button)

        main_layout.addWidget(source_card)
        main_layout.addWidget(execute_card)
        main_layout.addWidget(self.status_label)
        main_layout.addStretch(1)

    def create_connections(self):
        """连接 UI 信号。"""
        self.corrective_button.clicked.connect(
            self.pick_correctives
        )
        self.execute_button.clicked.connect(
            self.execute
        )

    def pick_correctives(self):
        """拾取当前选择中的全部有效 Mesh。"""
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(u"请选择一个或多个 Corrective Mesh。")
            return

        valid_meshes = []

        for node in selections:
            if blendshape_utils.get_mesh_shape(node):
                valid_meshes.append(node)

        if not valid_meshes:
            cmds.warning(u"选择中没有有效 Mesh。")
            return

        self.corrective_meshes = valid_meshes
        self.corrective_count_label.setText(
            u"已拾取 {} 个 Corrective Mesh".format(
                len(valid_meshes)
            )
        )

    def execute(self):
        """执行批量 Invert Shape。"""
        base_mesh = self.base_picker.get_value()

        if not base_mesh:
            cmds.warning(u"请先拾取基础模型。")
            return

        if not self.corrective_meshes:
            cmds.warning(u"请先拾取 Corrective Mesh。")
            return

        try:
            results = blendshape_utils.invert_shapes(
                base_mesh,
                self.corrective_meshes
            )
        except Exception as error:
            cmds.warning(str(error))
            self.status_label.setText(u"Invert Shape 失败")
            return

        if results:
            cmds.select(
                results,
                replace=True
            )

        self.status_label.setText(
            u"已生成 {} 个 Invert Shape".format(len(results))
        )


def main():
    """创建并返回 Invert Shape Tool。"""
    window = InvertShapeTool()
    return window


__all__ = [
    "InvertShapeTool",
    "main",
]
