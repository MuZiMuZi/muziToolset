import muziToolset.bind.module.base.bone as bone
from importlib import reload


reload (bone)

bone = bone.Bone (side = 'l', name = 'test', joint_number = 4)

# 创建定位系统
bone.build_setup ()

# 生成绑定
bone.build_rig ()
