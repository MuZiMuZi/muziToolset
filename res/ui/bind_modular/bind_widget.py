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
	
	
	
	def cmd_proxy_widget_dbclk(self , index) :
		u"""
		用来连接proxy_view双击所连接的功能槽函数
		index：鼠标双击的时候所在的位置
		"""
		# 获取proxy_view双击时候的位置信息
		index = self.proxy_widget.currentIndex()
		# 如果index.isValid的返回值有值的话，说明选择了可以点击的文件，不是的话则是空白的物体
		if index.isValid() :
			select_index = index.row()
			# 设置set_widget 的页数
			self.set_widget.setCurrentIndex(select_index)
		else :
			self.set_widget.setCurrentIndex(0)



if __name__ == '__main__' :
	app = QtWidgets.QApplication()
	qt_app = BindSystemWindow()
	qt_app.show()
	app.exec_()
