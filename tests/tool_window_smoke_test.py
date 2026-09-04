# coding=utf-8
u"""
Tool Window Smoke Test
======================

验证所有正式 UI Tool 的独立 ``main()`` 窗口入口。

测试目标：
    1. ``main()`` 返回有效 QWidget / QDialog；
    2. 窗口调用后立即可见；
    3. 同一个 Tool 连续调用 ``main()`` 返回同一个有效实例；
    4. ``ui.window_utils`` 可以统一关闭窗口；
    5. 测试只创建 UI，不执行绑定、清理、重命名等场景操作。

不参与本测试：
    - tools.basic.snap_tool：执行型 Tool；
    - tools.controller.create_fk_ctrl_tool：执行型 Tool。

兼容：
    Maya 2023+ / PySide2，Maya 2025+ 可使用 PySide6 fallback。
"""

from __future__ import print_function

import traceback

try:
    from PySide2.QtWidgets import QApplication
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtWidgets import QWidget

from ..ui import window_utils
from ..tools.basic import attr_tool
from ..tools.basic import connections_tool
from ..tools.basic import constraint_tool
from ..tools.basic import rename_tool
from ..tools.blendshape import add_blendshape_tool
from ..tools.blendshape import invert_shape_tool
from ..tools.clean import hierarchy_cleaner
from ..tools.clean import model_checker
from ..tools.controller import control_shape_tool
from ..tools.controller import create_ctrl_tool
from ..tools.face import face_rig_tool
from ..tools.face import face_select_key_tool
from ..tools.jnt import jnt_resamp_tool
from ..tools.jnt import jnt_tool
from ..tools.rig import rig_tool
from ..tools.rig import skirt_ctrl_tool
from ..tools.skin import skin_tool


# =============================================================================
# Test Cases
# =============================================================================

def get_test_cases():
    """返回正式 UI Tool 的窗口测试列表。"""
    return [
        (
            "basic.attr_tool",
            "tools.basic.attr_tool",
            attr_tool.main,
        ),
        (
            "basic.connections_tool",
            "tools.basic.connections_tool",
            connections_tool.main,
        ),
        (
            "basic.constraint_tool",
            "tools.basic.constraint_tool",
            constraint_tool.main,
        ),
        (
            "basic.rename_tool",
            "tools.basic.rename_tool",
            rename_tool.main,
        ),
        (
            "blendshape.add_blendshape_tool",
            "tools.blendshape.add_blendshape_tool",
            add_blendshape_tool.main,
        ),
        (
            "blendshape.invert_shape_tool",
            "tools.blendshape.invert_shape_tool",
            invert_shape_tool.main,
        ),
        (
            "clean.hierarchy_cleaner",
            "tools.clean.hierarchy_cleaner",
            hierarchy_cleaner.main,
        ),
        (
            "clean.model_checker",
            "tools.clean.model_checker",
            model_checker.main,
        ),
        (
            "controller.control_shape_tool",
            "tools.controller.control_shape_tool",
            control_shape_tool.main,
        ),
        (
            "controller.create_ctrl_tool",
            "tools.controller.create_ctrl_tool",
            create_ctrl_tool.main,
        ),
        (
            "face.face_rig_tool",
            "tools.face.face_rig_tool",
            face_rig_tool.main,
        ),
        (
            "face.face_select_key_tool",
            "tools.face.face_select_key_tool",
            face_select_key_tool.main,
        ),
        (
            "jnt.jnt_resamp_tool",
            "tools.jnt.jnt_resamp_tool",
            jnt_resamp_tool.main,
        ),
        (
            "jnt.jnt_tool",
            "tools.jnt.jnt_tool",
            jnt_tool.main,
        ),
        (
            "rig.rig_tool",
            "tools.rig.rig_tool",
            rig_tool.main,
        ),
        (
            "rig.skirt_ctrl_tool",
            "tools.rig.skirt_ctrl_tool",
            skirt_ctrl_tool.main,
        ),
        (
            "skin.skin_tool",
            "tools.skin.skin_tool",
            skin_tool.main,
        ),
    ]


def process_events():
    """让 Qt 处理 show / close / deleteLater 等待处理事件。"""
    application = QApplication.instance()

    if application is not None:
        application.processEvents()


# =============================================================================
# Single Case
# =============================================================================

def test_window_case(label, window_key, main_function):
    """测试一个 UI Tool 的 Direct Main 生命周期。"""
    # -------------------------------------------------------------------------
    # 步骤 1：确保上一轮同名窗口不会干扰当前测试。
    # -------------------------------------------------------------------------
    window_utils.close_window(window_key)
    process_events()

    first_window = None

    try:
        # ---------------------------------------------------------------------
        # 步骤 2：第一次 main() 必须创建、显示并返回有效 QWidget。
        # ---------------------------------------------------------------------
        first_window = main_function()
        process_events()

        if not isinstance(first_window, QWidget):
            raise RuntimeError(
                u"main() 没有返回 QWidget：{}".format(label)
            )

        if not first_window.isVisible():
            raise RuntimeError(
                u"main() 返回窗口但窗口不可见：{}".format(label)
            )

        cached_window = window_utils.get_window(window_key)

        if cached_window is not first_window:
            raise RuntimeError(
                u"window_utils 缓存实例与 main() 返回值不一致：{}".format(
                    label
                )
            )

        # ---------------------------------------------------------------------
        # 步骤 3：第二次 main() 必须恢复同一个实例，而不是重复创建窗口。
        # ---------------------------------------------------------------------
        second_window = main_function()
        process_events()

        if second_window is not first_window:
            raise RuntimeError(
                u"重复 main() 创建了第二个窗口实例：{}".format(label)
            )

        if not second_window.isVisible():
            raise RuntimeError(
                u"重复 main() 后窗口不可见：{}".format(label)
            )

        return u"Direct Main + Visible + Single Instance 成功"

    finally:
        # ---------------------------------------------------------------------
        # 步骤 4：无论测试成功还是失败，都关闭当前 Tool，避免 Smoke Test 留下一排窗口。
        # ---------------------------------------------------------------------
        window_utils.close_window(window_key)
        process_events()


# =============================================================================
# Runner
# =============================================================================

def run():
    """运行全部 UI Tool Direct Main Smoke Test。"""
    print("=" * 78)
    print("Muzi Toolset - Tool Window Smoke Test")
    print("=" * 78)

    results = []
    passed_count = 0
    failed_count = 0

    test_cases = get_test_cases()

    for label, window_key, main_function in test_cases:
        try:
            message = test_window_case(
                label,
                window_key,
                main_function
            )
            passed = True
            passed_count += 1

            print(
                u"[PASS] {} | {}".format(
                    label,
                    message
                )
            )

        except Exception as error:
            passed = False
            failed_count += 1
            message = u"{}".format(error)

            print(
                u"[FAIL] {} | {}".format(
                    label,
                    message
                )
            )
            traceback.print_exc()

        results.append({
            "name": label,
            "passed": passed,
            "message": message,
        })

    print("-" * 78)
    print(
        "Total: {} | Passed: {} | Failed: {}".format(
            len(test_cases),
            passed_count,
            failed_count
        )
    )
    print("=" * 78)

    return {
        "total": len(test_cases),
        "passed": passed_count,
        "failed": failed_count,
        "results": results,
    }


__all__ = [
    "get_test_cases",
    "test_window_case",
    "run",
]
