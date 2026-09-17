# coding=utf-8
# 获取需要绘制权重的模型和用来复制权重的低模
high_geo = cmds.ls (sl = True) [0].split('.f')[0]
skin_geo = cmds.duplicate (high_geo , name = 'skinModle_' + high_geo) [0]

# 获取需要绘制的模型上所选择的面
high_faces = cmds.ls (sl = True , flatten = True)

# 获取简模上应该选择的面
skin_faces = []
for face in high_faces :
    skin_face = face.replace (high_geo , skin_geo)
    skin_faces.append (skin_face)

# 在制作出来的简模上选择同样的面
cmds.select (skin_faces , replace = True)

# 获取简模上所有的面
all_skin_faces = cmds.ls (skin_geo + '.f[*]' , flatten = True)

non_selected_skin_faces = all_skin_faces
# 对简模上选择的面做循环，从所有的面的列表里移除，得出没有被选择的面删除
if skin_face in skin_faces :
    non_selected_skin_faces.remove (skin_face)
else :
    pass
# 删除物体没有被选择的面
pm.delete (non_selected_skin_faces)