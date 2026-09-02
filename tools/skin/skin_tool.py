# coding=utf-8
u"""
Skin Tool
=========

蒙皮工具 UI。

权重数据操作统一维护在：
    muziToolset.core.skin_utils

窗口生命周期：
    用户直接调用 main() 时，由 ui.window_utils 负责保存强引用并显示窗口；
    从主工具箱打开时，仍可继续交给 app.window_manager 做应用级窗口管理。
"""

from __future__ import print_function

import os

import maya.cmds as cmds
import maya.mel as mel

try:
    from PySide2.QtWidgets import QFileDialog
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QFileDialog
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...core import skin_utils
from ...ui import theme
from ...ui import window_utils
from ...core import scene_utils


class SkinTool(QWidget):
    """蒙皮工具窗口。"""

    def __init__(self, parent=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        super(SkinTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"Skin Tool",
            minimum_width=560
        )
        self.resize(590, 520)

    def create_widgets(self):
        u"""
        创建界面控件。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.title_label = theme.make_title(u"Skin Tool")
        self.subtitle_label = theme.make_subtitle(
            u"绑定、刷权重、复制权重、影响骨骼和 XML 权重文件管理。"
        )

        self.bind_button = QPushButton(u"Smooth Bind")
        self.detach_button = QPushButton(u"Detach Skin")
        self.paint_button = QPushButton(u"Paint Weights")
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.mirror_button = QPushButton(u"Mirror Weights")

        self.copy_button = QPushButton(u"复制权重")
        theme.style_primary(self.copy_button)

        self.select_influences_button = QPushButton(u"选择影响 Joint")
        self.normalize_button = QPushButton(u"强制归一化")

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.export_button = QPushButton(u"导出权重")
        self.import_button = QPushButton(u"导入权重")

        self.copy_info_label = QLabel(
            u"复制权重：第一个选择模型作为源，其余选择模型作为目标。"
        )
        self.copy_info_label.setWordWrap(True)
        theme.set_role(self.copy_info_label, "muted")

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.file_info_label = QLabel(
            u"每个模型使用 sc_<模型名>.xml 和 sc_<模型名>.infs.json。"
        )
        self.file_info_label.setWordWrap(True)
        theme.set_role(self.file_info_label, "muted")

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

        maya_card, maya_layout = theme.make_card(self)
        maya_layout.addWidget(
            theme.make_section_title(u"Maya Skin")
        )

        maya_description = QLabel(
            u"打开 Maya 自带蒙皮、解绑、刷权重和镜像权重工具。"
        )
        theme.set_role(maya_description, "muted")
        maya_layout.addWidget(maya_description)

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        maya_grid = QGridLayout()
        maya_grid.setHorizontalSpacing(8)
        maya_grid.setVerticalSpacing(8)
        maya_grid.addWidget(self.bind_button, 0, 0)
        maya_grid.addWidget(self.detach_button, 0, 1)
        maya_grid.addWidget(self.paint_button, 1, 0)
        maya_grid.addWidget(self.mirror_button, 1, 1)
        maya_layout.addLayout(maya_grid)

        weight_card, weight_layout = theme.make_card(self)
        weight_layout.addWidget(
            theme.make_section_title(u"权重工具")
        )
        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        weight_layout.addWidget(self.copy_info_label)
        weight_layout.addWidget(self.copy_button)

        utility_layout = QHBoxLayout()
        utility_layout.setContentsMargins(0, 0, 0, 0)
        utility_layout.addWidget(self.select_influences_button)
        utility_layout.addWidget(self.normalize_button)
        weight_layout.addLayout(utility_layout)

        file_card, file_layout = theme.make_card(self)
        file_layout.addWidget(
            theme.make_section_title(u"权重文件")
        )
        file_layout.addWidget(self.file_info_label)

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        file_action_layout = QHBoxLayout()
        file_action_layout.setContentsMargins(0, 0, 0, 0)
        file_action_layout.addWidget(self.export_button)
        file_action_layout.addWidget(self.import_button)
        file_layout.addLayout(file_action_layout)

        main_layout.addWidget(maya_card)
        main_layout.addWidget(weight_card)
        main_layout.addWidget(file_card)
        main_layout.addWidget(self.status_label)
        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        main_layout.addStretch(1)

    def create_connections(self):
        u"""
        连接 UI 信号。
        """
        self.bind_button.clicked.connect(
            self.open_smooth_bind_options
        )
        self.detach_button.clicked.connect(
            self.open_detach_skin_options
        )
        self.paint_button.clicked.connect(
            self.open_paint_skin_weights
        )
        self.mirror_button.clicked.connect(
            self.open_mirror_skin_weights_options
        )
        self.copy_button.clicked.connect(
            self.copy_selected
        )
        self.select_influences_button.clicked.connect(
            self.select_influences
        )
        self.normalize_button.clicked.connect(
            self.normalize_selected
        )
        self.export_button.clicked.connect(
            self.export_selected
        )
        self.import_button.clicked.connect(
            self.import_selected
        )

    def open_smooth_bind_options(self):
        u"""
        执行 `open_smooth_bind_options` 对应的 Maya 工具操作。
        """

        mel.eval("SmoothBindSkinOptions;")

    def open_detach_skin_options(self):
        u"""
        执行 `open_detach_skin_options` 对应的 Maya 工具操作。
        """

        mel.eval("DetachSkinOptions;")

    def open_paint_skin_weights(self):
        u"""
        执行 `open_paint_skin_weights` 对应的 Maya 工具操作。
        """

        mel.eval("ArtPaintSkinWeightsToolOptions;")

    def open_mirror_skin_weights_options(self):
        u"""
        执行 `open_mirror_skin_weights_options` 对应的 Maya 工具操作。
        """

        mel.eval("MirrorSkinWeightsOptions;")

    def get_selected_geometries(self):
        u"""
        返回当前选择。

        Returns:
            object:
            方法执行后的结果数据。
        """
        geometries = cmds.ls(
            selection=True,
            long=True
        )

        if geometries is None:
            geometries = []

        return geometries

    def copy_selected(self):
        u"""
        复制当前选择的 Skin Weight。
        """
        selections = self.get_selected_geometries()

        if len(selections) < 2:
            cmds.warning(
                u"请先选择源模型，再选择一个或多个目标模型。"
            )
            return

        try:
            results = skin_utils.copy_skin_weights(
                source=selections[0],
                targets=selections[1:]
            )
            self.status_label.setText(
                u"已复制权重到 {} 个模型".format(len(results))
            )
        except Exception as error:
            cmds.warning(str(error))
            self.status_label.setText(u"复制权重失败")

    def choose_directory(self, title):
        u"""
        选择权重目录。

        Args:
            title (str):
                窗口、Section、Dialog 或报告使用的标题文本。

        Returns:
            object:
            方法执行后的结果数据。
        """
        scene_path = cmds.file(
            query=True,
            sceneName=True
        )

        if scene_path is None:
            scene_path = ""

        start_directory = os.path.dirname(scene_path)

        return QFileDialog.getExistingDirectory(
            self,
            title,
            start_directory
        )

    def export_selected(self):
        u"""
        导出选择模型权重。
        """
        geometries = self.get_selected_geometries()

        if not geometries:
            cmds.warning(u"请选择需要导出权重的模型。")
            return

        directory = self.choose_directory(u"选择权重导出目录")

        if not directory:
            return

        success_count = 0

        for geometry in geometries:
            try:
                skin_utils.export_skin_weights(
                    geometry,
                    directory
                )
                success_count += 1
            except Exception as error:
                cmds.warning(str(error))

        self.status_label.setText(
            u"已导出 {} 个模型".format(success_count)
        )

    def import_selected(self):
        u"""
        从目录导入权重到选择模型。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        geometries = self.get_selected_geometries()

        if not geometries:
            cmds.warning(u"请选择需要导入权重的模型。")
            return

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        directory = self.choose_directory(u"选择权重目录")

        if not directory:
            return

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        success_count = 0

        scene_utils.open_undo_chunk("MuziImportSkinWeights")

        # -------------------------------------------------------------------------
        # Step 04：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            for geometry in geometries:
                try:
                    skin_utils.import_skin_weights(
                        geometry,
                        directory
                    )
                    success_count += 1
                except Exception as error:
                    cmds.warning(str(error))
        finally:
            scene_utils.close_undo_chunk()

        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"已导入 {} 个模型".format(success_count)
        )

    def select_influences(self):
        u"""
        选择当前模型的影响 Joint。
        """
        geometries = self.get_selected_geometries()

        if not geometries:
            cmds.warning(u"请先选择蒙皮模型。")
            return

        influences = skin_utils.select_influences(geometries)

        if not influences:
            cmds.warning(u"没有找到影响 Joint。")
            return

        self.status_label.setText(
            u"已选择 {} 个影响 Joint".format(len(influences))
        )

    def normalize_selected(self):
        u"""
        强制归一化选择模型权重。
        """
        geometries = self.get_selected_geometries()

        if not geometries:
            cmds.warning(u"请先选择蒙皮模型。")
            return

        normalized = skin_utils.normalize_geometries(geometries)
        self.status_label.setText(
            u"已归一化 {} 个模型".format(len(normalized))
        )


def main():
    u"""
    显示并返回 Skin Tool。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return window_utils.show_window(
        "tools.skin.skin_tool",
        SkinTool
    )


__all__ = [
    "SkinTool",
    "main",
]
