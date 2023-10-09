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
		self.setWindowTitle ('TestDialog')
		self.setMinimumHeight (200)
		self.setMinimumWidth (200)

		# 添加部件
		self.create_widgets ()
		self.create_layouts ()

		# 添加连接
		self.create_connections ()


	def create_widgets (self) :
		"""创建需要的小部件"""
		pass


	def create_layouts (self) :
		"""创建需要的布局"""
		pass


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


show()
