# coding=utf-8
from importlib import reload

from . import matehuman_base_rig
<<<<<<< HEAD
from . import matehuman_ikfk_rig
=======
from . import ikfk_rig
>>>>>>> origin/master
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.pipelineUtils as pipelineUtils
import muziToolset.core.snapUtils as snapUtils
import muziToolset.core.matehumanUtils as matehumanUtils



<<<<<<< HEAD
reload(matehuman_ikfk_rig)
=======
reload(ikfk_rig)
>>>>>>> origin/master
drv_jnts = ['upperarm_l_drv' , 'lowerarm_l_drv' , 'hand_l_drv']
joint_parent = None
control_parent = None
space_list = None
stretch = True



<<<<<<< HEAD
class Arm_rig(matehuman_ikfk_rig.IKFK_Rig) :
=======
class Arm_rig(ikfk_rig.IKFK_Rig) :
>>>>>>> origin/master



    def __init__(self , drv_jnts , joint_parent , control_parent , space_list , stretch , side) :
        super(Arm_rig , self).__init__(drv_jnts , joint_parent , control_parent , space_list , stretch)
        self.side = side
        self.create_arm_rig()



<<<<<<< HEAD
    def create_arm_rig(self) :
=======
    def create_arm_rig(self ) :
>>>>>>> origin/master
        u'''
        创建手臂的控制器绑定
        :return:
        '''
<<<<<<< HEAD
        # 创建锁骨部位的绑定
        self.create_clavicle_rig()
        # 创建手臂部位的绑定
        self.create_ikfk_chain_rig()



    def create_clavicle_rig(self) :
=======
        #创建锁骨部位的绑定
        self.create_clavicle_rig()
        #创建手臂部位的绑定
        self.create_ikfk_chain_rig()

    def create_clavicle_rig(self):
>>>>>>> origin/master
        # 创建锁骨的控制器
        clavicle_jnt = 'clavicle_{}_drv'.format(self.side)
        clavicle_ctrl = controlUtils.Control.create_mateHuman_ctrl(clavicle_jnt , 'ctrl' , shape = 'ball' ,
                                                                   radius = 12 ,
                                                                   axis = 'Z+' ,
                                                                   pos = clavicle_jnt , parent = None)
        clavicle_output = clavicle_ctrl.replace('ctrl' , 'output')
        # parent = 'output_m_chest_001'


        # 创建耸肩的控制器
        shrug_jnt = 'clavicle_outOff_{}_drv'.format(self.side)
        shrug_ctrl = controlUtils.Control.create_mateHuman_ctrl(shrug_jnt , 'ctrl' , shape = 'Cube' ,
                                                                radius = 5 ,
                                                                axis = 'Z+' ,
                                                                pos = None , parent = clavicle_ctrl.replace(
                    'ctrl' , 'output'))
        # 只吸附位移不吸附旋转

        cmds.matchTransform(shrug_ctrl.replace('ctrl' , 'zero') , shrug_jnt , position = True)
        shrug_output = shrug_ctrl.replace('ctrl' , 'output')

<<<<<<< HEAD
=======

>>>>>>> origin/master
        # 创建肩胛骨的控制器
        scapula_jnt = 'clavicle_scapOff_{}_drv'.format(self.side)
        scapula_ctrl = controlUtils.Control.create_mateHuman_ctrl(scapula_jnt , 'ctrl' , shape = 'Cube' ,
                                                                  radius = 5 ,
                                                                  axis = 'Z+' ,
                                                                  pos = None , parent = clavicle_ctrl.replace(
                    'ctrl' , 'output'))
        # 只吸附位移不吸附旋转

        cmds.matchTransform(scapula_ctrl.replace('ctrl' , 'zero') , scapula_jnt , position = True)
        scapula_output = scapula_ctrl.replace('ctrl' , 'output')

        # 创建约束
<<<<<<< HEAD
        ctrls = [clavicle_ctrl , shrug_ctrl , scapula_ctrl]
        for ctrl in ctrls :
            cmds.parentConstraint(ctrl , ctrl.replace('ctrl' , 'jnt') , mo = True)
            cmds.scaleConstraint(scapula_output , scapula_jnt , mo = True)
=======
        ctrls = [clavicle_ctrl , shrug_ctrl , scapula_ctrl ]
        for ctrl in ctrls :
            cmds.parentConstraint(ctrl , ctrl.replace('ctrl' , 'jnt') , mo = True)
            cmds.scaleConstraint(scapula_output , scapula_jnt , mo = True)


    def create_hand_rig(self):
        u'''
        创建手指的绑定
        :return:
        '''
>>>>>>> origin/master
