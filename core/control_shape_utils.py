# coding=utf-8
u"""
Controller Shape Utils
======================

控制器 NURBS Curve Shape 的通用底层读写模块。

模块职责
--------
这个模块只处理 Controller Shape 本身：

    - 读取 / 保存 / 删除 Controller Shape JSON；
    - 将 JSON 数据重新创建成 Maya NURBS Curve Shape；
    - 查询 Curve Shape / CV / Color / Radius；
    - 设置 Maya Index Color；
    - 对 Shape CV 做平移、缩放、旋转和镜像。

当前公开方法
------------
资源目录：
    get_library_dir()
        返回正式 Controller Shape JSON / Preview 资源目录。

Curve / CV 查询：
    get_curve_shapes(transform)
        获取 Transform 下全部有效 NURBS Curve Shape。

    get_shape_cvs(transform)
        获取控制器 Transform 下全部 CV Component。

    get_selected_curve_transforms()
        获取当前 Selection 中有效的 Curve Transform。

Shape 数据：
    get_shape_data(transform)
        将 Controller Curve Shape 转成可 JSON 序列化的数据。

    apply_shape_data(transform, shape_data_list)
        使用 Shape 数据替换 Transform 下现有 Curve Shape。

    load_shape_data(shape_name)
        从正式资源目录读取 Shape JSON。

    save_shape_data(shape_name, transform)
        将 Controller Shape 保存成 JSON。

    delete_shape_data(shape_name, delete_previews=True)
        删除 Shape JSON，并可同时删除 JPG / PNG Preview。

颜色 / 尺寸：
    get_shape_color(transform, default=None)
        获取第一个 Curve Shape 的 Maya Index Color。

    get_shape_radius(transform)
        获取所有 CV 到局部原点的最大距离。

    set_shape_color(transform, color_index)
        设置 Curve Shape Maya Index Color。

    set_shape_radius(transform, radius)
        将 Shape 最大局部半径调整到指定值。

CV 变换：
    translate_shape(transform, offset)
        在 Object Space 平移 Shape CV。

    scale_shape(transform, scale_value)
        在 Object Space 缩放 Shape CV。

    rotate_shape(transform, rotate_x=0.0, rotate_y=0.0, rotate_z=0.0)
        在 Object Space 旋转 Shape CV。

    mirror_shape(transform, axis="x")
        沿指定局部轴镜像 Shape CV。

Shape JSON 数据结构
-------------------
每一个 Transform 可以包含多个 Curve Shape，因此最外层是 list：

    [
        {
            "points": [...],
            "degree": 3,
            "periodic": False,
            "knot": [...],
        },
        ...
    ]

``points`` 使用扁平 XYZ 数组保存，方便 JSON 序列化和早期 Shape Library 兼容。

本模块不负责
------------
- Controller Zero / Driven / Connect / Output 层级；
- Sub Controller；
- Rig Controller Builder；
- Thumbnail Playblast；
- PySide Shape Library UI。

模块边界
--------
    Curve Shape 数据 / CV 编辑   -> control_shape_utils
    文件 / JSON                  -> file_utils
    Controller Rig Hierarchy     -> systems.controller
    Controller Tool UI           -> tools.controller

设计原则
--------
1. Shape 编辑只修改 CV，不修改 Controller Transform TRS；
2. Shape Library 文件操作统一复用 ``file_utils``；
3. apply_shape_data() 只替换 Curve Shape，不重建整个 Controller Transform；
4. 多 Shape Controller 保留 Shape 顺序并生成稳定 Shape 名；
5. 当前颜色 API 只负责 Maya Index Color；RGB Color 如以后需要应新增明确 API。
"""

from __future__ import print_function

import math
import os

import maya.cmds as cmds

from ..config import controller_shapes_dir
from . import file_utils


# =============================================================================
# Library - Shape 资源目录
# =============================================================================

def get_library_dir():
    u"""

        返回正式 Controller Shape 资源目录。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    return controller_shapes_dir


# =============================================================================
# Query - Curve Shape / CV / Selection
# =============================================================================

def get_curve_shapes(transform):
    u"""

        返回 Transform 下全部有效 NURBS Curve Shape。

        Intermediate Shape 会被过滤。

        Args:
            transform (str):
                需要处理的 Maya Transform 节点名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    # 步骤 1：直接按 nurbsCurve 类型查询 Shape。
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
    u"""

        返回一个 Controller Transform 下所有 Curve Shape 的全部 CV。

        Args:
            transform (str):
                需要处理的 Maya Transform 节点名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    cvs = []
    shapes = get_curve_shapes(transform)

    # 步骤 1：逐 Shape 展开 cv[*]。
    for shape in shapes:
        shape_cvs = cmds.ls(
            shape + ".cv[*]",
            flatten=True
        )

        if shape_cvs is None:
            shape_cvs = []

        # 步骤 2：保持 Shape / CV 原顺序加入总列表。
        for cv in shape_cvs:
            cvs.append(cv)

    return cvs


def get_selected_curve_transforms():
    u"""

        返回当前 Selection 中有效的 Curve Transform。

        Shape Selection 会自动转换到 Parent Transform，重复节点会去重。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    # 步骤 1：读取当前 Selection。
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    selections = cmds.ls(
        selection=True,
        long=True,
        objectsOnly=True
    )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if selections is None:
        selections = []

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    transforms = []

    # 步骤 2：逐节点整理成 Curve Transform。
    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node in selections:
        node_type = cmds.nodeType(node)

        # 选中 Shape 时转到 Transform。
        if node_type == "nurbsCurve":
            parents = cmds.listRelatives(
                node,
                parent=True,
                fullPath=True
            )

            if parents:
                node = parents[0]

        # 只接受 Transform。
        if cmds.nodeType(node) != "transform":
            continue

        # Transform 必须至少有一个有效 Curve Shape。
        if not get_curve_shapes(node):
            continue

        if node not in transforms:
            transforms.append(node)

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return transforms


# =============================================================================
# Shape Data - Maya Curve -> JSON Data
# =============================================================================

def get_shape_data(transform):
    u"""
    将一个 Controller Transform 转成 JSON 可保存的 Shape 数据。

    Args:
        transform (str):
            需要处理的 Maya Transform 节点名称。

    Returns:
        list: 每个 Curve Shape 对应一个字典。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    result = []
    # -------------------------------------------------------------------------
    # Step 02：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    shapes = get_curve_shapes(transform)

    # -------------------------------------------------------------------------
    # 步骤 1：逐 Shape 收集 Curve 定义。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 03：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for shape in shapes:
        degree = cmds.getAttr(shape + ".degree")
        form = cmds.getAttr(shape + ".form")
        periodic = form == 2

        # ---------------------------------------------------------------------
        # 步骤 2：按 Object Space 保存 CV。
        #
        # 使用 Object Space 是为了让 Shape 数据与 Controller 在世界中的位置无关，
        # 同一个 Shape 可以应用到任何 Controller Transform。
        # ---------------------------------------------------------------------
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

        # ---------------------------------------------------------------------
        # 步骤 3：保存 Knot Vector。
        # ---------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 04：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return result


def get_shape_color(transform, default=None):
    u"""

        返回第一个 Curve Shape 的 Maya Index Color。

        如果没有启用 Override，或者当前使用 RGB Override，则返回 default。

        Args:
            transform (str):
                需要处理的 Maya Transform 节点名称。
            default (object):
                当前查询、配置或 UI 逻辑在没有显式值时使用的默认值。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    # 步骤 1：取得第一个 Shape。
    shapes = get_curve_shapes(transform)

    if not shapes:
        return default

    shape = shapes[0]

    # 步骤 2：未启用 Override 时没有 Index Color 语义。
    override_enabled = cmds.getAttr(
        shape + ".overrideEnabled"
    )

    if not override_enabled:
        return default

    # 步骤 3：RGB 模式不属于当前 Index Color API。
    use_rgb = cmds.getAttr(
        shape + ".overrideRGBColors"
    )

    if use_rgb:
        return default

    return cmds.getAttr(
        shape + ".overrideColor"
    )


def get_shape_radius(transform):
    u"""

        返回 Controller Shape CV 到局部原点的最大距离。

        这个值作为 Shape 的近似“半径”，用于统一调整控制器尺寸。

        Args:
            transform (str):
                需要处理的 Maya Transform 节点名称。

        Returns:
            object | float:
            当前数学、权重或空间计算得到的浮点结果。

    """
    cvs = get_shape_cvs(transform)

    if not cvs:
        return 0.0

    maximum_distance = 0.0

    # 步骤 1：逐 CV 计算 Object Space 到原点的欧氏距离。
    for cv in cvs:
        position = cmds.xform(
            cv,
            query=True,
            objectSpace=True,
            translation=True
        )

        distance = math.sqrt(
            position[0] * position[0]
            + position[1] * position[1]
            + position[2] * position[2]
        )

        if distance > maximum_distance:
            maximum_distance = distance

    return maximum_distance


# =============================================================================
# Shape Data - JSON Data -> Maya Curve
# =============================================================================

def _create_temp_curve(shape_data):
    """
    根据单个 Shape 数据创建临时 Curve Transform。

    这是内部 Helper，不作为正式公开 API。
    """
    # 步骤 1：读取数据，并给旧文件缺失字段提供安全默认值。
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    points_flat = shape_data.get("points")

    if points_flat is None:
        points_flat = []

    degree = int(shape_data.get("degree", 1))
    # -------------------------------------------------------------------------
    # Step 02：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    periodic = bool(shape_data.get("periodic", False))
    knots = shape_data.get("knot")

    if knots is None:
        knots = []

    # 步骤 2：扁平 XYZ 数组还原成 [[x,y,z], ...]。
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # 步骤 3：Periodic Curve 需要在尾部重复前 degree 个点。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if periodic:
        extra_index = 0

        while extra_index < degree:
            if extra_index < len(points):
                points.append(points[extra_index])

            extra_index += 1

    # 步骤 4：准备 cmds.curve 参数。
    create_kwargs = {
        "degree": degree,
        "point": points,
        "periodic": periodic,
    }

    if knots:
        create_kwargs["knot"] = knots

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return cmds.curve(**create_kwargs)


def apply_shape_data(transform, shape_data_list):
    u"""

        使用 Shape 数据替换 Transform 下已有 Curve Shape。

        注意：
            只替换 Shape，不删除或重建 Controller Transform。

        Args:
            transform (str):
                需要处理的 Maya Transform 节点名称。
            shape_data_list (list):
                Controller Shape 的 CV、Degree、Form 等序列化数据列表。

        Returns:
            object:
            完成设置或应用后的目标对象 / 状态结果。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # 步骤 1：确认目标 Controller 存在。
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not cmds.objExists(transform):
        raise RuntimeError(
            u"控制器不存在：{}".format(transform)
        )

    # 步骤 2：删除旧 Curve Shape。
    # -------------------------------------------------------------------------
    # Step 02：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    old_shapes = get_curve_shapes(transform)

    if old_shapes:
        cmds.delete(old_shapes)

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    shape_index = 0

    # -------------------------------------------------------------------------
    # 步骤 3：逐条 Shape Data 创建临时 Curve，再把 Shape Parent 到目标 Transform。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for shape_data in shape_data_list:
        temp_curve = _create_temp_curve(shape_data)
        temp_shapes = get_curve_shapes(temp_curve)

        if not temp_shapes:
            cmds.delete(temp_curve)
            continue

        temp_shape = temp_shapes[0]

        parent_result = cmds.parent(
            temp_shape,
            transform,
            shape=True,
            relative=True
        )

        if not parent_result:
            cmds.delete(temp_curve)
            raise RuntimeError(
                u"无法把 Controller Shape 挂到目标 Transform：{}".format(
                    transform
                )
            )

        parented_shape = parent_result[0]

        # ---------------------------------------------------------------------
        # 步骤 4：生成稳定 Shape 名。
        # 第一个为 ctrlShape，后续为 ctrlShape2 / ctrlShape3 ...。
        # ---------------------------------------------------------------------
        short_name = transform.split("|")[-1]
        new_shape_name = "{}Shape".format(short_name)

        if shape_index > 0:
            new_shape_name = "{}Shape{}".format(
                short_name,
                shape_index + 1
            )

        cmds.rename(
            parented_shape,
            new_shape_name
        )

        # Transform 只是临时容器，Shape 已移走后可以删除。
        cmds.delete(temp_curve)
        shape_index += 1

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return transform


# =============================================================================
# Shape Library - JSON 文件读写
# =============================================================================

def load_shape_data(shape_name):
    u"""

        从正式 Controller Shape 资源目录读取一个 Shape JSON。

        Args:
            shape_name (str):
                `shape_name` 对应的 Maya 节点或资源名称。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    # 步骤 1：构建资源路径。
    file_path = os.path.join(
        get_library_dir(),
        "{}.json".format(shape_name)
    )

    # 步骤 2：统一通过 file_utils 读取 JSON。
    return file_utils.read_json(file_path)


def save_shape_data(shape_name, transform):
    u"""
    将 Controller Shape 保存到正式资源目录。

    Args:
        shape_name (str):
            `shape_name` 对应的 Maya 节点或资源名称。
        transform (str):
            需要处理的 Maya Transform 节点名称。

    Returns:
        str: 最终 JSON 文件路径。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：验证 Shape 名称。
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not shape_name:
        raise RuntimeError(u"Shape 名称不能为空。")

    # 步骤 2：从 Maya Controller 收集 Shape 数据。
    # -------------------------------------------------------------------------
    # Step 02：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    data = get_shape_data(transform)

    if not data:
        raise RuntimeError(u"所选对象没有 NURBS Curve Shape。")

    # 步骤 3：确保资源目录存在。
    # -------------------------------------------------------------------------
    # Step 03：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    library_dir = file_utils.ensure_directory(
        get_library_dir()
    )

    # 步骤 4：写入 UTF-8 JSON。
    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    file_path = os.path.join(
        library_dir,
        "{}.json".format(shape_name)
    )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return file_utils.write_json(
        file_path=file_path,
        data=data,
        indent=4,
        ensure_ascii=False,
        sort_keys=False
    )


def delete_shape_data(shape_name, delete_previews=True):
    u"""
    删除图库 Shape JSON，并可同时删除 JPG / PNG Preview。

    Args:
        shape_name (str):
            `shape_name` 对应的 Maya 节点或资源名称。
        delete_previews (bool):
            写入正式 Controller Shape 资源前是否删除临时 Preview 节点。

    Returns:
        list: 实际删除的文件路径。
    """
    if not shape_name:
        return []

    # 步骤 1：准备要删除的资源扩展名。
    extensions = [".json"]

    if delete_previews:
        extensions.append(".jpg")
        extensions.append(".png")

    deleted_files = []
    library_dir = get_library_dir()

    # 步骤 2：逐文件检查并删除。
    for extension in extensions:
        file_path = os.path.join(
            library_dir,
            shape_name + extension
        )

        if not os.path.isfile(file_path):
            continue

        os.remove(file_path)
        deleted_files.append(
            file_utils.normalize_path(file_path)
        )

    return deleted_files


# =============================================================================
# Color - Maya Index Color
# =============================================================================

def set_shape_color(transform, color_index):
    u"""
    设置 Transform 下全部 Curve Shape 的 Maya Index Color。

    Args:
        transform (str):
            需要处理的 Maya Transform 节点名称。
        color_index (int):
            对应 Maya Array Attribute、Target、Guide 或构建元素的逻辑索引。
    """
    shapes = get_curve_shapes(transform)

    # 步骤 1：每一个 Curve Shape 都需要独立开启 Override。
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


# =============================================================================
# CV Transform - 平移 / 缩放 / 半径 / 旋转 / 镜像
# =============================================================================

def translate_shape(transform, offset):
    u"""
    按 Object Space 平移 Controller Shape CV。

    Args:
        transform (str):
            需要处理的 Maya Transform 节点名称。
        offset (float):
            当前 Rig / Shape / Surface 操作使用的 Offset 数值或偏移向量。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：验证 Offset。
    if offset is None or len(offset) != 3:
        raise ValueError(
            u"offset 必须是包含 3 个数值的列表或元组。"
        )

    # 步骤 2：取得全部 CV；没有 Shape 时不做任何操作。
    cvs = get_shape_cvs(transform)

    if not cvs:
        return

    # 步骤 3：只移动 CV，不修改 Controller Transform。
    cmds.move(
        offset[0],
        offset[1],
        offset[2],
        cvs,
        relative=True,
        objectSpace=True
    )


def scale_shape(transform, scale_value):
    u"""
    按 Object Space 等比缩放 Controller Shape CV。

    Args:
        transform (str):
            需要处理的 Maya Transform 节点名称。
        scale_value (float | tuple[float, float, float]):
            Controller Shape CV 使用的统一或 XYZ Scale 值。
    """
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


def set_shape_radius(transform, radius):
    u"""
    将 Controller Shape 的最大局部半径调整为指定值。

    计算：
        scale = target_radius / current_radius

    Args:
        transform (str):
            需要处理的 Maya Transform 节点名称。
        radius (float):
            创建节点或控制器使用的半径值。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：验证目标半径。
    radius = float(radius)

    if radius < 0.0:
        raise ValueError(u"radius 不能小于 0。")

    # 步骤 2：读取当前最大 CV 半径。
    current_radius = get_shape_radius(transform)

    if current_radius == 0.0:
        return

    # 步骤 3：计算等比缩放值并复用 scale_shape。
    scale_value = radius / current_radius

    scale_shape(
        transform,
        scale_value
    )


def rotate_shape(
        transform,
        rotate_x=0.0,
        rotate_y=0.0,
        rotate_z=0.0
):
    u"""
    按 Object Space 旋转 Controller Shape CV。

    Args:
        transform (str):
            需要处理的 Maya Transform 节点名称。
        rotate_x (float):
            Controller Shape / Transform 绕 X 轴应用的旋转角度。
        rotate_y (float):
            Controller Shape / Transform 绕 Y 轴应用的旋转角度。
        rotate_z (float):
            Controller Shape / Transform 绕 Z 轴应用的旋转角度。
    """
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
    u"""
    沿指定局部轴镜像 Controller Shape CV。

    镜像只通过对应轴 Scale=-1 完成，不修改 Controller Transform Scale。

    Args:
        transform (str):
            需要处理的 Maya Transform 节点名称。
        axis (str):
            操作使用的轴向标记。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：准备三轴缩放值。
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    scale_x = 1.0
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    scale_y = 1.0
    scale_z = 1.0

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
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

    # 步骤 2：取得全部 CV。
    cvs = get_shape_cvs(transform)

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not cvs:
        return

    # 步骤 3：只镜像 Shape CV。
    # -------------------------------------------------------------------------
    # Step 05：执行当前阶段的核心处理
    # -------------------------------------------------------------------------
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
    "get_shape_color",
    "get_shape_radius",
    "apply_shape_data",
    "load_shape_data",
    "save_shape_data",
    "delete_shape_data",
    "set_shape_color",
    "translate_shape",
    "scale_shape",
    "set_shape_radius",
    "rotate_shape",
    "mirror_shape",
]
