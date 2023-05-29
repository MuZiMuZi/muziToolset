import os
import maya.cmds as cmds

from PySide2 import QtWidgets , QtGui

from PySide2.QtUiTools import QUiLoader
from . import boneUi
from ..config import Side , ui_dir
from . import Bind
from .....core import qtUtils

from importlib import reload



reload(Bind)

from . import base



class BaseUi(boneUi.RigItem , Bind.Ui_MainWindow) :
	
	
	
	def __init__(self , name = 'base' ) :
		'''
		使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象
		
		'''
		super(boneUi.RigItem , self).__init__(name)
		self.base_ui = 'base.ui'
		self.init_base()
		
	
	
	def init_base(self) :
		"""
		初始化作为QWidget对象的base_widget属性,用于设置绑定的基础属性（例如名称，边，关节数量，关节的父对象，控制器的父对象）
		"""
		
		self.base_widget = QUiLoader().load(os.path.join(ui_dir , self.base_ui))
	# # 添加边的combox
	# for side in Side :
	# 	self.base_widget.side_cbox.addItem(side.value)
	#
	
	
	def build_setup(self , side , base_name) :
		"""
		
		Args:
			side（str）: 需要生成的绑定的边
			base_name:读取到的输入信息

		Returns:

		"""
		self._obj = Base(side , base_name)
		self._obj.build_guide()
	
	
	
	def parse_base(self) :
		"""
		分析extra_widget中的输入并将其作为参数返回
		"""
		name = self.base_widget.name_edit.text()
		side = self.base_widget.side_cbox.currentText()
		return [Side(side) , name]
	
	
	
	def build_rig(self) :
		"""
		根据绑定模块的定位关节来生成对应的绑定系统
		"""
		self._obj.build_rig()
