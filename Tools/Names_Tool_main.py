import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from .config import ui_dir , icon_dir

from .ui import Names_Tool
from importlib import reload
import maya.cmds as cmds
reload(Names_Tool)

class Names_Tool_main (Names_Tool.Ui_MainWindow , QtWidgets.QMainWindow) :

    def __init__ (self, *args , **kwargs) :
        super ().__init__ (*args , **kwargs)
        # 调用父类的ui方法，来运行ui
        self.setupUi (self)


if __name__ == '__main__' :
    # 通过QApplication方法来生成应用
    app = QtWidgets.QApplication ()
    qt_app = Names_Tool_main ()
    qt_app.show ()
    app.exec_ ()
