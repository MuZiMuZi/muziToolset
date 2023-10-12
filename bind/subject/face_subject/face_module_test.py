import muziToolset.bind.subject.face_subject.face_rig as face_rig
from importlib import reload



reload(face_rig)

face = face_rig.Face_rig()

#创建定位系统
face.build_setup()
#生成绑定
face.build_rig()
