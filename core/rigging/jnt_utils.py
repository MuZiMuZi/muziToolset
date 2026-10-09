# coding=utf-8
u"""
jnt_utils：Maya Joint 基础工具。

方法介绍与使用场景：

    Jnt.__init__
        创建一个 Joint 工具对象。
        传入 Joint 名称后，如果场景中已经存在同名 Joint，则直接使用；
        如果不存在，则自动创建该名称的 Joint。

    Jnt._get_or_create_jnt
        根据名称获取或创建 Joint。
        作为 Jnt 类内部统一保证 self.jnt 有效的基础方法。

    Jnt.set_match_transform
        将当前 Joint 直接吸附到指定 Guide / Locator 的 Transform。
        Joint 的位置和旋转直接使用 Locator Transform，不读取 Locator Shape 的额外偏移。

    Jnt.set_radius
        设置当前 Joint 的显示半径。

    Jnt.reset_joint_orient
        将当前 Joint 的 jointOrient 清零。
"""



import maya.cmds as cmds
from ..common import hierarchy_utils
from ..common import rename_utils
from ..rigging import snap_utils
from ..common import transform_utils



class Jnt(object):

    def __init__(self, name):
        u"""
        初始化 Joint 工具对象。

        如果 Maya 场景中已经存在指定名称的 Joint，则直接使用；
        不存在时创建新的 Joint。

        Args:
            name (str):
                Joint 名称。
        """

        # 保存 Joint 的稳定名称。
        self.jnt_name = name

        # 保存 Maya Joint 对象。
        self.jnt = None

        # 根据名称获取或创建 Joint。
        self._get_or_create_jnt()

    def _get_or_create_jnt(self):
        u"""
        根据 self.jnt_name 获取或创建当前 Joint。

        场景中已经存在同名 Joint 时直接复用；
        不存在时创建新的 Joint。

        Returns:
            字符串节点名称: 当前 Joint 节点。
        """

        # 已经存在同名节点时直接获取。
        if cmds.objExists(self.jnt_name):
            self.jnt = str(self.jnt_name)

            # 同名节点必须是真正的 Joint。
            if not cmds.nodeType(self.jnt) == "joint":
                raise TypeError(u"{} 已经存在，但不是 Joint 节点。".format(self.jnt_name))

        else:
            # 创建 Joint 前清空选择，避免 Maya 自动把新 Joint 挂到当前选择的 Joint 下方。
            cmds.select(clear=True)
            self.jnt = cmds.joint(name=self.jnt_name)

        return self.jnt

    def set_match_transform(self, target, position=True, rotation=True):
        u"""
        将当前 Joint 直接吸附到指定 Guide / Locator。

        Guide 系统统一使用 Locator Transform 保存真正的定位数据。
        因此这里直接执行 matchTransform：
            Locator Transform
                    ↓
                 Joint
        不读取 Locator Shape.localPosition，也不额外计算 worldPosition。
        这样 Joint 的创建规则始终保持简单、明确。

        Args:
            target (str/字符串节点名称):
                需要吸附的 Guide / Locator。
            position (bool):
                是否匹配位置，默认 True。
            rotation (bool):
                是否匹配旋转，默认 True。

        Returns:
            None
        """

        # Joint 直接吸附 Locator Transform。
        cmds.matchTransform(
            self.jnt,
            target,
            position=position,
            rotation=rotation
        )

    def set_radius(self, radius):
        u"""
        设置当前 Joint 的显示半径。

        Args:
            radius (float):
                Joint 显示半径。

        Returns:
            None
        """

        cmds.setAttr(self.jnt + ".radius", radius)

    def reset_joint_orient(self):
        u"""
        将当前 Joint 的 jointOrient XYZ 清零。

        Returns:
            None
        """

        cmds.setAttr(self.jnt + ".jointOrient", 0, 0, 0)

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
        rotation 表示普通 World Rotation，不表示 jointOrient。

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
            "joint",
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

    def get_jnt_orient(self):
        u"""
        返回 [jointOrientX, jointOrientY, jointOrientZ]。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        attributes = [
            "jointOrientX",
            "jointOrientY",
            "jointOrientZ",
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
            "jointOrientX",
            "jointOrientY",
            "jointOrientZ",
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
            node_type="joint",
            full_path=True
        )

        if not children:
            cmds.joint(
                self.jnt,
                edit=True,
                orientJoint="none"
            )
            return self.jnt

        cmds.joint(
            self.jnt,
            edit=True,
            zeroScaleOrient=True,
            orientJoint=primary_axis,
            secondaryAxisOrient=secondary_axis
        )

        return self.jnt

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
            "joint": self.jnt,
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
