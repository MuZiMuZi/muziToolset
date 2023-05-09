from muziToolset.rigging.base import bone
from importlib import reload
reload(bone)


custom = bone.Bone(side = 'l' , name = 'zz' , index = 5 , joint_parent = None , control_parent = None)
custom.build_bp()
custom.build_rig()