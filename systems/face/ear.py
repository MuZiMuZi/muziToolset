import maya.cmds as cmds
from systems import rig_module
from importlib import reload
form ....core.common  import *
reload(rig_module)

class Ear(rig_module.RigModule):
    def __init__(self,module, side, guide, jnt_parent,ctrl_parent):
        super().__init__(module, side, guide, jnt_parent,ctrl_parent)

    def create_name(self):

        jnt_names =

        pass

    def create_joint(self):
        pass

