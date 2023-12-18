import muziToolset.bind.subject.face_subject.eyeLid as eyeLid
from importlib import reload


reload (eyeLid)
eye_lid_upper = eyeLid.EyeLid (side = 'l' , name = 'upper' , joint_number = 7 , joint_parent = None ,
                               control_parent = None)
# eye_lid_upper.build_setup ()
eye_lid_upper.build_rig ()



import muziToolset.bind.subject.face_subject.brow as brow
from importlib import reload


reload (brow)
brow_m = brow.Brow (side = 'm' , joint_parent = None , control_parent = None)
brow_m.build_setup ()
brow_m.build_rig ()

import muziToolset.bind.subject.face_subject.mouth as mouth
from importlib import reload


reload (mouth)
mouth_m = mouth.Mouth (side = 'm' , name = '' , joint_number = 2 , joint_parent = None ,
                       control_parent = None)
mouth_m.build_setup ()

mouth_m.build_rig ()

import muziToolset.bind.subject.face_subject.nose as nose
from importlib import reload


reload (nose)

nose_m = nose.Nose (joint_parent = None , control_parent = None)
nose_m.build_setup ()
nose_m.build_rig ()