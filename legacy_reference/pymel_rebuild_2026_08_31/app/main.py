# coding=utf-8
u"""Muzi Rigging 应用启动入口。"""

from __future__ import print_function

from . import toolbox


def main():
    u"""
    打开 Muzi Rigging 主工具箱。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return toolbox.main()


if __name__ == "__main__":
    main()
