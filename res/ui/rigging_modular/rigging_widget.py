# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals, print_function
import os

import PySide2
from PySide2.QtUiTools import QUiLoader
from maya.OpenMayaUI import  MQtUtil
import sys

import muziToolset.res.ui.backGround as backGround

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
import muziToolset.conf.config as config
import muziToolset.rigging.build_rig as build_rig



class RiggingWindow(QWidget):
    def __init__(self):
        super(RiggingWindow, self).__init__()
        self.ui = None
        self.init_ui()

    def init_ui(self):
        # 检查maya使用的python解释器版本,设置小部件的父对象
        if sys.version_info.major  >= 3:
            self.setParent(wrapInstance(int(MQtUtil.mainWindow()), QWidget))
        else:
            self.setParent(wrapInstance(long(MQtUtil.mainWindow()),QWidget))

        self.setWindowTitle('木子绑定系统 {}'.format(config.VERSION))
        self.setWindowFlags(Qt.Window)

        # 读取qt Designer 写的ui文件
        loader = QUiLoader()
        # currentDir = os.path.dirname(__file__)#如果是import到maya中就可以的使用方法获得路径
        currentDir = os.path.abspath(__file__ + "/../../../ui/rigging_modular")
        file = QFile(currentDir + "/rigging.ui")  # 这个方法要使用绝对路径
        self.ui = loader.load(file, parentWidget=self)  # 初始化

        # 连接ui文件的部件
        # 连接模版的listview
        self.Template_listView = self.ui.Template_listView
        #连接模块的listview
        self.modular_listView = self.ui.modular_listView
        #连接导入按钮
        self.import_button = self.ui.import_button
        self.import_button.clicked.connect(self.clicked_import_button)
        #连接关节方向的设置
        self.jointDirection_label = self.ui.jointDirection_label
        self.jointDirection_true_radioButton = self.ui.jointDirection_true_radioButton
        self.jointDirection_false_radioButton = self.ui.jointDirection_false_radioButton

        #连接关节大小的设置
        self.jointSize_label = self.ui.jointSize_label
        self.jointSize_slider = self.ui.jointSize_slider

        #连接清除的设置
        self.clear_button = self.ui.clear_button
        self.clear_button.clicked.connect(self.clicked_clear_button)

        #连接属性的lsitview
        self.property_listWidget = self.ui.property_listWidget

        #连接关节显示的设置
        self.jointVis_label = self.ui.jointVis_label
        self.jointVis_true_radioButton = self.ui.jointVis_true_radioButton
        self.jointVis_false_radioButton = self.ui.jointVis_false_radioButton

        #连接模型显示的设置
        self.modleVis_label = self.ui.modleVis_label
        self.modleVis_true_radioButton = self.ui.modleVis_true_radioButton
        self.modleVis_false_radioButton = self.ui.modleVis_false_radioButton

        #连接控制器显示的设置
        self.ctrlVis_label = self.ui.ctrlVis_label
        self.ctrlVis_true_radioButton = self.ui.ctrlVis_true_radioButton
        self.ctrlVis_false_radioButton = self.ui.ctrlVis_false_radioButton

        #连接控制器重置的设置
        self.reset_button = self.ui.reset_button
        self.reset_button.clicked.connect(self.clicked_reset_button)

        #连接创建绑定的设置
        self.build_button = self.ui.build_button
        self.build_button.clicked.connect(self.clicked_build_button)

    def clicked_import_button(self):
        build = build_rig.Build_Rig()
        build.import_modular()

    def clicked_clear_button(self):
        build = build_rig.Build_Rig()
        build.delete_modular()

    def clicked_reset_button(self):
        pass

    def clicked_build_button(self):
        build = build_rig.Build_Rig()
        build.build_rig()

#
def show():
    global win
    try:
        win.close()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
    except:
        pass
    win = RiggingWindow()
    win.show()
