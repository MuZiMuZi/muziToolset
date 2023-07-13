import muziToolset.bind.subject.body_subject.arm as arm
import muziToolset.bind.subject.body_subject.leg as leg
import muziToolset.bind.subject.body_subject.spine as spine
import muziToolset.bind.subject.body_subject.tail as tail
from importlib import reload


reload(leg)
reload(arm)
reload(spine)
reload(tail)



def build_setup() :
    arm_l = arm.Arm(side = 'l' , name = 'arm' , joint_number = 3 , direction = [1 , 0 , 0] , length = 10 ,
                    is_stretch = 1 , joint_parent = None ,
                    control_parent = None)
    arm_l.build_setup()



def build_rig() :
    arm_l = arm.Arm(side = 'l' , name = 'arm' , joint_number = 3 , direction = [1 , 0 , 0] , length = 10 ,
                    is_stretch = 1 , joint_parent = None ,
                    control_parent = None)
    arm_l.build_rig()



#
#
build_setup()
build_rig()