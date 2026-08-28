from importlib import reload

import maya.cmds as cmds

from . import chain , chainFK , chainIK
from ....core import controlUtils , jointUtils , vectorUtils


reload (chain)
reload (chainIK)


class ChainIKFK (chain.Chain) :
    rigType = 'ChainIKFK'


    def __init__ (self , side , name , jnt_number , direction = [0 , 1 , 0] , length = 10 , is_stretch = 1 ,
                  jnt_parent = None ,
                  ctrl_parent = None) :
        """
        创建ikfk的关节链条的绑定系统
        由三条关节链组成，ik关节链条，fk关节链条和ikfk关节链条组成
        side(str):边
        name(str):组件的名称
        direction(list):组件的轴向
        length(float)：组件的长度
        is_stretch(bool):组件是否可以拉伸
        jnt_parent(str):组件所对应的关节的父对象
        ctrl_parent(str):组件所对应的控制器的父对象
        """
        super ().__init__ (side , name , jnt_number , length , jnt_parent = None , ctrl_parent = None)
        # 获取初始的位置
        self.interval = length / (self.jnt_number - 1)
        self.direction = list (vectorUtils.Vector (direction).mult_interval (self.interval))
        self.is_stretch = is_stretch
        self.axis = vectorUtils.Vector (direction).axis

        # 初始化ik关节链条和fk关节链条
        self._init_ikfk ()


    # 初始化ik系统和fk系统
    def _init_ikfk (self) :
        # 初始化ik关节链条和fk关节链条
        self.ik_chain = chainIK.ChainIK (self.side , self.name , self.jnt_number , self.direction , self.length ,
                                         self.is_stretch)

        self.fk_chain = chainFK.ChainFK (self.side , self.name , self.jnt_number , self.direction , self.length)


    def create_namespace (self) :
        u"""
            创建名称进行规范整理
            """
        super ().create_namespace ()

        ## 初始化ik关节链条和fk关节链条的命名规范
        self._create_ikfk_namespace ()


    def _create_ikfk_namespace (self) :
        # 初始化ik关节链条和fk关节链条的命名规范
        self.ik_chain.create_namespace ()
        self.fk_chain.create_namespace ()


    def create_bpjnt (self) :
        """
        创建定位的bp关节
        """
        # 设置bpjnt创建出来的位置放置在top_bpjnt_grp的层级下
        super ().create_bpjnt ()

        ## 创建ik关节链条和fk关节链条的定位关节
        self._create_ikfk_bpjnt ()


    def _create_ikfk_bpjnt (self) :
        # 创建ik关节链条和fk关节链条的定位关节
        self.ik_chain.create_bpjnt ()
        self.fk_chain.create_bpjnt ()

        # 设置连接让定位关节驱动ik和fk的关节链条
        for bpjnt , ik_bpjnt , fk_bpjnt in zip (self.bpjnt_list , self.ik_chain.bpjnt_list , self.fk_chain.bpjnt_list) :
            cmds.parentConstraint (bpjnt , ik_bpjnt , mo = False)
            cmds.parentConstraint (bpjnt , fk_bpjnt , mo = False)
        # 将ik关节链条和fk关节链条进行隐藏可见性，方便选择和调整位置
        cmds.setAttr (self.ik_chain.bpjnt_list [0] + '.visibility' , 0)
        cmds.setAttr (self.fk_chain.bpjnt_list [0] + '.visibility' , 0)


    def create_joint (self) :
        """
        根据定位的bp关节创建关节
        """

        # 判断场景里是否已经存在对应的关节，重建的情况
        self._cheek_bpjnt_objExists ()

        # 创建ikfk的关节
        self._create_ikfk_joints ()

        # 进行关节定向
        jointUtils.Joint.joint_orientation (self.jnt_list)

        # 设置bp关节的可见性
        self._set_bpjnt_vis (False)

        # 设置关节的层级结构
        cmds.parent (self.jnt_list [0] , self.jnt_parent)


    def _set_bpjnt_vis (self , vis_bool) :
        super ()._set_bpjnt_vis (vis_bool)
        # 隐藏bp的定位关节
        cmds.setAttr (self.bpjnt_list [0] + '.visibility' , 0)
        # 设置ik关节链条和fk关节链条的可见性
        cmds.setAttr (self.ik_chain.jnt_list [0] + '.v' , 0)
        cmds.setAttr (self.fk_chain.jnt_list [0] + '.v' , 0)


    def _create_ikfk_joints (self) :
        """
        创建ikfk的关节
        """
        # 创建ik关节链条和fk关节链条的关节
        self.ik_chain.create_joint ()
        self.fk_chain.create_joint ()

        cmds.select (clear = True)
        for jnt_number , bpjnt in enumerate (self.bpjnt_list) :
            pos = cmds.xform (bpjnt , q = 1 , t = 1 , ws = 1)
            cmds.joint (p = pos , name = self.jnt_list [jnt_number])


    # 创建控制器
    def create_ctrl (self) :
        """
        创建控制器绑定
        """
        # 创建整体的控制器层级组
        self._create_ctrl_grp ()
        # 创建ik和fk系统各自的控制器
        self._create_ikfk_ctrl ()

        # 创建用于ikfk切换的控制器
        self._create_ikfk_switch_ctrl ()

        # 整理层级控制器组的层级结构
        self._create_ctrl_hierarchy ()


    # 创建ik和fk系统各自的控制器
    def _create_ikfk_ctrl (self) :
        self.ik_chain.create_ctrl ()
        self.fk_chain.create_ctrl ()


    # 创建IKFK切换控制器
    def _create_ikfk_switch_ctrl (self) :
        """
        创建IKFK切换控制器
        """
        self.ctrl = controlUtils.Control.create_ctrl (self.ctrl_list [0] , shape = 'pPlatonic' ,
                                                      radius = self.radius * 1.2 ,
                                                      axis = self.axis , pos = self.jnt_list [0] ,
                                                      parent = self.ctrl_grp)
        cmds.setAttr (self.zero_list [0] + '.translateZ' , -5)
        # 添加IKFK切换的属性
        cmds.addAttr (self.ctrl , sn = 'Switch' , ln = 'ikfkSwitch' , at = 'double' , dv = 1 , min = 0 , max = 1 ,
                      k = 1)


    def _create_ctrl_hierarchy (self) :
        """
        整理控制器组的层级结构
        """
        cmds.parent (self.ik_chain.ctrl_grp , self.output_list [0])
        cmds.parent (self.fk_chain.ctrl_grp , self.output_list [0])


    def add_constraint (self) :
        """
        添加约束,ikfk关节链的约束比较特别，需要连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
        """
        # 添加ik和fk系统各自的约束连接
        self._add_ikfk_constraint ()

        # IK关节链，FK关节链来约束IKFK关节链
        for jnt_number in range (self.jnt_number) :
            cons = self._create_ikfk_constraint (jnt_number)
            # 连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
            self._set_ikfk_driven_keyframes (cons , jnt_number)


    # 添加ik和fk系统各自的约束连接
    def _add_ikfk_constraint (self) :
        self.ik_chain.add_constraint ()
        self.fk_chain.add_constraint ()


    ## IK关节链，FK关节链来约束IKFK关节链
    def _create_ikfk_constraint (self , jnt_number) :
        """
        创建IKFK约束
        """
        cons = cmds.parentConstraint (
            self.ik_chain.jnt_list [jnt_number] ,
            self.fk_chain.jnt_list [jnt_number] ,
            self.jnt_list [jnt_number]) [0]
        return cons


    # 连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条，设置IKFK切换的驱动关键帧
    def _set_ikfk_driven_keyframes (self , cons , jnt_number) :
        """
        设置IKFK切换的驱动关键帧
        """
        cmds.setDrivenKeyframe (
            '{}.w0'.format (cons) , cd = self.ctrl_list [0] + '.Switch' , dv = 1 , v = 1)
        cmds.setDrivenKeyframe (
            '{}.w1'.format (cons) , cd = self.ctrl_list [0] + '.Switch' , dv = 1 , v = 0)
        cmds.setDrivenKeyframe (
            '{}.w0'.format (cons) , cd = self.ctrl_list [0] + '.Switch' , dv = 0 , v = 0)
        cmds.setDrivenKeyframe (
            '{}.w1'.format (cons) , cd = self.ctrl_list [0] + '.Switch' , dv = 0 , v = 1)

        cmds.setDrivenKeyframe (self.ik_chain.zero_list [jnt_number] + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 1 , v = 1)
        cmds.setDrivenKeyframe (self.ik_chain.zero_list [jnt_number] + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 0 , v = 0)
        cmds.setDrivenKeyframe (self.fk_chain.zero_list [jnt_number] + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 0 , v = 1)
        cmds.setDrivenKeyframe (self.fk_chain.zero_list [jnt_number] + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 1 , v = 0)


    def delete_rig (self) :
        super ().delete_rig ()
        # 删除IKFK的绑定
        self.ik_chain.delete_rig ()
        self.fk_chain.delete_rig ()


if __name__ == '__main__' :
    def build_setup () :
        chain_ikfk = chainIKFK.ChainIKFK (side = 'l' , name = 'zz' , jnt_number = 5 , direction = [1 , 0 , 0] ,
                                          jnt_parent = None , ctrl_parent = None)
        chain_ikfk.build_setup ()


    def y () :
        chain_ikfk = chainIKFK.ChainIKFK (side = 'l' , name = 'zz' , jnt_number = 5 , direction = [1 , 0 , 0] ,
                                          jnt_parent = None , ctrl_parent = None)
        chain_ikfk.build_rig ()


# build_setup()
# build_rig()
