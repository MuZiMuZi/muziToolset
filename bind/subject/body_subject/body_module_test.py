import muziToolset.bind.subject.body_subject.arm as arm
import muziToolset.bind.subject.body_subject.leg as leg
import muziToolset.bind.subject.body_subject.spine as spine
from importlib import reload


reload(leg)
reload(arm)
reload(spine)


def build_setup() :
    spine_m = spine.Spine(side = 'm' , name = 'zz' , joint_number = 4 , direction = [0 , 1 , 0] , length = 10 ,
                          is_stretch = 1 , joint_parent = None ,
                          control_parent = None)
    spine_m.build_setup()



def build_rig() :
    spine_m = spine.Spine(side = 'm' , name = 'zz' , joint_number = 4 , direction = [0 , 1 , 0] , length = 10 ,
                          is_stretch = 1 , joint_parent = None ,
                          control_parent = None)
    spine_m.build_rig()



# build_setup()
build_rig()

