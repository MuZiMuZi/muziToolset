# coding=utf-8
u"""
BlendShape Target Tool
======================

BlendShape Target 管理 UI。

实际 BlendShape 操作统一维护在：
    muziToolset.core.deformation

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
    from PySide2.QtWidgets import QScrollArea
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QListWidget
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QScrollArea
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...core.deformation import blendshape_utils
from ...core.deformation import corrective_target
from ...core.deformation import target_alias_utils
from ...ui import theme
from ...ui import window_utils
from ...core.common import scene_utils
from ...ui.widgets import MayaObjectPicker


class BlendShapeTargetTool(QWidget):
    """BlendShape Target 管理窗口。"""

    def __init__(self, parent=None):
        u"""
        初始化当前对象，并准备运行时需要的状态和成员。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        super(BlendShapeTargetTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"BlendShape Target",
            minimum_width=560
        )
        self.resize(660, 760)

    def create_widgets(self):
        u"""
        创建界面控件。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.title_label = theme.make_title(u"BlendShape Target")
        self.subtitle_label = theme.make_subtitle(
            u"使用真实 weight[index] 管理、添加、替换和烘焙 Target。"
        )

        self.blendshape_line = QLineEdit()
        self.blendshape_line.setPlaceholderText(u"BlendShape 节点")

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.pick_blendshape_button = QPushButton(u"从选择获取")
        self.refresh_button = QPushButton(u"刷新")
        theme.style_ghost(self.refresh_button)

        self.target_count_label = QLabel(u"0 个 Target")
        theme.set_role(self.target_count_label, "accent")

        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.target_list = QListWidget()
        self.target_list.setMinimumHeight(240)

        self.target_info_label = QLabel(
            u"列表显示真实 weight index；删除过中间 Target 后也不会发生索引错位。"
        )
        self.target_info_label.setWordWrap(True)
        theme.set_role(self.target_info_label, "muted")

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.add_target_button = QPushButton(u"添加 / 同名替换 Target")
        theme.style_primary(self.add_target_button)

        self.duplicate_targets_button = QPushButton(u"复制所有 Target Mesh")
        self.rename_mirrored_button = QPushButton(u"重命名 lf_*_Copy → rt_*")

        self.controller_picker = MayaObjectPicker(
            label_text=u"控制器",
            placeholder=u"载入驱动基础模型的控制器",
            node_types=["transform", "joint"]
        )
        self.inverted_target_name = QLineEdit()
        self.inverted_target_name.setPlaceholderText(u"反算 Target 名称（留空自动命名）")
        self.inverted_selection_label = QLabel(
            u"保持修型姿势，先选择修型 Mesh，再选择基础 Mesh。\n"
            u"TR 通道须未锁定且无输入连接；添加后恢复姿态，新 Target 权重为 0。"
        )
        self.inverted_selection_label.setWordWrap(True)
        theme.set_role(self.inverted_selection_label, "muted")
        self.add_inverted_button = QPushButton(u"添加反算 Target")
        theme.style_primary(self.add_inverted_button)

        self.status_label = QLabel(u"准备就绪")
        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.set_role(self.status_label, "muted")

    def create_layouts(self):
        u"""
        创建 Card 布局。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        node_card, node_layout = theme.make_card(self)
        node_layout.addWidget(
            theme.make_section_title(u"BlendShape Node")
        )

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        node_row = QHBoxLayout()
        node_row.setContentsMargins(0, 0, 0, 0)
        node_row.addWidget(self.blendshape_line, 1)
        node_row.addWidget(self.pick_blendshape_button)
        node_row.addWidget(self.refresh_button)
        node_layout.addLayout(node_row)

        target_card, target_layout = theme.make_card(self)

        target_header = QHBoxLayout()
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
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
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        action_row.setContentsMargins(0, 0, 0, 0)
        action_row.addWidget(self.duplicate_targets_button)
        action_row.addStretch(1)
        action_row.addWidget(self.add_target_button)
        target_layout.addLayout(action_row)
        target_layout.addWidget(self.rename_mirrored_button)

        corrective_card, corrective_layout = theme.make_card(self)
        corrective_layout.addWidget(theme.make_section_title(u"反算修型 → 添加 BS Target"))
        corrective_layout.addWidget(self.controller_picker)
        corrective_layout.addWidget(self.inverted_target_name)
        corrective_layout.addWidget(self.inverted_selection_label)
        corrective_layout.addWidget(self.add_inverted_button)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)
        content_layout.addWidget(node_card)
        content_layout.addWidget(target_card)
        content_layout.addWidget(corrective_card)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setWidget(content)
        main_layout.addWidget(scroll, 1)
        # -------------------------------------------------------------------------
        # Step 05：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        main_layout.addWidget(self.status_label)

    def create_connections(self):
        u"""
        连接 UI 信号。
        """
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
        self.add_inverted_button.clicked.connect(self.add_inverted_target)
        self.rename_mirrored_button.clicked.connect(self.rename_mirrored_targets)

    def add_inverted_target(self):
        u"""按修型、基础模型的选择顺序添加一个反算 Target。"""
        selections = cmds.ls(selection=True, long=True) or []
        if len(selections) != 2:
            cmds.warning(u"请先选择修型 Mesh，再选择基础 Mesh，共两个模型。")
            return
        try:
            result = corrective_target.add_inverted_target(
                controller=self.controller_picker.get_value(),
                blendshape_node=self.get_blendshape_node(),
                corrective_mesh=selections[0],
                base_mesh=selections[1],
                target_name=self.inverted_target_name.text().strip()
            )
        except Exception as error:
            cmds.warning(str(error))
            self.status_label.setText(u"添加反算 Target 失败：{}".format(error))
            return
        self.refresh_targets()
        self.status_label.setText(u"已添加 [{:03d}] {}，权重为 0".format(
            result["index"], result["alias"]))

    def rename_mirrored_targets(self):
        u"""按真实 Weight Index 把左右复制 Target 改名并刷新列表。"""
        try:
            results = target_alias_utils.rename_mirrored_targets(
                self.get_blendshape_node())
        except Exception as error:
            cmds.warning(str(error))
            self.status_label.setText(u"Target 改名失败：{}".format(error))
            return
        self.refresh_targets()
        self.status_label.setText(u"已重命名 {} 个 Target（只改名，不镜像几何）".format(
            len(results)))

    def get_blendshape_node(self):
        u"""
        返回当前输入的 BlendShape 节点。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        return self.blendshape_line.text().strip()

    def pick_blendshape(self):
        u"""
        从当前选择查找 BlendShape。
        """
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
        u"""
        刷新真实 Target Index。
        """
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
        u"""
        把当前选择 Mesh 添加到 BlendShape。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        blendshape_node = self.get_blendshape_node()

        if not blendshape_node:
            cmds.warning(u"请先指定 BlendShape 节点。")
            return

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(u"请选择一个或多个 Target Mesh。")
            return

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        added_count = 0

        scene_utils.open_undo_chunk("MuziAddBlendShapeTargets")

        # -------------------------------------------------------------------------
        # Step 04：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
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
            scene_utils.close_undo_chunk()

        self.refresh_targets()
        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"已添加 / 替换 {} 个 Target".format(added_count)
        )

    def duplicate_targets(self):
        u"""
        从 Base Mesh 烘焙全部 Target Mesh。
        """
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
    u"""
    显示并返回 BlendShape Target Tool。

    Returns:
        object:
        当前工具入口创建并显示的窗口或执行结果。
    """
    return window_utils.show_window(
        "tools.blendshape.add_blendshape_tool",
        BlendShapeTargetTool
    )


__all__ = [
    "BlendShapeTargetTool",
    "main",
]
