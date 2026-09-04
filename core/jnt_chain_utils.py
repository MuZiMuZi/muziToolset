# coding=utf-8
u"""
jnt Chain Utils
=================

Maya 多 jnt / jnt Chain 的通用底层算法。

模块职责：
    1. 验证明确传入的一组 jnt；
    2. 查询 Start jnt 到指定 Descendant jnt 的有序路径；
    3. 按调用方给定顺序建立 jnt Parent Chain；
    4. 根据 Maya Object / Component 世界位置批量创建 jnt；
    5. 根据 Curve CV 世界位置创建 jnt Chain。

模块边界：
    单个 jnt 属性 / 创建      -> jnt_utils
    DAG Parent / Group          -> hierarchy_utils
    Curve 查询                  -> curve_utils
    Transform 世界数据          -> transform_utils
    Component 世界位置          -> snap_utils
    Scene Node 创建 / 占用检查   -> scene_utils
    Selection / Warning / UI    -> tools
    Face / Body Rig 业务        -> systems

设计原则：
    1. 不读取当前 Maya Selection；调用者必须传入明确数据；
    2. 不维护第二套单 jnt 创建逻辑，统一复用 ``jnt_utils.jnt.create()``；
    3. 不维护第二套 Curve 查询逻辑，统一复用 ``curve_utils``；
    4. 不建立额外 jntChain 包装类，使用清晰的模块函数；
    5. 场景修改循环保持展开，方便在 Maya Script Editor 中逐步调试。
"""

from __future__ import print_function

import re

from . import curve_utils
from . import hierarchy_utils
from . import jnt_utils
from . import rename_utils
from . import scene_utils
from . import snap_utils
from . import transform_utils


# =============================================================================
# Validate
# =============================================================================

def validate_jnt_list(jnts):
    u"""
    验证输入 jnt，并返回一份独立列表。

    输入可以是单个 jnt 名称或 jnt 列表。每一个元素都会通过
    ``jnt_utils.jnt`` 做真实 Maya jnt 类型检查。

    Args:
        jnts (str | list[str]):
            需要验证的单个 jnt 或 jnt 列表。

    Returns:
        list[str]:
        保持调用方原有顺序的独立 jnt 列表。

    Raises:
        RuntimeError:
        输入为空，或任意节点不存在 / 不是 Maya jnt 时抛出。
    """
    if jnts is None:
        jnts = []

    if isinstance(jnts, str):
        jnts = [
            jnts
        ]

    if not jnts:
        raise RuntimeError(
            u"jnt 列表不能为空。"
        )

    result = []

    for jnt in jnts:
        jnt_utils.jnt(
            jnt
        )
        result.append(
            jnt
        )

    return result


# =============================================================================
# Chain Query / Edit
# =============================================================================

def get_jnt_path(start_jnt, end_jnt):
    u"""
    查询 Start jnt 到指定 Descendant jnt 的有序 jnt Path。

    该函数只沿 ``start_jnt`` 的 Child jnt 向下查找，因此不会跨到 Parent、
    Sibling 或另一条 Skeleton Branch。Start 与 End 不连通时返回 None。

    Args:
        start_jnt (str):
            路径查询起点 jnt。
        end_jnt (str):
            必须位于 Start jnt 子层级中的目标 jnt。

    Returns:
        list[str] | None:
        从 Start 到 End 的 Long DAG Path 列表；不连通时返回 None。

    Raises:
        RuntimeError:
        Start / End 节点不存在或不是 Maya jnt 时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：验证 Start / End 都是真实 Maya jnt，尽早阻止无效节点进入递归
    # -------------------------------------------------------------------------
    jnt_utils.jnt(
        start_jnt
    )
    jnt_utils.jnt(
        end_jnt
    )

    # -------------------------------------------------------------------------
    # Step 02：统一转换成唯一 Long DAG Path，避免场景重名 jnt 产生歧义
    # -------------------------------------------------------------------------
    start_jnt = scene_utils.get_long_name(
        start_jnt
    )
    end_jnt = scene_utils.get_long_name(
        end_jnt
    )

    # -------------------------------------------------------------------------
    # Step 03：Start 与 End 相同属于长度为 1 的有效 jnt Path
    # -------------------------------------------------------------------------
    if start_jnt == end_jnt:
        return [
            start_jnt
        ]

    # -------------------------------------------------------------------------
    # Step 04：从 Start 开始深度优先遍历 Child jnt，并持续复制当前有序路径
    # -------------------------------------------------------------------------
    def walk(current_jnt, current_path):
        children = hierarchy_utils.get_children(
            current_jnt,
            node_type="jnt",
            full_path=True
        )

        for child_jnt in children:
            child_path = []

            for path_jnt in current_path:
                child_path.append(
                    path_jnt
                )

            child_path.append(
                child_jnt
            )

            if child_jnt == end_jnt:
                return child_path

            result = walk(
                child_jnt,
                child_path
            )

            if result:
                return result

        return None

    # -------------------------------------------------------------------------
    # Step 05：返回第一条命中 End jnt 的路径；所有 Branch 都未命中则返回 None
    # -------------------------------------------------------------------------
    return walk(
        start_jnt,
        [start_jnt]
    )


def parent_jnts_as_chain(jnts):
    u"""
    按输入顺序把多个 jnt 建立为连续父子链。

    例如 ``[A, B, C]`` 最终建立 ``A → B → C``。函数只处理 Parent 关系，
    不重新计算 jnt Orient，也不修改世界 Transform。

    Args:
        jnts (str | list[str]):
            按目标父子顺序排列的 jnt。

    Returns:
        list[str]:
        验证后的原顺序 jnt 列表。

    Raises:
        RuntimeError:
        任意节点不存在或不是 Maya jnt 时抛出。
    """
    jnts = validate_jnt_list(
        jnts
    )

    if len(jnts) <= 1:
        return jnts

    jnt_index = len(jnts) - 1

    while jnt_index > 0:
        hierarchy_utils.parent(
            jnts[jnt_index],
            jnts[jnt_index - 1]
        )
        jnt_index -= 1

    return jnts


def create_jnts_at_items(
        items,
        name_prefix="jnt_snap",
        parent_chain=False,
        radius=None
):
    u"""
    在一组明确 Maya Object / Component 的世界位置创建 jnt。

    Component 只提供世界位置；Transform / jnt 同时复制世界 Translation 和
    Rotation。``parent_chain=True`` 时，新 jnt 会按输入顺序直接串成 Chain。

    Args:
        items (str | list[str]):
            需要作为 jnt 位置参考的 Maya Object / Component。
        name_prefix (str):
            新 jnt 的基础名称，例如 ``jnt_snap``；最终追加三位序号。
        parent_chain (bool):
            是否让后一个新 jnt Parent 到前一个新 jnt 下。
        radius (float | None):
            可选 jnt Radius；None 时使用 ``jnt.create`` 默认值。

    Returns:
        list[str]:
        按创建顺序返回的新 jnt 列表。

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
            u"没有给定用于创建 jnt 的 Maya Item。"
        )

    # -------------------------------------------------------------------------
    # Step 02：初始化 Build Result；Chain 模式用 current_parent 记录上一节 jnt
    # -------------------------------------------------------------------------
    jnts = []
    current_parent = None
    item_index = 0

    # -------------------------------------------------------------------------
    # Step 03：按输入顺序逐项取得世界 Transform，并创建对应编号 jnt
    # -------------------------------------------------------------------------
    while item_index < len(items):
        item = items[item_index]
        jnt_name = "{}_{:03d}".format(
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

            jnt = jnt_utils.jnt.create(
                name=jnt_name,
                position=position,
                parent=current_parent,
                radius=radius
            )
        else:
            # 普通 Transform / jnt 同时复制世界位置和世界旋转。
            transform_utils.validate_transform(
                item
            )
            position = transform_utils.get_world_translation(
                item
            )
            rotation = transform_utils.get_world_rotation(
                item
            )
            jnt = jnt_utils.jnt.create(
                name=jnt_name,
                position=position,
                rotation=rotation,
                parent=current_parent,
                radius=radius
            )

        jnts.append(
            jnt
        )

        # ---------------------------------------------------------------------
        # Step 04：Chain 模式把当前 jnt 保存为下一节 jnt 的 Parent
        # ---------------------------------------------------------------------
        if parent_chain:
            current_parent = jnt

        item_index += 1

    # -------------------------------------------------------------------------
    # Step 05：返回与输入 Item 顺序一致的新 jnt 列表
    # -------------------------------------------------------------------------
    return jnts


# =============================================================================
# Curve -> jnt
# =============================================================================

def get_curve_jnt_base_name(curve):
    u"""
    根据 Curve Transform Short Name 生成默认 jnt Base Name。

    ``crv_lf_brow_001`` 会得到 ``jnt_lf_brow``；非 ``crv_`` 前缀的 Curve
    则直接在 Short Name 前增加 ``jnt_``。

    Args:
        curve (str):
            Maya NURBS Curve Transform 或 Shape。

    Returns:
        str:
        去掉末尾三位序号后的默认 jnt Base Name。

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


def create_jnts_on_curve_cvs(
        curve,
        jnt_base_name=None,
        parent_chain=True,
        create_group=True,
        group_name=None,
        radius=None
):
    u"""
    根据 Curve 全部 CV 的世界位置创建 jnt。

    每一个 CV 对应一个 jnt。默认情况下新 jnt 会按 CV 顺序组成 Chain，
    并放到一个自动创建的 jnt Group 下。该函数只依据 CV Position 建 jnt，
    不负责 jnt Orient、Skin 或 Controller Build。

    Args:
        curve (str):
            Maya NURBS Curve Transform 或 Shape。
        jnt_base_name (str | None):
            jnt 基础名称；None 时由 Curve Name 自动生成。
        parent_chain (bool):
            是否按 CV 顺序建立连续 jnt Chain。
        create_group (bool):
            是否为本次 jnt Build 创建独立 Group。
        group_name (str | None):
            自定义 jnt Group 名称；None 时从 jnt Base Name 推导。
        radius (float | None):
            可选 jnt Radius；None 时使用 ``jnt.create`` 默认值。

    Returns:
        dict:
        包含 ``curve``、``jnt_list``、``jnt_grp`` 的 Build Result。

    Raises:
        RuntimeError:
        Curve 无效、没有 CV、Group 名称被占用或 jnt 创建失败时抛出。
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
    # Step 02：确定 jnt Base Name，并根据参数准备可选的 jnt Group
    # -------------------------------------------------------------------------
    if jnt_base_name is None:
        jnt_base_name = get_curve_jnt_base_name(
            curve
        )

    jnt_group = None

    if create_group:
        if group_name is None:
            group_base_name = jnt_base_name

            if group_base_name.startswith("jnt_"):
                group_base_name = group_base_name.replace(
                    "jnt_",
                    "grp_",
                    1
                )

            group_name = "{}_jnts".format(
                group_base_name
            )

        # ---------------------------------------------------------------------
        # Step 03：创建 Group 前先做 Scene Name Occupancy 检查，避免 Maya 自动改名
        # ---------------------------------------------------------------------
        scene_utils.ensure_nodes_available(
            group_name,
            label=u"jnt Group"
        )
        jnt_group = scene_utils.create_node(
            "transform",
            group_name
        )

    # -------------------------------------------------------------------------
    # Step 04：按 CV 顺序逐个创建 jnt，并根据 parent_chain 更新 Parent
    # -------------------------------------------------------------------------
    jnts = []
    current_parent = jnt_group
    position_index = 0

    while position_index < len(positions):
        jnt_name = "{}_{:03d}".format(
            jnt_base_name,
            position_index + 1
        )

        parent_node = jnt_group

        if parent_chain:
            parent_node = current_parent

        jnt = jnt_utils.jnt.create(
            name=jnt_name,
            position=positions[position_index],
            parent=parent_node,
            radius=radius
        )
        jnts.append(
            jnt
        )

        if parent_chain:
            current_parent = jnt

        position_index += 1

    # -------------------------------------------------------------------------
    # Step 05：返回 Curve、jnt List 和 jnt Group，供上层 Rig System 继续使用
    # -------------------------------------------------------------------------
    return {
        "curve": curve_transform,
        "jnt_list": jnts,
        "jnt_grp": jnt_group,
    }


__all__ = [
    "validate_jnt_list",
    "get_jnt_path",
    "parent_jnts_as_chain",
    "create_jnts_at_items",
    "get_curve_jnt_base_name",
    "create_jnts_on_curve_cvs",
]
