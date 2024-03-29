# coding=utf-8
'''
耳朵的绑定系统创建
'''
import os

import maya.cmds as cmds

from ...module.chain import chainFK


class Ear (chainFK.ChainFK) :


    def __init__ (self , side , name = '' , jnt_number = 3 , direction = [-1 , 0 , 0] ,
                  length = 5 , jnt_parent = None , ctrl_parent = None) :
        super ().__init__ (side , name , jnt_number , direction , length , jnt_parent , ctrl_parent)
        self.shape = 'circle'
        self.rigType = 'Ear'
        self.radius = 0.5


    def create_namespace (self) :
        super ().create_namespace ()


    def create_bpjnt (self) :
        # 获得ear_bpjnt 的路径
        self.ear_bpjnt_path = os.path.abspath (__file__ + "/../../../bpjnt/ear_bpjnt.ma")
        # 导入关节
        cmds.file (self.ear_bpjnt_path , i = True , rnn = True)


if __name__ == "__main__" :
    def build_setup () :
        ear_l = ear.Ear (side = 'l' , jnt_parent = None , ctrl_parent = None)
        ear_l.build_setup ()

        ear_r = ear.Ear (side = 'r' , jnt_parent = None , ctrl_parent = None)
        ear_r.build_setup ()


    def build_rig () :
        ear_l = ear.Ear (side = 'l' , jnt_parent = None , ctrl_parent = None)
        ear_l.build_rig ()

        ear_r = ear.Ear (side = 'r' , jnt_parent = None , ctrl_parent = None)
        ear_r.build_rig ()


    build_setup ()
    build_rig ()
