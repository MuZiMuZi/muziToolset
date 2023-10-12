import os

from PySide2.QtUiTools import QUiLoader
from ..widget import bone_widget
from ..config import Side , ui_dir
from ..ui import bind_ui , base_ui
from .....bind.module.base import base
from importlib import reload


reload (bone_widget)
reload(base)


class Base_Widget (bone_widget.Bone_Widget , base_ui.Ui_MainWindow) :


    def __init__ (self , name = 'base') :
        '''
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        super (bone_widget.Bone_Widget , self).__init__ (name)
        self.base_ui = 'base.ui'
        self.init_base ()


        self.name = None
        self.side = None
        self.jnt_number = None
        self.jnt_parent = None
        self.control_parent = None
        self.add_connect()

    def init_base (self) :
        """
        初始化作为QWidget对象的base_widget属性,用于设置绑定的基础属性（例如名称，边，关节数量，关节的父对象，控制器的父对象）
        """

        self.base_widget = QUiLoader ().load (os.path.join (ui_dir , self.base_ui))
        # 添加边的combox
        for side in Side :
            self.base_widget.side_cbox.addItem (side.value)



    def parse_base (self) :
        """
        分析base_widget中的输入并将其作为参数返回
        """
        self.name = self.base_widget.name_edit.text ()
        self.side = self.base_widget.side_cbox.currentText ()
        self.jnt_number = self.base_widget.jnt_number_sbox.currentText ()
        self.jnt_parent = self.base_widget.jnt_parent_edit.text ()
        self.control_parent = self.base_widget.control_parent_edit.text ()


    def add_connect (self) :
        u"""
        用来添加连接的槽函数
        """
        self.base_widget.create_btn.clicked.connect (self.build_setup)
        # self.base_widget.delete_btn.clicked.connect (self.delete_setup)



    def build_setup (self , *args , **kwargs) :
        super ().build_setup (*args , **kwargs)
        # 读取输入信息
        self.parse_base ()

        # 生成定位关节系统
        self.setup = base.Base (self.side , self.name , self.joint_number , self.joint_parent , self.control_parent)
        self.setup.build_setup ()
