# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'limb_ui.ui'
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

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.length_label = QLabel(self.centralwidget)
        self.length_label.setObjectName(u"length_label")
        sizePolicy.setHeightForWidth(self.length_label.sizePolicy().hasHeightForWidth())
        self.length_label.setSizePolicy(sizePolicy)
        self.length_label.setFont(font3)

        self.horizontalLayout_12.addWidget(self.length_label)

        self.length_sbox = QDoubleSpinBox(self.centralwidget)
        self.length_sbox.setObjectName(u"length_sbox")
        sizePolicy.setHeightForWidth(self.length_sbox.sizePolicy().hasHeightForWidth())
        self.length_sbox.setSizePolicy(sizePolicy)
        self.length_sbox.setValue(10.000000000000000)

        self.horizontalLayout_12.addWidget(self.length_sbox)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.direction_label = QLabel(self.centralwidget)
        self.direction_label.setObjectName(u"direction_label")
        sizePolicy.setHeightForWidth(self.direction_label.sizePolicy().hasHeightForWidth())
        self.direction_label.setSizePolicy(sizePolicy)
        self.direction_label.setFont(font3)

        self.horizontalLayout_10.addWidget(self.direction_label)

        self.direction_cbox = QComboBox(self.centralwidget)
        self.direction_cbox.setObjectName(u"direction_cbox")
        sizePolicy.setHeightForWidth(self.direction_cbox.sizePolicy().hasHeightForWidth())
        self.direction_cbox.setSizePolicy(sizePolicy)
        self.direction_cbox.setFont(font3)

        self.horizontalLayout_10.addWidget(self.direction_cbox)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

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

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.ikCtrl_label = QLabel(self.centralwidget)
        self.ikCtrl_label.setObjectName(u"ikCtrl_label")
        sizePolicy.setHeightForWidth(self.ikCtrl_label.sizePolicy().hasHeightForWidth())
        self.ikCtrl_label.setSizePolicy(sizePolicy)
        self.ikCtrl_label.setFont(font3)

        self.horizontalLayout_11.addWidget(self.ikCtrl_label)

        self.ikCtrl_cbox = QCheckBox(self.centralwidget)
        self.ikCtrl_cbox.setObjectName(u"ikCtrl_cbox")
        sizePolicy.setHeightForWidth(self.ikCtrl_cbox.sizePolicy().hasHeightForWidth())
        self.ikCtrl_cbox.setSizePolicy(sizePolicy)
        self.ikCtrl_cbox.setFont(font3)
        self.ikCtrl_cbox.setChecked(True)

        self.horizontalLayout_11.addWidget(self.ikCtrl_cbox)

        self.fkCtrl_label = QLabel(self.centralwidget)
        self.fkCtrl_label.setObjectName(u"fkCtrl_label")
        sizePolicy.setHeightForWidth(self.fkCtrl_label.sizePolicy().hasHeightForWidth())
        self.fkCtrl_label.setSizePolicy(sizePolicy)
        self.fkCtrl_label.setFont(font3)

        self.horizontalLayout_11.addWidget(self.fkCtrl_label)

        self.fkCtrl_cbox = QCheckBox(self.centralwidget)
        self.fkCtrl_cbox.setObjectName(u"fkCtrl_cbox")
        sizePolicy.setHeightForWidth(self.fkCtrl_cbox.sizePolicy().hasHeightForWidth())
        self.fkCtrl_cbox.setSizePolicy(sizePolicy)
        self.fkCtrl_cbox.setFont(font3)
        self.fkCtrl_cbox.setChecked(True)

        self.horizontalLayout_11.addWidget(self.fkCtrl_cbox)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.stretch_label = QLabel(self.centralwidget)
        self.stretch_label.setObjectName(u"stretch_label")
        sizePolicy.setHeightForWidth(self.stretch_label.sizePolicy().hasHeightForWidth())
        self.stretch_label.setSizePolicy(sizePolicy)
        self.stretch_label.setFont(font3)

        self.horizontalLayout_9.addWidget(self.stretch_label)

        self.stretch_cbox = QCheckBox(self.centralwidget)
        self.stretch_cbox.setObjectName(u"stretch_cbox")
        sizePolicy.setHeightForWidth(self.stretch_cbox.sizePolicy().hasHeightForWidth())
        self.stretch_cbox.setSizePolicy(sizePolicy)
        self.stretch_cbox.setFont(font3)
        self.stretch_cbox.setChecked(True)

        self.horizontalLayout_9.addWidget(self.stretch_cbox)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ribbon_label = QLabel(self.centralwidget)
        self.ribbon_label.setObjectName(u"ribbon_label")
        sizePolicy.setHeightForWidth(self.ribbon_label.sizePolicy().hasHeightForWidth())
        self.ribbon_label.setSizePolicy(sizePolicy)
        self.ribbon_label.setFont(font3)

        self.horizontalLayout_4.addWidget(self.ribbon_label)

        self.up_ribbon_sbox = QSpinBox(self.centralwidget)
        self.up_ribbon_sbox.setObjectName(u"up_ribbon_sbox")
        sizePolicy.setHeightForWidth(self.up_ribbon_sbox.sizePolicy().hasHeightForWidth())
        self.up_ribbon_sbox.setSizePolicy(sizePolicy)
        self.up_ribbon_sbox.setFont(font3)
        self.up_ribbon_sbox.setMinimum(1)
        self.up_ribbon_sbox.setValue(5)

        self.horizontalLayout_4.addWidget(self.up_ribbon_sbox)

        self.down_ribbon_sbox = QSpinBox(self.centralwidget)
        self.down_ribbon_sbox.setObjectName(u"down_ribbon_sbox")
        sizePolicy.setHeightForWidth(self.down_ribbon_sbox.sizePolicy().hasHeightForWidth())
        self.down_ribbon_sbox.setSizePolicy(sizePolicy)
        self.down_ribbon_sbox.setFont(font3)
        self.down_ribbon_sbox.setMinimum(1)
        self.down_ribbon_sbox.setValue(5)

        self.horizontalLayout_4.addWidget(self.down_ribbon_sbox)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.create_btn = QToolButton(self.centralwidget)
        self.create_btn.setObjectName(u"create_btn")
        self.create_btn.setEnabled(True)
        self.create_btn.setFont(font4)
        self.create_btn.setIconSize(QSize(40, 40))

        self.horizontalLayout_7.addWidget(self.create_btn)

        self.delete_btn = QToolButton(self.centralwidget)
        self.delete_btn.setObjectName(u"delete_btn")
        self.delete_btn.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
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
        self.length_label.setText(QCoreApplication.translate("MainWindow", u"length:", None))
        self.direction_label.setText(QCoreApplication.translate("MainWindow", u"direction:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"jnt_parent\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"ctrl_parent\uff1a", None))
        self.ikCtrl_label.setText(QCoreApplication.translate("MainWindow", u"ikCtrl:", None))
        self.ikCtrl_cbox.setText("")
        self.fkCtrl_label.setText(QCoreApplication.translate("MainWindow", u"fkCtrl:", None))
        self.stretch_label.setText(QCoreApplication.translate("MainWindow", u"stretch:", None))
        self.stretch_cbox.setText("")
        self.ribbon_label.setText(QCoreApplication.translate("MainWindow", u"ribbon:", None))
        self.create_btn.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.delete_btn.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
    # retranslateUi

