import maya.cmds as cmds
import maya.mel as mel
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import sys


def get_maya_window () :
    u'''
    获取maya的主窗口，判断python的版本号，如果大于3的话就使用int
    :return:
    '''
    # c++的指针概念，获取maya的窗口对象
    pointer = omui.MQtUtil.mainWindow ()
    # 判断python的版本号，如果大于3的话就使用int
    if sys.version_info.major >= 3 :
        return wrapInstance (int (pointer) , QWidget)
    else :
        return wrapInstance (long (pointer) , QWidget)


class shape_Tool (QDialog) :
    """
    计算修型形状的类
    """


    def __init__ (self , parent = get_maya_window ()) :
        super (shape_Tool , self).__init__ (parent)
        # 设置窗口标题
        self.setWindowTitle ("shape_Tool")
        self.setMinimumWidth (300)

        # 创建小部件、布局和连接
        self.create_widgets ()
        self.create_layouts ()
        self.create_connections ()


    def create_widgets (self) :
        # 创建蒙皮权重模型的小部件
        self.skin_modle_label = QLabel ("蒙皮权重模型:")
        self.skin_modle_line = QLineEdit ()
        self.skin_modle_line.setReadOnly (True)
        self.skin_modle_btn = QPushButton ('拾取')

        # 创建修型模型的小部件
        self.bs_modle_label = QLabel ("修型模型:")
        self.bs_modle_line = QLineEdit ()
        self.bs_modle_line.setReadOnly (True)
        self.bs_modle_btn = QPushButton ('拾取')

        # 创建执行计算命令的小部件
        self.click_btn = QPushButton ('计算修型形状')


    def create_layouts (self) :
        # 创建蒙皮权重页面布局
        self.skin_modle_layout = QHBoxLayout ()
        self.skin_modle_layout.addWidget (self.skin_modle_label)
        self.skin_modle_layout.addWidget (self.skin_modle_line)
        self.skin_modle_layout.addWidget (self.skin_modle_btn)

        # 创建修型页面布局
        self.bs_modle_layout = QHBoxLayout ()
        self.bs_modle_layout.addWidget (self.bs_modle_label)
        self.bs_modle_layout.addWidget (self.bs_modle_line)
        self.bs_modle_layout.addWidget (self.bs_modle_btn)

        # 创建主页面的布局
        # 设置标签布局
        self.main_layout = QVBoxLayout (self)
        self.main_layout.addLayout (self.skin_modle_layout)
        self.main_layout.addStretch ()
        self.main_layout.addLayout (self.bs_modle_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.click_btn)


    def create_connections (self) :
        self.skin_modle_btn.clicked.connect (self.clicked_skin_modle_btn)
        self.bs_modle_btn.clicked.connect (self.clicked_bs_modle_btn)
        self.click_btn.clicked.connect(self.clicked_click_btn)

    def clicked_skin_modle_btn (self) :
        # 连接获取权重模型的按钮的槽函数
        self.skin_modle = cmds.ls (sl = True) [0]
        self.skin_modle_line.setText ('{}'.format(self.skin_modle))


    def clicked_bs_modle_btn (self) :
        # 连接获取修型模型的按钮的槽函数
        #清空原有的输入栏输入
        self.bs_modle_line.clear()
        #对选择的修型模型做循环，添加进入输入栏内
        self.bs_modles = cmds.ls (sl = True)
        for bs_modle in self.bs_modles:
            self.bs_modle_line.insert ('{},'.format (bs_modle))

    def clicked_click_btn(self):
        "连接计算修型形状的槽函数"
        self.skin_modle = self.skin_modle_line.text()
        bs_modles_list = self.bs_modle_line.text()

        # 判断输入框上是否有符合的对象，没有的话则报错
        if not self.skin_modle :
            cmds.warning ("未加载权重模型，请重新选择权重模型加载")
            return
        if not bs_modles_list :
            cmds.warning ("未加载需要计算的修型模型。请重新选择修型模型进行加载")
            return

        self.bs_modles = bs_modles_list.split (',')
        for bs_modle in self.bs_modles :
            invert_shape = cmds.invertShape(self.skin_modle, bs_modle)
            cmds.rename(invert_shape, bs_modle + '_invert_geo')


if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = shape_Tool ()  # 创建实例
    window.show ()  # 显示窗口
