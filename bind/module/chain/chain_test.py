from importlib import reload

import muziToolset.bind.module.chain.chainIKFK as chainIKFK

reload (chainIKFK)

chain = chainIKFK.ChainIKFK (side = 'l' , name = 'zz' , jnt_number = 3 , direction = [-1 , 0 , 0] ,
                             length = 10 ,
                             is_stretch = 1 ,
                             jnt_parent = None ,
                             ctrl_parent = None)

# 创建定位系统
chain.build_setup ()

# 生成绑定
chain.build_rig ()
#
# #删除绑定
# bone.delete_rig()
