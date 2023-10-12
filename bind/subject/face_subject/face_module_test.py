import muziToolset.bind.subject.face_subject.face_rig as face_rig
from importlib import reload



reload(face_rig)

face = face_rig.Face_rig()

face.build_setup()
# build_rig()
