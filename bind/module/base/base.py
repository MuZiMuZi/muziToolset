# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals , print_function


try :
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import QUiLoader
    from PySide2 import __version__
    from shiboken2 import wrapInstance

except ImportError :
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtWidgets import *
    from PySide import __version__
    from shiboken import wrapInstance
from importlib import reload
from . import bone
from ....bind import config


reload (bone)
reload (config)


class Base (bone.Bone) :
    u"""
    基础的关节和控制器绑定，继承于bone
    """
    # 生成的绑定类型
    rigType = 'Base'


    def __init__ (self , side , name , jnt_number , jnt_parent = None , ctrl_parent = None) :
        super ().__init__ (side , name , jnt_number , jnt_parent , ctrl_parent)
