# coding=utf-8
u"""Legacy compatibility wrapper for the native Maya rename tool."""

from .tools.basic import rename_tool


def Names_Tool(*args, **kwargs):
    """兼容旧 ``Names_Tool()`` 调用，返回 Maya cmds.window 名称。"""
    return rename_tool.main()


def show():
    return rename_tool.main()


def main():
    return rename_tool.main()


__all__ = [
    "Names_Tool",
    "show",
    "main",
]
