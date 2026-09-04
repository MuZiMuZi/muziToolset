
def parent (child_node , parent_node) :
    u"""
    先查找子物体和父物体之间是否有父子层级关系，没有的话制作父子层级关系
    :param child_node（str）:子物体的节点名称
    :param parent_nodestr）:父物体的节点名称
    :return:
    """
    if parent_node :
        parent_original = cmds.listRelatives (child_node , parent = True)
        if not parent_original or parent_original [0] != parent_node :
            cmds.parent (child_node , parent_node)
        else :
            cmds.warning (u'{} 已为 {}的子物体'.format (child_node , parent_node))
    else :
        cmds.warning (u'没有给定父物体节点')

def chain_parent (child_nodes , parent_node) :
    """
    将链条式的列表按照顺序整理层级结构
    child_nodes：需要整理层级结构的物体列表
    parent_node：第一个物体的父物体
    """
    for child_node in child_nodes :
       parent(child_node , parent_node)
       parent_node = child_node

def add_extra_group (obj , grp_name , world_orient = False) :
    u"""在对象上方添加一个额外的组.

    Args:
        obj (str):要添加额外组的Maya对象.
        grp_name (str): 额外的组名
        world_orient (bool): 设置新组的世界位置是否改变。

    Returns:
        str: 新添加的组.

    """
    #创建一个组
    obj_grp = cmds.group (name = grp_name , empty = True)
    t_pos = cmds.xform (obj , query = True , worldSpace = True , translation = True)
    r_pos = cmds.xform (obj , query = True , worldSpace = True , rotation = True)
    if world_orient :
        r_pos = [0 , 0 , 0]
    s_pos = cmds.xform (obj , q = True , worldSpace = True , s = True)
    cmds.xform (obj_grp , s = s_pos)
    cmds.xform (obj_grp , ws = True , t = t_pos)
    cmds.xform (obj_grp , ws = True , ro = r_pos)

    obj_parent = cmds.listRelatives (obj , parent = True)
    if obj_parent :
        cmds.parent (obj_grp , obj_parent [0] , absolute = True)
        cmds.parent (obj , obj_grp , absolute = True)
    else :
        cmds.parent (obj , obj_grp , absolute = True)

    return obj_grp