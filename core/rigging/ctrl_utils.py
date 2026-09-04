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

import os
import json

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


    def set_ctrl_shape (self , shape_name) :
        u"""
        根据 Shape Library 中的 JSON 文件替换当前控制器的 Curve Shape。

        shape_name(str): Controller Shape 名称，例如 "circle"、"cube"、"ball"。

        Returns:
            list: 新创建的 NurbsCurve Shape 节点列表。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl(name="ctrl_lf_eye_main_001")
        ctrl_object.create_ctrl()

        ctrl_object.set_ctrl_shape("cube")
        """

        # 获取 muziToolset 项目根目录。
        rigging_path = os.path.dirname (__file__)
        core_path = os.path.dirname (rigging_path)
        project_path = os.path.dirname (core_path)

        # 拼接 Controller Shape JSON 文件路径。
        shape_file = os.path.join (
            project_path ,
            "resources" ,
            "controller_shapes" ,
            shape_name + ".json"
        )

        # 检查 Shape 文件是否存在。
        if not os.path.exists (shape_file) :
            pm.warning (u"找不到 Controller Shape 文件：{}".format (shape_file))
            return []

        # 读取 JSON 数据。
        with open (shape_file , "r") as file :
            shape_data = json.load (file)

        # 临时保存通过 JSON 创建出来的 Curve Transform。
        curve_transforms = []

        # 一个 JSON 文件可能包含多个 Curve Shape。
        for shape_info in shape_data :

            point_values = shape_info ["points"]
            degree = shape_info ["degree"]
            periodic = shape_info ["periodic"]
            knot = shape_info ["knot"]

            # 将一维 points 数据恢复成 Maya Curve 使用的 XYZ 点。
            points = []

            for index in range (0 , len (point_values) , 3) :
                point = (
                    point_values [index] ,
                    point_values [index + 1] ,
                    point_values [index + 2]
                )

                points.append (point)

            # Periodic Curve 需要重复前 degree 个点。
            if periodic :

                for index in range (degree) :
                    points.append (points [index])

            # 根据 JSON 数据创建临时 Curve。
            curve_transform = pm.curve (
                point = points ,
                degree = degree ,
                knot = knot ,
                periodic = periodic
            )

            curve_transforms.append (curve_transform)

        # 获取 Controller 原来的 Shape。
        old_shapes = self.ctrl.getShapes (noIntermediate = True)

        # 删除旧 Shape。
        for old_shape in old_shapes :
            pm.delete (old_shape)

        # 保存最终的新 Shape。
        new_shapes = []

        # 将临时 Curve 的 Shape 移到 Controller Transform 下面。
        for curve_transform in curve_transforms :
            curve_shape = curve_transform.getShape ()

            pm.parent (curve_shape , self.ctrl , shape = True , relative = True)

            new_shapes.append (curve_shape)

            # Shape 已经移动到 Controller 下面，
            # 所以原来的临时 Transform 可以删除。
            pm.delete (curve_transform)

        # 保持当前类原来的 self.ctrl_shape 设计。
        if new_shapes :
            self.ctrl_shape = new_shapes [0]

        return new_shapes
