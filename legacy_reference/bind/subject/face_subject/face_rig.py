from importlib import reload

from . import brow , cheek , ear , eye , jaw , mouth , nose , tongue


reload (brow)
reload (cheek)
reload (ear)
reload (eye)
reload (jaw)
reload (mouth)
reload (nose)


class Face_rig () :

    def __init__ (self) :
        self.tongue_m = tongue.Tongue (side = 'm' , name = '' , jnt_number = 5 , direction = [-1 , 0 , 0] ,
                                       length = 10 ,
                                       jnt_parent = None ,
                                       ctrl_parent = None)


    def build_setup (self) :
        self.tongue_m.build_setup ()


    def build_rig (self) :
        self.tongue_m.build_rig ()
