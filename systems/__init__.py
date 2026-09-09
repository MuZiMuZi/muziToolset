# coding=utf-8
u"""Muzi Toolset Rig System 集合。"""

def __getattr__(name):
    u"""按需加载绑定基类，让目录、配置和 Qt 预览可以在 Maya 外读取。"""
    if name == "RigModule":
        from .rig_module import RigModule

        return RigModule
    raise AttributeError(name)


__all__ = [
    "RigModule",
]
