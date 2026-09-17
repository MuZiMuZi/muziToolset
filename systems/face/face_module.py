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

Eye 当前结构：
    FaceModule
        -> EyePairModule
            -> 左 EyeModule
            -> 右 EyeModule
            -> 中间 Aim 总控制器

设计原则：
    1. face_guide.ma 是整个面部绑定唯一的 Guide Template。
    2. FaceModule 负责整个 Face Rig 的生命周期和模块调度。
    3. EyePairModule 负责把左右 EyeModule 和中间 Aim 总控组合成完整双眼系统。
    4. EyeModule / EarModule / TongueModule 只负责自己的具体绑定算法。
    5. 子模块需要使用哪些 Locator，由 FaceModule 根据 face_guide_config 统一传入。
    6. UI 不参与这里的逻辑，后续 UI 只需要调用 FaceModule 的公开阶段方法。
"""

import os

import maya.cmds as cmds

from ... import config as package_config
from ...core.common import name_utils, hierarchy_utils
from . import face_guide_config
from .eye_pair_module import EyePairModule
from .ear_module import EarModule
from .tongue_module import TongueModule


class FaceModule(object):
    u"""统一管理整个 Face Rig 的 Guide、构建、连接和删除阶段。"""

    def __init__(self):
        u"""
        初始化 Face Rig 的稳定名称、Guide 配置和当前已有的面部子模块。
        """

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
        # Eye 不再由 FaceModule 分别管理两个独立 EyeModule。
        # EyePairModule 内部统一持有左右 EyeModule，并额外负责中间 Aim 总控。
        # ---------------------------------------------------------------------
        self.eye = EyePairModule(
            lf_guide=lf_eye_guides,
            rt_guide=rt_eye_guides,
            jnt_parent=self.jnt_master_grp,
            ctrl_parent=self.ctrl_master_grp
        )

        # 保留 lf_eye / rt_eye 两个直接入口。
        # 这样已有测试代码或后续需要单独访问某一只眼睛时，不需要改调用方式。
        self.lf_eye = self.eye.lf_eye
        self.rt_eye = self.eye.rt_eye

        # 其他已经存在的 Face 子模块继续保持原来的独立结构。
        self.lf_ear = EarModule(side="lf", guide=lf_ear_guides, jnt_parent=self.jnt_master_grp, ctrl_parent=self.ctrl_master_grp)
        self.rt_ear = EarModule(side="rt", guide=rt_ear_guides, jnt_parent=self.jnt_master_grp, ctrl_parent=self.ctrl_master_grp)
        self.tongue = TongueModule(side="md", guide=tongue_guides, jnt_parent=self.jnt_master_grp, ctrl_parent=self.ctrl_master_grp)

        # ---------------------------------------------------------------------
        # modules 保存整个 Face Rig 当前真正参与构建的模块顺序。
        # Eye 这里只加入 EyePairModule 一次，不能再把 lf_eye / rt_eye 单独加入，
        # 否则 FaceModule.build_rig() 会重复创建两只眼睛。
        # ---------------------------------------------------------------------
        self.modules = [
            self.eye,
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

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """

        # Guide Root 已经存在时直接复用当前场景中的模板。
        if cmds.objExists(self.guide_root):
            return self.guide_root

        # 模板资源不存在时立即报错，避免 Maya 在一个错误路径上继续执行。
        if not os.path.isfile(self.guide_template_path):
            raise RuntimeError(u"找不到 Face Guide Template：{}".format(self.guide_template_path))

        # 直接把完整 face_guide.ma 导入当前 Maya 场景。
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
                    tuple:
                        按当前 API 约定组织的结果元组。
                
        """

        hierarchy_utils.get_or_create_group(self.jnt_master_grp)
        hierarchy_utils.get_or_create_group(self.ctrl_master_grp)

        return self.jnt_master_grp, self.ctrl_master_grp

    def build_eyes(self):
        u"""

                只创建完整双眼系统，方便当前阶段在 Maya 中单独测试 Eye。

                创建内容：
                    1. 左眼 Ball / Iris Joint 和 Main / Aim Controller。
                    2. 右眼 Ball / Iris Joint 和 Main / Aim Controller。
                    3. 左右 Aim 中间的 ctrl_md_eye_aim_001 总控制器。
                这个方法不会创建 Ear / Tongue 等其他 Face Module。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。
                
        """

        if not cmds.objExists(self.guide_root):
            raise RuntimeError(u"找不到 Face Guide，请先执行 FaceModule.import_guide()。")

        self.setup_hierarchy()

        return self.eye.build_rig()

    def connect_eyes(self):
        u"""

                只建立双眼系统的正式连接。

                左右 EyeModule 分别建立自己的 Aim / Orient Constraint，
                中间 Aim 总控再通过 Point Constraint 驱动左右 Aim Driven Group。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。
                
        """

        return self.eye.connect_rig()

    def delete_eyes(self):
        u"""

                只删除双眼系统，保留 Face Guide 和 Face 总组。

                适合当前 Eye 开发阶段反复执行：
                    调整 Guide -> build_eyes() -> connect_eyes() -> delete_eyes()

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。
                
        """

        return self.eye.delete_rig()

    def build_rig(self):
        u"""

                创建整个 Face Rig 当前已经实现的 Joint / Controller 输出。

                执行顺序：
                    1. 确认 face_guide.ma 已经导入。
                    2. 创建 Face Joint / Controller 两个总组。
                    3. 按 modules 顺序调用每个子模块的 build_rig()。
                这里只负责创建，不建立最终 Constraint / Matrix / Deformer 连接。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。
                
        """

        if not cmds.objExists(self.guide_root):
            raise RuntimeError(u"找不到 Face Guide，请先执行 FaceModule.import_guide()。")

        self.setup_hierarchy()

        for module in self.modules:
            module.build_rig()

        return self.modules

    def connect_rig(self):
        u"""

                建立整个 Face Rig 当前已经实现模块的最终驱动连接。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。
                
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
                    object:
                        当前 API 完成处理后返回的结果。
                
        """

        for module in self.modules:
            module.delete_rig()

        delete_nodes = []

        if cmds.objExists(self.ctrl_master_grp):
            delete_nodes.append(self.ctrl_master_grp)

        if cmds.objExists(self.jnt_master_grp):
            delete_nodes.append(self.jnt_master_grp)

        if delete_nodes:
            cmds.delete(delete_nodes)

        return delete_nodes
