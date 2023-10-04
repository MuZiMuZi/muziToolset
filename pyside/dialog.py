# coding=utf-8
import maya.OpenMayaUI as omui
from PySide2 import QtCore , QtWidgets
from shiboken2 import wrapInstance



def maya_main_window() :
	u"""
	返回maya的主窗口部件
	"""
	pointer = omui.MQtUtil.mainWindow()
	return wrapInstance(int(pointer) , QtWidgets.QWidget)



class custom_lineEdit(QtWidgets.QLineEdit) :
	u"""
	自定义一个新的lineEdit，重写keyPressEvent的方法
	"""
	enter_pressed = QtCore.Signal()
	
	
	
	def keyPressEvent(self , event) :
		u"""
		自定义一个键盘事件，当键盘事件触发的时候发出新的命令。类似clicked
		"""
		super().keyPressEvent(event)
		
		if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return :
			self.enter_pressed.emit(event.key())



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
		
		# # 添加连接
		# self.create_connections()
	
	
	
	def create_widgets(self) :
		self.lineedit = QtWidgets.QLineEdit()
		self.checkbox1 = QtWidgets.QCheckBox('Cheekbox1')
		self.checkbox2 = QtWidgets.QCheckBox('Cheekbox2')
		self.button1 = QtWidgets.QPushButton('Button1')
		self.button2 = QtWidgets.QPushButton('Button2')


	
	
	
	def create_layouts(self) :
		pass
		# 创建表单布局
		main_layout = QtWidgets.QVBoxLayout(self)
		main_layout.addWidget(self.lineedit)
		main_layout.addWidget(self.checkbox1)
		main_layout.addWidget(self.checkbox2)
		main_layout.addWidget(self.button1)
		main_layout.addWidget(self.button2)
		
		# 创建水平布局

		
		# 创建主布局，并添加空间

	
	
	



if __name__ == "__main__" :
	# 添加了销毁机制，如果之前有创建过这个窗口的话则先删除再创建新的窗口
	try :
		test_dialog.close()
		test_dialog.deleteLater()
	except :
		pass
	
	test_dialog = TestDialog()
	test_dialog.show()
