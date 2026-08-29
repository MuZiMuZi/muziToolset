from PySide2 import QtWidgets

from . import chain_widget
from ..ui import limb_ui
from importlib import reload


reload (limb_ui)


class Limb_Widget (limb_ui.Ui_MainWindow , chain_widget.Chain_Widget) :


    def __init__ (self , name = 'limb') :
        '''
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        self.base_ui = 'limb.ui'
        self.init_base ()
