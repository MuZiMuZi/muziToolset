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
	
	
	
	def apply_model(self) :
		u"""
		添加模型到view里
		"""





if __name__ == '__main__' :
	app = QtWidgets.QApplication()
	qt_app = BindSystemWindow()
	qt_app.show()
	app.exec_()
