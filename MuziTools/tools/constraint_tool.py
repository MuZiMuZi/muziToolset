#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Maya 约束工具 - Constraint Tool
================================
功能：在 Maya 中快速创建各种约束（父子、点、方向、缩放、目标、极向量）
兼容：Maya 2020+ (PySide2 / PySide6)
用法：
    1. 在 Maya 脚本编辑器的 Python 标签页中全选运行
    2. 或保存为 .py 文件，拖到 Maya 工具架上作为按钮
"""

# =============================================================================
#  导入模块
# =============================================================================
# 尝试导入 PySide2（Maya 2020~2024 使用），如果失败则导入 PySide6（Maya 2025+ 使用）
try :
    from PySide2.QtCore import *      # Qt 核心类：信号、事件、枚举等
    from PySide2.QtGui import *       # GUI 基础类：图标、颜色、字体等
    from PySide2.QtWidgets import *   # 界面部件类：按钮、标签、布局等
    from shiboken2 import wrapInstance  # 用于将 Maya 的 C++ 指针转为 Python 对象
except ImportError :
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from shiboken6 import wrapInstance

import maya.cmds as cmds   # Maya 核心命令模块，用于操作场景中的对象
import maya.mel as mel     # Maya MEL 语言接口，用于调用 MEL 脚本
import maya.OpenMayaUI as omui  # Maya UI 接口，用于获取主窗口指针


# =============================================================================
#  工具函数：获取 Maya 主窗口
# =============================================================================
def get_maya_main_window () :
    """
    获取 Maya 的主窗口对象，作为工具的父窗口
    这样工具窗口就不会跑到 Maya 主窗口的后面去
    """
    # MQtUtil.mainWindow() 返回 Maya 主窗口的内存地址（长整型指针）
    ptr = omui.MQtUtil.mainWindow ()
    # 如果指针有效，用 wrapInstance 把它包装成 Python 的 QWidget 对象
    if ptr is not None :
        return wrapInstance (int (ptr) , QWidget)
    # 如果获取失败，返回 None（一般不会发生）
    return None


# =============================================================================
#  主工具类
# =============================================================================
class Constraint_Tool (QWidget) :
    """
    约束工具的主类
    继承自 QWidget，是一个可以嵌入 Maya 的浮动面板
    """

    def __init__ (self , parent = None) :
        """
        构造函数：初始化工具窗口
        parent: 父窗口，如果不传则自动获取 Maya 主窗口
        """
        # 如果没有传入父窗口，自动获取 Maya 主窗口
        # 这一步很重要，否则窗口会显示不出来或者被 Maya 挡住
        if parent is None :
            parent = get_maya_main_window ()

        # 调用父类 QWidget 的构造函数
        super (Constraint_Tool , self).__init__ (parent)

        # 设置窗口属性
        self.setWindowTitle ("约束工具")          # 窗口标题栏显示的文字
        self.setWindowFlags (Qt.Window)           # 设置为独立窗口（不是内嵌面板），这样才能在 Maya 中正常显示
        self.setMinimumWidth (320)                # 窗口最小宽度，防止被压得太窄

        # 依次调用三个方法，分别创建界面部件、布局、信号连接
        self.create_widgets ()      # 创建按钮、标签、复选框等 UI 部件
        self.create_layouts ()      # 用布局管理器排列这些部件
        self.create_connections ()  # 把按钮的点击事件连接到对应的处理函数


    # =========================================================================
    #  创建 UI 部件
    # =========================================================================
    def create_widgets (self) :
        """
        创建所有需要的小部件（按钮、标签、复选框、单选按钮）
        """
        # --- 区域标题标签 ---
        # 创建一个 QLabel 作为标题，显示在界面上方
        self.constraint_objects_label = QLabel ("--------------约束工具--------------")
        # 设置文字颜色为浅绿色（RGB: 169, 255, 175）
        self.constraint_objects_label.setStyleSheet (u"color: rgb(169, 255, 175);")

        # --- 约束模式选择 ---
        # 单选按钮：多对1 模式（默认选中）
        # 含义：选择多个物体，最后一个物体被前面的物体约束
        self.mult_to_one_radio = QRadioButton ('mult_to_one(多对1)')
        self.mult_to_one_radio.setChecked (True)   # 默认选中这个选项

        # 单选按钮：1对多 模式
        # 含义：选择多个物体，第一个物体约束后面所有的物体
        self.one_to_mult_radio = QRadioButton ('one_to_mult(1对多)')

        # --- 保持偏移复选框 ---
        # 勾选后创建约束时会保留物体当前的相对位置/旋转/缩放偏移
        # 不勾选则会把被驱动者直接吸附到驱动者的位置上
        self.maintainOffset_checkBox = QCheckBox ('保持偏移')
        self.maintainOffset_checkBox.setChecked (True)   # 默认勾选

        # --- 约束类型按钮 ---
        # 每个按钮都带有一个 Maya 内置的约束图标
        # 点击后会在场景中创建对应类型的约束
        self.parent_constraint_btn = QPushButton (QIcon (':parentConstraint.png') , '父子约束')
        self.point_constraint_btn = QPushButton (QIcon (':posConstraint.png') , '点约束')
        self.orient_constraint_btn = QPushButton (QIcon (':orientConstraint.png') , '方向约束')
        self.scale_constraint_btn = QPushButton (QIcon (':scaleConstraint.png') , '缩放约束')
        self.aim_constraint_btn = QPushButton (QIcon (':aimConstraint.png') , '目标约束')
        self.pole_vector_constraint_btn = QPushButton (QIcon (':poleVectorConstraint.png') , '极向量约束')

        # --- 辅助操作按钮 ---
        # 选择约束：选中当前物体上所有的约束节点
        self.select_constraint_btn = QPushButton (QIcon (':menuIconModify.png') , '选择约束')
        # 删除约束：删除当前物体上所有的约束
        self.delete_constraint_btn = QPushButton (QIcon (':menuIconModify.png') , '删除约束')

        # 把所有约束相关的按钮放到一个列表里，方便后续批量添加到网格布局中
        self.constraint_btns = [
            self.parent_constraint_btn ,
            self.point_constraint_btn ,
            self.orient_constraint_btn ,
            self.scale_constraint_btn ,
            self.aim_constraint_btn ,
            self.pole_vector_constraint_btn ,
            self.select_constraint_btn ,
            self.delete_constraint_btn
        ]


    # =========================================================================
    #  创建布局
    # =========================================================================
    def create_layouts (self) :
        """
        用布局管理器（Layout）把上面创建的部件排列到窗口中
        """
        # --- 模式选择行 ---
        # 用水平布局把单选按钮和复选框放在同一行
        self.maintainOffset_layout = QHBoxLayout ()
        self.maintainOffset_layout.addWidget (self.mult_to_one_radio)      # 添加多对1单选按钮
        self.maintainOffset_layout.addWidget (self.one_to_mult_radio)      # 添加1对多单选按钮
        self.maintainOffset_layout.addStretch ()                           # 添加弹性空间，把后面的部件推到右边
        self.maintainOffset_layout.addWidget (self.maintainOffset_checkBox) # 添加保持偏移复选框
        self.maintainOffset_layout.addStretch ()                           # 再添加弹性空间，让复选框居中一点

        # --- 约束按钮网格 ---
        # 用网格布局（QGridLayout）把 8 个按钮排列成网格状
        self.constraint_layout = QGridLayout ()
        # 调用专门的方法把按钮添加到网格中
        self.create_constraint_layout ()

        # --- 约束区域总布局 ---
        # 用垂直布局把模式选择行和按钮网格组合在一起
        self.constraint_objects_layout = QVBoxLayout ()
        self.constraint_objects_layout.addLayout (self.maintainOffset_layout)
        self.constraint_objects_layout.addLayout (self.constraint_layout)

        # --- 主窗口总布局 ---
        # 这是整个窗口的根布局，所有内容都加到这里
        self.main_layout = QVBoxLayout (self)
        self.main_layout.addWidget (self.constraint_objects_label)    # 先放标题标签
        self.main_layout.addLayout (self.constraint_objects_layout)   # 再放约束区域
        self.main_layout.addStretch ()                                # 底部添加弹性空间，让内容靠上对齐


    # =========================================================================
    #  信号连接
    # =========================================================================
    def create_connections (self) :
        """
        连接按钮的点击信号（clicked）到对应的处理函数（槽函数）
        这样点击按钮时就会执行对应的操作
        """
        # 父子约束按钮 -> 调用 clicked_parent_constraint_btn 方法
        self.parent_constraint_btn.clicked.connect (self.clicked_parent_constraint_btn)
        # 点约束按钮 -> 调用 clicked_point_constraint_btn 方法
        self.point_constraint_btn.clicked.connect (self.clicked_point_constraint_btn)
        # 方向约束按钮 -> 调用 clicked_orient_constraint_btn 方法
        self.orient_constraint_btn.clicked.connect (self.clicked_orient_constraint_btn)
        # 缩放约束按钮 -> 调用 clicked_scale_constraint_btn 方法
        self.scale_constraint_btn.clicked.connect (self.clicked_scale_constraint_btn)
        # 目标约束按钮 -> 直接执行 MEL 命令（Maya 内置的目标约束创建流程）
        self.aim_constraint_btn.clicked.connect (lambda : mel.eval ("performAimConstraint 0;"))
        # 极向量约束按钮 -> 调用 clicked_pole_vector_constraint_btn 方法
        self.pole_vector_constraint_btn.clicked.connect (self.clicked_pole_vector_constraint_btn)
        # 选择约束按钮 -> 调用 clicked_select_constraint_btn 方法
        self.select_constraint_btn.clicked.connect (self.clicked_select_constraint_btn)
        # 删除约束按钮 -> 调用 clicked_delete_constraint_btn 方法
        self.delete_constraint_btn.clicked.connect (self.clicked_delete_constraint_btn)


    # =========================================================================
    #  核心辅助方法：获取驱动者和被驱动者
    # =========================================================================
    def get_driver_driven_obj (self) :
        """
        根据当前选择的约束模式（多对1 或 1对多），从当前选择的物体中分出驱动者和被驱动者

        返回：
            (driver, driven) 元组
            - mult_to_one 模式：driver 是列表（前面多个物体），driven 是字符串（最后一个物体）
            - one_to_mult 模式：driver 是字符串（第一个物体），driven 是列表（后面多个物体）
        """
        # 获取当前选择的物体列表（long=True 返回完整路径名，避免重名问题）
        obj_list = cmds.ls (selection = True , long = True)

        # 如果选择的物体少于 2 个，无法创建约束，弹出警告并返回 None
        if len (obj_list) < 2 :
            cmds.warning ("请至少选择两个物体！")
            return None , None

        # 判断当前选中的模式
        if self.mult_to_one_radio.isChecked () :
            # 多对1模式：前面所有物体是驱动者，最后一个物体是被驱动者
            driver = obj_list [0 :-1]   # 切片：从第0个到倒数第1个（不含最后一个）
            driven = obj_list [-1]       # 最后一个元素
        else :
            # 1对多模式：第一个物体是驱动者，后面所有物体是被驱动者
            driver = obj_list [0]        # 第一个元素
            driven = obj_list [1 :]      # 切片：从第1个到最后一个

        return driver , driven


    # =========================================================================
    #  布局辅助方法：把按钮放入网格
    # =========================================================================
    def create_constraint_layout (self) :
        """
        把约束按钮列表按顺序放入 QGridLayout 网格布局中
        每行放 3 个按钮，自动换行
        """
        # 生成网格坐标：5行 x 3列，生成 [(0,0), (0,1), (0,2), (1,0), (1,1), ...]
        positions = [(i , j) for i in range (5) for j in range (3)]
        # 用 zip 把坐标和按钮一一配对，然后逐个添加到网格中
        for position , button in zip (positions , self.constraint_btns) :
            self.constraint_layout.addWidget (button , *position)


    # =========================================================================
    #  按钮处理函数：父子约束
    # =========================================================================
    def clicked_parent_constraint_btn (self) :
        """
        点击"父子约束"按钮时执行
        根据当前模式（多对1 或 1对多）批量创建父子约束
        """
        # 获取驱动者和被驱动者
        driver , driven = self.get_driver_driven_obj ()
        # 如果选择不足2个物体，get_driver_driven_obj 会返回 (None, None)，直接退出
        if driver is None :
            return

        # 读取"保持偏移"复选框的状态（True 或 False）
        mo_value = self.maintainOffset_checkBox.isChecked ()

        # 打开 Maya 的撤销块，这样用户可以用 Ctrl+Z 撤销这次操作
        cmds.undoInfo (openChunk = True , chunkName = "ParentConstraint")
        try :
            # 根据模式分别处理
            if self.mult_to_one_radio.isChecked () :
                # 多对1：cmds.parentConstraint 支持传入列表作为驱动者
                cmds.parentConstraint (driver , driven , maintainOffset = mo_value)
            else :
                # 1对多：逐个为每个被驱动者创建约束
                for i in driven :
                    cmds.parentConstraint (driver , i , maintainOffset = mo_value)
        except Exception as e :
            # 如果创建过程中出错（比如物体不存在），弹出警告
            cmds.warning (str (e))
        finally :
            # 无论成功还是失败，都要关闭撤销块
            cmds.undoInfo (closeChunk = True)


    # =========================================================================
    #  按钮处理函数：点约束
    # =========================================================================
    def clicked_point_constraint_btn (self) :
        """
        点击"点约束"按钮时执行
        只约束位置（平移），不约束旋转和缩放
        """
        driver , driven = self.get_driver_driven_obj ()
        if driver is None :
            return
        mo_value = self.maintainOffset_checkBox.isChecked ()

        cmds.undoInfo (openChunk = True , chunkName = "PointConstraint")
        try :
            # 判断 driven 是列表还是单个字符串
            # 多对1模式下 driven 是字符串，1对多模式下 driven 是列表
            if isinstance (driven , list) :
                # 1对多：遍历列表，逐个创建
                for i in driven :
                    cmds.pointConstraint (driver , i , maintainOffset = mo_value)
            else :
                # 多对1：直接创建
                cmds.pointConstraint (driver , driven , maintainOffset = mo_value)
        except Exception as e :
            cmds.warning (str (e))
        finally :
            cmds.undoInfo (closeChunk = True)


    # =========================================================================
    #  按钮处理函数：方向约束
    # =========================================================================
    def clicked_orient_constraint_btn (self) :
        """
        点击"方向约束"按钮时执行
        只约束旋转，不约束位置和缩放
        """
        driver , driven = self.get_driver_driven_obj ()
        if driver is None :
            return
        mo_value = self.maintainOffset_checkBox.isChecked ()

        cmds.undoInfo (openChunk = True , chunkName = "OrientConstraint")
        try :
            if isinstance (driven , list) :
                for i in driven :
                    cmds.orientConstraint (driver , i , maintainOffset = mo_value)
            else :
                cmds.orientConstraint (driver , driven , maintainOffset = mo_value)
        except Exception as e :
            cmds.warning (str (e))
        finally :
            cmds.undoInfo (closeChunk = True)


    # =========================================================================
    #  按钮处理函数：缩放约束
    # =========================================================================
    def clicked_scale_constraint_btn (self) :
        """
        点击"缩放约束"按钮时执行
        只约束缩放，不约束位置和旋转
        """
        driver , driven = self.get_driver_driven_obj ()
        if driver is None :
            return
        mo_value = self.maintainOffset_checkBox.isChecked ()

        cmds.undoInfo (openChunk = True , chunkName = "ScaleConstraint")
        try :
            if isinstance (driven , list) :
                for i in driven :
                    cmds.scaleConstraint (driver , i , maintainOffset = mo_value)
            else :
                cmds.scaleConstraint (driver , driven , maintainOffset = mo_value)
        except Exception as e :
            cmds.warning (str (e))
        finally :
            cmds.undoInfo (closeChunk = True)


    # =========================================================================
    #  按钮处理函数：极向量约束
    # =========================================================================
    def clicked_pole_vector_constraint_btn (self) :
        """
        点击"极向量约束"按钮时执行
        极向量约束比较特殊：它只能有 1 个驱动者和 1 个被驱动者（IK手柄）
        所以需要恰好选择 2 个物体
        """
        # 极向量约束不通过 get_driver_driven_obj 处理，因为它只支持 1对1
        obj_list = cmds.ls (selection = True , long = True)
        if len (obj_list) != 2 :
            cmds.warning ("极向量约束需要恰好选择两个物体：控制器 -> IK手柄")
            return

        cmds.undoInfo (openChunk = True , chunkName = "PoleVectorConstraint")
        try :
            # cmds.poleVectorConstraint(驱动者, 被驱动者)
            # 这里假设用户先选控制器，再选 IK 手柄
            cmds.poleVectorConstraint (obj_list [0] , obj_list [1])
        except Exception as e :
            cmds.warning (str (e))
        finally :
            cmds.undoInfo (closeChunk = True)


    # =========================================================================
    #  按钮处理函数：选择约束
    # =========================================================================
    def clicked_select_constraint_btn (self) :
        """
        点击"选择约束"按钮时执行
        查找当前选中物体上连接的所有约束节点，并选中它们
        """
        # 获取当前选择的物体
        obj_list = cmds.ls (selection = True , long = True)
        if not obj_list :
            cmds.warning ("请先选择物体！")
            return

        # 定义所有约束类型的节点名称
        cst_types = [
            "parentConstraint" ,    # 父子约束
            "pointConstraint" ,     # 点约束
            "orientConstraint" ,    # 方向约束
            "scaleConstraint" ,     # 缩放约束
            "aimConstraint" ,       # 目标约束
            "poleVectorConstraint"  # 极向量约束
        ]

        # 收集所有找到的约束节点
        constraints = []
        for obj in obj_list :
            for cst in cst_types :
                # listConnections 查找与物体有连接的指定类型节点
                # source=True, destination=False 表示查找输入连接（约束节点 -> 物体）
                nodes = cmds.listConnections (obj , type = cst) or []
                constraints.extend (nodes)

        # 如果有找到约束节点
        if constraints :
            # 用 set 去重（一个约束可能同时连接多个属性），再转回列表
            unique_constraints = list (set (constraints))
            # 选中这些约束节点
            cmds.select (unique_constraints , replace = True)
            print ("[选择约束] 已选中 {} 个约束节点".format (len (unique_constraints)))
        else :
            cmds.warning ("未找到约束节点")


    # =========================================================================
    #  按钮处理函数：删除约束
    # =========================================================================
    def clicked_delete_constraint_btn (self) :
        """
        点击"删除约束"按钮时执行
        删除当前选中物体上连接的所有约束节点
        """
        obj_list = cmds.ls (selection = True , long = True)
        if not obj_list :
            cmds.warning ("请先选择物体！")
            return

        cmds.undoInfo (openChunk = True , chunkName = "DeleteConstraints")
        try :
            # 所有约束类型
            cst_types = [
                "parentConstraint" ,
                "pointConstraint" ,
                "orientConstraint" ,
                "scaleConstraint" ,
                "aimConstraint" ,
                "poleVectorConstraint"
            ]
            count = 0   # 统计删除的约束数量

            for obj in obj_list :
                for cst in cst_types :
                    # 查找与物体连接的约束节点
                    nodes = cmds.listConnections (obj , type = cst) or []
                    for node in nodes :
                        # 先检查节点是否还存在（可能已经被前面的循环删掉了）
                        if cmds.objExists (node) :
                            cmds.delete (node)   # 删除约束节点
                            count += 1

            print ("[删除约束] 共删除 {} 个约束节点".format (count))
        except Exception as e :
            cmds.warning (str (e))
        finally :
            cmds.undoInfo (closeChunk = True)


# =============================================================================
#  显示窗口的函数
# =============================================================================
def main () :
    """
    显示约束工具窗口
    如果窗口已经存在，先关闭旧窗口再创建新窗口
    """
    # 使用全局变量保存窗口实例，这样下次调用时可以找到并关闭旧窗口
    global constraint_tool_window

    # 尝试关闭并删除旧窗口（如果存在的话）
    try :
        constraint_tool_window.close ()
        constraint_tool_window.deleteLater ()
    except :
        # 如果窗口不存在或已经被删除，会抛出异常，直接忽略
        pass

    # 创建新的工具窗口实例
    constraint_tool_window = Constraint_Tool ()
    # 显示窗口
    constraint_tool_window.show ()
    # raise_() 把窗口提升到最前面，防止被其他窗口挡住
    constraint_tool_window.raise_ ()
    # activateWindow() 激活窗口，让它获得焦点
    constraint_tool_window.activateWindow ()
    return constraint_tool_window


# =============================================================================
#  脚本直接运行时自动打开窗口
# =============================================================================
if __name__ == "__main__" :
    # 当在 Maya 脚本编辑器中直接运行这段代码时，自动调用 main() 显示窗口
    main ()