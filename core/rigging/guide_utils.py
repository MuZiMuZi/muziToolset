# coding=utf-8
u"""
guide_utils：Maya Module Guide 基础工具。

方法介绍与使用场景：

    Guide.__init__
        创建一个 Module Guide 工具对象。
        根据 module 名称自动生成统一的 Guide 模板文件名、Guide Root 名称和模板路径。
        当前 Face Guide 仍然作为一个完整模板管理，不拆分 Brow、Eye、Mouth 等独立模板。

    Guide.import_template
        导入当前 Module 对应的 Maya Guide 模板。
        如果场景中已经存在 Guide Root，则直接获取并复用，不重复导入模板。

    Guide.get_guides
        根据模块名称获取该模块组下面所有 Locator Guide。
        适合后续按模块创建 Joint、Controller 或 Guide Display Curve。

    Guide.create_guide_curve
        根据指定模块和方向创建一条 Degree 1 Guide Display Curve。
        Locator Shape 的 worldPosition 会直接连接到 Curve CV，只用于辅助显示定位关系。
"""

import os

import pymel.core as pm

from ... import config as package_config


class Guide(object):

    def __init__(self, module="face"):
        u"""
        初始化 Module Guide 工具对象。

        Guide 模板统一使用以下命名规则：

            模板文件：<module>_guide.ma
            Guide Root：grp_md_<module>_guide_001

        例如：

            face -> face_guide.ma -> grp_md_face_guide_001
            arm  -> arm_guide.ma  -> grp_md_arm_guide_001

        当前项目只实际使用完整的 Face Guide 模板：

            resources/module_guide/face_guide.ma

        Face Guide 不在模板文件层面拆分 Brow、Eye、Nose、Mouth 等模块，
        后续真正构建 Joint / Controller 时再按照具体面部模块分别处理。

        module(str): Guide 模块名称，默认 "face"。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import guide_utils

        guide_object = guide_utils.Guide()

        print(guide_object.module)
        print(guide_object.guide_root_name)
        print(guide_object.guide_template_file_name)
        print(guide_object.guide_template_path)

        arm_guide_object = guide_utils.Guide("arm")
        """

        self.module = module

        self.guide_template_file_name = package_config.module_guide_template_file_format.format(self.module)
        self.guide_root_name = package_config.module_guide_root_name_format.format(self.module)
        self.guide_template_path = os.path.join(package_config.module_guide_dir, self.guide_template_file_name)

        self.guide_root = None
        self.guides = []

    def import_template(self):
        u"""
        导入当前 Module 的标准 Guide 模板，并返回 Guide Root。

        执行规则：

            1. 根据 module 自动得到模板文件名和 Guide Root 名称。
            2. 如果场景中已经存在 Guide Root，直接获取并复用。
            3. 如果不存在，则从 resources/module_guide 导入对应模板。
            4. 导入完成后再次检查 Guide Root，并保存为 PyNode。

        Returns:
            PyNode: 当前 Module Guide Root。

        Maya 使用示例：

        from muziToolset.core.rigging import guide_utils

        guide_object = guide_utils.Guide("face")
        guide_root = guide_object.import_template()

        print(guide_root)
        """

        if pm.objExists(self.guide_root_name):
            self.guide_root = pm.PyNode(self.guide_root_name)

            if not isinstance(self.guide_root, pm.nodetypes.Transform):
                raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(self.guide_root_name))

            return self.guide_root

        if not os.path.exists(self.guide_template_path):
            raise IOError(u"找不到 {} Guide 模板：{}".format(self.module, self.guide_template_path))

        pm.importFile(self.guide_template_path)

        if not pm.objExists(self.guide_root_name):
            raise RuntimeError(u"{} Guide 模板已经导入，但找不到 Guide Root：{}".format(self.module, self.guide_root_name))

        self.guide_root = pm.PyNode(self.guide_root_name)

        return self.guide_root

    def get_guides(self, module):
        u"""
        获取指定模块组下面全部 Locator Guide。

        Face Guide 模板作为整体导入，但真正读取和构建时按照面部模块分别处理。
        module 会按照统一命名规则转换成模块组名称：

            ear  -> grp_md_ear_guide_001
            eye  -> grp_md_eye_guide_001
            brow -> grp_md_brow_guide_001

        只扫描指定模块组下面的 Locator，不再一次获取整个 Face 的全部定位器。

        module(str): 需要获取 Guide 的面部模块名称，例如 "ear"、"eye"、"brow"。

        Returns:
            list: 指定模块下面全部 Locator Guide 的 PyNode 列表。

        Maya 使用示例：

        from muziToolset.core.rigging import guide_utils

        guide_object = guide_utils.Guide("face")
        guide_object.import_template()

        ear_guides = guide_object.get_guides("ear")

        for guide in ear_guides:
            print(guide)
        """

        if not self.guide_root:
            if pm.objExists(self.guide_root_name):
                self.guide_root = pm.PyNode(self.guide_root_name)
            else:
                pm.warning(u"当前场景中不存在 {} Guide：{}".format(self.module, self.guide_root_name))
                return []

        module_group_name = package_config.module_guide_root_name_format.format(module)

        if not pm.objExists(module_group_name):
            pm.warning(u"当前 Guide 中不存在模块组：{}".format(module_group_name))
            return []

        module_group = pm.PyNode(module_group_name)

        if not isinstance(module_group, pm.nodetypes.Transform):
            raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(module_group_name))

        if module_group != self.guide_root:
            module_parents = module_group.getAllParents()

            if self.guide_root not in module_parents:
                pm.warning(u"{} 不属于当前 Guide Root：{}".format(module_group_name, self.guide_root_name))
                return []

        child_objects = module_group.listRelatives(allDescendents=True, type="transform") or []

        self.guides = []

        for child_object in child_objects:
            child_shapes = child_object.getShapes(noIntermediate=True)

            for child_shape in child_shapes:
                if isinstance(child_shape, pm.nodetypes.Locator):
                    self.guides.append(child_object)
                    break

        return self.guides

    def create_guide_curve(self, module, side):
        u"""
        为指定 Guide 模块和方向创建一条实时显示曲线。

        左右两边分别创建独立 Curve，不再把 lf / rt Locator 连接到同一条曲线上。

        Curve CV 直接连接 Locator Shape 的 worldPosition：

            locatorShape.worldPosition[0]
                -> curveShape.controlPoints[index]

        这样不需要创建 multMatrix 或 decomposeMatrix 节点，
        并且读取的是 Locator 实际显示点的位置，而不是 Transform 的矩阵平移位置。

        Curve Transform 会关闭 inheritsTransform。
        因此 Curve 可以整理到对应模块组下面，同时 CV 仍然直接使用世界坐标。

        module(str): 需要创建显示曲线的模块名称，例如 "ear"、"brow"。
        side(str): Curve 方向，只接受 "lf"、"rt" 或 "md"。

        Returns:
            PyNode: 创建或已经存在的 Guide Display Curve Transform。

        Maya 使用示例：

        from muziToolset.core.rigging import guide_utils

        guide_object = guide_utils.Guide("face")
        guide_object.import_template()

        lf_curve = guide_object.create_guide_curve("ear", "lf")
        rt_curve = guide_object.create_guide_curve("ear", "rt")

        print(lf_curve)
        print(rt_curve)
        """

        if side not in ("lf", "rt", "md"):
            raise ValueError(u"side 只能使用 'lf'、'rt' 或 'md'，当前值：{}".format(side))

        guide_list = self.get_guides(module)

        side_guides = []

        for guide in guide_list:
            guide_name = guide.nodeName()
            name_parts = guide_name.split("_")

            if len(name_parts) > 1:
                if name_parts[1] == side:
                    side_guides.append(guide)

        if len(side_guides) < 2:
            pm.warning(u"{} {} Guide 少于两个 Locator，无法创建显示曲线。".format(side, module))
            return None

        # 当前命名中的序号已经使用 001、002、003 形式。
        # 直接按照节点名称排序即可得到稳定顺序。
        side_guides.sort(key=str)

        module_group_name = package_config.module_guide_root_name_format.format(module)
        module_group = pm.PyNode(module_group_name)

        curve_name = package_config.module_guide_curve_name_format.format(side, module)

        if pm.objExists(curve_name):
            guide_curve = pm.PyNode(curve_name)

            if not isinstance(guide_curve, pm.nodetypes.Transform):
                raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(curve_name))

            curve_shape = guide_curve.getShape()

            if not isinstance(curve_shape, pm.nodetypes.NurbsCurve):
                raise TypeError(u"{} 已经存在，但不是 NurbsCurve。".format(curve_name))

            return guide_curve

        # 使用 Locator Shape 的真实 World Position 创建初始 Degree 1 Curve。
        guide_positions = []

        for guide in side_guides:
            guide_shape = guide.getShape()
            guide_position = guide_shape.worldPosition[0].get()
            guide_positions.append(guide_position)

        guide_curve = pm.curve(
            point=guide_positions,
            degree=1,
            name=curve_name
        )

        # Curve CV 使用世界坐标，因此 Curve 自身不继承模块组 Transform。
        # 这样既可以整理层级，又不需要额外的矩阵空间转换节点。
        guide_curve.inheritsTransform.set(False)
        pm.parent(guide_curve, module_group, relative=True)

        curve_shape = guide_curve.getShape()
        first_guide_shape = side_guides[0].getShape()

        curve_shape.overrideEnabled.set(True)

        if first_guide_shape.overrideEnabled.get():
            if first_guide_shape.overrideRGBColors.get():
                curve_shape.overrideRGBColors.set(True)
                curve_shape.overrideColorRGB.set(first_guide_shape.overrideColorRGB.get())
            else:
                curve_shape.overrideColor.set(first_guide_shape.overrideColor.get())

        # Reference Display Type：曲线只用于显示，不能在 Maya 视图中被选择。
        curve_shape.overrideDisplayType.set(2)

        # Locator Shape World Position 直接驱动 Curve CV。
        guide_index = 0

        for guide in side_guides:
            guide_shape = guide.getShape()
            guide_shape.worldPosition[0] >> curve_shape.controlPoints[guide_index]
            guide_index += 1

        return guide_curve
