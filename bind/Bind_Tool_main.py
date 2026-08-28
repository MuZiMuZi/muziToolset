# coding=utf-8
# 导入sys模块为了防止程序运行崩溃
# ui界面生成需要三个模块QtWidgets，QtGui，QtCore
from importlib import reload

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from . import config
from .ui.setup import bind_ui
from .ui.widget import base_widget , chainEP_widget , chain_widget , limb_widget , face_widget , bone_widget
from ..core import qtUtils


reload (base_widget)
reload (chain_widget)
reload (limb_widget)
reload (chainEP_widget)
reload (bind_ui)
reload (face_widget)
reload (bone_widget)
#帮助文档
#https://www.yuque.com/yuqueyonghur5eqgu/gpxuh5

class Bind_Widget (bind_ui.Ui_MainWindow , QMainWindow) :
    u'''
    用于创建绑定系统的界面系统
    '''
    item_dict = {}


    def __init__ (self , parent = qtUtils.get_maya_window ()) :
        super ().__init__ (parent)
        # 调用父层级的创建ui方法
        self.setupUi (self)

        self.add_connect ()

        self.set_icon ()
        # 设置qss样式表
        self.setStyleSheet (qtUtils.QSSLoader.read_qss_file (config.qss_dir + './{}.qss'.format ('amoled')))


    # 设置按钮的图标
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


    # 用来添加连接的槽函数
    def add_connect (self) :
        """
        用来添加连接的槽函数
        """
        # 连接proxy_widget的双击槽函数
        self.proxy_widget.doubleClicked.connect (self.clicked_proxy_widget_dbclk)

        # 连接custom_widget的右键菜单和点击槽函数
        self.custom_widget.setContextMenuPolicy (Qt.CustomContextMenu)
        self.custom_widget.customContextMenuRequested.connect (self.clicked_custom_widget_menu)
        self.custom_widget.itemClicked.connect (self.clicked_custom_widget_clk)

        # 连接action的槽函数
        self.action_Refersh.triggered.connect (self.triggered_action_Refersh)

        # 连接创建绑定的槽函数
        self.build_button.clicked.connect (self.clicked_build_btn)

        # 连接删除绑定的槽函数
        self.delete_button.clicked.connect (self.clicked_delete_btn)


    # 用来连接proxy_widget双击所连接的功能槽函数,双击的时候将模版库的模版添加到自定义模块里
    def clicked_proxy_widget_dbclk (self) :
        """
        用来连接proxy_widget双击所连接的功能槽函数,双击的时候将模版库的模版添加到自定义模块里
        """
        # 获取proxy_view双击时候的位置信息
        index = self.proxy_widget.currentIndex ()

        # 如果index.isValid的返回值有值的话，说明选择了可以点击的文件，不是的话则是空白的物体
        if index.isValid () :
            # 获取item的模块名称
            item_text = self.proxy_widget.currentItem ().text ()

            # 获取self.custom_widget里所拥有的所有item
            all_items = self.custom_widget.findItems ("*" , Qt.MatchWildcard)
            all_items_texts = [custom_item.text () for custom_item in all_items]

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
            # 存储item的名称为item_text在Qt.UserRole + 1 里
            # 存储item的序号为item_index在Qt.UserRole + 2里
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
        """
        根据所得知的item，创建对应的设置面板
        """
        # 从item的data中获取对应的信息
        item_text = item.data (Qt.UserRole + 1)
        item_index = item.data (Qt.UserRole + 2)

        # 根据item的类型选择生成哪个界面
        rigType = config.rigType (item_text)
        widget_mapping = {
            'bone' : bone_widget.main ,
            'base' : base_widget.main ,
            'chain' : chain_widget.main ,
            'chainEP' : chainEP_widget.main ,
            'limb' : limb_widget.main ,
            'face' : face_widget.main ,
        }

        if rigType in widget_mapping :
            # 使用映射表来获取对应的组件
            item_widget = widget_mapping [rigType] ()
            item_widget.rigType_edit.setText ('{}'.format (item_text))
            item_widget.index_edit.setText ('{}'.format (item_index + 1))
            item.setData (Qt.UserRole , item_widget)
            self.setting_stack.addWidget (item_widget)
        else :
            cmds.warning ("未知的rigType：{}".format (rigType))


    # 根据提供的处理函数对self.custom_widget中的所有item进行处理
    def process_items (self , process_function) :
        """
        根据提供的处理函数对self.custom_widget中的所有item进行处理
        """
        all_items = self.custom_widget.findItems ("*" , Qt.MatchWildcard)

        for item in all_items :
            item_widget = item.data (Qt.UserRole)
            process_function (item_widget)


    # 连接创建绑定按钮的槽函数
    def clicked_build_btn (self) :
        """
        连接创建绑定按钮的槽函数
        """
        self.process_items (lambda item_widget : item_widget.build_rig ())


    # 连接删除绑定按钮的槽函数
    def clicked_delete_btn (self) :
        """
        连接删除绑定按钮的槽函数
        """
        self.process_items (lambda item_widget : item_widget.delete_rig ())


    # 刷新self.custom_widget里所有item的命名
    def refresh_custom_widget_items (self) :
        """
        刷新self.custom_widget里所有item的命名
        """
        all_items = self.custom_widget.findItems ("*" , Qt.MatchWildcard)
        all_items_texts = []

        for item in all_items :
            all_items_texts.append (item.text ())
            item_widget = item.data (Qt.UserRole)
            module = item_widget.rigType_edit.text ()
            side = item_widget.side_cbox.currentText ()
            name = item_widget.name_edit.text ()

            # 利用count方法来获取item的模块名称出现过的次数
            item_index = all_items_texts.count ('{}_{}'.format (side , item.text ()))

            item.setText ('bp_{}_{}{}_{:03d}'.format (side , module , name , item_index + 1))


    # 连接action_Refersh行为的槽函数，当按下这个行为键的时候刷新self.custom_widget里所有item的命名
    def triggered_action_Refersh (self) :
        """
        连接action_Refersh行为的槽函数，当按下这个行为键的时候刷新self.custom_widget里所有item的命名
        """
        self.refresh_custom_widget_items ()


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
