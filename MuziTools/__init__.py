# coding=utf-8
u"""
MuziTools
=========

统一的 Maya Rigging 工具入口。
"""


def show():
    """
    打开木子绑定工具盒。

    rigging_toolbox 在真正需要显示 UI 时才导入，
    避免普通 import muziToolset 时提前加载 Maya UI 模块。
    """
    from . import rigging_toolbox

    return rigging_toolbox.main()


def initialize():
    """
    兼容旧调用方式。
    """
    return show()