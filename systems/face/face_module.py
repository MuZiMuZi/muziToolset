# coding=utf-8
u"""
FaceModule：整个面部绑定系统的总调度模块。

FaceModule 不负责实现 Eye、Ear、Tongue 等具体部位的绑定算法，
它只负责把整个 Face Rig 的公共阶段统一组织起来。

当前流程：
    import_guide()
        -> 导入 resources/module_guide/face_guide.ma

    build_rig()
        -> 创建 Face Joint / Controller 两个总组
        -> 依次创建当前已经实现的面部子模块

    connect_rig()
        -> 依次执行每个面部子模块自己的连接逻辑

    delete_rig()
        -> 删除每个子模块自己的绑定结果
        -> 删除 Face Joint / Controller 两个总组
        -> 保留 face_guide.ma，方便继续调整 Guide 后重新 Build

设计原则：
    1. face_guide.ma 是整个面部绑定唯一的 Guide Template。
    2. FaceModule 负责整个 Face Rig 的生命周期和模块调度。
    3. EyeModule / EarModule / TongueModule 只负责自己的具体绑定算法。
    4. 子模块需要使用哪些 Locator，由 FaceModule 根据 face_guide_config 统一传入。
    5. UI 不参与这里的逻辑，后续 UI 只需要调用 FaceModule 的公开阶段方法。
"""

import os

import maya.cmds as cmds

from ... import config as package_config
from ...core.common import name_utils, hierarchy_utils
from . import face_guide_config
from .eye_module import EyeModule
from .ear_module import EarModule
from .tongue_module import TongueModule


class FaceModule(object):
    u"""统一管理整个 Face Rig 的 Guide、构建、连接和删除阶段。"""

    def __init__(self):
        u"""初始化 Face Rig 的稳定名称、Guide 配置和当前已有的面部子模块。"""

        # ---------------------------------------------------------------------
        # face_guide.ma 是整个面部唯一的 Guide Template。
        # 模板文件路径和 Guide Root 名称统一从全局配置读取，避免在不同模块中
        # 重复写资源路径和字符串名称。
        # ---------------------------------------------------------------------
        self.guide_template_path = os.path.join(package_config.module_guide_dir, face_guide_config.face_guide_template_file_name)
        self.guide_root = face_guide_config.face_guide_root_name

        # ---------------------------------------------------------------------
        # 整个 Face Rig 只创建一个 Joint 总组和一个 Controller 总组。
        # 每个子模块自己的模块组最终都会挂到这两个 Face 总组下面。
        # ---------------------------------------------------------------------
        self.jnt_master_grp = name_utils.Name(type="grp", side="md", part="face", function="jnt", index=1).name
        self.ctrl_master_grp = name_utils.Name(type="grp", side="md", part="face", function="ctrl", index=1).name

        # ---------------------------------------------------------------------
        # Eye Guide 使用明确的 Ball / Iris / Aim 语义名称。
        # Locator 名称全部来自 face_guide_config，不在这里重新手写 Naming 规则。
        # ---------------------------------------------------------------------
        lf_eye_guides = [
            face_guide_config.get_eye_locator("lf", "ball"),
            face_guide_config.get_eye_locator("lf", "iris"),
            face_guide_config.get_eye_locator("lf", "aim"),
        ]

        rt_eye_guides = [
            face_guide_config.get_eye_locator("rt", "ball"),
            face_guide_config.get_eye_locator("rt", "iris"),
            face_guide_config.get_eye_locator("rt", "aim"),
        ]

        # ---------------------------------------------------------------------
        # Ear 和 Tongue 都属于标准 Bind Locator。
        # Guide 的数量直接按照当前模块已经确定的绑定结构生成。
        # ---------------------------------------------------------------------
        lf_ear_guides = face_guide_config.get_bind_locator_names("lf", "ear", 3)
        rt_ear_guides = face_guide_config.get_bind_locator_names("rt", "ear", 3)
        tongue_guides = face_guide_config.get_bind_locator_names("md", "tongue", 5)

        # ---------------------------------------------------------------------
        # 当前已经实现的面部子模块统一在 FaceModule 中创建一次。
        # 子模块只拿自己需要的 Guide，并统一把模块 Joint / Ctrl 组挂到 Face 总组。
        # ---------------------------------------------------------------------
        self.lf_eye = EyeModule(side="lf", guide=lf_eye_guides, jnt_parent=self.jnt_master_grp, ctrl_parent=self.ctrl_master_grp)
        self.rt_eye = EyeModule(side="rt", guide=rt_eye_guides, jnt_parent=self.jnt_master_grp, ctrl_parent=self.ctrl_master_grp)
        self.lf_ear = EarModule(side="lf", guide=lf_ear_guides, jnt_parent=self.jnt_master_grp, ctrl_parent=self.ctrl_master_grp)
        self.rt_ear = EarModule(side="rt", guide=rt_ear_guides, jnt_parent=self.jnt_master_grp, ctrl_parent=self.ctrl_master_grp)
        self.tongue = TongueModule(side="md", guide=tongue_guides, jnt_parent=self.jnt_master_grp, ctrl_parent=self.ctrl_master_grp)

        # ---------------------------------------------------------------------
        # modules 保存整个 Face Rig 当前真正参与构建的模块顺序。
        # 后续增加 Brow / Eyelid / Mouth 时，只需要在这里增加实例并加入列表，
        # build / connect / delete 的总流程不需要重新改写。
        # ---------------------------------------------------------------------
        self.modules = [
            self.lf_eye,
            self.rt_eye,
            self.lf_ear,
            self.rt_ear,
            self.tongue,
        ]

    def import_guide(self):
        u"""
        导入整个面部绑定使用的 face_guide.ma 模板。

        如果 Guide Root 已经存在，说明模板已经在当前 Maya 场景中，
        此时直接返回，不重复导入，避免 Maya 自动产生重名节点。

        Returns:
            str:
                Face Guide Root 名称。
        """

        # Guide Root 已经存在时直接复用当前场景中的模板。
        if cmds.objExists(self.guide_root):
            return self.guide_root

        # 模板资源不存在时立即报错，避免 Maya 在一个错误路径上继续执行。
        if not os.path.isfile(self.guide_template_path):
            raise RuntimeError(u"找不到 Face Guide Template：{}".format(self.guide_template_path))

        # ---------------------------------------------------------------------
        # 直接把完整 face_guide.ma 导入当前 Maya 场景。
        # Eye / Ear / Tongue 等模块后续只读取模板中已经存在的 Locator。
        # ---------------------------------------------------------------------
        cmds.file(
            self.guide_template_path,
            i=True,
            type="mayaAscii",
            ignoreVersion=True
        )

        # 导入完成后再次确认 Guide Root，确保加载的确实是正确模板。
        if not cmds.objExists(self.guide_root):
            raise RuntimeError(u"Face Guide Template 导入完成，但找不到 Guide Root：{}".format(self.guide_root))

        return self.guide_root

    def setup_hierarchy(self):
        u"""
        创建整个 Face Rig 共用的 Joint / Controller 两个总组。

        子模块不会自己创建第二套 Face 总组，它们只保留自己的模块组，
        然后把模块组挂到这里创建的 Face 总组下面。

        Returns:
            tuple[str, str]:
                Face Joint 总组和 Controller 总组名称。
        """

        hierarchy_utils.get_or_create_group(self.jnt_master_grp)
        hierarchy_utils.get_or_create_group(self.ctrl_master_grp)

        return self.jnt_master_grp, self.ctrl_master_grp

    def build_rig(self):
        u"""
        创建整个 Face Rig 当前已经实现的 Joint / Controller 输出。

        执行顺序：
            1. 确认 face_guide.ma 已经导入。
            2. 创建 Face Joint / Controller 两个总组。
            3. 按 modules 顺序调用每个子模块的 build_rig()。

        这里只负责创建，不建立最终 Constraint / Matrix / Deformer 连接。
        connect_rig() 保持为独立阶段，方便在 Maya 中逐阶段测试。
        """

        # Build 前必须先有正式 Face Guide Template。
        # Guide 调整属于独立阶段，因此这里不会偷偷重新导入或覆盖模板。
        if not cmds.objExists(self.guide_root):
            raise RuntimeError(u"找不到 Face Guide，请先执行 FaceModule.import_guide()。")

        # 子模块 setup_hierarchy() 会把自己的模块组挂到这两个 Face 总组下面，
        # 所以必须先创建 Face 总组。
        self.setup_hierarchy()

        # 统一执行当前所有面部子模块的创建阶段。
        for module in self.modules:
            module.build_rig()

        return self.modules

    def connect_rig(self):
        u"""
        建立整个 Face Rig 当前已经实现模块的最终驱动连接。

        FaceModule 不知道具体模块使用 Aim Constraint、Parent Constraint、Matrix
        还是其他连接方式，只负责调用每个子模块自己的 connect_rig()。
        """

        for module in self.modules:
            module.connect_rig()

        return self.modules

    def delete_rig(self):
        u"""
        删除整个 Face Rig 的绑定输出，但保留 face_guide.ma。

        删除顺序：
            1. 每个子模块先删除自己创建的 Constraint 和模块 DAG 输出。
            2. 删除 Face Joint / Controller 两个总组。
            3. Guide Template 保留在场景中，可以继续调整后重新 build_rig()。

        Returns:
            list[str]:
                实际删除的 Face 总组名称。
        """

        # 子模块知道自己创建了哪些节点，所以由各自 delete_rig() 完成精确清理。
        for module in self.modules:
            module.delete_rig()

        # 子模块输出清理完成后，再删除已经为空的 Face 总组。
        delete_nodes = []

        if cmds.objExists(self.ctrl_master_grp):
            delete_nodes.append(self.ctrl_master_grp)

        if cmds.objExists(self.jnt_master_grp):
            delete_nodes.append(self.jnt_master_grp)

        if delete_nodes:
            cmds.delete(delete_nodes)

        return delete_nodes
