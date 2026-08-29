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
import maya.OpenMayaUI as OpenMayaUI

def get_maya_window():
    maya_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    maya_window_widget = wrapInstance(long(maya_window_ptr),QWidget)
    return maya_window_widget

class BackGround(QWidget):
    def paintEvent(self, *args, **kwargs):
        """
        制作一个用于区分各模块之间的黑色方框
        Args:
            *args:
            **kwargs:

        Returns:

        """
        p = QPainter(self)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(65, 65, 65)))
        p.drawRect(self.rect())
        p.end()

    def get_maya_window(self):
        maya_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        maya_window_widget = wrapInstance(long(maya_window_ptr), QWidget)
        return maya_window_widget