# coding=utf-8
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance



def maya_main_window() :
	u"""
	返回maya的主窗口部件
	"""
	pointer = omui.MQtUtil.mainWindow()
	return wrapInstance(int(pointer) , QtWidgets.QWidget)



class TestDialog(QtWidgets.QDialog) :
	
	
	
	def __init__(self , parent = maya_main_window()) :
		super(TestDialog , self).__init__(parent)
		# 设置标题和尺寸
		self.setWindowTitle('TestDialog')
		self.setMinimumHeight(300)
		self.setMinimumWidth(300)
		
		# 添加部件
		self.create_widgets()
		self.create_layouts()
	
	
	
	def create_widgets(self) :
		self.lineEdit = QtWidgets.QLineEdit()
		self.checkBox1 = QtWidgets.QCheckBox('checkBox1')
		self.checkBox2 = QtWidgets.QCheckBox('checkBox2')
		self.button1 = QtWidgets.QPushButton('button1')
		self.button2 = QtWidgets.QPushButton('button2')
	
	
	
	def create_layouts(self) :
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.addWidget(self.lineEdit)
		self.main_layout.addWidget(self.checkBox1)
		self.main_layout.addWidget(self.checkBox2)
		self.main_layout.addWidget(self.button1)
		self.main_layout.addWidget(self.button2)



if __name__ == "__main__" :
	t = TestDialog()
	t.show()
