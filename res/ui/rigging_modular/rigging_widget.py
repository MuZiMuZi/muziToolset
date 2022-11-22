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
reload(backGround)



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





def show():
    global win
    try:
        win.close()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
    except:
        pass
    win = RiggingWindow()
    win.show()
