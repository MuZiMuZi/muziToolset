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

import pymel.core as pm


class Transform(object):

    def __init__(self, object=None):
        u"""
        初始化 Transform 工具对象。

        Args:
            object(str/PyNode): 需要操作的 Maya 节点，可以是 Transform、Joint、Shape 等节点。
        """

        self.object = None
        self.world_matrix = None

        # 如果传入 Maya 节点，则统一转换成 PyNode 保存。
        if object:
            self.object = pm.PyNode(object)

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
            target(str/PyNode): 需要匹配的目标对象。
            position(bool): 是否匹配目标位置，默认 True。
            rotation(bool): 是否匹配目标旋转，默认 True。
            scale(bool): 是否匹配目标缩放，默认 True。

        Returns:
            None
        """

        # 目标统一转换成 PyNode，然后直接使用 Maya matchTransform 对齐。
        target = pm.PyNode(target)

        pm.matchTransform(
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

        self.world_matrix = self.object.getMatrix(worldSpace=True)
        return self.world_matrix

    def set_world_matrix(self, matrix):
        u"""
        将给定的世界矩阵设置到当前对象。

        Args:
            matrix(list[float] | maya.api.OpenMaya.MMatrix):
                用于 Transform、Constraint 或空间计算的 4x4 Matrix 数据。

        Returns:
            None
        """

        self.object.setMatrix(matrix, worldSpace=True)
        self.world_matrix = matrix

    def reset_transform(self, translate=True, rotate=True, scale=True):
        u"""
        将当前对象的 Transform 数值恢复到默认状态。

        Args:
            translate(bool): 是否将 Translate 重置为 0。
            rotate(bool): 是否将 Rotate 重置为 0。
            scale(bool): 是否将 Scale 重置为 1。

        Returns:
            None
        """

        if translate:
            self.object.translate.set((0, 0, 0))

        if rotate:
            self.object.rotate.set((0, 0, 0))

        if scale:
            self.object.scale.set((1, 1, 1))

    def get_transform(self):
        u"""
        获取当前对象对应的 Transform 节点。

        如果当前对象本身就是 Transform，则直接返回当前对象；
        如果当前对象是 Shape，则返回它的父 Transform。

        Returns:
            PyNode: 当前对象对应的 Transform 节点。
        """

        if isinstance(self.object, pm.nodetypes.Transform):
            return self.object

        parent_object = self.object.getParent()
        return parent_object
