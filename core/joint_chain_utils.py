# coding=utf-8
u"""
Joint Chain Utils
=================

Maya 多 Joint / Joint Chain 的通用底层算法。

模块职责：
    1. 验证明确传入的一组 Joint；
    2. 查询 Start Joint 到指定 Descendant Joint 的有序路径；
    3. 按调用方给定顺序建立 Joint Parent Chain；
    4. 根据 Maya Object / Component 世界位置批量创建 Joint；
    5. 根据 Curve CV 世界位置创建 Joint Chain。

模块边界：
    单个 Joint 属性 / 创建      -> joint_utils
    DAG Parent / Group          -> hierarchy_utils
    Curve 查询                  -> curve_utils
    Transform 世界数据          -> transform_utils
    Component 世界位置          -> snap_utils
    Scene Node 创建 / 占用检查   -> scene_utils
    Selection / Warning / UI    -> tools
    Face / Body Rig 业务        -> systems

设计原则：
    1. 不读取当前 Maya Selection；调用者必须传入明确数据；
    2. 不维护第二套单 Joint 创建逻辑，统一复用 ``joint_utils.Joint.create()``；
    3. 不维护第二套 Curve 查询逻辑，统一复用 ``curve_utils``；
    4. 不建立额外 JointChain 包装类，使用清晰的模块函数；
    5. 场景修改循环保持展开，方便在 Maya Script Editor 中逐步调试。
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
    验证输入 Joint，并返回一份独立列表。

    输入可以是单个 Joint 名称或 Joint 列表。每一个元素都会通过
    ``joint_utils.Joint`` 做真实 Maya Joint 类型检查。

    Args:
        joints (str | list[str]):
            需要验证的单个 Joint 或 Joint 列表。

    Returns:
        list[str]:
        保持调用方原有顺序的独立 Joint 列表。

    Raises:
        RuntimeError:
        输入为空，或任意节点不存在 / 不是 Maya Joint 时抛出。
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
    查询 Start Joint 到指定 Descendant Joint 的有序 Joint Path。

    该函数只沿 ``start_joint`` 的 Child Joint 向下查找，因此不会跨到 Parent、
    Sibling 或另一条 Skeleton Branch。Start 与 End 不连通时返回 None。

    Args:
        start_joint (str):
            路径查询起点 Joint。
        end_joint (str):
            必须位于 Start Joint 子层级中的目标 Joint。

    Returns:
        list[str] | None:
        从 Start 到 End 的 Long DAG Path 列表；不连通时返回 None。

    Raises:
        RuntimeError:
        Start / End 节点不存在或不是 Maya Joint 时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：验证 Start / End 都是真实 Maya Joint，尽早阻止无效节点进入递归
    # -------------------------------------------------------------------------
    joint_utils.Joint(
        start_joint
    )
    joint_utils.Joint(
        end_joint
    )

    # -------------------------------------------------------------------------
    # Step 02：统一转换成唯一 Long DAG Path，避免场景重名 Joint 产生歧义
    # -------------------------------------------------------------------------
    start_joint = scene_utils.get_long_name(
        start_joint
    )
    end_joint = scene_utils.get_long_name(
        end_joint
    )

    # -------------------------------------------------------------------------
    # Step 03：Start 与 End 相同属于长度为 1 的有效 Joint Path
    # -------------------------------------------------------------------------
    if start_joint == end_joint:
        return [
            start_joint
        ]

    # -------------------------------------------------------------------------
    # Step 04：从 Start 开始深度优先遍历 Child Joint，并持续复制当前有序路径
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
    # Step 05：返回第一条命中 End Joint 的路径；所有 Branch 都未命中则返回 None
    # -------------------------------------------------------------------------
    return walk(
        start_joint,
        [start_joint]
    )


def parent_joints_as_chain(joints):
    u"""
    按输入顺序把多个 Joint 建立为连续父子链。

    例如 ``[A, B, C]`` 最终建立 ``A → B → C``。函数只处理 Parent 关系，
    不重新计算 Joint Orient，也不修改世界 Transform。

    Args:
        joints (str | list[str]):
            按目标父子顺序排列的 Joint。

    Returns:
        list[str]:
        验证后的原顺序 Joint 列表。

    Raises:
        RuntimeError:
        任意节点不存在或不是 Maya Joint 时抛出。
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
    在一组明确 Maya Object / Component 的世界位置创建 Joint。

    Component 只提供世界位置；Transform / Joint 同时复制世界 Translation 和
    Rotation。``parent_chain=True`` 时，新 Joint 会按输入顺序直接串成 Chain。

    Args:
        items (str | list[str]):
            需要作为 Joint 位置参考的 Maya Object / Component。
        name_prefix (str):
            新 Joint 的基础名称，例如 ``jnt_snap``；最终追加三位序号。
        parent_chain (bool):
            是否让后一个新 Joint Parent 到前一个新 Joint 下。
        radius (float | None):
            可选 Joint Radius；None 时使用 ``Joint.create`` 默认值。

    Returns:
        list[str]:
        按创建顺序返回的新 Joint 列表。

    Raises:
        RuntimeError:
        输入为空、Component 无法取得位置或 Transform 无效时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：把单个 Item 统一转换成列表，并拒绝空输入
    # -------------------------------------------------------------------------
    if items is None:
        items = []

    if isinstance(items, str):
        items = [
            items
        ]

    if not items:
        raise RuntimeError(
            u"没有给定用于创建 Joint 的 Maya Item。"
        )

    # -------------------------------------------------------------------------
    # Step 02：初始化 Build Result；Chain 模式用 current_parent 记录上一节 Joint
    # -------------------------------------------------------------------------
    joints = []
    current_parent = None
    item_index = 0

    # -------------------------------------------------------------------------
    # Step 03：按输入顺序逐项取得世界 Transform，并创建对应编号 Joint
    # -------------------------------------------------------------------------
    while item_index < len(items):
        item = items[item_index]
        joint_name = "{}_{:03d}".format(
            name_prefix,
            item_index + 1
        )

        # Component 没有稳定的 Transform Rotation，因此只复制位置。
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
            # 普通 Transform / Joint 同时复制世界位置和世界旋转。
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

        # ---------------------------------------------------------------------
        # Step 04：Chain 模式把当前 Joint 保存为下一节 Joint 的 Parent
        # ---------------------------------------------------------------------
        if parent_chain:
            current_parent = joint

        item_index += 1

    # -------------------------------------------------------------------------
    # Step 05：返回与输入 Item 顺序一致的新 Joint 列表
    # -------------------------------------------------------------------------
    return joints


# =============================================================================
# Curve -> Joint
# =============================================================================

def get_curve_joint_base_name(curve):
    u"""
    根据 Curve Transform Short Name 生成默认 Joint Base Name。

    ``crv_lf_brow_001`` 会得到 ``jnt_lf_brow``；非 ``crv_`` 前缀的 Curve
    则直接在 Short Name 前增加 ``jnt_``。

    Args:
        curve (str):
            Maya NURBS Curve Transform 或 Shape。

    Returns:
        str:
        去掉末尾三位序号后的默认 Joint Base Name。

    Raises:
        RuntimeError:
        输入不是有效 Curve 时由 ``curve_utils`` 抛出。
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
    根据 Curve 全部 CV 的世界位置创建 Joint。

    每一个 CV 对应一个 Joint。默认情况下新 Joint 会按 CV 顺序组成 Chain，
    并放到一个自动创建的 Joint Group 下。该函数只依据 CV Position 建 Joint，
    不负责 Joint Orient、Skin 或 Controller Build。

    Args:
        curve (str):
            Maya NURBS Curve Transform 或 Shape。
        joint_base_name (str | None):
            Joint 基础名称；None 时由 Curve Name 自动生成。
        parent_chain (bool):
            是否按 CV 顺序建立连续 Joint Chain。
        create_group (bool):
            是否为本次 Joint Build 创建独立 Group。
        group_name (str | None):
            自定义 Joint Group 名称；None 时从 Joint Base Name 推导。
        radius (float | None):
            可选 Joint Radius；None 时使用 ``Joint.create`` 默认值。

    Returns:
        dict:
        包含 ``curve``、``jnt_list``、``jnt_grp`` 的 Build Result。

    Raises:
        RuntimeError:
        Curve 无效、没有 CV、Group 名称被占用或 Joint 创建失败时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：解析 Curve Transform，并一次取得全部 CV 世界位置
    # -------------------------------------------------------------------------
    curve_transform = curve_utils.get_curve_transform(
        curve
    )
    positions = curve_utils.get_curve_cv_positions(
        curve,
        world_space=True
    )

    if not positions:
        raise RuntimeError(
            u"Curve 没有找到 CV：{}".format(
                curve
            )
        )

    # -------------------------------------------------------------------------
    # Step 02：确定 Joint Base Name，并根据参数准备可选的 Joint Group
    # -------------------------------------------------------------------------
    if joint_base_name is None:
        joint_base_name = get_curve_joint_base_name(
            curve
        )

    joint_group = None

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

        # ---------------------------------------------------------------------
        # Step 03：创建 Group 前先做 Scene Name Occupancy 检查，避免 Maya 自动改名
        # ---------------------------------------------------------------------
        scene_utils.ensure_nodes_available(
            group_name,
            label=u"Joint Group"
        )
        joint_group = scene_utils.create_node(
            "transform",
            group_name
        )

    # -------------------------------------------------------------------------
    # Step 04：按 CV 顺序逐个创建 Joint，并根据 parent_chain 更新 Parent
    # -------------------------------------------------------------------------
    joints = []
    current_parent = joint_group
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
    # Step 05：返回 Curve、Joint List 和 Joint Group，供上层 Rig System 继续使用
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
