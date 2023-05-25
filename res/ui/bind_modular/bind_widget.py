# coding=utf-8
# 导入sys模块为了防止程序运行崩溃
import sys
# ui界面生成需要三个模块QtWidgets，QtGui，QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from importlib import reload
from . import bindSystem



reload(bindSystem)



class BindSystemWindow(bindSystem.Ui_MainWindow , QtWidgets.QMainWindow) :
	u'''
	用于创建绑定系统的界面系统
	'''
	
	
	
	def __init__(self , *args , **kwargs) :
		super().__init__(*args , **kwargs)
		# 调用父层级的创建ui方法
		self.setupUi(self)
		self.proxy_path = 'D:/'
		self.apply_model()
		
		self.add_connect()
	
	
	def apply_model(self) :
		u"""
		添加模型到view里
		"""
		# # 添加模型到proxy_view里
		# self.proxy_model = QtWidgets.QFileSystemModel()
		# self.proxy_view.setModel(self.proxy_model)
		# self.proxy_view.setRootIndex(self.proxy_path)
		# root_index= self.proxy_model.index(self.proxy_path)
		# self.proxy_view.setRootIndex(root_index)
		#
		# 添加模型到proxy_view里
		self.proxy_model = QtGui.QStandardItemModel()
		self.proxy_view.setModel(self.proxy_model)
	
	def add_connect(self):
		u"""
		用来添加连接的槽函数
		"""
		self.proxy_view.doubleClicked.connect(self.cmd_proxy_view_dbclk)
		


if __name__ == '__main__' :
	app = QtWidgets.QApplication()
	qt_app = BindSystemWindow()
	qt_app.show()
	app.exec_()
