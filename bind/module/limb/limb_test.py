from importlib import reload

import muziToolset.bind.module.limb.limbIK as limbIK


reload (limbIK)

custom = limbIK.LimbIK (side = 'l' , name = 'zz' , jnt_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
                        is_stretch = 1 ,
                        limb_type = 'arm' ,
                        jnt_parent = None ,
                        ctrl_parent = None)
# custom.build_setup ()
custom.build_rig ()