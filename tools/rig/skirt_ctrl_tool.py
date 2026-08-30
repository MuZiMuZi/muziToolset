# coding=utf-8
u"""
Skirt Rig Tool
==============

裙子绑定系统 UI。

实际绑定逻辑维护在：
    muziToolset.systems.body.skirt

窗口生命周期：
    用户直接调用 main() 时，由 ui.window_utils 负责保存强引用并显示窗口；
    从主工具箱打开时，仍可继续交给 app.window_manager 做应用级窗口管理。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QSpinBox
    from PySide2.QtWidgets import QVBoxLayout
except ImportError:
    from PySide6.QtWidgets import QDialog
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QSpinBox
    from PySide6.QtWidgets import QVBoxLayout

from ...systems.body.skirt import SkirtRigBuilder
from ...ui import theme
from ...ui import window_utils


class SkirtRigDialog(QDialog):
    """裙子绑定工具窗口。"""

    def __init__(self, parent=None):
        super(SkirtRigDialog, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"Skirt Rig",
            minimum_width=480
        )
        self.resize(520, 430)

    def create_widgets(self):
        """创建界面控件。"""
        self.title_label = theme.make_title(u"裙子绑定")
        self.subtitle_label = theme.make_subtitle(
            u"先创建上下定位曲线并调整造型，再生成纵向 Joint Chain 和 FK Controller。"
        )

        self.name_line = QLineEdit("skirt")
        self.name_line.setPlaceholderText(u"系统名称，例如 skirt")

        self.horizontal_spin = QSpinBox()
        self.horizontal_spin.setRange(3, 64)
        self.horizontal_spin.setValue(8)

        self.vertical_spin = QSpinBox()
        self.vertical_spin.setRange(2, 32)
        self.vertical_spin.setValue(4)

        self.create_setup_button = QPushButton(u"01 生成 / 重建定位")
        theme.style_primary(self.create_setup_button)

        self.select_setup_button = QPushButton(u"选择定位曲线")
        theme.style_ghost(self.select_setup_button)

        self.build_button = QPushButton(u"02 生成绑定")
        theme.style_primary(self.build_button)

        self.status_label = QLabel(u"准备就绪")
        theme.set_role(self.status_label, "muted")

    def create_layouts(self):
        """创建 Card 布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        config_card, config_layout = theme.make_card(self)
        config_layout.addWidget(
            theme.make_section_title(u"系统参数")
        )

        config_grid = QGridLayout()
        config_grid.setHorizontalSpacing(12)
        config_grid.setVerticalSpacing(10)
        config_grid.addWidget(QLabel(u"名称"), 0, 0)
        config_grid.addWidget(self.name_line, 0, 1, 1, 3)
        config_grid.addWidget(QLabel(u"横向链数量"), 1, 0)
        config_grid.addWidget(self.horizontal_spin, 1, 1)
        config_grid.addWidget(QLabel(u"纵向关节数量"), 1, 2)
        config_grid.addWidget(self.vertical_spin, 1, 3)
        config_grid.setColumnStretch(1, 1)
        config_grid.setColumnStretch(3, 1)
        config_layout.addLayout(config_grid)

        setup_card, setup_layout = theme.make_card(self)
        setup_layout.addWidget(
            theme.make_section_title(u"Step 01 · 定位")
        )

        setup_info = QLabel(
            u"生成 Up / Down 两条曲线。Blueprint Joint 会实时跟随曲线，"
            u"请在 Maya 视图中调整曲线贴合裙子轮廓。"
        )
        setup_info.setWordWrap(True)
        theme.set_role(setup_info, "muted")
        setup_layout.addWidget(setup_info)

        setup_action_layout = QHBoxLayout()
        setup_action_layout.setContentsMargins(0, 0, 0, 0)
        setup_action_layout.addWidget(self.select_setup_button)
        setup_action_layout.addStretch(1)
        setup_action_layout.addWidget(self.create_setup_button)
        setup_layout.addLayout(setup_action_layout)

        build_card, build_layout = theme.make_card(self)
        build_layout.addWidget(
            theme.make_section_title(u"Step 02 · Build")
        )

        build_info = QLabel(
            u"根据当前定位创建纵向 Bind Joint、标准 Controller 层级和 FK 约束。"
        )
        build_info.setWordWrap(True)
        theme.set_role(build_info, "muted")
        build_layout.addWidget(build_info)
        build_layout.addWidget(self.build_button)

        main_layout.addWidget(config_card)
        main_layout.addWidget(setup_card)
        main_layout.addWidget(build_card)
        main_layout.addWidget(self.status_label)
        main_layout.addStretch(1)

    def create_connections(self):
        """连接 UI 信号。"""
        self.create_setup_button.clicked.connect(
            self.create_setup
        )
        self.select_setup_button.clicked.connect(
            self.select_setup_curves
        )
        self.build_button.clicked.connect(
            self.build_rig
        )

    def create_builder(self):
        """根据当前 UI 参数创建 Skirt Builder。"""
        return SkirtRigBuilder(
            name=self.name_line.text(),
            horizontal_count=self.horizontal_spin.value(),
            vertical_count=self.vertical_spin.value()
        )

    def create_setup(self):
        """创建或重建定位系统。"""
        try:
            builder = self.create_builder()
            builder.create_setup()
            self.status_label.setText(
                u"定位已生成：{} 条纵向列".format(
                    builder.horizontal_count
                )
            )
        except Exception as error:
            cmds.warning(str(error))
            self.status_label.setText(u"定位创建失败")

    def select_setup_curves(self):
        """选择定位曲线。"""
        try:
            builder = self.create_builder()
            curves = builder.select_setup_curves()

            if curves:
                self.status_label.setText(u"已选择定位曲线")
        except Exception as error:
            cmds.warning(str(error))

    def build_rig(self):
        """执行完整裙子绑定 Build。"""
        try:
            builder = self.create_builder()
            result = builder.build()

            self.status_label.setText(
                u"Build 完成：{} × {}，{} 个控制器".format(
                    builder.horizontal_count,
                    builder.vertical_count,
                    len(result["controls"])
                )
            )
        except Exception as error:
            cmds.warning(str(error))
            self.status_label.setText(u"Build 失败")


def main():
    """显示并返回 Skirt Rig 窗口。"""
    return window_utils.show_window(
        "tools.rig.skirt_ctrl_tool",
        SkirtRigDialog
    )


__all__ = [
    "SkirtRigDialog",
    "main",
]
