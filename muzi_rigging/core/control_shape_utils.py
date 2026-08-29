# coding=utf-8
u"""
Controller Shape Utils
======================

控制器 NURBS Curve Shape 的底层读写模块。

职责：
    1. 读取 / 保存 Controller Shape JSON；
    2. 把 JSON 数据创建成 Maya NURBS Curve Shape；
    3. 获取控制器 Curve Shape / CV；
    4. 设置 Shape Maya Index Color；
    5. 对 Shape CV 做缩放、旋转和镜像。

本模块不包含任何 PySide UI。
"""

from __future__ import print_function

import json
import os

import maya.cmds as cmds

from ..config import controller_shapes_dir


def get_library_dir():
    """返回正式 Controller Shape 资源目录。"""
    return controller_shapes_dir


def get_curve_shapes(transform):
    """返回 Transform 下有效的 NURBS Curve Shape。"""
    shapes = cmds.listRelatives(
        transform,
        shapes=True,
        noIntermediate=True,
        fullPath=True,
        type="nurbsCurve"
    )

    if shapes is None:
        shapes = []

    return shapes


def get_shape_cvs(transform):
    """返回一个控制器 Transform 下的全部 CV。"""
    cvs = []
    shapes = get_curve_shapes(transform)

    for shape in shapes:
        shape_cvs = cmds.ls(
            shape + ".cv[*]",
            flatten=True
        )

        if shape_cvs is None:
            shape_cvs = []

        for cv in shape_cvs:
            cvs.append(cv)

    return cvs


def get_selected_curve_transforms():
    """返回当前选择中的 Curve Transform。"""
    selections = cmds.ls(
        selection=True,
        long=True,
        objectsOnly=True
    )

    if selections is None:
        selections = []

    transforms = []

    for node in selections:
        node_type = cmds.nodeType(node)

        if node_type == "nurbsCurve":
            parents = cmds.listRelatives(
                node,
                parent=True,
                fullPath=True
            )

            if parents:
                node = parents[0]

        if cmds.nodeType(node) != "transform":
            continue

        if not get_curve_shapes(node):
            continue

        if node not in transforms:
            transforms.append(node)

    return transforms


def get_shape_data(transform):
    """把一个控制器 Transform 转成 JSON 可保存数据。"""
    result = []
    shapes = get_curve_shapes(transform)

    for shape in shapes:
        degree = cmds.getAttr(shape + ".degree")
        form = cmds.getAttr(shape + ".form")
        periodic = form == 2

        cvs = cmds.ls(
            shape + ".cv[*]",
            flatten=True
        )

        if cvs is None:
            cvs = []

        points = []

        for cv in cvs:
            position = cmds.xform(
                cv,
                query=True,
                objectSpace=True,
                translation=True
            )

            for value in position:
                points.append(value)

        knot_count = cmds.getAttr(
            shape + ".knots",
            size=True
        )

        knots = []
        index = 0

        while index < knot_count:
            knot_value = cmds.getAttr(
                "{}.knots[{}]".format(
                    shape,
                    index
                )
            )
            knots.append(knot_value)
            index += 1

        shape_data = {
            "points": points,
            "degree": degree,
            "periodic": periodic,
            "knot": knots,
        }
        result.append(shape_data)

    return result


def _create_temp_curve(shape_data):
    """根据单个 Shape 数据创建临时 Curve Transform。"""
    points_flat = shape_data.get("points")

    if points_flat is None:
        points_flat = []

    degree = int(shape_data.get("degree", 1))
    periodic = bool(shape_data.get("periodic", False))
    knots = shape_data.get("knot")

    if knots is None:
        knots = []

    points = []
    index = 0

    while index + 2 < len(points_flat):
        point = [
            points_flat[index],
            points_flat[index + 1],
            points_flat[index + 2],
        ]
        points.append(point)
        index += 3

    if periodic:
        extra_index = 0

        while extra_index < degree:
            if extra_index < len(points):
                points.append(points[extra_index])
            extra_index += 1

    create_kwargs = {
        "degree": degree,
        "point": points,
        "periodic": periodic,
    }

    if knots:
        create_kwargs["knot"] = knots

    return cmds.curve(**create_kwargs)


def apply_shape_data(transform, shape_data_list):
    """用 Shape 数据替换 Transform 下已有 Curve Shape。"""
    if not cmds.objExists(transform):
        raise RuntimeError(
            u"控制器不存在：{}".format(transform)
        )

    old_shapes = get_curve_shapes(transform)

    if old_shapes:
        cmds.delete(old_shapes)

    shape_index = 0

    for shape_data in shape_data_list:
        temp_curve = _create_temp_curve(shape_data)
        temp_shapes = get_curve_shapes(temp_curve)

        if not temp_shapes:
            cmds.delete(temp_curve)
            continue

        temp_shape = temp_shapes[0]

        cmds.parent(
            temp_shape,
            transform,
            shape=True,
            relative=True
        )

        short_name = transform.split("|")[-1]
        new_shape_name = "{}Shape".format(short_name)

        if shape_index > 0:
            new_shape_name = "{}Shape{}".format(
                short_name,
                shape_index + 1
            )

        cmds.rename(
            temp_shape,
            new_shape_name
        )
        cmds.delete(temp_curve)
        shape_index += 1

    return transform


def load_shape_data(shape_name):
    """从正式资源目录读取一个 Shape JSON。"""
    file_path = os.path.join(
        get_library_dir(),
        "{}.json".format(shape_name)
    )

    if not os.path.isfile(file_path):
        raise RuntimeError(
            u"控制器 Shape 文件不存在：{}".format(file_path)
        )

    with open(file_path, "r") as file_object:
        data = json.load(file_object)

    return data


def save_shape_data(shape_name, transform):
    """把控制器 Shape 保存到正式资源目录。"""
    if not shape_name:
        raise RuntimeError(u"Shape 名称不能为空。")

    data = get_shape_data(transform)

    if not data:
        raise RuntimeError(u"所选对象没有 NURBS Curve Shape。")

    library_dir = get_library_dir()

    if not os.path.isdir(library_dir):
        os.makedirs(library_dir)

    file_path = os.path.join(
        library_dir,
        "{}.json".format(shape_name)
    )

    with open(file_path, "w") as file_object:
        json.dump(
            data,
            file_object,
            ensure_ascii=False,
            indent=4
        )

    return file_path


def set_shape_color(transform, color_index):
    """设置 Maya Index Color。"""
    shapes = get_curve_shapes(transform)

    for shape in shapes:
        cmds.setAttr(
            shape + ".overrideEnabled",
            1
        )
        cmds.setAttr(
            shape + ".overrideRGBColors",
            0
        )
        cmds.setAttr(
            shape + ".overrideColor",
            int(color_index)
        )


def scale_shape(transform, scale_value):
    """按 Object Space 缩放控制器 Shape。"""
    cvs = get_shape_cvs(transform)

    if not cvs:
        return

    cmds.scale(
        scale_value,
        scale_value,
        scale_value,
        cvs,
        relative=True,
        objectSpace=True
    )


def rotate_shape(transform, rotate_x=0.0, rotate_y=0.0, rotate_z=0.0):
    """按 Object Space 旋转控制器 Shape。"""
    cvs = get_shape_cvs(transform)

    if not cvs:
        return

    cmds.rotate(
        rotate_x,
        rotate_y,
        rotate_z,
        cvs,
        relative=True,
        objectSpace=True
    )


def mirror_shape(transform, axis="x"):
    """沿指定局部轴镜像控制器 Shape。"""
    scale_x = 1.0
    scale_y = 1.0
    scale_z = 1.0

    if axis.lower() == "x":
        scale_x = -1.0
    elif axis.lower() == "y":
        scale_y = -1.0
    elif axis.lower() == "z":
        scale_z = -1.0
    else:
        raise ValueError(
            u"不支持的镜像轴向：{}".format(axis)
        )

    cvs = get_shape_cvs(transform)

    if not cvs:
        return

    cmds.scale(
        scale_x,
        scale_y,
        scale_z,
        cvs,
        relative=True,
        objectSpace=True
    )


__all__ = [
    "get_library_dir",
    "get_curve_shapes",
    "get_shape_cvs",
    "get_selected_curve_transforms",
    "get_shape_data",
    "apply_shape_data",
    "load_shape_data",
    "save_shape_data",
    "set_shape_color",
    "scale_shape",
    "rotate_shape",
    "mirror_shape",
]
