# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds


def maya_main_window () :
    main_window_ptr = omui.MQtUtil.mainWindow ()
    return wrapInstance (int (main_window_ptr) , QtWidgets.QWidget)


class TreeViewDialog (QtWidgets.QDialog) :
    WINDOW_TITLE = "Tree View Dialog"


    def __init__ (self , parent = maya_main_window ()) :
        super (TreeViewDialog , self).__init__ (parent)

        self.setWindowTitle (self.WINDOW_TITLE)
        self.setMinimumSize (500 , 400)
        self.setWindowFlags (self.windowFlags () ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets ()
        self.create_layout ()
        self.create_connections ()


    def create_widgets (self) :
        root_path = "{}scripts".format (cmds.internalVar (userAppDir = True))  # 得到maya脚本目录
        #创建文件管理模型
        self.model = QtWidgets.QFileSystemModel ()
        self.model.setRootPath (root_path)

        self.tree_view = QtWidgets.QTreeView ()
        self.tree_view.setModel (self.model)
        self.tree_view.setRootIndex (self.model.index (root_path))
        self.tree_view.hideColumn (1)
        self.tree_view.setColumnWidth (0 , 240)

        # self.model.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)

        self.model.setNameFilters (["*.py"])  # 使只能选中.py后缀的文件
        self.model.setNameFilterDisables (False)  # 将不能选中的文件进行隐藏


    def create_layout (self) :
        main_layout = QtWidgets.QVBoxLayout (self)
        main_layout.setContentsMargins (2 , 2 , 2 , 2)
        main_layout.addWidget (self.tree_view)


    def create_connections (self) :
        self.tree_view.doubleClicked.connect (self.on_double_clicked)


    def on_double_clicked (self , index) :
        path = self.model.filePath (index)

        if self.model.isDir (index) :
            print ("Directory selected: {}".format (path))
        else :
            print ("Directory selected: {}".format (path))


if __name__ == '__main__' :
    try :
        ui.close ()
        ui.deleteLater ()
    except :
        pass
    ui = TreeViewDialog ()
    ui.show ()
