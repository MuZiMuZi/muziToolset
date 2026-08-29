# coding=utf-8
u"""
FK Control Creator
==================

根据当前选择顺序创建 FK 控制器层级。
仅依赖 maya.cmds 和本包的 control_shape_tool，不再依赖 PyMel。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import control_shape_tool


def _short_name(node):
    return node.split("|")[-1]


def _control_name_from_target(target):
    short_name = _short_name(target)

    if short_name.startswith("jnt_"):
        return short_name.replace("jnt_", "ctrl_", 1)

    if short_name.startswith("bpjnt_"):
        return short_name.replace("bpjnt_", "ctrl_", 1)

    return "ctrl_{}".format(short_name)


def _side_color(name):
    lower_name = name.lower()

    if "_l_" in lower_name or lower_name.startswith("ctrl_l_"):
        return 6

    if "_r_" in lower_name or lower_name.startswith("ctrl_r_"):
        return 13

    return 17


def _set_curve_color(transform, color_index):
    shapes = cmds.listRelatives(
        transform,
        shapes=True,
        noIntermediate=True,
        fullPath=True,
        type="nurbsCurve"
    ) or []

    for shape in shapes:
        cmds.setAttr(shape + ".overrideEnabled", 1)
        cmds.setAttr(shape + ".overrideRGBColors", 0)
        cmds.setAttr(shape + ".overrideColor", color_index)


def _scale_curve_shape(transform, radius):
    shapes = cmds.listRelatives(
        transform,
        shapes=True,
        noIntermediate=True,
        fullPath=True,
        type="nurbsCurve"
    ) or []

    cvs = []
    for shape in shapes:
        shape_cvs = cmds.ls(shape + ".cv[*]", flatten=True) or []
        for cv in shape_cvs:
            cvs.append(cv)

    if cvs:
        cmds.scale(
            radius,
            radius,
            radius,
            cvs,
            relative=True,
            objectSpace=True
        )


def create_fk_controls(
        targets,
        shape="circle",
        radius=1.0,
        constrain=True
):
    """
    根据 targets 顺序创建 FK 控制器。

    Args:
        targets(list[str]): 驱动目标，顺序即 FK 层级顺序。
        shape(str): MuziTools/image 中的 Shape JSON 名称。
        radius(float): Shape 缩放倍数。
        constrain(bool): 是否用 parentConstraint 驱动目标。

    Returns:
        list[str]: 创建的控制器 Transform。
    """
    if not targets:
        return []

    shape_data = control_shape_tool.load_shape_data(shape)
    controls = []
    previous_control = None

    cmds.undoInfo(openChunk=True, chunkName="MuziCreateFkControls")
    try:
        for target in targets:
            if not cmds.objExists(target):
                cmds.warning(u"目标不存在：{}".format(target))
                continue

            control_name = _control_name_from_target(target)
            if cmds.objExists(control_name):
                cmds.warning(u"控制器已存在，跳过：{}".format(control_name))
                continue

            zero_name = control_name.replace("ctrl_", "zero_", 1)
            control = cmds.createNode("transform", name=control_name)
            zero_group = cmds.createNode("transform", name=zero_name)

            control_shape_tool.apply_shape_data(
                control,
                shape_data
            )
            _scale_curve_shape(control, radius)
            _set_curve_color(control, _side_color(control_name))

            cmds.parent(control, zero_group)
            cmds.matchTransform(
                zero_group,
                target,
                position=True,
                rotation=True
            )

            if previous_control is not None:
                cmds.parent(zero_group, previous_control)

            if constrain:
                cmds.parentConstraint(
                    control,
                    target,
                    maintainOffset=False
                )

            controls.append(control)
            previous_control = control

    except Exception as error:
        cmds.warning(str(error))
        raise
    finally:
        cmds.undoInfo(closeChunk=True)

    if controls:
        cmds.select(controls, replace=True)

    return controls


def main():
    """按当前 Maya 选择顺序创建 FK 控制器。"""
    selections = cmds.ls(selection=True, long=True) or []

    if not selections:
        cmds.warning(u"请选择多个物体或关节后再创建 FK 控制器。")
        return []

    return create_fk_controls(
        targets=selections,
        shape="circle",
        radius=1.0,
        constrain=True
    )
