import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils
import muziToolset.res.ui.backGround as backGround
from .ui import Names_Tool
from importlib import reload
import maya.cmds as cmds


reload (Names_Tool)
reload (pipelineUtils)
reload (nameUtils)


class Names_Tool (Names_Tool.Ui_MainWindow , QtWidgets.QMainWindow) :

    def __init__ (self , parent = None) :
        super ().__init__ (parent)
        # 调用父类的ui方法，来运行ui
        self.winTitle = 'Names_Tool(命名工具)'
        self.setupUi (self)
        self.add_connect ()

        self.object_list = []

        self.set_input_content ()


    def set_input_content (self) :
        '''
        设置输入内容的规范
        '''
        ## 限制以下特殊符号在lineEdit中的输入
        rx = QtCore.QRegExp ("[^\\\\/:*?\"<>| ]*")
        validator = QtGui.QRegExpValidator (rx)

        for lineEdit in [self.prefix_lineEdit , self.subfix_lineEdit , self.search_lineEdit , self.replace_lineEdit ,
                         self.rename_lineEdit] :
            lineEdit.setValidator (validator)


    def add_connect (self) :
        """
        添加按钮的方法连接
        """
        self.execute_button.clicked.connect (self.rename_object)
        self.reset_button.clicked.connect (self.reset_input_field)


    def insert_modle (self) :
        """
        判断修改名称的模式,根据修改名称的模式来获取需要修改名称的对象
        """
        # 选中的物体修改命名的情况
        if self.selectied_button.isChecked () :
            self.object_list = cmds.ls (sl = True , l = 1)

        # 层级修改命名的情况
        elif self.hierarchy_button.isChecked () :
            self.object_list = pipelineUtils.Pipeline.select_sub_objects ()
        # 全部修改命名的情况
        else :
            cmds.select (allDagObjects = True)
            self.object_list = cmds.ls (sl = True , l = 1)
        # 判断object_list里是否有无法重命名的节点,如果有的话将其删除
        cmds.select (self.object_list)


    @pipelineUtils.Pipeline.make_undo
    def rename_object (self) :
        # 判断修改名称的模式,根据修改名称的模式来获取需要修改名称的对象
        self.insert_modle ()

        for object in self.object_list :
            obj = nameUtils.Name (name = object)
            # 添加前缀
            if self.prefix_lineEdit.text () :
                obj.add_prefix (self.prefix_lineEdit.text ())

            # 添加后缀
            if self.subfix_lineEdit.text () :
                obj.add_suffix (self.subfix_lineEdit.text ())
            # 根据搜索框的内容替换名称
            if self.search_lineEdit.text () :
                obj.search_replace_name (self.search_lineEdit.text () , self.replace_lineEdit.text ())
            # 重命名
            if self.rename_lineEdit.text () :
                obj.rename_to_name (self.rename_lineEdit.text ())


    def reset_input_field (self) :
        """
        重置输入栏的内容
        """
        for lineEdit in [self.prefix_lineEdit , self.subfix_lineEdit , self.search_lineEdit , self.replace_lineEdit ,
                         self.rename_lineEdit] :
            lineEdit.clear ()


def show () :
    try :
        name_tool.close ()
        name_tool.deleteLater ()
    except :
        pass
    name_tool = Names_Tool ()

    name_tool.show ()


def main () :
    return Names_Tool ()


if __name__ == '__main__' :
    # 通过QApplication方法来生成应用
    app = QtWidgets.QApplication ()
    qt_app = Names_Tool ()
    qt_app.show ()
    app.exec_ ()
