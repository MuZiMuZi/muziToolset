# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds
from ..core import qtUtils
from importlib import reload


reload (qtUtils)


def maya_main_window () :
    main_window_ptr = omui.MQtUtil.mainWindow ()
    return wrapInstance (int (main_window_ptr) , QtWidgets.QWidget)


class OpenImportDialog (qtUtils.Dialog) :
    FILE_FILTERS = "Maya(*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"  # 全部的过滤项

    selected_filter = "Maya (*.ma *.mb)"  # 记录选择的过滤项，每次更改过滤项的同时会更改这个全局变量的值

    dlg_instance = None


    def __init__ (self , parent = qtUtils.get_maya_window ()) :
        super (OpenImportDialog , self).__init__ (parent)
        # 设置标题和尺寸
        self.setWindowTitle ('Open/Import/Reference')
        self.setMinimumHeight (200)
        self.setMinimumWidth (300)

        # 添加部件
        self.create_widgets ()
        self.create_layouts ()

        # 添加连接
        self.create_connections ()


    def create_widgets (self) :
        """创建需要的小部件"""
        # 创建文件路径的小部件
        self.file_path_lineEdit = QtWidgets.QLineEdit ()
        self.selected_btn = QtWidgets.QPushButton ()
        # 选择文件的按钮设置图标和设置文字提示
        self.selected_btn.setIcon (QtGui.QIcon (':fileOpen.png'))
        self.selected_btn.setToolTip ('Select File')

        # 创建打开方式的单选按钮组
        self.open_rb = QtWidgets.QRadioButton ('Open')
        self.open_rb.setChecked (True)
        self.import_rb = QtWidgets.QRadioButton ('Import')
        self.reference_rb = QtWidgets.QRadioButton ('Reference')

        self.force_cb = QtWidgets.QCheckBox ('Force')

        # 创建确定和关闭的按钮
        self.apply_btn = QtWidgets.QPushButton ('Apply')
        self.close_btn = QtWidgets.QPushButton ('Close')


    def create_layouts (self) :
        """创建需要的布局"""
        # 创建文件路径的布局
        self.file_path_layout = QtWidgets.QHBoxLayout ()
        self.file_path_layout.addWidget (self.file_path_lineEdit)
        self.file_path_layout.addWidget (self.selected_btn)

        # 创建打开方式的布局
        self.radio_btn_layout = QtWidgets.QHBoxLayout ()
        self.radio_btn_layout.addWidget (self.open_rb)
        self.radio_btn_layout.addWidget (self.import_rb)
        self.radio_btn_layout.addWidget (self.reference_rb)

        # 创建表单布局来排列各个布局的顺序
        self.form_layout = QtWidgets.QFormLayout ()
        self.form_layout.addRow ('File:' , self.file_path_layout)
        self.form_layout.addRow (self.radio_btn_layout)
        self.form_layout.addRow (self.force_cb)

        # 创建按钮布局
        self.btn_layout = QtWidgets.QHBoxLayout ()
        self.btn_layout.addStretch ()
        self.btn_layout.addWidget (self.apply_btn)
        self.btn_layout.addWidget (self.close_btn)

        self.main_layout = QtWidgets.QVBoxLayout (self)
        self.main_layout.addLayout (self.form_layout)
        self.main_layout.addLayout (self.btn_layout)


    def create_connections (self) :
        """连接需要的部件和对应的信号"""
        self.selected_btn.clicked.connect (self.show_file_select_dialog)

        self.open_rb.toggled.connect (self.update_force_visibility)
        self.apply_btn.clicked.connect (self.load_file)
        self.close_btn.clicked.connect (self.close)


    def show_file_select_dialog (self) :
        '''
        打开文件资源浏览器
        '''
        #打开一个文件资源浏览器，file_path 是所选择的文件路径
        file_path,selected_filter = QtWidgets.QFileDialog.getOpenFileName(self,'Select File')
        #将所选择的文件路径添加到输入框内
        if file_path:
            self.file_path_lineEdit.setText(file_path)

    def update_force_visibility (self) :
        self.force_cb.setVisible (checked)


    def load_file (self) :
        pass


import os


def show () :
    try :
        test_dialog.close ()
        test_dialog.deleteLater ()
    except :
        pass

    test_dialog = OpenImportDialog ()
    test_dialog.show ()
