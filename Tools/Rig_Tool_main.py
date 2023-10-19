import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pymel.core as pm
from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils , jointUtils , qtUtils
from importlib import reload

import maya.cmds as cmds


reload (qtUtils)


class Rig_Tool (QWidget) :
    """
    一个绑定工具的类
    """


    def __init__ (self , parent = None) :
        super (Rig_Tool , self).__init__ (parent)
        self.win_name = 'Rig_Tool'
        self.win_title = 'Rig_Tool(绑定工具)'
        self.create_widgets ()
        self.create_layouts ()
        self.add_connnect ()


    def create_widgets (self) :
        # FK
        self.fk_label = QLabel ('---------------创建FK----------------')
        self.create_fk_button = QPushButton ('创建fk链条')
        self.delete_fk_button = QPushButton ('删除fk链条')
        # IK
        self.ik_label = QLabel ('---------------创建IK链条----------------')
        self.ik_start_button = QPushButton ('拾取ik起始关节')
        self.ik_start_line = QLineEdit ()
        self.ik_end_button = QPushButton ('拾取ik结束关节')
        self.ik_end_line = QLineEdit ()
        self.create_ik_button = QPushButton ('创建ik链条')
        self.delete_ik_button = QPushButton ('删除ik链条')

        # 约束
        self.constraint_label = QLabel ('---------------创建约束----------------')
        self.create_constraint_button = QPushButton ('创建约束')
        self.delete_constraint_button = QPushButton ('删除约束')

        # 工具
        self.tool_label = QLabel ('---------------绑定小工具---------------')
        self.create_tool_widgets ()


    def create_tool_widgets (self) :
        self.clear_keys_button = QPushButton (QIcon (':fileOpen.png') , "删除关键帧")

        self.reset_control_button = QPushButton ("重置控制器")

        self.batch_Constraints_modle_button = QPushButton ("批量约束_物体")

        self.batch_Constraints_joint_button = QPushButton ("批量约束_关节")

        self.default_grp_button = QPushButton (u"绑定层级组")

        self.create_joints_on_curve_button = QPushButton (u"曲线上点创建关节(通用)")

        self.create_joints_on_curve_rigging_button = QPushButton (u"曲线上点创建关节(自用)")

        self.control_hierarchy_button = QPushButton (u"自动打组(自用)")

        self.save_skinWeights_button = QPushButton (u"导出权重")

        self.load_skinWeights_button = QPushButton (u"导入权重")

        self.select_sub_objects_button = QPushButton ("快速选择子物体")

        self.print_duplicate_object_button = QPushButton ("检查并列出重名节点")

        self.rename_duplicate_object_button = QPushButton ("检查并重命名重名节点")

        self.create_dynamic_curve_driven_button = QPushButton ("创建动力学化曲线驱动头发")

        self.tool_buttons = [self.clear_keys_button , self.reset_control_button , self.batch_Constraints_modle_button ,
                             self.batch_Constraints_joint_button , self.default_grp_button ,
                             self.create_joints_on_curve_button ,
                             self.create_joints_on_curve_rigging_button , self.control_hierarchy_button ,
                             self.save_skinWeights_button ,
                             self.load_skinWeights_button , self.select_sub_objects_button ,
                             self.print_duplicate_object_button ,
                             self.rename_duplicate_object_button , self.create_dynamic_curve_driven_button]


    def create_layouts (self) :
        # 创建fk系统的layout
        self.fk_layout = QFormLayout ()
        self.fk_layout.addRow (self.fk_label)
        self.fk_ho_layout = QHBoxLayout ()
        self.fk_ho_layout.addWidget (self.create_fk_button)
        self.fk_ho_layout.addWidget (self.delete_fk_button)
        self.fk_layout.addRow (self.fk_ho_layout)

        # 创建ik系统的layout
        self.ik_layout = QFormLayout ()
        self.ik_layout.addRow (self.ik_label)
        self.ik_layout.addRow (self.ik_start_line , self.ik_start_button)
        self.ik_layout.addRow (self.ik_end_line , self.ik_end_button)
        self.ik_ho_layout = QHBoxLayout ()
        self.ik_ho_layout.addWidget (self.create_ik_button)
        self.ik_ho_layout.addWidget (self.delete_ik_button)
        self.ik_layout.addRow (self.ik_ho_layout)

        # 创建约束的layout
        self.constraint_layout = QFormLayout ()
        self.constraint_layout.addRow (self.constraint_label)

        self.constraint_ho_layout = QHBoxLayout ()
        self.constraint_ho_layout.addWidget (self.create_constraint_button)
        self.constraint_ho_layout.addWidget (self.delete_constraint_button)
        self.constraint_layout.addRow (self.constraint_ho_layout)

        # 创建小工具的layout
        self.tool_layout = QGridLayout ()
        self.create_tool_layouts ()

        # 创建main_layout的布局
        self.main_layout = QVBoxLayout (self)
        self.main_layout.addLayout (self.fk_layout)
        self.main_layout.addStretch ()
        self.main_layout.addLayout (self.ik_layout)
        self.main_layout.addStretch ()
        self.main_layout.addLayout (self.constraint_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.tool_label)
        self.main_layout.addLayout (self.tool_layout)


    def create_tool_layouts (self) :
        # 添加按钮
        positions = [(i , j) for i in range (5) for j in range (3)]

        for position , button in zip (positions , self.tool_buttons) :
            self.tool_layout.addWidget (button , *position)


    def add_connnect (self) :
        """
        链接信号与槽
        """
        # fk系统的部件连接
        self.create_fk_button.clicked.connect (lambda *args : print (1))
        self.create_fk_button.clicked.connect (lambda *args : print (1))

        # ik系统的部件连接
        self.ik_start_button.clicked.connect (lambda *args : print (1))
        self.ik_end_button.clicked.connect (lambda *args : print (1))
        self.create_ik_button.clicked.connect (lambda *args : print (1))
        self.delete_ik_button.clicked.connect (lambda *args : print (1))

        # 约束系统的部件连接
        self.create_constraint_button.clicked.connect (lambda : pipelineUtils.Pipeline.create_constraints ())
        self.delete_constraint_button.clicked.connect (lambda *args : pipelineUtils.Pipeline.delete_constraints ())

        # 绑定小工具的部件连接
        self.add_tool_connect ()


    def add_tool_connect (self) :
        """
        连接绑定小工具的连接
        """
        self.clear_keys_button.clicked.connect (lambda *args : pipelineUtils.Pipeline.clear_keys ())

        self.reset_control_button.clicked.connect (lambda *args : pipelineUtils.Pipeline.reset_control ())

        self.batch_Constraints_modle_button.clicked.connect (
            lambda *args : pipelineUtils.Pipeline.batch_Constraints_modle ())

        self.batch_Constraints_joint_button.clicked.connect (
            lambda *args : pipelineUtils.Pipeline.batch_Constraints_joint ())

        self.default_grp_button.clicked.connect (lambda *args : pipelineUtils.Pipeline.default_grp ())

        self.create_joints_on_curve_button.clicked.connect (lambda *args : jointUtils.Joint.create_joints_on_curve ())

        self.create_joints_on_curve_rigging_button.clicked.connect (
            lambda *args : jointUtils.Joint.create_joints_on_curve_rigging ())

        self.control_hierarchy_button.clicked.connect (lambda *args : hierarchyUtils.Hierarchy.control_hierarchy ())

        self.save_skinWeights_button.clicked.connect (self.save_skinWeights)

        self.load_skinWeights_button.clicked.connect (self.load_skinWeights)

        self.select_sub_objects_button.clicked.connect (lambda *args : pipelineUtils.Pipeline.select_sub_objects ())

        self.print_duplicate_object_button.clicked.connect (lambda *args : nameUtils.Name.print_duplicate_object ()
                                                            )

        self.rename_duplicate_object_button.clicked.connect (lambda *args : nameUtils.Name.rename_duplicate_object ())

        self.create_dynamic_curve_driven_button.clicked.connect (
            lambda *args : pipelineUtils.Pipeline.create_dynamic_curve_driven ())


    def save_skinWeights (self) :
        """
        保存权重
        """
        geos = cmds.ls (sl = True)
        for geo in geos :
            obj = weightsUtils.Weights (geo)
            obj.save_skinWeights ()


    def load_skinWeights (self) :
        """
        载入权重
        """
        geos = cmds.ls (sl = True)
        for geo in geos :
            obj = weightsUtils.Weights (geo)
            obj.load_skinWeights ()


def main () :
    return Rig_Tool ()


if __name__ == "__main__" :
    app = QApplication (sys.argv)
    mainwindow = Rig_Tool ()
    mainwindow.show ()
    sys.exit (app.exec_ ())
