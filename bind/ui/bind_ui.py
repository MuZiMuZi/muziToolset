# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bind_ui.ui'
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
        MainWindow.resize(832, 772)
        self.actionRefersh = QAction(MainWindow)
        self.actionRefersh.setObjectName(u"actionRefersh")
        self.action_Mirror_select = QAction(MainWindow)
        self.action_Mirror_select.setObjectName(u"action_Mirror_select")
        self.action_Mirror = QAction(MainWindow)
        self.action_Mirror.setObjectName(u"action_Mirror")
        self.action_Upward = QAction(MainWindow)
        self.action_Upward.setObjectName(u"action_Upward")
        self.action_Lowward = QAction(MainWindow)
        self.action_Lowward.setObjectName(u"action_Lowward")
        self.action_Rename = QAction(MainWindow)
        self.action_Rename.setObjectName(u"action_Rename")
        self.action_Delete = QAction(MainWindow)
        self.action_Delete.setObjectName(u"action_Delete")
        self.action_Clear = QAction(MainWindow)
        self.action_Clear.setObjectName(u"action_Clear")
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 250, 673))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.proxy_widget = QListWidget(self.scrollAreaWidgetContents)
        brush = QBrush(QColor(247, 255, 152, 255))
        brush.setStyle(Qt.SolidPattern)
        __qlistwidgetitem = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem.setForeground(brush);
        brush1 = QBrush(QColor(255, 183, 248, 255))
        brush1.setStyle(Qt.SolidPattern)
        __qlistwidgetitem1 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem1.setForeground(brush1);
        __qlistwidgetitem2 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem2.setFlags(Qt.NoItemFlags);
        icon = QIcon()
        icon.addFile(u"../../../tools/icon/componentFK_64.png", QSize(), QIcon.Normal, QIcon.Off)
        brush2 = QBrush(QColor(255, 137, 153, 255))
        brush2.setStyle(Qt.SolidPattern)
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.NoBrush)
        __qlistwidgetitem3 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem3.setBackground(brush3);
        __qlistwidgetitem3.setForeground(brush2);
        __qlistwidgetitem3.setIcon(icon);
        __qlistwidgetitem4 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem4.setForeground(brush2);
        font1 = QFont()
        font1.setKerning(True)
        __qlistwidgetitem5 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem5.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qlistwidgetitem5.setFont(font1);
        __qlistwidgetitem5.setForeground(brush2);
        __qlistwidgetitem6 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem6.setForeground(brush2);
        __qlistwidgetitem7 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem7.setForeground(brush2);
        __qlistwidgetitem8 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem8.setFlags(Qt.NoItemFlags);
        brush4 = QBrush(QColor(88, 76, 255, 255))
        brush4.setStyle(Qt.SolidPattern)
        __qlistwidgetitem9 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem9.setForeground(brush4);
        __qlistwidgetitem10 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem10.setForeground(brush4);
        __qlistwidgetitem11 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem11.setForeground(brush4);
        __qlistwidgetitem12 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem12.setForeground(brush4);
        __qlistwidgetitem13 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem13.setForeground(brush4);
        __qlistwidgetitem14 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem14.setForeground(brush4);
        __qlistwidgetitem15 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem15.setFlags(Qt.NoItemFlags);
        brush5 = QBrush(QColor(255, 79, 79, 255))
        brush5.setStyle(Qt.SolidPattern)
        __qlistwidgetitem16 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem16.setForeground(brush5);
        __qlistwidgetitem17 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem17.setForeground(brush5);
        __qlistwidgetitem18 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem18.setForeground(brush5);
        __qlistwidgetitem19 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem19.setForeground(brush5);
        __qlistwidgetitem20 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem20.setForeground(brush5);
        __qlistwidgetitem21 = QListWidgetItem(self.proxy_widget)
        __qlistwidgetitem21.setForeground(brush5);
        self.proxy_widget.setObjectName(u"proxy_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.proxy_widget.sizePolicy().hasHeightForWidth())
        self.proxy_widget.setSizePolicy(sizePolicy1)
        self.proxy_widget.setBaseSize(QSize(0, 0))
        font2 = QFont()
        font2.setFamily(u"Arial Narrow")
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
        self.proxy_widget.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.proxy_widget.setDragEnabled(False)
        self.proxy_widget.setDragDropOverwriteMode(False)
        self.proxy_widget.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.proxy_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.proxy_widget.setSelectionRectVisible(False)
        self.proxy_widget.setSortingEnabled(False)

        self.verticalLayout_2.addWidget(self.proxy_widget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.jointRadius_label = QLabel(self.scrollAreaWidgetContents)
        self.jointRadius_label.setObjectName(u"jointRadius_label")
        font3 = QFont()
        font3.setFamily(u"Arial")
        font3.setPointSize(9)
        font3.setKerning(True)
        self.jointRadius_label.setFont(font3)

        self.horizontalLayout_4.addWidget(self.jointRadius_label)

        self.jointRadius_Slider = QSlider(self.scrollAreaWidgetContents)
        self.jointRadius_Slider.setObjectName(u"jointRadius_Slider")
        self.jointRadius_Slider.setFont(font)
        self.jointRadius_Slider.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.jointRadius_Slider.setLayoutDirection(Qt.LeftToRight)
        self.jointRadius_Slider.setMinimum(1)
        self.jointRadius_Slider.setMaximum(50)
        self.jointRadius_Slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.jointRadius_Slider)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.jointAxis_label = QLabel(self.scrollAreaWidgetContents)
        self.jointAxis_label.setObjectName(u"jointAxis_label")
        font4 = QFont()
        font4.setFamily(u"Arial")
        self.jointAxis_label.setFont(font4)

        self.horizontalLayout_5.addWidget(self.jointAxis_label)

        self.jointAxis_on_radio = QRadioButton(self.scrollAreaWidgetContents)
        self.jointAxis_on_radio.setObjectName(u"jointAxis_on_radio")
        self.jointAxis_on_radio.setFont(font4)

        self.horizontalLayout_5.addWidget(self.jointAxis_on_radio)

        self.jointAxis_off_radio = QRadioButton(self.scrollAreaWidgetContents)
        self.jointAxis_off_radio.setObjectName(u"jointAxis_off_radio")
        self.jointAxis_off_radio.setFont(font4)
        self.jointAxis_off_radio.setChecked(True)

        self.horizontalLayout_5.addWidget(self.jointAxis_off_radio)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

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
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 249, 316))
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.preset_widget = QListWidget(self.scrollAreaWidgetContents_5)
        QListWidgetItem(self.preset_widget)
        QListWidgetItem(self.preset_widget)
        QListWidgetItem(self.preset_widget)
        self.preset_widget.setObjectName(u"preset_widget")
        font5 = QFont()
        font5.setPointSize(14)
        self.preset_widget.setFont(font5)
        self.preset_widget.setStyleSheet(u"")
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
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 249, 315))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_3.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_3.setSizePolicy(sizePolicy)
        self.gridLayout_4 = QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.custom_widget = QListWidget(self.scrollAreaWidgetContents_3)
        self.custom_widget.setObjectName(u"custom_widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.custom_widget.sizePolicy().hasHeightForWidth())
        self.custom_widget.setSizePolicy(sizePolicy2)
        font6 = QFont()
        font6.setFamily(u"Arial Narrow")
        font6.setPointSize(14)
        self.custom_widget.setFont(font6)
        self.custom_widget.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.custom_widget.setDragEnabled(True)
        self.custom_widget.setDragDropOverwriteMode(True)
        self.custom_widget.setDragDropMode(QAbstractItemView.InternalMove)

        self.gridLayout_4.addWidget(self.custom_widget, 1, 0, 1, 1)

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

        self.setting_stack = QStackedWidget(self.centralwidget)
        self.setting_stack.setObjectName(u"setting_stack")
        self.Page1 = QWidget()
        self.Page1.setObjectName(u"Page1")
        self.set_layout = QVBoxLayout(self.Page1)
        self.set_layout.setObjectName(u"set_layout")
        self.set_layout.setContentsMargins(-1, 9, -1, 9)
        self.setting_stack.addWidget(self.Page1)

        self.verticalLayout_4.addWidget(self.setting_stack)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.setting_layout.addLayout(self.verticalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.bpjnt_label = QLabel(self.centralwidget)
        self.bpjnt_label.setObjectName(u"bpjnt_label")
        self.bpjnt_label.setFont(font4)
        self.bpjnt_label.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_8.addWidget(self.bpjnt_label)

        self.bpjnt_on_radio = QRadioButton(self.centralwidget)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.bpjnt_on_radio)
        self.bpjnt_on_radio.setObjectName(u"bpjnt_on_radio")
        self.bpjnt_on_radio.setFont(font4)
        self.bpjnt_on_radio.setChecked(True)

        self.horizontalLayout_8.addWidget(self.bpjnt_on_radio)

        self.bpjnt_off_radio = QRadioButton(self.centralwidget)
        self.buttonGroup.addButton(self.bpjnt_off_radio)
        self.bpjnt_off_radio.setObjectName(u"bpjnt_off_radio")
        self.bpjnt_off_radio.setFont(font4)

        self.horizontalLayout_8.addWidget(self.bpjnt_off_radio)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.mesh_label = QLabel(self.centralwidget)
        self.mesh_label.setObjectName(u"mesh_label")
        self.mesh_label.setFont(font4)

        self.horizontalLayout_7.addWidget(self.mesh_label)

        self.mesh_on_radio = QRadioButton(self.centralwidget)
        self.buttonGroup_2 = QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.mesh_on_radio)
        self.mesh_on_radio.setObjectName(u"mesh_on_radio")
        self.mesh_on_radio.setFont(font4)
        self.mesh_on_radio.setChecked(True)

        self.horizontalLayout_7.addWidget(self.mesh_on_radio)

        self.mesh_off_radio = QRadioButton(self.centralwidget)
        self.buttonGroup_2.addButton(self.mesh_off_radio)
        self.mesh_off_radio.setObjectName(u"mesh_off_radio")
        self.mesh_off_radio.setFont(font4)
        self.mesh_off_radio.setChecked(False)

        self.horizontalLayout_7.addWidget(self.mesh_off_radio)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.joint_label = QLabel(self.centralwidget)
        self.joint_label.setObjectName(u"joint_label")
        self.joint_label.setFont(font4)

        self.horizontalLayout_6.addWidget(self.joint_label)

        self.joint_on_radio = QRadioButton(self.centralwidget)
        self.buttonGroup_3 = QButtonGroup(MainWindow)
        self.buttonGroup_3.setObjectName(u"buttonGroup_3")
        self.buttonGroup_3.addButton(self.joint_on_radio)
        self.joint_on_radio.setObjectName(u"joint_on_radio")
        self.joint_on_radio.setFont(font4)

        self.horizontalLayout_6.addWidget(self.joint_on_radio)

        self.joint_off_radio = QRadioButton(self.centralwidget)
        self.buttonGroup_3.addButton(self.joint_off_radio)
        self.joint_off_radio.setObjectName(u"joint_off_radio")
        self.joint_off_radio.setFont(font4)
        self.joint_off_radio.setChecked(True)

        self.horizontalLayout_6.addWidget(self.joint_off_radio)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.control_label = QLabel(self.centralwidget)
        self.control_label.setObjectName(u"control_label")
        self.control_label.setFont(font4)

        self.horizontalLayout_2.addWidget(self.control_label)

        self.control_on_radio = QRadioButton(self.centralwidget)
        self.buttonGroup_4 = QButtonGroup(MainWindow)
        self.buttonGroup_4.setObjectName(u"buttonGroup_4")
        self.buttonGroup_4.addButton(self.control_on_radio)
        self.control_on_radio.setObjectName(u"control_on_radio")
        self.control_on_radio.setFont(font4)

        self.horizontalLayout_2.addWidget(self.control_on_radio)

        self.control_off_radio = QRadioButton(self.centralwidget)
        self.buttonGroup_4.addButton(self.control_off_radio)
        self.control_off_radio.setObjectName(u"control_off_radio")
        self.control_off_radio.setFont(font4)
        self.control_off_radio.setChecked(True)

        self.horizontalLayout_2.addWidget(self.control_off_radio)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.orient_button = QToolButton(self.centralwidget)
        self.orient_button.setObjectName(u"orient_button")
        sizePolicy.setHeightForWidth(self.orient_button.sizePolicy().hasHeightForWidth())
        self.orient_button.setSizePolicy(sizePolicy)
        self.orient_button.setFont(font4)
        self.orient_button.setAutoFillBackground(False)
        self.orient_button.setIconSize(QSize(36, 46))
        self.orient_button.setCheckable(False)
        self.orient_button.setAutoRaise(False)

        self.horizontalLayout_9.addWidget(self.orient_button)

        self.delete_button = QToolButton(self.centralwidget)
        self.delete_button.setObjectName(u"delete_button")
        sizePolicy.setHeightForWidth(self.delete_button.sizePolicy().hasHeightForWidth())
        self.delete_button.setSizePolicy(sizePolicy)
        font7 = QFont()
        font7.setFamily(u"Arial")
        font7.setPointSize(10)
        self.delete_button.setFont(font7)
        self.delete_button.setAutoFillBackground(False)
        self.delete_button.setIconSize(QSize(36, 46))
        self.delete_button.setCheckable(False)

        self.horizontalLayout_9.addWidget(self.delete_button)

        self.reset_button = QToolButton(self.centralwidget)
        self.reset_button.setObjectName(u"reset_button")
        self.reset_button.setEnabled(True)
        sizePolicy.setHeightForWidth(self.reset_button.sizePolicy().hasHeightForWidth())
        self.reset_button.setSizePolicy(sizePolicy)
        self.reset_button.setFont(font7)
        self.reset_button.setAutoFillBackground(True)
        self.reset_button.setIconSize(QSize(36, 46))

        self.horizontalLayout_9.addWidget(self.reset_button)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)

        self.build_button = QToolButton(self.centralwidget)
        self.build_button.setObjectName(u"build_button")
        sizePolicy.setHeightForWidth(self.build_button.sizePolicy().hasHeightForWidth())
        self.build_button.setSizePolicy(sizePolicy)
        font8 = QFont()
        font8.setFamily(u"Arial")
        font8.setPointSize(20)
        self.build_button.setFont(font8)
        self.build_button.setAutoFillBackground(True)
        self.build_button.setStyleSheet(u"")
        self.build_button.setIconSize(QSize(122, 48))
        self.build_button.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_6.addWidget(self.build_button)


        self.horizontalLayout_3.addLayout(self.verticalLayout_6)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.setting_layout.addLayout(self.verticalLayout)


        self.horizontalLayout.addLayout(self.setting_layout)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 832, 23))
        self.menuWindow = QMenu(self.menubar)
        self.menuWindow.setObjectName(u"menuWindow")
        self.menuCustom = QMenu(self.menubar)
        self.menuCustom.setObjectName(u"menuCustom")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuCustom.menuAction())
        self.menuWindow.addAction(self.actionRefersh)
        self.menuCustom.addAction(self.action_Mirror_select)
        self.menuCustom.addAction(self.action_Mirror)
        self.menuCustom.addSeparator()
        self.menuCustom.addAction(self.action_Upward)
        self.menuCustom.addAction(self.action_Lowward)
        self.menuCustom.addAction(self.action_Rename)
        self.menuCustom.addSeparator()
        self.menuCustom.addAction(self.action_Delete)
        self.menuCustom.addAction(self.action_Clear)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MuZi_BindingSystem", None))
        self.actionRefersh.setText(QCoreApplication.translate("MainWindow", u"refersh", None))
        self.action_Mirror_select.setText(QCoreApplication.translate("MainWindow", u"Mirror_selection", None))
        self.action_Mirror.setText(QCoreApplication.translate("MainWindow", u"Mirror_All", None))
        self.action_Upward.setText(QCoreApplication.translate("MainWindow", u"Upward", None))
        self.action_Lowward.setText(QCoreApplication.translate("MainWindow", u"Downward", None))
        self.action_Rename.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.action_Delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.action_Clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.proxy_label.setText(QCoreApplication.translate("MainWindow", u"Proxy_Library", None))

        __sortingEnabled = self.proxy_widget.isSortingEnabled()
        self.proxy_widget.setSortingEnabled(False)
        ___qlistwidgetitem = self.proxy_widget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"master", None));
        ___qlistwidgetitem1 = self.proxy_widget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"base", None));
        ___qlistwidgetitem2 = self.proxy_widget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u2014\u2014\u2014chain\u2014\u2014\u2014", None));
        ___qlistwidgetitem3 = self.proxy_widget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"chainFK", None));
        ___qlistwidgetitem4 = self.proxy_widget.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"chainIK", None));
        ___qlistwidgetitem5 = self.proxy_widget.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("MainWindow", u"chainIKFK", None));
        ___qlistwidgetitem6 = self.proxy_widget.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("MainWindow", u"chainEP", None));
        ___qlistwidgetitem7 = self.proxy_widget.item(7)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("MainWindow", u"finger", None));
        ___qlistwidgetitem8 = self.proxy_widget.item(8)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("MainWindow", u"\u2014\u2014\u2014face\u2014\u2014\u2014", None));
        ___qlistwidgetitem9 = self.proxy_widget.item(9)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("MainWindow", u"brow", None));
        ___qlistwidgetitem10 = self.proxy_widget.item(10)
        ___qlistwidgetitem10.setText(QCoreApplication.translate("MainWindow", u"eye", None));
        ___qlistwidgetitem11 = self.proxy_widget.item(11)
        ___qlistwidgetitem11.setText(QCoreApplication.translate("MainWindow", u"nose", None));
        ___qlistwidgetitem12 = self.proxy_widget.item(12)
        ___qlistwidgetitem12.setText(QCoreApplication.translate("MainWindow", u"mouth", None));
        ___qlistwidgetitem13 = self.proxy_widget.item(13)
        ___qlistwidgetitem13.setText(QCoreApplication.translate("MainWindow", u"cheek", None));
        ___qlistwidgetitem14 = self.proxy_widget.item(14)
        ___qlistwidgetitem14.setText(QCoreApplication.translate("MainWindow", u"jaw", None));
        ___qlistwidgetitem15 = self.proxy_widget.item(15)
        ___qlistwidgetitem15.setText(QCoreApplication.translate("MainWindow", u"\u2014\u2014\u2014body\u2014\u2014\u2014", None));
        ___qlistwidgetitem16 = self.proxy_widget.item(16)
        ___qlistwidgetitem16.setText(QCoreApplication.translate("MainWindow", u"arm", None));
        ___qlistwidgetitem17 = self.proxy_widget.item(17)
        ___qlistwidgetitem17.setText(QCoreApplication.translate("MainWindow", u"hand", None));
        ___qlistwidgetitem18 = self.proxy_widget.item(18)
        ___qlistwidgetitem18.setText(QCoreApplication.translate("MainWindow", u"spine", None));
        ___qlistwidgetitem19 = self.proxy_widget.item(19)
        ___qlistwidgetitem19.setText(QCoreApplication.translate("MainWindow", u"leg", None));
        ___qlistwidgetitem20 = self.proxy_widget.item(20)
        ___qlistwidgetitem20.setText(QCoreApplication.translate("MainWindow", u"foot", None));
        ___qlistwidgetitem21 = self.proxy_widget.item(21)
        ___qlistwidgetitem21.setText(QCoreApplication.translate("MainWindow", u"tail", None));
        self.proxy_widget.setSortingEnabled(__sortingEnabled)

        self.jointRadius_label.setText(QCoreApplication.translate("MainWindow", u"Joint Radius:", None))
        self.jointAxis_label.setText(QCoreApplication.translate("MainWindow", u"JointAxis:", None))
        self.jointAxis_on_radio.setText(QCoreApplication.translate("MainWindow", u"On", None))
        self.jointAxis_off_radio.setText(QCoreApplication.translate("MainWindow", u"Off", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Presets", None))

        __sortingEnabled1 = self.preset_widget.isSortingEnabled()
        self.preset_widget.setSortingEnabled(False)
        ___qlistwidgetitem22 = self.preset_widget.item(0)
        ___qlistwidgetitem22.setText(QCoreApplication.translate("MainWindow", u"human", None));
        ___qlistwidgetitem23 = self.preset_widget.item(1)
        ___qlistwidgetitem23.setText(QCoreApplication.translate("MainWindow", u"face", None));
        ___qlistwidgetitem24 = self.preset_widget.item(2)
        ___qlistwidgetitem24.setText(QCoreApplication.translate("MainWindow", u"quadruped", None));
        self.preset_widget.setSortingEnabled(__sortingEnabled1)

        self.custom_label.setText(QCoreApplication.translate("MainWindow", u"Custom", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.bpjnt_label.setText(QCoreApplication.translate("MainWindow", u"Bpjnt", None))
        self.bpjnt_on_radio.setText(QCoreApplication.translate("MainWindow", u"On", None))
        self.bpjnt_off_radio.setText(QCoreApplication.translate("MainWindow", u"Off", None))
        self.mesh_label.setText(QCoreApplication.translate("MainWindow", u"Mesh", None))
        self.mesh_on_radio.setText(QCoreApplication.translate("MainWindow", u"On", None))
        self.mesh_off_radio.setText(QCoreApplication.translate("MainWindow", u"Off", None))
        self.joint_label.setText(QCoreApplication.translate("MainWindow", u"Joint", None))
        self.joint_on_radio.setText(QCoreApplication.translate("MainWindow", u"On", None))
        self.joint_off_radio.setText(QCoreApplication.translate("MainWindow", u"Off", None))
        self.control_label.setText(QCoreApplication.translate("MainWindow", u"Control", None))
        self.control_on_radio.setText(QCoreApplication.translate("MainWindow", u"On", None))
        self.control_off_radio.setText(QCoreApplication.translate("MainWindow", u"Off", None))
#if QT_CONFIG(tooltip)
        self.orient_button.setToolTip(QCoreApplication.translate("MainWindow", u"\u5173\u8282\u5b9a\u5411", None))
#endif // QT_CONFIG(tooltip)
        self.orient_button.setText("")
#if QT_CONFIG(tooltip)
        self.delete_button.setToolTip(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u7ed1\u5b9a", None))
#endif // QT_CONFIG(tooltip)
        self.delete_button.setText("")
#if QT_CONFIG(tooltip)
        self.reset_button.setToolTip(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e\u63a7\u5236\u5668", None))
#endif // QT_CONFIG(tooltip)
        self.reset_button.setText("")
#if QT_CONFIG(tooltip)
        self.build_button.setToolTip(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u7ed1\u5b9a", None))
#endif // QT_CONFIG(tooltip)
        self.build_button.setText("")
        self.menuWindow.setTitle(QCoreApplication.translate("MainWindow", u"Window", None))
        self.menuCustom.setTitle(QCoreApplication.translate("MainWindow", u"Custom", None))
    # retranslateUi

