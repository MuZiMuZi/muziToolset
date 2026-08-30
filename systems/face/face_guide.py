# coding=utf-8
u"""
Step 02 - Face Guide
====================

Face Guide Manager。

Step 生命周期：
    collect_inputs()
    prepare_data()
    process_data()
    finalize_step()

Step 02 有两个不同层级的操作：

1. build_guide()
    Step 内部的编辑准备工具，只负责导入 / 复用可编辑的 Face Guide Template。

2. run_step()
    继承自 systems.common.StepBase，代表用户点击“下一步”正式提交 Step 02。
    它会重新检查当前 Guide，Validation 通过后保存 Config 并完成当前 Step。

职责：
    1. 读取 Step 01 保存的公共 Face Setup 数据；
    2. 管理 resources/face/face_guide.ma 模板的导入 / 删除 / 重置；
    3. 提供统一的 Guide Locator 查询和世界坐标读取接口；
    4. 按 Face 部位整理 Guide 数据，供后续 Builder 使用；
    5. 检查 Guide 完整性和左右镜像连接；
    6. 在镜像结构损坏时提供 Repair Symmetry；
    7. 正式提交 Step 02，并把 Guide 状态保存到 Face Config。

重要边界：
    - DAG Short Name 统一复用 core.rename_utils；
    - 世界位置查询统一复用 core.transform_utils；
    - DAG Parent 修改统一复用 core.hierarchy_utils；
    - DG Plug 连接统一复用 core.connection_utils；
    - Scene Import / Generic Node Create 统一复用 core.scene_utils；
    - Locator 颜色、初始层级、左右节点和默认连接属于 face_guide.ma 模板；
    - Lip / Brow / Eyelid Curve 和 Joint 不在这里创建；
    - 后续 Builder 只消费 FaceGuide 输出的有序 Guide 数据。

兼容：
    - build() 保留为旧入口，内部只转调 build_guide()；
    - finalize() 保留为旧入口，内部转调统一 run_step()；
    - mirror_left_guide() / mirror_left_guides() 继续保留 Repair Symmetry 兼容 API。
"""

from __future__ import print_function

import os

import maya.cmds as cmds

from ... import config as package_config
from ...core import connection_utils
from ...core import file_utils
from ...core import hierarchy_utils
from ...core import rename_utils
from ...core import scene_utils
from ...core import transform_utils
from . import face_base


class FaceGuide(face_base.FaceBase):
    u"""Face Rig Step 02 - Guide 管理器。"""

    guide_template_file_name = "face_guide.ma"
    guide_move_ctrl_name = "ctrl_md_face_move_001"
    guide_version = "1.0"

    required_guide_names = [
        "loc_md_upper_lip_guide_001",
        "loc_md_lower_lip_guide_001",
        "loc_lf_mouth_corner_guide_001",
        "loc_rt_mouth_corner_guide_001",
        "loc_lf_eye_ball_guide_001",
        "loc_rt_eye_ball_guide_001",
    ]

    def __init__(self):
        u"""
        初始化 Face Guide Step。
        """
        super(FaceGuide, self).__init__()

        self.step_value = 2

        self.guide_root = None
        self.guide_move_ctrl = None

        # Step 正式提交时默认同时检查 LF -> RT 镜像完整性。
        self.check_symmetry = True
        self.validation_result = None

        # Config 已存在时读取 Step 01 最新输入；新场景保持空值，真正执行时再严格检查。
        if self.config_node_exists():
            self.refresh_setup_data()

        # 初始化当前场景中已经存在的 Guide Root / Move Ctrl 引用。
        self.refresh_guide_handles()

    # =========================================================================
    # Step Lifecycle - “下一步”正式提交 Step 02
    # =========================================================================

    def collect_inputs(self):
        u"""
        收集并检查 Step 02 正式提交所需输入。

        本阶段确认：
            1. Step 01 Config 有效；
            2. 当前场景已经存在可提交的 Face Guide。

        Returns:
            bool:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # 重新读取并检查 Step 01 保存的 Head / Eye / Mouth Joint 等公共输入。
        self.validate_setup()

        # 刷新当前场景中的 Guide Root 和 Move Ctrl，避免继续使用旧 DAG 引用。
        self.refresh_guide_handles()

        # 正式提交前必须已经加载 Guide Template，空 Guide Group 不能进入 Step 03。
        if not self.guide_exists():
            raise RuntimeError(
                u"Face Guide 尚未加载，请先执行 Build Face Guide。"
            )

        return True

    def prepare_data(self):
        u"""
        准备 Step 02 Finalize 使用的系统环境。

        本阶段不修改用户 Guide 调整，只确保 Face Hierarchy 和 Config 可以正常保存结果。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        # 确保 Face 系统基础层级仍然完整，避免外部删除 Group 后继续保存错误状态。
        self.ensure_hierarchy()

        # 创建或复用统一 Face Config Network Node，给 Finalize 提供持久化目标。
        self.ensure_config_node()

        return True

    def process_data(self):
        u"""
        检查当前用户调整后的 Face Guide 是否可以交给 Step 03。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # 对必要 Guide、重复命名和左右镜像结构执行完整 Validation。
        self.validation_result = self.validate_guides(
            check_symmetry=self.check_symmetry
        )

        if self.validation_result["valid"]:
            return self.validation_result

        error_message = u"Face Guide Validation 失败："

        for error in self.validation_result["errors"]:
            error_message += u"\n- {}".format(
                error
            )

        raise RuntimeError(
            error_message
        )

    def finalize_step(self):
        u"""
        保存当前 Guide，并把 Step 02 正式标记为完成。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        # 保存当前 Guide Root / Move Ctrl / Version，给后续 Face Builder 读取。
        self.save_guide_config()

        # Validation 已通过，把 Step 02 标记为 Completed。
        self.set_step_completed(
            completed=True
        )

        # Step 02 被重新提交后让 Step 03～04 的旧完成状态失效。
        self.invalidate_later_steps()

        return True

    # =========================================================================
    # Setup
    # =========================================================================

    def validate_setup(self):
        u"""
        检查 Step 02 所依赖的 Step 01 公共数据。

        Returns:
            object:
                方法执行后的结果数据。
        """
        # 使用 FaceBase 统一检查 Step 01 Config 和公共模型输入。
        return self.validate_setup_config(
            require_mouth_jnt_number=True
        )

    # =========================================================================
    # Name / DAG Helper - Compatibility
    # =========================================================================

    @staticmethod
    def get_short_name(node):
        u"""
        返回 DAG Short Name。

        保留 FaceGuide 旧调用入口，实际规则统一由 core.rename_utils 维护。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Returns:
            object:
                方法执行后的结果数据。
        """
        # 统一复用项目级 Short Name API，避免 FaceGuide 维护第二套 split("|") 规则。
        return rename_utils.get_short_name(
            node
        )

    @staticmethod
    def get_dag_depth(node):
        u"""
        返回 DAG Path 深度，用于父节点优先排序。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Returns:
            object | int:
                方法执行后的结果数据。
        """
        if not node:
            return 0

        return node.count("|")

    @staticmethod
    def get_parent(node):
        u"""
        返回节点的直接 Parent Long Path。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Returns:
            object | None:
                方法执行后的结果数据。
        """
        if not node:
            return None

        if not cmds.objExists(node):
            return None

        parents = cmds.listRelatives(
            node,
            parent=True,
            fullPath=True
        )

        if parents is None:
            parents = []

        if not parents:
            return None

        return parents[0]

    @staticmethod
    def get_locator_shapes(locator):
        u"""
        获取 Locator Transform 下全部有效 Locator Shape。

        Args:
            locator (str):
                Face Guide 系统中的 Locator Transform。

        Returns:
            object | list:
                方法执行后的结果数据。
        """
        if not locator:
            return []

        if not cmds.objExists(locator):
            return []

        shapes = cmds.listRelatives(
            locator,
            shapes=True,
            noIntermediate=True,
            fullPath=True,
            type="locator"
        )

        if shapes is None:
            shapes = []

        return shapes

    def get_node_under_parent(
            self,
            parent,
            short_name
    ):
        u"""
        获取指定 Parent 下的直接子 Transform。

        Args:
            parent (str):
                父级 Maya 节点名称。
            short_name (str):
                `short_name` 对应的 Maya 节点或资源名称。

        Returns:
            None | object:
                方法执行后的结果数据。
        """
        if not short_name:
            return None

        if parent:
            if not cmds.objExists(parent):
                return None

            children = cmds.listRelatives(
                parent,
                children=True,
                type="transform",
                fullPath=True
            )

            if children is None:
                children = []

            for child in children:
                # 使用统一 Short Name 规则比较 Child，避免 Parent Path 影响名称判断。
                child_short_name = self.get_short_name(
                    child
                )

                if child_short_name == short_name:
                    return child

            return None

        matches = cmds.ls(
            short_name,
            type="transform",
            long=True
        )

        if matches is None:
            matches = []

        if len(matches) == 1:
            return matches[0]

        return None

    # =========================================================================
    # Guide Template
    # =========================================================================

    def get_guide_template_path(self):
        u"""
        返回 face_guide.ma 的规范绝对路径。

        Returns:
            object:
                方法执行后的结果数据。
        """
        template_path = os.path.join(
            package_config.resources_dir,
            "face",
            self.guide_template_file_name
        )

        # 使用 File Core 统一规范路径分隔符和路径格式。
        template_path = file_utils.normalize_path(
            template_path
        )

        return template_path

    def validate_guide_template_file(self):
        u"""
        检查 Face Guide 模板文件是否存在。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # 获取项目 resources/face 下正式 Guide Template 路径。
        template_path = self.get_guide_template_path()

        if not os.path.isfile(template_path):
            raise RuntimeError(
                u"Face Guide 模板文件不存在: {}".format(
                    template_path
                )
            )

        return template_path

    def refresh_guide_handles(self):
        u"""
        刷新当前场景中的 Guide Root 和 Face Move Ctrl 引用。

        Returns:
            object | bool:
                方法执行后的结果数据。
        """
        self.guide_root = None
        self.guide_move_ctrl = None

        if not cmds.objExists(self.face_guide_grp):
            return False

        self.guide_root = self.face_guide_grp

        # 在正式 Guide Group 下查找 Template 的 Move Ctrl，判断 Guide 内容是否真实存在。
        move_ctrl = self.get_node_under_parent(
            self.face_guide_grp,
            self.guide_move_ctrl_name
        )

        if move_ctrl:
            self.guide_move_ctrl = move_ctrl

        return bool(self.guide_move_ctrl)

    def guide_exists(self):
        u"""
        检查正式 Guide 内容是否已经加载。

        FaceBase 创建的空 Guide Group 不代表模板已经加载，因此同时要求 Move Ctrl 存在。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        # 每次查询前刷新 DAG 引用，保证 Reparent / Reset 后状态准确。
        self.refresh_guide_handles()

        if not self.guide_root:
            return False

        if not self.guide_move_ctrl:
            return False

        return True

    def get_imported_template_root(self, imported_nodes):
        u"""
        从本次 Import 的新节点中找到模板临时 Root。

        Args:
            imported_nodes (list[str]):
                本次导入 face_guide.ma 后 Maya 返回的新节点列表。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        imported_transforms = cmds.ls(
            imported_nodes,
            type="transform",
            long=True
        )

        if imported_transforms is None:
            imported_transforms = []

        root_candidates = []

        for node in imported_transforms:
            # 查询导入 Transform 的直接 Parent，只有无 Parent 的节点才可能是 Template Root。
            parent = self.get_parent(
                node
            )

            if parent:
                continue

            # 使用统一 Short Name 规则判断导入 Root 是否属于 Face Guide。
            short_name = self.get_short_name(
                node
            )

            if not short_name.startswith(
                    "grp_md_face_guide_"
            ):
                continue

            root_candidates.append(
                node
            )

        if len(root_candidates) != 1:
            raise RuntimeError(
                u"无法唯一识别导入的 Face Guide 模板 Root，候选数量: {}".format(
                    len(root_candidates)
                )
            )

        return root_candidates[0]

    def merge_imported_template_root(self, template_root):
        u"""
        把模板临时 Root 的内容合并到正式 Face Guide Group。

        Args:
            template_root (str):
                刚导入的 Face Guide 模板临时 Root，用于合并到正式 Guide Group。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if not cmds.objExists(self.face_guide_grp):
            raise RuntimeError(
                u"正式 Face Guide Group 不存在: {}".format(
                    self.face_guide_grp
                )
            )

        children = cmds.listRelatives(
            template_root,
            children=True,
            type="transform",
            fullPath=True
        )

        if children is None:
            children = []

        if not children:
            raise RuntimeError(
                u"导入的 Face Guide 模板 Root 下没有可合并内容: {}".format(
                    template_root
                )
            )

        merged_nodes = []

        # 把临时 Template Root 的全部 Transform Child 移入正式 Face Guide Group。
        for child in children:
            merged_node = hierarchy_utils.Hierarchy.parent(
                child,
                self.face_guide_grp
            )

            if not merged_node:
                continue

            merged_nodes.append(
                merged_node
            )

        if cmds.objExists(template_root):
            cmds.delete(
                template_root
            )

        return merged_nodes

    def import_guide_template(self):
        u"""
        导入或复用 Face Guide Template。

        如果 Guide 已存在，则不重复导入。

        Returns:
            dict:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # 确保正式 Face Guide Group 已经存在，给 Template 合并提供稳定父级。
        self.ensure_hierarchy()

        # 当前 Guide 已经加载时直接复用，不重复创建第二套 Template。
        if self.guide_exists():
            return {
                "imported": False,
                "guide_root": self.guide_root,
                "guide_move_ctrl": self.guide_move_ctrl,
                "new_nodes": [],
            }

        # 检查 resources/face/face_guide.ma 是否真实存在。
        template_path = self.validate_guide_template_file()

        # 使用 Scene Core 导入模板并取得本次新创建的节点列表。
        imported_nodes = scene_utils.import_scene(
            template_path,
            ignore_version=True
        )

        # 从新节点中定位 Maya 自动重命名后的临时 Guide Root。
        template_root = self.get_imported_template_root(
            imported_nodes
        )

        # 把临时 Root 内容合并进正式 Face Guide Group，避免 _002 Root 泄漏到场景。
        merged_nodes = self.merge_imported_template_root(
            template_root
        )

        # 合并完成后重新获取正式 Guide Root 和 Move Ctrl DAG 引用。
        self.refresh_guide_handles()

        # 再次确认 Template 的核心 Move Ctrl 已经正确进入正式 Guide 层级。
        if not self.guide_exists():
            raise RuntimeError(
                u"Face Guide 模板导入完成，但没有找到 {}。".format(
                    self.guide_move_ctrl_name
                )
            )

        return {
            "imported": True,
            "guide_root": self.guide_root,
            "guide_move_ctrl": self.guide_move_ctrl,
            "new_nodes": merged_nodes,
        }

    def clear_guide_config(self):
        u"""
        清除 Config 中保存的 Guide Message 引用。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        if not self.config_node_exists():
            return False

        # 清空 Guide Root / Move Ctrl Message，避免 Reset 后 Config 仍引用旧节点。
        self.set_config_messages(
            attrs_dict={
                "face_guide_root": None,
                "face_guide_move_ctrl": None,
            },
            force=True,
            clear_empty=True
        )

        return True

    def remove_guide(self):
        u"""
        删除正式 Face Guide Group 下的 Template 内容。

        Face Guide Group 本身属于 FaceBase 主层级，因此不会删除。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        if not cmds.objExists(self.face_guide_grp):
            # Guide Group 已不存在时只刷新内部缓存，保持对象状态和场景一致。
            self.refresh_guide_handles()
            return False

        children = cmds.listRelatives(
            self.face_guide_grp,
            children=True,
            type="transform",
            fullPath=True
        )

        if children is None:
            children = []

        for child in children:
            if not cmds.objExists(child):
                continue

            cmds.delete(
                child
            )

        # Guide 节点删除后同步清除 Config 中保存的旧 Message 引用。
        self.clear_guide_config()

        # 删除完成后清空并重新计算当前 Guide Handle 状态。
        self.refresh_guide_handles()

        if self.config_node_exists():
            # Guide 被删除后 Step 02 必须重新标记为未完成。
            self.set_step_completed(
                completed=False
            )

            # Guide 数据改变后让 Step 03～04 的旧状态同步失效。
            self.invalidate_later_steps()

        return True

    def reset_guide(self):
        u"""
        删除当前 Guide 内容，并重新导入原始 face_guide.ma。

        Returns:
            object:
                方法执行后的结果数据。
        """
        # 删除当前用户调整后的 Guide Template 和对应 Config 引用。
        self.remove_guide()

        # 重新导入干净的资源模板，恢复初始 Guide 状态。
        result = self.import_guide_template()

        # 把重新导入后的 Guide Root / Move Ctrl / Version 写回 Config。
        self.save_guide_config()

        # Reset 后仍需要用户重新贴合，因此 Step 02 保持未完成。
        self.set_step_completed(
            completed=False
        )

        # Guide 被重置后让后续旧 Rig 状态失效。
        self.invalidate_later_steps()

        return result

    def build_guide(self):
        u"""
        创建或恢复可供绑定师编辑的 Face Guide。

        这是 Step 02 页面内部的辅助操作，不代表正式完成 Step 02。

        Returns:
            object:
                方法执行后的结果数据。
        """
        # 检查 Step 01 公共输入，确保 Guide 不是建立在无效 Setup 上。
        self.validate_setup()

        # 确保 Face 主层级和 Guide Group 存在。
        self.ensure_hierarchy()

        # 创建或复用 Face Config，给 Guide Root / Move Ctrl 提供持久化目标。
        self.ensure_config_node()

        # 导入新的 Guide Template，或复用当前场景已经存在的 Guide。
        import_result = self.import_guide_template()

        # 保存当前 Guide Root、Move Ctrl 和 Template Version。
        self.save_guide_config()

        # Build Guide 后还需要用户手动贴合，因此 Step 02 明确保持未完成。
        self.set_step_completed(
            completed=False
        )

        # Guide 被重新建立后让 Step 03～04 的旧状态失效。
        self.invalidate_later_steps()

        return import_result

    # =========================================================================
    # Guide Query
    # =========================================================================

    def get_guide_node(
            self,
            short_name,
            required=False
    ):
        u"""
        在正式 Face Guide 层级中按 Short Name 查找 Transform。

        Args:
            short_name (str):
                `short_name` 对应的 Maya 节点或资源名称。
            required (bool):
                目标不存在或数据缺失时是否直接抛出异常。

        Returns:
            None | object:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if not short_name:
            if required:
                raise RuntimeError(
                    u"Guide 节点名称不能为空。"
                )
            return None

        if not cmds.objExists(self.face_guide_grp):
            if required:
                raise RuntimeError(
                    u"Face Guide Group 不存在: {}".format(
                        self.face_guide_grp
                    )
                )
            return None

        candidates = []

        # 使用统一 Short Name 规则判断 Root 自己是否就是查询目标。
        root_short_name = self.get_short_name(
            self.face_guide_grp
        )

        if root_short_name == short_name:
            candidates.append(
                self.face_guide_grp
            )

        descendants = cmds.listRelatives(
            self.face_guide_grp,
            allDescendents=True,
            type="transform",
            fullPath=True
        )

        if descendants is None:
            descendants = []

        for node in descendants:
            # 使用统一 Short Name 规则在完整 Guide Hierarchy 中筛选目标节点。
            node_short_name = self.get_short_name(
                node
            )

            if node_short_name != short_name:
                continue

            candidates.append(
                node
            )

        if len(candidates) == 1:
            return candidates[0]

        if len(candidates) > 1:
            raise RuntimeError(
                u"Face Guide 中存在多个同名节点: {}".format(
                    short_name
                )
            )

        if required:
            raise RuntimeError(
                u"没有找到 Face Guide 节点: {}".format(
                    short_name
                )
            )

        return None

    def get_guide_locators(self, parent_group=None):
        u"""
        获取正式 Guide 层级中的全部 Locator Transform。

        Args:
            parent_group (str | None):
                新节点或新层级需要挂接的 Parent Group；None 表示不额外指定父级。

        Returns:
            object | list:
                方法执行后的结果数据。
        """
        if parent_group is None:
            parent_group = self.face_guide_grp

        if not cmds.objExists(parent_group):
            return []

        descendants = cmds.listRelatives(
            parent_group,
            allDescendents=True,
            type="transform",
            fullPath=True
        )

        if descendants is None:
            descendants = []

        locators = []

        for node in descendants:
            # 使用统一 Short Name 规则过滤 Face Guide Locator 命名。
            short_name = self.get_short_name(
                node
            )

            if not short_name.startswith("loc_"):
                continue

            if "_guide_" not in short_name:
                continue

            # 只有真实包含 Locator Shape 的 Transform 才计入 Guide Locator。
            shapes = self.get_locator_shapes(
                node
            )

            if not shapes:
                continue

            locators.append(
                node
            )

        locators.sort()
        return locators

    def get_part_guides(
            self,
            part,
            side=None,
            include_tokens=None,
            exclude_tokens=None
    ):
        u"""
        按命名 Token 查询某一个 Face 部位的 Locator。

        Args:
            part (str):
                Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            include_tokens (str | list[str] | None):
                Guide 名称必须包含的额外 Token；用于缩小部位查询范围。
            exclude_tokens (str | list[str] | None):
                Guide 名称出现这些 Token 时排除该节点。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if not part:
            raise ValueError(
                u"part 不能为空。"
            )

        if side is not None:
            valid_sides = [
                "lf",
                "rt",
                "md",
            ]

            if side not in valid_sides:
                raise ValueError(
                    u"side 必须是 lf / rt / md / None，当前值: {}".format(
                        side
                    )
                )

        if include_tokens is None:
            include_tokens = []

        if exclude_tokens is None:
            exclude_tokens = []

        # 获取当前正式 Guide Hierarchy 中全部有效 Locator，再按业务 Token 过滤。
        locators = self.get_guide_locators()
        result = []

        for locator in locators:
            short_name = self.get_short_name(
                locator
            )
            lower_name = short_name.lower()

            if part.lower() not in lower_name:
                continue

            if side is not None:
                side_token = "_{}_".format(
                    side
                )

                if side_token not in lower_name:
                    continue

            include_passed = True

            for token in include_tokens:
                if token.lower() in lower_name:
                    continue

                include_passed = False
                break

            if not include_passed:
                continue

            exclude_failed = False

            for token in exclude_tokens:
                if token.lower() not in lower_name:
                    continue

                exclude_failed = True
                break

            if exclude_failed:
                continue

            result.append(
                locator
            )

        result.sort()
        return result

    def get_world_position(self, guide):
        u"""
        获取一个 Guide Transform 的世界坐标。

        保留 FaceGuide 旧入口，实际 Transform 查询统一由 core.transform_utils 维护。

        Args:
            guide (str):
                需要查询或处理的 Guide Transform 名称。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if not guide:
            raise ValueError(
                u"Guide 不能为空。"
            )

        # 使用 Transform Core 统一验证 Transform 并读取 World Translation。
        return transform_utils.get_world_translation(
            guide
        )

    def get_guide_positions(self, guides):
        u"""
        按输入顺序返回多个 Guide 的世界坐标。

        Args:
            guides (str | list[str]):
                需要按顺序查询或传递给 Builder 的 Guide Transform / Locator 列表。

        Returns:
            object:
                方法执行后的结果数据。
        """
        positions = []

        if not guides:
            return positions

        for guide in guides:
            # 通过统一 Guide 世界位置入口保持单个 / 批量查询行为一致。
            position = self.get_world_position(
                guide
            )
            positions.append(
                position
            )

        return positions

    # =========================================================================
    # Face Part Query
    # =========================================================================

    def get_lip_guides(self, required=True):
        u"""
        返回上下嘴唇从 RT Corner -> MD -> LF Corner 的有序 Guide。

        Args:
            required (bool):
                目标不存在或数据缺失时是否直接抛出异常。

        Returns:
            dict:
                方法执行后的结果数据。
        """
        upper_names = [
            "loc_rt_mouth_corner_guide_001",
            "loc_rt_upper_lip_guide_002",
            "loc_rt_upper_lip_guide_001",
            "loc_md_upper_lip_guide_001",
            "loc_lf_upper_lip_guide_001",
            "loc_lf_upper_lip_guide_002",
            "loc_lf_mouth_corner_guide_001",
        ]

        lower_names = [
            "loc_rt_mouth_corner_guide_001",
            "loc_rt_lower_lip_guide_002",
            "loc_rt_lower_lip_guide_001",
            "loc_md_lower_lip_guide_001",
            "loc_lf_lower_lip_guide_001",
            "loc_lf_lower_lip_guide_002",
            "loc_lf_mouth_corner_guide_001",
        ]

        upper_guides = []
        lower_guides = []

        for guide_name in upper_names:
            guide = self.get_guide_node(
                guide_name,
                required=required
            )

            if guide:
                upper_guides.append(
                    guide
                )

        for guide_name in lower_names:
            guide = self.get_guide_node(
                guide_name,
                required=required
            )

            if guide:
                lower_guides.append(
                    guide
                )

        corners = []

        right_corner = self.get_guide_node(
            "loc_rt_mouth_corner_guide_001",
            required=required
        )
        left_corner = self.get_guide_node(
            "loc_lf_mouth_corner_guide_001",
            required=required
        )

        if right_corner:
            corners.append(
                right_corner
            )

        if left_corner:
            corners.append(
                left_corner
            )

        return {
            "upper": upper_guides,
            "lower": lower_guides,
            "corners": corners,
        }

    def get_eyelid_guides(self, side, required=True):
        u"""
        返回某一侧 Upper / Lower Eyelid 的有序 Guide。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            required (bool):
                目标不存在或数据缺失时是否直接抛出异常。

        Returns:
            dict:
                方法执行后的结果数据。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if side not in ["lf", "rt"]:
            raise ValueError(
                u"Eyelid side 必须是 lf 或 rt。"
            )

        inner_name = "loc_{}_inner_lid_guide_001".format(
            side
        )
        outer_name = "loc_{}_outer_lid_guide_001".format(
            side
        )

        upper_names = [
            inner_name,
            "loc_{}_upper_lid_guide_001".format(side),
            "loc_{}_upper_lid_guide_002".format(side),
            "loc_{}_upper_lid_guide_003".format(side),
            outer_name,
        ]

        lower_names = [
            inner_name,
            "loc_{}_lower_lid_guide_001".format(side),
            "loc_{}_lower_lid_guide_002".format(side),
            "loc_{}_lower_lid_guide_003".format(side),
            outer_name,
        ]

        upper_guides = []
        lower_guides = []

        for guide_name in upper_names:
            guide = self.get_guide_node(
                guide_name,
                required=required
            )

            if guide:
                upper_guides.append(
                    guide
                )

        for guide_name in lower_names:
            guide = self.get_guide_node(
                guide_name,
                required=required
            )

            if guide:
                lower_guides.append(
                    guide
                )

        return {
            "upper": upper_guides,
            "lower": lower_guides,
        }

    def get_brow_guides(self, side):
        u"""
        返回某一侧 Brow Main 和 Brow Point Guide。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。

        Returns:
            dict:
                方法执行后的结果数据。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if side not in ["lf", "rt"]:
            raise ValueError(
                u"Brow side 必须是 lf 或 rt。"
            )

        # 从全部 Guide Locator 中筛选当前 Side 的 Brow Guide。
        all_guides = self.get_part_guides(
            part="brow",
            side=side
        )

        main_guide = None
        point_guides = []

        for guide in all_guides:
            short_name = self.get_short_name(
                guide
            )

            if "_brow_main_" in short_name:
                main_guide = guide
                continue

            point_guides.append(
                guide
            )

        return {
            "main": main_guide,
            "points": point_guides,
            "all": all_guides,
        }

    def get_eye_guides(self, side, required=False):
        u"""
        返回某一侧 Eye Ball / Iris Guide。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            required (bool):
                目标不存在或数据缺失时是否直接抛出异常。

        Returns:
            dict:
                方法执行后的结果数据。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if side not in ["lf", "rt"]:
            raise ValueError(
                u"Eye side 必须是 lf 或 rt。"
            )

        eye_ball = self.get_guide_node(
            "loc_{}_eye_ball_guide_001".format(side),
            required=required
        )
        eye_iris = self.get_guide_node(
            "loc_{}_eye_iris_guide_001".format(side),
            required=required
        )

        return {
            "eye_ball": eye_ball,
            "eye_iris": eye_iris,
        }

    def get_eye_bag_guides(self, side):
        u"""
        返回某一侧 Eye Bag Guide。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if side not in ["lf", "rt"]:
            raise ValueError(
                u"Eye Bag side 必须是 lf 或 rt。"
            )

        return self.get_part_guides(
            part="eye_bag",
            side=side
        )

    def get_nose_guides(self):
        u"""
        返回全部 Nose Guide。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return self.get_part_guides(
            part="nose"
        )

    def get_jaw_guides(self):
        u"""
        返回全部 Jaw Guide。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return self.get_part_guides(
            part="jaw"
        )

    def get_teeth_guides(self):
        u"""
        返回全部 Teeth Guide。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return self.get_part_guides(
            part="teeth"
        )

    def get_tongue_guides(self):
        u"""
        返回全部 Tongue Guide。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return self.get_part_guides(
            part="tongue"
        )

    def get_ear_guides(self, side=None):
        u"""
        返回 Ear Guide。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return self.get_part_guides(
            part="ear",
            side=side
        )

    def get_zygoma_guides(self, side=None):
        u"""
        返回 Zygoma Guide。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return self.get_part_guides(
            part="zygoma",
            side=side
        )

    # =========================================================================
    # Symmetry - Name / Parent
    # =========================================================================

    @staticmethod
    def get_right_name(left_name):
        u"""
        把 lf 命名转换为对应 rt 命名。

        Args:
            left_name (str):
                `left_name` 对应的 Maya 节点或资源名称。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if "_lf_" not in left_name:
            raise ValueError(
                u"节点名称中没有 _lf_，无法生成右侧名称: {}".format(
                    left_name
                )
            )

        return left_name.replace(
            "_lf_",
            "_rt_",
            1
        )

    def get_mirror_parent(self, left_parent):
        u"""
        获取一个左侧 Parent 对应的右侧 Parent。

        Args:
            left_parent (str):
                左侧 Guide 当前 Parent；镜像修复时用于解析对应的右侧 Parent。

        Returns:
            object | None:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if not left_parent:
            return None

        # 使用统一 Short Name 规则判断当前 Parent 是公共空间还是左侧嵌套空间。
        left_parent_name = self.get_short_name(
            left_parent
        )

        if "_lf_" not in left_parent_name:
            return left_parent

        # 根据左侧 Parent 名称生成镜像右侧 Parent 名称。
        right_parent_name = self.get_right_name(
            left_parent_name
        )

        # 在正式 Guide Hierarchy 中查找对应右侧 Parent。
        right_parent = self.get_guide_node(
            right_parent_name,
            required=False
        )

        if not right_parent:
            raise RuntimeError(
                u"找不到嵌套 Guide 对应的右侧 Parent: {} -> {}".format(
                    left_parent_name,
                    right_parent_name
                )
            )

        return right_parent

    def get_left_zero_groups(self, parent_group=None):
        u"""
        查找需要镜像 / 修复的 zero_lf_* Guide Group。

        Args:
            parent_group (str | None):
                新节点或新层级需要挂接的 Parent Group；None 表示不额外指定父级。

        Returns:
            object | list:
                方法执行后的结果数据。
        """
        if parent_group is None:
            parent_group = self.face_guide_grp

        if not cmds.objExists(parent_group):
            return []

        descendants = cmds.listRelatives(
            parent_group,
            allDescendents=True,
            type="transform",
            fullPath=True
        )

        if descendants is None:
            descendants = []

        left_zero_groups = []

        for node in descendants:
            short_name = self.get_short_name(
                node
            )

            if not short_name.startswith("zero_lf_"):
                continue

            left_zero_groups.append(
                node
            )

        # 父级 Guide 必须先修复，子级才可以找到已经建立好的正确 RT Parent。
        left_zero_groups.sort(
            key=self.get_dag_depth
        )

        return left_zero_groups

    def get_left_locator(self, left_zero_group):
        u"""
        获取 zero_lf_* 下对应的 loc_lf_* Transform。

        Args:
            left_zero_group (str):
                当前 Rig / Guide / Controller 层级中的 Maya Group Transform。

        Returns:
            None | object:
                方法执行后的结果数据。
        """
        children = cmds.listRelatives(
            left_zero_group,
            children=True,
            type="transform",
            fullPath=True
        )

        if children is None:
            children = []

        for child in children:
            short_name = self.get_short_name(
                child
            )

            if short_name.startswith("loc_lf_"):
                return child

        return None

    # =========================================================================
    # Symmetry - Repair Helper
    # =========================================================================

    @staticmethod
    def set_attr_preserve_lock(
            node,
            attribute,
            value
    ):
        u"""
        设置属性值，并恢复属性原来的 Lock 状态。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。
            attribute (str):
                Maya Attribute 或完整 Plug 名称。
            value (float):
                需要读取、写入或参与计算的数值。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        plug = "{}.{}".format(
            node,
            attribute
        )

        if not cmds.objExists(plug):
            return False

        was_locked = cmds.getAttr(
            plug,
            lock=True
        )

        if was_locked:
            cmds.setAttr(
                plug,
                lock=False
            )

        try:
            cmds.setAttr(
                plug,
                value
            )
        finally:
            if was_locked:
                cmds.setAttr(
                    plug,
                    lock=True
                )

        return True

    @staticmethod
    def connect_attr_preserve_lock(
            source_attr,
            destination_attr
    ):
        u"""
        连接属性，并恢复目标属性原来的 Lock 状态。

        Args:
            source_attr (str):
                驱动端完整 Maya Plug，例如 `ctrl.translateX`。
            destination_attr (str):
                接收连接的完整 Maya Plug，例如 `jnt.rotateY`。

        Returns:
            bool | object:
                方法执行后的结果数据。
        """
        if not cmds.objExists(source_attr):
            return False

        if not cmds.objExists(destination_attr):
            return False

        if cmds.isConnected(
                source_attr,
                destination_attr
        ):
            return True

        was_locked = cmds.getAttr(
            destination_attr,
            lock=True
        )

        if was_locked:
            cmds.setAttr(
                destination_attr,
                lock=False
            )

        try:
            # 使用 Connection Core 建立 Plug 连接，FaceGuide 只负责额外的 Lock 状态保护。
            return connection_utils.connect_plugs(
                source_attr,
                destination_attr,
                force=True
            )
        finally:
            if was_locked:
                cmds.setAttr(
                    destination_attr,
                    lock=True
                )

    def create_or_update_right_zero(self, left_zero_group):
        u"""
        创建或修复对应 zero_rt_* 镜像空间。

        Args:
            left_zero_group (str):
                当前 Rig / Guide / Controller 层级中的 Maya Group Transform。

        Returns:
            object:
                方法执行后的结果数据。
        """
        # 取得左侧 Zero Short Name，并生成对应右侧名称。
        left_zero_name = self.get_short_name(
            left_zero_group
        )
        right_zero_name = self.get_right_name(
            left_zero_name
        )

        # 查询左侧 Zero Parent，并解析应该使用的右侧镜像 Parent。
        left_parent = self.get_parent(
            left_zero_group
        )
        right_parent = self.get_mirror_parent(
            left_parent
        )

        # 优先在目标 Parent 下查找现有右侧 Zero，避免错误复用其它同名层级。
        right_zero_group = self.get_node_under_parent(
            right_parent,
            right_zero_name
        )

        if right_zero_group is None:
            # Parent 下没找到时再在正式 Guide Hierarchy 中全局查找同名右侧 Zero。
            right_zero_group = self.get_guide_node(
                right_zero_name,
                required=False
            )

        if right_zero_group is None:
            # 右侧 Zero 完全不存在时使用 Scene Core 创建新的 Transform。
            right_zero_group = scene_utils.create_node(
                "transform",
                right_zero_name
            )

        # 查询当前 Parent，只有 Parent 错误时才重新挂接，减少无意义 DAG Path 变化。
        current_parent = self.get_parent(
            right_zero_group
        )

        if right_parent:
            if current_parent != right_parent:
                # 使用统一 Hierarchy API 把右侧 Zero 放入正确镜像 Parent。
                right_zero_group = hierarchy_utils.Hierarchy.parent(
                    right_zero_group,
                    right_parent
                )

        rotate_order = cmds.getAttr(
            left_zero_group + ".rotateOrder"
        )

        # 同步 Rotate Order，同时保留右侧属性原来的 Lock 状态。
        self.set_attr_preserve_lock(
            right_zero_group,
            "rotateOrder",
            rotate_order
        )

        translate_x = cmds.getAttr(
            left_zero_group + ".translateX"
        )
        translate_y = cmds.getAttr(
            left_zero_group + ".translateY"
        )
        translate_z = cmds.getAttr(
            left_zero_group + ".translateZ"
        )

        rotate_x = cmds.getAttr(
            left_zero_group + ".rotateX"
        )
        rotate_y = cmds.getAttr(
            left_zero_group + ".rotateY"
        )
        rotate_z = cmds.getAttr(
            left_zero_group + ".rotateZ"
        )

        scale_x = cmds.getAttr(
            left_zero_group + ".scaleX"
        )
        scale_y = cmds.getAttr(
            left_zero_group + ".scaleY"
        )
        scale_z = cmds.getAttr(
            left_zero_group + ".scaleZ"
        )

        is_mirror_root = True

        if left_parent:
            left_parent_name = self.get_short_name(
                left_parent
            )

            if "_lf_" in left_parent_name:
                is_mirror_root = False

        if is_mirror_root:
            # Root 镜像空间只在最外层执行一次 X Translate / Scale 镜像。
            self.set_attr_preserve_lock(
                right_zero_group,
                "translateX",
                -translate_x
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "translateY",
                translate_y
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "translateZ",
                translate_z
            )

            self.set_attr_preserve_lock(
                right_zero_group,
                "rotateX",
                rotate_x
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "rotateY",
                rotate_y
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "rotateZ",
                rotate_z
            )

            self.set_attr_preserve_lock(
                right_zero_group,
                "scaleX",
                -scale_x
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "scaleY",
                scale_y
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "scaleZ",
                scale_z
            )

        else:
            local_attributes = [
                "translateX",
                "translateY",
                "translateZ",
                "rotateX",
                "rotateY",
                "rotateZ",
                "scaleX",
                "scaleY",
                "scaleZ",
            ]

            # Nested Zero 已经处于镜像 Parent 空间，因此直接复制左侧 Local Transform。
            for attribute in local_attributes:
                value = cmds.getAttr(
                    "{}.{}".format(
                        left_zero_group,
                        attribute
                    )
                )

                self.set_attr_preserve_lock(
                    right_zero_group,
                    attribute,
                    value
                )

        return right_zero_group

    def create_or_update_right_locator(
            self,
            left_locator,
            right_zero_group
    ):
        u"""
        创建、复用或重新挂接对应 loc_rt_*。

        Args:
            left_locator (str):
                当前 Rig 定位流程使用的 Guide / Locator Transform。
            right_zero_group (str):
                当前 Rig / Guide / Controller 层级中的 Maya Group Transform。

        Returns:
            object:
                方法执行后的结果数据。
        """
        # 根据左侧 Locator Short Name 生成对应右侧 Locator 名称。
        left_locator_name = self.get_short_name(
            left_locator
        )
        right_locator_name = self.get_right_name(
            left_locator_name
        )

        # 优先在目标 Zero 下查找现有右侧 Locator。
        right_locator = self.get_node_under_parent(
            right_zero_group,
            right_locator_name
        )

        if right_locator is None:
            # Zero 下没有时再从完整 Guide Hierarchy 查找，兼容旧错误 Parent 场景。
            right_locator = self.get_guide_node(
                right_locator_name,
                required=False
            )

        if right_locator is None:
            right_locator = cmds.spaceLocator(
                name=right_locator_name
            )[0]

        # 检查现有右侧 Locator 是否已经位于正确镜像 Zero 下。
        current_parent = self.get_parent(
            right_locator
        )

        if current_parent != right_zero_group:
            # 使用统一 Hierarchy API 修复右侧 Locator Parent。
            right_locator = hierarchy_utils.Hierarchy.parent(
                right_locator,
                right_zero_group
            )

        return right_locator

    def connect_locator_transform(
            self,
            left_locator,
            right_locator
    ):
        u"""
        把左侧 Locator Transform 属性直接连接到右侧。

        Args:
            left_locator (str):
                当前 Rig 定位流程使用的 Guide / Locator Transform。
            right_locator (str):
                当前 Rig 定位流程使用的 Guide / Locator Transform。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        attributes = [
            "translateX",
            "translateY",
            "translateZ",
            "rotateX",
            "rotateY",
            "rotateZ",
            "scaleX",
            "scaleY",
            "scaleZ",
            "rotateOrder",
            "visibility",
        ]

        # 逐属性建立左侧到右侧连接，并保留右侧原有 Lock 状态。
        for attribute in attributes:
            source_attr = "{}.{}".format(
                left_locator,
                attribute
            )
            destination_attr = "{}.{}".format(
                right_locator,
                attribute
            )

            self.connect_attr_preserve_lock(
                source_attr,
                destination_attr
            )

        return True

    def connect_locator_shape(
            self,
            left_locator,
            right_locator
    ):
        u"""
        连接 Locator Shape 的 localPosition / localScale。

        Args:
            left_locator (str):
                当前 Rig 定位流程使用的 Guide / Locator Transform。
            right_locator (str):
                当前 Rig 定位流程使用的 Guide / Locator Transform。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        # 取得左右 Locator Shape，Shape 缺失时不继续建立 Shape Connection。
        left_shapes = self.get_locator_shapes(
            left_locator
        )
        right_shapes = self.get_locator_shapes(
            right_locator
        )

        if not left_shapes:
            return False

        if not right_shapes:
            return False

        left_shape = left_shapes[0]
        right_shape = right_shapes[0]

        shape_attributes = [
            "localPositionX",
            "localPositionY",
            "localPositionZ",
            "localScaleX",
            "localScaleY",
            "localScaleZ",
        ]

        # 逐属性把左侧 Locator Shape 的显示 Offset / Scale 同步到右侧。
        for attribute in shape_attributes:
            source_attr = "{}.{}".format(
                left_shape,
                attribute
            )
            destination_attr = "{}.{}".format(
                right_shape,
                attribute
            )

            self.connect_attr_preserve_lock(
                source_attr,
                destination_attr
            )

        return True

    # =========================================================================
    # Symmetry - Validate / Repair
    # =========================================================================

    def validate_symmetry(self):
        u"""
        检查 LF -> RT Guide 节点、Parent 和 Transform 连接是否完整。

        Returns:
            object:
                方法执行后的结果数据。
        """
        result = {
            "valid": True,
            "missing_nodes": [],
            "wrong_parents": [],
            "broken_connections": [],
        }

        # 没有正式 Guide Template 时直接记录 Move Ctrl 缺失。
        if not self.guide_exists():
            result["valid"] = False
            result["missing_nodes"].append(
                self.guide_move_ctrl_name
            )
            return result

        # 获取全部左侧 Zero，并按父级优先顺序检查对应右侧结构。
        left_zero_groups = self.get_left_zero_groups(
            self.face_guide_grp
        )

        for left_zero_group in left_zero_groups:
            left_zero_name = self.get_short_name(
                left_zero_group
            )
            right_zero_name = self.get_right_name(
                left_zero_name
            )

            right_zero_group = self.get_guide_node(
                right_zero_name,
                required=False
            )

            if not right_zero_group:
                result["missing_nodes"].append(
                    right_zero_name
                )
                continue

            left_parent = self.get_parent(
                left_zero_group
            )

            try:
                expected_right_parent = self.get_mirror_parent(
                    left_parent
                )
            except RuntimeError:
                expected_right_parent = None

            actual_right_parent = self.get_parent(
                right_zero_group
            )

            if expected_right_parent:
                expected_parent_name = self.get_short_name(
                    expected_right_parent
                )
                actual_parent_name = self.get_short_name(
                    actual_right_parent
                )

                if expected_parent_name != actual_parent_name:
                    result["wrong_parents"].append(
                        "{} -> {}".format(
                            right_zero_name,
                            expected_parent_name
                        )
                    )

            left_locator = self.get_left_locator(
                left_zero_group
            )

            if not left_locator:
                continue

            left_locator_name = self.get_short_name(
                left_locator
            )
            right_locator_name = self.get_right_name(
                left_locator_name
            )

            right_locator = self.get_guide_node(
                right_locator_name,
                required=False
            )

            if not right_locator:
                result["missing_nodes"].append(
                    right_locator_name
                )
                continue

            attributes = [
                "translateX",
                "translateY",
                "translateZ",
                "rotateX",
                "rotateY",
                "rotateZ",
                "scaleX",
                "scaleY",
                "scaleZ",
            ]

            for attribute in attributes:
                source_attr = "{}.{}".format(
                    left_locator,
                    attribute
                )
                destination_attr = "{}.{}".format(
                    right_locator,
                    attribute
                )

                if cmds.isConnected(
                        source_attr,
                        destination_attr
                ):
                    continue

                result["broken_connections"].append(
                    "{} -> {}".format(
                        source_attr,
                        destination_attr
                    )
                )

        if result["missing_nodes"]:
            result["valid"] = False

        if result["wrong_parents"]:
            result["valid"] = False

        if result["broken_connections"]:
            result["valid"] = False

        return result

    def mirror_left_guide(
            self,
            left_zero_group
    ):
        u"""
        修复一个 zero_lf_* + loc_lf_* Guide 镜像层级。

        Args:
            left_zero_group (str):
                当前 Rig / Guide / Controller 层级中的 Maya Group Transform。

        Returns:
            dict:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # 在当前左侧 Zero 下找到需要镜像的左侧 Locator。
        left_locator = self.get_left_locator(
            left_zero_group
        )

        if left_locator is None:
            raise RuntimeError(
                u"没有在 {} 下找到 loc_lf_*。".format(
                    left_zero_group
                )
            )

        # 创建或修复与当前左侧 Zero 对应的右侧镜像空间。
        right_zero_group = self.create_or_update_right_zero(
            left_zero_group
        )

        # 创建、复用或重新挂接当前左侧 Locator 对应的右侧 Locator。
        right_locator = self.create_or_update_right_locator(
            left_locator,
            right_zero_group
        )

        # 同步左右 Locator Transform 属性连接。
        self.connect_locator_transform(
            left_locator,
            right_locator
        )

        # 同步左右 Locator Shape 的显示 Offset / Scale 连接。
        self.connect_locator_shape(
            left_locator,
            right_locator
        )

        return {
            "left_zero": left_zero_group,
            "left_locator": left_locator,
            "right_zero": right_zero_group,
            "right_locator": right_locator,
        }

    def mirror_left_guides(self, parent_group=None):
        u"""
        批量修复全部 zero_lf_* Guide；正常 Build Guide 不主动调用。

        Args:
            parent_group (str | None):
                新节点或新层级需要挂接的 Parent Group；None 表示不额外指定父级。

        Returns:
            object:
                方法执行后的结果数据。
        """
        if parent_group is None:
            parent_group = self.face_guide_grp

        # 获取需要修复的左侧 Zero，并保证父级先于子级处理。
        left_zero_groups = self.get_left_zero_groups(
            parent_group=parent_group
        )

        results = []

        # 逐个调用单组镜像修复，所有修复都走同一套节点和连接规则。
        for left_zero_group in left_zero_groups:
            result = self.mirror_left_guide(
                left_zero_group
            )

            results.append(
                result
            )

        return results

    def repair_symmetry(self):
        u"""
        修复 Guide 左右节点层级和连接，并返回修复后的检查结果。

        Returns:
            dict:
                方法执行后的结果数据。
        """
        # 按父级优先顺序修复全部 LF -> RT Guide 镜像结构。
        repair_results = self.mirror_left_guides(
            parent_group=self.face_guide_grp
        )

        # 修复完成后重新执行完整 Symmetry Validation，确认结果是否可用。
        validation = self.validate_symmetry()

        return {
            "repairs": repair_results,
            "validation": validation,
        }

    # =========================================================================
    # Validation
    # =========================================================================

    def validate_guides(self, check_symmetry=True):
        u"""
        检查 Step 02 Guide 是否可以交给后续 Builder。

        返回结构化结果，方便 UI 一次展示全部问题。

        Args:
            check_symmetry (bool):
                Guide Validation / Finalize 时是否同时检查 LF → RT 镜像节点、Parent 和连接。

        Returns:
            object:
                方法执行后的结果数据。
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "guide_count": 0,
            "symmetry": None,
        }

        if not cmds.objExists(self.face_guide_grp):
            result["errors"].append(
                u"Face Guide Group 不存在: {}".format(
                    self.face_guide_grp
                )
            )
            result["valid"] = False
            return result

        # 检查 Guide Template 的核心 Move Ctrl 是否已经加载。
        if not self.guide_exists():
            result["errors"].append(
                u"Face Guide 模板尚未加载，缺少 {}。".format(
                    self.guide_move_ctrl_name
                )
            )

        # 收集全部有效 Locator，并记录当前 Guide 数据规模。
        locators = self.get_guide_locators()
        result["guide_count"] = len(locators)

        if not locators:
            result["errors"].append(
                u"Face Guide 层级中没有找到 Locator。"
            )

        # 逐个确认 Step 03 必须依赖的核心 Guide 是否存在。
        for guide_name in self.required_guide_names:
            guide = self.get_guide_node(
                guide_name,
                required=False
            )

            if guide:
                continue

            result["errors"].append(
                u"缺少必要 Guide: {}".format(
                    guide_name
                )
            )

        name_counts = {}

        for locator in locators:
            short_name = self.get_short_name(
                locator
            )

            if short_name not in name_counts:
                name_counts[short_name] = 0

            name_counts[short_name] += 1

        # 检查 Guide Short Name 是否重复，避免后续 Builder 查询目标不唯一。
        for short_name in name_counts:
            count = name_counts.get(
                short_name
            )

            if count <= 1:
                continue

            result["errors"].append(
                u"Guide 短名称重复: {} x {}".format(
                    short_name,
                    count
                )
            )

        if check_symmetry:
            # 执行 LF -> RT 镜像节点、Parent 和连接完整性检查。
            symmetry_result = self.validate_symmetry()
            result["symmetry"] = symmetry_result

            for missing_node in symmetry_result["missing_nodes"]:
                result["errors"].append(
                    u"左右镜像缺少节点: {}".format(
                        missing_node
                    )
                )

            for wrong_parent in symmetry_result["wrong_parents"]:
                result["errors"].append(
                    u"右侧 Guide Parent 错误: {}".format(
                        wrong_parent
                    )
                )

            for broken_connection in symmetry_result["broken_connections"]:
                result["errors"].append(
                    u"左右镜像连接断开: {}".format(
                        broken_connection
                    )
                )

        if result["errors"]:
            result["valid"] = False

        return result

    # =========================================================================
    # Config
    # =========================================================================

    def save_guide_config(self):
        u"""
        保存 Step 02 Guide Root、Move Ctrl 和 Guide Version。

        Returns:
            bool:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # 保存前刷新 Guide DAG 引用，保证 Config 连接的是当前真实节点。
        self.refresh_guide_handles()

        if not self.guide_root:
            raise RuntimeError(
                u"没有可保存的 Face Guide Root。"
            )

        if not self.guide_move_ctrl:
            raise RuntimeError(
                u"没有可保存的 Face Guide Move Ctrl。"
            )

        # 使用 Message 保存 Guide Root / Move Ctrl，Maya Rename 后引用仍然有效。
        self.set_config_messages(
            attrs_dict={
                "face_guide_root": self.guide_root,
                "face_guide_move_ctrl": self.guide_move_ctrl,
            },
            force=True,
            clear_empty=True
        )

        # 保存 Guide Template Version，给后续兼容检查和升级逻辑使用。
        self.set_config_values(
            attrs_dict={
                "face_guide_version": self.guide_version,
            },
            attr_types={
                "face_guide_version": "string",
            },
            lock=False,
            hide=True
        )

        return True

    # =========================================================================
    # Compatibility Entry
    # =========================================================================

    def build(self):
        u"""
        兼容旧版 FaceGuide.build()。

        新代码使用 build_guide() 表示“加载可编辑 Guide Template”。

        Returns:
            object:
                方法执行后的结果数据。
        """
        # 旧 Build API 只转发到明确命名的 Guide 编辑准备入口。
        return self.build_guide()

    def finalize(self, check_symmetry=True):
        u"""
        兼容旧版 FaceGuide.finalize()。

        新代码使用 run_step() 正式提交 Step 02。

        Args:
            check_symmetry (bool):
                Guide Validation / Finalize 时是否同时检查 LF → RT 镜像节点、Parent 和连接。

        Returns:
            object:
                方法执行后的结果数据。
        """
        self.check_symmetry = bool(
            check_symmetry
        )

        # 使用统一 Step 生命周期重新收集、检查并正式提交当前 Guide。
        self.run_step()

        return self.validation_result


__all__ = [
    "FaceGuide",
]
