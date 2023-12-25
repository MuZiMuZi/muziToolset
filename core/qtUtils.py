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
import sys
import subprocess
import maya.OpenMayaUI as omui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
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
    input_text = QInputDialog ()
    # *size 是为了解包元组
    input_text.setFixedSize (*size)
    input_text.setInputMode (QInputDialog.TextInput)
    input_text.setWindowTitle (title)
    input_text.setLabelText (label)

    if input_text.exec_ () == QDialog.Accepted :
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
    msg_box = QMessageBox ()
    msg_box.setFixedSize (*size)
    msg_box.setText (text)
    msg_box.setWindowTitle (title)
    # 设置弹出的窗口的提示语
    msg_box.setInformativeText (informative)
    # 设置弹出的窗口的按钮
    msg_box.setStandardButtons (QMessageBox.Yes | QMessageBox.No)
    msg_box.setDefaultButton (QMessageBox.Yes)

    # 确认最后执行的结果
    decision = msg_box.exec_ ()
    if decision == QMessageBox.Yes :
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


# 获取maya的主窗口，判断python的版本号，如果大于3的话就使用int
def get_maya_window () :
    u'''
    获取maya的主窗口，判断python的版本号，如果大于3的话就使用int
    :return:
    '''
    # c++的指针概念，获取maya的窗口对象
    pointer = omui.MQtUtil.mainWindow ()
    # 判断python的版本号，如果大于3的话就使用int
    if sys.version_info.major >= 3 :
        return wrapInstance (int (pointer) , QWidget)
    else :
        return wrapInstance (long (pointer) , QWidget)


class Left_menu_button (QPushButton) :
    """
    自定义的
    """


    def __init__ (self , action_1 = None , action_2 = None , *args , **kwargs , ) :
        super (Left_menu_button , self).__init__ (*args , **kwargs)
        self.action_1 = action_1
        self.action_2 = action_2

        # 创建右键菜单
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy (Qt.CustomContextMenu)
        self.customContextMenuRequested.connect (self.showContextMenu)


    # 创建右键菜单
    def showContextMenu (self , mouseClick = Qt.RightButton) :
        # Create menu, if it doesn't exist ------------------------------
        menu = self.menu (mouseClick)
        if not menu :
            menu = QMenu (self)
            self.setMenu (menu , mouseClick)

        self.action_1 = menu.addAction (QAction (self.action_1 , self))
        self.action_2 = menu.addAction (QAction (self.action_2 , self))

        # 菜单事件处理
        action = menu.exec_ (self.mapToGlobal (pos))


class FrameWidget (QGroupBox) :

    def __init__ (self , title = '' , parent = None) :
        super (FrameWidget , self).__init__ (title , parent)

        layout = QVBoxLayout ()
        layout.setContentsMargins (0 , 7 , 0 , 0)
        layout.setSpacing (0)
        super (FrameWidget , self).setLayout (layout)

        self.__widget = QFrame (parent)
        self.__widget.setFrameShape (QFrame.Panel)
        self.__widget.setFrameShadow (QFrame.Plain)
        self.__widget.setLineWidth (0)
        layout.addWidget (self.__widget)

        self.__collapsed = False


    def setLayout (self , layout) :
        self.__widget.setLayout (layout)


    def expandCollapseRect (self) :
        return QRect (0 , 0 , self.width () , 20)


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
        painter = QPainter ()
        painter.begin (self)

        font = painter.font ()
        font.setBold (True)
        painter.setFont (font)

        x = self.rect ().x ()
        y = self.rect ().y ()
        w = self.rect ().width ()
        offset = 25

        painter.setRenderHint (painter.Antialiasing)
        painter.fillRect (self.expandCollapseRect () , QColor (93 , 93 , 93))
        painter.drawText (
            x + offset , y + 3 , w , 16 ,
            Qt.AlignLeft | Qt.AlignTop ,
            self.title ()
        )
        self.__drawTriangle (painter , x , y)  # (1)
        painter.setRenderHint (QPainter.Antialiasing , False)
        painter.end ()


    def __drawTriangle (self , painter , x , y) :  # (2)
        if not self.__collapsed :  # (3)
            points = [QPoint (x + 10 , y + 6) ,
                      QPoint (x + 20 , y + 6) ,
                      QPoint (x + 15 , y + 11)
                      ]

        else :
            points = [QPoint (x + 10 , y + 4) ,
                      QPoint (x + 15 , y + 9) ,
                      QPoint (x + 10 , y + 14)
                      ]

        currentBrush = painter.brush ()  # (4)
        currentPen = painter.pen ()

        painter.setBrush (
            QBrush (
                QColor (187 , 187 , 187) ,
                Qt.SolidPattern
            )
        )  # (5)
        painter.setPen (QPen (Qt.NoPen))  # (6)
        painter.drawPolygon (QPolygon (points))  # (7)
        painter.setBrush (currentBrush)  # (8)
        painter.setPen (currentPen)


class Dialog (QDialog) :
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


class QSSLoader :
    """
    创建一个加载QSS样式表的公共类
    """


    def __init__ (self) :
        pass


    @staticmethod
    def read_qss_file (qss_file_name) :
        with open (qss_file_name , 'r' , encoding = 'UTF-8') as file :
            return file.read ()


    def example_of_loading_qss (self) :
        """
        在代码中加载qss样式表的示例
        """
        app = QApplication (sys.argv)
        window = MainWindow ()

        style_file = './style.qss'
        style_sheet = QSSLoader.read_qss_file (style_file)
        window.setStyleSheet (style_sheet)

        window.show ()
        sys.exit (app.exec_ ())


# 创建了一个可编辑的ListWidget，在项目双击时启动编辑，编辑完成时隐藏编辑框
class Editable_ListWidget_Item (QListWidgetItem) :

    # 创建了一个可编辑的ListWidget，在项目双击时启动编辑，编辑完成时隐藏编辑框

    def __init__ (self) :
        super (Editable_ListWidget_Item , self).__init__ ()
        # 跟踪当前编辑的项目
        self.current_item = None

        self.itemDoubleClicked.connect (self.start_editing)
        self.editingFinished.connect (self.finish_editing)


    def start_editing (self , item) :
        """
        当item被双击的时候启动编辑
        """
        if isinstance (item , EditableListWidgetItem) :
            self.current_item = item
            item.setFlags (item.flags () | Qt.ItemIsEditable)
            item.show_editor ()
            self.setItemWidget (item , item.edit_line)
            item.edit_line.selectAll ()


    def finish_editing (self) :
        """
        当item失去聚焦的时候结束编辑
        """
        if self.current_item :
            edited_text = self.current_item.edit_line.text ()
            self.current_item.setText (edited_text)
            self.current_item.hide_editor ()
            self.current_item.setFlags (self.current_item.flags () & ~Qt.ItemIsEditable)
            self.current_item = None

#用来读取ui文件
def load_ui (file_path) :
    # 创建一个应用程序对象
    app = QApplication ([])

    # 创建QUiLoader实例
    loader = QUiLoader ()

    # 使用QUiLoader加载UI文件
    ui_file = QFile (file_path)
    ui_file.open (QFile.ReadOnly)
    ui_widget = loader.load (ui_file)
    ui_file.close ()

    # 返回加载的UI部件
    return ui_widget
    # #示例
    # # 加载UI文件
    # ui_file_path = "your_ui_file.ui"  # 替换为你的UI文件路径
    # ui_widget = load_ui (ui_file_path)
    #
    # # 设置UI部件为主窗口的中心部件
    # self.setCentralWidget (ui_widget)