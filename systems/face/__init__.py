# coding=utf-8
u"""
Muzi Toolset 新版 Face System。

当前目录从 2026-09-07 开始按新的工程结构重新开发。
旧版 Face System 已完整存档到 legacy_reference，新的运行时代码不依赖旧版实现。
"""


def show():
    u"""从原 Face Rig 工具入口打开当前模块化绑定库。"""
    from ..rig import create_ui

    return create_ui()
