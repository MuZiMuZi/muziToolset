# coding=utf-8
"""

"""
from __future__ import unicode_literals,print_function
import sys


from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import *

from maya.OpenMayaUI import  MQtUtil
from shiboken2 import wrapInstance
import maya.cmds as cmds

import muziToolset.conf.config as config


import muziToolset.res.ui.rename_modular.rename_widget as rename_widget
import muziToolset.res.ui.setting_modular.setting_widget as setting_widget
import muziToolset.res.ui.snap_modular.snap_widget as snap_widget
import muziToolset.res.ui.control_modular.control_widget as control_widget
import muziToolset.res.ui.nodes_modular.nodes_widget as nodes_widget
import muziToolset.conf.setting as setting
import muziToolset.core.pipelineUtils as pipelineUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.rigging.weightsUtils as weightsUtils

reload(weightsUtils)
reload(rename_widget)
reload(nodes_widget)
reload(setting_widget)
reload(snap_widget)
reload(control_widget)
reload(pipelineUtils)
reload(jointUtils)
reload(hierarchyUtils)



class toolWidget(QWidget):
    def __init__(self):
        super(toolWidget, self).__init__()
        self.init_ui()

    def init_ui(self):
        # 创建常用工具页面布局
        self.main_layout = QGridLayout(self)

        # 取消面板设置中的黑边
        self.resize(500, 500)
        self.main_layout.addWidget(QLabel(u"工具:    "))

        # 创建模块按钮
        self.control_widget_bn = QPushButton("控制器工具")
        self.control_widget_bn.clicked.connect(self.control_widget)
        self.snap_widget_bn = QPushButton("吸附工具")
        self.snap_widget_bn.clicked.connect(self.snap_widget)
        self.rename_widget_bn = QPushButton("命名工具")
        self.rename_widget_bn.clicked.connect(self.rename_widget)
        self.nodes_widget_bn = QPushButton("节点创建工具")
        self.nodes_widget_bn.clicked.connect(self.nodes_widget)
        self.setting_widget_bn = QPushButton("全局设置工具")
        self.setting_widget_bn.clicked.connect(self.setting_widget)

        # 应用设置
        self.setting()

        # 添加按钮
        self.main_layout.addWidget(self.control_widget_bn,1,1)
        self.main_layout.addWidget(self.snap_widget_bn,1,2)
        self.main_layout.addWidget(self.rename_widget_bn,1,3)
        self.main_layout.addWidget(self.nodes_widget_bn,2,1)
        self.main_layout.addWidget(self.setting_widget_bn,2,2)

    def control_widget(self):
        control_widget.show()

    def snap_widget(self):
        snap_widget.show()

    def rename_widget(self):
        rename_widget.show()

    def nodes_widget(self):
        nodes_widget.show()

    def setting_widget(self):
        setting_widget.show()

    def setting(self):
        """
        根据设置的值来设置字体大小
        Returns:

        """
        font_size = setting.get("font", None)
        if font_size is None:
            font_size = QFont().toString()
        font = QFont()
        font.fromString(font_size)
        self.setFont(font)


class functionWidget(QWidget,pipelineUtils.Pipeline):
    def __init__(self):
        super(functionWidget, self).__init__()
        super(pipelineUtils.Pipeline, self).__init__()
        self.init_ui()

    def init_ui(self):
        # 创建常用节点页面布局
        self.main_layout = QGridLayout(self)

        # 取消面板设置中的黑边
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(QLabel(u"功能:    "))

        # 创建模块按钮
        self.clear_keys_bn = QPushButton("删除关键帧")
        self.clear_keys_bn.clicked.connect(self.clear_keys)

        self.reset_control_bn = QPushButton("重置控制器")
        self.reset_control_bn.clicked.connect(self.reset_control)

        self.batch_Constraints_bn = QPushButton("批量约束")
        self.batch_Constraints_bn.clicked.connect(self.batch_Constraints)

        self.default_grp_bn = QPushButton("绑定层级组")
        self.default_grp_bn.clicked.connect(self.default_grp)

        self.create_joints_on_curve_bn = QPushButton("曲线上点创建关节(通用)")
        self.create_joints_on_curve_bn.clicked.connect(self.create_joints_on_curve)

        self.create_joints_on_curve_rigging_bn = QPushButton("曲线上点创建关节(自用)")
        self.create_joints_on_curve_rigging_bn.clicked.connect(self.create_joints_on_curve_rigging)

        self.control_hierarchy_bn = QPushButton("自动打组(自用)")
        self.control_hierarchy_bn.clicked.connect(self.control_hierarchy)

        self.save_SkinWeights_bn = QPushButton("导出权重")
        self.save_SkinWeights_bn.clicked.connect(self.save_SkinWeights)

        self.load_SkinWeights_bn = QPushButton("导入权重")
        self.load_SkinWeights_bn.clicked.connect(self.load_SkinWeights)

        # 添加按钮
        self.main_layout.addWidget(self.clear_keys_bn,1,1)
        self.main_layout.addWidget(self.reset_control_bn,1,2)
        self.main_layout.addWidget(self.batch_Constraints_bn,1,3)
        self.main_layout.addWidget(self.default_grp_bn,1,4)
        self.main_layout.addWidget(self.create_joints_on_curve_bn,2,1)
        self.main_layout.addWidget(self.create_joints_on_curve_rigging_bn, 2, 2)
        self.main_layout.addWidget(self.control_hierarchy_bn,2,3)
        self.main_layout.addWidget(self.save_SkinWeights_bn, 2, 4)
        self.main_layout.addWidget(self.load_SkinWeights_bn, 3, 1)

    def clear_keys(self):
        pipelineUtils.Pipeline.clear_keys()

    def reset_control(self):
        pipelineUtils.Pipeline.reset_control()

    def batch_Constraints(self):
        pipelineUtils.Pipeline.batch_Constraints()

    def default_grp(self):
        pipelineUtils.Pipeline.default_grp()

    def create_joints_on_curve(self):
        jointUtils.Joint.create_joints_on_curve()

    def create_joints_on_curve_rigging(self):
        jointUtils.Joint.create_joints_on_curve_rigging()

    def control_hierarchy(self):
        hierarchyUtils.Hierarchy.control_hierarchy()

    def save_SkinWeights(self):
        geos = cmds.ls(sl =True)
        for geo in geos:
            obj = weightsUtils.Weights(geo)
            obj.save_SkinWeights()

    def load_SkinWeights(self):
        geos = cmds.ls(sl = True)
        for geo in geos:
            obj = weightsUtils.Weights(geo)
            obj.load_SkinWeights()


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()


    def init_ui(self):
        # 检查maya使用的python解释器版本,设置小部件的父对象
        if sys.version_info.major  >= 3:
            self.setParent(wrapInstance(int(MQtUtil.mainWindow()), QWidget))
        else:
            self.setParent(wrapInstance(long(MQtUtil.mainWindow()),QWidget))
        self.setWindowFlags(Qt.Window)

        self.setWindowTitle('木子工具集 {}'.format(config.VERSION))
        self.main_layout = QVBoxLayout(self)


        # 取消面板设置中的黑边
        self.main_layout.setContentsMargins(0,0,0,0)
        self.resize(700, 700)

        self.tool_layout = toolWidget()
        self.function_layout = functionWidget()

        self.main_layout.addWidget(self.tool_layout)
        self.main_layout.addStretch(0)
        self.main_layout.addWidget(self.function_layout)

def show():
    global win
    try:
        win.close()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
    except:
        pass
    win = MainWindow()
    win.show()
