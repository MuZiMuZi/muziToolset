# coding=utf-8
u"""
muziToolset
===========

木子 Maya Rigging Toolset 根包。

正式框架直接位于仓库根包：
    app         Maya 应用入口与窗口管理
    ui          通用 PySide UI、主题与组件
    core        不依赖具体 UI 的 Maya 底层功能
    tools       独立的小型绑定工具
    systems     完整绑定系统
    resources   图标、Controller Shape 等资源
"""

from __future__ import print_function


__version__ = "0.3.0"


def show():
    """打开 Muzi Rigging 主工具箱。"""
    from .app import toolbox

    return toolbox.main()


def initialize():
    """初始化并打开主工具箱。"""
    return show()


def smoke_test(test_window_manager=False):
    """运行 Maya 2023 非破坏性全工具 Smoke Test。"""
    from .tests import maya_smoke_test

    return maya_smoke_test.run(
        test_window_manager=test_window_manager
    )


def functional_smoke_test():
    """运行 Maya 2023 全工具真实功能 Smoke Test。"""
    from .tests import maya_functional_smoke_test

    return maya_functional_smoke_test.run()


def pipeline_smoke_test():
    """运行 pipelineUtils / Legacy Core 拆分后的功能 Smoke Test。"""
    from .tests import pipeline_refactor_smoke_test

    return pipeline_refactor_smoke_test.run()


def face_component_smoke_test():
    """运行 Face Eyelid / Curve Attachment / Zip Lip 功能 Smoke Test。"""
    from .tests import face_component_smoke_test

    return face_component_smoke_test.run()


def controller_component_smoke_test():
    """运行 Controller Parent Space Blend 功能 Smoke Test。"""
    from .tests import controller_component_smoke_test

    return controller_component_smoke_test.run()


__all__ = [
    "show",
    "initialize",
    "smoke_test",
    "functional_smoke_test",
    "pipeline_smoke_test",
    "face_component_smoke_test",
    "controller_component_smoke_test",
]
