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
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label.setTextFormat(Qt.PlainText)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label.setWordWrap(False)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.prefix_lineEdit = QLineEdit(self.centralwidget)
        self.prefix_lineEdit.setObjectName(u"prefix_lineEdit")

        self.verticalLayout.addWidget(self.prefix_lineEdit)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.subfix_lineEdit = QLineEdit(self.centralwidget)
        self.subfix_lineEdit.setObjectName(u"subfix_lineEdit")

        self.verticalLayout.addWidget(self.subfix_lineEdit)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"color: rgb(255, 255, 0);")
        self.label_6.setTextFormat(Qt.PlainText)
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_6.setWordWrap(False)

        self.verticalLayout.addWidget(self.label_6)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.search_lineEdit = QLineEdit(self.centralwidget)
        self.search_lineEdit.setObjectName(u"search_lineEdit")

        self.verticalLayout.addWidget(self.search_lineEdit)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.replace_lineEdit = QLineEdit(self.centralwidget)
        self.replace_lineEdit.setObjectName(u"replace_lineEdit")

        self.verticalLayout.addWidget(self.replace_lineEdit)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"color: rgb(85, 255, 127);")
        self.label_8.setTextFormat(Qt.PlainText)
        self.label_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_8.setWordWrap(False)

        self.verticalLayout.addWidget(self.label_8)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout.addWidget(self.label_7)

        self.rename_lineEdit = QLineEdit(self.centralwidget)
        self.rename_lineEdit.setObjectName(u"rename_lineEdit")

        self.verticalLayout.addWidget(self.rename_lineEdit)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.selectied_button = QRadioButton(self.splitter)
        self.insert_buttonGroup = QButtonGroup(MainWindow)
        self.insert_buttonGroup.setObjectName(u"insert_buttonGroup")
        self.insert_buttonGroup.addButton(self.selectied_button)
        self.selectied_button.setObjectName(u"selectied_button")
        self.selectied_button.setAcceptDrops(False)
        self.selectied_button.setChecked(True)
        self.splitter.addWidget(self.selectied_button)
        self.hierarchy_button = QRadioButton(self.splitter)
        self.insert_buttonGroup.addButton(self.hierarchy_button)
        self.hierarchy_button.setObjectName(u"hierarchy_button")
        self.splitter.addWidget(self.hierarchy_button)
        self.all_button = QRadioButton(self.splitter)
        self.insert_buttonGroup.addButton(self.all_button)
        self.all_button.setObjectName(u"all_button")
        self.splitter.addWidget(self.all_button)

        self.verticalLayout.addWidget(self.splitter)

        self.execute_button = QPushButton(self.centralwidget)
        self.execute_button.setObjectName(u"execute_button")
        self.execute_button.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 170, 255);")

        self.verticalLayout.addWidget(self.execute_button)

        self.reset_button = QPushButton(self.centralwidget)
        self.reset_button.setObjectName(u"reset_button")
        self.reset_button.setStyleSheet(u"background-color: rgb(255, 158, 255);")

        self.verticalLayout.addWidget(self.reset_button)

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
        self.execute_button.setText(QCoreApplication.translate("MainWindow", u"Execute(\u6267\u884c)", None))
        self.reset_button.setText(QCoreApplication.translate("MainWindow", u"Reset(\u91cd\u7f6e)", None))
    # retranslateUi

