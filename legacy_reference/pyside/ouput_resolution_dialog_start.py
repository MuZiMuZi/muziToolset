# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window () :
    main_window_ptr = omui.MQtUtil.mainWindow ()
    return wrapInstance (int (main_window_ptr) , QtWidgets.QWidget)


class OutputResolutionDialog (QtWidgets.QDialog) :
    # 数值用带小数点的原因是要计算长宽比，长宽比是小数
    RESOLUTION_ITEMS = [["1920X1080 (1080p)" , 1920.0 , 1080.0] ,
                        ["1280X720 (720p)" , 1280.0 , 720.0] ,
                        ["960X540 (540p)" , 960.0 , 540.0] ,
                        ["640X480" , 640.0 , 480.0] ,
                        ["320X240" , 320.0 , 240.0]]


    def __init__ (self , parent = maya_main_window ()) :
        super (OutputResolutionDialog , self).__init__ (parent)

        self.setWindowTitle ('Output Resolution')
        self.setFixedWidth (220)
        self.setWindowFlags (self.windowFlags () ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets ()
        self.create_layouts ()
        self.create_connections ()


    def create_widgets (self) :
        self.resolution_list_wdg = QtWidgets.QListWidget ()

        for resolution_item in self.RESOLUTION_ITEMS :
            list_wdg_item = QtWidgets.QListWidgetItem (resolution_item [0])
            # QtCore.Qt.UserRole可以理解为序号0,一个item可以拥有多个数据，因此可以通过QtCore.Qt.UserRole，QtCore.Qt.UserRole+1来设置数据的序号
            list_wdg_item.setData (QtCore.Qt.UserRole ,
                                   [resolution_item [1] , resolution_item [2]])
            self.resolution_list_wdg.addItem (list_wdg_item)

        self.close_btn = QtWidgets.QPushButton ('Close')


    def create_layouts (self) :
        button_layout = QtWidgets.QHBoxLayout ()
        button_layout.addStretch ()
        button_layout.addWidget (self.close_btn)

        main_layout = QtWidgets.QVBoxLayout (self)
        main_layout.setContentsMargins (2 , 2 , 2 , 2)  # 设置布局与窗口边界的距离
        main_layout.setSpacing (2)  # 设置布局中的控件之间的间隙
        main_layout.addWidget (self.resolution_list_wdg)
        main_layout.addStretch ()
        main_layout.addLayout (button_layout)


    def create_connections (self) :
        self.resolution_list_wdg.itemClicked.connect (self.set_output_resolution)

        self.close_btn.clicked.connect (self.close)


    def set_output_resolution (self , item) :
        resolution = item.data (QtCore.Qt.UserRole)

        cmds.setAttr ("defaultResolution.width" , resolution [0])
        cmds.setAttr ("defaultResolution.height" , resolution [1])
        cmds.setAttr ("defaultResolution.deviceAspectRatio" , resolution [0] / resolution [1])


if __name__ == '__main__' :
    try :
        ui.close ()
        ui.deleteLater ()
    except :
        pass
    ui = OutputResolutionDialog ()
    ui.show ()
