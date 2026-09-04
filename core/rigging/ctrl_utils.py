# coding=utf-8
u"""
ctrl_utils：Maya Controller 基础工具。

方法介绍与使用场景：

    Ctrl.__init__
        创建一个 Controller 工具对象。
        可以传入新的控制器名称，也可以传入场景中已经存在的控制器。

    Ctrl.create_ctrl
        创建一个基础圆形控制器。
        适合程序化创建 FK、Face、Eye 等基础绑定控制器。

    Ctrl.get_ctrl_shape
        获取当前控制器下面的 Curve Shape 节点。
        适合后续修改控制器颜色、大小和 Curve CV。

    Ctrl.set_ctrl_color
        设置当前控制器 Curve Shape 的显示颜色。
        适合按照左右侧或不同控制器功能统一设置显示颜色。

    Ctrl.set_ctrl_size
        通过缩放 Curve CV 修改控制器的显示大小。
        适合调整控制器视觉尺寸，同时保持 Transform Scale 为默认值。
"""

import pymel.core as pm


class Ctrl(object):

    def __init__(self, name=None, ctrl=None):
        u"""
        初始化 Controller 工具对象。

        name(str): 需要创建的新控制器名称。
        ctrl(str/PyNode): 场景中已经存在的控制器 Transform 节点。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        # 准备创建一个新的控制器。
        ctrl_object = ctrl_utils.Ctrl(name="ctrl_lf_eye_main_001")

        # 或者读取场景中已经存在的控制器。
        ctrl_object = ctrl_utils.Ctrl(ctrl="ctrl_lf_eye_main_001")
        """

        # 保存新控制器创建时使用的名称。
        self.name = name

        # 保存当前控制器的 Transform PyNode。
        self.ctrl = None

        # 保存当前控制器的 Curve Shape PyNode。
        self.ctrl_shape = None

        # 如果传入已经存在的控制器，则直接转换成 PyNode 保存。
        if ctrl:
            self.ctrl = pm.PyNode(ctrl)

    def create_ctrl(self, radius=1.0):
        u"""
        创建一个基础圆形控制器，并保存到 self.ctrl。

        创建出的控制器默认位于世界原点，圆形平面朝向 Y 轴。

        radius(float): 创建圆形控制器时使用的初始半径，默认 1.0。

        Returns:
            PyNode: 新创建的控制器 Transform 节点。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl(name="ctrl_lf_eye_main_001")
        ctrl = ctrl_object.create_ctrl(radius=1.0)

        print(ctrl)
        """

        # pm.circle 返回一个列表，第一个元素是新创建的控制器 Transform。
        self.ctrl = pm.circle(name=self.name, radius=radius, normal=(0, 1, 0))[0]

        return self.ctrl

    def get_ctrl_shape(self):
        u"""
        获取当前控制器下面的 Curve Shape 节点。

        当前基础控制器只处理一个 Curve Shape，因此使用 getShape() 获取第一个 Shape。

        Returns:
            PyNode: 当前控制器下面的 Curve Shape 节点。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl(ctrl="ctrl_lf_eye_main_001")
        ctrl_shape = ctrl_object.get_ctrl_shape()

        print(ctrl_shape)
        """

        # 获取控制器 Transform 下面的第一个 Shape 节点。
        self.ctrl_shape = self.ctrl.getShape()

        return self.ctrl_shape

    def set_ctrl_color(self, ctrl_color):
        u"""
        设置当前控制器 Curve Shape 的显示颜色。

        该方法使用 Maya Drawing Overrides 的索引颜色设置控制器颜色。

        ctrl_color(int): Maya Override Color 的颜色索引值。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl(ctrl="ctrl_lf_eye_main_001")
        ctrl_object.set_ctrl_color(6)
        """

        # 获取控制器的 Curve Shape。
        self.ctrl_shape = self.get_ctrl_shape()

        # 开启 Shape 的 Drawing Overrides。
        self.ctrl_shape.overrideEnabled.set(True)

        # 设置 Shape 的 Override Color 索引值。
        self.ctrl_shape.overrideColor.set(ctrl_color)

    def set_ctrl_size(self, ctrl_size):
        u"""
        设置当前控制器 Curve Shape 的显示大小。

        该方法直接缩放 Curve Shape 的所有 CV，不修改控制器 Transform 的 Scale。
        因此控制器的 scaleX、scaleY、scaleZ 可以继续保持为 1。

        ctrl_size(float): 控制器 Shape 的相对缩放倍率。
                          例如 2.0 表示在当前大小基础上放大 2 倍，
                          0.5 表示在当前大小基础上缩小为一半。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl(ctrl="ctrl_lf_eye_main_001")
        ctrl_object.set_ctrl_size(2.0)
        """

        # 获取控制器的 Curve Shape。
        self.ctrl_shape = self.get_ctrl_shape()

        # 当前基础 Controller 只处理 NurbsCurve Shape。
        if isinstance(self.ctrl_shape, pm.nodetypes.NurbsCurve):

            # 获取 Curve 的全部 CV，并在对象自身空间中进行相对缩放。
            # 这里只修改 Shape CV，因此不会改变控制器 Transform 的 Scale 数值。
            pm.scale(self.ctrl_shape.cv[:], ctrl_size, ctrl_size, ctrl_size, relative=True, objectSpace=True)
