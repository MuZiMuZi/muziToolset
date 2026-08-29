# coding=utf-8
u"""
MuziTools Window Manager
========================

统一管理从 Rigging Toolbox 打开的 PySide 窗口。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QWidget
    try:
        from shiboken2 import isValid
    except ImportError:
        isValid = None
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QWidget
    try:
        from shiboken6 import isValid
    except ImportError:
        isValid = None


_OPEN_WINDOWS = {}


def _is_valid_widget(widget):
    if widget is None:
        return False

    if not isinstance(widget, QWidget):
        return False

    if isValid is None:
        return True

    try:
        return bool(isValid(widget))
    except Exception:
        return False


def _remove_window(tool_key):
    _OPEN_WINDOWS.pop(tool_key, None)


def _prepare_window(window):
    try:
        window.setWindowModality(Qt.NonModal)
    except Exception:
        pass

    try:
        flags = window.windowFlags()
        flags = flags | Qt.Window
        flags = flags | Qt.WindowMinimizeButtonHint
        flags = flags | Qt.WindowCloseButtonHint
        window.setWindowFlags(flags)
    except Exception:
        pass


def show_tool(tool_key, tool_function):
    old_window = _OPEN_WINDOWS.get(tool_key)

    if _is_valid_widget(old_window):
        try:
            if old_window.isMinimized():
                old_window.showNormal()
            else:
                old_window.show()

            old_window.raise_()
            old_window.activateWindow()
            return old_window

        except Exception:
            _OPEN_WINDOWS.pop(tool_key, None)

    result = tool_function()

    if not isinstance(result, QWidget):
        return result

    window = result

    _prepare_window(window)

    _OPEN_WINDOWS[tool_key] = window

    try:
        window.destroyed.connect(
            lambda *args, key=tool_key: _remove_window(key)
        )
    except Exception:
        pass

    try:
        window.show()
        window.raise_()
        window.activateWindow()
    except Exception:
        pass

    return window


def close_tool(tool_key):
    window = _OPEN_WINDOWS.get(tool_key)

    if not _is_valid_widget(window):
        _OPEN_WINDOWS.pop(tool_key, None)
        return

    try:
        window.close()
    finally:
        _OPEN_WINDOWS.pop(tool_key, None)


def close_all_tools():
    tool_keys = list(_OPEN_WINDOWS.keys())

    for tool_key in tool_keys:
        close_tool(tool_key)


def get_open_windows():
    result = {}

    for tool_key, window in _OPEN_WINDOWS.items():
        if _is_valid_widget(window):
            result[tool_key] = window

    return result
