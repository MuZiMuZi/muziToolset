# coding=utf-8
u"""
Face Guide Template
===================

Face Guide Template 的正式导入流程。

问题背景：
    Step 01 会预先创建正式 grp_md_face_guide_001；
    resources/face/face_guide.ma 内部 Root 也使用同名 grp_md_face_guide_001。
    Maya 允许不同 DAG Path 下出现相同 Short Name，因此直接 Import 后如果继续使用短名称 Parent，
    很容易把模板 Child Parent 回模板 Root 自己，随后删除临时 Root 时把整套 Guide 一起删除。

设计目标：
    1. 导入前临时重命名 Step 01 创建的空 Guide Container，消除 Short Name 歧义；
    2. 直接保留 face_guide.ma 自己的 Root，并把它 Parent 到 Face Master；
    3. 删除旧空 Container；
    4. 导入完成后解除模板原有 LF -> RT 永久连接，使两侧可以独立编辑；
    5. 最终仍然使用 grp_md_face_guide_001 作为正式 Face Guide Root。

重要边界：
    - 本模块只负责 Guide Template Import / Restore；
    - Scene Import 复用 core.scene_utils；
    - DAG Parent 复用 core.hierarchy_utils；
    - Rename 复用 core.rename_utils；
    - 左右一次性镜像和永久连接解除复用 systems.face.guide_mirror；
    - Step Finalize 仍然由 FaceGuide.run_step() 负责。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import hierarchy_utils
from ...core import rename_utils
from ...core import scene_utils
from . import guide_mirror


temporary_guide_container_name = "grp_md_face_guide_container_001"


# =============================================================================
# Helper
# =============================================================================

def get_children(node):
    u"""返回一个 DAG 节点的全部直接 Child。"""
    if not node:
        return []

    if not cmds.objExists(node):
        return []

    children = cmds.listRelatives(
        node,
        children=True,
        fullPath=True
    )

    if children is None:
        children = []

    return children


def get_available_temporary_name():
    u"""返回场景中未被占用的临时 Guide Container 名称。"""
    if not cmds.objExists(
            temporary_guide_container_name
    ):
        return temporary_guide_container_name

    index = 2

    while True:
        candidate = "grp_md_face_guide_container_{:03d}".format(
            index
        )

        if not cmds.objExists(
                candidate
        ):
            return candidate

        index += 1


# =============================================================================
# Build
# =============================================================================

def build_guide(face_guide):
    u"""
    导入或复用可编辑的 Face Guide Template。

    Args:
        face_guide (FaceGuide):
            当前 Face Guide System 实例。

    Returns:
        dict:
            imported、guide_root、guide_move_ctrl、new_nodes。

    Raises:
        RuntimeError:
            Setup 无效、旧 Guide Container 非空、模板导入失败或核心 Move Ctrl 缺失时抛出。
    """
    # Step 02 必须建立在有效 Step 01 数据之上。
    face_guide.validate_setup()

    # 确保 Face Master / Config 等公共结构存在。
    face_guide.ensure_hierarchy()
    face_guide.ensure_config_node()

    # 当前 Guide 已经完整加载时直接复用，避免重复导入。
    if face_guide.guide_exists():
        return {
            "imported": False,
            "guide_root": face_guide.guide_root,
            "guide_move_ctrl": face_guide.guide_move_ctrl,
            "new_nodes": [],
        }

    # 获取正式 Guide Container 的唯一 Long Path。
    guide_container = scene_utils.get_long_name(
        face_guide.face_guide_grp
    )

    # 没有核心 Move Ctrl 但 Container 中已经有内容时，不自动删除未知用户数据。
    container_children = get_children(
        guide_container
    )

    if container_children:
        raise RuntimeError(
            u"Face Guide Group 中存在未知内容，无法安全自动导入模板：{}".format(
                face_guide.face_guide_grp
            )
        )

    template_path = face_guide.validate_guide_template_file()

    # 导入前先把 Step 01 创建的空 Container 临时改名，消除模板 Root 同名歧义。
    temporary_name = get_available_temporary_name()
    temporary_container = rename_utils.rename_node(
        guide_container,
        temporary_name
    )

    imported_nodes = []
    template_root = None

    try:
        imported_nodes = scene_utils.import_scene(
            template_path,
            ignore_version=True
        )

        # 此时场景里只有模板 Root 使用 grp_md_face_guide_* 正式名称，可以稳定识别。
        template_root = face_guide.get_imported_template_root(
            imported_nodes
        )

        # 直接保留模板 Root，并把它放入 Face Master，而不是把 Child 再合并到同名空 Group。
        template_root = hierarchy_utils.Hierarchy.parent(
            template_root,
            face_guide.face_master_grp
        )

        # 正式模板 Root 已接管 Guide 层级，删除 Step 01 创建的旧空 Container。
        if temporary_container:
            if cmds.objExists(
                    temporary_container
            ):
                cmds.delete(
                    temporary_container
                )

    except Exception:
        # 导入中途失败时尽可能恢复 Step 01 的空 Guide Container 名称。
        if temporary_container:
            if cmds.objExists(
                    temporary_container
            ):
                rename_utils.rename_node(
                    temporary_container,
                    face_guide.face_guide_grp
                )

        raise

    # 导入完成后重新查询正式 Root / Move Ctrl。
    face_guide.refresh_guide_handles()

    if not face_guide.guide_exists():
        raise RuntimeError(
            u"Face Guide 模板导入完成，但没有找到 {}。".format(
                face_guide.guide_move_ctrl_name
            )
        )

    # face_guide.ma 保留了旧版 LF -> RT 永久连接。
    # 通过一次 LF -> RT Mirror 复制当前状态并解除 Target 输入，保证左右之后可以独立编辑。
    guide_mirror.mirror_guides(
        face_guide,
        source_side="lf",
        target_side="rt"
    )

    # 保存正式 Guide Root / Move Ctrl / Version。
    face_guide.save_guide_config()

    # 导入后仍然需要用户贴合，因此 Step 02 保持未完成。
    face_guide.set_step_completed(
        completed=False
    )
    face_guide.invalidate_later_steps()

    return {
        "imported": True,
        "guide_root": face_guide.guide_root,
        "guide_move_ctrl": face_guide.guide_move_ctrl,
        "new_nodes": imported_nodes,
    }


__all__ = [
    "temporary_guide_container_name",
    "build_guide",
]
