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

    add_extra_group
        在指定对象上方创建一个额外的空组，并保持对象原来的层级和位置关系。
        适合创建 Zero、Offset、Connect、Space 等控制器层级组。

    get_child_object
        获取指定对象下面某种类型的所有子物体，并包含对象本身。
        适合获取 Joint Chain、Transform 层级等连续对象列表。

    select_sub_objects
        快速选择当前所选物体下面指定类型的所有子对象，并包含当前选择对象本身。
        适合快速选择完整 Joint Chain 或 Transform 层级。
"""

import maya.cmds as cmds
import pymel.core as pm


def parent(child_node, parent_node):
    u"""
    先检查子物体和父物体之间是否已经存在父子关系。
    如果不存在，则创建新的父子层级关系。

    该方法同时支持字符串节点名称和 PyNode。
    内部统一转换成 PyNode 后再进行层级检查和 Parent，
    避免 maya.cmds 和 PyNode 混用时出现“对象无效”的问题。

    child_node(str/PyNode): 需要设置父级的子物体节点。
    parent_node(str/PyNode): 需要作为父级的节点。

    Returns:
        None

    Maya 使用示例：

    from muziToolset.core.common import hierarchy_utils

    child_node = "ctrl_lf_eye_main_001"
    parent_node = "grp_md_face_ctrl_001"

    hierarchy_utils.parent(child_node, parent_node)
    """

    # 没有给定父物体时停止执行。
    if not parent_node:
        pm.warning(u"没有给定父物体节点")
        return

    # 统一将传入的字符串或 PyNode 转换成 PyNode。
    # 这样后续层级操作全部使用 PyMEL，避免 cmds.listRelatives() 接收到 PyNode 时
    # 在某些 Maya 环境中出现“对象无效”的问题。
    child_node = pm.PyNode(child_node)
    parent_node = pm.PyNode(parent_node)

    # 获取子物体当前的直接父物体。
    parent_original = child_node.getParent()

    # 当前父物体不是目标父物体时，创建新的 Parent 关系。
    if parent_original != parent_node:
        pm.parent(child_node, parent_node)

    # 已经存在正确父子关系时只给出提示，不重复 Parent。
    else:
        pm.warning(u"{} 已为 {} 的子物体".format(child_node, parent_node))


def chain_parent(child_nodes, parent_node):
    u"""
    将链条式的列表按照顺序整理层级结构。

    child_nodes(list): 需要整理层级结构的物体列表。
    parent_node(str): 第一个物体的父物体。

    Returns:
        None

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


def add_extra_group(object, grp_name, world_orient=False, relation="parent"):
    u"""
    在指定对象的父层级或子层级创建一个额外空组。

    relation="parent" 时：
    新组会插入到对象上方，并保持对象原来的父级关系。

    relation="child" 时：
    新组会创建到对象下方，并匹配对象当前的世界位置。

    object(str/PyNode): 需要添加额外组的 Maya 对象。
    grp_name(str): 新创建的组名称。
    world_orient(bool): 是否让新组保持世界旋转方向，默认 False。
    relation(str): 新组与对象的层级关系，可使用 "parent" 或 "child"，默认 "parent"。

    Returns:
        PyNode: 新创建的 Group 节点。

    Maya 使用示例：

    from muziToolset.core.common import hierarchy_utils

    ctrl = "ctrl_lf_eye_main_001"

    # 在 Controller 上方创建 Zero Group。
    zero_grp = hierarchy_utils.add_extra_group(
        ctrl,
        "zero_lf_eye_main_001",
        relation="parent"
    )

    # 在 Controller 下方创建 Output Group。
    output_grp = hierarchy_utils.add_extra_group(
        ctrl,
        "output_lf_eye_main_001",
        relation="child"
    )

    print(zero_grp)
    print(output_grp)
    """

    # 将传入对象转换成 PyNode。
    object = pm.PyNode(object)

    # 创建新的空组。
    object_grp = pm.group(empty=True, name=grp_name)

    # 根据 world_orient 设置新组的对齐方式。
    if world_orient:
        pm.matchTransform(object_grp, object, position=True, scale=True)
    else:
        pm.matchTransform(object_grp, object, position=True, rotation=True, scale=True)

    # ============================================================
    # Parent 模式
    # ============================================================
    if relation == "parent":

        # 保存对象原来的父物体。
        object_parent = object.getParent()

        # 如果对象原来有父物体，先把新组放回原父级下面。
        if object_parent:
            parent(child_node=object_grp, parent_node=object_parent)

        # 再把原对象放到新组下面。
        parent(child_node=object, parent_node=object_grp)

    # ============================================================
    # Child 模式
    # ============================================================
    elif relation == "child":

        # 将新组放到原对象下面。
        parent(child_node=object_grp, parent_node=object)

    else:
        pm.delete(object_grp)
        raise ValueError(
            u"relation 只能使用 'parent' 或 'child'，当前值：{}".format(relation)
        )

    return object_grp


def get_child_object(object, type="joint"):
    u"""
    获取对象下面指定类型的所有子物体，并包含对象本身。
    返回的列表按照从父级到子级的顺序排列。

    object(str): 需要获取子物体的对象。
    type(str): 需要获取的节点类型，默认 "joint"。

    Returns:
        list: 对象本身和所有指定类型子物体的名称列表。

    Maya 使用示例：

    from muziToolset.core.common import hierarchy_utils

    object = "jnt_lf_arm_bind_001"
    type = "joint"

    object_list = hierarchy_utils.get_child_object(object, type)

    print(object_list)
    """

    # 获取指定类型的所有后代节点。
    object_list = cmds.listRelatives(object, type=type, allDescendents=True) or []

    # 将对象本身加入列表。
    object_list.append(object)

    # 调整顺序，使父级节点排列在子级节点之前。
    object_list.reverse()

    return object_list


def select_sub_objects(obj_type="transform"):
    u"""
    快速选择当前所选物体下面指定类型的所有子对象，并包含当前选择的物体本身。
    支持同时选择多个父物体，并自动避免重复添加相同的子对象。

    obj_type(str): 需要选择的子对象类型，例如 "transform"、"joint"，默认 "transform"。

    Returns:
        list: 最终选择的所有对象名称列表。

    Maya 使用示例：

    from muziToolset.core.common import hierarchy_utils

    obj_type = "joint"

    selection = hierarchy_utils.select_sub_objects(obj_type)

    print(selection)
    """

    # 获取当前选择的所有对象。
    selection = cmds.ls(sl=True) or []
    object_list = []

    # 获取每个选择对象下面指定类型的所有子对象。
    for obj in selection:
        child_objects = get_child_object(obj, obj_type)

        # 避免相同节点被重复加入列表。
        for child_object in child_objects:
            if child_object not in object_list:
                object_list.append(child_object)

    # 将最终得到的对象列表设置为 Maya 当前选择。
    cmds.select(object_list, replace=True)

    return object_list
