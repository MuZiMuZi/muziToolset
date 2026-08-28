# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chainEP_ui.ui'
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
        MainWindow.resize(800, 730)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
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
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 5, 0, 1, 1)

        self.select_btn = QPushButton(self.widget)
        self.select_btn.setObjectName(u"select_btn")

        self.gridLayout_2.addWidget(self.select_btn, 6, 2, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)

        self.jnt_number_sbox = QSpinBox(self.widget)
        self.jnt_number_sbox.setObjectName(u"jnt_number_sbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.jnt_number_sbox.sizePolicy().hasHeightForWidth())
        self.jnt_number_sbox.setSizePolicy(sizePolicy1)
        self.jnt_number_sbox.setFont(font)
        self.jnt_number_sbox.setValue(1)

        self.gridLayout_2.addWidget(self.jnt_number_sbox, 3, 1, 1, 1)

        self.jnt_parent_edit = QLineEdit(self.widget)
        self.jnt_parent_edit.setObjectName(u"jnt_parent_edit")
        sizePolicy1.setHeightForWidth(self.jnt_parent_edit.sizePolicy().hasHeightForWidth())
        self.jnt_parent_edit.setSizePolicy(sizePolicy1)
        self.jnt_parent_edit.setFont(font)

        self.gridLayout_2.addWidget(self.jnt_parent_edit, 7, 1, 1, 1)

        self.delete_btn = QPushButton(self.widget)
        self.delete_btn.setObjectName(u"delete_btn")
        sizePolicy1.setHeightForWidth(self.delete_btn.sizePolicy().hasHeightForWidth())
        self.delete_btn.setSizePolicy(sizePolicy1)
        self.delete_btn.setFont(font)

        self.gridLayout_2.addWidget(self.delete_btn, 9, 1, 1, 1)

        self.side_label = QLabel(self.widget)
        self.side_label.setObjectName(u"side_label")
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

        self.gridLayout_2.addWidget(self.side_label, 1, 0, 1, 1)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setFont(font1)

        self.gridLayout_2.addWidget(self.label_7, 8, 0, 1, 1)

        self.curve_edit = QLineEdit(self.widget)
        self.curve_edit.setObjectName(u"curve_edit")

        self.gridLayout_2.addWidget(self.curve_edit, 6, 1, 1, 1)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setFont(font1)

        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setFont(font1)

        self.gridLayout_2.addWidget(self.label_6, 7, 0, 1, 1)

        self.name_edit = QLineEdit(self.widget)
        self.name_edit.setObjectName(u"name_edit")
        sizePolicy1.setHeightForWidth(self.name_edit.sizePolicy().hasHeightForWidth())
        self.name_edit.setSizePolicy(sizePolicy1)
        self.name_edit.setFont(font)

        self.gridLayout_2.addWidget(self.name_edit, 2, 1, 1, 1)

        self.control_parent_edit = QLineEdit(self.widget)
        self.control_parent_edit.setObjectName(u"control_parent_edit")
        sizePolicy1.setHeightForWidth(self.control_parent_edit.sizePolicy().hasHeightForWidth())
        self.control_parent_edit.setSizePolicy(sizePolicy1)
        self.control_parent_edit.setFont(font)

        self.gridLayout_2.addWidget(self.control_parent_edit, 8, 1, 1, 1)

        self.direction_cbox = QComboBox(self.widget)
        self.direction_cbox.setObjectName(u"direction_cbox")

        self.gridLayout_2.addWidget(self.direction_cbox, 5, 1, 1, 1)

        self.length_sbox = QDoubleSpinBox(self.widget)
        self.length_sbox.setObjectName(u"length_sbox")
        self.length_sbox.setDecimals(2)
        self.length_sbox.setValue(5.000000000000000)

        self.gridLayout_2.addWidget(self.length_sbox, 4, 1, 1, 1)

        self.side_cbox = QComboBox(self.widget)
        self.side_cbox.setObjectName(u"side_cbox")
        sizePolicy1.setHeightForWidth(self.side_cbox.sizePolicy().hasHeightForWidth())
        self.side_cbox.setSizePolicy(sizePolicy1)
        self.side_cbox.setFont(font1)

        self.gridLayout_2.addWidget(self.side_cbox, 1, 1, 1, 1)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setFont(font1)

        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 6, 0, 1, 1)

        self.create_btn = QPushButton(self.widget)
        self.create_btn.setObjectName(u"create_btn")
        sizePolicy1.setHeightForWidth(self.create_btn.sizePolicy().hasHeightForWidth())
        self.create_btn.setSizePolicy(sizePolicy1)
        self.create_btn.setFont(font)

        self.gridLayout_2.addWidget(self.create_btn, 9, 0, 1, 1)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)

        self.module_edit = QLineEdit(self.widget)
        self.module_edit.setObjectName(u"module_edit")
        self.module_edit.setEnabled(False)

        self.gridLayout_2.addWidget(self.module_edit, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"direction:", None))
        self.select_btn.setText(QCoreApplication.translate("MainWindow", u"select", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"length\uff1a", None))
        self.delete_btn.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u5b9a\u4f4d", None))
        self.side_label.setText(QCoreApplication.translate("MainWindow", u"side\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"control_parent\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"name\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"jnt_parent\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"jnt_number\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"curve:", None))
        self.create_btn.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u5b9a\u4f4d", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"module_label", None))
    # retranslateUi

