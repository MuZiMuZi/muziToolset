from importlib import reload

import muziToolset.bind.subject.body_subject.arm as arm
from muziToolset.core import pipelineUtils


reload (pipelineUtils)
reload (arm)


def build_setup () :
    arm_l = arm.Arm (side = 'l' , name = 'arm' , jnt_number = 3 , direction = [1 , 0 , 0] , length = 10 ,
                     is_stretch = 1 , jnt_parent = None ,
                     control_parent = None)
    arm_l.build_setup ()


def build_rig () :
    arm_l = arm.Arm (side = 'l' , name = 'arm' , jnt_number = 3 , direction = [1 , 0 , 0] , length = 10 ,
                     is_stretch = 1 , jnt_parent = None ,
                     control_parent = None)
    arm_l.build_rig ()


# 生成定位关节
build_setup ()

# # #生成绑定系统
# build_rig()
