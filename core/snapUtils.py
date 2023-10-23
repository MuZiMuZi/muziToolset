# coding=utf-8
u"""
这是一个吸附的。用来吸附对应的位置。

实现的功能：

返回对象列表的位移中心位置：find_centerPos_pivot
返回对象列表的选择中心位置：find_centerRet_pivot
将要吸附中心位置的对象捕捉到对象列表的中心位置：snap_to_PosCenter
将要吸附中心旋转的对象捕捉到对象列表的中心旋转：snap_to_retCenter
根据选择的吸附模式，进行对应的吸附功能：snap

"""
# 导入所有需要的模块

from __future__ import unicode_literals , print_function

import maya.cmds as cmds


class Snap (object) :


    def __init__ (self , obj , objs_list , combo) :
        """
        Args:
            obj(object):Objects requiring adsorption position
            objs_list(list):List of objects used as positioning reference to adsorb positions
        """
        self.obj = obj
        self.objs_list = objs_list
        self.combo = combo


    def find_centerPos_pivot (self) :
        """返回对象列表的中心位置.

        Args:
            objs_list (list/None): 要查询中心位置的对象列表.

        Returns:
            objs_list: 对象列表的中心位置, [center_pos_x, center_pos_y, center_pos_z].

        """

        num_of_obj = len (self.objs_list)
        pos_x_all = 0
        pos_y_all = 0
        pos_z_all = 0
        if num_of_obj :
            for i in range (num_of_obj) :
                pos = cmds.xform (self.objs_list [i] , query = True , worldSpace = True , translation = True)
                pos_x_all += pos [0]
                pos_y_all += pos [1]
                pos_z_all += pos [2]

            center_pos_x = pos_x_all / num_of_obj
            center_pos_y = pos_y_all / num_of_obj
            center_pos_z = pos_z_all / num_of_obj

            return [center_pos_x , center_pos_y , center_pos_z]

        return [pos_x_all , pos_y_all , pos_z_all]


    def find_centerRet_pivot (self) :
        """返回对象列表的选择中心位置.

        Args:
            objs_list (list/None):要查询中心旋转的对象列表.

        Returns:
            objs_list: 对象列表的中心旋转, [center_Ret_x, center_Ret_y, center_Ret_z].

        """

        num_of_obj = len (self.objs_list)
        Ret_x_all = 0
        Ret_y_all = 0
        Ret_z_all = 0
        if num_of_obj :
            for i in range (num_of_obj) :
                ret = cmds.xform (self.objs_list [i] , query = True , worldSpace = True , rotation = True)
                Ret_x_all += ret [0]
                Ret_y_all += ret [1]
                Ret_z_all += ret [2]

            center_Ret_x = Ret_x_all / num_of_obj
            center_Ret_y = Ret_y_all / num_of_obj
            center_Ret_z = Ret_z_all / num_of_obj

            return [center_Ret_x , center_Ret_y , center_Ret_z]

        return [Ret_x_all , Ret_y_all , Ret_z_all]


    def snap_to_PosCenter (self) :
        """将要吸附中心位置的对象捕捉到对象列表的中心位置。

        Args:
            objs_list (list): 要查询中心位置的对象列表.
            obj (str): 要吸附中心位置的对象.

        """

        self.objs_list = [obj_node for obj_node in self.objs_list if cmds.objExists (obj_node)]
        if self.objs_list :
            center_pos = self.find_centerPos_pivot ()
            cmds.xform (self.obj , worldSpace = True , translation = center_pos)


    def snap_to_RetCenter (self) :
        """将要吸附中心旋转的对象捕捉到对象列表的中心旋转.

        Args:
            objs_list (list): 要查询中心旋转的对象列表.
            obj (str):要吸附中心旋转的对象.

        """

        self.objs_list = [obj_node for obj_node in self.objs_list if cmds.objExists (obj_node)]
        if self.objs_list :
            center_Ret = self.find_centerRet_pivot ()
            cmds.xform (self.obj , worldSpace = True , rotation = center_Ret)


    def snap (self) :
        """
        根据选择的吸附模式，进行对应的吸附功能
        :return:
        """
        if self.combo == 'Position + Rotation' :
            self.snap_to_PosCenter ()
            self.snap_to_RetCenter ()

        if self.combo == 'Position' :
            self.snap_to_PosCenter ()

        if self.combo == 'Rotation' :
            self.snap_to_RetCenter ()


    @staticmethod
    def push_snip () :
        sel_list = cmds.ls (selection = True , flatten = True)
        if len (sel_list) >= 1 :
            objs_list = sel_list [:-1]
            obj = sel_list [-1]
            combo_txt = 'Position + Rotation'
            i = Snap (obj , objs_list , combo_txt)
            i.snap ()
        else :
            cmds.warning ("请选择两个或以上的物体或者Cv点")
