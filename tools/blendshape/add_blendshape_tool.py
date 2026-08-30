# coding=utf-8
u"""
BlendShape Target Tool
======================

BlendShape Target 管理 UI。

实际 BlendShape 操作统一维护在：
    muziToolset.core.blendshape_utils

窗口生命周期：
    用户直接调用 main() 时，由 ui.window_utils 负责保存强引用并显示窗口；
    从主工具箱打开时，仍可继续交给 app.window_manager 做应用级窗口管理。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QListWidget
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QListWidget
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...core import blendshape_utils
from ...ui import theme
from ...ui import window_utils


class BlendShapeTargetTool(QWidget):
    """BlendShape Target 管理窗口。"""

    def __init__(self, parent=None):
        super(BlendShapeTargetTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"BlendShape Target",
            minimum_width=560
        )
        self.resize(590, 570)

    def create_widgets(self):
        """创建界面控件。"""
        self.title_label = theme.make_title(u"BlendShape Target")
        self.subtitle_label = theme.make_subtitle(
            u"使用真实 weight[index] 管理、添加、替换和烘焙 Target。"
        )

        self.blendshape_line = QLineEdit()
        self.blendshape_line.setPlaceholderText(u"BlendShape 节点")

        self.pick_blendshape_button = QPushButton(u"从选择获取")
        self.refresh_button = QPushButton(u"刷新")
        theme.style_ghost(self.refresh_button)

        self.target_count_label = QLabel(u"0 个 Target")
        theme.set_role(self.target_count_label, "accent")

        self.target_list = QListWidget()
        self.target_list.setMinimumHeight(240)

        self.target_info_label = QLabel(
            u"列表显示真实 weight index；删除过中间 Target 后也不会发生索引错位。"
        )
        self.target_info_label.setWordWrap(True)
        theme.set_role(self.target_info_label, "muted")

        self.add_target_button = QPushButton(u"添加 / 同名替换 Target")
        theme.style_primary(self.add_target_button)

        self.duplicate_targets_button = QPushButton(u"复制所有 Target Mesh")

        self.status_label = QLabel(u"准备就绪")
        theme.set_role(self.status_label, "muted")

    def create_layouts(self):
        """创建 Card 布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        node_card, node_layout = theme.make_card(self)
        node_layout.addWidget(
            theme.make_section_title(u"BlendShape Node")
        )

        node_row = QHBoxLayout()
        node_row.setContentsMargins(0, 0, 0, 0)
        node_row.addWidget(self.blendshape_line, 1)
        node_row.addWidget(self.pick_blendshape_button)
        node_row.addWidget(self.refresh_button)
        node_layout.addLayout(node_row)

        target_card, target_layout = theme.make_card(self)

        target_header = QHBoxLayout()
        target_header.setContentsMargins(0, 0, 0, 0)
        target_header.addWidget(
            theme.make_section_title(u"Targets")
        )
        target_header.addStretch(1)
        target_header.addWidget(self.target_count_label)
        target_layout.addLayout(target_header)
        target_layout.addWidget(self.target_info_label)
        target_layout.addWidget(self.target_list, 1)

        action_row = QHBoxLayout()
        action_row.setContentsMargins(0, 0, 0, 0)
        action_row.addWidget(self.duplicate_targets_button)
        action_row.addStretch(1)
        action_row.addWidget(self.add_target_button)
        target_layout.addLayout(action_row)

        main_layout.addWidget(node_card)
        main_layout.addWidget(target_card, 1)
        main_layout.addWidget(self.status_label)

    def create_connections(self):
        """连接 UI 信号。"""
        self.pick_blendshape_button.clicked.connect(
            self.pick_blendshape
        )
        self.refresh_button.clicked.connect(
            self.refresh_targets
        )
        self.add_target_button.clicked.connect(
            self.add_targets
        )
        self.duplicate_targets_button.clicked.connect(
            self.duplicate_targets
        )
        self.blendshape_line.editingFinished.connect(
            self.refresh_targets
        )

    def get_blendshape_node(self):
        """返回当前输入的 BlendShape 节点。"""
        return self.blendshape_line.text().strip()

    def pick_blendshape(self):
        """从当前选择查找 BlendShape。"""
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(
                u"请选择 BlendShape 节点或带 BlendShape 的模型。"
            )
            return

        for node in selections:
            blendshape_node = blendshape_utils.find_blendshape(node)

            if not blendshape_node:
                continue

            self.blendshape_line.setText(blendshape_node)
            self.refresh_targets()
            return

        cmds.warning(u"选择中没有找到 BlendShape。")

    def refresh_targets(self):
        """刷新真实 Target Index。"""
        self.target_list.clear()
        blendshape_node = self.get_blendshape_node()

        if not blendshape_node:
            self.target_count_label.setText(u"0 个 Target")
            return

        if not cmds.objExists(blendshape_node):
            self.target_count_label.setText(u"0 个 Target")
            return

        targets = blendshape_utils.get_targets(blendshape_node)

        for target_info in targets:
            display_text = u"[{0:03d}]  {1}".format(
                target_info["index"],
                target_info["alias"]
            )
            self.target_list.addItem(display_text)

        self.target_count_label.setText(
            u"{} 个 Target".format(len(targets))
        )
        self.status_label.setText(u"Target 列表已刷新")

    def add_targets(self):
        """把当前选择 Mesh 添加到 BlendShape。"""
        blendshape_node = self.get_blendshape_node()

        if not blendshape_node:
            cmds.warning(u"请先指定 BlendShape 节点。")
            return

        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(u"请选择一个或多个 Target Mesh。")
            return

        added_count = 0

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziAddBlendShapeTargets"
        )

        try:
            for target in selections:
                try:
                    blendshape_utils.add_or_replace_target(
                        blendshape_node,
                        target
                    )
                    added_count += 1
                except Exception as error:
                    cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

        self.refresh_targets()
        self.status_label.setText(
            u"已添加 / 替换 {} 个 Target".format(added_count)
        )

    def duplicate_targets(self):
        """从 Base Mesh 烘焙全部 Target Mesh。"""
        blendshape_node = self.get_blendshape_node()

        if not blendshape_node:
            cmds.warning(u"请先指定 BlendShape 节点。")
            return

        try:
            copies = blendshape_utils.duplicate_all_targets(
                blendshape_node
            )
        except Exception as error:
            cmds.warning(str(error))
            self.status_label.setText(u"复制 Target 失败")
            return

        if copies:
            cmds.select(
                copies,
                replace=True
            )

        self.status_label.setText(
            u"已复制 {} 个 Target Mesh".format(len(copies))
        )


def main():
    """显示并返回 BlendShape Target Tool。"""
    return window_utils.show_window(
        "tools.blendshape.add_blendshape_tool",
        BlendShapeTargetTool
    )


__all__ = [
    "BlendShapeTargetTool",
    "main",
]
