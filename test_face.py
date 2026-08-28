from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys
from importlib import reload
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance


def get_maya_window () :
    u'''
    获取maya的主窗口，判断python的版本号，如果大于3的话就使用int
    :return:
    '''
    # c++的指针概念，获取maya的窗口对象
    pointer = omui.MQtUtil.mainWindow ()
    # 判断python的版本号，如果大于3的话就使用int
    if sys.version_info.major >= 3 :
        return wrapInstance (int (pointer) , QWidget)
    else :
        return wrapInstance (long (pointer) , QWidget)


class Face_tool (QMainWindow) :

    # 创建一个用来设置驱动关键帧的工具页面

    def __init__ (self , parent = get_maya_window ()) :
        super (Face_tool , self).__init__ (parent)

        # 设置标题
        self.setWindowTitle ("Face_tool")
        # 设置宽高
        self.setMinimumSize (500 , 600)

        # 添加ui布局
        self.create_layouts ()


    def create_layouts (self) :
        # 创建主布局
        self.main_layout = QHBoxLayout (self)  # 使用 QVBoxLayout 创建主布局，命名为 main_layout。

        self.test_button = QPushButton(parent = self.main_layout)
        self.main_layout.addWidget(self.test_button)




tool = Face_tool ()
tool.show ()
