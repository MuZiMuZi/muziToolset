import os
from PySide2 import QtCore , QtWidgets , QtGui

from PySide2.QtCore import Qt
from PySide2.QtUiTools import QUiLoader
from ..widget import bone_widget
from ..config import Side , ui_dir
from ..ui import bind_ui , base_ui
from .....bind.module.base import base
from importlib import reload


reload (bone_widget)
reload(base)


class Base_Widget (base_ui.Ui_MainWindow , QtWidgets.QMainWindow) :


    def __init__ (self , *args , **kwargs ) :
        '''
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        super ().__init__ (*args , **kwargs)


        self.name = None
        self.side = None
        self.jnt_number = None
        self.jnt_parent = None
        self.control_parent = None

        self.init_base()

    def init_base (self) :
        """
        初始化作为QWidget对象的base_widget属性,用于设置绑定的基础属性（例如名称，边，关节数量，关节的父对象，控制器的父对象）
        """
        # 调用父类的ui方法，来运行ui
        self.setupUi (self)
        self.base_widget = self.centralwidget
        # 添加边的combox
        for side in Side :
            self.side_cbox.addItem (side.value)
        self.add_connect()



    def add_connect (self) :
        u"""
        用来添加连接的槽函数
        """
        # self.create_btn.clicked.connect (lambda :print(12))
        self.create_btn.clicked.connect (self.print_test)
        # self.base_widget.delete_btn.clicked.connect (self.delete_setup)


    def print_test(self,zz):
        print(zz)

    def parse_base (self , zzz) :
        """
        分析base_widget中的输入并将其作为参数返回
        """
        self.name = self.name_edit.text ()
        self.side = self.side_cbox.currentText ()
        self.jnt_number = self.jnt_number_sbox.currentText ()
        self.jnt_parent = self.jnt_parent_edit.text ()
        self.control_parent = self.control_parent_edit.text ()
        print ('parse_base')


    def build_setup (self) :
        # 读取输入信息

        self.parse_base ()

        #
        # # 生成定位关节系统
        # self.setup = base.Base (self.side , self.name , self.jnt_number , self.jnt_parent , self.control_parent)
        # self.setup.build_setup ()
