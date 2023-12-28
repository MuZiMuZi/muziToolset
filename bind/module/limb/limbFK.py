from importlib import reload

from ..chain import chainFK


reload (chainFK)


class LimbFK (chainFK.ChainFK) :


    def __init__ (self , side , name , jnt_number = 3 , direction = [-1 , 0 , 0] , length = 10 , jnt_parent = None ,
                  ctrl_parent = None) :
        u"""
        创建手臂或者是腿部的四肢关节的FK绑定
        limbtype(str):给定的limbtype 是手臂还是腿部
        """
        super ().__init__ (side , name , jnt_number , direction , length , jnt_parent , ctrl_parent)
        self.rtype = 'LimbFK'


    def create_joint (self) :
        super ().create_joint ()


if __name__ == '__main__' :
    def build_setup () :
        custom = limbFK.LimbFK (side = 'l' , name = 'zz' , jnt_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
                                jnt_parent = None ,
                                ctrl_parent = None)
        custom.build_setup ()


    def build_rig () :
        custom = limbFK.LimbFK (side = 'l' , name = 'zz' , jnt_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
                                jnt_parent = None ,
                                ctrl_parent = None)
        custom.build_rig ()


    build_setup ()
    build_rig ()
