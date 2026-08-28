# coding=utf-8
from importlib import reload

import maya.cmds as cmds

from . import foot
from ...module.limb import limbIKFK


reload (foot)
reload (limbIKFK)


class Leg (limbIKFK.LimbIKFK) :
    rig_type = 'Leg'
    axis = 'Z+'


    def __init__ (self , side , name , jnt_number = 3 , axis = 'X+' , length = 15 ,
                  limbtype = 'leg' ,
                  jnt_parent = None , ctrl_parent = None) :
        """
        创建腿部的四肢关节的绑定系统。

        参数：
        - side (str): 侧边，如'left'或'right'。
        - name (str): 四肢的名称。
        - jnt_number (int): 关节数量，默认为3。
        - axis (list): 四肢的朝向，默认为[0, 1, 0]。
        - length (float): 四肢的长度，默认为15。
        - limbtype (str): 四肢的类型，如'arm'或'leg'。
        - jnt_parent (str): 四肢所对应的关节的父对象。
        - ctrl_parent (str): 四肢所对应的控制器的父对象。

        返回：
        无，但会调用父类的构造函数
        """
        super ().__init__ (side , name , jnt_number , axis , length , limbtype , jnt_parent ,
                           ctrl_parent)


    def _init_extra (self) :
        """
        初始化脚掌模块，作为 rig 设置的一部分。

        Returns:
            None
        """
        super ()._init_extra ()

        # 初始化脚部 Limb 模块
        self.foot_limb = foot.Foot (self.side , self.name , jnt_number = 3 , length = 6 , jnt_parent = None ,
                                    ctrl_parent = None)
        self.foot_limb.rig_type = 'foot'
        self.foot_limb._init_extra ()


    def _create_ctrl_grp (self) :
        super ()._create_ctrl_grp ()

        self.foot_limb._create_ctrl_grp ()


    def _create_base_namespace (self) :
        """
        创建基础的命名空间。

        Returns:
            None
        """
        super ()._create_base_namespace ()

        # 调用脚部 Limb 模块的基础命名空间创建方法
        self.foot_limb._create_base_namespace ()


    def _create_extra_namespace (self) :
        """
        创建额外的命名空间和规范。

        Returns:
            None
        """
        super ()._create_extra_namespace ()

        # 调用脚部 Limb 模块的额外命名空间创建方法
        self.foot_limb._create_extra_namespace ()


    def _create_base_bpjnt (self) :
        """
               创建用于定位的bp关节。

               Returns:
                   None
               """
        # 导入定位的关节
        self._import_base_bpjnt ()

        # 修改定位关节组的名称
        self._rename_base_bpjnt ()

        # 设置默认的定位关节的属性
        self._set_base_bpjnt ()
        # 调用脚部 Limb 模块的额外 bp 关节创建方法
        self.foot_limb._create_base_bpjnt ()


    def _create_extra_bpjnt (self) :
        """
        创建额外用于定位的 bp 关节。

        Returns:
            None
        """
        super ()._create_extra_bpjnt ()

        # 调用脚部 Limb 模块的额外 bp 关节创建方法
        self.foot_limb._create_extra_bpjnt ()


    def _create_base_joint (self) :
        super ()._create_base_joint ()

        # 调用脚部 Limb 模块的额外 bp 关节创建方法
        self.foot_limb._create_base_joint ()


    def _create_extra_joint (self) :
        super ()._create_extra_joint ()

        self.foot_limb._create_extra_joint ()


    def _create_base_ctrl (self) :
        super ()._create_base_ctrl ()

        self.foot_limb._create_base_ctrl ()


    def _create_extra_ctrl (self) :
        """
        创建额外用于定位 IK 旋转轴心点的控制器。

        Returns:
            None
        """
        super ()._create_extra_ctrl ()

        # 调用脚部 Limb 模块的额外控制器创建方法
        self.foot_limb._create_extra_ctrl ()


    def _create_base_constraint (self) :
        super ()._create_base_constraint ()

        self.foot_limb._create_base_constraint ()


    def _create_extra_constraint (self) :
        """
        创建额外的约束。

        Returns:
            None
        """
        super ()._create_extra_constraint ()

        # 调用脚部 Limb 模块的约束创建方法
        self.foot_limb._create_extra_constraint ()

        # 对脚部关节与脚掌的控制器组进行约束
        cmds.parentConstraint (self.jnt_list [-1] , self.foot_limb.ctrl_grp , mo = True)


if __name__ == '__main__' :
    def build_setup () :
        leg_l = leg.Leg (side = 'l' , name = 'zz' , jnt_number = 3 , axis = [0 , -1 , 0] , length = 10 ,
                         is_stretch = 1 , jnt_parent = None ,
                         ctrl_parent = None)
        leg_l.build_setup ()


    def build_rig () :
        leg_l = leg.Leg (side = 'l' , name = 'zz' , jnt_number = 3 , axis = [0 , -1 , 0] , length = 10 ,
                         is_stretch = 1 , jnt_parent = None ,
                         ctrl_parent = None)
        leg_l.build_rig ()


    #
    #
    build_setup ()
    build_rig ()
