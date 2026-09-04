# coding=utf-8
u"""
jnt_utils：Maya Joint 基础工具。

方法介绍与使用场景：

    Jnt.__init__
        创建一个 Joint 工具对象。
        可以传入新的 Joint 名称，也可以传入场景中已经存在的 Joint。

    Jnt.create_jnt
        根据给定名称创建一个新的 Joint。
        适合 Guide 转 Joint、程序化创建骨骼等场景。

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


class Jnt(object):

    def __init__(self, name=None, jnt=None):
        u"""
        初始化 Joint 工具对象。

        name(str): 需要创建的新 Joint 名称。
        jnt(str/PyNode): 场景中已经存在的 Joint 节点。

        Maya 使用示例：

        from muziToolset.core.rigging import jnt_utils

        jnt_object = jnt_utils.Jnt(name="jnt_lf_arm_bind_001")

        # 或者读取场景中已经存在的 Joint。
        jnt_object = jnt_utils.Jnt(jnt="jnt_lf_arm_bind_001")
        """

        self.name = name
        self.jnt = None

        # 如果传入已经存在的 Joint，则直接转换成 PyNode 保存。
        if jnt:
            self.jnt = pm.PyNode(jnt)

    def create_jnt(self):
        u"""
        根据当前 name 创建一个新的 Joint，并保存到 self.jnt。

        Returns:
            PyNode: 新创建的 Joint 节点。

        Maya 使用示例：

        from muziToolset.core.rigging import jnt_utils

        jnt_object = jnt_utils.Jnt(name="jnt_lf_arm_bind_001")
        new_jnt = jnt_object.create_jnt()

        print(new_jnt)
        """

        # 创建 Joint，PyMEL 会直接返回 Joint 的 PyNode。
        self.jnt = pm.joint(name=self.name)

        return self.jnt

    def match_transform(self, target):
        u"""
        将当前 Joint 对齐到指定目标的位置和旋转。

        target(str/PyNode): 需要对齐的目标对象，例如 Guide、Locator 或 Transform。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import jnt_utils

        jnt_object = jnt_utils.Jnt(jnt="jnt_lf_arm_bind_001")
        target = "guide_lf_arm_001"

        jnt_object.match_transform(target)
        """

        # 将目标对象转换成 PyNode，方便后续统一使用 PyMEL 操作。
        target = pm.PyNode(target)

        # 匹配目标对象的位置和旋转。
        pm.matchTransform(self.jnt, target, position=True, rotation=True)

    def set_radius(self, radius):
        u"""
        设置当前 Joint 的显示半径。

        radius(float): Joint 的显示半径数值。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import jnt_utils

        jnt_object = jnt_utils.Jnt(jnt="jnt_lf_arm_bind_001")
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

        jnt_object = jnt_utils.Jnt(jnt="jnt_lf_arm_bind_001")

        jnt_object.reset_joint_orient()
        """

        # jointOrient 是一个三维复合属性，可以一次性设置 XYZ 三个轴。
        self.jnt.jointOrient.set((0, 0, 0))
