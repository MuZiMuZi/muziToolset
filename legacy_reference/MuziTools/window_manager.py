# coding=utf-8
u"""
MuziTools Window Manager
========================

统一管理 Rigging Toolbox 打开的 PySide 子工具窗口。

主要目标：
    1. 保存 Python 强引用，避免窗口被垃圾回收；
    2. 把 Qt.Tool / Qt.Dialog / Qt.Popup 统一成可正常最小化的 Qt.Window；
    3. Maya 主窗口作为 owner，减少工具失焦后掉到 Maya 后面的情况；
    4. 同一个工具只保留一个窗口实例；
    5. 兼容 main() 已经 show() 但没有 return QWidget 的旧式工具；
    6. 不重复 re-parent 已经整理过的窗口，避免 Qt 重建 native window 时闪烁或隐藏；
    7. 所有 PySide 子工具自动使用统一的 Muzi Silicon UI Theme。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication
    from PySide2.QtWidgets import QWidget
    from shiboken2 import isValid
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication
    from PySide6.QtWidgets import QWidget
    from shiboken6 import isValid
    from shiboken6 import wrapInstance

try:
    import maya.OpenMayaUI as omui
except ImportError:
    omui = None

from . import ui_theme


_OPEN_WINDOWS = {}
_PREPARED_PROPERTY = "muzi_window_manager_prepared"
_THEME_PROPERTY = "muzi_window_theme_applied"


def _is_valid_widget(widget):
    """判断对象是否仍是有效 QWidget。"""
    if widget is None:
        return False

    if not isinstance(widget, QWidget):
        return False

    try:
        return bool(isValid(widget))
    except Exception:
        return False


def _get_maya_main_window():
    """返回 Maya 主窗口 QWidget。"""
    if omui is None:
        return None

    try:
        pointer = omui.MQtUtil.mainWindow()
    except Exception:
        pointer = None

    if pointer is None:
        return None

    try:
        return wrapInstance(int(pointer), QWidget)
    except Exception:
        return None


def _remove_window(tool_key, window=None):
    """从缓存中移除指定窗口。"""
    current_window = _OPEN_WINDOWS.get(tool_key)

    if window is not None:
        if current_window is not window:
            return

    _OPEN_WINDOWS.pop(tool_key, None)


def _top_level_window_ids():
    """返回当前 QApplication 顶层 QWidget 的 id 集合。"""
    result = set()
    app = QApplication.instance()

    if app is None:
        return result

    try:
        widgets = app.topLevelWidgets()
    except Exception:
        return result

    for widget in widgets:
        if _is_valid_widget(widget):
            result.add(id(widget))

    return result


def _is_new_tool_window(widget, before_ids):
    """判断 QWidget 是否是本次工具调用新创建的顶层窗口。"""
    if not _is_valid_widget(widget):
        return False

    if id(widget) in before_ids:
        return False

    try:
        if not widget.isWindow():
            return False
    except Exception:
        return False

    try:
        if widget.windowType() == Qt.ToolTip:
            return False
    except Exception:
        pass

    return True


def _find_new_top_level_window(before_ids):
    """兼容没有 return QWidget 的工具 main()。"""
    app = QApplication.instance()

    if app is None:
        return None

    try:
        widgets = app.topLevelWidgets()
    except Exception:
        return None

    candidates = []

    for widget in widgets:
        if _is_new_tool_window(widget, before_ids):
            candidates.append(widget)

    if not candidates:
        return None

    try:
        active_window = app.activeWindow()
    except Exception:
        active_window = None

    if active_window in candidates:
        return active_window

    for widget in candidates:
        try:
            if widget.isVisible():
                return widget
        except Exception:
            pass

    return candidates[0]


def _extract_window(result, before_ids):
    """从 main() 返回值中寻找 QWidget。"""
    if _is_valid_widget(result):
        return result

    if isinstance(result, (list, tuple)):
        for item in result:
            if _is_valid_widget(item):
                return item

    return _find_new_top_level_window(before_ids)


def _normal_window_flags(window):
    """构建 Maya 子工具使用的普通 Window flags。"""
    flags = window.windowFlags()

    try:
        flags = flags & ~Qt.WindowType_Mask
    except Exception:
        window_type_flags = [
            "Tool",
            "Popup",
            "Dialog",
            "Sheet",
            "Drawer",
            "SplashScreen",
        ]

        for flag_name in window_type_flags:
            try:
                flag_value = getattr(Qt, flag_name)
                flags = flags & ~flag_value
            except Exception:
                pass

    flags = flags | Qt.Window
    flags = flags | Qt.WindowTitleHint
    flags = flags | Qt.WindowSystemMenuHint
    flags = flags | Qt.WindowMinimizeButtonHint
    flags = flags | Qt.WindowCloseButtonHint

    unwanted_hints = [
        "WindowStaysOnTopHint",
        "WindowStaysOnBottomHint",
        "FramelessWindowHint",
        "WindowContextHelpButtonHint",
        "BypassWindowManagerHint",
        "X11BypassWindowManagerHint",
    ]

    for flag_name in unwanted_hints:
        try:
            flag_value = getattr(Qt, flag_name)
            flags = flags & ~flag_value
        except Exception:
            pass

    return flags


def _already_prepared(window):
    """检查窗口是否已经由 Window Manager 整理过。"""
    try:
        return bool(window.property(_PREPARED_PROPERTY))
    except Exception:
        return False


def _mark_prepared(window):
    """标记窗口已经完成 parent / flags 整理。"""
    try:
        window.setProperty(_PREPARED_PROPERTY, True)
    except Exception:
        pass


def _theme_already_applied(window):
    """检查当前窗口是否已经应用 Muzi Theme。"""
    try:
        return bool(window.property(_THEME_PROPERTY))
    except Exception:
        return False


def _apply_window_theme(window):
    """
    给子工具应用统一 Muzi Silicon Theme。

    Theme 只在每个 QWidget 实例第一次显示时设置一次，避免重复点击工具时
    反复 setStyleSheet 导致整棵控件树重新 polish。
    """
    if not _is_valid_widget(window):
        return False

    if _theme_already_applied(window):
        return True

    try:
        ui_theme.apply_theme(window)
    except Exception as error:
        print(
            u"[MuziTools] 应用 UI Theme 失败: {}".format(error)
        )
        return False

    try:
        window.setAttribute(Qt.WA_StyledBackground, True)
    except Exception:
        pass

    try:
        window.setProperty(_THEME_PROPERTY, True)
    except Exception:
        pass

    return True


def _prepare_window(window):
    """
    将窗口整理成 Maya 拥有的普通非模态 Qt.Window。

    Qt 在修改 parent / windowFlags 时可能销毁并重新创建 native window。
    因此每个 QWidget 只做一次结构性整理；重复点击工具时只恢复窗口，不再次
    re-parent。
    """
    if not _is_valid_widget(window):
        return False

    if _already_prepared(window):
        return True

    try:
        window.setWindowModality(Qt.NonModal)
    except Exception:
        pass

    flags = _normal_window_flags(window)
    maya_main_window = _get_maya_main_window()

    try:
        current_parent = window.parentWidget()
    except Exception:
        current_parent = None

    if _is_valid_widget(maya_main_window):
        if window is not maya_main_window:
            try:
                if current_parent is not maya_main_window:
                    window.setParent(maya_main_window, flags)
                else:
                    window.setWindowFlags(flags)
            except Exception:
                try:
                    window.setWindowFlags(flags)
                except Exception:
                    pass
    else:
        try:
            window.setWindowFlags(flags)
        except Exception:
            pass

    try:
        window.setAttribute(Qt.WA_DeleteOnClose, False)
    except Exception:
        pass

    try:
        window.setAttribute(Qt.WA_QuitOnClose, False)
    except Exception:
        pass

    _mark_prepared(window)
    return True


def _show_and_activate(window):
    """恢复、显示并激活窗口。"""
    if not _is_valid_widget(window):
        return False

    try:
        minimized = window.isMinimized()
    except Exception:
        minimized = False

    try:
        if minimized:
            window.showNormal()
        else:
            window.show()
    except Exception:
        return False

    try:
        window.raise_()
    except Exception:
        pass

    try:
        window.activateWindow()
    except Exception:
        pass

    return True


def show_tool(tool_key, tool_function):
    """
    显示或恢复一个工具。

    对非 QWidget 工具（例如 Maya cmds.window 工具）直接返回原始结果，
    不强行纳入 PySide Window Manager。
    """
    old_window = _OPEN_WINDOWS.get(tool_key)

    if _is_valid_widget(old_window):
        _prepare_window(old_window)
        _apply_window_theme(old_window)
        _show_and_activate(old_window)
        return old_window

    _OPEN_WINDOWS.pop(tool_key, None)

    before_ids = _top_level_window_ids()
    result = tool_function()
    window = _extract_window(result, before_ids)

    if not _is_valid_widget(window):
        return result

    _prepare_window(window)
    _apply_window_theme(window)

    # show 之前先保存强引用。
    _OPEN_WINDOWS[tool_key] = window

    try:
        window.destroyed.connect(
            lambda *args, key=tool_key, obj=window: _remove_window(
                key,
                obj
            )
        )
    except Exception:
        pass

    _show_and_activate(window)
    return window


def close_tool(tool_key):
    """关闭并真正释放一个受管理工具窗口。"""
    window = _OPEN_WINDOWS.pop(tool_key, None)

    if not _is_valid_widget(window):
        return

    try:
        window.close()
    except Exception:
        pass

    try:
        window.deleteLater()
    except Exception:
        pass


def close_all_tools():
    """关闭全部受管理的工具窗口。"""
    tool_keys = []

    for tool_key in _OPEN_WINDOWS:
        tool_keys.append(tool_key)

    for tool_key in tool_keys:
        close_tool(tool_key)


def get_open_windows():
    """返回当前有效窗口字典的浅拷贝。"""
    result = {}
    invalid_keys = []

    for tool_key in _OPEN_WINDOWS:
        window = _OPEN_WINDOWS[tool_key]

        if _is_valid_widget(window):
            result[tool_key] = window
        else:
            invalid_keys.append(tool_key)

    for tool_key in invalid_keys:
        _OPEN_WINDOWS.pop(tool_key, None)

    return result
