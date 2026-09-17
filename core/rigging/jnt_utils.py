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

import pymel.core as pm


class Jnt(object):

    def __init__(self, name):
        u"""
        初始化 Joint 工具对象。

        如果 Maya 场景中已经存在指定名称的 Joint，则直接使用；
        不存在时创建新的 Joint。

        Args:
            name(str): Joint 名称。
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
            PyNode: 当前 Joint 节点。
        """

        # 已经存在同名节点时直接获取。
        if pm.objExists(self.jnt_name):
            self.jnt = pm.PyNode(self.jnt_name)

            # 同名节点必须是真正的 Joint。
            if not isinstance(self.jnt, pm.nodetypes.Joint):
                raise TypeError(u"{} 已经存在，但不是 Joint 节点。".format(self.jnt_name))

        else:
            # 创建 Joint 前清空选择，避免 Maya 自动把新 Joint 挂到当前选择的 Joint 下方。
            pm.select(clear=True)
            self.jnt = pm.joint(name=self.jnt_name)

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
            target(str/PyNode): 需要吸附的 Guide / Locator。
            position(bool): 是否匹配位置，默认 True。
            rotation(bool): 是否匹配旋转，默认 True。

        Returns:
            None
        """

        # Joint 直接吸附 Locator Transform。
        pm.matchTransform(
            self.jnt,
            target,
            position=position,
            rotation=rotation
        )

    def set_radius(self, radius):
        u"""
        设置当前 Joint 的显示半径。

        Args:
            radius(float): Joint 显示半径。

        Returns:
            None
        """

        self.jnt.radius.set(radius)

    def reset_joint_orient(self):
        u"""
        将当前 Joint 的 jointOrient XYZ 清零。

        Returns:
            None
        """

        self.jnt.jointOrient.set((0, 0, 0))
