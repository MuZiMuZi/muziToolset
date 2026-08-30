# coding=utf-8
u"""
Hierarchy Utils
===============

Maya DAG 层级通用操作模块。

正式模块路径
------------
``muziToolset.core.hierarchy_utils`` 是 DAG Hierarchy 能力的唯一正式实现。
旧 ``hierarchyUtils.py`` 兼容模块已经完成迁移并删除，正式代码统一使用 snake_case Import。

模块职责
--------
本模块只处理 Transform / Joint 等 DAG 节点之间的父子关系、额外层级组、子层级查询和基础组创建。

公开类
------
Hierarchy
    Maya DAG 层级相关的通用静态方法集合。

公开方法
--------
Hierarchy.get_parent(node, full_path=True)
    返回节点直接 Parent。

Hierarchy.get_children(node, node_type=None, full_path=True)
    返回节点直接 Child，可选按 Maya Node Type 过滤。

Hierarchy.parent(child_node, parent_node)
    确保 child_node 位于指定 parent_node 下。

Hierarchy.add_extra_group(obj, grp_name, world_orient=False)
    在对象上方插入一个额外 Transform Group，并保持对象世界姿态。

Hierarchy.get_child_object(object, type="joint")
    获取指定类型的全部后代，并把根对象一起返回。

Hierarchy.select_sub_objects(obj_type="transform")
    兼容旧工具：根据当前 Selection 选择指定类型的全部后代。

Hierarchy.create_grp(grp, parent=None)
    安全创建一个 Transform Group；已存在时直接返回。

设计原则
--------
1. Maya 节点存在性统一复用 scene_utils.validate_node，不维护第二套底层校验；
2. Core 只负责 DAG 层级，不 import Controller / Face / Body System；
3. 插入额外 Group 时必须保持原对象世界 Transform；
4. Generic Query 不读取 UI，只有明确标为 Legacy Compatibility 的方法允许使用 Selection；
5. 已迁移到 systems.controller 的完整 Rig Workflow 不再继续扩张到本模块；
6. 模块文件名与所有正式 Import 统一使用 snake_case。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import rename_utils
from . import scene_utils


class Hierarchy(object):
    """Maya DAG 层级操作兼容类。"""

    # =========================================================================
    # Validate / Query / Parent
    # =========================================================================

    @staticmethod
    def _validate_node(node, label=u"节点"):
        u"""
        兼容旧内部调用的 DAG 节点校验入口。

        真正的节点存在性规则统一由 scene_utils.validate_node 维护。
        """
        try:
            # 使用 Scene Core 统一检查节点是否存在。
            scene_utils.validate_node(
                node
            )
        except RuntimeError:
            raise RuntimeError(
                u"{}不存在：{}".format(
                    label,
                    node
                )
            )

        return True

    @staticmethod
    def get_parent(node, full_path=True):
        u"""
        返回一个 DAG 节点的直接 Parent。

        Args:
            node (str):
                需要查询 Parent 的 Maya DAG 节点。
            full_path (bool):
                True 时返回 Long DAG Path。

        Returns:
            str | None:
                直接 Parent；没有 Parent 时返回 None。
        """
        # 使用 Scene Core 统一确认查询目标存在。
        scene_utils.validate_node(
            node
        )

        parents = cmds.listRelatives(
            node,
            parent=True,
            fullPath=full_path
        )

        if parents is None:
            parents = []

        if not parents:
            return None

        return parents[0]

    @staticmethod
    def get_children(
            node,
            node_type=None,
            full_path=True
    ):
        u"""
        返回一个 DAG 节点的直接 Child。

        Args:
            node (str):
                需要查询 Child 的 Maya DAG 节点。
            node_type (str | None):
                可选 Maya Node Type，例如 transform / joint。
            full_path (bool):
                True 时返回 Long DAG Path。

        Returns:
            list[str]:
                直接 Child 列表。
        """
        # 使用 Scene Core 统一确认查询目标存在。
        scene_utils.validate_node(
            node
        )

        kwargs = {
            "children": True,
            "fullPath": full_path,
        }

        if node_type:
            kwargs["type"] = node_type

        children = cmds.listRelatives(
            node,
            **kwargs
        )

        if children is None:
            children = []

        return children

    @staticmethod
    def parent(child_node, parent_node):
        u"""
        确保 child_node 位于指定 parent_node 下。

        Returns:
            str:
                Parent 后 Maya 返回的 Child Path；已经是正确父子关系时返回原节点。
        """
        # 使用统一节点校验入口检查 Child。
        Hierarchy._validate_node(
            child_node,
            label=u"子节点"
        )

        # 使用统一节点校验入口检查 Parent。
        Hierarchy._validate_node(
            parent_node,
            label=u"父节点"
        )

        # 查询当前直接 Parent，避免重复 Parent 导致无意义 DAG Path 变化。
        parent_original = Hierarchy.get_parent(
            child_node,
            full_path=True
        )

        parent_matches = cmds.ls(
            parent_node,
            long=True
        ) or []

        parent_long_name = parent_node

        if parent_matches:
            parent_long_name = parent_matches[0]

        if parent_original == parent_long_name:
            return child_node

        result = cmds.parent(
            child_node,
            parent_node,
            absolute=True
        )

        if result:
            return result[0]

        return child_node

    # =========================================================================
    # Insert Extra Group
    # =========================================================================

    @staticmethod
    def add_extra_group(obj, grp_name, world_orient=False):
        u"""
        在对象上方插入一个额外 Transform Group，并保持对象世界姿态。
        """
        # 使用统一节点校验入口检查需要插组的目标对象。
        Hierarchy._validate_node(
            obj,
            label=u"目标对象"
        )

        if not grp_name:
            raise RuntimeError(u"Group 名称不能为空。")

        if cmds.objExists(grp_name):
            raise RuntimeError(
                u"Group 名称已经存在：{}".format(grp_name)
            )

        # 记录目标对象世界位置 / 旋转 / 缩放，保证插入 Group 后视觉姿态不跳动。
        translation = cmds.xform(
            obj,
            query=True,
            worldSpace=True,
            translation=True
        )
        rotation = cmds.xform(
            obj,
            query=True,
            worldSpace=True,
            rotation=True
        )
        scale = cmds.xform(
            obj,
            query=True,
            relative=True,
            scale=True
        )

        # 使用统一 Parent 查询记录原层级，后面把新 Group 放回相同 Parent。
        original_parent = Hierarchy.get_parent(
            obj,
            full_path=True
        )

        if world_orient:
            rotation = [0.0, 0.0, 0.0]

        object_group = cmds.createNode(
            "transform",
            name=grp_name
        )

        cmds.xform(
            object_group,
            worldSpace=True,
            translation=translation
        )
        cmds.xform(
            object_group,
            worldSpace=True,
            rotation=rotation
        )
        cmds.xform(
            object_group,
            relative=True,
            scale=scale
        )

        if original_parent:
            # 把新 Group 放回目标对象原来的父级空间。
            object_group = Hierarchy.parent(
                object_group,
                original_parent
            )

        # 最后把目标对象放入新 Group，完成 Extra Group 插入。
        Hierarchy.parent(
            obj,
            object_group
        )

        return object_group

    # =========================================================================
    # Hierarchy Query
    # =========================================================================

    @staticmethod
    def get_child_object(object, type="joint"):
        u"""
        获取指定类型的全部后代，并把根对象放在列表第一位。
        """
        # 使用统一节点校验入口检查查询根对象。
        Hierarchy._validate_node(
            object,
            label=u"根对象"
        )

        descendants = cmds.listRelatives(
            object,
            allDescendents=True,
            type=type,
            fullPath=True
        ) or []

        # Maya allDescendents 通常从深层返回，这里反转成更直观的根到子层顺序。
        descendants.reverse()

        result = [object]

        for descendant in descendants:
            result.append(descendant)

        return result

    @staticmethod
    def select_sub_objects(obj_type="transform"):
        u"""
        兼容旧工具：选择当前 Selection 下指定类型的全部后代。

        新代码应由 Tool 读取 Selection，再调用无 UI 依赖的查询 API。
        """
        selections = cmds.ls(
            selection=True,
            long=True
        ) or []

        result = []

        for selection in selections:
            if selection not in result:
                result.append(selection)

            descendants = cmds.listRelatives(
                selection,
                allDescendents=True,
                type=obj_type,
                fullPath=True
            ) or []

            for descendant in descendants:
                if descendant not in result:
                    result.append(descendant)

        if result:
            cmds.select(
                result,
                replace=True
            )

        return result

    # =========================================================================
    # Generic Group Creation
    # =========================================================================

    @staticmethod
    def create_grp(grp, parent=None):
        u"""创建一个 Transform Group；已存在时直接返回现有节点。"""
        if not grp:
            raise RuntimeError(u"Group 名称不能为空。")

        if cmds.objExists(grp):
            return grp

        if parent:
            # 使用统一节点校验入口确认指定 Parent 可用。
            Hierarchy._validate_node(
                parent,
                label=u"父节点"
            )

        group = cmds.createNode(
            "transform",
            name=grp,
            parent=parent
        )

        return group

    # =========================================================================
    # Legacy Rig Group Presets
    # =========================================================================

    @staticmethod
    def create_rig_grp():
        u"""创建早期项目使用的基础 Rig Group。"""
        top_main_group = "grp_m_group_001"
        child_groups = [
            "grp_m_bpjnt_001",
            "grp_m_control_001",
            "grp_m_jnt_001",
            "grp_m_mesh_001",
            "grp_m_node_001",
        ]

        # 创建或复用旧版 Rig 顶层 Group。
        Hierarchy.create_grp(
            top_main_group
        )

        # 创建旧版 Blueprint / Control / Joint / Mesh / Node 子组。
        for group in child_groups:
            Hierarchy.create_grp(
                group,
                parent=top_main_group
            )

        return (
            child_groups[0],
            child_groups[1],
            child_groups[2],
            child_groups[3],
            child_groups[4],
            top_main_group,
        )

    @staticmethod
    def create_default_grp():
        u"""
        创建早期默认 Rig Group 结构。

        完整 Controller / Rig Build 应使用 systems.controller 或具体 Body Rig System。
        """
        # 创建旧版默认顶层和 Geometry / Control / Custom 三个主要分区。
        group = Hierarchy.create_grp("Group")
        geometry = Hierarchy.create_grp(
            "Geometry",
            parent=group
        )
        control = Hierarchy.create_grp(
            "Control",
            parent=group
        )
        custom = Hierarchy.create_grp(
            "Custom",
            parent=group
        )

        # 创建 Rig Node / Joint 子结构。
        rig_nodes = Hierarchy.create_grp(
            "RigNodes",
            parent=custom
        )
        joints = Hierarchy.create_grp(
            "Joints",
            parent=custom
        )
        rig_nodes_local = Hierarchy.create_grp(
            "RigNodesLocal",
            parent=rig_nodes
        )
        rig_nodes_world = Hierarchy.create_grp(
            "RigNodesWorld",
            parent=rig_nodes
        )
        ncloth_geometry_group = Hierarchy.create_grp(
            "nCloth_geo_grp",
            parent=custom
        )

        # 创建旧版 Low / Mid / High Model 分组。
        Hierarchy.create_grp(
            "grp_m_low_Modle_001",
            parent=geometry
        )
        Hierarchy.create_grp(
            "grp_m_mid_Modle_001",
            parent=geometry
        )
        Hierarchy.create_grp(
            "grp_m_high_Modle_001",
            parent=geometry
        )

        return {
            "Geometry": geometry,
            "Control": control,
            "RigNodes": rig_nodes,
            "Joints": joints,
            "RigNodes_Local": rig_nodes_local,
            "RigNodes_World": rig_nodes_world,
            "nCloth_geo_grp": ncloth_geometry_group,
        }

    # =========================================================================
    # Legacy Controller Hierarchy
    # =========================================================================

    @staticmethod
    def control_hierarchy():
        u"""
        兼容早期 Selection 驱动的 Controller 打组入口。

        新代码应使用 systems.controller Builder。
        """
        controls = cmds.ls(
            selection=True,
            long=True
        ) or []

        results = []

        for control in controls:
            # 使用统一 Rename Core 获取 Controller Short Name。
            short_name = rename_utils.get_short_name(
                control
            )

            if not short_name.startswith("ctrl_"):
                cmds.warning(
                    u"跳过非标准 Controller：{}".format(control)
                )
                continue

            zero_name = short_name.replace(
                "ctrl_",
                "zero_",
                1
            )
            driven_name = short_name.replace(
                "ctrl_",
                "driven_",
                1
            )
            connect_name = short_name.replace(
                "ctrl_",
                "connect_",
                1
            )
            offset_name = short_name.replace(
                "ctrl_",
                "offset_",
                1
            )

            zero = cmds.createNode(
                "transform",
                name=zero_name
            )
            driven = cmds.createNode(
                "transform",
                name=driven_name,
                parent=zero
            )
            connect = cmds.createNode(
                "transform",
                name=connect_name,
                parent=driven
            )
            offset = cmds.createNode(
                "transform",
                name=offset_name,
                parent=connect
            )

            cmds.matchTransform(
                zero,
                control,
                position=True,
                rotation=True
            )

            # 使用统一 Hierarchy API 把 Controller 放入新建 Offset Group。
            final_control = Hierarchy.parent(
                control,
                offset
            )

            results.append({
                "zero": zero,
                "driven": driven,
                "connect": connect,
                "offset": offset,
                "control": final_control,
            })

        return results


__all__ = [
    "Hierarchy",
]
