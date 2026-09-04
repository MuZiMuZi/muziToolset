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

    :param child_nodes: 需要整理层级结构的物体列表。
    :param parent_node: 第一个物体的父物体。

    Maya 使用示例：

        from muziToolset.core.common import hierarchy_utils

        hierarchy_utils.chain_parent(
            [
                "jnt_lf_arm_bind_001",
                "jnt_lf_arm_bind_002",
                "jnt_lf_arm_bind_003"
            ],
            "grp_md_skeleton_001"
        )

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
