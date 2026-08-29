import os
from functools import wraps

from PySide2 import QtWidgets , QtGui , QtCore

from ..config import icon_dir

from ..ui import bind_ui



def update_base_name(func) :
	"""
	更新组件模块中的名称属性和结构
	"""
	
	
	
	@wraps(func)
	def wrap(self) :
		self.base = '{}_{}_{}'.format(
				self._rtype , self._side.value , self._name)
		func(self)
	
	
	
	return wrap



class Bone_Widget(QtWidgets.QListWidgetItem) :
	
	
	
	def __init__(self , name) :
		'''
		使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象
		name(str):对应给定的模块名称
		'''
		super(Bone_Widget , self).__init__(name)
		
		# 初始化icon文件和ui文件
		self.icon = '{}.png'.format(name)
		self.base_ui = None
		self.extra_ui = None
		
		# 设置icon文件和ui文件的标题
		self.setText(name)
		icon = QtGui.QIcon()
		path = os.path.join(icon_dir , self.icon)
		icon.addFile(path)
		self.setIcon(icon)
		
		# 设置模板的widget
		# 调用父类的ui方法，来运行ui
		self.base_widget = None
		self.extra_widget = None
		
		# 绑定的组件对象
		self._obj = None
	
	
	
	def init_base(self) :
		"""
		初始化作为QWidget对象的base_widget属性,用于设置绑定的基础属性（例如名称，边，关节数量，关节的父对象，控制器的父对象）
		"""
		pass
	
	
	
	def init_extra(self) :
		"""
		初始化作为QWidget对象的extra_widget属性，用于显示绑定的特殊属性（例如长度、分段，朝向）
		"""
		pass
	
	
	
	def parse_base(self) :
		"""
		将base_widget中的输入作为参数进行分析并返回
		"""
		pass
	
	
	
	def parse_extra(self) :
		"""
		分析extra_widget中的输入并将其作为参数返回
		"""
		pass
	

	def add_connect(self):
		u"""
		用来添加连接的槽函数
		"""
		pass

	def build_setup(self , *args) :
		"""
		构建绑定的定位结构和生成准备
		"""
		pass
	
	
	
	def delete_setup(self) :
		"""
		删除生成准备的定位关节
		"""
		pass
