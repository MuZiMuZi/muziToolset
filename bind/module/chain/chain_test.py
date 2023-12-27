from importlib import reload

import muziToolset.bind.module.chain.chain as chain


reload (chain)

chain = chain.Chain (side = 'l' , name = 'test' , jnt_number = 4 , length = 10 , jnt_parent = None ,
                     control_parent = None)

# 创建定位系统
chain.build_setup ()

# # 生成绑定
# chain.build_rig ()
#
# #删除绑定
# bone.delete_rig()
