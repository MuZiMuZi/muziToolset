import muziToolset.rigging.mateHumanRigging.matehuman_base_rig as matehuman_base_rig
import muziToolset.rigging.mateHumanRigging.matehuman_master_rig as matehuman_master_rig
from importlib import reload
reload(matehuman_master_rig)
reload(matehuman_base_rig)

base = matehuman_master_rig.Master_Rig()


