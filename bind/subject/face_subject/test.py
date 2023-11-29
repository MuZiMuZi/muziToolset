import muziToolset.bind.subject.face_subject.eyeLid as eyeLid
from importlib import reload


reload (eyeLid)
eye_lid_upper = eyeLid.EyeLid (side = 'l' , name = 'upper' , joint_number = 7 , joint_parent = None ,
                               control_parent = None)
# eye_lid_upper.build_setup ()
eye_lid_upper.build_rig ()