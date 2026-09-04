# coding=utf-8
u"""
hierarchy_utils：Maya 层级关系基础工具。

方法介绍与使用场景：

    parent
        创建普通父子层级关系。
        适合 Controller、Joint、Group 等节点的父子整理。

    chain_parent
        按照列表顺序创建链条式父子层级关系。
        适合 Joint Chain、FK Chain 等连续层级结构。
"""

import maya.cmds as cmds
import pymel.core as pm

def parent(child_node, parent_node):
    u"""
    先查找子物体和父物体之间是否有父子层级关系，没有的话制作父子层级关系。

    :param child_node: 子物体节点名称。
    :param parent_node: 父物体节点名称。

    Maya 使用示例：

        from muziToolset.core.common import hierarchy_utils

        hierarchy_utils.parent(
            "ctrl_lf_eye_main_001",
            "grp_md_face_ctrl_001"
        )
    """

    if parent_node:
        parent_original = cmds.listRelatives(
            child_node,
            parent=True
        )

        if not parent_original or parent_original[0] != parent_node:
            cmds.parent(
                child_node,
                parent_node
            )
        else:
            cmds.warning(
                u"{} 已为 {} 的子物体".format(
                    child_node,
                    parent_node
                )
            )
    else:
        cmds.warning(
            u"没有给定父物体节点"
        )


def chain_parent(child_nodes, parent_node):
    u"""
    将链条式的列表按照顺序整理层级结构。

     child_nodes(list): 需要整理层级结构的物体列表。
     parent_node(str): 第一个物体的父物体。

    Maya 使用示例：

    from muziToolset.core.common import hierarchy_utils
    child_nodes = ["jnt_lf_arm_bind_001",
            "jnt_lf_arm_bind_002",
            "jnt_lf_arm_bind_003"]
    parent_node = "grp_md_skeleton_001"


    hierarchy_utils.chain_parent(child_nodes, parent_node)


    # 最终层级：
    # grp_md_skeleton_001
    #     jnt_lf_arm_bind_001
    #         jnt_lf_arm_bind_002
    #             jnt_lf_arm_bind_003
    """

    for child_node in child_nodes:
        parent(
            child_node,
            parent_node
        )
        parent_node = child_node

def add_extra_group(object, grp_name, world_orient=False):
    u"""
    在对象上方添加一个额外的组。

    object(str): 要添加额外组的 Maya 对象。
    grp_name(str): 新创建的组名称。
    world_orient(bool): 是否让新组保持世界旋转方向。

    Returns:
        str: 新创建的组名称。

    Maya 使用示例：

    import pymel.core as pm
    from muziToolset.core.common import hierarchy_utils

    object = "ctrl_lf_eye_main_001"
    grp_name = "offset_lf_eye_main_001"

    new_group = hierarchy_utils.add_extra_group(object, grp_name, world_orient=False)

    print(new_group)
    """
    #利用PyNode实例化object
    object = pm.PyNode(object)
    #获取object的父物体
    object_parent = object.getParent()
    #根据新的组名称创建新租
    object_grp = pm.group(empty=True, name=grp_name)
    #判断如果需要保持世界旋转方向
    if world_orient:
        pm.matchTransform(object_grp, object, position=True, scale=True)
    else:
        pm.matchTransform(object_grp, object, position=True, rotation=True, scale=True)
    #整理层级结构
    if object_parent:
        parent(child_node = object_grp, parent_node = object_parent)

    parent (child_node = object , parent_node = object_grp)

    return object_grp.name()

def get_child_object(object, type="joint"):
    u"""
    获取对象下面指定类型的所有子物体，并包含对象本身。

    object(str): 需要获取子物体的对象。
    type(str): 需要获取的节点类型，默认 joint。

    Returns:
        list: 对象本身和所有指定类型子物体的名称列表。

    Maya 使用示例：

    from muziToolset.core.common import hierarchy_utils

    object = "jnt_lf_arm_bind_001"
    type = "joint"

    object_list = hierarchy_utils.get_child_object(object, type)

    print(object_list)
    """

    object_list = cmds.listRelatives(object, type=type, allDescendents=True) or []

    object_list.append(object)
    object_list.reverse()

    return object_list