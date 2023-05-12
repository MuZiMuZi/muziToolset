import muziToolset.rigging.module.hand as hand
from importlib import reload



reload(hand)
def build_setup():
    finger_l = hand.Hand(side = 'l', name = 'zz' , joint_number = 4 , direction = [-1 , 0 , 0] , length = 10 , joint_parent = None ,
                         control_parent = None)
    finger_l.build_setup()
def build_rig():
    finger_l = hand.Hand(side = 'l' , name = 'zz', joint_number = 4 , direction = [-1 , 0 , 0] , length = 10 , joint_parent = None ,
                         control_parent = None)
    finger_l.build_rig()



build_setup()
build_rig()