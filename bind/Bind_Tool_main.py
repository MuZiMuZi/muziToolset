# coding=utf-8
from PySide2.QtWidgets import *

from res.ui.bind_modular.ui import Bind_Tool
from importlib import reload


reload (Bind_Tool)


class Bind_Tool (Bind_Tool.Ui_MainWindow , QMainWindow) :

    def __init__ (self , parent = None) :
        super ().__init__ (parent)
        # 调用父类的ui方法，来运行ui
        self.winTitle = 'Bind_Tool(命名工具)'
        self.setupUi (self)


def show () :
    try :
        bind_Tool.close ()
        bind_Tool.deleteLater ()
    except :
        pass
    bind_Tool = Bind_Tool ()

    bind_Tool.show ()


if __name__ == '__main__' :
    # 通过QApplication方法来生成应用
    app = QApplication ()
    qt_app = Bind_Tool ()
    qt_app.show ()
    app.exec_ ()
