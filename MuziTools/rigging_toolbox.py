#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rigging 工具箱主面板
功能：自动发现 tools 目录下按分类组织的工具，生成可折叠面板，点击即可打开对应工具

分类映射（由 tools/__init__.py 管理）：
    basic      -> 基础工具
    joint      -> 骨骼工具
    ctrl       -> 控制器工具
    skin       -> 蒙皮工具
    blendShape -> BlendShape工具
    clean      -> 清理工具
"""

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui

# 从 tools 包导入按分类组织的工具字典
from .tools import get_tools_by_category
from . import window_manager


def get_maya_main_window():
    """获取 Maya 主窗口，作为工具箱的父窗口"""
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(int(ptr), QWidget)
    return None


# =============================================================================
#  可折叠面板组件
# =============================================================================
class Collapsible_Box(QWidget):
    """
    可折叠面板组件
    类似 Maya cmds.frameLayout(collapsable=True) 的效果
    点击标题栏可以展开/收起内容区域
    """

    def __init__(self, title="", parent=None):
        super(Collapsible_Box, self).__init__(parent)

        # --- 标题按钮（带箭头图标，可点击切换）---
        self.toggle_button = QToolButton()
        self.toggle_button.setText(title)
        # 设置按钮样式：文字在左，图标在右，无边框，左对齐
        self.toggle_button.setStyleSheet("""
            QToolButton {
                border: none;
                padding: 4px;
                font-weight: bold;
                color: rgb(200, 200, 200);
            }
            QToolButton:hover {
                color: rgb(169, 255, 175);
            }
        """)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)   # 默认收起状态：右箭头
        self.toggle_button.setCheckable(True)             # 可勾选状态，用于记录展开/收起
        self.toggle_button.setChecked(False)              # 默认收起
        self.toggle_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # --- 内容区域（默认高度为0，即收起状态）---
        self.content_area = QFrame()
        self.content_area.setMaximumHeight(0)             # 收起时高度为0
        self.content_area.setMinimumHeight(0)
        self.content_area.setFrameShape(QFrame.NoFrame)

        # 内容区域使用垂直布局，内部可以添加任意部件
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setSpacing(4)
        self.content_layout.setContentsMargins(8, 4, 8, 4)

        # --- 组装自身布局 ---
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_area)

        # 连接信号：点击标题按钮时切换展开/收起
        self.toggle_button.toggled.connect(self._on_toggled)

    def _on_toggled(self, checked):
        """
        点击标题按钮时的回调
        checked=True 表示展开，checked=False 表示收起
        """
        # 切换箭头方向
        self.toggle_button.setArrowType(Qt.DownArrow if checked else Qt.RightArrow)

        if checked:
            # 展开：取消高度限制，让布局自动计算
            self.content_area.setMaximumHeight(16777215)
        else:
            # 收起：高度设为0
            self.content_area.setMaximumHeight(0)

    def add_widget(self, widget):
        """向内容区域添加部件"""
        self.content_layout.addWidget(widget)


# =============================================================================
#  主工具箱类
# =============================================================================
class Rigging_Toolbox(QWidget):
    """
    Rigging 工具箱主类
    按分类生成可折叠面板，每个面板内包含该分类下的工具按钮
    """

    def __init__(self, parent=None):
        # 如果没有传入父窗口，自动获取 Maya 主窗口
        if parent is None:
            parent = get_maya_main_window()
        super(Rigging_Toolbox, self).__init__(parent)

        # 设置窗口属性
        self.setWindowTitle("木子绑定工具盒")
        self.setWindowFlags(Qt.Window)
        self.setMinimumWidth(340)
        self.setMinimumHeight(400)

        # 创建界面
        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        """
        创建 UI 部件
        从 tools 包获取按分类组织的工具，为每个分类创建一个可折叠面板
        """
        # 标题标签
        self.title_label = QLabel("Rigging Toolbox")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: rgb(169, 255, 175);")
        self.title_label.setAlignment(Qt.AlignCenter)

        # 获取按分类组织的工具字典
        # 结构：{"基础工具": {"constraint_tool": func, ...}, ...}
        self.tools_by_category = get_tools_by_category()

        # 存储每个分类的可折叠面板实例 {分类名: Collapsible_Box}
        self.category_boxes = {}

        # 为每个分类创建折叠面板
        for category_name, tools_dict in self.tools_by_category.items():
            box = Collapsible_Box(title=category_name)

            # 在该分类下创建按钮
            for tool_name, tool_func in tools_dict.items():
                # 生成友好的显示名称：constraint_tool -> Constraint Tool
                display_name = tool_name.replace("_", " ").title()
                btn = QPushButton(display_name)
                btn.setToolTip(f"点击打开 {tool_name}.py")
                btn.setMinimumHeight(28)
                # 使用 *args 兼容不同 PySide 版本的信号参数传递
                tool_key = "{}/{}".format(category_name, tool_name)
                btn.clicked.connect(
                    lambda *args, key=tool_key, f=tool_func: window_manager.show_tool(key, f)
                )
                box.add_widget(btn)

            self.category_boxes[category_name] = box

        # 如果没有发现任何工具，显示提示
        if not self.tools_by_category:
            self.empty_label = QLabel("未发现工具\n请确保 tools 目录下有子文件夹和 .py 文件\n且每个 .py 文件包含 main() 函数")
            self.empty_label.setAlignment(Qt.AlignCenter)
            self.empty_label.setStyleSheet("color: rgb(255, 100, 100);")

    def create_layouts(self):
        """
        组装布局
        使用滚动区域防止分类过多时窗口被撑爆
        """
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # 添加标题
        main_layout.addWidget(self.title_label)

        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: rgb(100, 100, 100);")
        main_layout.addWidget(line)

        # 如果有工具分类，用滚动区域包裹所有折叠面板
        if self.tools_by_category:
            # 创建一个 QWidget 作为滚动区域的容器
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_layout.setSpacing(4)
            scroll_layout.setContentsMargins(0, 0, 0, 0)

            # 逐个添加分类折叠面板
            for box in self.category_boxes.values():
                scroll_layout.addWidget(box)

            # 底部弹性空间
            scroll_layout.addStretch()

            # 创建滚动区域
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)    # 内容区域可随窗口调整大小
            scroll_area.setFrameShape(QFrame.NoFrame)
            scroll_area.setWidget(scroll_content)

            main_layout.addWidget(scroll_area)
        else:
            main_layout.addWidget(self.empty_label)
            main_layout.addStretch()


def main():
    """
    显示 Rigging 工具箱窗口
    全局变量保存窗口实例，方便关闭旧窗口后重建
    """
    global rigging_toolbox_window

    # 关闭并删除旧窗口（如果存在）
    try:
        rigging_toolbox_window.close()
        rigging_toolbox_window.deleteLater()
    except:
        pass

    # 创建并显示新窗口
    rigging_toolbox_window = Rigging_Toolbox()
    rigging_toolbox_window.show()
    rigging_toolbox_window.raise_()
    rigging_toolbox_window.activateWindow()
    return rigging_toolbox_window


if __name__ == "__main__":
    main()