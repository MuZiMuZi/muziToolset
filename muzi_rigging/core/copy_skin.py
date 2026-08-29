def copy_weight () :
    u'''

    Returns:复制权重，先选择需要复制的蒙皮权重物体，再加选需要复制权重的物体

    '''
    # 获取选择
    sel = cmds.ls (selection = True)

    source_mesh = sel [0]
    target_meshes = sel [1 :]

    # 查询目标对象是否具有蒙皮信息
    for target_mesh in target_meshes :
        target_skin = mel.eval ('findRelatedSkinCluster("' + target_mesh + '")')
        if target_skin :
            cmds.delete (target_skin)

    # 获取源对象的蒙皮信息
    source_skin = mel.eval ('findRelatedSkinCluster("' + source_mesh + '")')

    # 获取源对象受影响的蒙皮信息
    source_joints = cmds.skinCluster (source_skin , query = True , influence = True)

    # 在每个目标对象中循环
    for target_mesh in target_meshes :
        # 用源关节绑定蒙皮
        target_skin = cmds.skinCluster (source_joints , target_mesh , toSelectedBones = True) [0]

        # 复制蒙皮权重
        cmds.copySkinWeights (sourceSkin = source_skin , destinationSkin = target_skin , noMirror = True ,
                              surfaceAssociation = 'closestPoint' , influenceAssociation = ['label' , 'oneToOne'])
copy_weight()
