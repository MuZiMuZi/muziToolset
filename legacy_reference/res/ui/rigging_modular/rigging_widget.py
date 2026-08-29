# coding=utf-8
# 导入所有需要的模块

u"""这是一个写绑定系统的类
目前已经实现的功能：
set_jointDirection：设置关节的方向是否显示
set_jointSize：设置关节的显示大小
set_jointsVis：设置关节组是否显示
set_geometryVis:设置模型组是否显示
set_controlsVis：设置控制器组是否显示
import_modular：导入绑定模块
claer_modular：清除绑定模块
reset_control：重置控制器
save_skinWeights：导出权重
load_skinWeights：导入权重
build_rig：创建绑定
"""

from __future__ import unicode_literals , print_function
import os



try :
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	from PySide2 import __version__ , QtCore , QtWidgets , QtGui
	from shiboken2 import wrapInstance

except ImportError :
	from PySide.QtCore import *
	from PySide.QtGui import *
	from PySide.QtWidgets import *
	from PySide import __version__ , __all__
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



class RiggingWindow(QWidget) :
	
	
	
	def __init__(self) :
		super(RiggingWindow , self).__init__()
		self.ui = None
		self.init_ui()
		self.custom_ctrl = 'ctrl_m_custom_001'
	
	
	
	def init_ui(self) :
		# 检查maya使用的python解释器版本,设置小部件的父对象
		if sys.version_info.major >= 3 :
			self.setParent(wrapInstance(int(MQtUtil.mainWindow()) , QWidget))
		else :
			self.setParent(wrapInstance(long(MQtUtil.mainWindow()) , QWidget))
		
		self.setWindowTitle('木子绑定系统 {}'.format(config.VERSION))
		self.setWindowFlags(Qt.Window)
		
		# 读取qt Designer 写的ui文件
		loader = QUiLoader()
		# currentDir = os.path.dirname(__file__)#如果是import到maya中就可以的使用方法获得路径
		currentDir = os.path.abspath(__file__ + "/../../../ui/rigging_modular")
		file = QFile(currentDir + "/rigging.ui")  # 这个方法要使用绝对路径
		self.ui = loader.load(file , parentWidget = self)  # 初始化
		
		# 连接ui文件的部件
		# 连接模版的listview
		self.template_listWidget = self.ui.template_listWidget
		
		# 模版的listWidget 添加模版
		self.modular_rig_list = ['neck_rig' , 'spine_rig' , 'chest_rig' , 'arm_rig' , 'hand_rig' , 'leg_rig' ,
		                         'foot_rig']
		for modular in self.modular_rig_list :
			self.template_listWidget.addItem('{}'.format(modular))
		
		# 设置模版的listWidget的无法拖拽模式
		self.template_listWidget.setMovement(self.template_listWidget.Static)
		#
		# #设置模版的listWidget的选择模式
		self.template_listWidget.setSelectionMode(self.template_listWidget.ExtendedSelection)
		self.template_listWidget.setResizeMode(self.template_listWidget.Adjust)
		
		# 设置模版的listWidget的右键页面布局
		self.template_listWidget_menu = QtWidgets.QMenu(self.template_listWidget)
		self.template_listWidget_menu.addAction(u'添加' , self.import_template_modular)
		
		# 连接模块的listWidget
		self.modular_listWidget = self.ui.modular_listWidget
		
		# 设置模块的listWidget的无法拖拽模式
		self.modular_listWidget.setMovement(self.modular_listWidget.Static)
		#
		# #设置模块的listWidget的选择模式
		self.modular_listWidget.setSelectionMode(self.modular_listWidget.ExtendedSelection)
		self.modular_listWidget.setResizeMode(self.modular_listWidget.Adjust)
		
		# 设置模块的listWidget的右键页面布局
		self.modular_listWidget_menu = QtWidgets.QMenu(self.modular_listWidget)
		self.modular_listWidget_menu.addAction(u'删除' , self.remove_template_modular)
		
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
		self.jointDirection_radioButton_group.addButton(self.jointDirection_false_radioButton , 0)
		self.jointDirection_radioButton_group.addButton(self.jointDirection_true_radioButton , 1)
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
		
		# 连接属性的StackedWidget(抽屉布局)
		self.property_StackedWidget = self.ui.property_StackedWidget
		
		# 属性的StackedWidget的页面顺序
		# [default,neck_rig,spine_rig,chest_rig,arm_rig,hand_rig,leg_rig,foot_rig]
		self.property_StackedWidget.setCurrentIndex(0)
		
		self.default_property_widget = self.ui.default_property_widget
		self.neck_rig_property_widget = self.ui.neck_rig_property_widget
		self.spine_rig_property_widget = self.ui.spine_rig_property_widget
		self.chest_rig_property_widget = self.ui.chest_rig_property_widget
		self.hand_rig_property_widget = self.ui.hand_rig_property_widget
		self.leg_rig_property_widget = self.ui.leg_rig_property_widget
		self.foot_rig_property_widget = self.ui.foot_rig_property_widget
		self.modular_listWidget.itemSelectionChanged.connect(self.set_property_StackedWidget)
		
		# 连接关节显示的设置
		self.jointsVis_label = self.ui.jointsVis_label
		self.jointsVis_false_radioButton = self.ui.jointsVis_false_radioButton
		self.jointsVis_true_radioButton = self.ui.jointsVis_true_radioButton
		self.jointsVis_true_radioButton.setChecked(True)
		
		# 连接控制器显示的设置的按钮组
		self.jointsVis_radioButton_group = QButtonGroup(self)
		self.jointsVis_radioButton_group.addButton(self.jointsVis_false_radioButton , 0)
		self.jointsVis_radioButton_group.addButton(self.jointsVis_true_radioButton , 1)
		self.jointsVis_radioButton_group.buttonClicked.connect(self.set_jointsVis)
		
		# 连接模型显示的设置
		self.geometryVis_label = self.ui.geometryVis_label
		self.geometryVis_false_radioButton = self.ui.geometryVis_false_radioButton
		self.geometryVis_true_radioButton = self.ui.geometryVis_true_radioButton
		self.geometryVis_true_radioButton.setChecked(True)
		
		# 连接模型显示的设置的按钮组
		self.geometryVis_radioButton_group = QButtonGroup(self)
		self.geometryVis_radioButton_group.addButton(self.geometryVis_false_radioButton , 0)
		self.geometryVis_radioButton_group.addButton(self.geometryVis_true_radioButton , 1)
		self.geometryVis_radioButton_group.buttonClicked.connect(self.set_geometryVis)
		
		# 连接控制器显示的设置
		self.controlsVis_label = self.ui.controlsVis_label
		self.controlsVis_false_radioButton = self.ui.controlsVis_false_radioButton
		self.controlsVis_true_radioButton = self.ui.controlsVis_true_radioButton
		self.controlsVis_true_radioButton.setChecked(True)
		
		# 连接控制器显示的设置的按钮组
		self.controlsVis_radioButton_group = QButtonGroup(self)
		self.controlsVis_radioButton_group.addButton(self.controlsVis_false_radioButton , 0)
		self.controlsVis_radioButton_group.addButton(self.controlsVis_true_radioButton , 1)
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
	
	
	
	def contextMenuEvent(self , event) :
		'''
		重写了template_listWidget和modular_listWidget的右键菜单事件
		'''
		# 必须要让右键点击后的menu菜单能够一直存在(直到用户再次点击)
		# 我们就必须要使用menu.exec_的方法让它一直存在
		# 但是只是用这个方法的话,出现的menu菜单不是在我们的主窗口上面\
		# 而是在我们的主窗口外面(而且是0, 0的位置),意思就是menu要运行,\
		# 但是它不知道我们主窗口运行在哪个位置,
		# 所以我们要用mapToGlobal(event.pos())这个函数,将主函数里面的\
		# 主窗口永真循环的exec_函数和这个联系起来,\
		# 这时我们获得的是事件触发(右键点击在哪里)时候的位置坐标\
		# event.pos,mapToGlobal返回的是一个位置坐标,
		# 同时让menu运行在这个位置,而不是默认的(0, 0)
		#
		# 获取鼠标指针的位置
		# pos = self.mapToGlobal(QCursor.pos())
		# # pos_y = QCursor.pos().y())
		# print (pos)
		
		
		QListWidget.contextMenuEvent(self.template_listWidget , event)
		# print (self.template_listWidget.rect())
		# if pos==self.template_listWidget.rect():
		self.template_listWidget_menu.exec_(self.mapToGlobal(event.pos()))
		
		QListWidget.contextMenuEvent(self.modular_listWidget , event)
		# if QCursor.pos() == self.modular_listWidget:
		# self.modular_listWidget_menu.exec_(self.mapToGlobal(event.pos()))
	
	
	
	def set_property_StackedWidget(self) :
		u"""
		根据模块界面选择的点击来切换不同的页面
		# 属性的StackedWidget的页面顺序
		# StackedWidget = ['default','neck_rig','spine_rig','chest_rig','arm_rig','hand_rig','leg_rig','foot_rig']

		"""
		StackedWidget = ['default' , 'neck_rig' , 'spine_rig' , 'chest_rig' , 'arm_rig' , 'hand_rig' , 'leg_rig' ,
		                 'foot_rig']
		for item in self.modular_listWidget.selectedItems() :
			index = StackedWidget.index(item.text())
			self.property_StackedWidget.setCurrentIndex(index)
		# else:
		#     self.property_StackedWidget.setCurrentIndex(0)
	
	
	
	def import_template_modular(self) :
		"""
		获取选择的模版项目添加到绑定模块里
		"""
		for item in self.template_listWidget.selectedItems() :
			self.modular_listWidget.addItem('{}'.format(item.text()))
	
	
	
	def remove_template_modular(self) :
		u"""
			   将所选的模块项目从绑定模块里移除
			   """
		for item in self.modular_listWidget.selectedItems() :
			self.modular_listWidget.removeItemWidget('{}'.format(item.text()))
	
	
	
	def set_jointDirection(self , item) :
		joints = cmds.ls(type = 'joint')
		for joint in joints :
			cmds.setAttr(joint + '.displayLocalAxis' , item.group().checkedId())
	
	
	
	def set_jointSize(self) :
		joints = cmds.ls(type = 'joint')
		for joint in joints :
			cmds.setAttr(joint + '.radius' , self.jointSize_slider.value())
	
	
	
	def set_jointsVis(self , item) :
		if cmds.objExists(self.custom_ctrl) :
			cmds.setAttr(self.custom_ctrl + '.jointsVis' , item.group().checkedId())
	
	
	
	def set_geometryVis(self , item) :
		if cmds.objExists(self.custom_ctrl) :
			cmds.setAttr(self.custom_ctrl + '.geometryVis' , item.group().checkedId())
	
	
	
	def set_controlsVis(self , item) :
		if cmds.objExists(self.custom_ctrl) :
			cmds.setAttr(self.custom_ctrl + '.controlsVis' , item.group().checkedId())
	
	
	
	def import_modular(self) :
		"""
		导入对应的绑定模块
		"""
		self.modular_listWidget.selectAll()
		modular_rig_list = []
		for item in self.modular_listWidget.selectedItems() :
			modular_rig_list.append((item.text()))
		build = build_rig.Build_Rig()
		build.import_modular(modular_rig_list)
	
	
	
	def claer_modular(self) :
		build = build_rig.Build_Rig()
		build.claer_modular()
		self.modular_listWidget.clear()
	
	
	
	def reset_control(self) :
		pipelineUtils.Pipeline.reset_control()
	
	
	
	def save_skinWeights(self) :
		geos = cmds.ls(sl = True)
		for geo in geos :
			obj = weightsUtils.Weights(geo)
			obj.save_skinWeights()
	
	
	
	def load_skinWeights(self) :
		geos = cmds.ls(sl = True)
		for geo in geos :
			obj = weightsUtils.Weights(geo)
			obj.load_skinWeights()
	
	
	
	def build_rig(self) :
		build = build_rig.Build_Rig()
		build.build_rig()



class arm_rig_property_widget(QWidget) :
	
	
	
	def __init__(self) :
		super(arm_rig_property_widget , self).__init__()
		self.arm_rig_ui = None
		self.init_ui()
	
	
	
	def init_ui(self) :
		# 读取qt Designer 写的ui文件
		loader = QUiLoader()
		# currentDir = os.path.dirname(__file__)#如果是import到maya中就可以的使用方法获得路径
		currentDir = os.path.abspath(__file__ + "/../../../ui/rigging_modular")
		file = QFile(currentDir + "/arm_rig.ui")  # 这个方法要使用绝对路径
		self.arm_rig_ui = loader.load(file , parentWidget = self)  # 初始化



#
def show() :
	global win
	try :
		win.close()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
	except :
		pass
	win = RiggingWindow()
	win.show()
