# coding=utf-8
u"""
guide_utils：Maya Module Guide 基础工具。

方法介绍与使用场景：

    Guide.__init__
        创建一个 Module Guide 工具对象。
        根据 module 名称自动生成统一的 Guide 模板文件名、Guide Root 名称和模板路径。

    Guide.import_template
        导入当前 Module 对应的 Maya Guide 模板。
        Guide Display Curve 作为模板内容一起保存和导入，不在正常运行时额外创建。

    Guide.get_guides
        根据模块名称获取该模块组下面所有 Locator Guide。
        适合后续按模块创建 Joint、Controller。

    Guide.create_guide_curve
        根据指定模块和方向创建 Guide Display Curve。
        这个方法保留给制作或更新 Guide 模板时使用，不属于正常绑定构建流程。
"""

import os

import maya.cmds as cmds
import pymel.core as pm

from ... import config as package_config


class Guide(object):

    def __init__(self, module="face"):
        u"""
        初始化 Module Guide 工具对象。

        module(str): Guide 模块名称，默认 "face"。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import guide_utils

        guide_object = guide_utils.Guide("face")

        print(guide_object.guide_root_name)
        print(guide_object.guide_template_path)
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

        Guide Display Curve 属于模板本身的一部分。
        正常使用时只需要导入模板，不需要再额外调用 create_guide_curve()。

        Returns:
            PyNode: 当前 Module Guide Root。

        Maya 使用示例：

        from muziToolset.core.rigging import guide_utils

        guide_object = guide_utils.Guide("face")
        guide_root = guide_object.import_template()

        print(guide_root)
        """

        if cmds.objExists(self.guide_root_name):
            if cmds.nodeType(self.guide_root_name) != "transform":
                raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(self.guide_root_name))

            self.guide_root = pm.PyNode(self.guide_root_name)
            return self.guide_root

        if not os.path.exists(self.guide_template_path):
            raise IOError(u"找不到 {} Guide 模板：{}".format(self.module, self.guide_template_path))

        cmds.file(self.guide_template_path, i=True, type="mayaAscii", ignoreVersion=True, mergeNamespacesOnClash=False, namespace=":", options="v=0;")

        if not cmds.objExists(self.guide_root_name):
            raise RuntimeError(u"{} Guide 模板已经导入，但找不到 Guide Root：{}".format(self.module, self.guide_root_name))

        self.guide_root = pm.PyNode(self.guide_root_name)
        return self.guide_root

    def get_guides(self, module):
        u"""
        获取指定模块组下面全部 Locator Guide。

        Face Guide 模板作为整体导入，但真正读取和构建时按照面部模块分别处理。

        module(str): 需要获取 Guide 的模块名称，例如 "ear"、"eye"、"brow"。

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
            if cmds.objExists(self.guide_root_name):
                self.guide_root = pm.PyNode(self.guide_root_name)
            else:
                cmds.warning(u"当前场景中不存在 {} Guide：{}".format(self.module, self.guide_root_name))
                return []

        module_group_name = package_config.module_guide_root_name_format.format(module)

        if not cmds.objExists(module_group_name):
            cmds.warning(u"当前 Guide 中不存在模块组：{}".format(module_group_name))
            return []

        if cmds.nodeType(module_group_name) != "transform":
            raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(module_group_name))

        module_parent_list = cmds.listRelatives(module_group_name, allParents=True, fullPath=False) or []

        if module_group_name != self.guide_root_name:
            current_parent = module_parent_list
            found_guide_root = False

            while current_parent:
                parent_name = current_parent[0]

                if parent_name == self.guide_root_name:
                    found_guide_root = True
                    break

                current_parent = cmds.listRelatives(parent_name, allParents=True, fullPath=False) or []

            if not found_guide_root:
                cmds.warning(u"{} 不属于当前 Guide Root：{}".format(module_group_name, self.guide_root_name))
                return []

        child_objects = cmds.listRelatives(module_group_name, allDescendents=True, type="transform", fullPath=False) or []

        self.guides = []

        for child_object in child_objects:
            child_shapes = cmds.listRelatives(child_object, shapes=True, noIntermediate=True, fullPath=False) or []

            for child_shape in child_shapes:
                if cmds.nodeType(child_shape) == "locator":
                    self.guides.append(pm.PyNode(child_object))
                    break

        return self.guides

    def create_guide_curve(self, module, side):
        u"""
        为指定 Guide 模块和方向创建一条 Guide Display Curve。

        这个方法主要用于制作或更新 Guide 模板。
        正常绑定流程中，Display Curve 应该已经保存到 <module>_guide.ma 模板里，
        import_template() 导入模板时会一起进入场景，不需要再次创建。

        Locator Shape 的 worldPosition 直接连接 Curve Shape 的 controlPoints，
        不额外创建 multMatrix 或 decomposeMatrix 节点。

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
        """

        if side not in ("lf", "rt", "md"):
            raise ValueError(u"side 只能使用 'lf'、'rt' 或 'md'，当前值：{}".format(side))

        guide_list = self.get_guides(module)
        side_guides = []

        for guide in guide_list:
            guide_name = guide.nodeName()
            name_parts = guide_name.split("_")

            if len(name_parts) > 1 and name_parts[1] == side:
                side_guides.append(guide)

        if len(side_guides) < 2:
            cmds.warning(u"{} {} Guide 少于两个 Locator，无法创建显示曲线。".format(side, module))
            return None

        side_guides.sort(key=str)

        module_group_name = package_config.module_guide_root_name_format.format(module)
        curve_name = package_config.module_guide_curve_name_format.format(side, module)

        if cmds.objExists(curve_name):
            if cmds.nodeType(curve_name) != "transform":
                raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(curve_name))

            curve_shapes = cmds.listRelatives(curve_name, shapes=True, noIntermediate=True, fullPath=False) or []

            if not curve_shapes or cmds.nodeType(curve_shapes[0]) != "nurbsCurve":
                raise TypeError(u"{} 已经存在，但不是 NurbsCurve。".format(curve_name))

            return pm.PyNode(curve_name)

        guide_positions = []

        for guide in side_guides:
            guide_shape = guide.getShape()
            guide_position = cmds.getAttr(guide_shape.name() + ".worldPosition[0]")[0]
            guide_positions.append(guide_position)

        guide_curve = cmds.curve(point=guide_positions, degree=1, name=curve_name)
        cmds.setAttr(guide_curve + ".inheritsTransform", 0)
        cmds.parent(guide_curve, module_group_name, relative=True)

        curve_shape = cmds.listRelatives(guide_curve, shapes=True, noIntermediate=True, fullPath=False)[0]
        first_guide_shape = side_guides[0].getShape().name()

        cmds.setAttr(curve_shape + ".overrideEnabled", 1)

        if cmds.getAttr(first_guide_shape + ".overrideEnabled"):
            if cmds.getAttr(first_guide_shape + ".overrideRGBColors"):
                guide_color = cmds.getAttr(first_guide_shape + ".overrideColorRGB")[0]
                cmds.setAttr(curve_shape + ".overrideRGBColors", 1)
                cmds.setAttr(curve_shape + ".overrideColorRGB", guide_color[0], guide_color[1], guide_color[2])
            else:
                guide_color = cmds.getAttr(first_guide_shape + ".overrideColor")
                cmds.setAttr(curve_shape + ".overrideColor", guide_color)

        cmds.setAttr(curve_shape + ".overrideDisplayType", 2)

        guide_index = 0

        for guide in side_guides:
            guide_shape = guide.getShape().name()
            source_attr = guide_shape + ".worldPosition[0]"
            target_attr = curve_shape + ".controlPoints[{}]".format(guide_index)
            cmds.connectAttr(source_attr, target_attr, force=True)
            guide_index += 1

        return pm.PyNode(guide_curve)
