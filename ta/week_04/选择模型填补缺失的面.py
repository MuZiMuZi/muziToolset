import  pymel.core as pm
# 获取所选择物体的shape节点
mesh = pm.selected()[0].getShape()

# 遍历模型上的线，检查是否有线没有相邻，这些没有相邻的线就是我们需要补充的空洞
boundaries = [e for e in mesh.e if e.isOnBoundary()]

# polyExtrudeEdge 是挤出的命令
pm.polyExtrudeEdge(boundaries,kft = True)

#选择的物体中减选模型的transform节点，
pm.select(mesh.getTransform(),deselect = True)

boundaries_vert_ids = []

#获取没有相邻的线上的点的编号
for e in boundaries:
    e_verts = e.connectedVertices()
    e_verts_ids = [v.index()for v in e_verts]
    boundaries_vert_ids.extend(e_verts_ids)

#根据没有相邻的线上的点的编号来获取对应点的位置信息

v_get_p = lambda id :mesh.vtx[id].getPosition(space = 'world')
boundaries_vert_points = [v_get_p(id)for id in list(set(boundaries_vert_ids))]

# 根据获取的所有点的位置信息来获取中心点位置
center = sum(boundaries_vert_points)/len(boundaries_vert_points)

#缩放
pm.scale(0,0,0,p = center,a = True)
