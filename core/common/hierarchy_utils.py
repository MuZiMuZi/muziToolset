
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