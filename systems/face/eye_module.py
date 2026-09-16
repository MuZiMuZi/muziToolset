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
        u"""

                初始化当前对象，并准备运行时需要的状态和成员。

                Args:
                    module (object):
                        当前方法执行 Maya / Rig 操作时使用的 `module` 数据。
                    side (str):
                        方向标记，常用值为 lf、rt 或 md。
                    guide (str):
                        需要查询或处理的 Guide Transform 名称。
                    jnt_parent (str | None):
                        新建 Jnt Chain 的父 Jnt / Parent Transform；None 表示保持在世界层级。
                    ctrl_parent (object):
                        当前方法执行 Maya / Rig 操作时使用的 `ctrl_parent` 数据。
                    guide_count (int):
                        当前构建、采样或查询过程使用的元素数量。
                    jnt_function (str):
                        当前 Maya / Rig 操作使用的 `jnt_function` 名称或标记。
                    ctrl_function (str):
                        当前 Maya / Rig 操作使用的 `ctrl_function` 名称或标记。
                    ctrl_shape (str):
                        当前 Maya / Rig 操作使用的 `ctrl_shape` 名称或标记。
                    ctrl_color (int):
                        当前 Maya / Rig 操作使用的 `ctrl_color` 整数参数。
                    ctrl_size (float):
                        当前 Maya / Rig 计算使用的 `ctrl_size` 数值参数。
                    ctrl_axis (str):
                        当前 Maya / Rig 操作使用的 `ctrl_axis` 名称或标记。

        """

        super (TongueModule , self).__init__ (
            module = module ,
            side = side ,
            guide = guide ,
            jnt_parent = jnt_parent ,
            ctrl_parent = ctrl_parent
        )

    def get_guides(self):
        u"""

                查询并返回当前 guides。

        """

        super().get_guides()
        #眼球控制器还需要额外创建一个目标约束的驱动，这个驱动