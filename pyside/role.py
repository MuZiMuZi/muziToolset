# -*- coding:utf-8 -*-
from PyQt6.QtWidgets import (QApplication , QWidget , QPushButton , QMessageBox , QVBoxLayout ,
                             QComboBox , QRadioButton , QGroupBox)
from PyQt6.QtCore import Qt
import sys
from enum import IntEnum


class Country_Type (IntEnum) :  # 1
    """定义三种类型的国家枚举值"""
    Country_Type_Large = 10000
    Country_Type_Middle = 10001
    Country_Type_Small = 10002


class MyWidget (QWidget) :

    def __init__ (self) :
        super ().__init__ ()
        self.initUi ()


    def initUi (self) :
        self.setWindowTitle ('自定义Role角色')
        self.resize (260 , 120)
        self.hlayout = QVBoxLayout ()
        self.setLayout (self.hlayout)
        self.group = QGroupBox ("数据角色")
        self.rbtn1 = QRadioButton ('UserRole')
        self.rbtn1.setChecked (True)
        self.rbtn2 = QRadioButton ('UserRole+1')
        self.rbtn3 = QRadioButton ('UserRole+2')
        self.rbtn4 = QRadioButton ("UserRole+3")
        self.vlayout = QVBoxLayout ()
        self.vlayout.addWidget (self.rbtn1)
        self.vlayout.addWidget (self.rbtn2)
        self.vlayout.addWidget (self.rbtn3)
        self.vlayout.addWidget (self.rbtn4)
        self.group.setLayout (self.vlayout)
        self.hlayout.addWidget (self.group)

        self.comb = QComboBox ()
        self.hlayout.addWidget (self.comb)

        # 插入text
        self.comb.addItem ('中国')  # 单个插入Item
        self.comb.addItems (['美国' , '俄罗斯' , '伊朗' , '沙特' , '日本' , '乌克兰' , '韩国' , '韩鲜'])  # 指量插入Item

        # 设置用户数据。这一部分是在界面上不显示出来的附加数据。这里的角色是自定义的Qt.UserRole+1等不同类型。

        self.comb.setItemData (0 , Country_Type.Country_Type_Large.value , Qt.UserRole + 1)  # 2
        self.comb.setItemData (1 , Country_Type.Country_Type_Large.value , Qt.UserRole + 1)
        self.comb.setItemData (2 , Country_Type.Country_Type_Large.value , Qt.UserRole + 1)

        self.comb.setItemData (3 , Country_Type.Country_Type_Middle.value , Qt.UserRole + 2)  # 3
        self.comb.setItemData (4 , Country_Type.Country_Type_Middle.value , Qt.UserRole + 2)

        self.comb.setItemData (5 , Country_Type.Country_Type_Small.value , Qt.UserRole + 3)  # 4
        self.comb.setItemData (6 , Country_Type.Country_Type_Small.value , Qt.UserRole + 3)

        self.comb.setItemData (7 , Country_Type.Country_Type_Small.value , Qt.UserRole)  # 5
        self.comb.setItemData (8 , Country_Type.Country_Type_Small.value)  # 6

        self.btn = QPushButton ('角色测试')
        self.btn.setMaximumWidth (120)
        self.btn.setStyleSheet ("background-color:yellow;")
        self.hlayout.addWidget (self.btn)

        self.btn.clicked.connect (self.showData)


    def showData (self) :  # 7
        """测试按钮槽函数"""
        if self.rbtn1.isChecked () :
            role = Qt.UserRole
            data = self.comb.currentData (role)
            self.showMessage (data)  # 8
        elif self.rbtn2.isChecked () :
            role = Qt.UserRole + 1
            data = self.comb.currentData (role)
            self.showMessage (data)
        elif self.rbtn3.isChecked () :
            role = Qt.UserRole + 2
            data = self.comb.currentData (role)
            self.showMessage (data)

        elif self.rbtn4.isChecked () :
            role = Qt.UserRole + 3
            data = self.comb.currentData (role)
            self.showMessage (data)


    def showMessage (self , data) :
        if data is not None :
            QMessageBox.information (self , '提示' , f'您选择的角色数据为：\n{data}' ,
                                     QMessageBox.Ok | QMessageBox.Cancel)
        else :
            QMessageBox.information (self , '提示' , '没有匹配的角色数据。' , QMessageBox.Ok | QMessageBox.Cancel)


if __name__ == "__main__" :
    app = QApplication (sys.argv)
    demo = MyWidget ()
    demo.show ()
    sys.exit (app.exec_ ())