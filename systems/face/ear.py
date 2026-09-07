import maya.cmds as cmds

from common import name_utils
from systems import rig_module
from importlib import reload
form ....core.common  import *
reload(rig_module)

class Ear(rig_module.RigModule):
    def __init__(self,module, side, guide, jnt_parent,ctrl_parent):
        super().__init__(module, side, guide, jnt_parent,ctrl_parent)

    def create_name(self):
        self.jnt_names_list = []
        for index in  range(3):
            self.jnt_names = name_utils.Name(type = 'jnt',side = self.side,part = 'ear',function = 'bind',index = index)
            self.jnt_names_list.append(self.jnt_names)

    def create_joint(self):
        pass

