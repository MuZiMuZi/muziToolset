# coding=utf-8
u"""
transform_utils：Maya Transform 基础工具。

方法介绍与使用场景：

    Transform.__init__
        创建一个 Transform 工具对象，并保存需要操作的 Maya 节点。
        适合后续统一处理 Transform、Joint、Controller、Guide、Group 等节点。

    Transform.match_transform
        将当前对象对齐到指定目标对象的位置、旋转和缩放。
        适合 Guide 对齐、Joint 对齐、Controller Group 对齐等场景。

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

        object(str/PyNode): 需要操作的 Maya 节点，可以是 Transform、Joint、Shape 等节点。

        Maya 使用示例：

        from muziToolset.core.common import transform_utils

        object = "ctrl_lf_eye_main_001"

        transform_object = transform_utils.Transform(object)

        print(transform_object.object)
        """

        self.object = None
        self.world_matrix = None

        # 如果传入 Maya 节点，则统一转换成 PyNode 保存。
        if object:
            self.object = pm.PyNode(object)

    def match_transform(self, target, position=True, rotation=True, scale=True):
        u"""
        将当前对象对齐到指定目标对象。

        target(str/PyNode): 需要匹配的目标对象。
        position(bool): 是否匹配目标对象的位置，默认 True。
        rotation(bool): 是否匹配目标对象的旋转，默认 True。
        scale(bool): 是否匹配目标对象的缩放，默认 True。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import transform_utils

        object = "jnt_lf_arm_bind_001"
        target = "guide_lf_arm_001"

        transform_object = transform_utils.Transform(object)
        transform_object.match_transform(target, position=True, rotation=True, scale=False)
        """

        # 将目标对象转换成 PyNode，统一使用 PyMEL 节点对象进行操作。
        target = pm.PyNode(target)

        # 根据给定开关匹配目标对象的位置、旋转和缩放。
        pm.matchTransform(self.object, target, position=position, rotation=rotation, scale=scale)

    def get_world_matrix(self):
        u"""
        获取当前对象的世界矩阵。

        Returns:
            Matrix: 当前对象的世界矩阵。

        Maya 使用示例：

        from muziToolset.core.common import transform_utils

        object = "ctrl_lf_eye_main_001"

        transform_object = transform_utils.Transform(object)
        world_matrix = transform_object.get_world_matrix()

        print(world_matrix)
        """

        # 获取对象的世界矩阵，并保存到当前实例中。
        self.world_matrix = self.object.getMatrix(worldSpace=True)

        return self.world_matrix

    def set_world_matrix(self, matrix):
        u"""
        将给定的世界矩阵设置到当前对象。

        matrix(Matrix): 需要设置给当前对象的世界矩阵。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import transform_utils

        source = transform_utils.Transform("guide_lf_arm_001")
        target = transform_utils.Transform("jnt_lf_arm_bind_001")

        matrix = source.get_world_matrix()

        target.set_world_matrix(matrix)
        """

        # 将给定矩阵设置到当前对象的世界空间。
        self.object.setMatrix(matrix, worldSpace=True)

        # 保存最近一次设置的世界矩阵，方便后续继续使用。
        self.world_matrix = matrix

    def reset_transform(self, translate=True, rotate=True, scale=True):
        u"""
        将当前对象的 Transform 数值恢复到默认状态。

        translate(bool): 是否将 translate 重置为 (0, 0, 0)，默认 True。
        rotate(bool): 是否将 rotate 重置为 (0, 0, 0)，默认 True。
        scale(bool): 是否将 scale 重置为 (1, 1, 1)，默认 True。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import transform_utils

        object = "ctrl_lf_eye_main_001"

        transform_object = transform_utils.Transform(object)
        transform_object.reset_transform(translate=True, rotate=True, scale=True)
        """

        # 重置位移数值。
        if translate:
            self.object.translate.set((0, 0, 0))

        # 重置旋转数值。
        if rotate:
            self.object.rotate.set((0, 0, 0))

        # 重置缩放数值。
        if scale:
            self.object.scale.set((1, 1, 1))

    def get_transform(self):
        u"""
        获取当前对象对应的 Transform 节点。

        如果当前对象本身就是 Transform，则直接返回当前对象。
        如果当前对象是 Shape，则返回它的父 Transform。

        Returns:
            PyNode: 当前对象对应的 Transform 节点。

        Maya 使用示例：

        from muziToolset.core.common import transform_utils

        object = "ctrl_lf_eye_main_001Shape"

        transform_object = transform_utils.Transform(object)
        transform = transform_object.get_transform()

        print(transform)
        # ctrl_lf_eye_main_001
        """

        # 如果当前对象本身就是 Transform 或 Transform 的子类型，则直接返回。
        if isinstance(self.object, pm.nodetypes.Transform):
            return self.object

        # Shape 节点通常位于 Transform 节点下面，因此获取它的父节点。
        parent_object = self.object.getParent()

        return parent_object
