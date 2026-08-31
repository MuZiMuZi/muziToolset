# coding=utf-8
u"""
Muzi Face Rig System
====================

Face Rig 是本次 PyMEL 架构重建后唯一继续保留的业务系统。

注意：
旧 Face 源码正在按新的 PyMEL-first 架构逐步迁移。
本 __init__ 不再 eager import 具体 Step / Builder，避免迁移期间旧依赖污染包导入。
"""

from __future__ import print_function


def show():
    u"""延迟打开 Face Rig Workflow UI。"""
    from . import ui
    return ui.show()


__all__ = [
    "show",
]
