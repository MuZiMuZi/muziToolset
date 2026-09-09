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
        设置当前 Controller 的 Shape、颜色、大小、轴向，并根据需要创建完整控制器层级。
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

    Ctrl.set_ctrl_axis
        将当前控制器 Shape 绝对设置为 X+ / X- / Y+ / Y- / Z+ / Z- 面朝方向。
        轴向切换只修改 Curve CV，不修改 Transform，并且重复切换不会累积旋转。

    Ctrl.set_ctrl_rotate
        通过旋转全部 NurbsCurve Shape 的 CV 增加额外相对旋转。
        适合在基础轴向之外继续调整控制器图形方向，同时保持 Transform Rotate 为默认值。

    Ctrl.set_ctrl_offset
        通过移动全部 NurbsCurve Shape 的 CV 修改控制器显示位置。
        适合偏移控制器图形，同时保持 Transform Translate 为默认值。

    Ctrl.set_ctrl_shape
        从 Controller Shape Library 读取 JSON 数据并替换当前控制器 Shape。
        Shape Library 统一以 X+ 作为标准面朝方向。

    Ctrl.save_ctrl_shape
        将当前控制器的全部 NurbsCurve Shape 保存到 Shape Library。
        保存时会把当前轴向还原到标准 X+，避免把模块轴向写进 Shape 资源。

    Ctrl.create_sub_ctrl
        创建主控制器下面的次级控制器，并保持次级控制器本地 Transform 干净。
        SubCtrl 与主控制器使用相同的 Shape 轴向。

    Ctrl.create_ctrl_hierarchy
        创建完整 Controller 层级结构，并支持安全重复执行。
        层级 Group 的“存在则获取、不存在则创建”统一交给 hierarchy_utils.add_extra_group() 处理。
        当前结构为 zero -> driven -> space -> connect -> offset -> ctrl，
        ctrl 下方同时包含 subctrl 和 output，subctrl 通过属性连接驱动 output。
"""

import os
import json

import maya.cmds as cmds
import pymel.core as pm

from ..common import hierarchy_utils, attr_utils, transform_utils


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
        #                     ├── subctrl
        #                     └── output
        #
        # subctrl 的 TRS / rotateOrder 通过属性连接传给 output，
        # 因此隐藏 subctrl 不会影响 output 以及 output 下方的其他层级。
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
        如果场景中不存在同名对象，则创建一个默认半径为 1、面朝 X+ 的圆形 Controller。

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

            # 新系统统一把 X+ 作为 Controller Shape Library 的标准面朝方向。
            # 因此基础圆形 Controller 直接创建在 YZ 平面，法线约定为 X+。
            self.ctrl = pm.circle(name=self.ctrl_name, radius=1.0, normal=(1, 0, 0))[0]

            # 新创建的基础 Shape 已经处于标准 X+ 轴向，记录轴向元数据。
            ctrl_name = self.ctrl.name()
            axis_attr = ctrl_name + ".ctrl_axis"

            if not cmds.attributeQuery("ctrl_axis", node=ctrl_name, exists=True):
                cmds.addAttr(ctrl_name, longName="ctrl_axis", dataType="string")

            cmds.setAttr(axis_attr, "X+", type="string")
            cmds.setAttr(axis_attr, keyable=False, channelBox=False)

        return self.ctrl

    def create_ctrl(
        self,
        shape_name="circle",
        ctrl_color=17,
        ctrl_size=1.0,
        ctrl_axis="X+",
        create_hierarchy=True,
        match_transform_target=None
    ):
        u"""
        完成当前 Controller 的基础设置，并根据需要创建完整控制器层级。

        Ctrl 类在实例化时已经通过 _get_or_create_ctrl() 保证 self.ctrl 存在，
        因此该方法不再重复创建新的 Transform，而是负责设置 Controller Shape、颜色、大小和轴向。

        执行顺序为：
            1. 设置 Shape，并恢复为 Shape Library 标准 X+ 轴向。
            2. 设置颜色。
            3. 设置显示大小。
            4. 设置目标绝对轴向。
            5. 可选匹配 Guide / Target。
            6. 根据 create_hierarchy 决定是否创建完整 Controller 层级。

        Shape 必须最先设置，因为 set_ctrl_shape() 会替换旧 Shape。
        如果先设置颜色、大小或轴向，再替换 Shape，之前的显示设置会被新的 Shape 覆盖。

        shape_name(str): Controller Shape Library 中的 Shape 名称，默认 "circle"。
        ctrl_color(int): Maya Override Color 颜色索引，默认 17。
        ctrl_size(float): Controller Shape 相对缩放倍率，默认 1.0。
        ctrl_axis(str): Controller Shape 面朝方向，支持 X+ / X- / Y+ / Y- / Z+ / Z-，默认 "X+"。
        create_hierarchy(bool): 是否创建完整控制器层级，默认 True。
        match_transform_target(str/PyNode): 可选位置、旋转、缩放匹配目标。

        Returns:
            PyNode: 当前主 Controller Transform 节点。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        ctrl = ctrl_object.create_ctrl(
            shape_name="circle",
            ctrl_color=6,
            ctrl_size=1.5,
            ctrl_axis="Z+",
            create_hierarchy=True
        )

        print(ctrl)
        """

        # 先替换 Controller Shape。
        self.set_ctrl_shape(shape_name)

        # Shape 创建完成后再设置颜色，确保颜色作用于最终 Shape。
        self.set_ctrl_color(ctrl_color)

        # 通过缩放 Curve CV 调整显示大小，不修改 Controller Transform Scale。
        self.set_ctrl_size(ctrl_size)

        # 使用绝对轴向设置 Shape 面朝方向，不修改 Controller Transform Rotate。
        self.set_ctrl_axis(ctrl_axis)

        # 根据参数决定是否需要匹配目标位置、旋转和缩放。
        if match_transform_target:
            self.set_match_transform(target=match_transform_target)

        # 根据参数决定是否创建完整控制器层级。
        if create_hierarchy:
            self.create_ctrl_hierarchy(
                sub_ctrl_shape=shape_name,
                sub_ctrl_color=ctrl_color,
                sub_ctrl_size=ctrl_size * 0.7,
                ctrl_axis=ctrl_axis
            )

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

    def set_ctrl_axis(self, ctrl_axis="X+"):
        u"""
        将当前 Controller Shape 设置到指定的绝对面朝方向。

        Controller Shape Library 统一把 X+ 作为标准面朝方向。
        该方法只转换 NurbsCurve CV 的对象空间坐标，不修改 Controller Transform Rotate。

        当前轴向会保存在 Controller Transform 的隐藏字符串属性 ctrl_axis 中。
        每次切换时先把当前 Shape 从已记录轴向还原到标准 X+，再从 X+ 转换到目标轴向，
        因此 X+ -> Z+ -> Y- -> Z+ 不会产生旋转累积，也不会重新加载 Shape JSON，
        所以动画师手动修改过的 CV 形状能够继续保留。

        ctrl_axis(str): 目标面朝方向，只支持 X+ / X- / Y+ / Y- / Z+ / Z-。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        ctrl_object.set_ctrl_shape("circle")
        ctrl_object.set_ctrl_axis("Z+")
        ctrl_object.set_ctrl_axis("Y-")
        ctrl_object.set_ctrl_axis("Z+")
        """

        valid_axes = ("X+", "X-", "Y+", "Y-", "Z+", "Z-")

        if ctrl_axis not in valid_axes:
            raise ValueError(
                u"ctrl_axis 只能使用 X+ / X- / Y+ / Y- / Z+ / Z-，当前值：{}".format(ctrl_axis)
            )

        ctrl_name = self.ctrl.name()
        axis_attr = ctrl_name + ".ctrl_axis"
        current_axis = "X+"

        # 读取当前 Shape 已记录的绝对轴向。
        # 旧场景没有该属性时，按照新版 Shape Library 标准 X+ 处理。
        if cmds.attributeQuery("ctrl_axis", node=ctrl_name, exists=True):
            stored_axis = cmds.getAttr(axis_attr)

            if stored_axis in valid_axes:
                current_axis = stored_axis
        else:
            cmds.addAttr(ctrl_name, longName="ctrl_axis", dataType="string")

        # 已经是目标轴向时不再次旋转 CV，只同步元数据。
        if current_axis == ctrl_axis:
            cmds.setAttr(axis_attr, ctrl_axis, type="string")
            cmds.setAttr(axis_attr, keyable=False, channelBox=False)
            return

        self.ctrl_shapes = self.get_ctrl_shapes()

        for ctrl_shape in self.ctrl_shapes:
            if not isinstance(ctrl_shape, pm.nodetypes.NurbsCurve):
                continue

            for cv in ctrl_shape.cv:
                point = pm.xform(cv, query=True, translation=True, objectSpace=True)
                point_x = point[0]
                point_y = point[1]
                point_z = point[2]

                # -------------------------------------------------------------
                # 第一步：从当前绝对轴向还原到 Shape Library 标准 X+。
                # -------------------------------------------------------------
                if current_axis == "X+":
                    canonical_x = point_x
                    canonical_y = point_y
                    canonical_z = point_z

                elif current_axis == "X-":
                    canonical_x = -point_x
                    canonical_y = point_y
                    canonical_z = -point_z

                elif current_axis == "Y+":
                    canonical_x = point_y
                    canonical_y = -point_x
                    canonical_z = point_z

                elif current_axis == "Y-":
                    canonical_x = -point_y
                    canonical_y = point_x
                    canonical_z = point_z

                elif current_axis == "Z+":
                    canonical_x = point_z
                    canonical_y = point_y
                    canonical_z = -point_x

                else:
                    canonical_x = -point_z
                    canonical_y = point_y
                    canonical_z = point_x

                # -------------------------------------------------------------
                # 第二步：从标准 X+ 转换到目标绝对轴向。
                # X+ 的单位方向 (1, 0, 0) 会真正映射到对应目标轴方向。
                # -------------------------------------------------------------
                if ctrl_axis == "X+":
                    target_x = canonical_x
                    target_y = canonical_y
                    target_z = canonical_z

                elif ctrl_axis == "X-":
                    target_x = -canonical_x
                    target_y = canonical_y
                    target_z = -canonical_z

                elif ctrl_axis == "Y+":
                    target_x = -canonical_y
                    target_y = canonical_x
                    target_z = canonical_z

                elif ctrl_axis == "Y-":
                    target_x = canonical_y
                    target_y = -canonical_x
                    target_z = canonical_z

                elif ctrl_axis == "Z+":
                    target_x = -canonical_z
                    target_y = canonical_y
                    target_z = canonical_x

                else:
                    target_x = canonical_z
                    target_y = canonical_y
                    target_z = -canonical_x

                pm.xform(
                    cv,
                    translation=(target_x, target_y, target_z),
                    objectSpace=True
                )

        # 保存最终轴向，让下一次切换能够从正确的当前状态还原。
        cmds.setAttr(axis_attr, ctrl_axis, type="string")
        cmds.setAttr(axis_attr, keyable=False, channelBox=False)

    def set_ctrl_rotate(self, rotate_x=0.0, rotate_y=0.0, rotate_z=0.0):
        u"""
        相对旋转当前控制器全部 NurbsCurve Shape 的 CV。

        该方法用于在 set_ctrl_axis() 的绝对基础轴向之外增加额外图形旋转。
        它只修改 Curve Shape 的 CV，不修改 Controller Transform 的 Rotate。
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

    def set_match_transform(self, target, position=True, rotation=True, scale=True):
        u"""
        将当前 Controller 对齐到指定目标的位置、旋转和缩放。

        target(str/PyNode): 需要对齐的目标对象，例如 Guide、Locator 或 Transform。
        position(bool): 是否匹配位置，默认 True。
        rotation(bool): 是否匹配旋转，默认 True。
        scale(bool): 是否匹配缩放，默认 True。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        ctrl_object.set_match_transform("loc_lf_eye_guide_001")
        """

        ctrl_object = transform_utils.Transform(self.ctrl_name)
        ctrl_object.match_transform(target, position=position, rotation=rotation, scale=scale)

    def set_ctrl_shape(self, shape_name):
        u"""
        根据 Shape Library 中的 JSON 文件替换当前控制器的 Curve Shape。

        一个 JSON 文件可以保存一个或多个 NurbsCurve Shape。
        方法会先读取 JSON 数据并创建临时 Curve，然后删除当前控制器旧 Shape，
        最后把新 Curve Shape 移到当前控制器 Transform 下面。

        新版 Shape Library 统一把 X+ 作为标准面朝方向。
        Shape 替换完成后会把隐藏属性 ctrl_axis 重置为 X+，
        后续 set_ctrl_axis() 再根据模块需要转换到最终绝对轴向。

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

        # Shape Library 数据统一视为标准 X+ 轴向。
        # 替换 Shape 后必须同步重置轴向元数据，避免沿用旧 Shape 的轴向状态。
        ctrl_name = self.ctrl.name()
        axis_attr = ctrl_name + ".ctrl_axis"

        if not cmds.attributeQuery("ctrl_axis", node=ctrl_name, exists=True):
            cmds.addAttr(ctrl_name, longName="ctrl_axis", dataType="string")

        cmds.setAttr(axis_attr, "X+", type="string")
        cmds.setAttr(axis_attr, keyable=False, channelBox=False)

        return self.ctrl_shapes

    def save_ctrl_shape(self, shape_name):
        u"""
        将当前控制器的全部 NurbsCurve Shape 保存到 Controller Shape Library。

        该方法会读取当前控制器下面每一个 NurbsCurve Shape 的 CV 坐标、
        Degree、Curve Form 和 Knot Vector，并整理成当前 Shape Library 使用的
        JSON 数据结构保存到 resources/controller_shapes 目录。

        Controller Shape Library 统一以 X+ 作为标准面朝方向。
        如果当前 Controller 已经设置成 Y+、Z- 等模块轴向，保存时只在数据层把 CV
        还原到标准 X+ 后写入 JSON，不会修改 Maya 场景中当前 Controller 的实际外观。

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
        ctrl_object.set_ctrl_axis("Z+")
        shape_file = ctrl_object.save_ctrl_shape("my_ctrl_shape")

        print(shape_file)
        """

        # 获取当前控制器下面的全部 Shape。
        self.ctrl_shapes = self.get_ctrl_shapes()

        # 获取当前 Controller 的轴向状态。
        # 资源保存时会把这个轴向逆转换回 Shape Library 标准 X+。
        valid_axes = ("X+", "X-", "Y+", "Y-", "Z+", "Z-")
        current_axis = "X+"
        ctrl_name = self.ctrl.name()
        axis_attr = ctrl_name + ".ctrl_axis"

        if cmds.attributeQuery("ctrl_axis", node=ctrl_name, exists=True):
            stored_axis = cmds.getAttr(axis_attr)

            if stored_axis in valid_axes:
                current_axis = stored_axis

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
            # 保存前先把当前模块轴向还原到标准 X+。
            point_values = []

            for point in curve_points:
                point_x = point[0]
                point_y = point[1]
                point_z = point[2]

                if current_axis == "X+":
                    canonical_x = point_x
                    canonical_y = point_y
                    canonical_z = point_z

                elif current_axis == "X-":
                    canonical_x = -point_x
                    canonical_y = point_y
                    canonical_z = -point_z

                elif current_axis == "Y+":
                    canonical_x = point_y
                    canonical_y = -point_x
                    canonical_z = point_z

                elif current_axis == "Y-":
                    canonical_x = -point_y
                    canonical_y = point_x
                    canonical_z = point_z

                elif current_axis == "Z+":
                    canonical_x = point_z
                    canonical_y = point_y
                    canonical_z = -point_x

                else:
                    canonical_x = -point_z
                    canonical_y = point_y
                    canonical_z = point_x

                point_values.append(canonical_x)
                point_values.append(canonical_y)
                point_values.append(canonical_z)

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

    def create_sub_ctrl(
        self,
        shape_name="circle",
        ctrl_color=17,
        ctrl_size=0.7,
        ctrl_axis="X+"
    ):
        u"""
        创建主 Controller 下方的次级控制器 SubCtrl。

        次级控制器本身仍然使用 Ctrl 类创建，因此可以直接复用现有的
        Shape、Color、Size、Axis 等 Controller 基础功能。

        创建步骤：
            1. 根据主控制器名称生成 subctrl 名称。
            2. 创建或获取 SubCtrl。
            3. 设置 SubCtrl 的 Shape、颜色、大小和轴向。
            4. 将 SubCtrl 世界 Transform 匹配到主 Ctrl。
            5. 将 SubCtrl Parent 到主 Ctrl 下方。

        在 Parent 之前先进行 matchTransform，可以让 SubCtrl Parent 完成后
        保持本地 Translate / Rotate 接近 0，Scale 接近 1，方便动画师进行二级调整。

        SubCtrl 只负责提供第二层动画调整和显示，Output 不再作为它的子节点。
        Output 会和 SubCtrl 一样直接位于主 Ctrl 下方，并通过属性连接接收 SubCtrl 的变换。
        因此关闭 sub_ctrl_vis 时只会隐藏 SubCtrl，不会隐藏 Output 或后续 FK 层级。

        shape_name(str): SubCtrl 使用的 Shape 名称，默认 "circle"。
        ctrl_color(int): SubCtrl 的 Override Color，默认 17。
        ctrl_size(float): SubCtrl Shape 的相对大小，默认 0.7。
        ctrl_axis(str): SubCtrl Shape 面朝方向，默认与主 Controller 一致传入。

        Returns:
            PyNode: 创建或获取到的 SubCtrl Transform 节点。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")
        sub_ctrl = ctrl_object.create_sub_ctrl(
            shape_name="circle",
            ctrl_color=6,
            ctrl_size=0.7,
            ctrl_axis="Z+"
        )

        print(sub_ctrl)
        """

        # 如果 create_ctrl_hierarchy() 还没有生成名称，
        # 单独调用 create_sub_ctrl() 时也可以自行得到 SubCtrl 名称。
        if not self.sub_ctrl_name:
            self.sub_ctrl_name = self.ctrl_name.replace("ctrl_", "subctrl_", 1)

        # 使用同一个 Ctrl 类创建或获取次级控制器。
        # Ctrl(sub_ctrl_name) 只保证 Transform 存在，不会自动创建完整层级。
        sub_ctrl_object = Ctrl(self.sub_ctrl_name)

        # 设置 SubCtrl 的最终 Shape、颜色、视觉大小和轴向。
        # create_hierarchy=False 可以避免 SubCtrl 自己再次创建 Zero / Driven 等完整层级。
        sub_ctrl_object.create_ctrl(
            shape_name=shape_name,
            ctrl_color=ctrl_color,
            ctrl_size=ctrl_size,
            ctrl_axis=ctrl_axis,
            create_hierarchy=False
        )

        # 保存真正的 Maya SubCtrl PyNode，供后续 Output 和其他系统继续使用。
        self.sub_ctrl = sub_ctrl_object.ctrl

        # Parent 之前先让 SubCtrl 的世界位置、旋转、缩放完全匹配主 Ctrl。
        pm.matchTransform(self.sub_ctrl, self.ctrl, position=True, rotation=True, scale=True)

        # 将 SubCtrl 放到主 Ctrl 下方。
        # hierarchy_utils.parent() 会保持当前世界 Transform，
        # 因此前面已经匹配主 Ctrl 的 SubCtrl 会得到干净的本地 Transform。
        hierarchy_utils.parent(child_node=self.sub_ctrl, parent_node=self.ctrl)

        # 给控制器上创建 sub_ctrl_vis 属性，用来控制次级控制器是否显示。
        attr_object = attr_utils.Attr(self.ctrl_name)
        attr_object.add_attr(attr_name="sub_ctrl_vis", attr_type="bool", default_value=0, keyable=True)

        # 将主控制器的 sub_ctrl_vis 连接到次级控制器 visibility。
        attr_object.connect_attr(
            attr_name="sub_ctrl_vis",
            target_object=self.sub_ctrl_name,
            target_attr_name="visibility"
        )

        return self.sub_ctrl

    def create_ctrl_hierarchy(
        self,
        sub_ctrl_shape="circle",
        sub_ctrl_color=17,
        sub_ctrl_size=0.7,
        ctrl_axis="X+"
    ):
        u"""
        创建当前 Controller 的完整层级结构，并支持安全重复执行。

        最终结构：

        zero
        └── driven
            └── space
                └── connect
                    └── offset
                        └── ctrl
                            ├── subctrl
                            └── output

        SubCtrl 与 Output 是主 Ctrl 下方的兄弟节点，不再使用 subctrl -> output 的父子关系。
        SubCtrl 的 translate / rotate / scale / rotateOrder 通过属性连接传递到 Output。
        因此 SubCtrl 被隐藏时不会影响 Output，也不会继续隐藏 Output 下方的 FK 层级。

        Group 的创建、获取和层级恢复统一交给 hierarchy_utils.add_extra_group()：
        如果同名 Group 已经存在，则直接获取并复用；
        如果不存在，则创建新 Group；
        如果父子关系不正确，则恢复到当前调用要求的层级关系。

        因此 create_ctrl_hierarchy() 本身只负责描述 Controller 需要什么层级，
        不再重复编写每一个 Group 的 pm.objExists() 判断。

        上方五个 Group 从最靠近 Ctrl 的 Offset 开始向外逐层处理。
        SubCtrl 通过 create_sub_ctrl() 创建或获取，并继承主 Controller 的 ctrl_axis。
        Output 通过 relation="child" 创建或获取在主 Ctrl 下方。

        sub_ctrl_shape(str): SubCtrl 使用的 Shape 名称，默认 "circle"。
        sub_ctrl_color(int): SubCtrl 的 Override Color，默认 17。
        sub_ctrl_size(float): SubCtrl Shape 的相对大小，默认 0.7。
        ctrl_axis(str): Main Ctrl 与 SubCtrl 共用的绝对 Shape 面朝方向。

        Returns:
            PyNode: 完整 Controller 层级最外层的 Zero Group。

        Maya 使用示例：

        from muziToolset.core.rigging import ctrl_utils

        ctrl_object = ctrl_utils.Ctrl("ctrl_lf_eye_main_001")

        # 第一次执行：不存在的层级会被创建。
        zero_grp = ctrl_object.create_ctrl_hierarchy(ctrl_axis="Z+")

        # 第二次执行：已经存在的层级会被直接获取和复用。
        zero_grp = ctrl_object.create_ctrl_hierarchy(ctrl_axis="Z+")

        print(zero_grp)
        print(ctrl_object.output_grp)
        """

        # 根据主 Controller 名称生成完整层级名称。
        self.zero_name = self.ctrl_name.replace("ctrl_", "zero_", 1)
        self.driven_name = self.ctrl_name.replace("ctrl_", "driven_", 1)
        self.space_name = self.ctrl_name.replace("ctrl_", "space_", 1)
        self.connect_name = self.ctrl_name.replace("ctrl_", "connect_", 1)
        self.offset_name = self.ctrl_name.replace("ctrl_", "offset_", 1)
        self.sub_ctrl_name = self.ctrl_name.replace("ctrl_", "subctrl_", 1)
        self.output_name = self.ctrl_name.replace("ctrl_", "output_", 1)

        # 从 Ctrl 开始向外创建或获取父层级。
        # add_extra_group() 内部已经统一处理：存在则获取，不存在则创建，层级不正确则恢复。
        self.offset_grp = hierarchy_utils.add_extra_group(self.ctrl, self.offset_name, relation="parent")
        self.connect_grp = hierarchy_utils.add_extra_group(self.offset_grp, self.connect_name, relation="parent")
        self.space_grp = hierarchy_utils.add_extra_group(self.connect_grp, self.space_name, relation="parent")
        self.driven_grp = hierarchy_utils.add_extra_group(self.space_grp, self.driven_name, relation="parent")
        self.zero_grp = hierarchy_utils.add_extra_group(self.driven_grp, self.zero_name, relation="parent")

        # 创建或获取主 Controller 下方的次级控制器，并保持 Main Ctrl / SubCtrl 轴向一致。
        self.create_sub_ctrl(
            shape_name=sub_ctrl_shape,
            ctrl_color=sub_ctrl_color,
            ctrl_size=sub_ctrl_size,
            ctrl_axis=ctrl_axis
        )

        # 创建或获取最终 Output Group，并确保它直接位于主 Ctrl 下方。
        # 如果旧版本的 Output 仍然位于 SubCtrl 下方，add_extra_group() 会自动恢复父子关系。
        self.output_grp = hierarchy_utils.add_extra_group(self.ctrl, self.output_name, relation="child")

        # SubCtrl 与 Output 保持兄弟层级，因此 Visibility 不会沿 DAG 传播到 Output。
        # 通过属性连接将 SubCtrl 的局部变换传给 Output，使 Output 仍然包含第二层控制效果。
        sub_ctrl_attr = attr_utils.Attr(self.sub_ctrl)
        sub_ctrl_attr.connect_attr(attr_name="translate", target_object=self.output_grp, target_attr_name="translate")
        sub_ctrl_attr.connect_attr(attr_name="rotate", target_object=self.output_grp, target_attr_name="rotate")
        sub_ctrl_attr.connect_attr(attr_name="scale", target_object=self.output_grp, target_attr_name="scale")
        sub_ctrl_attr.connect_attr(attr_name="rotateOrder", target_object=self.output_grp, target_attr_name="rotateOrder")

        return self.zero_grp
