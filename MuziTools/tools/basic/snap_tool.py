# coding=utf-8
u"""
快速吸附工具
============

选择规则：
    1. 前面的选择对象作为吸附参考。
    2. 最后一个选择对象作为需要移动的对象。
    3. 目标会吸附到前面所有参考对象的平均位置和平均旋转。

支持 Transform，也保留 core.snapUtils 对组件选择的兼容能力。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import snapUtils


def main():
    """执行一次快速 Position + Rotation 吸附。"""

    selected_items = cmds.ls(
        selection=True,
        flatten=True
    )

    if selected_items is None:
        selected_items = []

    if len(selected_items) < 2:
        cmds.warning(u"请选择两个或以上的物体或者 CV 点。")
        return False

    snapUtils.Snap.push_snip()
    return True


if __name__ == "__main__":
    main()
