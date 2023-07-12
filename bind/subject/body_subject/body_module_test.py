import muziToolset.bind.subject.body_subject.arm as arm
from importlib import reload



reload(arm)



def build_setup() :
    arm_l = arm.Arm(side = 'l' , name = 'zz' , joint_number = 3 , direction = [1 , 0 , 0] , length = 10 ,
                    is_stretch = 1 , joint_parent = None ,
                    control_parent = None)
    arm_l.build_setup()



def build_rig() :
    arm_l = arm.Arm(side = 'l' , name = 'zz' , joint_number = 3 , direction = [1 , 0 , 0] , length = 10 ,
                    is_stretch = 1 , joint_parent = None ,
                    control_parent = None)
    arm_l.build_rig()



#

build_setup()
build_rig()
