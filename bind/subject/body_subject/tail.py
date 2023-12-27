from ...module.chain import chainIKFK


class Tail (chainIKFK.ChainIKFK) :


    def __init__ (self , side , name , jnt_number , direction , is_stretch = 1 , length = 10 , jnt_parent = None ,
                  ctrl_parent = None) :
        super ().__init__ (side , name , jnt_number , direction , is_stretch , length , jnt_parent , ctrl_parent)
        self._rtype = 'Tail'


if __name__ == '__main__' :
    def build_setup () :
        finger_l = tail.Tail (side = 'l' , name = 'zz' , jnt_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
                              jnt_parent = None , ctrl_parent = None)
        finger_l.build_setup ()


    def build_rig () :
        finger_l = tail.Tail (side = 'l' , name = 'zz' , jnt_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
                              jnt_parent = None , ctrl_parent = None)
        finger_l.build_rig ()


    build_setup ()
    build_rig ()
