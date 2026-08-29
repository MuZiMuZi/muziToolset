# coding=utf-8
u"""
Face Rig Tool
=============

面部工具分类中的 Face Rig 系统启动入口。
工具层只调用 Face System 公共 API，不依赖具体 Wizard 文件。
"""

from __future__ import print_function

from ...systems import face as face_system


def main():
    """创建并返回 Face Rig Wizard。"""
    return face_system.show()


if __name__ == "__main__":
    window = main()

    if window is not None:
        window.show()
