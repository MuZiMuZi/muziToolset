from __future__ import unicode_literals,print_function
import sys
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from importlib import reload
from ..core import pipelineUtils

class Test_main(QtWidgets.QWidget):
    def __init__(self,parent = None):
        super(Test_main,self).__init__(parent)
        button = QtWidgets.QPushButton('ceshi',parent = self)



def show():
    return  Test_main()