# coding=utf-8
u"""
Muzi Rigging Window Manager
===========================

统一管理主工具箱打开的 PySide 子工具窗口。

职责：
    1. 保存 Python 强引用，避免窗口被垃圾回收；
    2. 把 Qt.Tool / Qt.Dialog / Qt.Popup 整理成普通 Qt.Window；
    3. 使用 Maya 主窗口作为 owner；
    4. 同一个工具只保留一个窗口实例；
    5. 兼容 main() 已经 show() 但没有返回 QWidget 的旧工具；
    6. 避免重复 setParent / setWindowFlags 导致 native window 重建；
    7. 统一应用当前 Muzi Rigging UI Theme。
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

from ..ui import theme


_open_windows = {}
_prepared_property = "muzi_window_manager_prepared"
_theme_property = "muzi_window_theme_applied"


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
    """从窗口缓存中移除指定工具。"""
    current_window = _open_windows.get(tool_key)

    if window is not None:
        if current_window is not window:
            return

    _open_windows.pop(tool_key, None)


def _top_level_window_ids():
    """返回当前 QApplication 顶层 QWidget 的 id 集合。"""
    result = set()
    application = QApplication.instance()

    if application is None:
        return result

    try:
        widgets = application.topLevelWidgets()
    except Exception:
        return result

    for widget in widgets:
        if _is_valid_widget(widget):
            result.add(id(widget))

    return result


def _is_new_tool_window(widget, before_ids):
    """判断 QWidget 是否是本次工具调用新创建的顶层窗口。"""
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not _is_valid_widget(widget):
        return False

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if id(widget) in before_ids:
        return False

    # -------------------------------------------------------------------------
    # Step 03：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        if not widget.isWindow():
            return False
    except Exception:
        return False

    # -------------------------------------------------------------------------
    # Step 04：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        if widget.windowType() == Qt.ToolTip:
            return False
    except Exception:
        pass

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return True


def _find_new_top_level_window(before_ids):
    """兼容没有 return QWidget 的工具 main()。"""
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    application = QApplication.instance()

    if application is None:
        return None

    # -------------------------------------------------------------------------
    # Step 02：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        widgets = application.topLevelWidgets()
    except Exception:
        return None

    candidates = []

    for widget in widgets:
        if _is_new_tool_window(widget, before_ids):
            candidates.append(widget)

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not candidates:
        return None

    try:
        active_window = application.activeWindow()
    except Exception:
        active_window = None

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if active_window in candidates:
        return active_window

    for widget in candidates:
        try:
            if widget.isVisible():
                return widget
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return candidates[0]


def _extract_window(result, before_ids):
    """从工具返回值中寻找 QWidget。"""
    if _is_valid_widget(result):
        return result

    if isinstance(result, (list, tuple)):
        for item in result:
            if _is_valid_widget(item):
                return item

    return _find_new_top_level_window(before_ids)


def _normal_window_flags(window):
    """构建 Maya 子工具需要的普通 Window flags。"""
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    flags = window.windowFlags()

    try:
        flags = flags & ~Qt.WindowType_Mask
    except Exception:
        window_type_names = [
            "Tool",
            "Popup",
            "Dialog",
            "Sheet",
            "Drawer",
            "SplashScreen",
        ]

        for flag_name in window_type_names:
            try:
                flag_value = getattr(Qt, flag_name)
                flags = flags & ~flag_value
            except Exception:
                pass

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    flags = flags | Qt.Window
    flags = flags | Qt.WindowTitleHint
    flags = flags | Qt.WindowSystemMenuHint
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    flags = flags | Qt.WindowMinimizeButtonHint
    flags = flags | Qt.WindowCloseButtonHint

    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    unwanted_hint_names = [
        "WindowStaysOnTopHint",
        "WindowStaysOnBottomHint",
        "FramelessWindowHint",
        "WindowContextHelpButtonHint",
        "BypassWindowManagerHint",
        "X11BypassWindowManagerHint",
    ]

    for flag_name in unwanted_hint_names:
        try:
            flag_value = getattr(Qt, flag_name)
            flags = flags & ~flag_value
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return flags


def _already_prepared(window):
    """检查窗口是否已经完成 parent / flags 整理。"""
    try:
        return bool(window.property(_prepared_property))
    except Exception:
        return False


def _mark_prepared(window):
    """标记窗口已经完成结构整理。"""
    try:
        window.setProperty(_prepared_property, True)
    except Exception:
        pass


def _theme_already_applied(window):
    """检查窗口是否已经应用统一主题。"""
    try:
        return bool(window.property(_theme_property))
    except Exception:
        return False


def _apply_window_theme(window):
    """给子工具窗口应用统一主题。"""
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not _is_valid_widget(window):
        return False

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if _theme_already_applied(window):
        return True

    try:
        theme.apply_theme(window)
    except Exception as error:
        print(
            u"[muzi_rigging] 应用 UI Theme 失败: {}".format(error)
        )
        return False

    # -------------------------------------------------------------------------
    # Step 03：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        window.setAttribute(Qt.WA_StyledBackground, True)
    except Exception:
        pass

    # -------------------------------------------------------------------------
    # Step 04：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        window.setProperty(_theme_property, True)
    except Exception:
        pass

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return True


def _prepare_window(window):
    """
    将窗口整理成 Maya 拥有的普通非模态 Qt.Window。

    parent / windowFlags 只在每个 QWidget 第一次显示时整理一次，避免 Qt
    重建 native window 后造成闪烁、隐藏或最小化状态异常。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not _is_valid_widget(window):
        return False

    if _already_prepared(window):
        return True

    # -------------------------------------------------------------------------
    # Step 02：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        window.setWindowModality(Qt.NonModal)
    except Exception:
        pass

    flags = _normal_window_flags(window)
    maya_main_window = _get_maya_main_window()

    # -------------------------------------------------------------------------
    # Step 03：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 04：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        window.setAttribute(Qt.WA_QuitOnClose, False)
    except Exception:
        pass

    _mark_prepared(window)
    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return True


def _show_and_activate(window):
    """恢复、显示并激活窗口。"""
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not _is_valid_widget(window):
        return False

    # -------------------------------------------------------------------------
    # Step 02：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 03：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        window.raise_()
    except Exception:
        pass

    # -------------------------------------------------------------------------
    # Step 04：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        window.activateWindow()
    except Exception:
        pass

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return True


def _connect_destroyed_signal(tool_key, window):
    """连接窗口 destroyed 信号，并清理窗口缓存。"""

    def on_window_destroyed(*args):
        _remove_window(
            tool_key,
            window
        )

    try:
        window.destroyed.connect(on_window_destroyed)
    except Exception:
        pass


def show_tool(tool_key, tool_function):
    u"""

        显示新工具，或恢复已经打开的工具窗口。

        Args:
            tool_key (str):
                Tool Registry / Window Manager 中唯一识别工具的 Key。
            tool_function (callable):
                执行当前工具功能的 Callable。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    old_window = _open_windows.get(tool_key)

    if _is_valid_widget(old_window):
        _prepare_window(old_window)
        _apply_window_theme(old_window)
        _show_and_activate(old_window)
        return old_window

    _open_windows.pop(tool_key, None)

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    before_ids = _top_level_window_ids()
    result = tool_function()
    window = _extract_window(result, before_ids)

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not _is_valid_widget(window):
        return result

    _prepare_window(window)
    _apply_window_theme(window)

    # 必须先保存强引用，再调用 show()。
    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    _open_windows[tool_key] = window

    _connect_destroyed_signal(
        tool_key,
        window
    )

    _show_and_activate(window)
    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return window


def close_tool(tool_key):
    u"""
    关闭并释放一个受管理的工具窗口。

    Args:
        tool_key (str):
            Tool Registry / Window Manager 中唯一识别工具的 Key。
    """
    window = _open_windows.pop(tool_key, None)

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
    u"""
    关闭全部受管理的工具窗口。
    """
    tool_keys = []

    for tool_key in _open_windows:
        tool_keys.append(tool_key)

    for tool_key in tool_keys:
        close_tool(tool_key)


def get_open_windows():
    u"""

        返回当前有效工具窗口字典的浅拷贝。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    result = {}
    invalid_keys = []

    for tool_key in _open_windows:
        window = _open_windows[tool_key]

        if _is_valid_widget(window):
            result[tool_key] = window
        else:
            invalid_keys.append(tool_key)

    for tool_key in invalid_keys:
        _open_windows.pop(tool_key, None)

    return result
