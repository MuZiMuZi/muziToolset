# coding=utf-8
# 导入sys模块为了防止程序运行崩溃
# ui界面生成需要三个模块QtWidgets，QtGui，QtCore
from importlib import reload

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from . import config
from .ui.setup import bind_ui
from .ui.widget import base_widget , chainEP_widget , chain_widget , limb_widget , face_widget
from ..core import qtUtils


reload (base_widget)
reload (chain_widget)
reload (limb_widget)
reload (chainEP_widget)
reload (bind_ui)
reload (face_widget)

#item里存储的数据
# item_widget = item.data (Qt.UserRole)
# item_text = item.data (Qt.UserRole + 1)
# item_index = item.data (Qt.UserRole + 2)


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

        self.set_icon ()
        # 设置qss样式表
        self.setStyleSheet (qtUtils.QSSLoader.read_qss_file (config.qss_dir + './{}.qss'.format ('amoled')))


    def set_icon (self) :
        # 设置按钮的图标，美化界面

        orient_icon = QIcon (config.icon_dir + '/directions.png')
        self.orient_button.setIcon (orient_icon)
        # self.orient_button.setIconSize (orient_icon.actualSize (self.orient_button.size ()))

        delete_icon = QIcon (config.icon_dir + '/delete.png')
        self.delete_button.setIcon (delete_icon)
        # self.delete_button.setIconSize (delete_icon.actualSize (self.delete_button.size ()))

        reset_icon = QIcon (config.icon_dir + '/reset.png')
        self.reset_button.setIcon (reset_icon)
        # self.reset_button.setIconSize (reset_icon.actualSize (self.reset_button.size ()))

        build_icon = QIcon (config.icon_dir + '/control.png')
        self.build_button.setIcon (build_icon)
        self.build_button.setIconSize (build_icon.actualSize (self.build_button.size ()))


    def apply_model (self) :
        pass


    def add_connect (self) :
        u"""
        用来添加连接的槽函数
        """
        self.proxy_widget.doubleClicked.connect (self.clicked_proxy_widget_dbclk)

        # custom_widget 的连接
        self.custom_widget.setContextMenuPolicy (Qt.CustomContextMenu)
        self.custom_widget.customContextMenuRequested.connect (self.clicked_custom_widget_menu)
        self.custom_widget.itemClicked.connect (self.clicked_custom_widget_clk)

        # 连接action的槽函数
        self.action_Refersh.triggered.connect (self.triggered_action_Refersh)

        # 连接创建绑定的槽函数
        self.build_button.clicked.connect (self.clicked_build_btn)


    # 用来连接proxy_widget双击所连接的功能槽函数,双击的时候将模版库的模版添加到自定义模块里
    def clicked_proxy_widget_dbclk (self) :
        u"""
            用来连接proxy_widget双击所连接的功能槽函数,双击的时候将模版库的模版添加到自定义模块里
            index：鼠标双击的时候所在的位置
            """
        # 获取proxy_view双击时候的位置信息
        index = self.proxy_widget.currentIndex ()
        # 如果index.isValid的返回值有值的话，说明选择了可以点击的文件，不是的话则是空白的物体
        if index.isValid () :
            # 1.获取self.custom_widget里所拥有的所有item
            all_items = self.custom_widget.findItems ("*" , Qt.MatchWildcard)
            all_items_texts = [custom_item.text () for custom_item in all_items]

            # 获取item的模块名称
            item_text = self.proxy_widget.currentItem ().text ()
            # 利用count方法来获取item的模块名称出现过的次数
            item_index = all_items_texts.count ('side_{}'.format (item_text))

            # 获得proxy_widget里所选择的item_name
            item_name = 'bp_side_{}_{:03d}'.format (item_text , item_index + 1)
            # 在custom_widget里添加这个item
            item = QListWidgetItem (item_name)
            self.custom_widget.addItem (item)
            # 添加完成item后设置为选中模式
            self.custom_widget.setCurrentItem (item)
            # 设置字体颜色为红色
            item.setForeground (QColor (255 , 0 , 0))

            # 设置item的文本和索引
            #存储item的名称为item_text在Qt.UserRole + 1 里
            #存储item的序号为item_index在Qt.UserRole + 2里
            item.setData (Qt.UserRole + 1 , item_text)
            item.setData (Qt.UserRole + 2 , item_index)  # 存储索引值
            self.update_current (item)
        else :
            return


    # 用来连接custom_widget单击所连接的功能槽函数。单击按钮的时候可以切换到对应的模块设置
    def clicked_custom_widget_clk (self , item) :
        u"""
        用来连接custom_widget单击所连接的功能槽函数。单击按钮的时候可以切换到对应的模块设置
        item：鼠标单击的时候所在的位置
        """
        # 获取当前选中项目的索引
        selected_index = self.custom_widget.currentRow ()

        # 根据选中项目的索引切换到对应的属性设置面板
        self.setting_stack.setCurrentIndex (selected_index + 1)


    # 用来创建custom_widget右键的菜单
    def clicked_custom_widget_menu (self) :
        """
        用来创建custom_widget右键的菜单
        """
        custom_menu = QMenu ()
        # 添加右键菜单的设置
        custom_menu.addActions ([
            self.action_Mirror_select ,
            self.action_Mirror ,
            custom_menu.addSeparator () ,
            self.action_Upward ,
            self.action_Lowward ,
            self.action_Rename ,
            custom_menu.addSeparator () ,
            self.action_Delete ,
            self.action_Clear ,
            self.action_Refersh
        ])
        # 创建一个光标对象，在光标对象右击的位置运行这个右键菜单
        cursor = QCursor ()
        custom_menu.exec_ (cursor.pos ())


    # 获取proxy_widget所选择的项目，从而更新set_layout的面板
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


    # 根据所得知的item，创建setting_layout里对应的设置面板
    def initialize_field (self , item) :
        u"""
        根据所得知的item，创建对应的设置面板
        Returns:
        """
        #从item的data中获取对应的信息
        item_text = item.data (Qt.UserRole + 1)
        item_index = item.data (Qt.UserRole + 2)
        # 判断item的类型，根据item的类型选择生成哪个界面
        rigtype = config.Rigtype (item_text)


        if rigtype == 'custom' :
            item_widget = base_item_widget.main ()
        elif rigtype == 'chain' :
            item_widget = chain_item_widget.main ()
        elif rigtype == 'chainEP' :
            item_widget = chainEP_item_widget.main ()
        elif rigtype == 'limb' :
            item_widget = limb_item_widget.main ()
        elif rigtype == 'face' :
            item_widget = face_item_widget.main ()

        # 将item_widget与item关联
        item.setData (Qt.UserRole , item_widget)

        # 从item中获取关联的item_widget
        item_widget = item.data (Qt.UserRole)
        item_widget.module_edit.setText ('{}'.format (item_text))
        item_widget.index_edit.setText ('{}'.format (item_index + 1))
        self.setting_stack.additem_widget (item_widget)


    def clicked_build_btn (self) :
        """
        连接创建绑定按钮的槽函数
        """

        # 1.获取self.custom_widget里所拥有的所有item
        all_items = self.custom_widget.findItems ("*" , Qt.MatchWildcard)

        # 对所有item做循环遍历，根据item里面的信息来创建对应的绑定结构
        for item in all_items :
            item_widget = item.data(Qt.UserRole)
            item_widget.build_rig ()


    def triggered_action_Refersh (self) :
        """
        连接action_Refersh行为的槽函数，当按下这个行为键的时候刷新self.custom_widget里所有item的命名
        """
        # 1.获取self.custom_widget里所拥有的所有item
        all_items = self.custom_widget.findItems ("*" , Qt.MatchWildcard)
        all_items_texts = []
        # 对所有item做循环遍历，获取item.widget里的组件信息，module，side和name，用于重新命名item
        for item in all_items :
            all_items_texts.append (item.text ())
            module = item.widget.module_edit.text ()
            side = item.widget.side
            name = item.widget.name
            # 利用count方法来获取item的模块名称出现过的次数
            item_index = all_items_texts.count ('{}_{}'.format (side , item_text))

            item.setText ('bp_{}_{}{}_{:03d}'.format (side , module , name , item_index + 1))


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
        window.deleteLater ()
    except :
        pass
    window.setAttribute (Qt.WA_DeleteOnClose)
    window.show ()
