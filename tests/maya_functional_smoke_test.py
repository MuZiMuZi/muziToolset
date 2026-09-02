# coding=utf-8
u"""
Maya Functional Smoke Test
==========================

MuziTools Maya 真机功能总调度器。

0.4 架构以后不再在本文件复制各 System 的创建 API，
而是组合正式的专项 Smoke Test：

    Pipeline Core
    Extended Core / RigBase
    CtrlBase
    Face Build
    Rig Integration

这样 RigBase / ModuleBase / CtrlBase 的接口变化只需要修改各自专项测试。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import ctrl_base_smoke_test
from . import extended_core_smoke_test
from . import face_build_smoke_test
from . import pipeline_refactor_smoke_test
from . import rig_integration_test


# =============================================================================
# Helpers
# =============================================================================

def normalize_result(name, result):
    u"""把不同专项 Smoke Test 的统计统一成总报告格式。"""
    passed = int(
        result.get(
            "passed",
            0
        )
    )
    failed = int(
        result.get(
            "failed",
            0
        )
    )

    return {
        "name": name,
        "passed": passed,
        "failed": failed,
        "result": result,
    }


def run_test(name, test_function):
    u"""运行一个专项 Smoke Test，并转换结果。"""
    result = test_function()

    if not isinstance(result, dict):
        raise RuntimeError(
            u"{} Smoke Test 没有返回 dict。".format(
                name
            )
        )

    return normalize_result(
        name,
        result
    )


# =============================================================================
# Runner
# =============================================================================

def run():
    u"""运行 Maya Functional Smoke Test 总套件。"""
    maya_version = str(
        cmds.about(
            version=True
        )
    )

    reports = []

    print("")
    print("=" * 78)
    print("Muzi Toolset - Maya Functional Smoke Test")
    print("Maya: {}".format(maya_version))
    print("Architecture: RigBase / ModuleBase / CtrlBase")
    print("=" * 78)

    test_items = [
        (
            "Pipeline Core",
            pipeline_refactor_smoke_test.run,
        ),
        (
            "Extended Core / RigBase",
            extended_core_smoke_test.run,
        ),
        (
            "CtrlBase",
            ctrl_base_smoke_test.run,
        ),
        (
            "Face Build",
            face_build_smoke_test.run,
        ),
        (
            "Rig Integration",
            rig_integration_test.run,
        ),
    ]

    for test_item in test_items:
        name = test_item[0]
        test_function = test_item[1]

        try:
            report = run_test(
                name,
                test_function
            )
        except Exception as error:
            report = {
                "name": name,
                "passed": 0,
                "failed": 1,
                "result": {
                    "error": str(error),
                },
            }

        reports.append(
            report
        )

    passed_count = 0
    failed_count = 0

    print("")
    print("-" * 78)
    print("Functional Smoke Summary")
    print("-" * 78)

    for report in reports:
        passed_count += report["passed"]
        failed_count += report["failed"]

        status = "PASS"

        if report["failed"]:
            status = "FAIL"

        print(
            "[{}] {} | Passed={} Failed={}".format(
                status,
                report["name"],
                report["passed"],
                report["failed"]
            )
        )

    print("-" * 78)
    print(
        "Passed: {} | Failed: {}".format(
            passed_count,
            failed_count
        )
    )
    print("=" * 78)

    return {
        "maya_version": maya_version,
        "architecture": "RigBase / ModuleBase / CtrlBase",
        "reports": reports,
        "passed": passed_count,
        "failed": failed_count,
    }


__all__ = [
    "run",
]
