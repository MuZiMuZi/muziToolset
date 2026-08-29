# coding=utf-8
u"""
Face Rig Tool
=============

面部工具分类中的 Face Rig 系统启动入口。
完整 Face Rig 实现维护在 ``muzi_rigging.systems.face``。
"""

from __future__ import print_function

from ...systems.face import face_rig_ui


def main():
    """创建并返回 Face Rig Wizard。"""
    window = face_rig_ui.main()
    return window


if __name__ == "__main__":
    window = main()

    if window is not None:
        window.show()
