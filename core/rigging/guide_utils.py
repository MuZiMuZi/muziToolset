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
        根据指定模块下面的 Locator 创建一条 Degree 1 Guide Display Curve。
        Curve CV 会实时跟随 Locator，并设置为不可在视图中选择，只用于辅助显示模块定位关系。
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

        # 保存当前 Guide 所属模块名称。
        # 例如 face、arm、leg。
        self.module = module

        # 根据 config.py 中的统一命名规则生成 Guide 静态信息。
        self.guide_template_file_name = package_config.module_guide_template_file_format.format(self.module)
        self.guide_root_name = package_config.module_guide_root_name_format.format(self.module)
        self.guide_template_path = os.path.join(package_config.module_guide_dir, self.guide_template_file_name)

        # 以下属性属于当前 Maya Scene 的运行状态，不放到 config.py。
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

    def create_guide_curve(self, module):
        u"""
        为指定 Guide 模块创建一条实时显示曲线。

        Curve 只负责辅助显示 Locator 之间的定位关系，不参与 Joint、Controller 或绑定计算。
        当前第一版统一使用 Degree 1 Curve，让曲线直接经过每一个 Locator 定位点。

        Curve 创建后会：

            1. 获取指定模块下面全部 Locator Guide。
            2. 按 Locator 名称排序，保证重复执行时顺序稳定。
            3. 创建 crv_md_<module>_guide_001。
            4. 将 Curve 放到对应模块组下面。
            5. 使用 multMatrix + decomposeMatrix 将 Locator 世界位置转换到模块局部空间。
            6. 将转换后的 Translate 实时连接到对应 Curve CV。
            7. 将 Curve Shape 设置为 Reference Display Type，使其在 Maya 视图中不可选择。
            8. 尽量继承第一个 Locator Shape 的显示颜色，用来区分不同 Guide 模块。

        module(str): 需要创建显示曲线的面部模块名称，例如 "ear"、"brow"。

        Returns:
            PyNode: 创建或已经存在的 Guide Display Curve Transform。

        Maya 使用示例：

        from muziToolset.core.rigging import guide_utils

        guide_object = guide_utils.Guide("face")
        guide_object.import_template()

        ear_curve = guide_object.create_guide_curve("ear")

        print(ear_curve)
        """

        guide_list = self.get_guides(module)

        if len(guide_list) < 2:
            pm.warning(u"{} Guide 少于两个 Locator，无法创建显示曲线。".format(module))
            return None

        # 使用节点名称排序，让同一个模块每次构建时得到稳定的 CV 顺序。
        guide_list.sort(key=str)

        module_group_name = package_config.module_guide_root_name_format.format(module)
        module_group = pm.PyNode(module_group_name)

        curve_name = package_config.module_guide_curve_name_format.format(module)

        # 已经存在同名显示曲线时直接复用，避免重复创建 Curve 和驱动节点。
        if pm.objExists(curve_name):
            guide_curve = pm.PyNode(curve_name)

            if not isinstance(guide_curve, pm.nodetypes.Transform):
                raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(curve_name))

            curve_shape = guide_curve.getShape()

            if not isinstance(curve_shape, pm.nodetypes.NurbsCurve):
                raise TypeError(u"{} 已经存在，但不是 NurbsCurve。".format(curve_name))

            return guide_curve

        # 先使用 Locator 的世界位置创建 Degree 1 Curve。
        guide_positions = []

        for guide in guide_list:
            guide_position = guide.getTranslation(space="world")
            guide_positions.append(guide_position)

        guide_curve = pm.curve(
            point=guide_positions,
            degree=1,
            name=curve_name
        )

        # 显示曲线属于对应模块组。
        # Parent 后冻结自身 Transform，让 Curve CV 使用模块组局部空间坐标。
        pm.parent(guide_curve, module_group, absolute=True)
        pm.makeIdentity(guide_curve, apply=True, translate=True, rotate=True, scale=True)

        curve_shape = guide_curve.getShape()

        # 复制当前模块第一个 Locator 的显示颜色。
        first_guide_shape = guide_list[0].getShape()

        curve_shape.overrideEnabled.set(True)

        if first_guide_shape and first_guide_shape.hasAttr("overrideEnabled"):
            if first_guide_shape.overrideEnabled.get():
                if first_guide_shape.hasAttr("overrideRGBColors") and first_guide_shape.overrideRGBColors.get():
                    curve_shape.overrideRGBColors.set(True)
                    curve_shape.overrideColorRGB.set(first_guide_shape.overrideColorRGB.get())
                else:
                    curve_shape.overrideColor.set(first_guide_shape.overrideColor.get())

        # Reference Display Type：曲线可以显示，但不能在 Maya 视图中被选择。
        curve_shape.overrideDisplayType.set(2)

        # 每一个 Locator 对应一个 Curve CV。
        # Locator World Matrix 先转换到 Module Group Local Space，
        # 再把局部位置实时连接到 Curve Shape 的 controlPoints。
        guide_index = 0

        for guide in guide_list:
            mult_matrix = pm.createNode("multMatrix")
            decompose_matrix = pm.createNode("decomposeMatrix")

            guide.worldMatrix[0] >> mult_matrix.matrixIn[0]
            module_group.worldInverseMatrix[0] >> mult_matrix.matrixIn[1]

            mult_matrix.matrixSum >> decompose_matrix.inputMatrix
            decompose_matrix.outputTranslate >> curve_shape.controlPoints[guide_index]

            guide_index += 1

        return guide_curve
