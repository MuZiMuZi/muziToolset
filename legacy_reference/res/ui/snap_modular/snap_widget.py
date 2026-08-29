# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals, print_function
import os
from maya.OpenMayaUI import  MQtUtil
import sys

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
from importlib import reload
import muziToolset.core.snapUtils as snapUtils
import muziToolset.res.ui.backGround as backGround
reload(backGround)
reload(snapUtils)


class SnapWindow(backGround.BackGround):
    def __init__(self,parent =None):
        super(SnapWindow, self).__init__(parent)
        self.ui = None
        self.init_ui()

    def init_ui(self):
        # loader = PySide2.QtUiTools.QUiLoader()
        # # currentDir = os.path.dirname(__file__)#如果是import到maya中就可以的使用方法获得路径
        # currentDir = os.path.abspath(__file__ + "/../../../ui/snap_modular")
        # file = QFile(currentDir + "/test.ui")  # 这个方法要使用绝对路径
        # self.ui = loader.load(file, parentWidget=self)  # 初始化

        # 添加主页面布局

        self.main_layout = QVBoxLayout(self)
        self.setWindowTitle(u'吸附工具')
        self.resize(300, 300)
        self.main_layout.addWidget(QLabel("吸附方式"))


        # 添加主页面布局小部件

        self.combo_box = QComboBox(self)
        self.combo_box.addItem('Position + Rotation')
        self.combo_box.addItem('Position')
        self.combo_box.addItem('Rotation')
        self.combo_box.currentIndexChanged.connect(self.show_combo_selection)

        self.push_button = QPushButton("吸附")
        self.push_button.clicked.connect(self.push_snip)

        self.create_locator_button = QPushButton("创建定位器")
        self.create_locator_button.clicked.connect(self.create_locator)

        self.create_joint_button = QPushButton("创建关节")
        self.create_joint_button.clicked.connect(self.create_joint)

        # 添加主页面布局小部件到主页面布局
        self.main_layout.addWidget(self.combo_box)
        self.main_layout.addWidget(self.push_button)
        self.main_layout.addWidget(self.create_locator_button)
        self.main_layout.addWidget(self.create_joint_button)
        self.main_layout.addStretch(0)

    def show_combo_selection(self):
      return self.combo_box.currentText()

    def push_snip(self):
        sel_list = cmds.ls(selection=True, flatten=True)
        if len(sel_list) >= 1:
            objs_list = sel_list[:-1]
            obj = sel_list[-1]
            combo_txt = self.show_combo_selection()
            i = snapUtils.Snap(obj, objs_list, combo_txt)
            i.snap()
        else :
            cmds.warning("请选择两个或以上的物体或者Cv点")

    def create_locator(self):
        """
        快速定位定位器
        :return:
        """
        objs_list = cmds.ls(selection=True, flatten=True)
        if len(objs_list) >= 1:
            obj = cmds.spaceLocator(name = 'loc_' + objs_list[0] )
            combo_txt = self.show_combo_selection()
            loc = snapUtils.Snap(obj, objs_list, combo_txt)
            loc.snap()
        else:
            cmds.warning("请选择一个或以上的物体或者Cv点")

    def create_joint(self):
        """
        快速定位关节
        :return:
        """
        objs_list = cmds.ls(selection=True, flatten=True)
        if len(objs_list) >= 1:
            obj = cmds.createNode('joint',name = 'jnt_' + objs_list[0] )
            combo_txt = self.show_combo_selection()
            jnt = snapUtils.Snap(obj, objs_list, combo_txt)
            jnt.snap()
        else:
            cmds.warning("请选择一个或以上的物体或者Cv点")

def show():
    global win
    try:
        win.close()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
    except:
        pass
    win = SnapWindow()
    win.show()

def main():
    return SnapWindow()