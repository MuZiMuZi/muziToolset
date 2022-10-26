# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals, print_function
"""
这是一个批量创建常用节点的类，根据指定的数量和名称批量创建指定的常用节点


"""
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtWidgets import *
    from PySide import __version__
    from shiboken import wrapInstance

import maya.cmds as cmds


import muziToolset.res.ui.backGround as backGround

class NodeWidget(backGround.BackGround):
    def __init__(self,parent = None):
        super(NodeWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 创建主页面布局
        self.main_layout = QVBoxLayout(self)
        self.setWindowTitle(u'节点创建工具')
        self.resize(300, 300)
        # 创建常用节点页面布局
        self.node_layout = QGridLayout(self)
        self.node_layout.addWidget(QLabel("创建常用节点:    "))

        # 创建常用节点页面布局的小部件
        self.transform_bn = QPushButton("空组_transform")
        self.joint_bn = QPushButton("关节_joint")
        self.loc_bn = QPushButton("定位器_locator")
        self.transform_bn.clicked.connect(lambda: self.create(self.transform_bn))
        self.joint_bn.clicked.connect(lambda: self.create(self.joint_bn))
        self.loc_bn.clicked.connect(self.create_locator)

        # 添加常用节点页面布局的小部件
        self.node_layout.addWidget(self.transform_bn)
        self.node_layout.addWidget(self.joint_bn,1,1)
        self.node_layout.addWidget(self.loc_bn, 1, 2)

        # 创建数学节点页面布局
        self.math_node_layout = QGridLayout(self)
        self.math_node_layout.addWidget(QLabel("创建数学节点:    "))

        # 创建数学节点页面的小部件
        self.add_node_bn = QPushButton("加减节点_addDoubleLinear")
        self.add_node_bn.clicked.connect(lambda: self.create(self.add_node_bn))


        self.mult_node_bn = QPushButton("乘除节点_multDoubleLinear")
        self.mult_node_bn.clicked.connect(lambda: self.create(self.mult_node_bn))


        self.plusMi_node_bn = QPushButton("加减平均节点_plusMinusAverage")
        self.plusMi_node_bn.clicked.connect(lambda: self.create(self.plusMi_node_bn))

        self.multDiv_node_bn = QPushButton("乘除平均节点_multiplyDivide")
        self.multDiv_node_bn.clicked.connect(lambda: self.create(self.multDiv_node_bn))

        self.dis_node_bn = QPushButton("距离节点_distanceBetween")
        self.dis_node_bn.clicked.connect(lambda: self.create(self.dis_node_bn))


        # 添加数学节点页面的小部件
        self.math_node_layout.addWidget(self.add_node_bn,1,0)
        self.math_node_layout.addWidget(self.plusMi_node_bn,1,1)
        self.math_node_layout.addWidget(self.mult_node_bn,2,0)
        self.math_node_layout.addWidget(self.multDiv_node_bn,2,1)
        self.math_node_layout.addWidget(self.dis_node_bn,1,4)



        # 创建流程节点页面布局
        self.process_node_layout = QGridLayout(self)
        self.process_node_layout.addWidget(QLabel("创建流程节点:    "))


        # 创建流程节点页面小部件
        self.cond_bn = QPushButton("判断节点_condition")
        self.cond_bn.clicked.connect(lambda: self.create(self.cond_bn))

        self.blend_bn = QPushButton("混合颜色节点_blendColors")
        self.blend_bn.clicked.connect(lambda: self.create(self.blend_bn))

        self.clamp_bn = QPushButton("切割节点_clamp")
        self.clamp_bn.clicked.connect(lambda: self.create(self.clamp_bn))

        self.reverse_bn = QPushButton("反转节点_reverse")
        self.reverse_bn.clicked.connect(lambda: self.create(self.reverse_bn))

        self.remap_bn = QPushButton("重新映射节点_remapValue")
        self.remap_bn.clicked.connect(lambda: self.create(self.remap_bn))

        self.set_bn = QPushButton("设置范围节点_setRange")
        self.set_bn.clicked.connect(lambda: self.create(self.set_bn))


        # 添加流程节点页面的小部件
        self.process_node_layout.addWidget(self.cond_bn,1,0)
        self.process_node_layout.addWidget(self.blend_bn,1,1)
        self.process_node_layout.addWidget(self.clamp_bn,1,2)

        self.process_node_layout.addWidget(self.reverse_bn,2,0)
        self.process_node_layout.addWidget(self.remap_bn,2,1)
        self.process_node_layout.addWidget(self.set_bn, 2, 2)




        # 创建预设页面布局
        self.preset_layout = QVBoxLayout(self)
        self.preset_layout.addWidget(QLabel("预设 ：  "))


        # 创建预设页面布局的小部件
        self.node_eum = QSpinBox()
        self.node_eum.setRange(1, 999)
        self.node_name = QLineEdit()


        # 添加预设页面布局的小部件
        self.preset_layout.addWidget(QLabel("节点个数: "))
        self.preset_layout.addWidget(self.node_eum)

        self.preset_layout.addWidget(QLabel("名称: "))
        self.preset_layout.addWidget(self.node_name)
        self.preset_layout.addStretch(0)

        # 添加主页面布局的小部件
        self.main_layout.addLayout(self.node_layout)
        self.main_layout.addLayout(self.math_node_layout)
        self.main_layout.addLayout(self.process_node_layout)
        self.main_layout.addLayout(self.preset_layout)


    def create(self,type):
        node_type = type.text().split("_")[-1]
        node_eum = self.node_eum.value()
        for i in range(node_eum):
            if self.node_name.text():
                node_name = self.node_name.text()
                cmds.createNode(node_type, name=node_name)
            else:
                cmds.createNode(node_type)

    def create_locator(self):
        node_eum = self.node_eum.value()
        for i in range(node_eum):
            if self.node_name.text():
                node_name = self.node_name.text()
                cmds.spaceLocator(name=node_name)
            else:
                cmds.spaceLocator()

window = None

def show():
    global window
    if window is None:
        window = NodeWidget()
    window.show()
