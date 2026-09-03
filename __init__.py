# coding=utf-8
u"""
muziToolset
===========

木子 Maya Rigging Toolset 根包。

正式框架：
    app         Maya 应用入口与窗口管理
    ui          通用 PySide UI、主题与组件
    core        不依赖具体 Rig 业务的 Maya 底层功能
    tools       独立的小型绑定工具
    systems     RigBase / ModuleBase / CtrlBase 和完整绑定系统
    resources   图标、Controller Shape 等资源

0.4 架构约定：
    - Rig Naming -> systems.rig_base.RigBase
    - Rig Lifecycle -> systems.module_base.ModuleBase / RigModuleBase
    - Controller Workflow -> systems.ctrl_base
    - 完整业务单元统一称为 Module，不再使用 Component
"""

from __future__ import print_function


__version__ = "0.4.0"


def show():
    u"""
    打开 Muzi Rigging 主工具箱。

    Returns:
        object:
        当前工具入口创建并显示的窗口或执行结果。
    """
    from .app import toolbox

    return toolbox.main()


def initialize():
    u"""
    初始化并打开主工具箱。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    return show()


def smoke_test(test_window_manager=False):
    u"""
    运行 Maya 2023 非破坏性全工具 Smoke Test。

    Args:
        test_window_manager (bool):
            包初始化阶段是否运行 Window Manager 自检。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import maya_smoke_test

    return maya_smoke_test.run(
        test_window_manager=test_window_manager
    )


def functional_smoke_test():
    u"""
    运行 Maya 2023 全工具真实功能 Smoke Test。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import maya_functional_smoke_test

    return maya_functional_smoke_test.run()


def maya2023_smoke_test():
    u"""
    运行当前 Rig 架构的 Maya 2023 Runtime Smoke Test。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import maya2023_smoke_test

    return maya2023_smoke_test.run()


def face_modules_maya2023_smoke_test():
    u"""
    逐模块运行新 Face Rig 架构的 Maya 2023 Runtime Smoke Test。

    测试会使用正式 FaceSetup、FaceGuide 和 face_guide.ma，然后按依赖顺序执行
    Brow / Eye / Eyelid / Nose / Cheek / Ear / Jaw / Teeth / Tongue / Lip / Mouth。

    Returns:
        dict:
        Maya 版本、逐模块 PASS / FAIL / SKIP 结果和统计数量。
    """
    from .tests import face_modules_maya2023_smoke_test

    return face_modules_maya2023_smoke_test.run()


def face_build_step_maya2023_smoke_test():
    u"""
    运行完整 Face Workflow Step 03 的 Maya 2023 Runtime Smoke Test。

    测试只通过 FaceBuild.run_step() 进入 FaceRig，并验证 11 个正式 Module
    全部构建成功、Step 03 完成以及 Current Face Step 推进到 Step 04。

    Returns:
        dict:
        Maya 版本、完整 FaceBuild 通过状态、Step 状态与精简 Module 摘要。
    """
    from .tests import face_build_step_maya2023_smoke_test

    return face_build_step_maya2023_smoke_test.run()


def face_finalize_step_maya2023_smoke_test():
    u"""
    运行完整 Face Workflow Step 04 的 Maya 2023 Runtime Smoke Test。

    测试先通过 FaceBuild.run_step() 完成 11 Module，然后执行 FaceFinalizer，
    验证 Controller Set、最终 Visibility、Step04 状态以及重复 Finalize 的幂等性。

    Returns:
        dict:
        Maya 版本、Finalize 通过状态、Controller / Visibility 摘要和失败 Traceback。
    """
    from .tests import face_finalize_step_maya2023_smoke_test

    return face_finalize_step_maya2023_smoke_test.run()


def pipeline_smoke_test():
    u"""
    运行基础 Core / Legacy Pipeline 拆分后的功能 Smoke Test。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import pipeline_refactor_smoke_test

    return pipeline_refactor_smoke_test.run()


def extended_core_smoke_test():
    u"""
    运行 Extended Core / RigBase Smoke Test。

    测试范围：
        attr_utils
        hierarchy_utils
        joint_utils
        RigBase / rename_utils
        model_check_utils
        scene_utils

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import extended_core_smoke_test

    return extended_core_smoke_test.run()


def core_import_style_test():
    u"""
    运行旧 CamelCase Core Import Gate。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import core_import_style_test

    return core_import_style_test.run()


def rig_architecture_gate_test():
    u"""
    检查退休的 name_utils / Component / controller 包是否重新出现。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import rig_architecture_gate_test

    return rig_architecture_gate_test.run()


def rig_base_contract_test():
    u"""
    运行 RigBase Naming Contract Test。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import rig_base_contract_test

    return rig_base_contract_test.run()


def module_base_contract_test():
    u"""
    运行 ModuleBase / RigModuleBase Lifecycle Contract Test。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import module_base_contract_test

    return module_base_contract_test.run()


def tool_window_smoke_test():
    u"""
    运行所有正式 UI Tool 的 Direct Main 窗口 Smoke Test。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import tool_window_smoke_test

    return tool_window_smoke_test.run()


def face_build_smoke_test():
    u"""
    运行 Face Eyelid / Curve Attachment / Zip Lip Build Smoke Test。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import face_build_smoke_test

    return face_build_smoke_test.run()


def ctrl_base_smoke_test():
    u"""
    运行 CtrlBase Controller / Follow Smoke Test。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import ctrl_base_smoke_test

    return ctrl_base_smoke_test.run()


def rig_integration_test(keep_result=False):
    u"""
    运行基础 Rig 跨模块 Integration Test。

    Args:
        keep_result (bool):
            控制当前方法中的 `keep_result` 选项是否启用。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    from .tests import rig_integration_test

    return rig_integration_test.run(
        keep_result=keep_result
    )


__all__ = [
    "show",
    "initialize",
    "smoke_test",
    "functional_smoke_test",
    "maya2023_smoke_test",
    "face_modules_maya2023_smoke_test",
    "face_build_step_maya2023_smoke_test",
    "face_finalize_step_maya2023_smoke_test",
    "pipeline_smoke_test",
    "extended_core_smoke_test",
    "core_import_style_test",
    "rig_architecture_gate_test",
    "rig_base_contract_test",
    "module_base_contract_test",
    "tool_window_smoke_test",
    "face_build_smoke_test",
    "ctrl_base_smoke_test",
    "rig_integration_test",
]
