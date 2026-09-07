import maya.cmds as cmds
import pymel.core as pm


class RigModule(object):
    def __init__(self, module=None, side='md', guide=None, jnt_parent=None, ctrl_parent=None):
        self.module = module
        self.side = side
        self.guide = guide
        self.jnt_parent = jnt_parent
        self.ctrl_parent = ctrl_parent

    def get_guides(self):
        pass

    def create_joints(self):
        pass

    def create_controls(self):
        pass

    def connect_rig(self):
        pass

    def setup_hierarchy(self):
        pass

    def build(self):
        self.get_guides()
        self.create_joints()
        self.create_controls()
        self.connect_rig()
        self.setup_hierarchy()
