from importlib import reload

import muziToolset.bind.module.base.base as base


reload (base)

bone = base.Base (side = 'l' , name = 'test' , jnt_number = 4)

# 创建定位系统
bone.build_setup ()

# 生成绑定
bone.build_rig ()
#
# #删除绑定
# bone.delete_rig()
