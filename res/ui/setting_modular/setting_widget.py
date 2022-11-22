# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals, print_function

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtWidgets import *
    from PySide import __version__
    from shiboken import wrapInstance

import maya.cmds as cmds

import muziToolset.res.ui.backGround as backGround
import muziToolset.conf.setting as setting

class FontSettingWidget(backGround.BackGround):
    def __init__(self,parent = None):
        super(FontSettingWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 创建主页面布局
        self.setWindowTitle(u'设置')
        self.main_layout = QHBoxLayout(self)

        # 创建主页面布局小部件
        self.font = QLabel(self.font_setting())
        self.font_setting_button = QPushButton("设置")
        self.font_setting_button.clicked.connect(self.set_font_setting)

        # 添加主页面布局的小部件
        self.main_layout.addWidget(QLabel("字体 ： "))
        self.main_layout.addWidget(self.font)
        self.main_layout.addWidget(self.font_setting_button)

    def font_setting(self):
        """
        字体设置
        :return:
        """
        font = setting.get("font", None)
        if font is None:
            return QFont().toString()
        return font

    def set_font_setting(self):
        """
        设置字体的设置
        :return:
        """
        a,b = QFontDialog.getFont()
        if type(a) == bool:
            ok = a
            font = b
        else:
            ok = b
            font = a
        if ok:
            setting.set("font", font.toString())
        else:
            cmds.warning("取消了操作")




class SettingWidget(QWidget):
    def __init__(self,parent = None):
        super(SettingWidget, self).__init__(parent)
        self.init_ui()
    def init_ui(self):
        # 创建主页面布局
        self.main_layout = QVBoxLayout(self)
        self.setWindowTitle(u'全局设置工具')
        self.resize(300, 300)

        # 创建子页面布局
        self.font_setting_widget = FontSettingWidget()

        # 添加主页面布局的小部件
        self.main_layout.addWidget(self.font_setting_widget)
        self.main_layout.addStretch(0)

def show():
    global win
    try:
        win.close()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
    except:
        pass
    win = SettingWidget()
    win.show()


