from importlib import reload

import maya.cmds as cmds

from . import finger


reload (finger)


class Hand (finger.Finger) :
    rigType = 'finger'


    def __init__ (self , side , name , jnt_number = 4 , direction = [-1 , 0 , 0] , length = 3 , jnt_parent = None ,
                  ctrl_parent = None) :
        super ().__init__ (side , name , jnt_number , direction , length , jnt_parent , ctrl_parent)
        # 初始化手指的模块
        self.thumb_finger = finger.Finger (side , 'thumb' , jnt_number = 3 , direction = self.direction ,
                                           length = self.length , jnt_parent = self.jnt_parent ,
                                           ctrl_parent = self.ctrl_parent)

        self.index_finger = finger.Finger (side , 'index' , jnt_number = 4 , direction = self.direction ,
                                           length = self.length , jnt_parent = self.jnt_parent ,
                                           ctrl_parent = self.ctrl_parent)

        self.middle_finger = finger.Finger (side , 'middle' , jnt_number = 4 , direction = self.direction ,
                                            length = self.length , jnt_parent = self.jnt_parent ,
                                            ctrl_parent = self.ctrl_parent)

        self.ring_finger = finger.Finger (side , 'ring' , jnt_number = 4 , direction = self.direction ,
                                          length = self.length , jnt_parent = self.jnt_parent ,
                                          ctrl_parent = self.ctrl_parent)

        self.pinky_finger = finger.Finger (side , 'pinky' , jnt_number = 4 , direction = self.direction ,
                                           length = self.length , jnt_parent = self.jnt_parent ,
                                           ctrl_parent = self.ctrl_parent)
        self.finger_list = [self.thumb_finger , self.index_finger , self.middle_finger , self.ring_finger ,
                            self.pinky_finger]


    def create_namespace (self) :
        # 创建手指各模块的定位关节
        for finger in self.finger_list :
            finger.create_namespace ()
        self.finger_grp = ('grp_{}_{}Finger_001'.format (self.side , self.name))


    def create_bpjnt (self) :
        # 创建手指各模块的定位关节
        for index , finger in enumerate (self.finger_list) :
            finger.create_bpjnt ()
            # 移动初始关节的位置
            cmds.setAttr (finger.bpjnt_list [0] + '.translateZ' , int (index * 1))
            cmds.setAttr (finger.bpjnt_list [0] + '.translateX' , int (20 * self.side_value))


    def create_joint (self) :
        # 创建手指各模块的蒙皮关节
        for index , finger in enumerate (self.finger_list) :
            finger.create_joint ()


    def create_ctrl (self) :
        self.finger_grp = cmds.createNode ('transform' , name = self.finger_grp , parent = self.ctrl_parent)
        # 创建手指各模块的绑定控制器
        for finger in self.finger_list :
            finger.create_ctrl ()
            cmds.parent (finger.ctrl_grp , self.finger_grp)


    def add_constraint (self) :
        for finger in self.finger_list :
            finger.add_constraint ()


if __name__ == '__main__' :
    def build_setup () :
        finger_l = hand.Hand (side = 'l' , name = 'zz' , jnt_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
                              jnt_parent = None ,
                              ctrl_parent = None)
        finger_l.build_setup ()


    def build_rig () :
        finger_l = hand.Hand (side = 'l' , name = 'zz' , jnt_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
                              jnt_parent = None ,
                              ctrl_parent = None)
        finger_l.build_rig ()


    build_setup ()
    build_rig ()
