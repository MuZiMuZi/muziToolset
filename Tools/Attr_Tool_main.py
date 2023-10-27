import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pymel.core as pm
from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils , jointUtils , qtUtils , controlUtils , snapUtils , connectionUtils , \
    attrUtils
from importlib import reload
import maya.mel as mel
import maya.cmds as cmds


class Attr_Tool (QWidget) :
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
        # 创建属性编辑器的页面部件
        self.attr_window_label = QLabel ('属性编辑——————————')
        self.add_attr_window_btn = QPushButton ('Add_Attribute(添加属性)')
        self.edit_attr_window_btn = QPushButton ('Edit_Attribute(编辑属性)')
        self.connect_attr_window_btn = QPushButton ('Connect_Attr(连接编辑器)')
        self.channel_control_window_btn = QPushButton ('Channel_Control(通道控制)')
        self.delete_attr_window_btn = QPushButton ('Delete_Attr(删除属性)')

        # 创建属性工具的页面部件
        self.attr_tool_label = QLabel ('属性工具——————————')
        self.attr_up_btn = QPushButton ('attr_up(属性上移)')
        self.attr_down_btn = QPushButton ('attr_down(属性下移)')

        # 创建属性设置的页面部件
        self.attr_set_label = QLabel ('属性设置——————————')
        # 位移
        self.translation_set_label = QLabel ('Translation:')
        self.translation_locked_cheekbox = QCheckBox ('Locked')
        self.translation_hidden_cheekbox = QCheckBox ('Hidden')
        self.translation_nonkeyable_cheekbox = QCheckBox ('Nonkeyable')
        # 选择
        self.rotate_set_label = QLabel ('Rotate:')
        self.rotate_locked_cheekbox = QCheckBox ('Locked')
        self.rotate_hidden_cheekbox = QCheckBox ('Hidden')
        self.rotate_nonkeyable_cheekbox = QCheckBox ('Nonkeyable')
        # 缩放
        self.scale_set_label = QLabel ('Scale:')
        self.scale_locked_cheekbox = QCheckBox ('Locked')
        self.scale_hidden_cheekbox = QCheckBox ('Hidden')
        self.scale_nonkeyable_cheekbox = QCheckBox ('Nonkeyable')
        # 可见性
        self.visability_set_label = QLabel ('Visability:')
        self.visability_locked_cheekbox = QCheckBox ('Locked')
        self.visability_hidden_cheekbox = QCheckBox ('Hidden')
        self.visability_nonkeyable_cheekbox = QCheckBox ('Nonkeyable')
        # 设置按钮
        self.attr_set_btn = QPushButton ('set(设置)')
        self.attr_reset_btn = QPushButton ('reset(重置)')

        self.attr_cheekbox = [self.translation_locked_cheekbox , self.translation_hidden_cheekbox ,
                              self.translation_nonkeyable_cheekbox ,
                              self.rotate_locked_cheekbox , self.rotate_hidden_cheekbox ,
                              self.rotate_nonkeyable_cheekbox ,
                              self.scale_locked_cheekbox , self.scale_hidden_cheekbox ,
                              self.scale_nonkeyable_cheekbox ,
                              self.visability_locked_cheekbox , self.visability_hidden_cheekbox ,
                              self.visability_nonkeyable_cheekbox]


    def create_layouts (self) :
        # 创建属性编辑器的页面布局
        self.attr_window_layout = QGridLayout ()
        self.attr_window_layout.addWidget (self.add_attr_window_btn , 0 , 0)
        self.attr_window_layout.addWidget (self.edit_attr_window_btn , 0 , 1)
        self.attr_window_layout.addWidget (self.connect_attr_window_btn , 0 , 2)
        self.attr_window_layout.addWidget (self.channel_control_window_btn , 1 , 0)
        self.attr_window_layout.addWidget(self.delete_attr_window_btn,1,1)

        # 创建属性工具的页面布局
        self.attr_tool_layout = QVBoxLayout ()
        self.attr_translate_layout = QHBoxLayout ()
        self.attr_translate_layout.addWidget (self.attr_up_btn)
        self.attr_translate_layout.addWidget (self.attr_down_btn)
        self.attr_tool_layout.addLayout (self.attr_translate_layout)

        # 创建属性设置的页面布局
        self.attr_set_layout = QVBoxLayout ()
        self.create_attr_set_layout ()

        self.main_layout = QVBoxLayout (self)
        self.main_layout.addWidget (self.attr_window_label)
        self.main_layout.addLayout (self.attr_window_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.attr_tool_label)
        self.main_layout.addLayout (self.attr_tool_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.attr_set_label)
        self.main_layout.addLayout (self.attr_set_layout)
        self.main_layout.addStretch ()


    def create_attr_set_layout (self) :
        """
        创建属性设置的页面布局
        """
        # 位移属性设置页面
        self.translation_set_layout = QHBoxLayout ()
        self.translation_set_layout.addWidget (self.translation_set_label)
        self.translation_set_layout.addWidget (self.translation_locked_cheekbox)
        self.translation_set_layout.addWidget (self.translation_hidden_cheekbox)
        self.translation_set_layout.addWidget (self.translation_nonkeyable_cheekbox)
        # 旋转属性设置页面
        self.rotate_set_layout = QHBoxLayout ()
        self.rotate_set_layout.addWidget (self.rotate_set_label)
        self.rotate_set_layout.addWidget (self.rotate_locked_cheekbox)
        self.rotate_set_layout.addWidget (self.rotate_hidden_cheekbox)
        self.rotate_set_layout.addWidget (self.rotate_nonkeyable_cheekbox)
        # 缩放属性设置页面
        self.scale_set_layout = QHBoxLayout ()
        self.scale_set_layout.addWidget (self.scale_set_label)
        self.scale_set_layout.addWidget (self.scale_locked_cheekbox)
        self.scale_set_layout.addWidget (self.scale_hidden_cheekbox)
        self.scale_set_layout.addWidget (self.scale_nonkeyable_cheekbox)
        # 可见性属性设置页面
        self.visability_set_layout = QHBoxLayout ()
        self.visability_set_layout.addWidget (self.visability_set_label)
        self.visability_set_layout.addWidget (self.visability_locked_cheekbox)
        self.visability_set_layout.addWidget (self.visability_hidden_cheekbox)
        self.visability_set_layout.addWidget (self.visability_nonkeyable_cheekbox)

        # 操作页面布局
        self.attr_operate_layout = QHBoxLayout ()
        self.attr_operate_layout.addWidget (self.attr_set_btn)
        self.attr_operate_layout.addWidget (self.attr_reset_btn)

        # 将所有页面布局添加到创建属性设置的页面布局
        self.attr_set_layout.addLayout (self.translation_set_layout)
        self.attr_set_layout.addLayout (self.rotate_set_layout)
        self.attr_set_layout.addLayout (self.scale_set_layout)
        self.attr_set_layout.addLayout (self.visability_set_layout)
        self.attr_set_layout.addLayout (self.attr_operate_layout)


    def add_connnect (self) :
        # 创建属性编辑器的页面部件连接
        self.add_attr_window_btn.clicked.connect (lambda *args : mel.eval ("dynAddAttrWin({})"))
        self.edit_attr_window_btn.clicked.connect (lambda *args : mel.eval ("dynRenameAttrWin({})"))
        self.connect_attr_window_btn.clicked.connect (lambda *args : cmds.ConnectionEditor ())
        self.channel_control_window_btn.clicked.connect (lambda *args :cmds.ChannelControlEditor() )
        self.delete_attr_window_btn.clicked.connect(lambda *args : mel.eval ("dynDeleteAttrWin({})"))

        #创建属性工具的页面部件连接
        self.attr_up_btn.clicked.connect(lambda *args :attrUtils.Attr.move_channelBox_attr(up = True))
        self.attr_down_btn.clicked.connect(lambda *args :attrUtils.Attr.move_channelBox_attr(down = True))


def main () :
    return Attr_Tool ()


if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = Attr_Tool ()  # 创建实例
    window.show ()  # 显示窗口
