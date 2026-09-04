
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