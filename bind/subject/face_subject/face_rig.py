from . import brow , cheek , ear , eye , jaw , mouth , nose , tongue
from importlib import reload

reload(brow)
reload (cheek)
reload (ear)
reload (eye)
reload (jaw)
reload (mouth)
reload (nose)




class Face_rig () :

    def __init__ (self) :
        pass


    def build_setup (self) :
        self.tongue_m = tongue.Tongue (side = 'm' , name = '' , joint_number = 5 , direction = [-1 , 0 , 0] ,
                                       length = 10 ,
                                       joint_parent = None ,
                                       control_parent = None)
        self.tongue_m.build_setup ()


    def build_rig (self) :
        self.tongue_m.build_rig ()


