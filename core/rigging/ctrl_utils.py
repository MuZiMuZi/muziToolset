# coding=utf-8
u"""
ctrl_utils：Maya Controller 基础工具。

方法介绍与使用场景：

    Ctrl.__init__
        创建一个 Controller 工具对象。
        传入 Controller 名称后，如果场景中已经存在同名 Transform，则直接使用；
        如果不存在，则自动创建一个基础圆形 Controller。

    Ctrl._get_or_create_ctrl
        根据名称获取或创建 Controller Transform。
        作为 Ctrl 类内部统一保证 self.ctrl 有效的基础方法。

    Ctrl.create_ctrl
        设置当前 Controller 的 Shape、颜色、大小，并根据需要创建完整控制器层级。
        适合程序化创建 FK、Face、Eye 等绑定控制器。

    Ctrl.get_ctrl_shapes
        获取当前控制器下面的全部 Shape 节点。
        适合统一修改多 Shape 控制器的颜色、大小和 Curve CV。

    Ctrl.get_ctrl_shape_list
        获取 Controller Shape Library 中所有可用的 Shape 名称。
        适合给 UI 下拉菜单、Shape Picker 等功能提供资源列表。

    Ctrl.set_ctrl_color
        设置当前控制器全部 Shape 的显示颜色。
        适合按照左右侧或不同控制器功能统一设置显示颜色。

    Ctrl.set_ctrl_size
        通过缩放全部 NurbsCurve Shape 的 CV 修改控制器显示大小。
        适合调整多 Shape 控制器视觉尺寸，同时保持 Transform Scale 为默认值。

    Ctrl.set_ctrl_rotate
        通过旋转全部 NurbsCurve Shape 的 CV 修改控制器显示朝向。
        适合调整控制器图形方向，同时保持 Transform Rotate 为默认值。

    Ctrl.set_ctrl_offset
        通过移动全部 NurbsCurve Shape 的 CV 修改控制器显示位置。
        适合偏移控制器图形，同时保持 Transform Translate 为默认值。

    Ctrl.set_ctrl_shape
        从 Controller Shape Library 读取 JSON 数据并替换当前控制器 Shape。
        适合创建或切换 circle、cube、ball 等控制器形状。

    Ctrl.save_ctrl_shape
        将当前控制器的全部 NurbsCurve Shape 保存到 Shape Library。
        适合把 Maya 中编辑完成的控制器图形保存为可重复使用的 JSON 资源。

    Ctrl.create_sub_ctrl
        创建主控制器下面的次级控制器，并保持次级控制器本地 Transform 干净。
        适合给动画师提供主控制器之后的第二层细节调整能力。

    Ctrl.create_ctrl_hierarchy
        创建完整 Controller 层级结构。
        当前结构为 zero -> driven -> space -> connect -> offset -> ctrl -> subctrl -> output。
"""

import os
import json

import pymel.core as pm

from ..common import hierarchy_utils,attr_utils


class Ctrl(object):

    def __init__(self, name):
        u"""
        初始化 Controller 工具对象。

        如果 Maya 场景中已经存在指定名称的 Transform，则直接将它作为当前 Controller。
        如果不存在，则自动创建一个基础圆形 Controller。

        这样后续所有方法都可以直接使用 self.ctrl，不需要重复判断 Controller 是否存在。

        name(str): Controller 名称。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")

        print(ctrl_object.ctrl)
        """

        # 保存 Controller 标准名称。
        # self.ctrl_name 始终保存字符串名称，主要用于生成层级节点名称。
        self.ctrl_name = name

        # 保存主 Controller Transform PyNode。
        # _get_or_create_ctrl() 执行完成后，该属性一定会指向一个有效 Transform。
        self.ctrl = None

        # 保存当前主 Controller 下面的全部 Shape PyNode。
        self.ctrl_shapes = []

        # ---------------------------------------------------------------------
        # 保存 Controller 层级节点名称。
        # 名称和 Maya 节点分开保存：xxx_name 保存字符串，xxx_grp / sub_ctrl 保存 PyNode。
        # ---------------------------------------------------------------------
        self.zero_name = None
        self.driven_name = None
        self.space_name = None
        self.connect_name = None
        self.offset_name = None
        self.sub_ctrl_name = None
        self.output_name = None

        # ---------------------------------------------------------------------
        # 保存 Controller 层级 Maya 节点。
        # 完整层级结构：
        # zero
        # └── driven
        #     └── space
        #         └── connect
        #             └── offset
        #                 └── ctrl
        #                     └── subctrl
        #                         └── output
        # ---------------------------------------------------------------------
        self.zero_grp = None
        self.driven_grp = None
        self.space_grp = None
        self.connect_grp = None
        self.offset_grp = None
        self.sub_ctrl = None
        self.output_grp = None

        # 根据名称获取或创建主 Controller。
        self._get_or_create_ctrl()

    def _get_or_create_ctrl(self):
        u"""
        根据 self.ctrl_name 获取或创建当前 Controller。

        如果 Maya 场景中已经存在同名对象，则直接转换成 PyNode 使用。
        如果同名对象存在但不是 Transform，则抛出错误，避免把错误节点当作 Controller。
        如果场景中不存在同名对象，则创建一个默认半径为 1 的圆形 Controller。

        Returns:
            PyNode: 当前 Controller Transform 节点。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        ctrl = ctrl_object._get_or_create_ctrl()

        print(ctrl)
        """

        # 判断场景中是否已经存在这个名称的 Maya 节点。
        if pm.objExists(self.ctrl_name):

            # 已经存在时直接转换成 PyNode，后续统一使用 PyMEL 对象操作。
            self.ctrl = pm.PyNode(self.ctrl_name)

            # Controller 必须是 Transform。
            # 这里只检查 Transform，不强制要求已经存在 NurbsCurve Shape，
            # 因为后续 set_ctrl_shape() 可以给空 Transform 创建控制器 Shape。
            if not isinstance(self.ctrl, pm.nodetypes.Transform):
                raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(self.ctrl_name))

        else:

            # 场景中不存在时创建一个基础圆形 Controller。
            # pm.circle 返回列表，第一个元素为新创建的 Transform。
            self.ctrl = pm.circle(name=self.ctrl_name, radius=1.0, normal=(0, 1, 0))[0]

        return self.ctrl

    def create_ctrl(self, shape_name="circle", ctrl_color=17, ctrl_size=1.0, create_hierarchy=True):
        u"""
        完成当前 Controller 的基础设置，并根据需要创建完整控制器层级。

        Ctrl 类在实例化时已经通过 _get_or_create_ctrl() 保证 self.ctrl 存在，
        因此该方法不再重复创建新的 Transform，而是负责设置 Controller Shape、颜色和大小。

        执行顺序为：
            1. 设置 Shape。
            2. 设置颜色。
            3. 设置显示大小。
            4. 根据 create_hierarchy 决定是否创建完整 Controller 层级。

        Shape 必须最先设置，因为 set_ctrl_shape() 会替换旧 Shape。
        如果先设置颜色或大小，再替换 Shape，之前的显示设置会被新的 Shape 覆盖。

        shape_name(str): Controller Shape Library 中的 Shape 名称，默认 "circle"。
        ctrl_color(int): Maya Override Color 颜色索引，默认 17。
        ctrl_size(float): Controller Shape 相对缩放倍率，默认 1.0。
        create_hierarchy(bool): 是否创建完整控制器层级，默认 True。

        Returns:
            PyNode: 当前主 Controller Transform 节点。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        ctrl = ctrl_object.create_ctrl(shape_name="circle", ctrl_color=6, ctrl_size=1.5, create_hierarchy=True)

        print(ctrl)
        """

        # 先替换 Controller Shape。
        self.set_ctrl_shape(shape_name)

        # Shape 创建完成后再设置颜色，确保颜色作用于最终 Shape。
        self.set_ctrl_color(ctrl_color)

        # 通过缩放 Curve CV 调整显示大小，不修改 Controller Transform Scale。
        self.set_ctrl_size(ctrl_size)

        # 根据参数决定是否创建完整控制器层级。
        if create_hierarchy:
            self.create_ctrl_hierarchy(sub_ctrl_shape=shape_name, sub_ctrl_color=ctrl_color, sub_ctrl_size=ctrl_size*0.7)
        else:
            pass
        return self.ctrl

    def get_ctrl_shapes(self):
        u"""
        获取当前控制器下面的全部 Shape 节点。

        一个 Controller Transform 可以同时拥有一个或多个 NurbsCurve Shape。
        统一返回 Shape 列表后，颜色、大小、旋转和偏移等操作可以同时作用于整个控制器。

        Returns:
            list: 当前控制器下面的全部 Shape PyNode。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        ctrl_shapes = ctrl_object.get_ctrl_shapes()

        print(ctrl_shapes)
        """

        # 获取 Controller Transform 下面全部非 Intermediate Shape 节点。
        self.ctrl_shapes = self.ctrl.getShapes(noIntermediate=True)

        return self.ctrl_shapes

    def get_ctrl_shape_list(self):
        u"""
        获取 Controller Shape Library 中所有可用的 Shape 名称。

        该方法扫描 resources/controller_shapes 目录中的 JSON 文件，
        并去掉 .json 扩展名后返回 Shape 名称列表。

        Returns:
            list: Controller Shape Library 中所有可用的 Shape 名称。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_md_shape_list_main_001")
        shape_list = ctrl_object.get_ctrl_shape_list()

        print(shape_list)
        """

        # 获取 muziToolset 项目根目录。
        rigging_path = os.path.dirname(__file__)
        core_path = os.path.dirname(rigging_path)
        project_path = os.path.dirname(core_path)

        # 拼接 Controller Shape Library 路径。
        shape_library_path = os.path.join(project_path, "resources", "controller_shapes")

        # 保存找到的 Shape 名称。
        shape_list = []

        # Shape Library 不存在时返回空列表。
        if not os.path.exists(shape_library_path):
            pm.warning(u"找不到 Controller Shape Library：{}".format(shape_library_path))
            return shape_list

        # 获取资源目录中的全部文件。
        file_names = os.listdir(shape_library_path)

        # 只读取 JSON 文件，并去掉文件扩展名。
        for file_name in file_names:
            if file_name.lower().endswith(".json"):
                shape_name = os.path.splitext(file_name)[0]
                shape_list.append(shape_name)

        # 按名称排序，方便 UI 或 Shape Picker 显示。
        shape_list.sort()

        return shape_list

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

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
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

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        ctrl_object.set_ctrl_size(2.0)
        """

        # 获取控制器下面的全部 Shape。
        self.ctrl_shapes = self.get_ctrl_shapes()

        # 逐个检查 Shape，只对 NurbsCurve 的 CV 进行缩放。
        for ctrl_shape in self.ctrl_shapes:
            if isinstance(ctrl_shape, pm.nodetypes.NurbsCurve):
                pm.scale(ctrl_shape.cv[:], ctrl_size, ctrl_size, ctrl_size, relative=True, objectSpace=True)

    def set_ctrl_rotate(self, rotate_x=0.0, rotate_y=0.0, rotate_z=0.0):
        u"""
        旋转当前控制器全部 NurbsCurve Shape 的 CV。

        该方法只修改 Curve Shape 的 CV，不修改 Controller Transform 的 Rotate。
        因此控制器的 rotateX、rotateY、rotateZ 可以继续保持为 0。

        rotate_x(float): X 轴相对旋转角度，默认 0.0。
        rotate_y(float): Y 轴相对旋转角度，默认 0.0。
        rotate_z(float): Z 轴相对旋转角度，默认 0.0。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        ctrl_object.set_ctrl_rotate(rotate_x=90.0, rotate_y=0.0, rotate_z=0.0)
        """

        # 获取控制器下面的全部 Shape。
        self.ctrl_shapes = self.get_ctrl_shapes()

        # 逐个检查 Shape，只旋转 NurbsCurve 的 CV。
        for ctrl_shape in self.ctrl_shapes:
            if isinstance(ctrl_shape, pm.nodetypes.NurbsCurve):
                pm.rotate(ctrl_shape.cv[:], rotate_x, rotate_y, rotate_z, relative=True, objectSpace=True)

    def set_ctrl_offset(self, offset_x=0.0, offset_y=0.0, offset_z=0.0):
        u"""
        偏移当前控制器全部 NurbsCurve Shape 的 CV。

        该方法只移动 Curve Shape 的 CV，不修改 Controller Transform 的 Translate。
        因此控制器的 translateX、translateY、translateZ 可以继续保持为 0。

        offset_x(float): X 轴相对偏移距离，默认 0.0。
        offset_y(float): Y 轴相对偏移距离，默认 0.0。
        offset_z(float): Z 轴相对偏移距离，默认 0.0。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        ctrl_object.set_ctrl_offset(offset_x=0.0, offset_y=2.0, offset_z=0.0)
        """

        # 获取控制器下面的全部 Shape。
        self.ctrl_shapes = self.get_ctrl_shapes()

        # 逐个检查 Shape，只移动 NurbsCurve 的 CV。
        for ctrl_shape in self.ctrl_shapes:
            if isinstance(ctrl_shape, pm.nodetypes.NurbsCurve):
                pm.move(ctrl_shape.cv[:], offset_x, offset_y, offset_z, relative=True, objectSpace=True)

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

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
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

    def save_ctrl_shape(self, shape_name):
        u"""
        将当前控制器的全部 NurbsCurve Shape 保存到 Controller Shape Library。

        该方法会读取当前控制器下面每一个 NurbsCurve Shape 的 CV 坐标、
        Degree、Curve Form 和 Knot Vector，并整理成当前 Shape Library 使用的
        JSON 数据结构保存到 resources/controller_shapes 目录。

        对于 Periodic Curve，Maya 内部会保留重复的 degree 个 CV。
        保存时会去掉末尾重复 CV，使保存的数据能够和 set_ctrl_shape() 的
        Periodic Curve 重建逻辑保持对应关系。

        shape_name(str): 保存到 Shape Library 中使用的 Shape 名称，不需要包含 .json 扩展名。

        Returns:
            str: 保存完成后的 JSON 文件路径。
            None: 当前控制器没有可保存的 NurbsCurve Shape 时返回 None。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_md_test_main_001")
        shape_file = ctrl_object.save_ctrl_shape("my_ctrl_shape")

        print(shape_file)
        """

        # 获取当前控制器下面的全部 Shape。
        self.ctrl_shapes = self.get_ctrl_shapes()

        # 外层列表保存整个 Controller 的全部 NurbsCurve Shape 数据。
        # 一个 Controller 可以由一个或多个 Curve Shape 组合而成。
        shape_data = []

        # 逐个读取当前 Controller 下面的 Shape。
        for ctrl_shape in self.ctrl_shapes:

            # Shape Library 当前只保存 NurbsCurve。
            # 如果 Transform 下面存在其他类型 Shape，则直接跳过。
            if not isinstance(ctrl_shape, pm.nodetypes.NurbsCurve):
                continue

            # 获取当前 Curve 的 Degree。
            # 常见值为 1（Linear）或 3（Cubic）。
            degree = ctrl_shape.getAttr("degree")

            # 获取当前 Curve Form。
            # Maya 中：0 = Open，1 = Closed，2 = Periodic。
            curve_form = ctrl_shape.getAttr("form")

            # Shape Library 使用 bool 保存 Periodic 状态，
            # 所以这里只判断 Curve Form 是否为 2。
            periodic = curve_form == 2

            # 获取 Curve 自身对象空间中的全部 CV 坐标。
            # 使用 object space 可以避免 Controller Transform 的世界位置影响 Shape 数据。
            curve_points = ctrl_shape.getCVs(space="object")

            # Periodic Curve 在 Maya 内部会包含重复的 degree 个 CV。
            # set_ctrl_shape() 加载时会重新补回这些重复点，
            # 因此保存时只保留基础 CV，避免数据重复。
            if periodic:
                curve_points = curve_points[:-degree]

            # Shape Library 的 points 使用一维数组保存：
            # [x0, y0, z0, x1, y1, z1, ...]
            # 因此需要把 Maya Point 列表逐个拆成 XYZ 数值。
            point_values = []

            for point in curve_points:
                point_values.append(point[0])
                point_values.append(point[1])
                point_values.append(point[2])

            # 获取当前 Curve 原始 Knot Vector。
            # 保存原始 Knot 可以让 set_ctrl_shape() 重建时保持曲线结构一致。
            knot_values = []
            knots = ctrl_shape.getKnots()

            for knot in knots:
                knot_values.append(knot)

            # 整理当前一个 NurbsCurve Shape 的完整 JSON 数据。
            shape_info = {
                "points": point_values,
                "degree": degree,
                "periodic": periodic,
                "knot": knot_values
            }

            # 添加到整个 Controller 的 Shape 数据列表中。
            shape_data.append(shape_info)

        # 如果没有找到任何 NurbsCurve Shape，则停止保存。
        if not shape_data:
            pm.warning(u"当前控制器没有可以保存的 NurbsCurve Shape。")
            return None

        # 获取 muziToolset 项目根目录。
        rigging_path = os.path.dirname(__file__)
        core_path = os.path.dirname(rigging_path)
        project_path = os.path.dirname(core_path)

        # 获取统一的 Controller Shape Library 路径。
        shape_library_path = os.path.join(project_path, "resources", "controller_shapes")

        # 根据传入名称拼接最终 JSON 文件路径。
        shape_file = os.path.join(shape_library_path, shape_name + ".json")

        # 将全部 Shape 数据写入 JSON。
        # indent=4 让文件保持可读，方便以后直接检查和维护 Shape 数据。
        with open(shape_file, "w") as file:
            json.dump(shape_data, file, indent=4)

        # 返回保存路径，方便 UI 或其他工具继续使用。
        return shape_file


    def create_sub_ctrl(self, shape_name="circle", ctrl_color=17, ctrl_size=0.7):
        u"""
        创建主 Controller 下方的次级控制器 SubCtrl。

        次级控制器本身仍然使用 Ctrl 类创建，因此可以直接复用现有的
        Shape、Color、Size 等 Controller 基础功能。

        创建步骤：
            1. 根据主控制器名称生成 subctrl 名称。
            2. 创建或获取 SubCtrl。
            3. 设置 SubCtrl 的 Shape、颜色和大小。
            4. 将 SubCtrl 世界 Transform 匹配到主 Ctrl。
            5. 将 SubCtrl Parent 到主 Ctrl 下方。

        在 Parent 之前先进行 matchTransform，可以让 SubCtrl Parent 完成后
        保持本地 Translate / Rotate 接近 0，Scale 接近 1，方便动画师进行二级调整。

        shape_name(str): SubCtrl 使用的 Shape 名称，默认 "circle"。
        ctrl_color(int): SubCtrl 的 Override Color，默认 17。
        ctrl_size(float): SubCtrl Shape 的相对大小，默认 0.7。

        Returns:
            PyNode: 创建或获取到的 SubCtrl Transform 节点。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        sub_ctrl = ctrl_object.create_sub_ctrl(shape_name="circle", ctrl_color=6, ctrl_size=0.7)

        print(sub_ctrl)
        """

        # 如果 create_ctrl_hierarchy() 还没有生成名称，
        # 单独调用 create_sub_ctrl() 时也可以自行得到 SubCtrl 名称。
        if not self.sub_ctrl_name:
            self.sub_ctrl_name = self.ctrl_name.replace("ctrl_", "subctrl_", 1)

        # 使用同一个 Ctrl 类创建或获取次级控制器。
        # Ctrl(sub_ctrl_name) 只保证 Transform 存在，不会自动创建完整层级。
        sub_ctrl_object = Ctrl(self.sub_ctrl_name)

        # 设置 SubCtrl 的最终 Shape、颜色和视觉大小。
        # create_hierarchy=False 可以避免 SubCtrl 自己再次创建 Zero / Driven 等完整层级。
        sub_ctrl_object.create_ctrl(shape_name=shape_name, ctrl_color=ctrl_color, ctrl_size=ctrl_size, create_hierarchy=False)

        # 保存真正的 Maya SubCtrl PyNode，供后续 Output 和其他系统继续使用。
        self.sub_ctrl = sub_ctrl_object.ctrl

        # Parent 之前先让 SubCtrl 的世界位置、旋转、缩放完全匹配主 Ctrl。
        pm.matchTransform(self.sub_ctrl, self.ctrl, position=True, rotation=True, scale=True)

        # 将 SubCtrl 放到主 Ctrl 下方。
        # hierarchy_utils.parent() 会保持当前世界 Transform，
        # 因此前面已经匹配主 Ctrl 的 SubCtrl 会得到干净的本地 Transform。
        hierarchy_utils.parent(child_node=self.sub_ctrl, parent_node=self.ctrl)

        #给控制器上创建sub_ctrl_vis的属性来方便控制次级控制器是否进行显示
        attr_object = attr_utils.Attr(self.ctrl_name)
        attr_object.add_attr(attr_name = 'sub_ctrl_vis',attr_type = bool, default_value = 0, keyable = False )
        #属性进行连接
        attr_object.connect_attr (attr_name = 'sub_ctrl_vis' , target_object = self.sub_ctrl_name, target_attr_name = '.visibility')


        return self.sub_ctrl

    def create_ctrl_hierarchy(self, sub_ctrl_shape="circle", sub_ctrl_color=17, sub_ctrl_size=0.7):
        u"""
        创建当前 Controller 的完整层级结构。

        最终结构：

        zero
        └── driven
            └── space
                └── connect
                    └── offset
                        └── ctrl
                            └── subctrl
                                └── output

        上方五个 Group 使用 hierarchy_utils.add_extra_group(..., relation="parent")
        从最靠近 Ctrl 的 offset 开始向外逐层创建。

        SubCtrl 是真正的 Controller，而不是普通 Group，
        因此通过 create_sub_ctrl() 单独创建并放到主 Ctrl 下方。

        Output 是最终输出节点，使用 relation="child" 创建在 SubCtrl 下方，
        后续 Joint、Matrix 或 Deformer 可以统一读取 Output 的最终 Transform。

        sub_ctrl_shape(str): SubCtrl 使用的 Shape 名称，默认 "circle"。
        sub_ctrl_color(int): SubCtrl 的 Override Color，默认 17。
        sub_ctrl_size(float): SubCtrl Shape 的相对大小，默认 0.7。

        Returns:
            PyNode: 完整 Controller 层级最外层的 Zero Group。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        zero_grp = ctrl_object.create_ctrl_hierarchy(sub_ctrl_shape="circle", sub_ctrl_color=6, sub_ctrl_size=0.7)

        print(zero_grp)
        print(ctrl_object.output_grp)
        """

        # ---------------------------------------------------------------------
        # 根据主 Controller 名称生成完整层级名称。
        # 例如 ctrl_lf_eye_main_001 会得到：
        # zero_lf_eye_main_001
        # driven_lf_eye_main_001
        # space_lf_eye_main_001
        # connect_lf_eye_main_001
        # offset_lf_eye_main_001
        # subctrl_lf_eye_main_001
        # output_lf_eye_main_001
        # ---------------------------------------------------------------------
        self.zero_name = self.ctrl_name.replace("ctrl_", "zero_", 1)
        self.driven_name = self.ctrl_name.replace("ctrl_", "driven_", 1)
        self.space_name = self.ctrl_name.replace("ctrl_", "space_", 1)
        self.connect_name = self.ctrl_name.replace("ctrl_", "connect_", 1)
        self.offset_name = self.ctrl_name.replace("ctrl_", "offset_", 1)
        self.sub_ctrl_name = self.ctrl_name.replace("ctrl_", "subctrl_", 1)
        self.output_name = self.ctrl_name.replace("ctrl_", "output_", 1)

        # ---------------------------------------------------------------------
        # 从 Ctrl 开始向外创建父层级。
        # add_extra_group(..., relation="parent") 会把新 Group 插入传入对象上方，
        # 所以创建顺序必须和最终 Outliner 顺序相反：
        # ctrl -> offset -> connect -> space -> driven -> zero
        # ---------------------------------------------------------------------

        # Offset 是距离主 Controller 最近的一层父 Group。
        self.offset_grp = hierarchy_utils.add_extra_group(self.ctrl_name, self.offset_name, relation="parent")

        # Connect 创建在 Offset 上方。
        self.connect_grp = hierarchy_utils.add_extra_group(self.offset_grp, self.connect_name, relation="parent")

        # Space 创建在 Connect 上方，后续可以作为 Space Switch 的处理层。
        self.space_grp = hierarchy_utils.add_extra_group(self.connect_grp, self.space_name, relation="parent")

        # Driven 创建在 Space 上方，后续可以用于程序驱动、SDK 或自动运动。
        self.driven_grp = hierarchy_utils.add_extra_group(self.space_grp, self.driven_name, relation="parent")

        # Zero 创建在最外层，作为整个 Controller 系统的初始归零层。
        self.zero_grp = hierarchy_utils.add_extra_group(self.driven_grp, self.zero_name, relation="parent")

        # ---------------------------------------------------------------------
        # 创建主 Controller 下方的次级控制器。
        # SubCtrl 用于动画师进行第二层细节调整。
        # ---------------------------------------------------------------------
        self.create_sub_ctrl(shape_name=sub_ctrl_shape, ctrl_color=sub_ctrl_color, ctrl_size=sub_ctrl_size)

        # ---------------------------------------------------------------------
        # 创建最终 Output Group。
        # relation="child" 会把 Output 创建在 SubCtrl 下方。
        # Output 只负责提供最终 Transform，不作为动画师直接操作的控制器。
        # ---------------------------------------------------------------------
        self.output_grp = hierarchy_utils.add_extra_group(self.sub_ctrl, self.output_name, relation="child")

        return self.zero_grp
