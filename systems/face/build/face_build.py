# coding=utf-8
u"""
Face Rig Step 03 - Build
========================

Face Workflow 的 Step 03 正式入口。

职责：
    1. 验证 Step 01 Setup / Step 02 Guide 已完成；
    2. 验证当前正式 Face Guide 完整；
    3. 通过 FaceRig Orchestrator 按依赖顺序构建全部 Face Module；
    4. 校验每个 Module 的统一 create_build() 结果；
    5. 成功后把 Step 03 标记完成，并把 Workflow 推进到 Step 04。

设计边界：
    - FaceBuild 是 Workflow Step，因此使用 run_step()；
    - FaceRig 是 Module Orchestrator，因此使用 create_build()；
    - Brow / Eye / Lip 等具体业务逻辑只存在于 systems.face.modules；
    - 本 Step 不复制任何具体 Joint / Controller / Deformer 算法。
"""

from __future__ import print_function

from ..face_base import FaceBase
from ..guide import FaceGuide
from ..modules.face_rig import FaceRig


class FaceBuild(FaceBase):
    u"""统一执行 Face Workflow Step 03，并保存完整 FaceRig 构建结果。"""

    def __init__(self):
        u"""初始化 Step 03 Build 状态。"""
        super(FaceBuild, self).__init__(
            side="md",
            part="face",
            index=1
        )

        self.step_value = 3
        self.face_guide = FaceGuide()
        self.face_rig = None
        self.guide_validation = None
        self.build_result = None

    def collect_inputs(self):
        u"""
        验证 Step 03 所依赖的 Setup、Guide 和 Workflow 状态。

        Returns:
            bool:
                所有 Step 03 前置条件都满足时返回 True。

        Raises:
            RuntimeError:
                Setup / Guide 未完成、Guide 不完整或 Step 03 已完成时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：验证 Step 01 保存的模型与 Mouth Joint Number
        # -------------------------------------------------------------------------
        self.validate_setup_config(
            require_mouth_jnt_number=True
        )

        # -------------------------------------------------------------------------
        # Step 02：只允许在 Step 01 / Step 02 都正式完成后进入完整 Build
        # -------------------------------------------------------------------------
        if not self.is_step_completed(
                step_value=1
        ):
            raise RuntimeError(
                u"Face Setup 尚未完成，不能执行 Step 03 Build。"
            )

        if not self.is_step_completed(
                step_value=2
        ):
            raise RuntimeError(
                u"Face Guide 尚未完成，不能执行 Step 03 Build。"
            )

        # -------------------------------------------------------------------------
        # Step 03：当前版本不维护隐式 Rebuild，避免重复生成同名 Rig 节点
        # -------------------------------------------------------------------------
        if self.is_step_completed(
                step_value=3
        ):
            raise RuntimeError(
                u"Face Build 已经完成。需要修改 Guide 时请先进入正式 Rebuild 流程。"
            )

        # -------------------------------------------------------------------------
        # Step 04：再次验证正式 Guide Schema，防止 Step 02 完成后节点被人工删除
        # -------------------------------------------------------------------------
        self.guide_validation = self.face_guide.validate_guides()

        if not self.guide_validation.get(
                "valid",
                False
        ):
            error_message = u"Face Guide 不完整，不能执行 Step 03 Build。"

            for error in self.guide_validation.get("errors", []):
                error_message += u"\n- {}".format(
                    error
                )

            raise RuntimeError(
                error_message
            )

        return True

    def prepare_data(self):
        u"""
        准备 Face Hierarchy、Config 和完整 FaceRig Orchestrator。

        Returns:
            bool:
                Step 03 构建环境准备完成后返回 True。
        """
        # -------------------------------------------------------------------------
        # Step 01：确保正式 Face Hierarchy / Config Schema 已存在
        # -------------------------------------------------------------------------
        self.ensure_hierarchy()
        self.ensure_config_layout()

        # -------------------------------------------------------------------------
        # Step 02：开始构建前把 Step 03 / Step 04 状态恢复为未完成
        # -------------------------------------------------------------------------
        self.set_step_completed(
            completed=False
        )
        self.invalidate_later_steps()
        self.set_current_step_value(
            3
        )

        # -------------------------------------------------------------------------
        # Step 03：创建本次唯一的 FaceRig Orchestrator 和结果容器
        # -------------------------------------------------------------------------
        self.face_rig = FaceRig()
        self.build_result = {}
        return True

    def process_data(self):
        u"""
        通过 FaceRig.create_build() 完整构建全部正式 Face Module。

        Returns:
            dict:
                Key 为 Module Part，Value 为对应 Module 的公开构建结果。

        Raises:
            RuntimeError:
                Module 数量、返回结构或 built 状态不符合统一契约时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：FaceRig 只负责编排依赖顺序，具体算法仍由各 Module 自己执行
        # -------------------------------------------------------------------------
        self.build_result = self.face_rig.create_build()

        # -------------------------------------------------------------------------
        # Step 02：确认 Orchestrator 返回的 Module 数量与正式 Module Class 一致
        # -------------------------------------------------------------------------
        expected_module_count = len(
            self.face_rig.module_classes
        )

        if len(self.build_result) != expected_module_count:
            raise RuntimeError(
                u"FaceRig Module 数量错误：期望 {}，实际 {}。".format(
                    expected_module_count,
                    len(self.build_result)
                )
            )

        # -------------------------------------------------------------------------
        # Step 03：逐模块验证统一公开结果，正式 Build 不允许 silently skip
        # -------------------------------------------------------------------------
        for module_part in self.build_result:
            module_result = self.build_result.get(
                module_part
            )

            if not isinstance(module_result, dict):
                raise RuntimeError(
                    u"{} Module 没有返回 dict。".format(
                        module_part
                    )
                )

            if module_result.get("skipped"):
                raise RuntimeError(
                    u"{} Module 在正式 Step 03 中被跳过。".format(
                        module_part
                    )
                )

            if module_result.get("built") is not True:
                raise RuntimeError(
                    u"{} Module 没有返回 built=True。".format(
                        module_part
                    )
                )

        # -------------------------------------------------------------------------
        # Step 04：返回完整结果，供 UI / Runtime Test / 后续 Finalize 使用
        # -------------------------------------------------------------------------
        return self.build_result

    def finalize_step(self):
        u"""
        标记 Step 03 完成，并把 Workflow 推进到 Step 04 Finalize。

        Returns:
            bool:
                Step 03 状态成功保存后返回 True。
        """
        # -------------------------------------------------------------------------
        # Step 01：只有全部 Module 校验通过后才写入正式完成状态
        # -------------------------------------------------------------------------
        self.set_step_completed(
            completed=True
        )

        # -------------------------------------------------------------------------
        # Step 02：Step 03 重建会让后续 Finalize 失效，确保 Step 04 为未完成
        # -------------------------------------------------------------------------
        self.invalidate_later_steps()

        # -------------------------------------------------------------------------
        # Step 03：成功后把 Workflow 推进到 Step 04，并整理 Config Attribute
        # -------------------------------------------------------------------------
        self.set_current_step_value(
            4
        )
        self.organize_config_attributes()
        return True


def build_face_step():
    u"""
    执行完整 Face Workflow Step 03，并返回全部 Module 构建结果。

    Returns:
        dict:
            FaceRig.create_build() 返回的全部正式 Module 结果。
    """
    face_build = FaceBuild()
    face_build.run_step()
    return face_build.build_result


__all__ = [
    "FaceBuild",
    "build_face_step",
]
