import maya.cmds as cmds
import pymel.core as pm


class RigBase(object):
    def __init__(self, module = None, side = 'md', guide=None, jnt_parent=None,ctrl_parent=None):
        self.module = module
        self.side = side
        self.guide = guide
        self.jnt_parent = jnt_parent
        self.ctrl_parent = ctrl_parent



    def create_name (self) :
        pass

    def get_guides(self):
        pass


    def create_jnt(self):
        pass

    def create_ctrl (self):
        pass

    def create_constraint(self):
        pass

    def hierarchy_rig(self):
        pass

    def create_rig(self):
        self.create_name()
        self.create_joint()
        self.create_ctrl()
        self.create_constraint()

