import muziToolset.rigging.module.tail as tail
from importlib import reload



reload(tail)
def x():
    finger_l = tail.Tail(side = 'l' , name = 'zz' , joint_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
                         joint_parent = None , control_parent = None)
    finger_l.build_setup()
def y():
    finger_l = tail.Tail(side = 'l' , name = 'zz' , joint_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
                             joint_parent = None , control_parent = None)
    finger_l.build_rig()
    
    
x()
y()