# coding=utf-8
"""控制器工具的构建编排，统一复用当前 Ctrl 基础实现。"""

import maya.cmds as cmds

from ...core.rigging.ctrl_utils import Ctrl
from ...core.rigging import constraint_utils
from ...core.common import hierarchy_utils, scene_utils


def create_ctrl(name, shape="circle", radius=1.0, axis="X+",
                target_node=None, parent_node=None, color=17,
                rotate_x=0.0, create_sub_ctrl=True, add_to_set=True):
    """创建控制器并返回 UI 使用的节点信息。

    Args:
        name (str): 控制器名称，已有同名节点时拒绝覆盖。
        shape (str): 图库形状名称。
        radius (float): 图形大小倍率。
        axis (str): 图形朝向。
        target_node (str | None): 吸附目标。
        parent_node (str | None): 控制器最外层的父节点。
        color (int): Maya 颜色索引。
        rotate_x (float): 图形额外 X 旋转。
        create_sub_ctrl (bool): 是否创建次级控制器。
        add_to_set (bool): 是否加入 ctrl_set。

    Returns:
        dict: 主控制器、Zero 组和 Output 组名称。

    Raises:
        ValueError: 名称冲突、资源不存在或大小无效。
    """
    if cmds.objExists(name):
        raise ValueError(u"控制器已存在，请修改名称：{}".format(name))
    if radius <= 0:
        raise ValueError(u"控制器大小必须大于零。")
    # 先验证资源和输入节点，避免失败后留下空控制器。
    import os
    from ...config import controller_shapes_dir
    if not os.path.isfile(os.path.join(controller_shapes_dir, shape + ".json")):
        raise ValueError(u"找不到控制器图形：{}".format(shape))
    for node in (target_node, parent_node):
        if node is not None and not cmds.objExists(node):
            raise ValueError(u"节点不存在：{}".format(node))

    control = Ctrl(name)
    control.create_ctrl(shape_name=shape, ctrl_color=color,
                        ctrl_size=radius, ctrl_axis=axis,
                        create_hierarchy=False,
                        match_transform_target=target_node)
    control.set_ctrl_rotate(rotate_x=rotate_x)
    control.create_ctrl_hierarchy(sub_ctrl_shape=shape,
                                  sub_ctrl_color=color,
                                  sub_ctrl_size=radius * 0.7,
                                  ctrl_axis=axis,
                                  create_sub_ctrl=create_sub_ctrl)
    if parent_node:
        hierarchy_utils.parent(control.zero_grp, parent_node)
    if add_to_set:
        if not cmds.objExists("ctrl_set"):
            cmds.sets(empty=True, name="ctrl_set")
        cmds.sets(control.ctrl, add="ctrl_set")
        if control.sub_ctrl:
            cmds.sets(control.sub_ctrl, add="ctrl_set")
    return {"ctrl_node": control.ctrl, "zero_node": control.zero_grp,
            "output_node": control.output_grp, "top_grp": control.zero_grp}


def create_fk_ctrl(target_list, ctrl_name_list, shape="circle", radius=1.0,
                   axis="Y+", constrain=True, add_to_set=True):
    """按输入顺序创建 FK 控制器，以前一个 Output 驱动后一个 Zero。

    Args:
        target_list (list[str]): 按链顺序排列的目标。
        ctrl_name_list (list[str]): 对应控制器名称。
        shape (str): 图库形状。
        radius (float): 图形大小倍率。
        axis (str): 图形朝向。
        constrain (bool): 是否约束目标的位置和旋转。
        add_to_set (bool): 是否加入 ctrl_set。

    Returns:
        list[dict]: 每个控制器的节点信息。

    Raises:
        ValueError: 输入数量不匹配、目标失效或名称冲突。
    """
    if len(target_list) != len(ctrl_name_list):
        raise ValueError(u"目标数量与控制器名称数量不一致。")
    seen = set()
    for target, name in zip(target_list, ctrl_name_list):
        if not cmds.objExists(target):
            raise ValueError(u"目标不存在：{}".format(target))
        if name in seen or cmds.objExists(name):
            raise ValueError(u"控制器名称重复：{}".format(name))
        seen.add(name)
    results = []
    previous_output = None
    scene_utils.open_undo_chunk("MuziCreateFKControllers")
    try:
        for target, name in zip(target_list, ctrl_name_list):
            result = create_ctrl(name=name, shape=shape, radius=radius,
                                 axis=axis, target_node=target,
                                 parent_node=previous_output,
                                 add_to_set=add_to_set)
            if constrain:
                constraint_utils.create_constraint(
                    driver_objects=result["output_node"], driven_object=target,
                    constraint_type="parentConstraint", maintain_offset=True)
            previous_output = result["output_node"]
            results.append(result)
    finally:
        scene_utils.close_undo_chunk()
    return results
