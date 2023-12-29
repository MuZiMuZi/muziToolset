from importlib import reload

import maya.cmds as cmds

from . import chain , chainFK , chainIK
from ....core import controlUtils , jointUtils , vectorUtils


reload (chain)
reload (chainIK)


class ChainIKFK (chain.Chain) :
    u'''
    创建ikfk的关节链条的绑定系统
    由三条关节链组成，ik关节链条，fk关节链条和ikfk关节链条组成
    '''
    rtype = 'ChainIKFK'


    def __init__ (self , side , name , jnt_number , direction = [0 , 1 , 0] , length = 10 , is_stretch = 1 ,
                  jnt_parent = None ,
                  ctrl_parent = None) :

        # 初始化ik关节链条和fk关节链条
        self.ik_chain = chainIK.ChainIK (side , name , jnt_number , direction , length , is_stretch)

        self.fk_chain = chainFK.ChainFK (side , name , jnt_number , direction , length)
        self.rtype = 'ChainIKFK'
        self.radius = 6

        super ().__init__ (side , name , jnt_number , length , jnt_parent = None , ctrl_parent = None)
        # 获取初始的位置
        self.interval = length / (self.jnt_number - 1)
        self.direction = list (vectorUtils.Vector (direction).mult_interval (self.interval))
        self.is_stretch = is_stretch
        self.axis = vectorUtils.Vector (direction).axis


    def create_bpjnt (self) :
        super ().create_bpjnt ()

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


    def create_namespace (self) :
        u"""
            创建名称进行规范整理
            """
        # 初始化ik关节链条和fk关节链条的命名规范
        self.ik_chain.create_namespace ()
        self.fk_chain.create_namespace ()
        super ().create_namespace ()
        print (self.ctrl_list)
        print (self.rtype)


    def create_joint (self) :
        """
        根据定位的bp关节创建关节
        """
        # 创建ik关节链条和fk关节链条的关节
        self.ik_chain.create_joint ()
        self.fk_chain.create_joint ()

        # 判断场景里是否已经存在对应的关节，重建的情况
        if cmds.objExists (self.jnt_list [0]) :
            # 删除过去的关节后，并重新创建关节
            cmds.delete (self.jnt_list [0])

        # 创建ikfk的关节
        self._create_ikfk_joints ()

        # 进行关节定向
        jointUtils.Joint.joint_orientation (self.jnt_list)

        # 隐藏bp的定位关节
        cmds.setAttr (self.bpjnt_list [0] + '.visibility' , 0)
        # 设置ik关节链条和fk关节链条的可见性
        cmds.setAttr (self.ik_chain.jnt_list [0] + '.v' , 0)
        cmds.setAttr (self.fk_chain.jnt_list [0] + '.v' , 0)

        cmds.parent (self.jnt_list [0] , self.jnt_parent)


    def _create_ikfk_joints (self) :
        """
        创建ikfk的关节
        """
        cmds.select (clear = True)
        for jnt_number , bpjnt in enumerate (self.bpjnt_list) :
            pos = cmds.xform (bpjnt , q = 1 , t = 1 , ws = 1)
            cmds.joint (p = pos , name = self.jnt_list [jnt_number])


    # 创建控制器
    def create_ctrl (self) :
        """
        创建控制器绑定
        """
        self.ik_chain.create_ctrl ()
        self.fk_chain.create_ctrl ()

        # 创建整体的控制器层级组
        self.ctrl_grp = cmds.createNode ('transform' , name = self.ctrl_grp , parent = self.ctrl_parent)

        # 创建用于ikfk切换的控制器
        self._create_ikfk_switch_ctrl ()


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


    def add_constraint (self) :
        """
        添加约束,ikfk关节链的约束比较特别，需要连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
        """
        self.ik_chain.add_constraint ()
        self.fk_chain.add_constraint ()

        # IK关节链，FK关节链来约束IKFK关节链
        for jnt_number in range (self.jnt_number) :
            cons = self._create_ikfk_constraint (jnt_number)
            # 连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
            self._set_ikfk_driven_keyframes (cons , jnt_number)


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

        cmds.setDrivenKeyframe (self.ik_chain.ctrl_list [jnt_number] + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 1 , v = 1)
        cmds.setDrivenKeyframe (self.ik_chain.ctrl_list [jnt_number] + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 0 , v = 0)
        cmds.setDrivenKeyframe (self.fk_chain.ctrl_list [jnt_number] + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 0 , v = 1)
        cmds.setDrivenKeyframe (self.fk_chain.ctrl_list [jnt_number] + '.v' ,
                                cd = self.ctrl_list [0] + '.Switch' , dv = 1 , v = 0)


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
