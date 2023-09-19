import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils
from .ui import Names_Tool
from importlib import reload
import maya.cmds as cmds


reload (Names_Tool)
reload (pipelineUtils)
reload (nameUtils)


class Names_Tool_main (Names_Tool.Ui_MainWindow , QtWidgets.QMainWindow) :

    def __init__ (self , *args , **kwargs) :
        super ().__init__ (*args , **kwargs)
        # 调用父类的ui方法，来运行ui
        self.setupUi (self)
        self.add_connect ()

        self.object_list = []


    def add_connect (self) :
        """
        添加按钮的方法连接
        """
        self.execute_button.clicked.connect (self.rename_object)


    def insert_modle (self) :
        """
        判断修改名称的模式,根据修改名称的模式来获取需要修改名称的对象
        """
        if self.selectied_button.isChecked () :
            self.object_list = cmds.ls (sl = True)
        elif self.hierarchy_button.isChecked () :
            self.object_list = pipelineUtils.Pipeline.select_sub_objects ()
        else :
            self.object_list = cmds.ls ('*')

        cmds.select (self.object_list)


    @pipelineUtils.Pipeline.make_undo
    def rename_object (self) :
        # 判断修改名称的模式,根据修改名称的模式来获取需要修改名称的对象
        self.insert_modle ()
        for object in self.object_list :
            obj = nameUtils.Name (name = object)
            # 添加前缀
            obj.add_prefix (self.prefix_lineEdit.text ())

            # 添加后缀
            obj.add_suffix (self.subfix_lineEdit.text ())
            # 根据搜索框的内容替换名称

            # 重命名


if __name__ == '__main__' :
    # 通过QApplication方法来生成应用
    app = QtWidgets.QApplication ()
    qt_app = Names_Tool_main ()
    qt_app.show ()
    app.exec_ ()
