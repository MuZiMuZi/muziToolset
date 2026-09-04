# coding=utf-8
u"""
Jnt Utils
===========

Maya Jnt 领域的专属底层能力模块。

设计原则
--------
Jnt 类只负责“单个 Jnt 节点自己特有的能力”：

    - 创建 Jnt；
    - Jnt Orient；
    - Radius / Local Rotation Axis；
    - Segment Scale Compensate；
    - Maya Jnt Label。

模块级 API 只保留 Maya 全局 Jnt Display Setting：

    - get_display_scale()
    - set_display_scale()

通用能力不在本模块重复包装：

    - 名称 / Rename        -> rename_utils
    - World Transform      -> transform_utils
    - Object / Locator Snap -> snap_utils
    - DAG Parent / Child   -> hierarchy_utils
    - 全场景 Node 查询     -> scene_utils

Jnt 实例在 __init__() 时只验证一次节点存在性和节点类型。
初始化成功后，普通方法默认 self.jnt 仍然是有效 Jnt，
不为每一次操作重复执行存在性和类型检查。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import hierarchy_utils
from . import rename_utils
from . import snap_utils
from . import transform_utils


# =============================================================================
# Global Jnt Display
# =============================================================================

def get_display_scale():
    u"""
    返回 Maya 当前全局 Jnt Display Scale。

    Returns:
        object:
        当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
    """
    return float(
        __MUZI_MAYA_JNT_PROTECTED_00000__(
            query=True
        )
    )


def set_display_scale(scale):
    u"""
    设置 Maya 全局 Jnt Display Scale，并返回最终数值。

    Args:
        scale (bool):
            是否处理 Scale 通道。

    Returns:
        object:
        完成设置或应用后的目标对象 / 状态结果。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    try:
        scale = float(
            scale
        )
    except (TypeError, ValueError):
        raise ValueError(
            u"Jnt Display Scale 必须是数值。"
        )

    if scale <= 0.0:
        raise ValueError(
            u"Jnt Display Scale 必须大于 0。"
        )

    __MUZI_MAYA_JNT_PROTECTED_00001__(
        scale
    )
    return scale


class Jnt(object):
    u"""单个 Maya Jnt 节点的专属操作对象。"""

    def __init__(self, jnt):
        u"""
        初始化当前对象，并准备运行时需要的状态和成员。

        Args:
            jnt (str):
                需要处理的 Maya Jnt 节点名称。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """

        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if jnt is None:
            raise RuntimeError(
                u"Jnt 节点不能为空。"
            )

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        jnt = str(jnt).strip()

        if not jnt:
            raise RuntimeError(
                u"Jnt 节点不能为空。"
            )

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not cmds.objExists(jnt):
            raise RuntimeError(
                u"Jnt 节点不存在：{}".format(
                    jnt
                )
            )

        node_type = cmds.nodeType(
            jnt
        )

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if node_type != __MUZI_MAYA_JNT_PROTECTED_00016__:
            raise RuntimeError(
                u"节点不是 Jnt：{} | type={}".format(
                    jnt,
                    node_type
                )
            )

        # -------------------------------------------------------------------------
        # Step 05：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.jnt = jnt

    # =========================================================================
    # Create
    # =========================================================================

    @staticmethod
    def create(
            name,
            position=None,
            rotation=None,
            parent=None,
            radius=None
    ):
        u"""
        创建一个 Jnt。

        position / rotation 都表示 World Space。
        rotation 表示普通 World Rotation，不表示 __MUZI_MAYA_JNT_PROTECTED_00015__。

        Args:
            name (str):
                创建或查询时使用的节点名称。
            position (list[float] | tuple[float, float, float]):
                Jnt / Transform 使用的 XYZ Position。
            rotation (list[float] | tuple[float, float, float]):
                Jnt / Transform 使用的 XYZ Rotation。
            parent (str):
                父级 Maya 节点名称。
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if name is None:
            raise RuntimeError(
                u"Jnt 名称不能为空。"
            )

        name = str(name).strip()

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not name:
            raise RuntimeError(
                u"Jnt 名称不能为空。"
            )

        if cmds.objExists(name):
            raise RuntimeError(
                u"节点已经存在：{}".format(
                    name
                )
            )

        if parent is not None:
            transform_utils.validate_transform(
                parent
            )

        # -------------------------------------------------------------------------
        # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        jnt = cmds.createNode(
            __MUZI_MAYA_JNT_PROTECTED_00017__,
            name=name
        )

        if parent is not None:
            jnt = hierarchy_utils.parent(
                jnt,
                parent
            )

        if position is not None:
            transform_utils.set_world_translation(
                jnt,
                position
            )

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if rotation is not None:
            transform_utils.set_world_rotation(
                jnt,
                rotation
            )

        if radius is not None:
            jnt_object = Jnt(
                jnt
            )
            jnt_object.set_radius(
                radius
            )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return jnt

    @staticmethod
    def create_at_object(
            obj,
            name,
            parent=None,
            match_rotation=True,
            radius=None
    ):
        u"""
        在指定 Transform / Jnt 的世界位置创建 Jnt。

        Args:
            obj (str):
                当前操作使用的 Maya DAG 节点或场景对象。
            name (str):
                创建或查询时使用的节点名称。
            parent (str):
                父级 Maya 节点名称。
            match_rotation (bool):
                根据目标 Transform 创建 Jnt 时是否同时匹配目标 Rotation。
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object:
            创建或构建完成后的 Maya / Rig 对象或 Build Result。
        """
        # -------------------------------------------------------------------------
        # Step 01：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        transform_utils.validate_transform(
            obj
        )

        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        position = snap_utils.get_item_world_position(
            obj
        )
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        rotation = None

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if match_rotation:
            rotation = transform_utils.get_world_rotation(
                obj
            )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return Jnt.create(
            name=name,
            position=position,
            rotation=rotation,
            parent=parent,
            radius=radius
        )

    # =========================================================================
    # Jnt Orient
    # =========================================================================

    def get_jnt_orient(self):
        u"""
        返回 [__MUZI_MAYA_JNT_PROTECTED_00006__, __MUZI_MAYA_JNT_PROTECTED_00009__, __MUZI_MAYA_JNT_PROTECTED_00012__]。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        attributes = [
            "__MUZI_MAYA_JNT_PROTECTED_00007__",
            "__MUZI_MAYA_JNT_PROTECTED_00010__",
            "__MUZI_MAYA_JNT_PROTECTED_00013__",
        ]
        jnt_orient = []

        for attribute in attributes:
            value = cmds.getAttr(
                "{}.{}".format(
                    self.jnt,
                    attribute
                )
            )
            jnt_orient.append(
                value
            )

        return jnt_orient

    def set_jnt_orient(self, jnt_orient):
        u"""
        设置 jntOrientXYZ。

        Args:
            jnt_orient (object):
                当前方法执行 Maya / Rig 操作时使用的 `jnt_orient` 数据。

        Returns:
            object:
            完成设置或应用后的目标对象 / 状态结果。

        Raises:
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if jnt_orient is None:
            raise ValueError(
                u"jnt_orient 必须包含 3 个数值。"
            )

        # -------------------------------------------------------------------------
        # Step 02：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            value_count = len(
                jnt_orient
            )
        except TypeError:
            raise ValueError(
                u"jnt_orient 必须包含 3 个数值。"
            )

        if value_count != 3:
            raise ValueError(
                u"jnt_orient 必须包含 3 个数值。"
            )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        attributes = [
            "__MUZI_MAYA_JNT_PROTECTED_00008__",
            "__MUZI_MAYA_JNT_PROTECTED_00011__",
            "__MUZI_MAYA_JNT_PROTECTED_00014__",
        ]

        index = 0

        # -------------------------------------------------------------------------
        # Step 04：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        while index < len(attributes):
            cmds.setAttr(
                "{}.{}".format(
                    self.jnt,
                    attributes[index]
                ),
                jnt_orient[index]
            )
            index += 1

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.jnt

    def clear_jnt_orient(self):
        u"""
        把当前 Jnt 的 jntOrientXYZ 清零。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        return self.set_jnt_orient(
            (0.0, 0.0, 0.0)
        )

    # =========================================================================
    # Display
    # =========================================================================

    def get_radius(self):
        u"""
        返回当前 Jnt 的 radius。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        return cmds.getAttr(
            self.jnt + ".radius"
        )

    def set_radius(self, radius):
        u"""
        设置当前 Jnt 的 radius。

        Args:
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object:
            完成设置或应用后的目标对象 / 状态结果。

        Raises:
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        try:
            radius = float(
                radius
            )
        except (TypeError, ValueError):
            raise ValueError(
                u"Jnt radius 必须是数值。"
            )

        if radius < 0.0:
            raise ValueError(
                u"Jnt radius 不能小于 0。"
            )

        cmds.setAttr(
            self.jnt + ".radius",
            radius
        )

        return self.jnt

    def is_axis_visible(self):
        u"""
        返回当前 Jnt 的 Local Rotation Axis 是否显示。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        return bool(
            cmds.getAttr(
                self.jnt + ".displayLocalAxis"
            )
        )

    def show_axis(self):
        u"""
        显示当前 Jnt 的 Local Rotation Axis。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        cmds.setAttr(
            self.jnt + ".displayLocalAxis",
            1
        )

        return self.jnt

    def hide_axis(self):
        u"""
        隐藏当前 Jnt 的 Local Rotation Axis。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        cmds.setAttr(
            self.jnt + ".displayLocalAxis",
            0
        )

        return self.jnt

    # =========================================================================
    # Jnt Property
    # =========================================================================

    def get_scale_compensate(self):
        u"""
        返回当前 Jnt 的 segmentScaleCompensate 状态。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        return bool(
            cmds.getAttr(
                self.jnt + ".segmentScaleCompensate"
            )
        )

    def set_scale_compensate(self, enabled=True):
        u"""
        设置当前 Jnt 的 segmentScaleCompensate。

        Args:
            enabled (bool):
                当前 UI 控件或 Rig 功能是否启用。

        Returns:
            object:
            完成设置或应用后的目标对象 / 状态结果。
        """
        cmds.setAttr(
            self.jnt + ".segmentScaleCompensate",
            bool(enabled)
        )

        return self.jnt

    # =========================================================================
    # Orient
    # =========================================================================

    def orient(
            self,
            primary_axis="xyz",
            secondary_axis="xup"
    ):
        u"""
        根据直接 Child Jnt 整理当前 Jnt Orient。

        Args:
            primary_axis (str):
                当前 Maya / Rig 操作使用的 `primary_axis` 名称或标记。
            secondary_axis (str):
                当前 Maya / Rig 操作使用的 `secondary_axis` 名称或标记。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        children = hierarchy_utils.get_children(
            self.jnt,
            node_type=__MUZI_MAYA_JNT_PROTECTED_00018__,
            full_path=True
        )

        if not children:
            __MUZI_MAYA_JNT_PROTECTED_00002__(
                self.jnt,
                edit=True,
                __MUZI_MAYA_JNT_PROTECTED_00004__="none"
            )
            return self.jnt

        __MUZI_MAYA_JNT_PROTECTED_00003__(
            self.jnt,
            edit=True,
            zeroScaleOrient=True,
            __MUZI_MAYA_JNT_PROTECTED_00005__=primary_axis,
            secondaryAxisOrient=secondary_axis
        )

        return self.jnt

    # =========================================================================
    # Label
    # =========================================================================

    def set_label(
            self,
            side=0,
            label_type=18,
            other_type=""
    ):
        u"""
        设置 Maya Jnt Label。

        Args:
            side (int):
                方向标记，常用值为 lf、rt 或 md。
            label_type (int):
                当前 Maya / Rig 操作使用的 `label_type` 整数参数。
            other_type (str):
                当前 Maya / Rig 操作使用的 `other_type` 名称或标记。

        Returns:
            dict:
            包含本次构建、查询或处理结果的结构化字典。

        Raises:
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        side = int(
            side
        )
        label_type = int(
            label_type
        )

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if side not in [0, 1, 2]:
            raise ValueError(
                u"Jnt Label side 只能是 0 / 1 / 2。"
            )

        if other_type is None:
            other_type = ""

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        other_type = str(
            other_type
        )

        cmds.setAttr(
            self.jnt + ".side",
            side
        )
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        cmds.setAttr(
            self.jnt + ".type",
            label_type
        )
        cmds.setAttr(
            self.jnt + ".otherType",
            other_type,
            type="string"
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return {
            __MUZI_MAYA_JNT_PROTECTED_00019__: self.jnt,
            "side": side,
            "type": label_type,
            "otherType": other_type,
        }

    def tag(self):
        u"""
        根据项目标准 Jnt 名称生成 Maya Jnt Label。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        short_name = rename_utils.get_short_name(
            self.jnt
        )
        name_parts = short_name.split(
            "_"
        )

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if len(name_parts) < 3:
            raise RuntimeError(
                u"Jnt 名称格式不正确：{}".format(
                    short_name
                )
            )

        side_name = name_parts[1].lower()

        if side_name in [
                "l",
                "lf",
        ]:
            side_index = 1
        elif side_name in [
                "r",
                "rt",
        ]:
            side_index = 2
        else:
            side_index = 0

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        description_parts = []
        index = 2

        # -------------------------------------------------------------------------
        # Step 04：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        while index < len(name_parts):
            part = name_parts[index]
            is_last_part = index == len(name_parts) - 1
            is_index = len(part) == 3 and part.isdigit()

            if not (is_last_part and is_index):
                description_parts.append(
                    part
                )

            index += 1

        description = "_".join(
            description_parts
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.set_label(
            side=side_index,
            label_type=18,
            other_type=description
        )


__all__ = [
    "get_display_scale",
    "set_display_scale",
    __MUZI_MAYA_JNT_PROTECTED_00020__,
]
