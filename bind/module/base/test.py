import muziToolset.bind.module.base.bone as bone
from importlib import reload


reload (bone)

bone = bone.Bone ()

# 创建定位系统
bone.build_setup ()
# 生成绑定
bone.build_rig ()
