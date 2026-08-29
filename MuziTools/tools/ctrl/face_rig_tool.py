# coding=utf-8
u"""
Face Rig Tool Compatibility Launcher
====================================

这个文件历史上位于 ``tools/ctrl``，但它实际应该启动项目的 Face Rig Wizard。
旧版内容只是一个“获取当前选择”的示例面板，与文件名和工具入口都不一致。

现在保留此路径作为兼容入口，真正的 Face Rig UI 统一维护在 ``face.face_rig_ui``。
"""

from __future__ import print_function

from importlib import reload

from ....face import face_rig_ui


_window = None


def main():
    """显示 Face Rig Wizard。"""
    global _window

    reload(face_rig_ui)

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = face_rig_ui.main()

    if _window is not None:
        try:
            _window.raise_()
            _window.activateWindow()
        except Exception:
            pass

    return _window


if __name__ == "__main__":
    main()
