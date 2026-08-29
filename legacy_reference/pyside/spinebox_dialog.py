# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window () :
    main_window_ptr = omui.MQtUtil.mainWindow ()
    return wrapInstance (long (main_window_ptr) , QtWidgets.QWidget)


class SpinBoxDialog (QtWidgets.QDialog) :

    def __init__ (self , parent = maya_main_window ()) :
        super (SpinBoxDialog , self).__init__ (parent)

        self.setWindowTitle ('Spin Box Dialog')
        self.setWindowFlags (self.windowFlags () ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets ()
        self.create_layouts ()
        self.create_connections ()


    def create_widgets (self) :
        #设置spinbox的属性
        self.spin_box = QtWidgets.QSpinBox ()
        self.spin_box.setFixedWidth (80)
        self.spin_box.setMinimum (-100)
        self.spin_box.setMaximum (100)
        self.spin_box.setSingleStep (5)
        self.spin_box.setPrefix ("$ ")  # 设置显示的前缀 但是不会当值来交互，仅仅是显示
        self.spin_box.setButtonSymbols (QtWidgets.QAbstractSpinBox.NoButtons)  # 取消显示上下按钮框

        self.double_spin_box = QtWidgets.QDoubleSpinBox ()
        self.double_spin_box.setFixedWidth (80)
        self.double_spin_box.setRange (-50.0 , 50.0)
        self.double_spin_box.setSuffix (" m")


    def create_layouts (self) :
        main_layout = QtWidgets.QFormLayout (self)
        main_layout.addRow ("Spin Box:" , self.spin_box)
        main_layout.addRow ("Double Spin Box:" , self.double_spin_box)


    def create_connections (self) :
        self.spin_box.valueChanged.connect (self.print_value)
        self.double_spin_box.valueChanged.connect (self.print_value)


    def print_value (self , value) :
        print ("Value: {}".format (value))


if __name__ == '__main__' :
    try :
        ui.close ()
        ui.deleteLater ()
    except :
        pass
    ui = SpinBoxDialog ()
    ui.show ()
