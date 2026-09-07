import maya.cmds as cmds

from .. import rig_module
from ...core.common import name_utils
from ...core.rigging import jnt_utils


class EarModule(rig_module.RigModule):

    def __init__(self, module, side, guide, jnt_parent, ctrl_parent):
        super().__init__(module, side, guide, jnt_parent, ctrl_parent)

    def create_joints(self):
        self.jnt_names = []

        for index in range(1, 4):
            name_object = name_utils.Name(
                type="jnt",
                side=self.side,
                part=self.module,
                function="bind",
                index=index
            )

            jnt_name = name_object.compose_name()
            self.jnt_names.append(jnt_name)


