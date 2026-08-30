# coding=utf-8
u"""
Face Rig Tool
=============

面部工具分类中的 Face Rig 系统启动入口。

职责：
    1. Tool 层只调用 Face System 公共 API；
    2. 不依赖具体 Wizard 文件路径；
    3. 用户直接调用 main() 时，由 ui.window_utils 负责窗口显示和强引用。
"""

from __future__ import print_function

from ...systems import face as face_system
from ...ui import window_utils


def main():
    """显示并返回 Face Rig Wizard。"""
    return window_utils.show_window(
        "tools.face.face_rig_tool",
        face_system.show
    )


if __name__ == "__main__":
    main()
