# coding=utf-8
# 导入sys模块为了防止程序运行崩溃
# ui界面生成需要三个模块QtWidgets，QtGui，QtCore
from importlib import reload

from PySide2 import QtCore , QtWidgets
from PySide2.QtCore import Qt

from . import base_widget , chainEP_widget , chain_widget , limb_widget
from ..ui import bind
from .....core import qtUtils



rigtype_custom = ['baseRig']
rigtype_chain = ['chainFKRig' , 'chainIKRig' , 'chainIKFKRig' , 'fingerRig' , 'spineRig']
rigtype_chainEP = ['chainEPRig']
rigtype_limb = ['armRig' , 'legRig' , 'handRig' , 'tailRig' , 'spineRig']

reload(base_widget)
reload(chain_widget)
reload(bind)
reload(limb_widget)
reload(chainEP_widget)


class Bind_Widget(bind.Ui_MainWindow , QtWidgets.QMainWindow) :
	u'''
	用于创建绑定系统的界面系统
	'''
	
	
	
	def __init__(self , parent = qtUtils.get_maya_window()) :
		super().__init__(parent)
		# 调用父层级的创建ui方法
		self.setupUi(self)
		self.apply_model()
		
		self.add_connect()
		
		self.item = None
		self.edit_item = None
	
	
	def apply_model(self) :
		u"""
		添加模型到view里
		"""
		pass
	
	
	
	def add_connect(self) :
		u"""
		用来添加连接的槽函数
		"""
		self.proxy_widget.doubleClicked.connect(self.cmd_proxy_widget_dbclk)
		self.custom_widget.itemDoubleClicked.connect(self.cmd_custom_widget_dbclk)
		self.custom_widget.itemClicked.connect(self.cmd_custom_widget_clk)
	
	
	
	def cmd_proxy_widget_dbclk(self) :
		u"""
		用来连接proxy_widget双击所连接的功能槽函数
		index：鼠标双击的时候所在的位置
		"""
		# 获取proxy_view双击时候的位置信息
		index = self.proxy_widget.currentIndex()
		# 如果index.isValid的返回值有值的话，说明选择了可以点击的文件，不是的话则是空白的物体
		if index.isValid() :
			select_index = index.row()
			# 获得proxy_widget里所选择的item
			item = self.proxy_widget.currentItem().text()
			# 在custom_widget里添加这个item
			self.custom_widget.addItem(item[0 :-3])
			self.update_current(item)
		else :
			return
	
	
	
	def cmd_custom_widget_dbclk(self,item) :
		u"""
		用来连接custom_widget双击所连接的功能槽函数
		item：鼠标双击的时候所在的位置
		"""
		# 双击的时候可以重命名名称
		self.edit_item = item
		self.custom_widget.openPersistentEditor(self.edit_item)
		self.custom_widget.editItem(self.edit_item)
			
	
	def cmd_custom_widget_clk(self, item):
		u"""
		用来连接custom_widget双击所连接的功能槽函数
		item：鼠标单机的时候所在的位置
		"""
		self.edit_item = item
		# 单机的时候关闭重命名
		self.custom_widget.closePersistentEditor(self.edit_item)
	
	
	def close_edit(self) :
		u"""
		关闭edit
		"""
		if not self.edited_item:
			self.closePersistentEditor(self.edited_item)
	
	
	

	
	def update_current(self , item) :
		u"""
		获取proxy_widget所选择的项目，从而更新set_layout的面板
		Args:
			item:

		Returns:

		"""
		self.item = item
		self.initialize_field()
		# 获取custom_widget 里的item数量，切换到对应的设置面板
		index = self.custom_widget.count()
		self.setting_stack.setCurrentIndex(index)
	
	
	
	def initialize_field(self) :
		u"""
		根据所得知的item，创建对应的设置面板
		Returns:

		"""
		if self.item in rigtype_chain :
			chain = chain_widget.Chain_Widget()
			self.base_widget = chain.base_widget
		elif self.item in rigtype_chainEP :
			chainEP = chainEP_widget.ChainEP_Widget()
			self.base_widget = chainEP.base_widget
		elif self.item in rigtype_limb :
			limb = limb_widget.Limb_Widget()
			self.base_widget = limb.base_widget
		else :
			base = base_widget.Base_Widget()
			self.base_widget = base.base_widget
		self.base_widget.module_edit.setText('{}'.format(self.item))
		self.setting_stack.addWidget(self.base_widget)



def show() :
	# 添加了销毁机制，如果之前有创建过这个窗口的话则先删除再创建新的窗口
	global win
	try :
		win.close()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
	except :
		pass
	win = Bind_Widget()
	win.show()



if __name__ == "__main__" :
	# 添加了销毁机制，如果之前有创建过这个窗口的话则先删除再创建新的窗口
	window = Bind_Widget()
	# 添加了销毁机制，如果之前有创建过这个窗口的话则先删除再创建新的窗口
	try :
		window.close()
	except :
		pass
	window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
	window.show()
