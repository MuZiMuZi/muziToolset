import os

from PySide2.QtUiTools import QUiLoader
from ..widget import base_widget
from ..config import Side , ui_dir , Direction
from ..ui import bind , base , chain,chainEP
from . import base_widget,chain_widget
from importlib import reload



reload(chain_widget)
reload(chainEP)



class ChainEP_Widget(chain_widget.Chain_Widget , chainEP.Ui_MainWindow) :
	
	
	
	def __init__(self , name = 'chainEP') :
		'''
		使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

		'''
		super(chain_widget.Chain_Widget, self).__init__(name)
		self.base_ui = 'chainEP.ui'
		self.init_base()
