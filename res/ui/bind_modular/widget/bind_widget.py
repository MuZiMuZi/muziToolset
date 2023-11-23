# coding=utf-8
# 导入sys模块为了防止程序运行崩溃
# ui界面生成需要三个模块QtWidgets，QtGui，QtCore
from importlib import reload

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


from . import base_widget , chainEP_widget , chain_widget , limb_widget
from ..ui import bind_ui
from .....core import qtUtils


rigtype_custom = ['base']
rigtype_chain = ['chainFK' , 'chainIK' , 'chainIKFK' , 'finger' , 'spine']
rigtype_chainEP = ['chainEP']
rigtype_limb = ['arm' , 'leg' , 'hand' , 'tail' , 'spine']

reload (base_widget)
reload (chain_widget)
reload (bind_ui)
reload (limb_widget)
reload (chainEP_widget)


class Bind_Widget (bind_ui.Ui_MainWindow , QMainWindow) :
    u'''
    用于创建绑定系统的界面系统
    '''
    item_dict = {}


    def __init__ (self , parent = qtUtils.get_maya_window ()) :
        super ().__init__ (parent)
        # 调用父层级的创建ui方法
        self.setupUi (self)
        self.apply_model ()

        self.add_connect ()


    def apply_model (self) :
        u"""
        添加模型到view里
        """
        pass


    def add_connect (self) :
        u"""
        用来添加连接的槽函数
        """
        self.proxy_widget.doubleClicked.connect (self.cmd_proxy_widget_dbclk)

        # custom_widget 的连接
        self.custom_widget.setContextMenuPolicy (Qt.CustomContextMenu)
        self.custom_widget.customContextMenuRequested.connect (self.cmd_custom_widget_menu)
        # self.custom_widget.itemDoubleClicked.connect(self.cmd_custom_widget_menu)
        self.custom_widget.itemClicked.connect (self.cmd_custom_widget_clk)


    def cmd_proxy_widget_dbclk (self) :
        u"""
        用来连接proxy_widget双击所连接的功能槽函数,双击的时候将模版库的模版添加到自定义模块里
        index：鼠标双击的时候所在的位置
        """
        # 获取proxy_view双击时候的位置信息
        index = self.proxy_widget.currentIndex ()
        # 如果index.isValid的返回值有值的话，说明选择了可以点击的文件，不是的话则是空白的物体
        if index.isValid () :
            select_index = index.row ()
            # 获得proxy_widget里所选择的item_name
            item_name = self.proxy_widget.currentItem ().text () [0 :-3]
            # 在custom_widget里添加这个item
            item = QListWidgetItem (item_name)
            self.custom_widget.addItem (item)
            item.text = item_name
            self.update_current (item)
        else :
            return





    def cmd_custom_widget_clk (self , item) :
        u"""
        用来连接custom_widget单击所连接的功能槽函数。
        单击按钮的时候可以切换到对应的模块设置
        item：鼠标单击的时候所在的位置
        """
        # 获取当前选中项目的索引
        selected_index = self.custom_widget.currentRow ()

        # 根据选中项目的索引切换到对应的属性设置面板
        self.setting_stack.setCurrentIndex (selected_index + 1)


    def cmd_custom_widget_dbclk(self,item):
        """
        用来连接custom_widget双击所连接的功能槽函数。
        双击的时候可以修改item的名称，并且在离开聚焦的时候取消重命名
        """
        self.proxy_widget.currentItem ().text () [0 :-3]


    def cmd_custom_widget_menu (self) :
        """
        用来创建custom_widget右键的菜单
        """
        custom_menu = QMenu ()
        #添加右键菜单的设置
        custom_menu.addActions ([
            self.action_Mirror_select ,
            self.action_Mirror ,
            custom_menu.addSeparator () ,
            self.action_Upward ,
            self.action_Lowward ,
            self.action_Rename ,
            custom_menu.addSeparator () ,
            self.action_Delete ,
            self.action_Clear
        ])
        # 创建一个光标对象，在光标对象右击的位置运行这个右键菜单
        cursor = QCursor ()
        custom_menu.exec_ (cursor.pos ())


    def close_edit (self) :
        u"""
        关闭edit
        """
        if not self.edited_item :
            self.closePersistentEditor (self.edited_item)


    def update_current (self , item) :
        u"""
        获取proxy_widget所选择的项目，从而更新set_layout的面板
        Args:
            item:

        Returns:

        """
        self.item = item
        self.initialize_field (item)
        # 获取custom_widget 里的item数量，切换到对应的设置面板
        index = self.custom_widget.count ()
        self.setting_stack.setCurrentIndex (index)


    def initialize_field (self , item) :
        u"""
        根据所得知的item，创建对应的设置面板
        Returns:

        """
        base = base_widget.Base_Widget ()
        self.base_widget = base.base_widget
        base.module_edit.setText ('{}'.format (item.text))
        self.setting_stack.addWidget (self.base_widget)


def show () :
    # 添加了销毁机制，如果之前有创建过这个窗口的话则先删除再创建新的窗口
    global win
    try :
        win.close ()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
        win.deleteLater ()
    except :
        pass
    win = Bind_Widget ()
    win.show ()


if __name__ == "__main__" :
    # 添加了销毁机制，如果之前有创建过这个窗口的话则先删除再创建新的窗口
    window = Bind_Widget ()
    # 添加了销毁机制，如果之前有创建过这个窗口的话则先删除再创建新的窗口
    try :
        window.close ()
        window.deleteLater()
    except :
        pass
    window.setAttribute (Qt.WA_DeleteOnClose)
    window.show ()
