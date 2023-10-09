# coding=utf-8
import maya.OpenMayaUI as omui
from PySide2 import QtCore , QtWidgets
from shiboken2 import wrapInstance


def maya_main_window () :
    u"""
    返回maya的主窗口部件
    """
    pointer = omui.MQtUtil.mainWindow ()
    return wrapInstance (int (pointer) , QtWidgets.QWidget)


class custom_lineEdit (QtWidgets.QLineEdit) :
    u"""
    自定义一个新的lineEdit，重写keyPressEvent的方法
    """
    enter_pressed = QtCore.Signal ()


    def keyPressEvent (self , event) :
        u"""
        自定义一个键盘事件，当键盘事件触发的时候发出新的命令。类似clicked
        """
        super ().keyPressEvent (event)

        if event.key () == QtCore.Qt.Key_Enter or event.key () == QtCore.Qt.Key_Return :
            self.enter_pressed.emit (event.key ())


class TestDialog (QtWidgets.QDialog) :


    def __init__ (self , parent = maya_main_window ()) :
        super (TestDialog , self).__init__ (parent)
        # 设置标题和尺寸
        self.setWindowTitle ('TestDialog')
        self.setMinimumHeight (200)
        self.setMinimumWidth (200)

        # 添加部件
        self.create_widgets ()
        self.create_layouts ()

        # 添加连接
        self.create_connections ()


    def create_widgets (self) :
        self.lineedit = QtWidgets.QLineEdit ()
        self.checkbox1 = QtWidgets.QCheckBox ('Cheekbox1')
        self.checkbox2 = QtWidgets.QCheckBox ('Cheekbox2')
        self.ok_button = QtWidgets.QPushButton ('ok')
        self.cancel_button = QtWidgets.QPushButton ('cancel')

        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(['com1','com2','com3','com4'])


    def create_layouts (self) :
        # 创建表单布局
        from_layout = QtWidgets.QFormLayout ()
        from_layout.addRow ('Name:' , self.lineedit)
        from_layout.addRow ('Hidden:' , self.checkbox1)
        from_layout.addRow ('Locked:' , self.checkbox2)
        from_layout.addRow(self.combobox)

        # 创建水平布局
        button_layout = QtWidgets.QHBoxLayout ()
        button_layout.addStretch ()
        button_layout.addWidget (self.ok_button)
        button_layout.addWidget (self.cancel_button)

        # 创建主布局，并添加空间
        main_layout = QtWidgets.QVBoxLayout (self)
        main_layout.addLayout (from_layout)
        main_layout.addLayout (button_layout)


    def create_connections (self) :
        self.cancel_button.clicked.connect (self.close)
        self.lineedit.editingFinished.connect (self.print_hello_name)
        self.checkbox1.toggled.connect (self.print_is_hidden)


    def print_hello_name (self) :
        name = self.lineedit.text ()
        print ('hello,{}'.format (name))


    def print_is_hidden (self , checked) :
        # hidden = self.checkbox1.isChecked ()
        if checked :
            print ('hidden')
        else :
            print ('visible')

    def on_activated_int(self,index):
        print('comboBox Index : {}',format(index))


    def on_activated_int (self , text) :
        print ('comboBox Text : {}' , format (text))


if __name__ == "__main__" :
    # 添加了销毁机制，如果之前有创建过这个窗口的话则先删除再创建新的窗口
    try :
        test_dialog.close ()
        test_dialog.deleteLater ()
    except :
        pass

    test_dialog = TestDialog ()
    test_dialog.show ()
