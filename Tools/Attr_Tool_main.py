import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pymel.core as pm
from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils , jointUtils , qtUtils , controlUtils , snapUtils , connectionUtils , \
    attrUtils
from importlib import reload

import maya.cmds as cmds


class Attr_Tool(QWidget) :
    """
    属性工具的面板
    """


    def __init__ (self , parent = None) :
        super (Attr_Tool , self).__init__ (parent)
        self.win_name = 'Attr_Tool'
        self.win_title = 'Attr_Tool(属性工具)'
        self.create_widgets ()
        self.create_layouts ()
        self.add_connnect ()


    def create_widgets (self) :
        """
        创建连接的部件
        """
        self.attr_window_label = QLabel('属性编辑——————————')
        self.add_attr_window_btn = QPushButton('Add_Attribute(添加属性)')
        self.edit_attr_window_btn = QPushButton ('Edit_Attribute(编辑属性)')
        self.set_driven_key_window_btn = QPushButton ('Set Driven Key(设置收驱动关键帧)')
        self.channel_control_window_btn = QPushButton ('Channel Control(通道控制)')

    def create_layouts (self) :
        self.attr_window_layout = QVBoxLayout()
        self.main_layout.addWidget (self.add_attr_window_btn)
        self.main_layout.addWidget (self.edit_attr_window_btn)
        self.main_layout.addWidget (self.edit_attr_window_btn)
        self.main_layout.addWidget (self.edit_attr_window_btn)



        self.main_layout = QHBoxLayout(self)



    def add_connnect (self) :
        pass


def main():
    return Attr_Tool()

if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = Attr_Tool ()  # 创建实例
    window.show ()  # 显示窗口
