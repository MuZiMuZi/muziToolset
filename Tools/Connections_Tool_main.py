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


reload (connectionUtils)
reload (attrUtils)


class Connections_Tool (QWidget) :
    """
这是一个用来写属性连接工具的类
"""


    def __init__ (self , parent = None) :
        super (Connections_Tool , self).__init__ (parent)
        self.win_name = 'Connections_Tool'
        self.win_title = 'Connections_Tool(连接工具)'
        self.create_widgets ()
        self.create_layouts ()
        self.add_connnect ()


    def create_widgets (self) :
        """
        创建连接的部件
        """
        # 创建默认属性连接的部件
        self.connect_default_connection_label = QLabel ('---------------连接默认属性---------------')
        self.connect_default_connection_label.setStyleSheet (u"color: rgb(169, 255, 175);")
        self.translate_attr_cheekbox = QCheckBox ('Translate')
        self.rotate_attr_cheekbox = QCheckBox ('Rotate')
        self.scale_attr_cheekbox = QCheckBox ('Scale')
        self.matrix_attr_cheekbox = QCheckBox ('Matrix')
        self.reset_attr_btn = QPushButton (QIcon (icon_dir + '/reset.png') , 'Reset')

        self.connect_default_connection_btn = QPushButton (QIcon (':parentConstraint.png') ,
                                                           'Create_connection')
        self.delete_default_connection_btn = QPushButton (QIcon (icon_dir + '/delete.png') ,
                                                          'Delete_connection')

        # 创建自定义属性连接的部件
        self.connect_custom_connection_label = QLabel ('---------------连接自定义属性---------------')
        self.connect_custom_connection_label.setStyleSheet (u"color: rgb(85, 255, 255);")
        self.driver_attr_label = QLabel ('Driver(驱动者):---')
        self.driver_attr_line = QLineEdit ()
        self.pick_driver_attr_btn = QPushButton (QIcon (icon_dir + '/select.png') , 'pick')

        self.driven_attr_label = QLabel ('Driven(被驱动者):')
        self.driven_attr_line = QLineEdit ()
        self.pick_driven_attr_btn = QPushButton (QIcon (icon_dir + '/select.png') , 'pick')

        self.connect_custom_connection_btn = QPushButton (QIcon (':parentConstraint.png') ,
                                                          'Create_connection')
        self.delete_custom_connection_btn = QPushButton (QIcon (icon_dir + '/delete.png') ,
                                                         'Delete_connection')

        # 创建复制属性连接的部件
        self.copy_delete_connection_label = QLabel ('---------------复制/删除属性连接---------------')
        self.copy_delete_connection_label.setStyleSheet (u"color: rgb(170, 255, 128);")
        self.copy_connection_btn = QPushButton (QIcon (icon_dir + '/copy.png') ,
                                                'Copy_Driven_connection--未完成')
        self.delete_connection_btn = QPushButton (QIcon (icon_dir + '/delete.png') ,
                                                  'Delete_Driven_connection')


    def create_layouts (self) :
        ##创建默认属性连接的的布局
        self.connect_default_connection_layout = QVBoxLayout ()
        # 创建默认属性的布局
        self.default_attr_layout = QHBoxLayout ()
        self.default_attr_layout.addWidget (self.translate_attr_cheekbox)
        self.default_attr_layout.addWidget (self.rotate_attr_cheekbox)
        self.default_attr_layout.addWidget (self.scale_attr_cheekbox)
        self.default_attr_layout.addWidget (self.matrix_attr_cheekbox)
        self.default_attr_layout.addWidget (self.reset_attr_btn)

        # 创建操作默认属性链接的布局
        self.operate_default_connection_layout = QHBoxLayout ()
        self.operate_default_connection_layout.addWidget (self.connect_default_connection_btn)
        self.operate_default_connection_layout.addWidget (self.delete_default_connection_btn)

        # 将default_attr_layout和operate_default_connection_layout，添加到connect_default_connection_layout里
        self.connect_default_connection_layout.addLayout (self.default_attr_layout)
        self.connect_default_connection_layout.addLayout (self.operate_default_connection_layout)

        ##创建自定义属性连接的布局
        self.connect_custom_connection_layout = QVBoxLayout ()

        # 创建驱动者的属性连接布局
        self.driver_attr_layout = QHBoxLayout ()
        self.driver_attr_layout.addWidget (self.driver_attr_label)
        self.driver_attr_layout.addWidget (self.driver_attr_line)
        self.driver_attr_layout.addWidget (self.pick_driver_attr_btn)

        # 创建驱动者的属性连接布局
        self.driven_attr_layout = QHBoxLayout ()
        self.driven_attr_layout.addWidget (self.driven_attr_label)
        self.driven_attr_layout.addWidget (self.driven_attr_line)
        self.driven_attr_layout.addWidget (self.pick_driven_attr_btn)

        # 创建操作自定义属性连接按钮的布局
        self.operate_custom_connection_layout = QHBoxLayout ()
        self.operate_custom_connection_layout.addWidget (self.connect_custom_connection_btn)
        self.operate_custom_connection_layout.addWidget (self.delete_custom_connection_btn)

        # 将驱动者的属性布局和被驱动者的属性布局添加到自定义属性连接布局
        self.connect_custom_connection_layout.addLayout (self.driver_attr_layout)
        self.connect_custom_connection_layout.addLayout (self.driven_attr_layout)
        self.connect_custom_connection_layout.addLayout (self.operate_custom_connection_layout)

        # 创建复制属性连接的页面布局
        self.copy_delete_connection_layout = QHBoxLayout ()
        self.copy_delete_connection_layout.addWidget (self.copy_connection_btn)
        self.copy_delete_connection_layout.addWidget (self.delete_connection_btn)

        # 创建main_layout的布局
        self.main_layout = QVBoxLayout (self)
        self.main_layout.addWidget (self.connect_default_connection_label)
        self.main_layout.addLayout (self.connect_default_connection_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.connect_custom_connection_label)
        self.main_layout.addLayout (self.connect_custom_connection_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.copy_delete_connection_label)
        self.main_layout.addLayout (self.copy_delete_connection_layout)
        self.main_layout.addStretch ()


    def add_connnect (self) :
        # 连接默认属性的部件
        self.matrix_attr_cheekbox.stateChanged.connect (self.stateChanged_matrix_attr_cheekbox)
        self.reset_attr_btn.clicked.connect (self.clicked_reset_attr_btn)
        self.connect_default_connection_btn.clicked.connect (self.clicked_connect_default_connection_btn)
        self.delete_default_connection_btn.clicked.connect (self.clicked_delete_default_connection_btn)

        # 连接自定义属性的部件
        self.pick_driver_attr_btn.clicked.connect (self.clicked_pick_driver_attr_btn)
        self.pick_driven_attr_btn.clicked.connect (self.clicked_pick_driven_attr_btn)
        self.connect_custom_connection_btn.clicked.connect (self.clicked_connect_custom_connection_btn)
        self.delete_custom_connection_btn.clicked.connect (self.clicked_delete_custom_connection_btn)

        # 连接复制/删除属性的部件
        self.copy_connection_btn.clicked.connect (self.clicked_copy_connection_btn)
        self.delete_connection_btn.clicked.connect (self.clicked_delete_connection_btn)


    def stateChanged_matrix_attr_cheekbox (self) :
        """
        当matrix_attr_cheekbox按钮被选中的时候，则将位移,旋转，缩放的属性选项全部取消
        """
        matrix_check_value = self.matrix_attr_cheekbox.isChecked ()
        if matrix_check_value :
            self.translate_attr_cheekbox.setChecked (False)
            self.rotate_attr_cheekbox.setChecked (False)
            self.scale_attr_cheekbox.setChecked (False)


    def clicked_reset_attr_btn (self) :
        """
        当reset_attr_btn按钮被按下的时候，则将位移,旋转，缩放，矩阵的属性选项全部取消
        """
        self.translate_attr_cheekbox.setChecked (False)
        self.rotate_attr_cheekbox.setChecked (False)
        self.scale_attr_cheekbox.setChecked (False)
        self.matrix_attr_cheekbox.setChecked (False)


    def clicked_connect_default_connection_btn (self) :
        translate_value = self.translate_attr_cheekbox.isChecked ()
        rotate_value = self.rotate_attr_cheekbox.isChecked ()
        scale_value = self.scale_attr_cheekbox.isChecked ()
        matrix_value = self.matrix_attr_cheekbox.isChecked ()
        if not translate_value and not rotate_value and not scale_value and not matrix_value :
            cmds.warning ('没有选中任何内容连接。请选中复选框进行连接')
            return
        obj_con = connectionUtils.Connection ()
        obj_con.create_srt_connections (translate = translate_value ,
                                           rotation = rotate_value ,
                                           scale = scale_value ,
                                           matrix = matrix_value)


    def clicked_delete_default_connection_btn (self) :
        translate_value = self.translate_attr_cheekbox.isChecked ()
        rotate_value = self.rotate_attr_cheekbox.isChecked ()
        scale_value = self.scale_attr_cheekbox.isChecked ()
        matrix_value = self.matrix_attr_cheekbox.isChecked ()
        if not translate_value and not rotate_value and not scale_value and not matrix_value :
            cmds.warning ('没有选中任何内容连接。请选中复选框进行断开连接')
            return

        obj_con = connectionUtils.Connection ()
        obj_con.delete_connect_srt_connections (translate = translate_value ,
                                          rotation = rotate_value ,
                                          scale = scale_value)


    def clicked_pick_driver_attr_btn (self) :
        # 获取选择的驱动者的属性
        driver_attr = attrUtils.Attr.get_channelBox_attrs ()
        # 获取选择的驱动者的对象
        driver = cmds.ls (sl = True) [0]
        # 将选定的驱动者的对象和属性添加到输入框内
        self.driver_attr_line.setText ('{}.{}'.format (driver , driver_attr [0]))


    def clicked_pick_driven_attr_btn (self) :
        self.driven_attr_line.clear()
        # 获取选择的被驱动者的对象
        drivens = cmds.ls (sl = True)
        self.driven_attr_line.drivens_attrs = []
        #对每个选择的被驱动对象循环，获取被驱动对象上需要被驱动的属性
        for driven in drivens :
            cmds.select (driven,replace = True)
            # 获取选择的被驱动者的属性
            driven_attr = attrUtils.Attr.get_channelBox_attrs ()
            # 将选定的驱动者的对象和属性存为一个变量drivens_attrs方便后续调用
            self.driven_attr_line.drivens_attrs.append(driven_attr)
            # 将选定的被驱动者的对象和属性添加到输入框内
            self.driven_attr_line.insert(driven_attr + ',')


    def clicked_connect_custom_connection_btn (self) :
        """
        连接自定义属性的槽函数
        """
        #获取driver_attr_line上的输入，格式为driver_obj.source_attr,
        # 例如['loctaor1.translate']
        source = self.driver_attr_line.text ()
        # 获取driver_attr_line上的输入，格式为driven_obj1.destination_attr,driven_obj2.destination_attr
        # 例如['loctaor1.translate','loctaor1.translate']
        destination_attr = self.driven_attr_line.text ()
        #判断输入框上是否有符合的对象，没有的话则报错
        if not sourceAttr:
            cmds.warning ("未加载驱动者的连接属性。请重新选择通道盒的属性进行加载")
        if not targetAttr :
            cmds.warning ("未加载被驱动者的连接属性。请重新选择通道盒的属性进行加载")

        #拆分driver_obj和source_attr
        driver_obj = source.split ('.') [0]
        source_attr = source.split ('.') [1]

        #拆分driven_obj_list 和 destination_attr
        print(self.driven_attr_line.drivens_attrs)
        #输入框上都有符合的对象的以后才进行连接
        # if source_attr and destination_attr:
        #     obj_con = connectionUtils.Connection ()
        #     obj_con.create_connect_connections_list(driver_obj , source_attr , driven_obj_list , destination_attr)


    def clicked_delete_custom_connection_btn (self) :
        sourceAttr = self.driver_attr_line.text ()
        targetAttr = self.driven_attr_line.text ()
        obj_con = connectionUtils.Connection ()
        obj_con.breakConnectionAttrsOrChannelBox (driverAttr = sourceAttr ,
                                                  drivenAttr = targetAttr)


    def clicked_copy_connection_btn (self) :
        obj_con = connectionUtils.Connection ()
        obj_con.copyDrivenConnectedAttrsSel ()


    def clicked_delete_connection_btn (self) :
        obj_con = connectionUtils.Connection ()
        obj_con.breakAllDrivenOrChannelBoxSel ()


def main () :
    return Connections_Tool ()


if __name__ == "__main__" :
    app = QApplication (sys.argv)
    mainwindow = Connections_Tool ()
    mainwindow.show ()
    sys.exit (app.exec_ ())
