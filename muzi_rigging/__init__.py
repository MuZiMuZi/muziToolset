# coding=utf-8
u"""
muzi_rigging
============

木子 Maya Rigging Toolset 主包。

包职责：
    app         Maya 应用入口与窗口管理
    ui          通用 PySide UI、主题与组件
    core        不依赖具体 UI 的 Maya 底层功能
    tools       独立的小型绑定工具
    systems     完整绑定系统，例如 Face Rig、Body Rig
    resources   图标、Controller Shape 等资源
"""

from __future__ import print_function


__version__ = "0.3.0"


def show():
    """打开木子绑定工具箱。"""
    from .app import toolbox

    return toolbox.main()


def initialize():
    """启动工具箱。"""
    return show()
