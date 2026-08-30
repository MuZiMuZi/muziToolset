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

Hierarchy.create_rig_grp()
    创建早期 Rig 顶层组命名结构。保留用于兼容旧场景。

Hierarchy.create_default_grp()
    创建早期默认 Rig Group 结构。旧版曾同时创建 Controller，职责越界且依赖已删除的 controlUtils；
    当前版本只创建层级组并返回结果，完整 Controller 构建应使用 systems.controller。

Hierarchy.control_hierarchy()
    兼容早期 Controller 层级创建入口。新代码应使用 systems.controller Builder。

设计原则
--------
1. Core 只负责 DAG 层级，不 import Controller / Face / Body System；
2. 插入额外 Group 时必须保持原对象世界 Transform；
3. Generic Query 不读取 UI，只有明确标为 Legacy Compatibility 的方法允许使用 Selection；
4. 已迁移到 systems.controller 的完整 Rig Workflow 不再继续扩张到本模块；
5. 模块文件名与所有正式 Import 统一使用 snake_case。
"""

from __future__ import print_function

import maya.cmds as cmds


class Hierarchy(object):
    """Maya DAG 层级操作兼容类。"""

    # =========================================================================
    # Validate / Parent
    # =========================================================================

    @staticmethod
    def _validate_node(node, label=u"节点"):
        """检查 Maya DAG 节点是否存在。"""
        if not node:
            raise RuntimeError(
                u"{}不能为空。".format(label)
            )

        if not cmds.objExists(node):
            raise RuntimeError(
                u"{}不存在：{}".format(
                    label,
                    node
                )
            )

        return True

    @staticmethod
    def parent(child_node, parent_node):
        u"""
        确保 child_node 位于 parent_node 下。

        Args:
            child_node (object):
                `child_node` 对应的输入数据。
            parent_node (object):
                `parent_node` 对应的输入数据。

        Returns:
            str:
            Parent 后 Maya 返回的 Child Path；如果已经是正确父子关系则返回原节点。
        """
        # ---------------------------------------------------------------------
        # 步骤 1：验证 Child / Parent。
        # ---------------------------------------------------------------------
        Hierarchy._validate_node(
            child_node,
            label=u"子节点"
        )
        Hierarchy._validate_node(
            parent_node,
            label=u"父节点"
        )

        # ---------------------------------------------------------------------
        # 步骤 2：查询当前 Parent，避免重复 parent 导致无意义 DAG 路径变化。
        # ---------------------------------------------------------------------
        parent_original = cmds.listRelatives(
            child_node,
            parent=True,
            fullPath=True
        ) or []

        parent_matches = cmds.ls(
            parent_node,
            long=True
        ) or []

        parent_long_name = parent_node

        if parent_matches:
            parent_long_name = parent_matches[0]

        if parent_original and parent_original[0] == parent_long_name:
            return child_node

        # ---------------------------------------------------------------------
        # 步骤 3：建立父子关系，并使用 Maya 返回值更新最终路径。
        # ---------------------------------------------------------------------
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
        在对象上方插入一个额外 Transform Group。

        Args:
            obj (str):
                需要插入额外组的对象。
            grp_name (str):
                新 Group 名称。
            world_orient (bool):
                False：Group 旋转与对象当前世界旋转一致； True：Group 使用世界零旋转。

        Returns:
            str: 新 Group。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。

        Notes:
            插组前先记录对象原 Parent 和世界 Transform，再插入 Group，确保对象视觉姿态不跳动。
        """
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

        # ---------------------------------------------------------------------
        # 步骤 1：记录目标对象世界位置 / 旋转 / 缩放以及原 Parent。
        # ---------------------------------------------------------------------
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
        original_parent = cmds.listRelatives(
            obj,
            parent=True,
            fullPath=True
        ) or []

        if world_orient:
            rotation = [0.0, 0.0, 0.0]

        # ---------------------------------------------------------------------
        # 步骤 2：创建 Group 并对齐到目标对象。
        # ---------------------------------------------------------------------
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

        # ---------------------------------------------------------------------
        # 步骤 3：先把新 Group 放回原 Parent，再把目标对象放进 Group。
        # 这样不会丢失原来的 DAG 结构。
        # ---------------------------------------------------------------------
        if original_parent:
            parent_result = cmds.parent(
                object_group,
                original_parent[0],
                absolute=True
            )

            if parent_result:
                object_group = parent_result[0]

        cmds.parent(
            obj,
            object_group,
            absolute=True
        )

        return object_group

    # =========================================================================
    # Hierarchy Query
    # =========================================================================

    @staticmethod
    def get_child_object(object, type="joint"):
        u"""
        获取指定类型的全部后代，并把根对象放在列表第一位。

        Args:
            object (str):
                根对象。
            type (str):
                Maya Node Type，例如 joint / transform。

        Returns:
            object:
            方法执行后的结果数据。
        """
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

        # Maya listRelatives(allDescendents=True) 的顺序通常从更深层开始。
        # 这里反转后让结果更接近“根 -> 子 -> 孙”的阅读顺序。
        descendants.reverse()

        result = [object]

        for descendant in descendants:
            result.append(descendant)

        return result

    @staticmethod
    def select_sub_objects(obj_type="transform"):
        u"""
        兼容旧工具：选择当前 Selection 下指定类型的全部后代。

        新 Core 逻辑不应依赖 Selection；新 Tool 可以自行读取 Selection 后调用 get_child_object。

        Args:
            obj_type (str):
                `obj_type` 对应的名称、标记或字符串参数。

        Returns:
            object:
            方法执行后的结果数据。
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
        u"""
        创建一个 Transform Group；已存在时直接返回现有节点。

        Args:
            grp (object):
                `grp` 对应的输入数据。
            parent (str):
                父级 Maya 节点名称。

        Returns:
            str: Group 名称 / Path。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if not grp:
            raise RuntimeError(u"Group 名称不能为空。")

        if cmds.objExists(grp):
            return grp

        if parent:
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
        u"""
        创建早期项目使用的基础 Rig Group。

        Returns:
            tuple:
            方法执行后的结果数据。

        Notes:
            这些名称属于旧场景兼容命名（m），新系统应使用项目当前 md / lf / rt 命名规范。
        """
        top_main_group = "grp_m_group_001"
        child_groups = [
            "grp_m_bpjnt_001",
            "grp_m_control_001",
            "grp_m_jnt_001",
            "grp_m_mesh_001",
            "grp_m_node_001",
        ]

        Hierarchy.create_grp(
            top_main_group
        )

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

        旧实现同时创建 Character / World / COG Controller，并依赖已经退出正式 Core 的 controlUtils，
        因此该函数曾处于“调用即 NameError”的坏状态。
        当前版本只做它名字真正表达的职责：创建默认 Group。完整 Controller / Rig Build 请使用
        ``systems.controller`` 或具体 Body Rig System。

        Returns:
            dict:
            方法执行后的结果数据。
        """
        # ---------------------------------------------------------------------
        # 步骤 1：创建顶层结构。
        # ---------------------------------------------------------------------
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

        # ---------------------------------------------------------------------
        # 步骤 2：创建 Rig Node / Joint 子结构。
        # ---------------------------------------------------------------------
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

        # ---------------------------------------------------------------------
        # 步骤 3：创建旧版 Low / Mid / High Model 分组。
        # ---------------------------------------------------------------------
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

        新代码应使用 systems.controller Builder。本方法只保留基础 Zero / Driven / Connect / Offset
        层级创建，不再复制 Sub Controller、颜色、Visibility 等完整 Controller System 职责。

        Returns:
            list(dict): 每个选中 Controller 对应的层级节点。
        """
        controls = cmds.ls(
            selection=True,
            long=True
        ) or []

        results = []

        for control in controls:
            short_name = control.split("|")[-1]

            if not short_name.startswith("ctrl_"):
                cmds.warning(
                    u"跳过非标准 Controller：{}".format(control)
                )
                continue

            # -----------------------------------------------------------------
            # 步骤 1：创建标准上层组。
            # -----------------------------------------------------------------
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

            # -----------------------------------------------------------------
            # 步骤 2：Zero 对齐 Controller，再把 Controller 放进 Offset。
            # -----------------------------------------------------------------
            cmds.matchTransform(
                zero,
                control,
                position=True,
                rotation=True
            )
            parent_result = cmds.parent(
                control,
                offset,
                absolute=True
            )

            final_control = control

            if parent_result:
                final_control = parent_result[0]

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
