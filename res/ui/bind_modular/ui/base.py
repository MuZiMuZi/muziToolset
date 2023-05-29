# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'base.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.formLayout_2 = QFormLayout(self.centralwidget)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Arial Narrow")
        font.setPointSize(16)
        self.widget.setFont(font)
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.side_label = QLabel(self.widget)
        self.side_label.setObjectName(u"side_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.side_label.sizePolicy().hasHeightForWidth())
        self.side_label.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamily(u"Arial Narrow")
        font1.setPointSize(16)
        font1.setBold(False)
        font1.setWeight(50)
        self.side_label.setFont(font1)
        self.side_label.setFocusPolicy(Qt.NoFocus)
        self.side_label.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.side_label.setLayoutDirection(Qt.LeftToRight)
        self.side_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.side_label)

        self.side_cbox = QComboBox(self.widget)
        self.side_cbox.addItem("")
        self.side_cbox.addItem("")
        self.side_cbox.addItem("")
        self.side_cbox.setObjectName(u"side_cbox")
        sizePolicy1.setHeightForWidth(self.side_cbox.sizePolicy().hasHeightForWidth())
        self.side_cbox.setSizePolicy(sizePolicy1)
        self.side_cbox.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.side_cbox)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.name_edit = QLineEdit(self.widget)
        self.name_edit.setObjectName(u"name_edit")
        sizePolicy1.setHeightForWidth(self.name_edit.sizePolicy().hasHeightForWidth())
        self.name_edit.setSizePolicy(sizePolicy1)
        self.name_edit.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.name_edit)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setFont(font1)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setFont(font1)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.jnt_parent_edit = QLineEdit(self.widget)
        self.jnt_parent_edit.setObjectName(u"jnt_parent_edit")
        sizePolicy1.setHeightForWidth(self.jnt_parent_edit.sizePolicy().hasHeightForWidth())
        self.jnt_parent_edit.setSizePolicy(sizePolicy1)
        self.jnt_parent_edit.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.jnt_parent_edit)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setFont(font1)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_7)

        self.control_parent_edit = QLineEdit(self.widget)
        self.control_parent_edit.setObjectName(u"control_parent_edit")
        sizePolicy1.setHeightForWidth(self.control_parent_edit.sizePolicy().hasHeightForWidth())
        self.control_parent_edit.setSizePolicy(sizePolicy1)
        self.control_parent_edit.setFont(font)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.control_parent_edit)

        self.create_btn = QPushButton(self.widget)
        self.create_btn.setObjectName(u"create_btn")
        sizePolicy1.setHeightForWidth(self.create_btn.sizePolicy().hasHeightForWidth())
        self.create_btn.setSizePolicy(sizePolicy1)
        self.create_btn.setFont(font)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.create_btn)

        self.delete_btn = QPushButton(self.widget)
        self.delete_btn.setObjectName(u"delete_btn")
        sizePolicy1.setHeightForWidth(self.delete_btn.sizePolicy().hasHeightForWidth())
        self.delete_btn.setSizePolicy(sizePolicy1)
        self.delete_btn.setFont(font)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.delete_btn)

        self.jnt_number_sbox = QSpinBox(self.widget)
        self.jnt_number_sbox.setObjectName(u"jnt_number_sbox")
        sizePolicy1.setHeightForWidth(self.jnt_number_sbox.sizePolicy().hasHeightForWidth())
        self.jnt_number_sbox.setSizePolicy(sizePolicy1)
        self.jnt_number_sbox.setFont(font)
        self.jnt_number_sbox.setValue(1)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.jnt_number_sbox)


        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.side_label.setText(QCoreApplication.translate("MainWindow", u"side", None))
        self.side_cbox.setItemText(0, QCoreApplication.translate("MainWindow", u"m", None))
        self.side_cbox.setItemText(1, QCoreApplication.translate("MainWindow", u"l", None))
        self.side_cbox.setItemText(2, QCoreApplication.translate("MainWindow", u"r", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"name", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"jnt_number", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"jnt_parent", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"control_parent", None))
        self.create_btn.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa", None))
        self.delete_btn.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
    # retranslateUi

