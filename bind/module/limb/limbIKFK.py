from importlib import reload

import maya.cmds as cmds

from ..chain import chainIKFK
from ..limb import limbFK , limbIK
from ....core import jointUtils


reload (limbFK)
reload (limbIK)
reload (chainIKFK)


class LimbIKFK (chainIKFK.ChainIKFK) :
    rigType = 'LimbIKFK'
    radius = 5


    def __init__ (self , side , name , jnt_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,is_stretch = 1 ,
                  limbtype = None ,
                  jnt_parent = None ,
                  ctrl_parent = None) :
        '''
        创建手臂或者是腿部的四肢关节的绑定系统
        由三条关节链组成，ik关节链条，fk关节链条和ikfk关节链条组成
        side(str):边
        name(str):组件的名称
        direction(list):组件的轴向
        length(float)：组件的长度
        is_stretch(bool):组件是否可以拉伸
        limbtype(str):组件的类型，为arm还是leg，判断为手部的绑定还是腿部的绑定
        jnt_parent(str):组件所对应的关节的父对象
        ctrl_parent(str):组件所对应的控制器的父对象
        '''
        self.limbtype = limbtype
        # 判断给定的limbtype 是手臂还是腿部

        if self.limbtype == 'arm' :
            self.z_value = 1
        else :
            self.z_value = -1
        super ().__init__ (side , name , jnt_number , direction , length , is_stretch , jnt_parent , ctrl_parent)
    # 初始化ik系统和fk系统
    def _init_ikfk (self) :
        self.ik_limb = limbIK.LimbIK (self.side , self.name , self.jnt_number , self.direction , self.length ,
                                      self.is_stretch ,
                                      self.limbtype)
        self.fk_limb = limbFK.LimbFK (self.side , self.name , self.jnt_number , self.direction , self.length)


    # 创建名称进行规范整理
    def create_namespace (self) :
        u"""
            创建名称进行规范整理
            """
        super ().create_namespace ()




    def _create_ikfk_namespace (self) :
        # 初始化ik关节链条和fk关节链条的命名规范
        self.ik_limb.create_namespace ()
        self.fk_limb.create_namespace ()


    # 创建定位的bp关节
    def create_bpjnt (self) :
        """
        创建定位的bp关节
        """
        super ().create_bpjnt ()

    # 创建ik系统和fk系统的关节
    def _create_ikfk_bpjnt (self) :
        # 创建ik关节链条和fk关节链条的定位关节
        self.ik_limb.create_bpjnt ()
        self.fk_limb.create_bpjnt ()

        # 设置ik关节链条和fk关节链条的定位关节的显示
        cmds.setAttr (self.ik_limb.bpjnt_list [0] + '.v' , 0)
        cmds.setAttr (self.fk_limb.bpjnt_list [0] + '.v' , 0)

        # 设置连接让定位关节驱动ik和fk的关节链条
        for bpjnt , ik_bpjnt , fk_bpjnt in zip (self.bpjnt_list , self.ik_limb.bpjnt_list , self.fk_limb.bpjnt_list) :
            cmds.parentConstraint (bpjnt , ik_bpjnt , mo = False)
            cmds.parentConstraint (bpjnt , fk_bpjnt , mo = False)
        # 创建logging用来记录日志
        self.logger.debug (u'{}_{}  :  BP joint creation completed for positioning'.format (self.name , self.side))


    # 根据定位的bp关节创建关节
    def create_joint (self) :
        '''
        根据定位的bp关节创建关节
        '''
        # 判断场景里是否已经存在对应的关节，重建的情况,当之前的关节存在于场景中的时候进行删除
        self._cheek_bpjnt_objExists ()

        # 创建ikfk的关节
        self._create_ikfk_joints ()

        # 进行关节定向
        jointUtils.Joint.joint_orientation (self.jnt_list)

        # 设置bp关节的可见性
        self._set_bpjnt_vis (False)

        # 整理关节层级结构
        cmds.parent (self.jnt_list [0] , self.jnt_parent)
        # 创建logging用来记录日志
        self.logger.debug (u'{}_{}  :  Skin joint creation completed'.format (self.name , self.side))


    # 创建ik系统和fk系统的关节链条
    def _create_ikfk_joints (self) :
        # 创建ik关节链条和fk关节链条的关节
        self.ik_limb.create_joint ()
        self.fk_limb.create_joint ()

        # 创建ikfk的关节
        cmds.select (clear = True)
        for jnt_number , bpjnt in enumerate (self.bpjnt_list) :
            pos = cmds.xform (bpjnt , q = 1 , t = 1 , ws = 1)
            cmds.joint (p = pos , name = self.jnt_list [jnt_number])


    # 设置定位关节的可见性
    def _set_bpjnt_vis (self , vis_bool) :
        # 隐藏bp的定位关节
        cmds.setAttr (self.bpjnt_list [0] + '.visibility' , vis_bool)
        # 设置ik关节链条和fk关节链条的可见性
        cmds.setAttr (self.ik_limb.jnt_list [0] + '.v' , vis_bool)
        cmds.setAttr (self.fk_limb.jnt_list [0] + '.v' , vis_bool)


    # 创建控制器绑定
    def create_ctrl (self) :
        u'''
        创建控制器绑定
        '''
        # 判断场景里是否已经存在对应的控制器，重建的情况
        self._create_ctrl_grp ()

        # 创建ik模块和fk模块的控制器
        self._create_ikfk_ctrl ()

        # 创建用于ikfk切换的控制器
        self._create_ikfk_switch_ctrl ()

        # 整理控制器的层级结构
        self._create_ctrl_hierarchy ()

        # 创建logging用来记录日志
        self.logger.debug (u'{}_{}  :  Controller creation completed'.format (self.name , self.side))


    # 创建ik和fk系统各自的控制器
    def _create_ikfk_ctrl (self) :
        # 创建ik模块和fk模块的控制器
        self.ik_limb.create_ctrl ()
        self.fk_limb.create_ctrl ()


    def _create_ctrl_hierarchy (self) :
        """
        整理控制器组的层级结构
        """
        cmds.parent (self.ik_limb.ctrl_grp , self.output_list [0])
        cmds.parent (self.fk_limb.ctrl_grp , self.output_list [0])


    # 添加约束,ikfk关节链的约束比较特别，需要连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
    def add_constraint (self) :
        '''
        添加约束,ikfk关节链的约束比较特别，需要连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
        '''
        # 添加ik和fk系统各自的约束连接
        self._add_ikfk_constraint ()

        # IK关节链，FK关节链来约束IKFK关节链
        for jnt_number in range (self.jnt_number) :
            cons = self._create_ikfk_constraint (jnt_number)
            # 连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
            self._set_ikfk_driven_keyframes (cons , jnt_number)

        # 创建logging用来记录日志
        self.logger.debug (u'{}_{}  :  Constraint creation completed'.format (self.name , self.side))


    # 添加ik和fk系统各自的约束连接
    def _add_ikfk_constraint (self) :
        # 添加ik和fk系统各自的约束连接
        self.ik_limb.add_constraint ()
        self.fk_limb.add_constraint ()


    def _create_ikfk_constraint (self , jnt_number) :
        """
        创建IKFK约束
        """
        cons = cmds.parentConstraint (
            self.ik_limb.jnt_list [jnt_number] ,
            self.fk_limb.jnt_list [jnt_number] ,
            self.jnt_list [jnt_number]) [0]
        return cons


    def _set_ikfk_driven_keyframes (self , cons , jnt_number) :
        # 连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
        cmds.setDrivenKeyframe (
            '{}.w0'.format (cons) , cd = self.ctrl_list [0] + '.Switch' , dv = 1 , v = 1)
        cmds.setDrivenKeyframe (
            '{}.w1'.format (cons) , cd = self.ctrl_list [0] + '.Switch' , dv = 1 , v = 0)
        cmds.setDrivenKeyframe (
            '{}.w0'.format (cons) , cd = self.ctrl_list [0] + '.Switch' , dv = 0 , v = 0)
        cmds.setDrivenKeyframe (
            '{}.w1'.format (cons) , cd = self.ctrl_list [0] + '.Switch' , dv = 0 , v = 1)

        # 设置ik关节链条和ik控制器的可见性
        cmds.setDrivenKeyframe (self.ik_limb.ctrl_grp + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 1 , v = 1)
        cmds.setDrivenKeyframe (self.ik_limb.ctrl_grp + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 0 , v = 0)

        # 设置fk关节链条和fk控制器的可见性
        cmds.setDrivenKeyframe (self.fk_limb.ctrl_grp + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 0 , v = 1)
        cmds.setDrivenKeyframe (self.fk_limb.ctrl_grp + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 1 , v = 0)


    def build_setup (self) :
        super ().build_setup ()


    def build_rig (self) :
        super ().build_rig ()


if __name__ == '__main__' :
    def build_setup () :
        custom = limbIKFK.LimbIKFK (side = 'l' , name = 'zz' , jnt_number = 3 , direction = [-1 , 0 , 0] ,
                                    length = 10 ,
                                    is_stretch = 1 ,
                                    limbtype = 'arm' ,
                                    jnt_parent = None ,
                                    ctrl_parent = None)
        custom.build_setup ()


    def build_rig () :
        custom = limbIKFK.LimbIKFK (side = 'l' , name = 'zz' , jnt_number = 3 , direction = [-1 , 0 , 0] ,
                                    length = 10 ,
                                    limbtype = 'arm' ,
                                    jnt_parent = None ,
                                    ctrl_parent = None)
        custom.build_rig ()


    build_setup ()
    build_rig ()
