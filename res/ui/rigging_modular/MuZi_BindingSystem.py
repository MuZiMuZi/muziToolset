# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MuZi_BindingSystem.ui'
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
        MainWindow.resize(733, 839)
        self.actionRefersh = QAction(MainWindow)
        self.actionRefersh.setObjectName(u"actionRefersh")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.proxy_layout = QVBoxLayout()
        self.proxy_layout.setObjectName(u"proxy_layout")
        self.proxy_label = QLabel(self.centralwidget)
        self.proxy_label.setObjectName(u"proxy_label")
        self.proxy_label.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.proxy_label.sizePolicy().hasHeightForWidth())
        self.proxy_label.setSizePolicy(sizePolicy)
        self.proxy_label.setSizeIncrement(QSize(0, 0))
        self.proxy_label.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.proxy_label.setLayoutDirection(Qt.LeftToRight)
        self.proxy_label.setAlignment(Qt.AlignCenter)

        self.proxy_layout.addWidget(self.proxy_label)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 207, 752))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.listView = QListView(self.scrollAreaWidgetContents)
        self.listView.setObjectName(u"listView")

        self.gridLayout_2.addWidget(self.listView, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.proxy_layout.addWidget(self.scrollArea)


        self.horizontalLayout.addLayout(self.proxy_layout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.preset_layout = QVBoxLayout()
        self.preset_layout.setObjectName(u"preset_layout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.preset_layout.addWidget(self.label)

        self.scrollArea_2 = QScrollArea(self.centralwidget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 204, 361))
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.listView_2 = QListView(self.scrollAreaWidgetContents_5)
        self.listView_2.setObjectName(u"listView_2")

        self.gridLayout_5.addWidget(self.listView_2, 0, 0, 1, 1)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_5)

        self.preset_layout.addWidget(self.scrollArea_2)


        self.verticalLayout_3.addLayout(self.preset_layout)

        self.custom_layout = QVBoxLayout()
        self.custom_layout.setObjectName(u"custom_layout")
        self.custom_label = QLabel(self.centralwidget)
        self.custom_label.setObjectName(u"custom_label")
        self.custom_label.setAlignment(Qt.AlignCenter)

        self.custom_layout.addWidget(self.custom_label)

        self.scrollArea_3 = QScrollArea(self.centralwidget)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 204, 361))
        self.gridLayout_4 = QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.listView_3 = QListView(self.scrollAreaWidgetContents_3)
        self.listView_3.setObjectName(u"listView_3")

        self.gridLayout_4.addWidget(self.listView_3, 0, 0, 1, 1)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.custom_layout.addWidget(self.scrollArea_3)


        self.verticalLayout_3.addLayout(self.custom_layout)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.setting_layout = QVBoxLayout()
        self.setting_layout.setObjectName(u"setting_layout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_3)

        self.scrollArea_5 = QScrollArea(self.centralwidget)
        self.scrollArea_5.setObjectName(u"scrollArea_5")
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName(u"scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 274, 512))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.listView_4 = QListView(self.scrollAreaWidgetContents_6)
        self.listView_4.setObjectName(u"listView_4")

        self.gridLayout_6.addWidget(self.listView_4, 0, 0, 1, 1)

        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_6)

        self.verticalLayout_4.addWidget(self.scrollArea_5)


        self.setting_layout.addLayout(self.verticalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.scrollArea_4 = QScrollArea(self.centralwidget)
        self.scrollArea_4.setObjectName(u"scrollArea_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea_4.sizePolicy().hasHeightForWidth())
        self.scrollArea_4.setSizePolicy(sizePolicy1)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 274, 210))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.radioButton_2 = QRadioButton(self.scrollAreaWidgetContents_4)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_3.addWidget(self.radioButton_2, 1, 0, 1, 1)

        self.pushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_3.addWidget(self.pushButton, 2, 0, 1, 1)

        self.radioButton = QRadioButton(self.scrollAreaWidgetContents_4)
        self.radioButton.setObjectName(u"radioButton")

        self.gridLayout_3.addWidget(self.radioButton, 0, 0, 1, 1)

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout.addWidget(self.scrollArea_4)


        self.setting_layout.addLayout(self.verticalLayout)


        self.horizontalLayout.addLayout(self.setting_layout)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 733, 23))
        self.menuWindow = QMenu(self.menubar)
        self.menuWindow.setObjectName(u"menuWindow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuWindow.menuAction())
        self.menuWindow.addAction(self.actionRefersh)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MuZi_BindingSystem", None))
        self.actionRefersh.setText(QCoreApplication.translate("MainWindow", u"refersh", None))
        self.proxy_label.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u677f\u5e93", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u9884\u8bbe", None))
        self.custom_label.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u5b9a\u4e49\u6a21\u5757", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7ed1\u5b9a\u5de5\u5177", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.menuWindow.setTitle(QCoreApplication.translate("MainWindow", u"Window", None))
    # retranslateUi

