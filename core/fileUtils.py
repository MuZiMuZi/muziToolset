# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds
from importlib import reload
from . import qtUtils

class File (object) :
    """
    对于文件操作的类
    """

    def __init__ (self , file_path) :
        self.file_path = file_path
        # 设置文件的选择类型过滤器
        self.file_filter = "Maya(*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"  # 全部的过滤项

        self.selected_filter = "Maya (*.ma *.mb)"  # 记录选择的过滤项，每次更改过滤项的同时会更改这个全局变量的值


    def show_file_select_dialog (self) :
        '''
        打开文件资源浏览器
        '''
        # 打开一个文件资源浏览器，file_path 是所选择的文件路径,selected_filter是选择过滤的文件类型
        self.file_path , self.selected_filter = QtWidgets.QFileDialog.getOpenFileName (self , "Select File" , "" ,
                                                                                       self.file_filter ,
                                                                                       self.selected_filter)
    def load_file(self,load_method):
        """
        读取文件
        load_method(str):三种不同的读取方式，open,import,reference
        """
        # 检查文件路径是否存在，如果不存在则返回
        if not self.file_path :
            return
        # 判断给定的文件路径是否正确有对应的文件
        file_info = QtCore.QFileInfo (self.file_path)
        if not file_info.exists () :
            om.MGlobal.displayError ('这个路径的文件不存在：{}'.format (self.file_path))
            return

        #根据读取方式读取对应的文件
        self.load_method = load_method
        if self.load_method == 'open' :
            self.open_file ()
        elif self.load_method == 'import' :
            self.import_file ()
        else :
            self.reference_file ()

    def open_file (self) :
        force = False
        # 弹出一个对话框来让用户确认是否已经保存文件
        if not force and cmds.file (q = True , modified = True) :
            result = QtWidgets.QMessageBox.question (qtUtils.get_maya_window () , "提示" , "当前场景有未保存的更改。是否确定打开新文件？")
            if result == QtWidgets.QMessageBox.StandardButton.Yes :
                force = True
            else :
                return
        cmds.file (self.file_path , open = True , ignoreVersion = True , force = force)


    def import_file (self) :
        cmds.file (self.file_path , i = True , ignoreVersion = True)


    def reference_file (self) :
        cmds.file (self.file_path , r = True , ignoreVersion = True)


def text():
    """
    对于文件操作的例子
    """
    path = 'D:/rig/701Car_Rig/701_car_Rig_003Constraint.mb'
    file_obj = fileUtils.File (path)

    file_obj.load_file ('open')