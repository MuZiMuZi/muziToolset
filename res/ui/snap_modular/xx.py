# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals, print_function

import PySide2

from maya.OpenMayaUI import MQtUtil

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

import os

mayaMainWindowPtr = MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)  # type: object # 获得Maya主窗口


class CreateUI(QWidget):
    def __init__(self, *args, **kwargs):
        super(CreateUI, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)  # 将新窗口设置为maya的子级
        self.ui = None
        self.setWindowFlags(Qt.Window)
        self.initUI()

    def initUI(self):
        loader = PySide2.QtUiTools.QUiLoader()
        # currentDir = os.path.dirname(__file__)#如果是import到maya中就可以的使用方法获得路径
        currentDir = os.path.abspath(__file__ + "/../../../ui/widget")
        file = QFile(currentDir + "/test.ui") # 这个方法要使用绝对路径
        self.ui = loader.load(file)  # 初始化
        # file.open(QFile.ReadOnly)
        # file.open
        # file.close()


def show():
    win = CreateUI()
    win.show()
    return win


if __name__ == '__main__':
    show()



