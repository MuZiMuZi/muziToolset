import muziToolset.bind.module.base.base as base
from importlib import reload


reload (base)

bone = base.Base (side = 'l', name = 'test', joint_number = 4)

# 创建定位系统
bone.build_setup ()

# 生成绑定
bone.build_rig ()
#
# #删除绑定
# bone.delete_rig()