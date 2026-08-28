import maya.cmds as cmds

from ...module.chain import chainFK


class Finger (chainFK.ChainFK) :
    rigType = 'Finger'
    radius = 2


    def __init__ (self , side , name , jnt_number = 4 , direction = [-1 , 0 , 0] , length = 10 , jnt_parent = None ,
                  ctrl_parent = None) :
        if side == 'r' :
            direction = [1 , 0 , 0]
        super ().__init__ (side , name , jnt_number , direction , length , jnt_parent , ctrl_parent)


    def create_ctrl (self) :
        super ().create_ctrl ()

        # 添加手指头一键弯曲的属性
        cmds.addAttr (self.ctrl_list [0] , ln = 'Curl' , at = 'double' , dv = 0 , min = -10 ,
                      max = 10 ,
                      k = 1)

        self.add_curl ()


    def add_curl (self) :
        """
        添加手指弯曲的效果
        """
        curl_attr = self.ctrl_list [0] + '.Curl'

        for ctrl in self.ctrl_list [1 :-1] :
            mult_node = cmds.createNode ('multDoubleLinear' , name = ctrl.replace ('ctrl' , 'mult'))
            cmds.setAttr (mult_node + '.input2' , 9)
            cmds.connectAttr (curl_attr , mult_node + '.input1')
            cmds.connectAttr (mult_node + '.output' , ctrl.replace ('ctrl' , 'connect') + '.rotateZ')


if __name__ == '__main__' :
    def x () :
        finger_l = finger.Finger (side = 'l' , name = 'zz' , jnt_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
                                  jnt_parent = None , ctrl_parent = None)
        finger_l.build_setup ()


    def y () :
        finger_l = finger.Finger (side = 'l' , name = 'zz' , jnt_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
                                  jnt_parent = None , ctrl_parent = None)
        finger_l.build_rig ()


    x ()
    y ()
