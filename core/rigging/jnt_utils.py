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

    Jnt.match_transform
        将当前 Joint 对齐到指定目标的位置和旋转。
        适合将 Joint 对齐到 Guide、Locator 或其他 Transform 节点。

    Jnt.set_radius
        设置当前 Joint 的显示半径。
        适合统一调整 Joint 在 Maya 视图中的显示大小。

    Jnt.reset_joint_orient
        将当前 Joint 的 jointOrient 清零。
        适合重新计算 Joint 方向或清理已有 Joint Orient 数据。
"""

import pymel.core as pm
from ..common import transform_utils


class Jnt(object):

    def __init__(self, name):
        u"""
        初始化 Joint 工具对象。

        如果 Maya 场景中已经存在指定名称的 Joint，则直接将它作为当前 Joint。
        如果不存在，则自动创建一个新的 Joint。

        这样后续所有方法都可以直接使用 self.jnt，不需要重复判断 Joint 是否存在。

        name(str): Joint 名称。

        Maya 使用示例：

        from muziToolset.core.rigging import jnt_utils

        jnt_object = jnt_utils.Jnt("jnt_lf_arm_bind_001")

        print(jnt_object.jnt)
        """

        # 保存 Joint 标准名称。
        self.jnt_name = name

        # 保存 Joint PyNode。
        # _get_or_create_jnt() 执行完成后，该属性一定会指向一个有效 Joint。
        self.jnt = None

        # 根据名称获取或创建 Joint。
        self._get_or_create_jnt()

    def _get_or_create_jnt(self):
        u"""
        根据 self.jnt_name 获取或创建当前 Joint。

        如果 Maya 场景中已经存在同名对象，则直接转换成 PyNode 使用。
        如果同名对象存在但不是 Joint，则抛出错误，避免把错误节点当作 Joint。
        如果场景中不存在同名对象，则创建一个新的 Joint。

        Returns:
            PyNode: 当前 Joint 节点。

        Maya 使用示例：

        from muziToolset.core.rigging import jnt_utils

        jnt_object = jnt_utils.Jnt("jnt_lf_arm_bind_001")
        jnt = jnt_object._get_or_create_jnt()

        print(jnt)
        """

        # 判断场景中是否已经存在这个名称的 Maya 节点。
        if pm.objExists(self.jnt_name):

            # 已经存在时直接转换成 PyNode，后续统一使用 PyMEL 对象操作。
            self.jnt = pm.PyNode(self.jnt_name)

            # 同名对象必须是 Joint。
            if not isinstance(self.jnt, pm.nodetypes.Joint):
                raise TypeError(u"{} 已经存在，但不是 Joint 节点。".format(self.jnt_name))

        else:

            # 清空 Maya 当前选择，避免新 Joint 自动成为其他已选 Joint 的子节点。
            pm.select(clear=True)

            # 场景中不存在时创建新的 Joint。
            self.jnt = pm.joint(name=self.jnt_name)

        return self.jnt

    def set_match_transform(self, target,position=True,rotation=True):
        u"""
        将当前 Joint 对齐到指定目标的位置和旋转。

        target(str/PyNode): 需要对齐的目标对象，例如 Guide、Locator 或 Transform。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import jnt_utils

        jnt_object = jnt_utils.Jnt("jnt_lf_arm_bind_001")
        target = "guide_lf_arm_001"

        jnt_object.match_transform(target)
        """
        jnt_object = transform_utils.Transform(self.jnt)
        jnt_object.match_transform(target, position=position, rotation=rotation)

    def set_radius(self, radius):
        u"""
        设置当前 Joint 的显示半径。

        radius(float): Joint 的显示半径数值。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import jnt_utils

        jnt_object = jnt_utils.Jnt("jnt_lf_arm_bind_001")
        radius = 0.5

        jnt_object.set_radius(radius)
        """

        # radius 是 Joint 自身属性，可以直接通过 PyNode 设置。
        self.jnt.radius.set(radius)

    def reset_joint_orient(self):
        u"""
        清除当前 Joint 的关节定向数值。

        将 jointOrientX、jointOrientY、jointOrientZ 一次性设置为 0。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import jnt_utils

        jnt_object = jnt_utils.Jnt("jnt_lf_arm_bind_001")

        jnt_object.reset_joint_orient()
        """

        # jointOrient 是一个三维复合属性，可以一次性设置 XYZ 三个轴。
        self.jnt.jointOrient.set((0, 0, 0))
