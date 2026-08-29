import os

from PySide2.QtUiTools import QUiLoader
from ..widget import base_widget
from ..config import Side , ui_dir , Direction
from ..ui import base_ui , chain_ui
from . import base_widget
from importlib import reload



reload(base_widget)
reload(chain_ui)



class Chain_Widget(base_widget.Base_Widget , chain_ui.Ui_MainWindow) :
	
	
	
	def __init__(self , name = 'chain') :
		'''
		使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

		'''
		super(base_widget.Base_Widget , self).__init__(name)
		self.base_ui = 'chain.ui'
		self.init_base()
	
	
	
	def init_base(self) :
		"""
		初始化作为QWidget对象的base_widget属性,用于设置绑定的基础属性（例如名称，边，关节数量，关节的父对象，控制器的父对象）
		"""
		super().init_base()
		# 添加direction的combox
		for direction in Direction :
			self.base_widget.direction_cbox.addItem(str(direction.value))
	
	
	
	def parse_extra(self) :
		length = self.extra_widget.length_sbox.value()
		direction = ast.literal_eval(self.extra_widget.direction_cbox.currentText())
		
		return [length , direction]
