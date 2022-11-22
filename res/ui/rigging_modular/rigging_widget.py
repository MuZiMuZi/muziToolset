# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals, print_function
import os

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtWidgets import *
    from PySide import __version__
    from shiboken import wrapInstance

import maya.cmds as cmds
from PySide2.QtUiTools import QUiLoader
from maya.OpenMayaUI import MQtUtil
import sys

import muziToolset.conf.config as config
import muziToolset.rigging.build_rig as build_rig
import muziToolset.res.ui.backGround as backGround
import muziToolset.core.pipelineUtils as pipelineUtils
import muziToolset.rigging.weightsUtils as weightsUtils


class RiggingWindow(QWidget):
    def __init__(self):
        super(RiggingWindow, self).__init__()
        self.ui = None
        self.init_ui()
        self.custom_ctrl = 'ctrl_m_custom_001'
    def init_ui(self):
        # 检查maya使用的python解释器版本,设置小部件的父对象
        if sys.version_info.major >= 3:
            self.setParent(wrapInstance(int(MQtUtil.mainWindow()), QWidget))
        else:
            self.setParent(wrapInstance(long(MQtUtil.mainWindow()), QWidget))

        self.setWindowTitle('木子绑定系统 {}'.format(config.VERSION))
        self.setWindowFlags(Qt.Window)

        # 读取qt Designer 写的ui文件
        loader = QUiLoader()
        # currentDir = os.path.dirname(__file__)#如果是import到maya中就可以的使用方法获得路径
        currentDir = os.path.abspath(__file__ + "/../../../ui/rigging_modular")
        file = QFile(currentDir + "/rigging.ui")  # 这个方法要使用绝对路径
        self.ui = loader.load(file, parentWidget = self)  # 初始化

        # 连接ui文件的部件
        # 连接模版的listview
        self.Template_listView = self.ui.Template_listView

        # 连接模块的listview
        self.modular_listView = self.ui.modular_listView
        # 连接导入按钮

        self.import_button = self.ui.import_button
        self.import_button.clicked.connect(self.import_modular)

        # 连接关节方向的设置
        self.jointDirection_label = self.ui.jointDirection_label
        self.jointDirection_false_radioButton = self.ui.jointDirection_false_radioButton
        self.jointDirection_true_radioButton = self.ui.jointDirection_true_radioButton
        self.jointDirection_false_radioButton.setChecked(True)

        # 连接关节方向显示的设置的按钮组
        self.jointDirection_radioButton_group = QButtonGroup(self)
        self.jointDirection_radioButton_group.addButton(self.jointDirection_false_radioButton, 0)
        self.jointDirection_radioButton_group.addButton(self.jointDirection_true_radioButton, 1)
        self.jointDirection_radioButton_group.buttonClicked.connect(self.set_jointDirection)

        # 连接关节大小的设置
        self.jointSize_label = self.ui.jointSize_label
        self.jointSize_slider = self.ui.jointSize_slider
        self.jointSize_slider.setMinimum(0)  # 设置最小值
        self.jointSize_slider.setMaximum(50)  # 设置最大值
        self.jointSize_slider.valueChanged.connect(self.set_jointSize)

        # 连接清除的设置
        self.clear_button = self.ui.clear_button
        self.clear_button.clicked.connect(self.claer_modular)

        # 连接属性的lsitview
        self.property_listWidget = self.ui.property_listWidget

        # 连接关节显示的设置
        self.jointsVis_label = self.ui.jointsVis_label
        self.jointsVis_false_radioButton = self.ui.jointsVis_false_radioButton
        self.jointsVis_true_radioButton = self.ui.jointsVis_true_radioButton
        self.jointsVis_true_radioButton.setChecked(True)

        # 连接控制器显示的设置的按钮组
        self.jointsVis_radioButton_group = QButtonGroup(self)
        self.jointsVis_radioButton_group.addButton(self.jointsVis_false_radioButton, 0)
        self.jointsVis_radioButton_group.addButton(self.jointsVis_true_radioButton, 1)
        self.jointsVis_radioButton_group.buttonClicked.connect(self.set_jointsVis)

        # 连接模型显示的设置
        self.geometryVis_label = self.ui.geometryVis_label
        self.geometryVis_false_radioButton = self.ui.geometryVis_false_radioButton
        self.geometryVis_true_radioButton = self.ui.geometryVis_true_radioButton
        self.geometryVis_true_radioButton.setChecked(True)

        # 连接模型显示的设置的按钮组
        self.geometryVis_radioButton_group = QButtonGroup(self)
        self.geometryVis_radioButton_group.addButton(self.geometryVis_false_radioButton, 0)
        self.geometryVis_radioButton_group.addButton(self.geometryVis_true_radioButton, 1)
        self.geometryVis_radioButton_group.buttonClicked.connect(self.set_geometryVis)

        # 连接控制器显示的设置
        self.controlsVis_label = self.ui.controlsVis_label
        self.controlsVis_false_radioButton = self.ui.controlsVis_false_radioButton
        self.controlsVis_true_radioButton = self.ui.controlsVis_true_radioButton
        self.controlsVis_true_radioButton.setChecked(True)

        # 连接控制器显示的设置的按钮组
        self.controlsVis_radioButton_group = QButtonGroup(self)
        self.controlsVis_radioButton_group.addButton(self.controlsVis_false_radioButton, 0)
        self.controlsVis_radioButton_group.addButton(self.controlsVis_true_radioButton, 1)
        self.controlsVis_radioButton_group.buttonClicked.connect(self.set_controlsVis)

        # 连接控制器重置的设置
        self.reset_button = self.ui.reset_button
        self.reset_button.clicked.connect(self.reset_control)

        # 连接导出权重的设置
        self.save_skinWeights_button = self.ui.save_skinWeights_button
        self.save_skinWeights_button.clicked.connect(self.save_skinWeights)
        # 连接导入权重的设置
        self.load_skinWeights_button = self.ui.load_skinWeights_button
        self.load_skinWeights_button.clicked.connect(self.load_skinWeights)

        # 连接生成绑定的设置
        self.build_button = self.ui.build_button
        self.build_button.clicked.connect(self.build_rig)



    def set_jointDirection(self, item):
        joints = cmds.ls(type = 'joint')
        for joint in joints:
            cmds.setAttr(joint + '.displayLocalAxis', item.group().checkedId())

    def set_jointSize(self):
        joints = cmds.ls(type = 'joint')
        for joint in joints:
            cmds.setAttr(joint + '.radius', self.jointSize_slider.value())
    def set_jointsVis(self, item):
        if cmds.objExists(self.custom_ctrl):
            cmds.setAttr(self.custom_ctrl + '.jointsVis',item.group().checkedId())


    def set_geometryVis(self, item):
        if cmds.objExists(self.custom_ctrl):
            cmds.setAttr(self.custom_ctrl + '.geometryVis',item.group().checkedId())

    def set_controlsVis(self, item):
        if cmds.objExists(self.custom_ctrl):
            cmds.setAttr(self.custom_ctrl + '.controlsVis',item.group().checkedId())
    def import_modular(self):
        build = build_rig.Build_Rig()
        build.import_modular()

    def claer_modular(self):
        build = build_rig.Build_Rig()
        build.claer_modular()

    def reset_control(self):
        pipelineUtils.Pipeline.reset_control()

    def save_skinWeights(self):
        geos = cmds.ls(sl = True)
        for geo in geos:
            obj = weightsUtils.Weights(geo)
            obj.save_skinWeights()

    def load_skinWeights(self):
        geos = cmds.ls(sl = True)
        for geo in geos:
            obj = weightsUtils.Weights(geo)
            obj.load_skinWeights()

    def build_rig(self):
        build = build_rig.Build_Rig()
        build.build_rig()


#
def show():
    global win
    try:
        win.close()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
    except:
        pass
    win = RiggingWindow()
    win.show()
