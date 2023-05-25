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
		pass

		
	def add_connect(self) :
		u"""
		用来添加连接的槽函数
		"""
		pass
	
	
	
	def cmd_proxy_view_dbclk(self , index) :
		u"""
		用来连接proxy_view双击所连接的功能槽函数
		index：鼠标双击的时候所在的位置
		"""
		# 判断点击的地方是否是可以选择的东西，不是空白的地方
		pass
	
	
	
	def add_item_proxy_view(self) :
		# # 以文件的名称制作item
		# file_path= 'aa'
		# Qitem = QtGui.QStandardItem(file_path)
		# self.proxy_model.appendRow(Qitem)
		pass



if __name__ == '__main__' :
	app = QtWidgets.QApplication()
	qt_app = BindSystemWindow()
	qt_app.show()
	app.exec_()
