# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bone_ui.ui'
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
        MainWindow.resize(580, 559)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.side_label = QLabel(self.centralwidget)
        self.side_label.setObjectName(u"side_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.side_label.sizePolicy().hasHeightForWidth())
        self.side_label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.side_label.setFont(font)
        self.side_label.setFocusPolicy(Qt.NoFocus)
        self.side_label.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.side_label.setLayoutDirection(Qt.LeftToRight)
        self.side_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.side_label)

        self.side_cbox = QComboBox(self.centralwidget)
        self.side_cbox.setObjectName(u"side_cbox")
        sizePolicy.setHeightForWidth(self.side_cbox.sizePolicy().hasHeightForWidth())
        self.side_cbox.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamily(u"Arial Narrow")
        font1.setPointSize(18)
        font1.setBold(False)
        font1.setWeight(50)
        self.side_cbox.setFont(font1)

        self.horizontalLayout_2.addWidget(self.side_cbox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(18)
        font2.setKerning(True)
        self.label.setFont(font2)
        self.label.setContextMenuPolicy(Qt.PreventContextMenu)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label)

        self.rigType_edit = QLineEdit(self.centralwidget)
        self.rigType_edit.setObjectName(u"rigType_edit")
        self.rigType_edit.setEnabled(False)
        sizePolicy.setHeightForWidth(self.rigType_edit.sizePolicy().hasHeightForWidth())
        self.rigType_edit.setSizePolicy(sizePolicy)
        font3 = QFont()
        font3.setPointSize(18)
        self.rigType_edit.setFont(font3)

        self.horizontalLayout.addWidget(self.rigType_edit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(Qt.LeftToRight)
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.name_edit = QLineEdit(self.centralwidget)
        self.name_edit.setObjectName(u"name_edit")
        sizePolicy.setHeightForWidth(self.name_edit.sizePolicy().hasHeightForWidth())
        self.name_edit.setSizePolicy(sizePolicy)
        font4 = QFont()
        font4.setFamily(u"Arial Narrow")
        font4.setPointSize(18)
        self.name_edit.setFont(font4)

        self.horizontalLayout_3.addWidget(self.name_edit)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.index_label = QLabel(self.centralwidget)
        self.index_label.setObjectName(u"index_label")
        sizePolicy.setHeightForWidth(self.index_label.sizePolicy().hasHeightForWidth())
        self.index_label.setSizePolicy(sizePolicy)
        self.index_label.setFont(font3)

        self.horizontalLayout_8.addWidget(self.index_label)

        self.index_edit = QLineEdit(self.centralwidget)
        self.index_edit.setObjectName(u"index_edit")
        self.index_edit.setEnabled(False)
        sizePolicy.setHeightForWidth(self.index_edit.sizePolicy().hasHeightForWidth())
        self.index_edit.setSizePolicy(sizePolicy)
        self.index_edit.setFont(font3)

        self.horizontalLayout_8.addWidget(self.index_edit)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(Qt.LeftToRight)
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.jnt_number_sbox = QSpinBox(self.centralwidget)
        self.jnt_number_sbox.setObjectName(u"jnt_number_sbox")
        sizePolicy.setHeightForWidth(self.jnt_number_sbox.sizePolicy().hasHeightForWidth())
        self.jnt_number_sbox.setSizePolicy(sizePolicy)
        self.jnt_number_sbox.setFont(font4)
        self.jnt_number_sbox.setValue(1)

        self.horizontalLayout_4.addWidget(self.jnt_number_sbox)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setFont(font)
        self.label_6.setLayoutDirection(Qt.LeftToRight)
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_6)

        self.jnt_parent_edit = QLineEdit(self.centralwidget)
        self.jnt_parent_edit.setObjectName(u"jnt_parent_edit")
        sizePolicy.setHeightForWidth(self.jnt_parent_edit.sizePolicy().hasHeightForWidth())
        self.jnt_parent_edit.setSizePolicy(sizePolicy)
        self.jnt_parent_edit.setFont(font4)

        self.horizontalLayout_5.addWidget(self.jnt_parent_edit)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setFont(font)
        self.label_7.setLayoutDirection(Qt.LeftToRight)
        self.label_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_7)

        self.ctrl_parent_edit = QLineEdit(self.centralwidget)
        self.ctrl_parent_edit.setObjectName(u"ctrl_parent_edit")
        sizePolicy.setHeightForWidth(self.ctrl_parent_edit.sizePolicy().hasHeightForWidth())
        self.ctrl_parent_edit.setSizePolicy(sizePolicy)
        self.ctrl_parent_edit.setFont(font4)

        self.horizontalLayout_6.addWidget(self.ctrl_parent_edit)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.create_btn = QToolButton(self.centralwidget)
        self.create_btn.setObjectName(u"create_btn")
        self.create_btn.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.create_btn.sizePolicy().hasHeightForWidth())
        self.create_btn.setSizePolicy(sizePolicy1)
        self.create_btn.setFont(font4)
        self.create_btn.setIconSize(QSize(40, 40))

        self.horizontalLayout_7.addWidget(self.create_btn)

        self.delete_btn = QToolButton(self.centralwidget)
        self.delete_btn.setObjectName(u"delete_btn")
        self.delete_btn.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.delete_btn.sizePolicy().hasHeightForWidth())
        self.delete_btn.setSizePolicy(sizePolicy1)
        self.delete_btn.setFont(font4)
        self.delete_btn.setIconSize(QSize(40, 40))
        self.delete_btn.setChecked(False)

        self.horizontalLayout_7.addWidget(self.delete_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_7)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 580, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.side_label.setText(QCoreApplication.translate("MainWindow", u"side\uff1a", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"rigType\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"name\uff1a", None))
        self.index_label.setText(QCoreApplication.translate("MainWindow", u"index:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"jnt _number\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"jnt_parent\uff1a", None))
        self.jnt_parent_edit.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"ctrl_parent\uff1a", None))
        self.create_btn.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.delete_btn.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
    # retranslateUi

