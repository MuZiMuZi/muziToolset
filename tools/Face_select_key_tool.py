# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds


def maya_main_window () :
    main_window_ptr = omui.MQtUtil.mainWindow ()
    return wrapInstance (int (main_window_ptr) , QtWidgets.QWidget)


class Select_key_tool (QtWidgets.QDialog) :
    '''
    创建一个拾取驱动工具的窗口
    用法：用于拾取设置驱动关键帧的驱动工具
    '''
    def __init__ (self , parent = maya_main_window ()) :
        super (Select_key_tool , self).__init__ (parent)

        self.setWindowTitle (u'拾取驱动工具')

        self.initial_directory = cmds.internalVar (userPrefDir = True)  # 默认文件窗口打开路径
        self.initial_color = QtGui.QColor (255 , 0 , 0)  # 默认颜色窗口初始选择的颜色

        self.create_widgets ()
        self.create_layouts ()
        self.create_connections ()


    def create_widgets (self) :
        self.pick_driven_label = QtWidgets.QLabel (u'驱动控制器:')
        self.pick_driven_line = QtWidgets.QLineEdit ()
        self.pick_driven_btn = QtWidgets.QPushButton (u"拾取")

        self.execute_label = QtWidgets.QLabel (u'驱动属性:')
        self.execute_line = QtWidgets.QLineEdit ()
        self.execute_btn = QtWidgets.QPushButton (u"选择需要控制的控制器然后执行")


    def create_layouts (self) :
        """
        创建layout面板
        """
        self.main_layout = QtWidgets.QVBoxLayout (self)

        self.driver_layout = QtWidgets.QVBoxLayout ()
        self.main_layout.addLayout (self.driver_layout)

        self.driven_layout = QtWidgets.QHBoxLayout ()
        self.driven_layout.addWidget (self.pick_driven_label)
        self.driven_layout.addWidget (self.pick_driven_line)
        self.driven_layout.addWidget (self.pick_driven_btn)
        self.main_layout.addLayout (self.driven_layout)

        self.execute_layout = QtWidgets.QHBoxLayout ()
        self.execute_layout.addWidget (self.execute_label)
        self.execute_layout.addWidget (self.execute_line)
        self.execute_layout.addWidget (self.execute_btn)
        self.main_layout.addLayout (self.execute_layout)


    def create_connections (self) :
        # 创建按钮的槽函数链接
        self.pick_driven_btn.clicked.connect (self.clicked_pick_driven_btn)
        self.execute_btn.clicked.connect (self.clicked_execute_btn)


    def clicked_pick_driven_btn (self) :
        # 获取驱动的控制器名称

        self.driven_ctrl = cmds.ls (sl = True) [0]
        self.pick_driven_line.setText (self.driven_ctrl)
        # 取消选择的控制器
        cmds.select (clear = True)


    def clicked_execute_btn (self) :
        # 获取用来控制的属性
        self.driven_attr = self.execute_line.text ()
        # 判断驱动的控制器上是否有对应的属性，如果没有的话则添加，有的话则跳过
        if not cmds.objExists ('{}.{}'.format (self.driven_ctrl , self.driven_attr)) :
            cmds.addAttr ('{}'.format (self.driven_ctrl) , ln = '{}'.format (self.driven_attr) ,
                          attributeType = 'float' , min = 0 , max = 10 , keyable = True)

        # 给控制器上层添加一个驱动组
        self.driver_ctrls = cmds.ls (sl = True)

        # 检查是否符合条件，可以进行添加控制
        # 1.检查是否有用来控制的属性
        if self.driven_attr :
            self.driven_value = True
        else :
            self.driven_value = False

        # 2.检查是否有需要驱动的控制器
        if self.driver_ctrls :
            self.driven_value = True
        else :
            self.driven_value = False
        # 检查如果符合条件的话则进行下一步
        if self.driven_value :
            driver_grps = []
            for ctrl in self.driver_ctrls :
                driver_grp = add_extra_group (obj = ctrl , grp_name = '{}_driver'.format (ctrl) , world_orient = False)
                driver_grps.append (driver_grp)

            # 给上层的驱动组K驱动关键帧
            # 设置最大值的驱动关键帧
            attrs = ['translateX' , 'translateY' , 'translateZ' , 'rotateX' , 'rotateY' , 'rotateZ']
            scale_attrs = ['scaleX' , 'scaleY' , 'scaleZ']
            for driver_grp in driver_grps :
                for attr in attrs :
                    cmds.setAttr (self.driven_ctrl + '.{}'.format (self.driven_attr) , 10)
                    cmds.setDrivenKeyframe (driver_grp + '.{}'.format (attr) ,
                                            cd = self.driven_ctrl + '.{}'.format (self.driven_attr))

                    # 将驱动属性和控制器的属性归零后再重新设置驱动关键帧，这是位移旋转属性
                    cmds.setAttr (self.driven_ctrl + '.{}'.format (self.driven_attr) , 0)
                    cmds.setAttr (driver_grp + '.{}'.format (attr) , 0)
                    cmds.setDrivenKeyframe (driver_grp + '.{}'.format (attr) ,
                                            cd = self.driven_ctrl + '.{}'.format (self.driven_attr))
                for scale_attr in scale_attrs :
                    cmds.setAttr (self.driven_ctrl + '.{}'.format (self.driven_attr) , 10)
                    cmds.setDrivenKeyframe (driver_grp + '.{}'.format (scale_attr) ,
                                            cd = self.driven_ctrl + '.{}'.format (self.driven_attr))

                    # 将驱动属性的属性归一后再重新设置驱动关键帧，这是缩放属性
                    cmds.setAttr (self.driven_ctrl + '.{}'.format (self.driven_attr) , 0)
                    cmds.setAttr (driver_grp + '.{}'.format (scale_attr) , 1)
                    cmds.setDrivenKeyframe (driver_grp + '.{}'.format (scale_attr) ,
                                            cd = self.driven_ctrl + '.{}'.format (self.driven_attr))
        else :
            # 如果不符合条件的话则报错
            cmds.warning (u'请检查是否给定驱动的属性或者是否选择了被驱动的控制器')


def add_extra_group (obj , grp_name , world_orient = False) :
    """
    在对象上方添加一个额外的组.

    Args:
        obj (str): 要添加额外组的Maya对象.
        grp_name (str): 额外的组名
        world_orient (bool): 设置新组的世界位置是否改变。

    Returns:
        str: 新添加的组.
    """
    # 判断额外的组名是否存在
    if cmds.objExists (grp_name) :
        # 如果存在的话则不再创建新的额外组
        return
    else :
        # 创建新组
        obj_grp = cmds.group (name = grp_name , empty = True)

        # 获取对象的世界空间位置、旋转和缩放信息
        t_pos = cmds.xform (obj , query = True , worldSpace = True , translation = True)
        r_pos = cmds.xform (obj , query = True , worldSpace = True , rotation = True)

        # 如果设置了世界定位参数，将旋转信息设为零
        if world_orient :
            r_pos = [0 , 0 , 0]

        s_pos = cmds.xform (obj , q = True , worldSpace = True , s = True)

        # 将新组的缩放、位置和旋转信息设置为对象的相应信息
        cmds.xform (obj_grp , s = s_pos)
        cmds.xform (obj_grp , ws = True , t = t_pos)
        cmds.xform (obj_grp , ws = True , ro = r_pos)

        obj_parent = cmds.listRelatives (obj , parent = True)

        # 如果对象有父物体，将新组和对象一起父物体
        if obj_parent :
            cmds.parent (obj_grp , obj_parent [0] , absolute = True)
            cmds.parent (obj , obj_grp , absolute = True)
        else :
            cmds.parent (obj , obj_grp , absolute = True)

        return obj_grp


if __name__ == '__main__' :
    try :
        ui.close ()
        ui.deleteLater ()
    except :
        pass
    ui = Select_key_tool ()
    ui.show ()
