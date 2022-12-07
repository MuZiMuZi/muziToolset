import  pymel.core as pm
shapenodes = pm.selected()[0].getShape()

def getBindJoints(shape):
    # 获取形状节点的历史节点类型为joint的节点
    all_jnts = shape.history(type = 'joint')

    assert len(all_jnts),u'请选择具有蒙皮的模型'
    #根据关节名称的长度进行排序
    sort_function = lambda jnt:len(jnt.longName())
    all_jnts = sorted(all_jnts,key = sort_function)
    all_jnts_longName=[]
    for jnt in all_jnts:
        all_jnts_longName.append(jnt.longName())

    return all_jnts_longName

def getRootJoint(shape):
    all_jnts = getBindJoints(shape)
    return all_jnts[0]

print(getBindJoints(shapenodes))