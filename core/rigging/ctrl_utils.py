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

    Ctrl.get_ctrl_shapes
        获取当前控制器下面的全部 Shape 节点。
        适合统一修改多 Shape 控制器的颜色、大小和 Curve CV。

    Ctrl.set_ctrl_color
        设置当前控制器全部 Shape 的显示颜色。
        适合按照左右侧或不同控制器功能统一设置显示颜色。

    Ctrl.set_ctrl_size
        通过缩放全部 NurbsCurve Shape 的 CV 修改控制器显示大小。
        适合调整多 Shape 控制器视觉尺寸，同时保持 Transform Scale 为默认值。

    Ctrl.set_ctrl_shape
        从 Controller Shape Library 读取 JSON 数据并替换当前控制器 Shape。
        适合创建或切换 circle、cube、ball 等控制器形状。
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

        # 保存当前控制器下面的全部 Shape PyNode。
        self.ctrl_shapes = []

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

    def get_ctrl_shapes(self):
        u"""
        获取当前控制器下面的全部 Shape 节点。

        一个 Controller Transform 可以同时拥有一个或多个 NurbsCurve Shape。
        统一返回 Shape 列表后，颜色、大小等操作可以同时作用于整个控制器。

        Returns:
            list: 当前控制器下面的全部 Shape PyNode。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl(ctrl="ctrl_lf_eye_main_001")
        ctrl_shapes = ctrl_object.get_ctrl_shapes()

        print(ctrl_shapes)
        """

        # 获取控制器 Transform 下面的全部非 Intermediate Shape 节点。
        self.ctrl_shapes = self.ctrl.getShapes(noIntermediate=True)

        return self.ctrl_shapes

    def set_ctrl_color(self, ctrl_color):
        u"""
        设置当前控制器全部 Shape 的显示颜色。

        该方法使用 Maya Drawing Overrides 的索引颜色设置控制器颜色。
        如果一个控制器包含多个 Shape，会依次修改每一个 Shape。

        ctrl_color(int): Maya Override Color 的颜色索引值。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl(ctrl="ctrl_lf_eye_main_001")
        ctrl_object.set_ctrl_color(6)
        """

        # 获取控制器下面的全部 Shape。
        self.ctrl_shapes = self.get_ctrl_shapes()

        # 逐个设置 Shape 的 Drawing Overrides 和颜色。
        for ctrl_shape in self.ctrl_shapes:
            ctrl_shape.overrideEnabled.set(True)
            ctrl_shape.overrideColor.set(ctrl_color)

    def set_ctrl_size(self, ctrl_size):
        u"""
        设置当前控制器全部 NurbsCurve Shape 的显示大小。

        该方法直接缩放 Curve Shape 的所有 CV，不修改控制器 Transform 的 Scale。
        因此控制器的 scaleX、scaleY、scaleZ 可以继续保持为 1。
        如果一个控制器包含多个 NurbsCurve Shape，会依次缩放每一个 Shape。

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

        # 获取控制器下面的全部 Shape。
        self.ctrl_shapes = self.get_ctrl_shapes()

        # 逐个检查 Shape，只对 NurbsCurve 的 CV 进行缩放。
        for ctrl_shape in self.ctrl_shapes:
            if isinstance(ctrl_shape, pm.nodetypes.NurbsCurve):
                pm.scale(ctrl_shape.cv[:], ctrl_size, ctrl_size, ctrl_size, relative=True, objectSpace=True)

    def set_ctrl_shape(self, shape_name):
        u"""
        根据 Shape Library 中的 JSON 文件替换当前控制器的 Curve Shape。

        一个 JSON 文件可以保存一个或多个 NurbsCurve Shape。
        方法会先读取 JSON 数据并创建临时 Curve，然后删除当前控制器旧 Shape，
        最后把新 Curve Shape 移到当前控制器 Transform 下面。

        shape_name(str): Controller Shape 名称，例如 "circle"、"cube"、"ball"。

        Returns:
            list: 新创建并挂到当前控制器下面的 NurbsCurve Shape 节点列表。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl(name="ctrl_lf_eye_main_001")
        ctrl_object.create_ctrl()

        ctrl_shapes = ctrl_object.set_ctrl_shape("cube")

        print(ctrl_shapes)
        """

        # 获取 muziToolset 项目根目录。
        rigging_path = os.path.dirname(__file__)
        core_path = os.path.dirname(rigging_path)
        project_path = os.path.dirname(core_path)

        # 拼接 Controller Shape JSON 文件路径。
        shape_file = os.path.join(project_path, "resources", "controller_shapes", shape_name + ".json")

        # Shape 文件不存在时停止执行，避免删除当前控制器已有 Shape。
        if not os.path.exists(shape_file):
            pm.warning(u"找不到 Controller Shape 文件：{}".format(shape_file))
            return []

        # 读取 JSON 中保存的 Controller Shape 数据。
        with open(shape_file, "r") as file:
            shape_data = json.load(file)

        # 临时保存根据 JSON 创建出来的 Curve Transform。
        curve_transforms = []

        # 一个 JSON 文件可能包含多个 Curve Shape，所以逐个创建临时 Curve。
        for shape_info in shape_data:
            point_values = shape_info["points"]
            degree = shape_info["degree"]
            periodic = shape_info["periodic"]
            knot = shape_info["knot"]

            # JSON 中 points 使用一维数组保存 XYZ，需要每三个数重新组合成一个点。
            points = []

            for index in range(0, len(point_values), 3):
                point = (
                    point_values[index],
                    point_values[index + 1],
                    point_values[index + 2]
                )
                points.append(point)

            # Periodic Curve 需要在点列表末尾重复最前面的 degree 个点。
            if periodic:
                for index in range(degree):
                    points.append(points[index])

            # 根据 JSON 保存的 CV、Degree、Knot 和 Periodic 状态创建临时 Curve。
            curve_transform = pm.curve(point=points, degree=degree, knot=knot, periodic=periodic)
            curve_transforms.append(curve_transform)

        # 获取当前控制器原来的全部 Shape。
        old_shapes = self.get_ctrl_shapes()

        # 删除旧 Shape，只保留当前 Controller Transform。
        for old_shape in old_shapes:
            pm.delete(old_shape)

        # 保存最终挂到 Controller Transform 下面的新 Shape。
        new_shapes = []

        # 将每一个临时 Curve Shape 移到当前 Controller Transform 下面。
        for curve_transform in curve_transforms:
            curve_shape = curve_transform.getShape()
            pm.parent(curve_shape, self.ctrl, shape=True, relative=True)
            new_shapes.append(curve_shape)

            # Shape 已经移动完成，删除空的临时 Curve Transform。
            pm.delete(curve_transform)

        # 更新当前实例保存的 Shape 列表。
        self.ctrl_shapes = new_shapes

        return self.ctrl_shapes
