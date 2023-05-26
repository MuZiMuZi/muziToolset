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
		self.setWindowTitle('TestDialog')
		self.setMinimumHeight(300)
		self.setMinimumWidth(300)



if __name__ == "__main__" :
	t = TestDialog()
	t.show()
