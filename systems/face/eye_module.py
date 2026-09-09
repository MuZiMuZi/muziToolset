import maya.cmds as cmds

from .. import rig_module
from ...core.common import name_utils, hierarchy_utils
class TongueModule(rig_module.RigModule):

    def __init__ (
            self ,
            module ,
            side = "md" ,
            guide = None ,
            jnt_parent = None ,
            ctrl_parent = None ,
            guide_count = 1 ,
            jnt_function = "bind" ,
            ctrl_function = "fk" ,
            ctrl_shape = "circle" ,
            ctrl_color = 17 ,
            ctrl_size = 1.0 ,
            ctrl_axis = "X+"
    ) :
        super (TongueModule , self).__init__ (
            module = module ,
            side = side ,
            guide = guide ,
            jnt_parent = jnt_parent ,
            ctrl_parent = ctrl_parent
        )

    def get_guides(self):
        super().get_guides()
        #眼球控制器还需要额外创建一个目标约束的驱动，这个驱动