from importlib import reload

import maya.cmds as cmds

from ..chain import chainIK
from ....core import controlUtils , hierarchyUtils


reload (chainIK)


class LimbIK (chainIK.ChainIK) :
    u"""
    创建手臂或者是腿部的四肢关节的IK绑定,IK绑定需要创建极向量控制器和ikHandle
    """
    rigType = 'LimbIK'
    shape = 'cube'


    def __init__ (self , side , name , jnt_number = 3 , direction = [-1 , 0 , 0] , length = 10 , is_stretch = 1 ,
                  limb_type = None ,
                  jnt_parent = None ,
                  ctrl_parent = None) :
        u"""
        创建手臂或者是腿部的四肢关节的IK绑定
        limb_type(str):给定的limb_type 是手臂还是腿部
        """
        super ().__init__ (side , name , jnt_number , direction , length , is_stretch , jnt_parent , ctrl_parent)
        # 判断给定的limb_type 是手臂还是腿部
        if limb_type == 'arm' :
            self.z_value = 1
        else :
            self.z_value = -1


    def create_namespace (self) :
        super ().create_namespace ()

        self.pv_ctrl = ('ctrl_{}_{}{}PV_001'.format (self.side , self.name , self.rigType))
        self.pv_loc = ('loc_{}_{}{}PV_001'.format (self.side , self.name , self.rigType))
        self.jnt_loc = ('jnt_{}_{}{}PV_001'.format (self.side , self.name , self.rigType))
        self.pv_curve = ('crv_{}_{}{}PV_001'.format (self.side , self.name , self.rigType))
        self.local_ctrl = ('ctrl_{}_{}{}Local_001'.format (self.side , self.name , self.rigType))
        self.startIK_pos_loc = self.jnt_list [0].replace ('jnt' , 'loc')
        self.endIK_pos_loc = self.jnt_list [-1].replace ('jnt' , 'loc')

        # 添加一个末端的iK关节用来制作singleIKhandle，
        self.endIK_handle = ('handle_{}_{}{}End_001'.format (self.side , self.name , self.rigType))
        self.endIK_jnt = 'jnt_{}_{}{}_{:03d}'.format (self.side , self.name , self.rigType , self.jnt_number + 1)


    def create_joint (self) :
        super ().create_joint ()
        # 隐藏bp的定位关节

        self.endIK_jnt = cmds.createNode ('joint' , name = self.endIK_jnt , parent = self.jnt_list [-1])
        con = cmds.parentConstraint (self.jnt_list [-1] , self.endIK_jnt , mo = False)
        cmds.delete (con)
        cmds.setAttr (self.endIK_jnt + '.translateX' , 5 * self.side_value)


    # 创建ikHandle
    def build_ik_handle (self) :
        """
        创建ikHandle
        """
        # 创建ikSolverHandle
        self.ik_handle = cmds.ikHandle (name = self.ik_handle , startJoint = self.jnt_list [0] ,
                                        endEffector = self.jnt_list [2] ,
                                        sticky = 'sticky' , solver = 'ikRPsolver' , setupForRPsolver = True) [0]

        # 创建末端的ikspineHandle
        self.endIK_handle = cmds.ikHandle (name = self.endIK_handle , startJoint = self.jnt_list [2] ,
                                           endEffector = self.endIK_jnt ,
                                           sticky = 'sticky' , solver = 'ikRPsolver' , setupForRPsolver = True) [0]

        cmds.setAttr (f'{self.ik_handle}.v' , 0)
        cmds.setAttr (f'{self.endIK_handle}.v' , 0)


    # 创建极向量控制器
    def create_pv_ctrl (self) :
        """
        创建极向量控制器
        """
        self.pv_ctrl = controlUtils.Control.create_ctrl (self.pv_ctrl , shape = 'ball' ,
                                                         radius = self.radius * 0.6 ,
                                                         axis = 'X+' , pos = self.jnt_list [1] ,
                                                         parent = self.ctrl_grp)

        # 移动极向量控制器组的位置
        cmds.setAttr (f'{self.pv_ctrl.replace ("ctrl" , "zero")}.translateZ' , -10 * self.z_value * self.side_value)


    # 创建ik极向量控制器的曲线指示器
    def create_ik_pv_curve (self) :
        """
        创建ik极向量控制器的曲线指示器
        """
        # 创建pv控制器的loc来记录位置
        self.midIK_pv_loc = cmds.spaceLocator (name = self.pv_loc) [0]
        cmds.matchTransform (self.midIK_pv_loc , self.pv_ctrl.replace ('ctrl' , 'output') , position = True ,
                             rotation = True ,
                             scale = True)
        cmds.parent (self.midIK_pv_loc , self.pv_ctrl)
        cmds.setAttr (f'{self.midIK_pv_loc}.visibility' , 0)

        # 创建pvjnt的loc来记录位置
        self.midIK_jnt_loc = cmds.spaceLocator (name = self.jnt_loc) [0]
        cmds.matchTransform (self.midIK_jnt_loc , self.jnt_list [1] , position = True , rotation = True , scale = True)
        cmds.parent (self.midIK_jnt_loc , self.jnt_list [1])
        cmds.setAttr (f'{self.midIK_jnt_loc}.visibility' , 0)

        # 连接loc和曲线来表示位置
        self.ikpv_curve = cmds.curve (degree = 1 , point = [(0.0 , 0.0 , 0.0) , (0.0 , 0.0 , 0.0)] , name = self.pv_curve)
        self.midIK_jnt_loc_shape = cmds.listRelatives (self.midIK_jnt_loc , shapes = True) [0]
        self.midIK_pv_loc_shape = cmds.listRelatives (self.midIK_pv_loc , shapes = True) [0]
        self.ikpv_curve_shape = cmds.listRelatives (self.ikpv_curve , shapes = True) [0]

        # 连接曲线与loc
        cmds.connectAttr (f'{self.midIK_jnt_loc_shape}.worldPosition[0]' , f'{self.ikpv_curve_shape}.controlPoints[0]')
        cmds.connectAttr (f'{self.midIK_pv_loc_shape}.worldPosition[0]' , f'{self.ikpv_curve_shape}.controlPoints[1]')

        # 设置曲线的可见性
        cmds.setAttr (f'{self.ikpv_curve_shape}.overrideEnabled' , 1)
        cmds.setAttr (f'{self.ikpv_curve_shape}.overrideDisplayType' , 2)
        cmds.setAttr (f'{self.ikpv_curve}.inheritsTransform' , 0)
        cmds.parent (self.ikpv_curve , self.ctrl_grp)


    # 创建local控制器给手腕
    def create_local_ctrl (self) :
        """
        创建local控制器给手腕
        """
        self.local_ctrl = controlUtils.Control.create_ctrl (self.local_ctrl , shape = 'cross' ,
                                                            radius = self.radius * 0.75 ,
                                                            axis = 'X+' , pos = self.jnt_list [-1] ,
                                                            parent = self.ctrl_list [-1])
        # ikHandle放到local控制器层级下
        cmds.parent (self.ik_handle , self.local_ctrl.replace ('ctrl' , 'output'))


    # 创建控制器结构
    def create_ctrl (self) :
        """
        创建控制器结构
        """
        super ().create_ctrl ()
        # 创建ikhandle系统
        self.build_ik_handle ()
        cmds.setAttr (f'{self.zero_list [1]}.v' , 0)

        # 创建极向量控制器
        self.create_pv_ctrl ()

        cmds.parent (self.ik_handle , self.endIK_handle , self.output_list [-1])

        # 创建ik极向量控制器的曲线指示器
        self.create_ik_pv_curve ()

        # 创建local控制器给手腕
        self.create_local_ctrl ()

        # 判断是否需要添加拉伸功能，如果是则添加
        if self.is_stretch :
            self.add_stretch ()


    # 控制器与关节之间创建连接
    def add_constraint (self) :
        '''
        控制器与关节之间创建连接
        '''
        # 极向量控制器约束ikHandle
        cmds.poleVectorConstraint (self.pv_ctrl.replace ('ctrl' , 'output') , self.ik_handle)



        # 首段ik控制器点约束首段ik关节
        cmds.pointConstraint (self.output_list [0] , self.jnt_list [0] , mo = True)


    def add_stretch (self) :
        u"""
        添加ik链条的拉伸功能
        """

        # 用来获取总的拉伸的长度，计算原理：通过获取起始端和末端控制器的位置信息获取拉伸后的距离长度，减去原先关节的长度即可获得拉伸的长度距离
        self.get_stretch_length ()

        # 为末端控制器添加一个stretch属性，动画师根据需要可以选择是否拉伸。
        self.set_stretch_ctrl ()

        # 创建极向量锁定的属性，并为中端控制器添加PvLock属性，动画师可以选择是否进行极向量锁定。
        self.set_pvLock_ctrl ()


    # 用来获取总的拉伸的长度，计算原理：通过获取起始端和末端控制器的位置信息获取拉伸后的距离长度，减去原先关节的长度即可获得拉伸的长度距离
    def get_stretch_length (self) :
        '''
        用来获取总的拉伸的长度，计算原理：
        通过获取起始端和末端控制器的位置信息获取拉伸后的距离长度，减去原先关节的长度即可获得拉伸的长度距离

        步骤：
        1.创建起始端和末端关节控制器的定位locator，并将其与对应控制器匹配。
        2.创建计算距离的distanceBetween节点，计算起始端关节到末端控制器的距离。
        3.计算原本关节的距离值，将现有关节距离减去原关节的距离得到拉伸的距离。
        4.将拉伸的距离均匀分配给首端和末端的拉伸关节。
        '''

        # 1.创建起始端和末端关节控制器的定位locator，并将其与对应控制器匹配。
        # 创建起始端关节控制器的定位loctor
        self.startIK_pos_loc = cmds.spaceLocator (name = self.startIK_pos_loc) [0]
        self.startIK_pos_loc_shape = cmds.listRelatives (self.startIK_pos_loc , shapes = True) [0]
        cmds.matchTransform (self.startIK_pos_loc , self.ctrl_list [0])
        cmds.setAttr (self.startIK_pos_loc + '.v' , 0)
        hierarchyUtils.Hierarchy.parent (child_node = self.startIK_pos_loc , parent_node = self.output_list [0])

        # 创建末端关节控制器的定位loctor
        self.endIK_pos_loc = cmds.spaceLocator (name = self.endIK_pos_loc) [0]
        self.endIK_pos_loc_shape = cmds.listRelatives (self.endIK_pos_loc , shapes = True) [0]
        cmds.setAttr (self.endIK_pos_loc + '.v' , 0)
        cmds.matchTransform (self.endIK_pos_loc , self.ctrl_list [-1])
        hierarchyUtils.Hierarchy.parent (child_node = self.endIK_pos_loc , parent_node = self.output_list [-1])

        # 2.创建计算距离的distanceBetween节点，计算起始端关节到末端控制器的距离。
        # 创建计算距离的distween节点，来计算首端关节到中端控制器的距离
        self.disBtw_node = cmds.createNode ('distanceBetween' , name = self.endIK_pos_loc.replace ('loc' , 'disBtw'))
        cmds.connectAttr (self.startIK_pos_loc_shape + '.worldPosition' , self.disBtw_node + '.point1')
        cmds.connectAttr (self.endIK_pos_loc_shape + '.worldPosition' , self.disBtw_node + '.point2')

        # 3.计算原本关节的距离值，将现有关节距离减去原关节的距离得到拉伸的距离。
        # 计算原本关节的距离值
        self.midIK_jnt_value = cmds.getAttr (self.jnt_list [1] + '.translateX')
        self.endIK_jnt_value = cmds.getAttr (self.jnt_list [-1] + '.translateX')
        self.distance_value = self.midIK_jnt_value * self.side_value + self.endIK_jnt_value * self.side_value

        # 将现有的关节距离减去原本关节的距离得到拉伸的距离
        self.reduce_node = cmds.createNode ('addDoubleLinear' , name = self.jnt_list [0].replace ('jnt' , 'reduce'))
        cmds.connectAttr (self.disBtw_node + '.distance' , self.reduce_node + '.input1')
        cmds.setAttr (self.reduce_node + '.input2' , self.distance_value * -1 * self.z_value)

        # 4.将拉伸的距离均匀分配给首端和末端的拉伸关节。
        # 将变化的数值除以二，均匀分配给对应的拉伸关节
        self.mult_node = cmds.createNode ('multDoubleLinear' , name = self.jnt_list [0].replace ('jnt' , 'mult'))
        cmds.connectAttr (self.reduce_node + '.output' , self.mult_node + '.input1')
        cmds.setAttr (self.mult_node + '.input2' , 0.5 * self.side_value * self.z_value)

        # 将变化的数值连接给对应的拉伸关节
        self.add_midIK_jnt_node = cmds.createNode ('addDoubleLinear' , name = self.jnt_list [1].replace ('jnt' , 'add'))
        self.add_endIK_jnt_node = cmds.createNode ('addDoubleLinear' , name = self.jnt_list [-1].replace ('jnt' , 'add'))

        cmds.connectAttr (self.mult_node + '.output' , self.add_midIK_jnt_node + '.input1')
        cmds.setAttr (self.add_midIK_jnt_node + '.input2' , self.midIK_jnt_value)

        cmds.connectAttr (self.mult_node + '.output' , self.add_endIK_jnt_node + '.input1')
        cmds.setAttr (self.add_endIK_jnt_node + '.input2' , self.endIK_jnt_value)


    # 用来创建拉伸的控制器的开启与混合连接
    def set_stretch_ctrl (self) :
        """
        用来创建拉伸的控制器的开启与混合连接，通过创建判断节点和混合节点来控制拉伸的开启
        步骤：
        1.创建判断节点，当拉伸距离大于0时才进行拉伸，否则保持原关节长度。
        2.为末端控制器添加一个stretch属性，动画师根据需要可以选择是否拉伸。
        3.创建blendColors节点用来混合拉伸和非拉伸状态的关节长度。
        4.将拉伸后的关节长度连接到blendColors节点，用于混合时的非拉伸状态。
        """

        # 1.创建判断节点，当拉伸距离大于0时才进行拉伸，否则保持原关节长度。
        # 创建一个判断节点，当变化的数值大于0时才进行拉伸
        self.cond_node = cmds.createNode ('condition' , name = self.jnt_list [0].replace ('jnt' , 'cond'))
        cmds.setAttr (self.cond_node + '.operation' , 2)
        cmds.connectAttr (self.reduce_node + '.output' , self.cond_node + '.firstTerm')
        cmds.connectAttr (self.add_midIK_jnt_node + '.output' , self.cond_node + '.colorIfTrueR')
        cmds.connectAttr (self.add_endIK_jnt_node + '.output' , self.cond_node + '.colorIfTrueG')

        cmds.setAttr (self.cond_node + '.colorIfFalseR' , self.midIK_jnt_value)
        cmds.setAttr (self.cond_node + '.colorIfFalseG' , self.endIK_jnt_value)

        # 2.为末端控制器添加一个stretch属性，动画师根据需要可以选择是否拉伸。
        # 给控制器创建一个拉伸的属性，动画师根据需要可以选择是否拉伸
        cmds.addAttr (self.ctrl_list [-1] , longName = 'stretch' , attributeType = 'double' ,
                      niceName = u'拉伸' , minValue = 0 , maxValue = 1 , defaultValue = 1 , keyable = 1)

        # 3.创建blendColors节点用来混合拉伸和非拉伸状态的关节长度。
        # 创建blendcolor节点用来承载拉伸的设置
        self.stretch_blend_node = cmds.createNode ('blendColors' , name = self.ctrl_list [-1].replace ('ctrl' , 'blend'))
        cmds.connectAttr (self.ctrl_list [-1] + '.stretch' , self.stretch_blend_node + '.blender')

        # 4.将拉伸后的关节长度连接到blendColors节点，用于混合时的非拉伸状态。
        # 设置blendcolor节点混合值为0的时候，也就是没有拉伸的时候，color2R 和 color2G 的值是原关节的长度
        # 连接拉伸后的关节长度
        self.stretch_divBtw_node = cmds.createNode ('multiplyDivide' ,
                                               name = self.stretch_blend_node.replace ('blend' , 'div'))

        cmds.setAttr (self.stretch_divBtw_node + '.operation' , 2)
        cmds.setAttr (self.stretch_divBtw_node + '.input1X' , self.midIK_jnt_value)
        cmds.setAttr (self.stretch_divBtw_node + '.input1Y' , self.endIK_jnt_value)
        cmds.connectAttr (self.stretch_divBtw_node + '.outputX' , self.stretch_blend_node + '.color2R')
        cmds.connectAttr (self.stretch_divBtw_node + '.outputY' , self.stretch_blend_node + '.color2G')
        cmds.connectAttr (self.cond_node + '.outColorR' , self.stretch_blend_node + '.color1R')
        cmds.connectAttr (self.cond_node + '.outColorG' , self.stretch_blend_node + '.color1G')


    # 用来创建极向量锁定的属性连接
    def set_pvLock_ctrl (self) :
        '''
        用来创建极向量锁定的属性连接
        步骤：
        1. 创建极向量锁定的属性，并为中端控制器添加PvLock属性，动画师可以选择是否进行极向量锁定。
        2.创建另一个blendColors节点用来混合极向量锁定和非锁定状态的关节长度。
        3.计算起始端到极向量控制器和末端到极向量控制器的距离，并将结果乘以侧边和Z轴的值，用于极向量锁定状态的混合。
        4.将真实的距离和拉伸后的距离分别连接到极向量锁定的blendColors节点，用于混合时的非锁定状态。
        5.最终将混合后的关节长度连接到原关节。
        '''

        # 1. 创建极向量锁定的属性，并为末端控制器添加PvLock属性，动画师可以选择是否进行极向量锁定。
        # 给控制器创建一个极向量锁定的属性，动画师根据需要可以选择是否进行极向量锁定
        cmds.addAttr (self.ctrl_list [-1] , longName = 'PvLock' , attributeType = 'double' ,
                      niceName = u'极向量锁定' , minValue = 0 , maxValue = 1 , defaultValue = 0 , keyable = 1)
        self.pv_loc_shape = cmds.listRelatives (self.pv_loc , shapes = True) [0]

        # 2.创建另一个blendColors节点用来混合极向量锁定和非锁定状态的关节长度。
        # 创建blendColors节点用来承载极向量锁定的设置
        self.pvLock_blend_node  = cmds.createNode ('blendColors' , name = self.pv_ctrl.replace ('ctrl' , 'blend'))
        cmds.connectAttr (self.ctrl_list [-1] + '.PvLock' , self.pvLock_blend_node  + '.blender')

        # 3.计算起始端到极向量控制器和末端到极向量控制器的距离，并将结果乘以侧边和Z轴的值，用于极向量锁定状态的混合。
        # 获取起始控制器，极向量控制器，末端控制器层级下用来定位位置的loc.(startIK_pos_loc,self.midIK_pv_loc,endIK_pos_loc)
        # 创建对应的disteween节点来获取距离
        # 计算起始控制器到极向量控制器的距离
        self.upper_disBtw_node = cmds.createNode ('distanceBetween' ,
                                             name = self.startIK_pos_loc.replace ('loc' , 'disBtw_upper'))
        cmds.connectAttr (self.startIK_pos_loc_shape + '.worldPosition' , self.upper_disBtw_node + '.point1')
        cmds.connectAttr (self.pv_loc_shape + '.worldPosition' , self.upper_disBtw_node + '.point2')

        # 创建一个相乘节点来连接
        self.mult_upper_disBtw_node = cmds.createNode ('multDoubleLinear' ,
                                                  name = self.upper_disBtw_node.replace ('disBtw_lower' , 'mult'))
        cmds.connectAttr (self.upper_disBtw_node + '.distance' , self.mult_upper_disBtw_node + '.input1')
        cmds.setAttr (self.mult_upper_disBtw_node + '.input2' , self.side_value * self.z_value)

        # 计算末端控制器到极向量控制器的距离
        self.lower_disBtw_node = cmds.createNode ('distanceBetween' ,
                                             name = self.startIK_pos_loc.replace ('loc' , 'disBtw_lower'))
        cmds.connectAttr (self.pv_loc_shape + '.worldPosition' , self.lower_disBtw_node + '.point1')
        cmds.connectAttr (self.endIK_pos_loc_shape + '.worldPosition' , self.lower_disBtw_node + '.point2')
        # 创建一个相乘节点来连接
        self.mult_lower_disBtw_node = cmds.createNode ('multDoubleLinear' ,
                                                  name = self.lower_disBtw_node.replace ('disBtw_lower' , 'mult'))
        cmds.connectAttr (self.lower_disBtw_node + '.distance' , self.mult_lower_disBtw_node + '.input1')
        cmds.setAttr (self.mult_lower_disBtw_node + '.input2' , self.side_value * self.z_value)

        # 4.将真实的距离和拉伸后的距离分别连接到极向量锁定的blendColors节点，用于混合时的非锁定状态。
        # 将真实的距离连接给极向量锁定的blendcolor节点
        # 原理：当极向量锁定值为1打开的时候，启用的是color1的数值。当极向量锁定值为0关闭的时候，启用的是color2的数值

        cmds.connectAttr (self.mult_upper_disBtw_node + '.output' , self.pvLock_blend_node  + '.color1R')
        cmds.connectAttr (self.mult_lower_disBtw_node + '.output' , self.pvLock_blend_node  + '.color1G')

        # 将原先关节拉伸后的距离连接给极向量锁定的blendcolor节点的color2
        cmds.connectAttr (self.stretch_blend_node + '.outputR' , self.pvLock_blend_node  + '.color2R')
        cmds.connectAttr (self.stretch_blend_node + '.outputG' , self.pvLock_blend_node  + '.color2G')

        # 5.最终将混合后的关节长度连接到原关节。
        # 把混合后的关节长度连接给原关节
        cmds.connectAttr (self.pvLock_blend_node  + '.outputR' , self.jnt_list [1] + '.translateX')
        cmds.connectAttr (self.pvLock_blend_node  + '.outputG' , self.jnt_list [-1] + '.translateX')


if __name__ == '__main__' :
    def build_setup () :
        custom = limbIK.LimbIK (side = 'l' , name = 'zz' , jnt_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
                                is_stretch = 1 ,
                                limb_type = 'arm' ,
                                jnt_parent = None ,
                                ctrl_parent = None)
        custom.build_setup ()


    def build_rig () :
        custom = limbIK.LimbIK (side = 'l' , name = 'zz' , jnt_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
                                limb_type = 'arm' ,
                                jnt_parent = None ,
                                ctrl_parent = None)
        custom.build_rig ()


    build_setup ()
    build_rig ()
