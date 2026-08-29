# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds



def maya_main_window() :
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr) , QtWidgets.QWidget)



class CustomDialog(QtWidgets.QDialog) :
	
	
	
	def __init__(self , parent = maya_main_window()) :
		super(CustomDialog , self).__init__(parent)
		
		self.setWindowTitle("Custom Dialog")
		self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
		
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
	
	
	
	def create_widgets(self) :
		self.lineedit = QtWidgets.QLineEdit()
		self.ok_btn = QtWidgets.QPushButton('OK')
	
	
	
	def create_layouts(self) :
		wdg_layout = QtWidgets.QHBoxLayout()
		wdg_layout.addWidget(QtWidgets.QLabel("Name: "))
		wdg_layout.addWidget(self.lineedit)
		
		btn_layout = QtWidgets.QHBoxLayout()
		btn_layout.addStretch()
		btn_layout.addWidget(self.ok_btn)
		
		main_layout = QtWidgets.QVBoxLayout(self)
		main_layout.addLayout(wdg_layout)
		main_layout.addLayout(btn_layout)
	
	
	
	def create_connections(self) :
		self.ok_btn.clicked.connect(self.accept)
	
	
	
	def get_text(self) :
		return (self.lineedit.text())



class TestDialog(QtWidgets.QDialog) :
	
	
	
	def __init__(self , parent = maya_main_window()) :
		super(TestDialog , self).__init__(parent)
		
		self.setWindowTitle('Test Dialog')
		self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
		
		self.initial_directory = cmds.internalVar(userPrefDir = True)  # 默认文件窗口打开路径
		self.initial_color = QtGui.QColor(255 , 0 , 0)  # 默认颜色窗口初始选择的颜色
		
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
	
	
	
	def create_widgets(self) :
		self.warning_btn = QtWidgets.QPushButton("Warning")
		self.folder_select_btn = QtWidgets.QPushButton("Folder Select")
		self.color_select_btn = QtWidgets.QPushButton("Color Select")
		self.custom_btn = QtWidgets.QPushButton("Modal (Custom)")
	
	
	
	def create_layouts(self) :
		main_layout = QtWidgets.QHBoxLayout(self)
		main_layout.addWidget(self.warning_btn)
		main_layout.addWidget(self.folder_select_btn)
		main_layout.addWidget(self.color_select_btn)
		main_layout.addWidget(self.custom_btn)
	
	
	
	def create_connections(self) :
		self.warning_btn.clicked.connect(self.show_warning_dialog)
		self.folder_select_btn.clicked.connect(self.show_folder_select)
		self.color_select_btn.clicked.connect(self.show_color_select)
		self.custom_btn.clicked.connect(self.show_custom_dialog)
	
	
	
	def show_warning_dialog(self) :
		QtWidgets.QMessageBox.warning(self , "Object Not Found" , "Camera 'shotcam' not found.")
	
	
	
	def show_folder_select(self) :
		new_directory = QtWidgets.QFileDialog.getExistingDirectory(self , "Select Folder" , self.initial_directory)
		if new_directory :
			self.initial_directory = new_directory
		
		print("Selected Folder : {}".format(new_directory))
	
	
	
	def show_color_select(self) :
		self.initial_color = QtWidgets.QColorDialog.getColor(self.initial_color , self)
		
		print("Red:{} Green:{} Blue:{}".format(self.initial_color.red() ,
		                                       self.initial_color.green() ,
		                                       self.initial_color.blue()))
	
	
	
	def show_custom_dialog(self) :
		custom_dialog = CustomDialog()
		
		result = custom_dialog.exec_()  # 自定义窗口模式 这个模式是打开后只能够在当前窗口操作，窗口关闭前不能执行窗口外的操作
		
		if result == QtWidgets.QDialog.Accepted :
			print("Name: {}".format(custom_dialog.get_text()))



if __name__ == '__main__' :
	try :
		ui.close()
		ui.deleteLater()
	except :
		pass
	ui = TestDialog()
	ui.show()
