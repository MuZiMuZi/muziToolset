try :
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	from PySide2 import __version__ , QtCore , QtGui
	from shiboken2 import wrapInstance

except ImportError :
	from PySide.QtCore import *
	from PySide.QtGui import *
	from PySide.QtWidgets import *
	from PySide import __version__
	from shiboken import wrapInstance



class Widget(QWidget) :
	
	
	
	def __init__(self) :
		super(Widget , self).__init__()
		self.init_ui()
	
	
	
	def init_ui(self) :
		self.main_layout = QHBoxLayout(self)
		
		self.test_line = QLineEdit()
		
		self.main_layout.addWidget(self.test_line)



def show() :
	global win
	try :
		win.close()
	except :
		pass
	win = Widget()
	win.show()



show()
