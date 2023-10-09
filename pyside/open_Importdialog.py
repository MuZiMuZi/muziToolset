# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds
from ..core import qtUtils
from importlib import reload
reload(qtUtils)

def maya_main_window() :
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr) , QtWidgets.QWidget)



class OpenImportDialog(qtUtils.Dialog) :
	FILE_FILTERS = "Maya(*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"  # 全部的过滤项
	
	selected_filter = "Maya (*.ma *.mb)"  # 记录选择的过滤项，每次更改过滤项的同时会更改这个全局变量的值
	
	dlg_instance = None


	def __init__ (self , parent = qtUtils.get_maya_window ()) :
		super(OpenImportDialog,self).__init__(parent)
		# 设置标题和尺寸
		self.setWindowTitle ('Open/Import/Reference')
		self.setMinimumHeight (200)
		self.setMinimumWidth (300)

		# 添加部件
		self.create_widgets ()
		self.create_layouts ()

		# 添加连接
		self.create_connections ()


	def create_widgets (self) :
		"""创建需要的小部件"""
		#创建文件路径的小部件
		self.file_path_lineEdit = QtWidgets.QLineEdit()
		self.selected_btn = QtWidgets.QPushButton('...')

		#创建打开方式的单选按钮组
		self.open_rb = QtWidgets.QRadioButton()
		self.import_rb = QtWidgets.QRadioButton()
		self.reference_rb = QtWidgets.QRadioButton()



	def create_layouts (self) :
		"""创建需要的布局"""
		#创建文件路径的布局
		self.file_path_layout = QtWidgets.QHBoxLayout()
		self.file_path_layout.addWidget(self.file_path_lineEdit)
		self.file_path_layout.addWidget(self.selected_btn)

		#创建打开方式的布局
		self.radio_btn_layout = QtWidgets.QHBoxLayout()
		self.radio_btn_layout.addWidget(self.open_rb)
		self.radio_btn_layout.addWidget(self.import_rb)
		self.radio_btn_layout.addWidget(self.reference_rb)

		#创建表单布局来排列各个布局的顺序
		self.form_layout = QtWidgets.QFormLayout()
		self.form_layout.addRow('File:',self.file_path_layout)
		self.form_layout.addRow(self.radio_btn_layout)

		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.addLayout(self.form_layout)





	def create_connections (self) :
		"""连接需要的部件和对应的信号"""
		pass
	
	




import os



def show() :
	try :
		test_dialog.close ()
		test_dialog.deleteLater ()
	except :
		pass

	test_dialog = OpenImportDialog ()
	test_dialog.show ()

