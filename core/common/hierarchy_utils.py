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

    get_or_create_group
        根据名称获取或创建一个空的 Transform Group。
        适合各类 Rig Module 创建 Joint、Controller、Deformer 等总组层级。

    add_extra_group
        在指定对象的父层级或子层级添加一个额外空组。
        如果同名组已经存在则直接获取并复用，不存在时才创建。
        适合创建 Zero、Offset、Connect、Space、Output 等控制器层级组。

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


def get_or_create_group(group_name):
    u"""
    根据名称获取或创建一个空的 Transform Group。

    如果场景中已经存在同名 Transform，则直接获取并返回。
    如果同名节点存在但不是 Transform，则抛出错误。
    如果场景中不存在该名称，则创建新的空 Group。

    group_name(str): 需要获取或创建的 Group 名称。

    Returns:
        PyNode: 获取或创建的 Transform Group。

    Maya 使用示例：

    from muziToolset.core.common import hierarchy_utils

    group = hierarchy_utils.get_or_create_group(
        "grp_lf_ear_ctrl_001"
    )

    print(group)
    """

    # 场景中已经存在同名节点时直接获取。
    if pm.objExists(group_name):
        group = pm.PyNode(group_name)

        # Rig Group 必须是 Transform，避免误用其他同名节点。
        if not isinstance(group, pm.nodetypes.Transform):
            raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(group_name))

        return group

    # 场景中不存在时创建新的空 Group。
    group = pm.group(empty=True, name=group_name)

    return group


def add_extra_group(object, grp_name, world_orient=False, relation="parent"):
    u"""
    在指定对象的父层级或子层级添加一个额外空组，并支持安全重复执行。

    relation="parent" 时：
    Group 会位于对象上方。
    新建 Group 时会保持对象原来的父级关系；
    如果同名 Group 已经存在，则直接获取并确保对象位于该 Group 下方。

    relation="child" 时：
    Group 会位于对象下方。
    如果同名 Group 已经存在，则直接获取并确保它位于对象下方。

    已经存在的 Group 不会再次执行 matchTransform，避免重复调用时修改已有层级的 Transform。
    只有真正新建 Group 时才会根据 world_orient 对齐到指定对象。

    object(str/PyNode): 需要添加额外组的 Maya 对象。
    grp_name(str): 需要创建或获取的 Group 名称。
    world_orient(bool): 是否让新创建的 Group 保持世界旋转方向，默认 False。
    relation(str): Group 与对象的层级关系，可使用 "parent" 或 "child"，默认 "parent"。

    Returns:
        PyNode: 创建或获取到的 Group 节点。

    Maya 使用示例：

    from muziToolset.core.common import hierarchy_utils

    ctrl = "ctrl_lf_eye_main_001"

    # 第一次执行会创建 Offset Group。
    offset_grp = hierarchy_utils.add_extra_group(
        ctrl,
        "offset_lf_eye_main_001",
        relation="parent"
    )

    # 再次执行会直接获取并复用同名 Group，不会创建 offset_lf_eye_main_0011。
    offset_grp = hierarchy_utils.add_extra_group(
        ctrl,
        "offset_lf_eye_main_001",
        relation="parent"
    )

    # 在 Controller 下方创建或获取 Output Group。
    output_grp = hierarchy_utils.add_extra_group(
        ctrl,
        "output_lf_eye_main_001",
        relation="child"
    )

    print(offset_grp)
    print(output_grp)
    """

    # relation 只接受 parent 和 child。
    # 在创建任何 Maya 节点之前先检查参数，避免无效参数产生多余节点。
    if relation not in ("parent", "child"):
        raise ValueError(u"relation 只能使用 'parent' 或 'child'，当前值：{}".format(relation))

    # 将传入对象转换成 PyNode，后续统一使用 PyMEL 对象操作。
    object = pm.PyNode(object)

    # Parent 模式在新建 Group 时需要保持对象原来的父级关系，
    # 因此在修改层级之前先保存对象当前父物体。
    object_parent = None
    if relation == "parent":
        object_parent = object.getParent()

    # ------------------------------------------------------------
    # 获取或创建 Group。
    # ------------------------------------------------------------
    if pm.objExists(grp_name):
        # 同名节点已经存在时直接获取，不重复创建。
        object_grp = pm.PyNode(grp_name)

        # Extra Group 必须是 Transform，避免同名 Shape 或其他 DG 节点被误用。
        if not isinstance(object_grp, pm.nodetypes.Transform):
            raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(grp_name))

    else:
        # 同名 Group 不存在时才真正创建新的空组。
        object_grp = pm.group(empty=True, name=grp_name)

        # 只有新创建的 Group 才需要匹配对象 Transform。
        if world_orient:
            pm.matchTransform(object_grp, object, position=True, scale=True)
        else:
            pm.matchTransform(object_grp, object, position=True, rotation=True, scale=True)

        # Parent 模式下，新 Group 需要插入对象原来的父级与对象之间。
        # 先把新 Group 放回对象原来的父级下面，再把对象放到新 Group 下面。
        if relation == "parent" and object_parent:
            parent(child_node=object_grp, parent_node=object_parent)

    # ------------------------------------------------------------
    # Parent 模式：object_grp -> object
    # ------------------------------------------------------------
    if relation == "parent":
        if object.getParent() != object_grp:
            parent(child_node=object, parent_node=object_grp)

    # ------------------------------------------------------------
    # Child 模式：object -> object_grp
    # ------------------------------------------------------------
    elif relation == "child":
        if object_grp.getParent() != object:
            parent(child_node=object_grp, parent_node=object)

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
