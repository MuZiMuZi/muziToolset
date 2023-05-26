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
		self.setMinimumHeight(200)
		self.setMinimumWidth(200)
		
		# 添加部件
		self.create_widgets()
		self.create_layouts()
	
	
	
	def create_widgets(self) :
		self.lineEdit = QtWidgets.QLineEdit()
		self.checkBox1 = QtWidgets.QCheckBox()
		self.checkBox2 = QtWidgets.QCheckBox()
		self.ok_btn = QtWidgets.QPushButton('ok')
		self.cancel_btn = QtWidgets.QPushButton('cancel')
	
	
	
	def create_layouts(self) :
		# 创建表单布局
		self.form_layout = QtWidgets.QFormLayout()
		self.form_layout.addRow('name:' , self.lineEdit)
		self.form_layout.addRow('hiddon:' , self.checkBox1)
		self.form_layout.addRow('locked:' , self.checkBox2)
		
		# 创建水平布局
		self.button_layout = QtWidgets.QHBoxLayout()
		self.button_layout.addStretch()
		self.button_layout.addWidget(self.ok_btn)
		self.button_layout.addWidget(self.cancel_btn)
		
		# 创建主布局，并添加空间
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.addLayout(self.form_layout)
		self.main_layout.addLayout(self.button_layout)



if __name__ == "__main__" :
	t = TestDialog()
	t.show()
