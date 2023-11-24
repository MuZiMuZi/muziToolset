from __future__ import print_function , unicode_literals

import sys
from importlib import reload

import maya.cmds as cmds
import muziToolset.conf.config as config
import muziToolset.conf.setting as setting
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.matehumanUtils as matehumanUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.pipelineUtils as pipelineUtils
import muziToolset.core.weightsUtils as weightsUtils
import muziToolset.res.ui.control_modular.control_widget as control_widget
import muziToolset.res.ui.nodes_modular.nodes_widget as nodes_widget
import muziToolset.res.ui.rename_modular.rename_widget as rename_widget
import muziToolset.res.ui.setting_modular.setting_widget as setting_widget
import muziToolset.res.ui.snap_modular.snap_widget as snap_widget
import muziToolset.tools.Names_Tool_main as Names_Tool_main
from importlib import reload
import muziToolset.tools.Names_Tool_main as Names_Tool_main
from importlib import reload


reload (Names_Tool_main)

from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import *
from maya.OpenMayaUI import MQtUtil
from shiboken2 import wrapInstance


reload (pipelineUtils)


class toolWidget (QWidget) :

    def __init__ (self) :
        super (toolWidget , self).__init__ ()
        self.init_ui ()


    def init_ui (self) :
        # 创建常用工具页面布局
        self.main_layout = QGridLayout (self)

        # 取消面板设置中的黑边
        self.resize (500 , 500)
        self.main_layout.addWidget (QLabel (u"工具:    "))

        # 创建模块按钮
        self.control_widget_button = QPushButton ("控制器工具")
        self.control_widget_button.clicked.connect (self.control_widget)
        self.snap_widget_button = QPushButton ("吸附工具")
        self.snap_widget_button.clicked.connect (self.snap_widget)
        self.rename_widget_button = QPushButton ("命名工具")
        self.rename_widget_button.clicked.connect (self.rename_widget)
        self.nodes_widget_button = QPushButton ("节点创建工具")
        self.nodes_widget_button.clicked.connect (self.nodes_widget)
        self.setting_widget_button = QPushButton ("全局设置工具")
        self.setting_widget_button.clicked.connect (self.setting_widget)

        # 应用设置
        self.setting ()

        # 添加按钮
        self.main_layout.addWidget (self.control_widget_button , 1 , 1)
        self.main_layout.addWidget (self.snap_widget_button , 1 , 2)
        self.main_layout.addWidget (self.rename_widget_button , 1 , 3)
        self.main_layout.addWidget (self.nodes_widget_button , 2 , 1)
        self.main_layout.addWidget (self.setting_widget_button , 2 , 2)


    def control_widget (self) :
        control_widget.show ()


    def snap_widget (self) :
        snap_widget.show ()


    def rename_widget (self) :
        # name_tool = Names_Tool_main.Names_Tool_main (self)

        Names_Tool_main.show ()


    def nodes_widget (self) :
        nodes_widget.show ()


    def setting_widget (self) :
        setting_widget.show ()


    def setting (self) :
        """
        根据设置的值来设置字体大小
        Returns:

        """
        font_size = setting.get ("font" , None)
        if font_size is None :
            font_size = QFont ().toString ()
        font = QFont ()
        font.fromString (font_size)
        self.setFont (font)


class functionWidget (QWidget , pipelineUtils.Pipeline) :

    def __init__ (self) :
        super (functionWidget , self).__init__ ()
        super (pipelineUtils.Pipeline , self).__init__ ()
        self.init_ui ()


    def init_ui (self) :
        # 创建常用节点页面布局
        self.main_layout = QGridLayout (self)

        # 取消面板设置中的黑边
        self.main_layout.setContentsMargins (0 , 0 , 0 , 0)
        self.main_layout.addWidget (QLabel (u"功能:    "))

        # 创建模块按钮
        self.clear_keys_button = QPushButton ("删除关键帧")
        self.clear_keys_button.clicked.connect (self.clear_keys)

        self.reset_control_button = QPushButton ("重置控制器")
        self.reset_control_button.clicked.connect (self.reset_control)

        self.batch_Constraints_modle_button = QPushButton ("批量约束_物体")
        self.batch_Constraints_modle_button.clicked.connect (self.batch_Constraints_modle)

        self.batch_Constraints_joint_button = QPushButton ("批量约束_关节")
        self.batch_Constraints_joint_button.clicked.connect (self.batch_Constraints_joint)

        self.default_grp_button = QPushButton (u"绑定层级组")
        self.default_grp_button.clicked.connect (self.default_grp)

        self.create_joints_on_curve_button = QPushButton (u"曲线上点创建关节(通用)")
        self.create_joints_on_curve_button.clicked.connect (self.create_joints_on_curve)

        self.create_joints_on_curve_rigging_button = QPushButton (u"曲线上点创建关节(自用)")
        self.create_joints_on_curve_rigging_button.clicked.connect (self.create_joints_on_curve_rigging)

        self.control_hierarchy_button = QPushButton (u"自动打组(自用)")
        self.control_hierarchy_button.clicked.connect (self.control_hierarchy)

        self.save_skinWeights_button = QPushButton (u"导出权重")
        self.save_skinWeights_button.clicked.connect (self.save_skinWeights)

        self.load_skinWeights_button = QPushButton (u"导入权重")
        self.load_skinWeights_button.clicked.connect (self.load_skinWeights)

        self.create_constraints_button = QPushButton (u"快速约束")
        self.create_constraints_button.clicked.connect (self.create_constraints)

        self.delete_constraints_button = QPushButton ("删除约束")
        self.delete_constraints_button.clicked.connect (self.delete_constraints)

        self.select_sub_objects_button = QPushButton ("快速选择子物体")
        self.select_sub_objects_button.clicked.connect (self.select_sub_objects)

        self.print_duplicate_object_button = QPushButton ("检查并列出重名节点")
        self.print_duplicate_object_button.clicked.connect (self.print_duplicate_object)

        self.rename_duplicate_object_button = QPushButton ("检查并重命名重名节点")
        self.rename_duplicate_object_button.clicked.connect (self.rename_duplicate_object)

        self.create_dynamic_curve_driven_button = QPushButton ("创建动力学化曲线驱动头发")
        self.create_dynamic_curve_driven_button.clicked.connect (self.create_dynamic_curve_driven)

        # 添加按钮
        self.main_layout.addWidget (self.clear_keys_button , 1 , 1)
        self.main_layout.addWidget (self.reset_control_button , 1 , 2)
        self.main_layout.addWidget (self.batch_Constraints_modle_button , 1 , 3)

        self.main_layout.addWidget (self.batch_Constraints_joint_button , 1 , 4)

        self.main_layout.addWidget (self.create_joints_on_curve_button , 2 , 1)
        self.main_layout.addWidget (self.create_joints_on_curve_rigging_button , 2 , 2)
        self.main_layout.addWidget (self.control_hierarchy_button , 2 , 3)
        self.main_layout.addWidget (self.save_skinWeights_button , 2 , 4)

        self.main_layout.addWidget (self.load_skinWeights_button , 3 , 1)
        self.main_layout.addWidget (self.create_constraints_button , 3 , 2)
        self.main_layout.addWidget (self.delete_constraints_button , 3 , 3)
        self.main_layout.addWidget (self.select_sub_objects_button , 3 , 4)

        self.main_layout.addWidget (self.print_duplicate_object_button , 4 , 1)
        self.main_layout.addWidget (self.rename_duplicate_object_button , 4 , 2)
        self.main_layout.addWidget (self.default_grp_button , 4 , 3)
        self.main_layout.addWidget (self.create_dynamic_curve_driven_button , 4 , 4)


    def clear_keys (self) :
        pipelineUtils.Pipeline.clear_keys ()


    def reset_control (self) :
        pipelineUtils.Pipeline.reset_control ()


    def batch_Constraints_modle (self) :
        pipelineUtils.Pipeline.batch_Constraints_modle ()


    def batch_Constraints_joint (self) :
        pipelineUtils.Pipeline.batch_Constraints_joint ()


    def default_grp (self) :
        pipelineUtils.Pipeline.default_grp ()


    def create_joints_on_curve (self) :
        jointUtils.Joint.create_joints_on_curve ()


    def create_joints_on_curve_rigging (self) :
        jointUtils.Joint.create_joints_on_curve_rigging ()


    def control_hierarchy (self) :
        hierarchyUtils.Hierarchy.control_hierarchy ()


    def save_skinWeights (self) :
        geos = cmds.ls (sl = True)
        for geo in geos :
            obj = weightsUtils.Weights (geo)
            obj.save_skinWeights ()


    def load_skinWeights (self) :
        geos = cmds.ls (sl = True)
        for geo in geos :
            obj = weightsUtils.Weights (geo)
            obj.load_skinWeights ()


    def create_constraints (self) :
        pipelineUtils.Pipeline.create_constraints ()


    def delete_constraints (self) :
        pipelineUtils.Pipeline.delete_constraints ()


    def select_sub_objects (self) :
        hierarchyUtils.Hierarchy.select_sub_objects ()


    def print_duplicate_object (self) :
        nameUtils.Name.print_duplicate_object ()


    def rename_duplicate_object (self) :
        nameUtils.Name.rename_duplicate_object ()


    def create_dynamic_curve_driven (self) :
        """
        选择曲线。创建动力学化曲线驱动头发
        """
        pipelineUtils.Pipeline.create_dynamic_curve_driven ()


class matehuman_Widget (QWidget) :

    def __init__ (self) :
        super (matehuman_Widget , self).__init__ ()
        self.init_ui ()


    def init_ui (self) :
        # 创建常用节点页面布局
        self.main_layout = QGridLayout (self)

        # 取消面板设置中的黑边
        self.main_layout.setContentsMargins (0 , 0 , 0 , 0)
        self.main_layout.addWidget (QLabel (u"matehuman 工具:    "))

        # 创建模块按钮
        self.mate_rig_button = QPushButton (u"创建身体绑定")
        self.mate_rig_button.clicked.connect (self.create_matehuman_rig)

        self.mate_ctrl_button = QPushButton (u"重置控制器")
        self.mate_ctrl_button.clicked.connect (self._reset_mateHuman_control)

        self.mate_face_button = QPushButton (u"导出面部动画")
        self.mate_face_button.clicked.connect (self._export_face_animation)

        self.mate_body_button = QPushButton (u"导出身体动画")
        self.mate_body_button.clicked.connect (self._export_body_animation)

        self.mate_piker_button = QPushButton (u"控制器piker(开发中)")
        # self.mate_piker_button.clicked.connect(self.clear_keys)

        # 添加按钮到布局里
        self.main_layout.addWidget (self.mate_rig_button , 1 , 1)
        self.main_layout.addWidget (self.mate_ctrl_button , 1 , 2)
        self.main_layout.addWidget (self.mate_face_button , 1 , 3)
        self.main_layout.addWidget (self.mate_body_button , 1 , 4)
        self.main_layout.addWidget (self.mate_piker_button , 2 , 1)


    def create_matehuman_rig (self) :
        u'''
        创建matehuman的身体绑定系统
        :return:
        '''
        if cmds.objExists ('rig_group') :
            cmds.warning (u'已经生成身体绑定')
            pass
        else :
            matehuman = matehuman_rig.MateHuman_Rig ()
            matehuman.create_rig ()


    def _export_face_animation (self) :
        u'''
                导出matehuman的身体动画
                :return:
                '''
        matehumanUtils.MateHuman.export_face_animation ()


    def _export_body_animation (self) :
        u'''
        导出matehuman的身体动画
        :return:
        '''
        matehumanUtils.MateHuman.export_body_animation ()


    def _reset_mateHuman_control (self) :
        u'''
        重置matehuman的控制器
        :return:
        '''
        matehumanUtils.MateHuman.reset_mateHuman_control ()


class MainWindow (QWidget) :

    def __init__ (self) :
        super (MainWindow , self).__init__ ()
        self.init_ui ()


    def init_ui (self) :
        # 检查maya使用的python解释器版本,设置小部件的父对象
        if sys.version_info.major >= 3 :
            self.setParent (wrapInstance (int (MQtUtil.mainWindow ()) , QWidget))
        else :
            self.setParent (wrapInstance (long (MQtUtil.mainWindow ()) , QWidget))
        self.setWindowFlags (Qt.Window)

        self.setWindowTitle ('木子工具集 {}'.format (config.VERSION))
        self.main_layout = QVBoxLayout (self)

        # 取消面板设置中的黑边
        self.main_layout.setContentsMargins (0 , 0 , 0 , 0)
        self.resize (700 , 700)

        self.tool_layout = toolWidget ()
        self.function_layout = functionWidget ()
        self.matehuman_layout = matehuman_Widget ()

        self.main_layout.addWidget (self.tool_layout)
        self.main_layout.addStretch (0)
        self.main_layout.addWidget (self.function_layout)
        self.main_layout.addStretch (0)
        self.main_layout.addWidget (self.matehuman_layout)


def show () :
    global win
    try :
        win.close ()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
    except :
        pass
    win = MainWindow ()
    win.show ()
