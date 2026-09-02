# coding=utf-8
u"""
Joint Chain Utils
=================

Maya 多 Joint / Joint Chain 的通用底层算法。

模块职责
--------
- 验证一组 Joint；
- 查询一个 Start Joint 到 Descendant Joint 的有序路径；
- 按明确输入顺序组成 Joint Chain；
- 根据一组 Maya Item 的世界位置创建 Joint；
- 根据 Curve CV 世界位置创建 Joint Chain。

模块边界
--------
    单个 Joint 属性 / 创建      -> joint_utils
    DAG Parent / Group          -> hierarchy_utils
    Curve 查询                  -> curve_utils
    Transform 世界数据          -> transform_utils
    Component 世界位置          -> snap_utils
    Selection / Warning / UI    -> tools
    Face / Body Rig 业务        -> systems

设计原则
--------
1. 不读取当前 Maya Selection；调用者必须传入明确的数据；
2. 不维护第二套单 Joint 创建逻辑，全部复用 joint_utils.Joint.create()；
3. 不维护第二套 Curve 查询逻辑，全部复用 curve_utils；
4. 不建立 JointChain / JointCurve 包装类，使用明确的模块函数；
5. 场景修改循环保持展开，方便 Maya Script Editor 调试。
"""

from __future__ import print_function

import re

from . import curve_utils
from . import hierarchy_utils
from . import joint_utils
from . import rename_utils
from . import scene_utils
from . import snap_utils
from . import transform_utils


# =============================================================================
# Validate
# =============================================================================

def validate_joint_list(joints):
    u"""
    验证并返回一份独立的 Joint 列表。

    Args:
        joints (str | list[str]):
            需要批量处理的 Maya Joint 节点或 Joint Chain。

    Returns:
        object:
            方法执行后的结果数据。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    if joints is None:
        joints = []

    if isinstance(joints, str):
        joints = [
            joints
        ]

    if not joints:
        raise RuntimeError(
            u"Joint 列表不能为空。"
        )

    result = []

    for joint in joints:
        joint_utils.Joint(
            joint
        )
        result.append(
            joint
        )

    return result


# =============================================================================
# Chain Query / Edit
# =============================================================================

def get_joint_path(start_joint, end_joint):
    u"""
    返回 Start Joint 到指定 Descendant Joint 的有序路径；不连通时返回 None。

    Args:
        start_joint (str):
            当前 Rig 计算或构建使用的 Maya Joint 节点。
        end_joint (str):
            当前 Rig 计算或构建使用的 Maya Joint 节点。

    Returns:
        object | list | None:
            方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # Step 01：执行当前阶段的核心处理
    # -------------------------------------------------------------------------
    joint_utils.Joint(
        start_joint
    )
    # -------------------------------------------------------------------------
    # Step 02：执行当前阶段的核心处理
    # -------------------------------------------------------------------------
    joint_utils.Joint(
        end_joint
    )

    start_joint = scene_utils.get_long_name(
        start_joint
    )
    # -------------------------------------------------------------------------
    # Step 03：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    end_joint = scene_utils.get_long_name(
        end_joint
    )

    if start_joint == end_joint:
        return [
            start_joint
        ]

    # -------------------------------------------------------------------------
    # Step 04：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    def walk(current_joint, current_path):
        children = hierarchy_utils.get_children(
            current_joint,
            node_type="joint",
            full_path=True
        )

        for child_joint in children:
            child_path = []

            for path_joint in current_path:
                child_path.append(
                    path_joint
                )

            child_path.append(
                child_joint
            )

            if child_joint == end_joint:
                return child_path

            result = walk(
                child_joint,
                child_path
            )

            if result:
                return result

        return None

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return walk(
        start_joint,
        [start_joint]
    )


def parent_joints_as_chain(joints):
    u"""
    按照输入顺序把 Joint 组成父子链，并返回原顺序 Joint 列表。

    Args:
        joints (str | list[str]):
            需要批量处理的 Maya Joint 节点或 Joint Chain。

    Returns:
        object:
            方法执行后的结果数据。
    """
    joints = validate_joint_list(
        joints
    )

    if len(joints) <= 1:
        return joints

    joint_index = len(joints) - 1

    while joint_index > 0:
        hierarchy_utils.parent(
            joints[joint_index],
            joints[joint_index - 1]
        )
        joint_index -= 1

    return joints


def create_joints_at_items(
        items,
        name_prefix="jnt_snap",
        parent_chain=False,
        radius=None
):
    u"""
    在明确给定的一组 Maya Object / Component 世界位置创建 Joint。

    Component 只提供位置；Transform / Joint 同时复制世界位置和旋转。

    Args:
        items (object):
            当前方法执行 Maya / Rig 操作时使用的 `items` 数据。
        name_prefix (str):
            批量创建 Joint 时写入节点名称前部的 Prefix。
        parent_chain (bool):
            创建多个 Joint 时是否按输入顺序建立父子 Joint Chain。
        radius (float):
            创建节点或控制器使用的半径值。

    Returns:
        object:
            方法执行后的结果数据。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if items is None:
        items = []

    if isinstance(items, str):
        items = [
            items
        ]

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not items:
        raise RuntimeError(
            u"没有给定用于创建 Joint 的 Maya Item。"
        )

    joints = []
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    current_parent = None
    item_index = 0

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    while item_index < len(items):
        item = items[item_index]
        joint_name = "{}_{:03d}".format(
            name_prefix,
            item_index + 1
        )

        if snap_utils.is_component(
                item
        ):
            position = snap_utils.get_item_world_position(
                item
            )

            if position is None:
                raise RuntimeError(
                    u"无法获取组件世界位置：{}".format(
                        item
                    )
                )

            joint = joint_utils.Joint.create(
                name=joint_name,
                position=position,
                parent=current_parent,
                radius=radius
            )
        else:
            transform_utils.validate_transform(
                item
            )
            position = transform_utils.get_world_translation(
                item
            )
            rotation = transform_utils.get_world_rotation(
                item
            )
            joint = joint_utils.Joint.create(
                name=joint_name,
                position=position,
                rotation=rotation,
                parent=current_parent,
                radius=radius
            )

        joints.append(
            joint
        )

        if parent_chain:
            current_parent = joint

        item_index += 1

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return joints


# =============================================================================
# Curve -> Joint
# =============================================================================

def get_curve_joint_base_name(curve):
    u"""
    根据 Curve Transform Short Name 生成默认 Joint Base Name。

    Args:
        curve (str):
            需要处理的 Maya Curve Transform 或 Shape 名称。

    Returns:
        object:
            方法执行后的结果数据。
    """
    curve_transform = curve_utils.get_curve_transform(
        curve
    )
    short_name = rename_utils.get_short_name(
        curve_transform
    )

    if short_name.startswith("crv_"):
        base_name = short_name.replace(
            "crv_",
            "jnt_",
            1
        )
    else:
        base_name = "jnt_{}".format(
            short_name
        )

    return re.sub(
        r"_\d{3}$",
        "",
        base_name
    )


def create_joints_on_curve_cvs(
        curve,
        joint_base_name=None,
        parent_chain=True,
        create_group=True,
        group_name=None,
        radius=None
):
    u"""
    根据 Curve CV 世界位置创建 Joint，并可按顺序组成 Chain。

    Args:
        curve (str):
            需要处理的 Maya Curve Transform 或 Shape 名称。
        joint_base_name (str):
            `joint_base_name` 对应的 Maya 节点或资源名称。
        parent_chain (bool):
            创建多个 Joint 时是否按输入顺序建立父子 Joint Chain。
        create_group (bool):
            当前 Rig / Guide / Controller 层级中的 Maya Group Transform。
        group_name (str):
            `group_name` 对应的 Maya 节点或资源名称。
        radius (float):
            创建节点或控制器使用的半径值。

    Returns:
        dict:
            方法执行后的结果数据。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    curve_transform = curve_utils.get_curve_transform(
        curve
    )
    positions = curve_utils.get_curve_cv_positions(
        curve,
        world_space=True
    )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not positions:
        raise RuntimeError(
            u"Curve 没有找到 CV：{}".format(
                curve
            )
        )

    if joint_base_name is None:
        joint_base_name = get_curve_joint_base_name(
            curve
        )

    joint_group = None

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if create_group:
        if group_name is None:
            group_base_name = joint_base_name

            if group_base_name.startswith("jnt_"):
                group_base_name = group_base_name.replace(
                    "jnt_",
                    "grp_",
                    1
                )

            group_name = "{}_joints".format(
                group_base_name
            )

        scene_utils.ensure_nodes_available(
            group_name,
            label=u"Joint Group"
        )
        joint_group = scene_utils.create_node(
            "transform",
            group_name
        )

    joints = []
    current_parent = joint_group
    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    position_index = 0

    while position_index < len(positions):
        joint_name = "{}_{:03d}".format(
            joint_base_name,
            position_index + 1
        )

        parent_node = joint_group

        if parent_chain:
            parent_node = current_parent

        joint = joint_utils.Joint.create(
            name=joint_name,
            position=positions[position_index],
            parent=parent_node,
            radius=radius
        )
        joints.append(
            joint
        )

        if parent_chain:
            current_parent = joint

        position_index += 1

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return {
        "curve": curve_transform,
        "jnt_list": joints,
        "jnt_grp": joint_group,
    }


__all__ = [
    "validate_joint_list",
    "get_joint_path",
    "parent_joints_as_chain",
    "create_joints_at_items",
    "get_curve_joint_base_name",
    "create_joints_on_curve_cvs",
]
