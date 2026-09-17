# coding=utf-8
u"""
muziToolset
===========

MuziTools Maya Rigging Toolset 根包与公开启动入口。

当前正式 Runtime 分层：
    app
        Maya 应用入口、主工具箱和窗口生命周期。

    ui
        通用 PySide Theme、Window 与可复用 Widget。

    core/common
        Attribute、Hierarchy、Naming、Transform 等通用 Maya 能力。

    core/rigging
        Controller、Guide、Joint 等 Rig Primitive。

    systems
        完整、可重复构建的 Rig Module / Workflow。
        当前通用 Module Lifecycle 位于 systems/rig_module.py。

    tools
        绑定师直接使用的小型 UI / Action Tool；部分旧 Tool 仍处于 Core 迁移期。

    resources
        Controller Shape、Face Guide、Icon 等静态资源。

主要公开入口：
    show()
        打开 MuziTools 主工具箱。

    show_rig_library()
        打开当前四步模块化绑定库。

    initialize()
        与 show() 等价的初始化入口。

当前核心约定：
    - Rig 标准命名由 core.common.name_utils.Name 负责；
    - Module Lifecycle 由 systems.rig_module.RigModule 负责；
    - Controller Primitive 由 core.rigging.ctrl_utils.Ctrl 负责；
    - Joint Primitive 由 core.rigging.jnt_utils.Jnt 负责；
    - core/bake 与 legacy_reference 属于历史兼容区，不定义新架构。

兼容说明：
    根包仍暴露若干历史 Smoke Test 包装入口，便于旧 Maya Shelf / 调试脚本继续调用。
    这些函数名可能保留旧架构术语；它们不代表当前推荐 Runtime 分层。
"""

from __future__ import print_function


__version__ = "0.4.0"


def show():
    u"""
    打开 MuziTools 主工具箱。

    这是普通用户进入工具集的顶层入口。函数内部延迟导入 ``app.toolbox``，
    避免仅导入 ``muziToolset`` 时立刻创建 Maya / Qt 窗口。

    Returns:
        object:
        ``app.toolbox.main()`` 创建或恢复的主工具箱窗口。

    Example:
        >>> import muziToolset
            >>> window = muziToolset.show()
    """
    from .app import toolbox

    return toolbox.main()


def initialize():
    u"""
    初始化并打开 MuziTools 主工具箱。

    当前实现直接转发到 :func:`show`，保留该名称主要用于旧 Shelf、启动脚本
    或需要显式 ``initialize`` 语义的集成入口。

    Returns:
        object:
        ``show()`` 返回的主工具箱窗口。

    Example:
        >>> import muziToolset
            >>> window = muziToolset.initialize()
    """
    return show()


def show_rig_library():
    u"""
    打开当前模块化 Rig Library 窗口。

    Rig Library 使用 Setup → Guide → Ctrl → Final 四步工作流，并通过
    ``systems.rig.library_service.RigLibraryService`` 管理配置、Build、Rebuild、
    Mirror 与 Final Connection。

    Returns:
        object:
        ``tools.rig.modular_rig_tool.main()`` 创建或恢复的 Rig Library 窗口。

    Example:
        >>> import muziToolset
            >>> window = muziToolset.show_rig_library()
    """
    from .tools.rig import modular_rig_tool

    return modular_rig_tool.main()


def smoke_test(test_window_manager=False):
    u"""
    运行仓库保留的 Maya 非破坏性全工具 Smoke Test。

    该函数是测试包装入口，不参与正常 Rig 构建。具体覆盖范围以
    ``tests/maya_smoke_test.py`` 当前实现为准。

    Args:
        test_window_manager (bool):
            是否额外执行 Window Manager 相关检查。

    Returns:
        object:
        ``maya_smoke_test.run()`` 返回的测试结果。
    """
    from .tests import maya_smoke_test

    return maya_smoke_test.run(
        test_window_manager=test_window_manager
    )


def functional_smoke_test():
    u"""
    运行仓库保留的 Maya 全工具功能 Smoke Test。

    该入口会执行比普通导入检查更接近真实操作的功能测试；具体场景修改范围、
    清理方式和结果结构以 ``tests/maya_functional_smoke_test.py`` 为准。

    Returns:
        object:
        ``maya_functional_smoke_test.run()`` 返回的测试结果。
    """
    from .tests import maya_functional_smoke_test

    return maya_functional_smoke_test.run()


def maya2023_smoke_test():
    u"""
    运行仓库当前 Maya 2023 Runtime Smoke Test 入口。

    这是测试包装函数；它不定义当前 Rig 架构。实际测试契约以
    ``tests/maya2023_smoke_test.py`` 当前内容为准。

    Returns:
        object:
        ``maya2023_smoke_test.run()`` 返回的测试结果。
    """
    from .tests import maya2023_smoke_test

    return maya2023_smoke_test.run()


def face_modules_maya2023_smoke_test():
    u"""
    运行仓库保留的 Face Modules Maya 2023 Smoke Test。

    该函数属于历史 / 兼容测试入口。当前正式 Face Runtime 以
    ``systems/face``、``systems/rig/library_service.py`` 和 Rig Library 四步工作流
    为事实来源；测试脚本内部若仍引用旧 Face 类型，应按测试迁移任务单独更新。

    Returns:
        dict:
        测试脚本返回的逐项结果与统计数据。
    """
    from .tests import face_modules_maya2023_smoke_test

    return face_modules_maya2023_smoke_test.run()


def face_build_step_maya2023_smoke_test():
    u"""
    运行仓库保留的旧 Face Build Step Maya 2023 Smoke Test。

    当前 Rig Library 已采用 Setup → Guide → Ctrl → Final 流程，因此这个函数名
    中的旧 Step 语义仅用于兼容已有测试入口，不应作为当前工作流文档依据。

    Returns:
        dict:
        ``face_build_step_maya2023_smoke_test.run()`` 返回的测试数据。
    """
    from .tests import face_build_step_maya2023_smoke_test

    return face_build_step_maya2023_smoke_test.run()


def face_controller_appearance_maya2023_smoke_test():
    u"""
    运行 Face Controller Appearance Maya 2023 Smoke Test。

    该测试入口用于验证控制器外观修改不会意外改变 Rig Transform / Output。
    当前实际外观工作流以 Rig Library Step 03 和 ``core.rigging.ctrl_utils`` 为准。

    Returns:
        dict:
        测试脚本返回的外观验证结果。
    """
    from .tests import face_controller_appearance_maya2023_smoke_test

    return face_controller_appearance_maya2023_smoke_test.run()


def face_finalize_step_maya2023_smoke_test():
    u"""
    运行仓库保留的 Face Finalize Maya 2023 Smoke Test。

    当前模块化绑定的正式 Final 行为由 ``RigLibraryService.finalize()`` 与各 Module
    的 ``connect_outputs()`` 定义。本函数仅作为旧测试套件兼容入口。

    Returns:
        dict:
        测试脚本返回的 Finalize 验证结果。
    """
    from .tests import face_finalize_step_maya2023_smoke_test

    return face_finalize_step_maya2023_smoke_test.run()


def pipeline_smoke_test():
    u"""
    运行仓库保留的 Pipeline / Core 迁移 Smoke Test。

    该入口主要用于历史迁移验证；当前正式 Core 结构是 ``core/common`` 与
    ``core/rigging``，而不是旧的平铺 ``core.*_utils`` 架构。

    Returns:
        object:
        ``pipeline_refactor_smoke_test.run()`` 返回的测试结果。
    """
    from .tests import pipeline_refactor_smoke_test

    return pipeline_refactor_smoke_test.run()


def extended_core_smoke_test():
    u"""
    运行仓库保留的 Extended Core Smoke Test。

    这是兼容测试包装入口。测试脚本若仍包含退休 Core / RigBase 名称，表示对应
    测试尚未完成迁移，不代表这些路径重新成为正式 Runtime 架构。

    Returns:
        object:
        ``extended_core_smoke_test.run()`` 返回的测试结果。
    """
    from .tests import extended_core_smoke_test

    return extended_core_smoke_test.run()


def core_import_style_test():
    u"""
    运行 Core Import Style 静态检查包装入口。

    Returns:
        object:
        ``core_import_style_test.run()`` 返回的检查结果。
    """
    from .tests import core_import_style_test

    return core_import_style_test.run()


def rig_architecture_gate_test():
    u"""
    运行仓库 Rig Architecture Gate 静态检查包装入口。

    Gate 的具体禁止项以 ``tests/rig_architecture_gate_test.py`` 当前实现为准；
    根包不在这里复制另一份架构规则，避免测试与文档再次漂移。

    Returns:
        object:
        ``rig_architecture_gate_test.run()`` 返回的检查结果。
    """
    from .tests import rig_architecture_gate_test

    return rig_architecture_gate_test.run()


def rig_base_contract_test():
    u"""
    运行仓库保留的 RigBase Contract Test 包装入口。

    ``RigBase`` 属于旧架构术语；保留此函数是为了兼容历史测试调用。
    当前 Naming 事实来源是 ``core.common.name_utils.Name``。

    Returns:
        object:
        ``rig_base_contract_test.run()`` 返回的测试结果。
    """
    from .tests import rig_base_contract_test

    return rig_base_contract_test.run()


def module_base_contract_test():
    u"""
    运行仓库保留的 ModuleBase Contract Test 包装入口。

    当前正式 Module Lifecycle 位于 ``systems.rig_module.RigModule``；本函数名称
    保留旧测试兼容语义，不表示 ``ModuleBase / RigModuleBase`` 仍是正式架构。

    Returns:
        object:
        ``module_base_contract_test.run()`` 返回的测试结果。
    """
    from .tests import module_base_contract_test

    return module_base_contract_test.run()


def tool_window_smoke_test():
    u"""
    运行正式 UI Tool 的 Direct Main 窗口 Smoke Test。

    Returns:
        object:
        ``tool_window_smoke_test.run()`` 返回的窗口测试结果。
    """
    from .tests import tool_window_smoke_test

    return tool_window_smoke_test.run()


def face_build_smoke_test():
    u"""
    运行仓库保留的旧 Face Build Smoke Test 包装入口。

    该测试脚本可能覆盖历史 Eyelid / Curve Attachment / Zip Lip 实现；当前正式
    Face Module 可用范围应以 ``systems/face`` 和 Rig Library Catalog 为准。

    Returns:
        object:
        ``face_build_smoke_test.run()`` 返回的测试结果。
    """
    from .tests import face_build_smoke_test

    return face_build_smoke_test.run()


def ctrl_base_smoke_test():
    u"""
    运行仓库保留的 CtrlBase Smoke Test 包装入口。

    ``CtrlBase`` 是历史架构名称；当前正式 Controller Primitive 位于
    ``core.rigging.ctrl_utils.Ctrl``。保留本入口只用于兼容已有测试调用。

    Returns:
        object:
        ``ctrl_base_smoke_test.run()`` 返回的测试结果。
    """
    from .tests import ctrl_base_smoke_test

    return ctrl_base_smoke_test.run()


def rig_integration_test(keep_result=False):
    u"""
    运行仓库保留的 Rig 跨模块 Integration Test。

    Args:
        keep_result (bool):
            为 True 时按测试脚本约定保留生成结果；具体清理行为以测试实现为准。

    Returns:
        object:
        ``rig_integration_test.run()`` 返回的集成测试结果。
    """
    from .tests import rig_integration_test

    return rig_integration_test.run(
        keep_result=keep_result
    )


__all__ = [
    "show",
    "show_rig_library",
    "initialize",
    "smoke_test",
    "functional_smoke_test",
    "maya2023_smoke_test",
    "face_modules_maya2023_smoke_test",
    "face_build_step_maya2023_smoke_test",
    "face_controller_appearance_maya2023_smoke_test",
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
