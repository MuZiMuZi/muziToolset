# coding=utf-8
u"""
Face Rig Tool
=============

MuziTools 面部绑定系统入口。

真正的分步 Face Rig UI 维护在项目 ``face.face_rig_ui`` 中；这里负责把它注册到
MuziTools 的“面部工具”分类。
"""

from __future__ import print_function

from importlib import reload

from ....face import face_rig_ui


def main():
    """创建并返回 Face Rig Wizard。"""
    reload(face_rig_ui)
    window = face_rig_ui.main()
    return window


if __name__ == "__main__":
    window = main()

    if window is not None:
        window.show()
