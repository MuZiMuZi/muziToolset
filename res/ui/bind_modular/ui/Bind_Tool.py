# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Bind_Tool.ui'
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
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(114, 32, 564, 467))
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(self.layoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 273, 210))
        self.layoutWidget1 = QWidget(self.scrollAreaWidgetContents)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(9, 1, 258, 225))
        self.verticalLayout = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.pushButton_7 = QPushButton(self.layoutWidget1)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout_4.addWidget(self.pushButton_7)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.components_widget = QListWidget(self.layoutWidget1)
        self.components_widget.setObjectName(u"components_widget")

        self.verticalLayout.addWidget(self.components_widget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        self.scrollArea_2 = QScrollArea(self.layoutWidget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 273, 210))
        self.layoutWidget2 = QWidget(self.scrollAreaWidgetContents_2)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(9, 9, 258, 225))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.layoutWidget2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.pushButton_6 = QPushButton(self.layoutWidget2)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_3.addWidget(self.pushButton_6)

        self.pushButton_5 = QPushButton(self.layoutWidget2)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_3.addWidget(self.pushButton_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.templates_widget = QListWidget(self.layoutWidget2)
        self.templates_widget.setObjectName(u"templates_widget")

        self.verticalLayout_2.addWidget(self.templates_widget)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_3.addWidget(self.scrollArea_2)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.scrollArea_3 = QScrollArea(self.layoutWidget)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 275, 430))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.pushButton_8 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_5.addWidget(self.pushButton_8)

        self.pushButton_9 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout_5.addWidget(self.pushButton_9)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.setting_widget = QTreeWidget(self.scrollAreaWidgetContents_3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.setting_widget.setHeaderItem(__qtreewidgetitem)
        self.setting_widget.setObjectName(u"setting_widget")

        self.verticalLayout_4.addWidget(self.setting_widget)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.horizontalLayout.addWidget(self.scrollArea_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.bpjnt_btn = QPushButton(self.layoutWidget)
        self.bpjnt_btn.setObjectName(u"bpjnt_btn")

        self.horizontalLayout_2.addWidget(self.bpjnt_btn)

        self.jnt_btn = QPushButton(self.layoutWidget)
        self.jnt_btn.setObjectName(u"jnt_btn")

        self.horizontalLayout_2.addWidget(self.jnt_btn)

        self.build_btn = QPushButton(self.layoutWidget)
        self.build_btn.setObjectName(u"build_btn")

        self.horizontalLayout_2.addWidget(self.build_btn)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

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
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Components", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Templates", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u83dc\u5355", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u83dc\u5355", None))
        self.bpjnt_btn.setText(QCoreApplication.translate("MainWindow", u" Bpjnt", None))
        self.jnt_btn.setText(QCoreApplication.translate("MainWindow", u"Jnt", None))
        self.build_btn.setText(QCoreApplication.translate("MainWindow", u"Build", None))
    # retranslateUi

