# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bindSystem.ui'
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
        MainWindow.resize(961, 761)
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
        self.proxy_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.proxy_label = QLabel(self.centralwidget)
        self.proxy_label.setObjectName(u"proxy_label")
        self.proxy_label.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.proxy_label.sizePolicy().hasHeightForWidth())
        self.proxy_label.setSizePolicy(sizePolicy)
        self.proxy_label.setSizeIncrement(QSize(0, 0))
        font = QFont()
        font.setFamily(u"Agency FB")
        font.setPointSize(14)
        self.proxy_label.setFont(font)
        self.proxy_label.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.proxy_label.setLayoutDirection(Qt.LeftToRight)
        self.proxy_label.setAlignment(Qt.AlignCenter)

        self.proxy_layout.addWidget(self.proxy_label)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 299, 662))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.jointRadius_label = QLabel(self.scrollAreaWidgetContents)
        self.jointRadius_label.setObjectName(u"jointRadius_label")
        self.jointRadius_label.setFont(font)

        self.horizontalLayout_2.addWidget(self.jointRadius_label)

        self.jointRadius_Slider = QSlider(self.scrollAreaWidgetContents)
        self.jointRadius_Slider.setObjectName(u"jointRadius_Slider")
        self.jointRadius_Slider.setFont(font)
        self.jointRadius_Slider.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.jointRadius_Slider.setLayoutDirection(Qt.LeftToRight)
        self.jointRadius_Slider.setMinimum(1)
        self.jointRadius_Slider.setMaximum(50)
        self.jointRadius_Slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.jointRadius_Slider)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.proxy_widget = QListWidget(self.scrollAreaWidgetContents)
        brush = QBrush(QColor(247, 255, 152, 255))
        brush.setStyle(Qt.SolidPattern)
        __qlistwidgetitem = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem.setForeground(brush);
        brush1 = QBrush(QColor(88, 76, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        __qlistwidgetitem1 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem1.setForeground(brush1);
        __qlistwidgetitem2 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem2.setForeground(brush1);
        __qlistwidgetitem3 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem3.setForeground(brush1);
        __qlistwidgetitem4 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem4.setForeground(brush1);
        __qlistwidgetitem5 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem5.setForeground(brush1);
        __qlistwidgetitem6 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem6.setForeground(brush1);
        brush2 = QBrush(QColor(255, 79, 79, 255))
        brush2.setStyle(Qt.SolidPattern)
        __qlistwidgetitem7 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem7.setForeground(brush2);
        __qlistwidgetitem8 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem8.setForeground(brush2);
        __qlistwidgetitem9 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem9.setForeground(brush2);
        __qlistwidgetitem10 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem10.setForeground(brush2);
        __qlistwidgetitem11 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem11.setForeground(brush2);
        __qlistwidgetitem12 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem12.setForeground(brush2);
        brush3 = QBrush(QColor(255, 137, 153, 255))
        brush3.setStyle(Qt.SolidPattern)
        font1 = QFont()
        font1.setKerning(True)
        __qlistwidgetitem13 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem13.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qlistwidgetitem13.setFont(font1);
        __qlistwidgetitem13.setForeground(brush3);
        brush4 = QBrush(QColor(0, 0, 0, 255))
        brush4.setStyle(Qt.NoBrush)
        __qlistwidgetitem14 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem14.setBackground(brush4);
        __qlistwidgetitem14.setForeground(brush3);
        __qlistwidgetitem15 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem15.setForeground(brush3);
        brush5 = QBrush(QColor(255, 183, 248, 255))
        brush5.setStyle(Qt.SolidPattern)
        __qlistwidgetitem16 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem16.setForeground(brush5);
        self.proxy_widget.setObjectName(u"proxy_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.proxy_widget.sizePolicy().hasHeightForWidth())
        self.proxy_widget.setSizePolicy(sizePolicy1)
        self.proxy_widget.setBaseSize(QSize(0, 0))
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setWeight(75)
        self.proxy_widget.setFont(font2)
        self.proxy_widget.setMouseTracking(False)
        self.proxy_widget.setFocusPolicy(Qt.StrongFocus)
        self.proxy_widget.setLayoutDirection(Qt.LeftToRight)
        self.proxy_widget.setAutoFillBackground(False)
        self.proxy_widget.setStyleSheet(u"")
        self.proxy_widget.setLineWidth(0)
        self.proxy_widget.setAutoScroll(True)
        self.proxy_widget.setDragEnabled(False)
        self.proxy_widget.setDragDropOverwriteMode(False)
        self.proxy_widget.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.proxy_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.proxy_widget.setSelectionRectVisible(False)

        self.gridLayout_2.addWidget(self.proxy_widget, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.proxy_layout.addWidget(self.scrollArea)


        self.horizontalLayout.addLayout(self.proxy_layout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.preset_layout = QVBoxLayout()
        self.preset_layout.setObjectName(u"preset_layout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.preset_layout.addWidget(self.label)

        self.scrollArea_2 = QScrollArea(self.centralwidget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 296, 310))
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.preset_widget = QListWidget(self.scrollAreaWidgetContents_5)
        QListWidgetItem(self.preset_widget)
        QListWidgetItem(self.preset_widget)
        QListWidgetItem(self.preset_widget)
        self.preset_widget.setObjectName(u"preset_widget")
        font3 = QFont()
        font3.setPointSize(14)
        self.preset_widget.setFont(font3)
        self.preset_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.preset_widget.setSelectionRectVisible(False)

        self.gridLayout_5.addWidget(self.preset_widget, 0, 0, 1, 1)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_5)

        self.preset_layout.addWidget(self.scrollArea_2)


        self.verticalLayout_3.addLayout(self.preset_layout)

        self.custom_layout = QVBoxLayout()
        self.custom_layout.setObjectName(u"custom_layout")
        self.custom_label = QLabel(self.centralwidget)
        self.custom_label.setObjectName(u"custom_label")
        self.custom_label.setFont(font)
        self.custom_label.setAlignment(Qt.AlignCenter)

        self.custom_layout.addWidget(self.custom_label)

        self.scrollArea_3 = QScrollArea(self.centralwidget)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 296, 310))
        self.gridLayout_4 = QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.custom_widget = QListWidget(self.scrollAreaWidgetContents_3)
        QListWidgetItem(self.custom_widget)
        QListWidgetItem(self.custom_widget)
        self.custom_widget.setObjectName(u"custom_widget")

        self.gridLayout_4.addWidget(self.custom_widget, 0, 0, 1, 1)

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
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_3)

        self.scrollArea_5 = QScrollArea(self.centralwidget)
        self.scrollArea_5.setObjectName(u"scrollArea_5")
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName(u"scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 318, 549))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.set_widget = QStackedWidget(self.scrollAreaWidgetContents_6)
        self.set_widget.setObjectName(u"set_widget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.set_widget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.set_widget.addWidget(self.page_2)

        self.gridLayout_6.addWidget(self.set_widget, 0, 1, 1, 1)

        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_6)

        self.verticalLayout_4.addWidget(self.scrollArea_5)


        self.setting_layout.addLayout(self.verticalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.reset_button = QPushButton(self.centralwidget)
        self.reset_button.setObjectName(u"reset_button")
        font4 = QFont()
        font4.setFamily(u"Agency FB")
        font4.setPointSize(10)
        self.reset_button.setFont(font4)

        self.horizontalLayout_3.addWidget(self.reset_button)

        self.delete_button = QPushButton(self.centralwidget)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setFont(font4)

        self.horizontalLayout_3.addWidget(self.delete_button)

        self.ctrl_button = QPushButton(self.centralwidget)
        self.ctrl_button.setObjectName(u"ctrl_button")
        self.ctrl_button.setFont(font4)

        self.horizontalLayout_3.addWidget(self.ctrl_button)

        self.set_button = QPushButton(self.centralwidget)
        self.set_button.setObjectName(u"set_button")
        self.set_button.setFont(font4)

        self.horizontalLayout_3.addWidget(self.set_button)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.build_button = QPushButton(self.centralwidget)
        self.build_button.setObjectName(u"build_button")
        font5 = QFont()
        font5.setFamily(u"Agency FB")
        font5.setPointSize(20)
        self.build_button.setFont(font5)

        self.verticalLayout.addWidget(self.build_button)


        self.setting_layout.addLayout(self.verticalLayout)


        self.horizontalLayout.addLayout(self.setting_layout)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 961, 23))
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
        self.jointRadius_label.setText(QCoreApplication.translate("MainWindow", u"\u5173\u8282\u5927\u5c0f\u663e\u793a", None))

        __sortingEnabled = self.proxy_widget.isSortingEnabled()
        self.proxy_widget.setSortingEnabled(False)
        ___qlistwidgetitem = self.proxy_widget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"masterRig", None));
        ___qlistwidgetitem1 = self.proxy_widget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"browRig", None));
        ___qlistwidgetitem2 = self.proxy_widget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"eyeRig", None));
        ___qlistwidgetitem3 = self.proxy_widget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"noseRig", None));
        ___qlistwidgetitem4 = self.proxy_widget.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"mouthRig", None));
        ___qlistwidgetitem5 = self.proxy_widget.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("MainWindow", u"cheekRig", None));
        ___qlistwidgetitem6 = self.proxy_widget.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("MainWindow", u"jawRig", None));
        ___qlistwidgetitem7 = self.proxy_widget.item(7)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("MainWindow", u"armRig", None));
        ___qlistwidgetitem8 = self.proxy_widget.item(8)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("MainWindow", u"handRig", None));
        ___qlistwidgetitem9 = self.proxy_widget.item(9)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("MainWindow", u"spineRig", None));
        ___qlistwidgetitem10 = self.proxy_widget.item(10)
        ___qlistwidgetitem10.setText(QCoreApplication.translate("MainWindow", u"legRig", None));
        ___qlistwidgetitem11 = self.proxy_widget.item(11)
        ___qlistwidgetitem11.setText(QCoreApplication.translate("MainWindow", u"footRig", None));
        ___qlistwidgetitem12 = self.proxy_widget.item(12)
        ___qlistwidgetitem12.setText(QCoreApplication.translate("MainWindow", u"tailRig", None));
        ___qlistwidgetitem13 = self.proxy_widget.item(13)
        ___qlistwidgetitem13.setText(QCoreApplication.translate("MainWindow", u"ikfkRig", None));
        ___qlistwidgetitem14 = self.proxy_widget.item(14)
        ___qlistwidgetitem14.setText(QCoreApplication.translate("MainWindow", u"fkRig", None));
        ___qlistwidgetitem15 = self.proxy_widget.item(15)
        ___qlistwidgetitem15.setText(QCoreApplication.translate("MainWindow", u"ikRig", None));
        ___qlistwidgetitem16 = self.proxy_widget.item(16)
        ___qlistwidgetitem16.setText(QCoreApplication.translate("MainWindow", u"baseRig", None));
        self.proxy_widget.setSortingEnabled(__sortingEnabled)

        self.label.setText(QCoreApplication.translate("MainWindow", u"\u9884\u8bbe", None))

        __sortingEnabled1 = self.preset_widget.isSortingEnabled()
        self.preset_widget.setSortingEnabled(False)
        ___qlistwidgetitem17 = self.preset_widget.item(0)
        ___qlistwidgetitem17.setText(QCoreApplication.translate("MainWindow", u"human", None));
        ___qlistwidgetitem18 = self.preset_widget.item(1)
        ___qlistwidgetitem18.setText(QCoreApplication.translate("MainWindow", u"face", None));
        ___qlistwidgetitem19 = self.preset_widget.item(2)
        ___qlistwidgetitem19.setText(QCoreApplication.translate("MainWindow", u"quadruped", None));
        self.preset_widget.setSortingEnabled(__sortingEnabled1)

        self.custom_label.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u5b9a\u4e49\u6a21\u5757", None))

        __sortingEnabled2 = self.custom_widget.isSortingEnabled()
        self.custom_widget.setSortingEnabled(False)
        ___qlistwidgetitem20 = self.custom_widget.item(0)
        ___qlistwidgetitem20.setText(QCoreApplication.translate("MainWindow", u"m_Master_01", None));
        ___qlistwidgetitem21 = self.custom_widget.item(1)
        ___qlistwidgetitem21.setText(QCoreApplication.translate("MainWindow", u"m_Neck_01", None));
        self.custom_widget.setSortingEnabled(__sortingEnabled2)

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7ed1\u5b9a\u5de5\u5177", None))
        self.reset_button.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e\u7ed1\u5b9a", None))
        self.delete_button.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u7ed1\u5b9a", None))
        self.ctrl_button.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e\u63a7\u5236\u5668", None))
        self.set_button.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.build_button.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u7ed1\u5b9a", None))
        self.menuWindow.setTitle(QCoreApplication.translate("MainWindow", u"Window", None))
    # retranslateUi

