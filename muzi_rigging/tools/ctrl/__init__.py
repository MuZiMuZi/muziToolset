# coding=utf-8
u"""
临时 Controller 包名迁移桥。

正式目录：
    muzi_rigging.tools.controller

旧模块仍有少量 ``from ..ctrl`` 引用。
这些文件迁移完成后删除本包。
"""

from .. import controller as _controller


__path__ = _controller.__path__
