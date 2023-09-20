import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import pymel.core as pm
from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils,jointUtils
from importlib import reload
import maya.cmds as cmds


class Joint_Tool () :
    """
    一个关节工具的类
    """
    def __init__ (self , *args , **kwargs) :
        super ().__init__ (*args , **kwargs)
        self.win_name = 'Joint_Tool'
        self.win_title = 'Joint_Tool(关节工具)'
        self.init_ui()

    def init_ui(self):
        # columnWidth3设置三个部件的宽度，adjustableColumn表示第几个部件跟随着窗口缩放
        # placeholderText提示语
        # self.main_window = pm.window(height = 500,
        #                              width = 300)
        with pm.frameLayout (height = 600,width = 600) as self.mainForm :
            pass




def show():
    try :
        cmds.delete (joint_tool)
    except :
        pass
    joint_tool = Joint_Tool ()


if __name__ == '__main__' :

    Tool = Joint_Tool ()


    if workspaceControl (Tool.win_title , exists = True) :
        workspaceControl (Tool.win_title , edit = True , close = True)

    workspaceControl (Tool.win_title , retain = False , floating = True , uiScript = 'Tool.init_UI()')
