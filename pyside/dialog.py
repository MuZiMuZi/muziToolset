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
		按键事件
		"""
		super().keyPressEvent(event)
		
		if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return :
			self.enter_pressed.emit()



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
		
		# 添加连接
		self.create_connections()
	
	
	
	def create_widgets(self) :
		self.lineEdit = custom_lineEdit()
		self.hidden_box = QtWidgets.QCheckBox()
		self.checkBox2 = QtWidgets.QCheckBox()
		
		self.combo_box = QtWidgets.QComboBox()
		self.combo_box.addItems(['test1' , 'test2' , 'test3' , 'test4'])
		
		self.ok_btn = QtWidgets.QPushButton('ok')
		self.cancel_btn = QtWidgets.QPushButton('cancel')
	
	
	
	def create_layouts(self) :
		# 创建表单布局
		self.form_layout = QtWidgets.QFormLayout()
		self.form_layout.addRow('name:' , self.lineEdit)
		self.form_layout.addRow('hidden:' , self.hidden_box)
		self.form_layout.addRow('locked:' , self.checkBox2)
		self.form_layout.addRow(self.combo_box)
		
		# 创建水平布局
		self.button_layout = QtWidgets.QHBoxLayout()
		self.button_layout.addStretch()
		self.button_layout.addWidget(self.ok_btn)
		self.button_layout.addWidget(self.cancel_btn)
		
		# 创建主布局，并添加空间
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.addLayout(self.form_layout)
		self.main_layout.addLayout(self.button_layout)
	
	
	
	def create_connections(self) :
		u"""
		创建槽函数的连接
		"""
		self.lineEdit.enter_pressed.connect(self.on_enter_presseed)
		self.hidden_box.toggled.connect(self.print_is_hidden)
		self.cancel_btn.clicked.connect(self.close)
		
		# 连接combo_box的连接信号
		self.combo_box.activated.connect(self.on_activated_int)
		self.combo_box.activated[str].connect(self.on_activated_str)
	
	
	
	def print_hello_name(self) :
		name = self.lineEdit.text()
		print('hello {}!'.format(name))
	
	
	
	def print_is_hidden(self) :
		hidden = self.hidden_box.isChecked()
		if hidden :
			print('hidden')
		else :
			print('visible')
	
	
	
	@QtCore.Slot(int)
	def on_activated_int(self , index) :
		print('comboBox Index : {}'.format(index))
	
	
	
	@QtCore.Slot(str)
	def on_activated_str(self , text) :
		print('comboBox Text : {}'.format(text))
	
	
	
	def on_enter_presseed(self) :
		print('Enter Key Pressed')



if __name__ == "__main__" :
	# 添加了销毁机制，如果之前有创建过这个窗口的话则先删除再创建新的窗口
	try :
		test_dialog.close()
		test_dialog.deleteLater()
	except :
		pass
	
	test_dialog = TestDialog()
	test_dialog.show()
