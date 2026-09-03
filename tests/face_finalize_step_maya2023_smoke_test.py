# coding=utf-8
u"""
Face Finalize Step Maya 2023 Runtime Smoke Test
===============================================

在真正 Autodesk Maya 2023 中验证完整 Face Workflow：

    FaceSetup.run_step()
        -> FaceGuide.build_guide() / run_step()
            -> FaceBuild.run_step()
                -> 11 个正式 Face Module
                    -> FaceFinalizer.run_step()

成功标准：
    - Step 03 完整 FaceBuild 无异常；
    - FaceFinalizer.run_step() 无异常；
    - Controller 数量大于 0；
    - Face Controller Set 为 objectSet，并已通过 Finalizer 成员校验；
    - Step 04 Visibility 与 config.py 完全一致；
    - Step 04 标记完成；
    - Current Face Step 保持 04；
    - 第二次执行 Finalize 仍成功，且 Controller 数量保持一致。
"""

from __future__ import print_function

import traceback

import maya.cmds as cmds

from ..systems import face as face_system
from ..systems.face import config as face_config
from .face_modules_maya2023_smoke_test import create_face_fixture
from .face_modules_maya2023_smoke_test import prepare_default_shading_group
from .face_modules_maya2023_smoke_test import restore_default_shading_group
from .maya2023_smoke_test import create_namespace
from .maya2023_smoke_test import remove_namespace
from .maya2023_smoke_test import require_maya_2023


def validate_finalize_result(finalizer):
    u"""
    验证 FaceFinalizer 的场景结果和 Workflow 状态。

    Args:
        finalizer (FaceFinalizer):
            已执行 run_step() 的 Step 04 实例。

    Returns:
        dict:
            Runtime Smoke 使用的精简验证摘要。

    Raises:
        RuntimeError:
            Controller、Set、Visibility 或 Step 状态不符合契约时抛出。
    """
    validation = finalizer.validation_result

    if not isinstance(validation, dict):
        raise RuntimeError(
            u"FaceFinalizer.validation_result 必须是 dict。"
        )

    controller_count = validation.get(
        "controller_count",
        0
    )

    if controller_count <= 0:
        raise RuntimeError(
            u"Face Finalize Controller 数量必须大于 0。"
        )

    controller_set = validation.get(
        "controller_set"
    )

    if not controller_set:
        raise RuntimeError(
            u"Face Finalize 没有返回 Controller Set。"
        )

    if not cmds.objExists(
            controller_set
    ):
        raise RuntimeError(
            u"Face Controller Set 不存在：{}".format(
                controller_set
            )
        )

    if cmds.nodeType(
            controller_set
    ) != "objectSet":
        raise RuntimeError(
            u"Face Controller Set 不是 objectSet：{}".format(
                controller_set
            )
        )

    visibility = validation.get(
        "visibility"
    )

    if not isinstance(visibility, dict):
        raise RuntimeError(
            u"Face Finalize Visibility 结果必须是 dict。"
        )

    expected_visibility = face_config.face_step_visibility_rules.get(
        4,
        {}
    )

    for group_key in expected_visibility:
        if group_key not in visibility:
            raise RuntimeError(
                u"Face Finalize Visibility 缺少：{}".format(
                    group_key
                )
            )

        expected_value = bool(
            expected_visibility.get(
                group_key
            )
        )
        actual_value = bool(
            visibility.get(
                group_key
            )
        )

        if actual_value == expected_value:
            continue

        raise RuntimeError(
            u"Face Finalize Visibility 错误：{} expected={} actual={}".format(
                group_key,
                expected_value,
                actual_value
            )
        )

    if not finalizer.is_step_completed(
            step_value=4
    ):
        raise RuntimeError(
            u"Face Finalize 完成后 step_04_completed 不是 True。"
        )

    current_step_value = finalizer.get_current_step_value()

    if current_step_value != 4:
        raise RuntimeError(
            u"Face Finalize 完成后 Current Face Step 应保持 4，实际为 {}。".format(
                current_step_value
            )
        )

    return {
        "controller_count": controller_count,
        "controller_set": controller_set,
        "visibility": visibility,
        "step_04_completed": True,
        "current_step": current_step_value,
    }


def run():
    u"""
    在 Maya 2023 中执行完整 Face Step 03 + Step 04 Runtime Smoke。

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
        "Muzi Toolset - Face Finalize Step Maya 2023 Runtime Smoke Test"
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
        # Step 02：执行完整 Step 03 FaceBuild
        # ---------------------------------------------------------------------
        face_build = face_system.FaceBuild()
        face_build.run_step()

        if not face_build.is_step_completed(
                step_value=3
        ):
            raise RuntimeError(
                u"进入 Finalize 前 Step 03 没有完成。"
            )

        print(
            u"[PASS] FaceBuild | 11 Module 完整构建成功"
        )

        # ---------------------------------------------------------------------
        # Step 03：执行第一次正式 Finalize，并校验场景结果
        # ---------------------------------------------------------------------
        finalizer = face_system.FaceFinalizer()
        finalizer.run_step()
        summary = validate_finalize_result(
            finalizer
        )

        print(
            u"[PASS] FaceFinalize | Controller Set + Visibility 验收成功"
        )

        # ---------------------------------------------------------------------
        # Step 04：再次执行 Finalize，验证幂等性
        # ---------------------------------------------------------------------
        second_finalizer = face_system.FaceFinalizer()
        second_finalizer.run_step()
        second_summary = validate_finalize_result(
            second_finalizer
        )

        if second_summary.get(
                "controller_count"
        ) != summary.get(
                "controller_count"
        ):
            raise RuntimeError(
                u"重复 Finalize 后 Controller 数量发生变化：{} -> {}".format(
                    summary.get("controller_count"),
                    second_summary.get("controller_count")
                )
            )

        print(
            u"[PASS] Idempotent | 第二次 Finalize 结果稳定"
        )
        print(
            u"[PASS] Workflow | Step04=True · Current Step=04"
        )
        print(
            "-" * 78
        )
        print(
            u"Passed: 5 | Failed: 0"
        )
        print(
            "=" * 78
        )

        summary["second_finalize_controller_count"] = second_summary.get(
            "controller_count"
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
            u"[FAIL] FaceFinalize | {}".format(
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
