import muziToolset.bind.subject.face_subject.eyeLid as eyeLid
from importlib import reload


reload (eyeLid)
eye_lid_upper = eyeLid.EyeLid (side = 'l' , name = 'upper' , jnt_number = 7 , jnt_parent = None ,
                               control_parent = None)
# eye_lid_upper.build_setup ()
eye_lid_upper.build_rig ()



import muziToolset.bind.subject.face_subject.brow as brow
from importlib import reload


reload (brow)
brow_m = brow.Brow (side = 'm' , jnt_parent = None , control_parent = None)
brow_m.build_setup ()
brow_m.build_rig ()
#mouth
import muziToolset.bind.subject.face_subject.mouth as mouth
from importlib import reload


reload (mouth)
mouth_m = mouth.Mouth (side = 'm' , name = '' , jnt_number = 2 , jnt_parent = None ,
                       control_parent = None)
mouth_m.build_setup ()

mouth_m.build_rig ()

#nose
import muziToolset.bind.subject.face_subject.nose as nose
from importlib import reload


reload (nose)

nose_m = nose.Nose (jnt_parent = None , control_parent = None)
nose_m.build_setup ()
nose_m.build_rig ()


#tongue
import muziToolset.bind.subject.face_subject.tongue as tongue
from importlib import reload


reload (tongue)
tongue_m = tongue.Tongue (side = 'm' , name = '' , jnt_number = 5 , direction = [-1 , 0 , 0] , length = 10 ,
                          jnt_parent = None ,
                          control_parent = None)
tongue_m.build_setup ()
tongue_m.build_rig ()


#cheek
import muziToolset.bind.subject.face_subject.cheek as cheek
from importlib import reload


reload (cheek)
cheek_m = cheek.Cheek (side = 'm' , name = '' , jnt_number = 8 , jnt_parent = None ,
                       control_parent = None)
cheek_m.build_setup ()
cheek_m.build_rig ()

# jaw
import muziToolset.bind.subject.face_subject.jaw as jaw
from importlib import reload


reload (jaw)
jaw_m = jaw.Jaw (side = 'm' , name = '' , jnt_number = 2 , jnt_parent = None ,
                       control_parent = None)
jaw_m.build_setup ()
jaw_m.build_rig ()

#eye
import muziToolset.bind.subject.face_subject.eye as eye
from importlib import reload


reload (eye)
eye_l = eye.Eye (side = 'l' , name = '' , jnt_number = 2 , length = 10 , jnt_parent = None ,
                 control_parent = None)
eye_l.build_setup ()
eye_r = eye.Eye (side = 'r' , name = '' , jnt_number = 2 , length = 10 , jnt_parent = None ,
                 control_parent = None)
eye_r.build_setup ()

eye_l.build_rig ()
eye_r.build_rig ()

#ear
import muziToolset.bind.subject.face_subject.ear as ear
from importlib import reload


reload (ear)
ear_l = ear.Ear (side = 'l' , jnt_parent = None , control_parent = None)
ear_l.build_setup ()

ear_r = ear.Ear (side = 'r' , jnt_parent = None , control_parent = None)
ear_r.build_setup ()



ear_l.build_rig ()


ear_r.build_rig ()


