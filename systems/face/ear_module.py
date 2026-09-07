import maya.cmds as cmds

from rigging import ctrl_utils
from .. import rig_module
from ...core.common import name_utils,hierarchy_utils
from ...core.rigging import jnt_utils


class EarModule(rig_module.RigModule):

    def __init__(self, module, side, guide, jnt_parent, ctrl_parent):
        super().__init__(module, side, guide, jnt_parent, ctrl_parent)
    def get_guides(self):
        self.ear_guide_list = []

        for index in range (1 , 4) :
            gudie_object = name_utils.Name (
                type = "loc" ,
                side = self.side ,
                part = self.module ,
                function = "guide" ,
                index = index
            )

            self.ear_guide_list.append (gudie_object.name)


    def create_joints(self):
        self.ear_jnt_list = []

        for index in range(1, 4):
            jnt_object = name_utils.Name(
                type="jnt",
                side=self.side,
                part=self.module,
                function="bind",
                index=index
            )

            self.ear_jnt_list.append(jnt_object.name)
            self.ear_jnt = jnt_utils.Jnt (jnt_object.name)
            self.ear_jnt.set_match_transform(target = jnt_object.name.replace('jnt_','loc_').replace('bind','guide'))

    def create_ctrls(self):
        self.ear_ctrl_list = []
        for index in range(1, 4):
            ctrl_object = name_utils.Name(
                type="ctrl",
                side=self.side,
                part=self.module,
                function="fk",
                index=index
            )
    
            self.ear_ctrl_list.append(ctrl_object.name)
            self.ear_ctrl = ctrl_utils.Ctrl (ctrl_object.name)
            self.ear_ctrl.create_ctrl(shape_name="circle", ctrl_color=17, ctrl_size=1.0, create_hierarchy=True,
                                      match_transform_target =ctrl_object.name.replace('ctrl_','loc_').replace('fk','guide') )




    def connect_rig(self):
        for jnt,ctrl in zip(self.ear_jnt_list, self.ear_ctrl_list):
            cmds.parentConstraint(ctrl,jnt,mo = True)
    
    
    



    def create_hierarchy(self):
        #创建关节的总组层级
        self.jnt_master_grp = name_utils.Name(type="grp",side=self.side, part=self.module,function="jnt",index=1)
        #创建控制器的总组层级
        self.ctrl_master_grp = name_utils.Name (type = "grp" , side = self.side , part = self.module , function = "ctrl" ,
                                               index = 1)
        self.jnt_master_grp = cmds.createNode(name = self.jnt_master_grp.name)
        self.ctrl_master_grp = cmds.createNode(name = self.ctrl_master_grp.name)
        
        
        #整理层级结构
        hierarchy_utils.chain_parent(self.ear_jnt_list,parent_node = self.jnt_master_grp)
        hierarchy_utils.chain_parent (self.ear_ctrl_list , parent_node = self.ctrl_master_grp)

