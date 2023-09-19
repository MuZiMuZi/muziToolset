# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Names_Tool.ui'
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
        MainWindow.resize(355, 500)
        MainWindow.setSizeIncrement(QSize(300, 700))
        MainWindow.setContextMenuPolicy(Qt.NoContextMenu)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMaximumSize(QSize(743, 706))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label.setTextFormat(Qt.PlainText)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label.setWordWrap(False)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.prefix_lineEdit = QLineEdit(self.centralwidget)
        self.prefix_lineEdit.setObjectName(u"prefix_lineEdit")

        self.gridLayout.addWidget(self.prefix_lineEdit, 1, 1, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.subfix_lineEdit = QLineEdit(self.centralwidget)
        self.subfix_lineEdit.setObjectName(u"subfix_lineEdit")

        self.gridLayout.addWidget(self.subfix_lineEdit, 2, 1, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"color: rgb(255, 255, 0);")
        self.label_6.setTextFormat(Qt.PlainText)
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_6.setWordWrap(False)

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 2)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.search_lineEdit = QLineEdit(self.centralwidget)
        self.search_lineEdit.setObjectName(u"search_lineEdit")

        self.gridLayout.addWidget(self.search_lineEdit, 4, 1, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.replace_lineEdit = QLineEdit(self.centralwidget)
        self.replace_lineEdit.setObjectName(u"replace_lineEdit")

        self.gridLayout.addWidget(self.replace_lineEdit, 5, 1, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"color: rgb(85, 255, 127);")
        self.label_8.setTextFormat(Qt.PlainText)
        self.label_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_8.setWordWrap(False)

        self.gridLayout.addWidget(self.label_8, 6, 0, 1, 2)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)

        self.rename_lineEdit = QLineEdit(self.centralwidget)
        self.rename_lineEdit.setObjectName(u"rename_lineEdit")

        self.gridLayout.addWidget(self.rename_lineEdit, 7, 1, 1, 1)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.selectied_button = QRadioButton(self.splitter)
        self.selectied_button.setObjectName(u"selectied_button")
        self.selectied_button.setAcceptDrops(False)
        self.selectied_button.setChecked(True)
        self.splitter.addWidget(self.selectied_button)
        self.hierarchy_button = QRadioButton(self.splitter)
        self.hierarchy_button.setObjectName(u"hierarchy_button")
        self.splitter.addWidget(self.hierarchy_button)
        self.all_button = QRadioButton(self.splitter)
        self.all_button.setObjectName(u"all_button")
        self.splitter.addWidget(self.all_button)

        self.gridLayout.addWidget(self.splitter, 8, 0, 1, 2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 170, 255);")

        self.gridLayout.addWidget(self.pushButton, 9, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 355, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Names_Tool\uff08\u547d\u540d\u5de5\u5177\uff09", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u524d\u7f00\u540e\u7f00----------------------------------------", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Prefix\uff08\u524d\u7f00\uff09:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Subfix\uff08\u540e\u7f00\uff09:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u66ff\u6362----------------------------------------", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Search\uff08\u641c\u7d22\uff09:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Replace\uff08\u66ff\u6362\uff09:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u547d\u540d----------------------------------------", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Rename\uff08\u91cd\u547d\u540d\uff09:", None))
        self.selectied_button.setText(QCoreApplication.translate("MainWindow", u"Selectied(\u9009\u62e9)", None))
        self.hierarchy_button.setText(QCoreApplication.translate("MainWindow", u"Hierarchy\uff08\u5c42\u7ea7\uff09", None))
        self.all_button.setText(QCoreApplication.translate("MainWindow", u"All\uff08\u5168\u90e8\uff09", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Execute(\u6267\u884c)", None))
    # retranslateUi

