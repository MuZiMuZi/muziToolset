# coding=utf-8
faces = cmds.ls (sl = True)
geo1 = 'pCylinder1'
geo2 = 'pCylinder2'

skin_faces = []
for face in faces :
    skin_face = face.replace (geo1 , geo2)
    skin_faces.append (skin_face)

# 选择同样的面
cmds.select (skin_faces , replace = True)
# 在简模物体上删除未选择的面
all_skin_faces = pm.ls (geo2 + '.f[*]' , flatten = True)

set_a = set (all_skin_faces)
set_b = set (skin_faces)
#
non_selected_skin_faces = list (set_a.difference (set_b))
print(non_selected_skin_faces)
pm.delete (non_selected_skin_faces)