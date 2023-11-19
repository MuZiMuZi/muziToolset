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
        self.attr_window_label = QLabel ('----------------属性编辑----------------')
        self.attr_window_label.setStyleSheet (u"color: rgb(255, 0, 0);")
        self.add_attr_window_btn = QPushButton (QIcon (icon_dir + '/add.png') , 'Add_Attribute')
        self.add_attr_window_btn.setToolTip ('打开添加属性窗口')
        self.edit_attr_window_btn = QPushButton (QIcon (icon_dir + '/edit.png') , 'Edit_Attribute')
        self.edit_attr_window_btn.setToolTip ('打开编辑属性窗口')
        self.connect_attr_window_btn = QPushButton (QIcon (icon_dir + '/connect-empty.png') ,
                                                    'Connect_Attr')
        self.connect_attr_window_btn.setToolTip ('打开连接编辑器')
        self.channel_control_window_btn = QPushButton (QIcon (icon_dir + '/set.png') , 'Channel_Control')
        self.channel_control_window_btn.setToolTip ('打开通道控制编辑器')
        self.delete_attr_window_btn = QPushButton (QIcon (icon_dir + '/delete.png') , 'Delete_Attr')
        self.delete_attr_window_btn.setToolTip ('删除选中的属性')

        # 创建属性工具的页面部件
        self.attr_tool_label = QLabel ('----------------属性工具----------------')
        self.attr_tool_label.setStyleSheet (u"color: rgb(255,170, 255);")
        self.attr_move_label = QLabel ('选择单个属性进行位移-------')
        self.attr_up_btn = QPushButton (QIcon (icon_dir + '/arrow-upward .png') , 'Attr_up')
        self.attr_up_btn.setToolTip ('使选中的属性在通道盒上移')
        self.attr_down_btn = QPushButton (QIcon (icon_dir + '/arrow-downward.png') , 'Attr_down')
        self.attr_down_btn.setToolTip ('使选中的属性在通道盒下移')

        # 创建属性设置的页面部件
        self.attr_set_label = QLabel ('----------------属性设置----------------')
        self.attr_set_label.setStyleSheet (u"color: rgb(170, 255, 255);")
        # 位移
        self.translation_set_label = QLabel ('Translation:')
        self.translation_locked_cheekbox = QCheckBox ('Locked')
        self.translation_hidden_cheekbox = QCheckBox ('Hidden')

        # 选择
        self.rotate_set_label = QLabel ('Rotate:')
        self.rotate_locked_cheekbox = QCheckBox ('Locked')
        self.rotate_hidden_cheekbox = QCheckBox ('Hidden')

        # 缩放
        self.scale_set_label = QLabel ('Scale:')
        self.scale_locked_cheekbox = QCheckBox ('Locked')
        self.scale_hidden_cheekbox = QCheckBox ('Hidden')

        # 可见性
        self.visability_set_label = QLabel ('Visability:')
        self.visability_locked_cheekbox = QCheckBox ('Locked')
        self.visability_hidden_cheekbox = QCheckBox ('Hidden')

        # 设置按钮
        self.attr_set_btn = QPushButton (QIcon (icon_dir + '/set.png') ,'Set')
        self.attr_set_btn.setToolTip ('根据选择的属性设置来设置属性的锁定和隐藏')
        self.attr_reset_btn = QPushButton (QIcon (icon_dir + '/reset.png') ,'Reset')
        self.attr_reset_btn.setToolTip ('重置选择的属性设置')

        self.attr_cheekbox = [self.translation_locked_cheekbox , self.translation_hidden_cheekbox ,

                              self.rotate_locked_cheekbox , self.rotate_hidden_cheekbox ,

                              self.scale_locked_cheekbox , self.scale_hidden_cheekbox ,

                              self.visability_locked_cheekbox , self.visability_hidden_cheekbox ,
                              ]


    def create_layouts (self) :
        # 创建属性编辑器的页面布局
        self.attr_window_layout = QGridLayout ()
        self.attr_window_layout.addWidget (self.add_attr_window_btn , 0 , 0)
        self.attr_window_layout.addWidget (self.edit_attr_window_btn , 0 , 1)
        self.attr_window_layout.addWidget (self.connect_attr_window_btn , 0 , 2)
        self.attr_window_layout.addWidget (self.channel_control_window_btn , 1 , 0)
        self.attr_window_layout.addWidget (self.delete_attr_window_btn , 1 , 1)

        # 创建属性工具的页面布局
        self.attr_tool_layout = QVBoxLayout ()
        self.attr_translate_layout = QHBoxLayout ()
        self.attr_translate_layout.addWidget (self.attr_move_label)
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

        # 旋转属性设置页面
        self.rotate_set_layout = QHBoxLayout ()
        self.rotate_set_layout.addWidget (self.rotate_set_label)
        self.rotate_set_layout.addWidget (self.rotate_locked_cheekbox)
        self.rotate_set_layout.addWidget (self.rotate_hidden_cheekbox)

        # 缩放属性设置页面
        self.scale_set_layout = QHBoxLayout ()
        self.scale_set_layout.addWidget (self.scale_set_label)
        self.scale_set_layout.addWidget (self.scale_locked_cheekbox)
        self.scale_set_layout.addWidget (self.scale_hidden_cheekbox)

        # 可见性属性设置页面
        self.visability_set_layout = QHBoxLayout ()
        self.visability_set_layout.addWidget (self.visability_set_label)
        self.visability_set_layout.addWidget (self.visability_locked_cheekbox)
        self.visability_set_layout.addWidget (self.visability_hidden_cheekbox)

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
        self.channel_control_window_btn.clicked.connect (lambda *args : cmds.ChannelControlEditor ())
        self.delete_attr_window_btn.clicked.connect (lambda *args : mel.eval ("dynDeleteAttrWin({})"))

        # 创建属性工具的页面部件连接
        self.attr_up_btn.clicked.connect (lambda *args : attrUtils.Attr.move_channelBox_attr (up = True))
        self.attr_down_btn.clicked.connect (lambda *args : attrUtils.Attr.move_channelBox_attr (down = True))

        # 创建属性设置的页面布局连接
        self.attr_set_btn.clicked.connect (self.clicked_attr_set_btn)
        self.attr_reset_btn.clicked.connect (self.clicked_attr_reset_btn)


    def clicked_attr_set_btn (self) :
        """
        设置所选择的物体的属性
        """
        # 获取所选择的物体
        obj_list = cmds.ls (sl = True)

        # 设置物体的属性
        for obj in obj_list :
            for axis in ['X' , 'Y' , 'Z'] :
                # 设置物体的位移设置
                attrUtils.Attr.lock_hide_attr (obj , 'translate' + axis ,
                                               lock = self.translation_locked_cheekbox.isChecked () ,
                                               hide = self.translation_hidden_cheekbox.isChecked ()
                                               )
                # 设置物体的旋转设置
                attrUtils.Attr.lock_hide_attr (obj , 'rotate' + axis ,
                                               lock = self.rotate_locked_cheekbox.isChecked () ,
                                               hide = self.rotate_hidden_cheekbox.isChecked ()
                                               )
                # 设置物体的缩放设置
                attrUtils.Attr.lock_hide_attr (obj , 'scale' + axis ,
                                               lock = self.scale_locked_cheekbox.isChecked () ,
                                               hide = self.scale_hidden_cheekbox.isChecked ()
                                               )
            attrUtils.Attr.lock_hide_attr (obj , 'visibility' ,
                                           lock = self.visability_locked_cheekbox.isChecked () ,
                                           hide = self.visability_hidden_cheekbox.isChecked ()
                                           )


    def clicked_attr_reset_btn (self) :
        """
        重置所有属性设置
        """
        for cheekbox in self.attr_cheekbox :
            cheekbox.setChecked (False)


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
