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
    finger_l = tail.Tail(side = 'l' , name = 'zz' , joint_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
                         joint_parent = None , control_parent = None)
    finger_l.build_setup()



def build_rig() :
    finger_l = tail.Tail(side = 'l' , name = 'zz' , joint_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
                         joint_parent = None , control_parent = None)
    finger_l.build_rig()



build_setup()
build_rig()
