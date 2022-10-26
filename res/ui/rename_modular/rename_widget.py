# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals, print_function

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

import muziToolset.res.ui.backGround as backGround

import  muziToolset.core.nameUtils as nameUtils

reload(nameUtils)


class AddNamePrefixWidget(backGround.BackGround):
    def __init__(self,parent = None):
        super(AddNamePrefixWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addStretch(0)

        # 创建子布局（重新命名）
        self.body_layout = QVBoxLayout(self)


        # 创建添加前缀的部件
        self.prefix = QLineEdit()
        self.prefix_bn = QPushButton("添加")
        self.prefix_bn.clicked.connect(self.add_prefix)

        # 创建添加层级前缀的部件
        self.hierarchy_prefix = QLineEdit()
        self.hierarchy_prefix_bn = QPushButton("添加")
        self.hierarchy_prefix_bn.clicked.connect(self.add_hierarchy_prefix)

        # 创建添加后缀的部件
        self.suffix = QLineEdit()
        self.suffix_bn = QPushButton("添加")
        self.suffix_bn.clicked.connect(self.add_suffix)

        # 创建添加层级后缀的部件
        self.hierarchy_suffix = QLineEdit()
        self.hierarchy_suffix_bn = QPushButton("添加")
        self.hierarchy_suffix_bn.clicked.connect(self.add_hierarchy_suffix)

        # 创建重命名的部件
        self.rename = QLineEdit()
        self.rename_bn = QPushButton("替换")
        self.rename_bn.clicked.connect(self.set_rename)

        # 添加主布局的小部件
        self.main_layout.addLayout(self.body_layout)
        self.main_layout.addStretch(0)

        # 添加子布局的小部件
        self.body_layout.addWidget(QLabel("添加前缀"))
        self.body_layout.addWidget(self.prefix)
        self.body_layout.addWidget(self.prefix_bn)

        self.body_layout.addWidget(QLabel("添加后缀"))
        self.body_layout.addWidget(self.suffix )
        self.body_layout.addWidget(self.suffix_bn)

        self.body_layout.addWidget(QLabel("添加层级前缀"))
        self.body_layout.addWidget(self.hierarchy_prefix)
        self.body_layout.addWidget(self.hierarchy_prefix_bn)

        self.body_layout.addWidget(QLabel("添加层级后缀"))
        self.body_layout.addWidget(self.hierarchy_suffix)
        self.body_layout.addWidget(self.hierarchy_suffix_bn)

        self.body_layout.addWidget(QLabel("重命名"))
        self.body_layout.addWidget(self.rename)
        self.body_layout.addWidget(self.rename_bn)

    def add_prefix(self):
        """
        用来调用添加前缀的方法
        Returns:

        """
        name = nameUtils.Name()
        name.add_prefix(self.prefix.text())

    def add_hierarchy_prefix(self):
        """
        用来调用添加层级前缀的方法
        Returns:

        """
        name = nameUtils.Name()
        name.add_hierarchy_prefix(self.hierarchy_prefix.text())

    def add_suffix(self):
        """
        用来调用添加后缀的方法
        Returns:

        """
        name = nameUtils.Name()
        name.add_suffix(self.suffix.text())

    def add_hierarchy_suffix(self):
        """
        用来调用添加层级后缀的方法
        Returns:

        """
        name = nameUtils.Name()
        name.add_hierarchy_suffix(self.hierarchy_suffix.text())

    def set_rename(self):
        """
        用来调用重命名的方法
        Returns:

        """
        name = nameUtils.Name()
        name.set_rename(self.rename.text())


class ReplaceNameWidget(backGround.BackGround):
    def __init__(self,parent = None):
        super(ReplaceNameWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        # 创建搜索子布局
        self.search_layout = QHBoxLayout()
        self.search  = QLineEdit()

        self.search_layout.addWidget(QLabel("搜索:"))
        self.search_layout.addWidget(self.search)


        # 创建替换子布局
        self.replace_layout = QHBoxLayout()

        self.replace = QLineEdit()

        self.replace_layout.addWidget(QLabel("替换:"))
        self.replace_layout.addWidget(self.replace)

        # 创建按钮布局
        self.do_bn_layout = QHBoxLayout()

        self.search_replace_bn = QPushButton("搜索替换")
        self.search_replace_bn.clicked.connect(self.search_replace_name)

        self.do_bn_layout.addWidget(self.search_replace_bn)

       # 添加主布局部件
        self.main_layout.addWidget(QLabel("搜索替换名称：  "))
        self.main_layout.addLayout(self.search_layout)
        self.main_layout.addLayout(self.replace_layout)
        self.main_layout.addLayout(self.do_bn_layout)
        self.main_layout.addStretch(0)

    def search_replace_name(self):
        """
           用来调用替换查找替换名称的方法
           Returns:

           """
        name = nameUtils.Name()
        name.search_replace_name(self.search.text(), self.replace.text())

class RenameWidget(QWidget):
    def __init__(self,parent = None):
        super(RenameWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.main_layout  = QVBoxLayout(self)
        self.setWindowTitle(u'命名工具')
        self.resize(300, 300)

        self.add_name_prefix = AddNamePrefixWidget()
        self.replace_name_widget = ReplaceNameWidget()

        self.main_layout.addWidget(self.add_name_prefix)
        self.main_layout.addWidget(self.replace_name_widget)


window = None

def show():
    global window
    if window is None:
        window = RenameWidget()
    window.show()
