"""
选择边创建关节，这个关节在边的中心位置，并且根据边的长度可以进行调整关节的半径大小
"""

import  pymel.core as pm
# 获取所选择物体的shape节点
edges = pm.selected(flatten = True)

mesh = edges[0].node()
boundaries_vert_ids = []
parent_jnt = None
#获取没有相邻的线上的点的编号
for e in edges:
    e_verts = e.connectedVartices()
    e_verts_ids = [v.index()for v in e_verts]
    boundaries_vert_ids.extend(e_verts_ids)


v_get_p = lambda id :mesh.vtx[id].getPosition(space = 'world')
boundaries_vert_points = [v_get_p(id)for id in list(set(boundaries_vert_ids))]

# 根据获取的所有点的位置信息来获取中心点位置
center = sum(boundaries_vert_points)/len(boundaries_vert_points)


# 创建关节并且设置关节的半径大小显示
jnt = pm.joint(p = center)

edge_length = sum([e.getLength()]for e in edges)

jnt.radius.set(edge_length/5)

# 设置关节的父对象
if parent_jnt is None:
    pass
else:
    jnt.setParent(parent_jnt)
    parent_jnt.orientJoint('xyz',secondaryAxisOrient = 'yup')

parent_jnt = jnt
