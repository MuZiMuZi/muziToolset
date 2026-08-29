# coding=utf-8
u"""
Control Setter
==============

控制器 Shape 编辑入口。

实际 Shape 图库、颜色、缩放、旋转、镜像、替换、上传和删除逻辑统一维护在
``control_shape_tool`` 中，本文件只保留兼容入口，避免两份近乎相同的 UI 和
Shape 处理代码继续分叉。
"""

from PySide2.QtCore import Qt

from . import control_shape_tool


_window = None


class ControlSetterUI(control_shape_tool.ControlShapeTool):
    """兼容旧 ``ControlSetterUI`` 名称的控制器编辑窗口。"""

    def __init__(self, parent=None):
        super(ControlSetterUI, self).__init__(parent=parent)
        self.setWindowTitle(u"Control Setter")


def main():
    """显示控制器编辑工具。"""
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = ControlSetterUI()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window


if __name__ == "__main__":
    main()
