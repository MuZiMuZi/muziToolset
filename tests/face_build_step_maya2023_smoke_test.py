# coding=utf-8
u"""
Face Build Step Maya 2023 Runtime Smoke Test
============================================

在真正 Autodesk Maya 2023 中验证完整 Step 03 Workflow：

    FaceSetup.run_step()
        -> FaceGuide.build_guide() / run_step()
            -> FaceBuild.run_step()
                -> FaceRig.create_build()
                    -> 11 个正式 Face Module

成功标准：
    - FaceBuild.run_step() 无异常；
    - 11 个 Module 都返回 built=True；
    - 没有 Module skipped；
    - Step 03 标记完成；
    - Current Face Step 推进到 Step 04。
"""

from __future__ import print_function

import traceback

from ..systems import face as face_system
from .face_modules_maya2023_smoke_test import create_face_fixture
from .face_modules_maya2023_smoke_test import prepare_default_shading_group
from .face_modules_maya2023_smoke_test import restore_default_shading_group
from .maya2023_smoke_test import create_namespace
from .maya2023_smoke_test import remove_namespace
from .maya2023_smoke_test import require_maya_2023


EXPECTED_MODULE_PARTS = [
    "brow",
    "eye",
    "eyelid",
    "nose",
    "cheek",
    "ear",
    "jaw",
    "teeth",
    "tongue",
    "lip",
    "mouth",
]


def validate_face_build_result(face_build):
    u"""
    验证完整 FaceBuild 的 Module 结果和 Workflow 状态。

    Args:
        face_build (FaceBuild):
            已执行 run_step() 的 Step 03 实例。

    Returns:
        dict:
            Runtime Smoke 使用的精简验证摘要。

    Raises:
        RuntimeError:
            Module 结果或 Step 03 状态不符合契约时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：确认 Step 03 返回完整 Module Dict，并保持固定 Module 顺序
    # -------------------------------------------------------------------------
    build_result = face_build.build_result

    if not isinstance(build_result, dict):
        raise RuntimeError(
            u"FaceBuild.build_result 必须是 dict。"
        )

    actual_module_parts = []

    for module_part in build_result:
        actual_module_parts.append(
            module_part
        )

    if actual_module_parts != EXPECTED_MODULE_PARTS:
        raise RuntimeError(
            u"FaceBuild Module 顺序错误：{}".format(
                actual_module_parts
            )
        )

    # -------------------------------------------------------------------------
    # Step 02：逐模块确认 built=True 且没有 skipped
    # -------------------------------------------------------------------------
    for module_part in EXPECTED_MODULE_PARTS:
        module_result = build_result.get(
            module_part
        )

        if not isinstance(module_result, dict):
            raise RuntimeError(
                u"{} Module Result 不是 dict。".format(
                    module_part
                )
            )

        if module_result.get("skipped"):
            raise RuntimeError(
                u"{} Module 不应在完整 FaceBuild 中 skipped。".format(
                    module_part
                )
            )

        if module_result.get("built") is not True:
            raise RuntimeError(
                u"{} Module 没有 built=True。".format(
                    module_part
                )
            )

    # -------------------------------------------------------------------------
    # Step 03：确认 Workflow 已正式完成 Step 03，并推进到 Step 04
    # -------------------------------------------------------------------------
    if not face_build.is_step_completed(
            step_value=3
    ):
        raise RuntimeError(
            u"FaceBuild 完成后 step_03_completed 不是 True。"
        )

    current_step_value = face_build.get_current_step_value()

    if current_step_value != 4:
        raise RuntimeError(
            u"FaceBuild 完成后 Current Face Step 应为 4，实际为 {}。".format(
                current_step_value
            )
        )

    # -------------------------------------------------------------------------
    # Step 04：返回精简摘要，避免再次打印完整 Module Dict
    # -------------------------------------------------------------------------
    return {
        "module_count": len(actual_module_parts),
        "module_parts": actual_module_parts,
        "step_03_completed": True,
        "current_step": current_step_value,
    }


def run():
    u"""
    在 Maya 2023 中执行完整 FaceBuild Step Runtime Smoke。

    Returns:
        dict:
            Maya 版本、通过状态、摘要和失败 Traceback。
    """
    maya_version = require_maya_2023()
    namespace = create_namespace()
    shading_group_state = prepare_default_shading_group()

    print(
        "=" * 78
    )
    print(
        "Muzi Toolset - Face Build Step Maya 2023 Runtime Smoke Test"
    )
    print(
        "Maya: {}".format(
            maya_version
        )
    )
    print(
        "=" * 78
    )

    try:
        # ---------------------------------------------------------------------
        # Step 01：创建正式 Setup + Guide Fixture
        # ---------------------------------------------------------------------
        create_face_fixture()
        print(
            u"[PASS] Face Fixture | Step01 + Step02 准备成功"
        )

        # ---------------------------------------------------------------------
        # Step 02：只通过正式 FaceBuild.run_step() 执行完整 Step 03
        # ---------------------------------------------------------------------
        face_build = face_system.FaceBuild()
        face_build.run_step()

        # ---------------------------------------------------------------------
        # Step 03：校验 11 Module 结果和 Workflow Step 状态
        # ---------------------------------------------------------------------
        summary = validate_face_build_result(
            face_build
        )

        print(
            u"[PASS] FaceBuild | 11 Module 完整构建成功"
        )
        print(
            u"[PASS] Workflow | Step03=True → Current Step=04"
        )
        print(
            "-" * 78
        )
        print(
            u"Passed: 3 | Failed: 0"
        )
        print(
            "=" * 78
        )

        return {
            "maya_version": maya_version,
            "passed": True,
            "failed": 0,
            "summary": summary,
            "traceback": "",
        }

    except Exception as error:
        error_traceback = traceback.format_exc()

        print(
            u"[FAIL] FaceBuild | {}".format(
                error
            )
        )
        print(
            error_traceback
        )
        print(
            "-" * 78
        )
        print(
            u"Passed: 0 | Failed: 1"
        )
        print(
            "=" * 78
        )

        return {
            "maya_version": maya_version,
            "passed": False,
            "failed": 1,
            "summary": None,
            "traceback": error_traceback,
        }

    finally:
        remove_namespace(
            namespace
        )
        restore_default_shading_group(
            shading_group_state
        )


if __name__ == "__main__":
    run()
