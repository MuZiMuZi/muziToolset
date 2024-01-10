# coding=utf-8
faces = cmds.ls (sl = True , flatten = True)
geo1 = 'pCylinder1'
geo2 = 'pCylinder2'

skin_faces = []
for face in faces :
    skin_face = face.replace (geo1 , geo2)
    skin_faces.append (skin_face)

# 选择同样的面
cmds.select (skin_faces , replace = True)
# 在简模物体上删除未选择的面
all_skin_faces = cmds.ls (geo2 + '.f[*]' , flatten = True)
set_a = all_skin_faces
# set_a = set (all_skin_faces)
#
print(skin_faces)
for skin_face in skin_faces:
    set_a.remove(skin_face)
print(skin_face)
non_selected_skin_faces = set_a
pm.delete (non_selected_skin_faces)