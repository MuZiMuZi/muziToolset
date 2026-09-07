# coding=utf-8
u"""
guide_utils：Maya Face Guide 基础工具。

方法介绍与使用场景：

    Guide.__init__
        创建一个 Face Guide 工具对象，并准备标准 Guide Root 和模板路径。
        当前 Face Guide 作为一个整体模板管理，不拆分 Brow、Eye、Mouth 等独立模板。

    Guide.import_template
        导入标准 Face Guide Maya 模板。
        如果场景中已经存在 Guide Root，则直接获取并复用，不重复导入模板。

    Guide.get_guides
        获取当前 Face Guide Root 下面所有 Locator Guide。
        适合后续创建 Joint、Controller 或保存 Guide 数据时统一读取定位器。
"""

import os

import pymel.core as pm

from ... import config as package_config


class Guide(object):

    def __init__(self):
        u"""
        初始化 Face Guide 工具对象。

        当前 Guide Core 第一版只管理一个完整的 Face Guide 模板：

        resources/module_guide/face_guide.ma

        Face Guide 不在模板文件层面拆分 Brow、Eye、Nose、Mouth 等模块，
        后续真正构建 Joint / Controller 时再按照具体面部模块分别处理。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.rigging import guide_utils

        guide_object = guide_utils.Guide()

        print(guide_object.guide_root_name)
        print(guide_object.face_guide_template_path)
        """

        # Face Guide 的统一根组名称。
        # 所有 Face Guide 节点都应该位于这个根组下面。
        self.guide_root_name = "grp_md_face_guide_001"

        # 保存场景中的 Guide Root PyNode。
        # import_template() 或 get_guides() 找到 Guide Root 后会更新该属性。
        self.guide_root = None

        # 当前 Face Guide 使用一个完整 Maya ASCII 模板，不按面部模块拆分文件。
        self.face_guide_template_file_name = "face_guide.ma"

        # 模板统一存放在 resources/module_guide 目录。
        self.face_guide_template_path = os.path.join(
            package_config.module_guide_dir,
            self.face_guide_template_file_name
        )

        # 保存 get_guides() 最后获取到的 Locator Guide PyNode。
        self.guides = []

    def import_template(self):
        u"""
        导入标准 Face Guide 模板，并返回 Guide Root。

        执行规则：

            1. 如果场景中已经存在 grp_md_face_guide_001，直接获取并复用。
            2. 如果不存在，则导入 resources/module_guide/face_guide.ma。
            3. 导入完成后再次检查 Guide Root，并保存为 PyNode。

        这样可以避免重复点击创建 Guide 时，在场景中重复导入整套 Face Guide。

        Returns:
            PyNode: Face Guide Root。

        Maya 使用示例：

        from muziToolset.core.rigging import guide_utils

        guide_object = guide_utils.Guide()
        guide_root = guide_object.import_template()

        print(guide_root)
        """

        # 如果 Guide Root 已经存在，说明 Face Guide 已经在当前场景中。
        # 直接获取已有节点，不再次导入模板。
        if pm.objExists(self.guide_root_name):
            self.guide_root = pm.PyNode(self.guide_root_name)

            # Guide Root 必须是 Transform，避免同名其他节点被误当成 Guide 根组。
            if not isinstance(self.guide_root, pm.nodetypes.Transform):
                raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(self.guide_root_name))

            return self.guide_root

        # 导入前先检查模板文件是否真实存在。
        # 路径错误时直接报出明确错误，方便快速定位资源问题。
        if not os.path.exists(self.face_guide_template_path):
            raise IOError(u"找不到 Face Guide 模板：{}".format(self.face_guide_template_path))

        # 导入完整 Face Guide Maya 模板。
        # 当前模板只负责 Guide 的默认 Shape、层级和初始位置。
        pm.importFile(self.face_guide_template_path)

        # 模板导入完成后必须能够找到标准 Guide Root。
        # 如果找不到，说明模板本身的根组命名不符合当前 Guide Core 约定。
        if not pm.objExists(self.guide_root_name):
            raise RuntimeError(u"Face Guide 模板已经导入，但找不到 Guide Root：{}".format(self.guide_root_name))

        # 将 Guide Root 保存为 PyNode，后续统一使用 PyMEL 操作。
        self.guide_root = pm.PyNode(self.guide_root_name)

        return self.guide_root

    def get_guides(self):
        u"""
        获取 Face Guide Root 下面全部 Locator Guide。

        当前 Face Guide 模板中除了真正的定位器外，还可能包含：

            grp_*   层级组
            zero_*  归零组
            ctrl_*  Guide 显示或整体移动控制器

        因此这里不单纯依赖名称字符串判断，而是检查 Transform 下面是否拥有 Locator Shape。
        只有真正的 Locator Transform 才会加入最终 Guide 列表。

        Returns:
            list: Face Guide Root 下全部 Locator Guide 的 PyNode 列表。

        Maya 使用示例：

        from muziToolset.core.rigging import guide_utils

        guide_object = guide_utils.Guide()
        guide_object.import_template()

        guide_list = guide_object.get_guides()

        for guide in guide_list:
            print(guide)
        """

        # 如果当前实例还没有保存 Guide Root，则尝试从 Maya 场景中获取。
        if not self.guide_root:
            if pm.objExists(self.guide_root_name):
                self.guide_root = pm.PyNode(self.guide_root_name)
            else:
                pm.warning(u"当前场景中不存在 Face Guide：{}".format(self.guide_root_name))
                return []

        # 获取 Guide Root 下面全部 Transform 后代节点。
        child_objects = self.guide_root.listRelatives(allDescendents=True, type="transform") or []

        # 每次调用重新整理 Guide 列表，避免保存旧场景中的 PyNode。
        self.guides = []

        # 逐个检查 Transform 的 Shape。
        # 只保存真正拥有 Locator Shape 的 Transform。
        for child_object in child_objects:
            child_shapes = child_object.getShapes(noIntermediate=True)

            for child_shape in child_shapes:
                if isinstance(child_shape, pm.nodetypes.Locator):
                    self.guides.append(child_object)
                    break

        return self.guides
