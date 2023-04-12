# import matehuman_base_rig
# import matehuman_master_rig
from importlib import reload



reload(matehuman_master_rig)
reload(matehuman_base_rig)

base = matehuman_master_rig.Master_Rig()
