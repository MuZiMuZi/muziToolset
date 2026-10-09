# coding=utf-8
u"""
transform_utils：Maya Transform 基础工具。

方法介绍与使用场景：

    Transform.__init__
        创建一个 Transform 工具对象，并保存需要操作的 Maya 节点。
        适合后续统一处理 Transform、Joint、Controller、Guide、Group 等节点。

    Transform.match_transform
        将当前对象直接对齐到指定目标对象的 Transform。
        Guide Locator 的 Translate / Rotate 就是绑定定位数据，不读取 Locator Shape 的额外偏移。

    Transform.get_world_matrix
        获取当前对象的世界矩阵。
        适合矩阵对齐、矩阵驱动、Offset Matrix 计算等场景。

    Transform.set_world_matrix
        将给定的世界矩阵设置到当前对象。
        适合复制 Transform 状态、矩阵对齐和矩阵绑定等场景。

    Transform.reset_transform
        将当前对象的位移、旋转、缩放恢复到默认数值。
        适合清理 Controller、Group、Joint 等节点的 Transform 数值。

    Transform.get_transform
        获取当前对象对应的 Transform 节点。
        适合输入 Shape 节点时自动找到其父 Transform，也可以直接处理 Transform 节点。
"""



import maya.cmds as cmds
from ..common import math_utils
from ..common import scene_utils



class Transform(object):

    def __init__(self, object=None):
        u"""
        初始化 Transform 工具对象。

        Args:
            object (str/字符串节点名称):
                需要操作的 Maya 节点，可以是 Transform、Joint、Shape 等节点。
        """

        self.object = None
        self.world_matrix = None

        # 如果传入 Maya 节点，则统一转换成 字符串节点名称 保存。
        if object:
            self.object = str(object)

    def match_transform(self, target, position=True, rotation=True, scale=True):
        u"""
        将当前对象直接对齐到指定目标对象的 Transform。

        Guide 系统统一把 Locator Transform 作为真正的定位数据：
            Locator Translate / Rotate / Scale
                        ↓
                  Target Transform
        不读取 Locator Shape.localPosition，也不额外计算 Shape.worldPosition。
        这样 Joint、Controller 和其他绑定节点都使用同一套简单明确的对齐规则。

        Args:
            target (str/字符串节点名称):
                需要匹配的目标对象。
            position (bool):
                是否匹配目标位置，默认 True。
            rotation (bool):
                是否匹配目标旋转，默认 True。
            scale (bool):
                是否匹配目标缩放，默认 True。

        Returns:
            None
        """

        # 目标统一转换成 字符串节点名称，然后直接使用 Maya matchTransform 对齐。
        target = str(target)

        cmds.matchTransform(
            self.object,
            target,
            position=position,
            rotation=rotation,
            scale=scale
        )

    def get_world_matrix(self):
        u"""
        获取当前对象的世界矩阵。

        Returns:
            Matrix: 当前对象的世界矩阵。
        """

        self.world_matrix = cmds.xform(self.object, query=True, matrix=True, worldSpace=True)
        return self.world_matrix

    def set_world_matrix(self, matrix):
        u"""
        将给定的世界矩阵设置到当前对象。

        Args:
            matrix (list[float] | maya.api.OpenMaya.MMatrix):
                用于 Transform、Constraint 或空间计算的 4x4 Matrix 数据。

        Returns:
            None
        """

        cmds.xform(self.object, matrix=matrix, worldSpace=True)
        self.world_matrix = matrix

    def reset_transform(self, translate=True, rotate=True, scale=True):
        u"""
        将当前对象的 Transform 数值恢复到默认状态。

        Args:
            translate (bool):
                是否将 Translate 重置为 0。
            rotate (bool):
                是否将 Rotate 重置为 0。
            scale (bool):
                是否将 Scale 重置为 1。

        Returns:
            None
        """

        if translate:
            cmds.setAttr(self.object + ".translate", 0, 0, 0)

        if rotate:
            cmds.setAttr(self.object + ".rotate", 0, 0, 0)

        if scale:
            cmds.setAttr(self.object + ".scale", 1, 1, 1)

    def get_transform(self):
        u"""
        获取当前对象对应的 Transform 节点。

        如果当前对象本身就是 Transform，则直接返回当前对象；
        如果当前对象是 Shape，则返回它的父 Transform。

        Returns:
            字符串节点名称: 当前对象对应的 Transform 节点。
        """

        if cmds.objectType(self.object, isAType="transform"):
            return self.object

        parent_object = (cmds.listRelatives(self.object, parent=True, fullPath=True) or [None])[0]
        return parent_object

def validate_transform(node):
    u"""
    检查节点存在，并确认它是 Maya Transform / Jnt。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        bool:
        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    scene_utils.validate_node(
        node
    )

    node_type = cmds.nodeType(
        node
    )

    if node_type not in ["transform", "joint"]:
        raise RuntimeError(
            u"节点不是 Transform / Jnt：{} | type={}".format(
                node,
                node_type
            )
        )

    return True

def _validate_vector3(value, label):
    u"""检查 Translation / Rotation / Offset 是否包含 3 个数值。"""
    if value is None:
        raise ValueError(
            u"{} 必须包含 3 个数值。".format(
                label
            )
        )

    try:
        value_count = len(
            value
        )
    except TypeError:
        raise ValueError(
            u"{} 必须包含 3 个数值。".format(
                label
            )
        )

    if value_count != 3:
        raise ValueError(
            u"{} 必须包含 3 个数值。".format(
                label
            )
        )

    return True

def get_world_translation(node):
    u"""
    返回 Transform / Jnt 的 World Translation。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
    """
    validate_transform(
        node
    )

    return cmds.xform(
        node,
        query=True,
        worldSpace=True,
        translation=True
    )

def set_world_translation(node, translation):
    u"""
    设置 Transform / Jnt 的 World Translation。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。
        translation (object):
            当前方法执行 Maya / Rig 操作时使用的 `translation` 数据。

    Returns:
        object:
        完成设置或应用后的目标对象 / 状态结果。
    """
    validate_transform(
        node
    )
    _validate_vector3(
        translation,
        "translation"
    )

    cmds.xform(
        node,
        worldSpace=True,
        translation=translation
    )

    return node

def get_world_rotation(node):
    u"""
    返回 Transform / Jnt 的 World Rotation。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
    """
    validate_transform(
        node
    )

    return cmds.xform(
        node,
        query=True,
        worldSpace=True,
        rotation=True
    )

def set_world_rotation(node, rotation):
    u"""
    设置 Transform / Jnt 的 World Rotation。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。
        rotation (list[float] | tuple[float, float, float]):
            Jnt / Transform 使用的 XYZ Rotation。

    Returns:
        object:
        完成设置或应用后的目标对象 / 状态结果。
    """
    validate_transform(
        node
    )
    _validate_vector3(
        rotation,
        "rotation"
    )

    cmds.xform(
        node,
        worldSpace=True,
        rotation=rotation
    )

    return node
