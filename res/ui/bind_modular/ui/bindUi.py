import os

import maya.cmds as cmds
from PySide2 import QtCore , QtWidgets
from PySide2.QtUiTools import QUiLoader
from ..config import icon_dir , Side , Direction , ui_dir , chain_dir , module_dir , base_dir , limb_dir
from .....core import qtUtils
from .....bind.base import *
from .....bind.chain import *
from .....bind.limb import *
from .....bind.module import *
from . import Bind
from . import baseUi

from importlib import reload



reload(baseUi)



class BindWindow(QtWidgets.QMainWindow , Bind.Ui_MainWindow) :
	"""
	Main dialog window class
	"""
	
	
	
	def __init__(self , parent = qtUtils.get_maya_window()) :
		"""
		Initialization
		"""
		super(BindWindow , self).__init__(parent)
		# 调用父类的ui方法，来运行ui
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.Window)
		
		self.item = None
		self.create_layout()
	
	
	
	def create_layout(self) :
		base = baseUi.BaseUi()
		base_widget = base.base_widget
		self.set_layout.addWidget(base_widget)
	
	def update_current(self):
		pass
	

def show() :
	window = BindWindow()
	try :
		window.close()
	except :
		pass
	window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
	window.show()
	return window
