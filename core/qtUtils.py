# coding=utf-8
'''
已有：
创建一个输入的弹窗:input_dialog_text
弹出询问是否执行的窗口:input_dialog_message
删除指定的文件夹：remove_folder
删除指定的文件：remove_file
弹出创建新文件名的窗口：new_folder
重命名给定的文件或者是文件夹的名称：rename_file_or_folder
选择文件点击按钮后可以在系统文件资源管理器里打开这个文件：show_file_in_explorer
选择文件夹点击按钮后可以在系统文件资源管理器里打开这个文件夹:show_folder_in_explorer
'''
import os
import subprocess
import maya.OpenMayaUI as omui
from PySide2 import QtCore , QtWidgets , QtGui
from shiboken2 import wrapInstance


path_joiner = lambda *args : os.path.join (*args).replace ('\\' , '/')


def input_dialog_text (title , label , size = (400 , 200)) :
    u'''
    创建一个输入的弹窗
    :param title:弹窗的标题
    :param label:弹窗的提示
    :param size:弹窗的大小
    :return:
    '''
    input_text = QtWidgets.QInputDialog ()
    # *size 是为了解包元组
    input_text.setFixedSize (*size)
    input_text.setInputMode (QtWidgets.QInputDialog.TextInput)
    input_text.setWindowTitle (title)
    input_text.setLabelText (label)

    if input_text.exec_ () == QtWidgets.QDialog.Accepted :
        return input_text.textValue ()
    else :
        return None


def input_dialog_message (title , text = '' , informative = u'确认?' , size = (400 , 200)) :
    u'''
    弹出询问是否执行的窗口
    :param title:窗口的标题
    :param text:
    :param informative:弹出的窗口的提示语
    :param size:弹出的窗口的大小
    :return:
    '''
    msg_box = QtWidgets.QMessageBox ()
    msg_box.setFixedSize (*size)
    msg_box.setText (text)
    msg_box.setWindowTitle (title)
    # 设置弹出的窗口的提示语
    msg_box.setInformativeText (informative)
    # 设置弹出的窗口的按钮
    msg_box.setStandardButtons (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msg_box.setDefaultButton (QtWidgets.QMessageBox.Yes)

    # 确认最后执行的结果
    decision = msg_box.exec_ ()
    if decision == QtWidgets.QMessageBox.Yes :
        return True
    else :
        return False


def remove_folder (folder_path) :
    u'''
    删除指定的文件夹
    :param folder_path:
    :return:
    '''
    import shutil


    decision = input_dialog_message (
        'Deleting_folder' ,
        u'请问是否删除这个文件夹{}?'.format (folder_path)
    )
    if not decision :
        return
    shutil.rmtree (folder_path)


def remove_file (file_path) :
    u'''
    删除指定的文件
    :param file_path:
    :return:
    '''
    decision = input_dialog_message (
        'Deleting_file' ,
        u'请问是否删除这个文件{}?'.format (file_path)
    )
    if not decision :
        return
    os.remove (file_path)


def new_folder (current_path) :
    u'''
    弹出创建新文件名的窗口
    :param current_path: 新文件的路径
    :return:
    '''
    folder_name = input_dialog_text (u'新文件' , u'请输入新文件名' , (400 , 400))
    if folder_name is None :
        return
    new_folder_path = os.path.join (current_path , folder_name).replace ('\\' , '/')
    if os.path.exists (new_folder_path) :
        print ('{} already exists .Request ignored.'.format (new_folder_path))
        return
    os.makedirs (new_folder_path)


def rename_file_or_folder (old_path) :
    u'''
    重命名给定的文件或者是文件夹的名称
    :param old_path: 过去的文件或者是文件夹的名称
    :return:
    '''
    old_name = os.path.basename (old_path)
    new_name = input_dialog_text (u'重命名_{}'.format (old_name) , u'重命名为新的名称' , (500 , 200))
    if new_name is None :
        return
    current_path = os.path.dirname (old_path)
    new_path = path_joiner (current_path , new_name)
    if os.path.isfile (old_path) :
        new_path = '.'.join ([new_name , old_name.split ('.') [-1]])
    if os.path.exists (new_path) :
        print ('{} already exists .Request ignored.'.format (new_path))
        return

    os.rename (old_path , new_path)


def show_file_in_explorer (file_path) :
    u'''
            选择文件点击按钮后可以在系统文件资源管理器里打开这个文件
    :param file_path:
    :return:
    '''
    if not os.path.exists (file_path) :
        return
    command = f'explorer /select,"{os.path.abspath (file_path)}"'
    subprocess.Popen (command)


def show_folder_in_explorer (folder_path) :
    u'''
            选择文件夹点击按钮后可以在系统文件资源管理器里打开这个文件夹
    :param file_path:
    :return:
    '''
    if not os.path.exists (folder_path) :
        return
    command = f'explorer /open,"{os.path.abspath (folder_path)}"'
    subprocess.Popen (command)


def get_maya_window () :
    u"""
    返回maya的主窗口部件
    """
    pointer = omui.MQtUtil.mainWindow ()
    return wrapInstance (int (pointer) , QtWidgets.QWidget)


class FrameWidget (QtWidgets.QGroupBox) :

    def __init__ (self , title = '' , parent = None) :
        super (FrameWidget , self).__init__ (title , parent)

        layout = QtWidgets.QVBoxLayout ()
        layout.setContentsMargins (0 , 7 , 0 , 0)
        layout.setSpacing (0)
        super (FrameWidget , self).setLayout (layout)

        self.__widget = QtWidgets.QFrame (parent)
        self.__widget.setFrameShape (QtWidgets.QFrame.Panel)
        self.__widget.setFrameShadow (QtWidgets.QFrame.Plain)
        self.__widget.setLineWidth (0)
        layout.addWidget (self.__widget)

        self.__collapsed = False


    def setLayout (self , layout) :
        self.__widget.setLayout (layout)


    def expandCollapseRect (self) :
        return QtCore.QRect (0 , 0 , self.width () , 20)


    def mouseReleaseEvent (self , event) :
        if self.expandCollapseRect ().contains (event.pos ()) :
            self.toggleCollapsed ()
            event.accept ()
        else :
            event.ignore ()


    def toggleCollapsed (self) :
        self.setCollapsed (not self.__collapsed)


    def setCollapsed (self , state = True) :
        self.__collapsed = state

        if state :
            self.setMinimumHeight (20)
            self.setMaximumHeight (20)
            self.__widget.setVisible (False)
        else :
            self.setMinimumHeight (0)
            self.setMaximumHeight (1000000)
            self.__widget.setVisible (True)


    def paintEvent (self , event) :
        painter = QtGui.QPainter ()
        painter.begin (self)

        font = painter.font ()
        font.setBold (True)
        painter.setFont (font)

        x = self.rect ().x ()
        y = self.rect ().y ()
        w = self.rect ().width ()
        offset = 25

        painter.setRenderHint (painter.Antialiasing)
        painter.fillRect (self.expandCollapseRect () , QtGui.QColor (93 , 93 , 93))
        painter.drawText (
            x + offset , y + 3 , w , 16 ,
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop ,
            self.title ()
        )
        self.__drawTriangle (painter , x , y)  # (1)
        painter.setRenderHint (QtGui.QPainter.Antialiasing , False)
        painter.end ()


    def __drawTriangle (self , painter , x , y) :  # (2)
        if not self.__collapsed :  # (3)
            points = [QtCore.QPoint (x + 10 , y + 6) ,
                      QtCore.QPoint (x + 20 , y + 6) ,
                      QtCore.QPoint (x + 15 , y + 11)
                      ]

        else :
            points = [QtCore.QPoint (x + 10 , y + 4) ,
                      QtCore.QPoint (x + 15 , y + 9) ,
                      QtCore.QPoint (x + 10 , y + 14)
                      ]

        currentBrush = painter.brush ()  # (4)
        currentPen = painter.pen ()

        painter.setBrush (
            QtGui.QBrush (
                QtGui.QColor (187 , 187 , 187) ,
                QtCore.Qt.SolidPattern
            )
        )  # (5)
        painter.setPen (QtGui.QPen (QtCore.Qt.NoPen))  # (6)
        painter.drawPolygon (QtGui.QPolygon (points))  # (7)
        painter.setBrush (currentBrush)  # (8)
        painter.setPen (currentPen)


class Dialog (QtWidgets.QDialog) :
    """
    创建一个自定义的dialog模版
    """

    def __init__ (self , parent = get_maya_window ()) :
        super (Dialog , self).__init__ (parent)
        # 添加部件
        self.create_widgets ()
        self.create_layouts ()

        # 添加连接
        self.create_connections ()


    def create_widgets (self) :
        """创建需要的小部件"""
        pass


    def create_layouts (self) :
        """创建需要的布局"""
        pass


    def create_connections (self) :
        """连接需要的部件和对应的信号"""
        pass
