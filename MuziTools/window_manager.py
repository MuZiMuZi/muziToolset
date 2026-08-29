# coding=utf-8
u"""
MuziTools Window Manager
========================

统一管理从 Rigging Toolbox 打开的 PySide 窗口。

主要解决 Maya 中 PySide 子工具窗口的几个常见问题：
    1. 子窗口失去焦点后自动消失；
    2. Qt.Tool / Qt.Popup 类型窗口不能正常最小化；
    3. Python 局部变量释放后窗口被垃圾回收；
    4. 重复点击工具时创建多个相同窗口。
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


# -----------------------------------------------------------------------------
# 全局窗口引用
# -----------------------------------------------------------------------------
#
# Maya 中如果 PySide 窗口只保存在函数局部变量里，函数结束后 Python 可能会
# 回收这个对象，最终表现为窗口突然消失。
#
# 因此这里始终保存强引用，直到窗口真正 destroyed。
# -----------------------------------------------------------------------------
_OPEN_WINDOWS = {}


def _is_valid_widget(widget):
    """判断 PySide QWidget 是否仍然有效。"""
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
    """从窗口缓存中删除已经销毁的窗口。"""
    _OPEN_WINDOWS.pop(tool_key, None)


def _normal_window_flags(window):
    """
    返回适合 Maya 子工具的普通顶层窗口 flags。

    重点：不能简单使用::

        flags = window.windowFlags() | Qt.Window

    因为 Qt.Tool、Qt.Popup、Qt.SplashScreen 等窗口类型位可能仍然保留。
    Qt 的窗口类型位于 WindowType_Mask 中，所以必须先清除旧窗口类型，
    再明确设置成 Qt.Window。
    """
    flags = window.windowFlags()

    try:
        flags = flags & ~Qt.WindowType_Mask
    except Exception:
        # 极少数 PySide 版本如果 WindowType_Mask 不可用，至少显式清除
        # Maya 工具窗口中最容易造成失焦隐藏的几种类型。
        try:
            flags = flags & ~Qt.Tool
        except Exception:
            pass

        try:
            flags = flags & ~Qt.Popup
        except Exception:
            pass

        try:
            flags = flags & ~Qt.SplashScreen
        except Exception:
            pass

    flags = flags | Qt.Window
    flags = flags | Qt.WindowTitleHint
    flags = flags | Qt.WindowSystemMenuHint
    flags = flags | Qt.WindowMinimizeButtonHint
    flags = flags | Qt.WindowCloseButtonHint

    # 不让子工具始终置顶。Qt.WindowStaysOnTopHint 在 Maya 中容易造成
    # 焦点切换体验异常。
    try:
        flags = flags & ~Qt.WindowStaysOnTopHint
    except Exception:
        pass

    return flags


def _prepare_window(window):
    """
    将工具窗口转换为真正的普通顶层窗口。

    Maya 工具经常使用 Qt.Tool 或带 Maya MainWindow 作为 parent。
    Qt.Tool 的特点就是依附于父窗口，并且在焦点/应用状态变化时可能隐藏，
    同时也不具备普通窗口完整的最小化行为。

    这里将窗口从这种“临时工具窗”状态转换为独立的 Qt.Window。
    """
    try:
        window.setWindowModality(Qt.NonModal)
    except Exception:
        pass

    flags = _normal_window_flags(window)

    # setParent(None, flags) 有两个作用：
    #   1. 清除 Maya 主窗口对这个工具窗的 owned/tool-window 关系；
    #   2. 一次性应用新的顶层窗口类型。
    #
    # 这样窗口失焦后不会因为 Qt.Tool 行为被隐藏，并且能够正常最小化。
    try:
        window.setParent(None, flags)
    except Exception:
        try:
            window.setWindowFlags(flags)
        except Exception:
            pass

    # 某些工具自己设置了“关闭即删除”。这没有问题，destroyed 信号会负责
    # 清理 _OPEN_WINDOWS；这里不强制修改 WA_DeleteOnClose。


def _show_and_activate(window):
    """显示窗口，并尽量恢复到可见、可交互状态。"""
    try:
        if window.isMinimized():
            window.showNormal()
        else:
            window.show()
    except Exception:
        return

    try:
        window.raise_()
    except Exception:
        pass

    try:
        window.activateWindow()
    except Exception:
        pass


def show_tool(tool_key, tool_function):
    """
    显示一个工具窗口。

    如果相同 tool_key 的窗口已经存在，则直接恢复并激活旧窗口；
    否则执行 tool_function() 创建新窗口。
    """
    old_window = _OPEN_WINDOWS.get(tool_key)

    if _is_valid_widget(old_window):
        _show_and_activate(old_window)
        return old_window

    _OPEN_WINDOWS.pop(tool_key, None)

    result = tool_function()

    # 一些非 PySide 工具可能没有返回 QWidget，保持原来的调用行为。
    if not isinstance(result, QWidget):
        return result

    window = result

    _prepare_window(window)

    # 必须先保存强引用，再 show。
    # 避免窗口显示后函数退出时被 Python 垃圾回收。
    _OPEN_WINDOWS[tool_key] = window

    try:
        window.destroyed.connect(
            lambda *args, key=tool_key: _remove_window(key)
        )
    except Exception:
        pass

    _show_and_activate(window)

    return window


def close_tool(tool_key):
    """关闭指定工具窗口。"""
    window = _OPEN_WINDOWS.get(tool_key)

    if not _is_valid_widget(window):
        _OPEN_WINDOWS.pop(tool_key, None)
        return

    try:
        window.close()
    finally:
        _OPEN_WINDOWS.pop(tool_key, None)


def close_all_tools():
    """关闭所有由 Window Manager 管理的工具窗口。"""
    tool_keys = list(_OPEN_WINDOWS.keys())

    for tool_key in tool_keys:
        close_tool(tool_key)


def get_open_windows():
    """返回当前仍然有效的工具窗口。"""
    result = {}

    invalid_keys = []

    for tool_key, window in _OPEN_WINDOWS.items():
        if _is_valid_widget(window):
            result[tool_key] = window
        else:
            invalid_keys.append(tool_key)

    for tool_key in invalid_keys:
        _OPEN_WINDOWS.pop(tool_key, None)

    return result
