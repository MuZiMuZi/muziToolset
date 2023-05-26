# coding=utf-8
# 导入sys模块为了防止程序运行崩溃
import sys
# ui界面生成需要三个模块QtWidgets，QtGui，QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from importlib import reload
from . import bindSystem
from ....core import qtUtils
reload(qtUtils)

reload(bindSystem)



class BindSystemWindow(bindSystem.Ui_MainWindow , QtWidgets.QMainWindow) :
	u'''
	用于创建绑定系统的界面系统
	'''
	
	
	
	def __init__(self , *args , **kwargs) :
		super().__init__(*args , **kwargs)
		# 调用父层级的创建ui方法
		self.setupUi(self)
		self.apply_model()
		
		self.add_connect()
	
	
	
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
			#在custom_widget里添加这个item
			self.custom_widget.addItem(item[0:-3])
		else :
			return
		
	def cmd_custom_widget_dbclk(self):
		u"""
		用来连接custom_widget双击所连接的功能槽函数
		index：鼠标双击的时候所在的位置
		"""
		index = self.custom_widget.currentIndex()
		# 如果index.isValid的返回值有值的话，说明选择了可以点击的文件，不是的话则是空白的物体
		if index.isValid() :
			# 获得custom_widget里所选择的item
			self.edited_item = self.custom_widget.currentItem()
			#开始编辑模式
			self.custom_widget.openPersistentEditor(self.edited_item)
			self.custom_widget.editItem(self.edited_item)
		else :
			self.custom_widget.closePersistentEditor(self.edited_item)

		
	def close_edit(self):
		u"""
		关闭edit
		"""
		if self.edited_item and self.isPersistentEditorOpen(self.edited_item) :
			self.closePersistentEditor(self.edited_item)

		
if __name__ == '__main__' :
	app = QtWidgets.QApplication()
	qt_app = BindSystemWindow()
	qt_app.show()
	app.exec_()
