import muziToolset.bind.subject.body_subject.arm as arm
import muziToolset.bind.subject.body_subject.leg as leg
import muziToolset.bind.subject.body_subject.spine as spine
import muziToolset.bind.subject.body_subject.tail as tail
from importlib import reload
from muziToolset.core import controlUtils , hierarchyUtils , jointUtils , pipelineUtils
reload(pipelineUtils)
reload(arm)


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




# #生成定位关节
build_setup()

#生成绑定系统
# build_rig()
