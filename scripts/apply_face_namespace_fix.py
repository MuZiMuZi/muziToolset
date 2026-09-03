# coding=utf-8
u"""
临时迁移脚本：修复 FaceBase 基础层级的 Namespace Long Path 缓存。

仅用于当前 refactor/full-code-cn-comments 测试修复。
修复完成并验证后删除，不作为 Runtime API 保留。
"""

from __future__ import print_function

from pathlib import Path


FILE_PATH = Path("systems/face/face_base.py")
START_MARKER = "    def ensure_hierarchy(self):\n"
END_MARKER = "    # =========================================================================\n    # Config Node / Face API\n"


NEW_METHOD = '''    def ensure_hierarchy(self):
        u"""
        确保 Face Rig 基础 Group 存在，并保存 Maya 返回的真实 DAG Long Path。

        Config 只负责提供标准节点名称。真正创建或查询 Maya Group 后，必须把
        ``hierarchy_utils.ensure_group()`` 返回的唯一 Long Path 写回当前实例，
        这样 Namespace、同名 DAG 和 Rebuild 场景都继续使用真实场景节点。

        Returns:
            bool:
                Face 基础层级全部存在、Parent 正确，并完成真实路径缓存后返回 True。
        """
        # -------------------------------------------------------------------------
        # Step 01：创建 Face Master，并保存 Maya 实际返回的唯一 Long Path
        # -------------------------------------------------------------------------
        self.face_master_grp = hierarchy_utils.ensure_group(
            self.face_master_grp
        )

        # -------------------------------------------------------------------------
        # Step 02：创建 Model 主组，并挂到 Face Master 下
        # -------------------------------------------------------------------------
        self.face_model_grp = hierarchy_utils.ensure_group(
            self.face_model_grp,
            parent_node=self.face_master_grp
        )

        # -------------------------------------------------------------------------
        # Step 03：创建 Face 类型层级，并逐项保存真实场景路径
        # -------------------------------------------------------------------------
        self.face_guide_grp = hierarchy_utils.ensure_group(
            self.face_guide_grp,
            parent_node=self.face_master_grp
        )
        self.face_ctrl_grp = hierarchy_utils.ensure_group(
            self.face_ctrl_grp,
            parent_node=self.face_master_grp
        )
        self.face_jnt_grp = hierarchy_utils.ensure_group(
            self.face_jnt_grp,
            parent_node=self.face_master_grp
        )
        self.face_rig_nodes_grp = hierarchy_utils.ensure_group(
            self.face_rig_nodes_grp,
            parent_node=self.face_master_grp
        )
        self.face_pos_driver_grp = hierarchy_utils.ensure_group(
            self.face_pos_driver_grp,
            parent_node=self.face_master_grp
        )

        # -------------------------------------------------------------------------
        # Step 04：创建 Head Work Model 层级，并保存真实场景路径
        # -------------------------------------------------------------------------
        self.face_tweak_grp = hierarchy_utils.ensure_group(
            self.face_tweak_grp,
            parent_node=self.face_model_grp
        )
        self.face_stretch_grp = hierarchy_utils.ensure_group(
            self.face_stretch_grp,
            parent_node=self.face_model_grp
        )
        self.face_deform_grp = hierarchy_utils.ensure_group(
            self.face_deform_grp,
            parent_node=self.face_model_grp
        )

        # -------------------------------------------------------------------------
        # Step 05：刷新公共 Group 列表，后续 Module 统一复用真实 Long Path
        # -------------------------------------------------------------------------
        self.type_groups = [
            self.face_guide_grp,
            self.face_ctrl_grp,
            self.face_jnt_grp,
            self.face_rig_nodes_grp,
            self.face_pos_driver_grp,
        ]
        self.model_groups = [
            self.face_tweak_grp,
            self.face_stretch_grp,
            self.face_deform_grp,
        ]

        return True

'''


def run():
    u"""定点替换 FaceBase.ensure_hierarchy()，不修改其它 Runtime 代码。"""
    source = FILE_PATH.read_text(
        encoding="utf-8"
    )

    start_index = source.find(
        START_MARKER
    )

    if start_index < 0:
        raise RuntimeError(
            u"没有找到 FaceBase.ensure_hierarchy()。"
        )

    end_index = source.find(
        END_MARKER,
        start_index
    )

    if end_index < 0:
        raise RuntimeError(
            u"没有找到 FaceBase Config Node 分区标记。"
        )

    current_method = source[
        start_index:end_index
    ]

    if "self.face_master_grp = hierarchy_utils.ensure_group" in current_method:
        print("Face namespace hierarchy fix already applied.")
        return False

    updated_source = (
        source[:start_index]
        + NEW_METHOD
        + source[end_index:]
    )

    FILE_PATH.write_text(
        updated_source,
        encoding="utf-8"
    )

    print("Applied Face namespace hierarchy Long Path fix.")
    return True


if __name__ == "__main__":
    run()
