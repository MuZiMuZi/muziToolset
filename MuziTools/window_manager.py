# coding=utf-8
u"""
MuziTools Window Manager
========================

统一管理从 Rigging Toolbox 打开的 PySide 窗口。

主要解决 Maya 中 PySide 子工具窗口的几个常见问题：
    1. 子窗口失去焦点后消失或跑到 Maya 主窗口后面；
    2. Qt.Tool / Qt.Popup 类型窗口不能正常最小化；
    3. Python 局部变量释放后窗口被垃圾回收；
    4. 旧工具 main() 自己 show()、但没有 return QWidget；
    5. 重复点击工具时创建多个相同窗口。

设计原则：
    - 子工具仍然以 Maya MainWindow 作为 owner；
    - 但窗口类型强制转换成真正的 Qt.Window，而不是 Qt.Tool；
    - Window Manager 保存强引用，避免窗口被 Python 回收；
    - 对没有返回 QWidget 的旧工具，自动查找本次新创建的顶层窗口。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QWidget
    try:
        from shiboken2 import isValid, wrapInstance
    except ImportError:
        isValid = None
        wrapInstance = None
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication, QWidget
    try:
        from shiboken6 import isValid, wrapInstance
    except ImportError:
        isValid = None
        wrapInstance = None

try:
    import maya.OpenMayaUI as omui
except ImportError:
    omui = None


# -----------------------------------------------------------------------------
# 全局窗口引用
# -----------------------------------------------------------------------------
# Maya 中 PySide 顶层窗口必须保存 Python 强引用。
# 否则创建函数退出以后，窗口可能被垃圾回收，表现为刚打开不久就消失。
# -----------------------------------------------------------------------------
_OPEN_WINDOWS = {}


# -----------------------------------------------------------------------------
# 基础工具函数
# -----------------------------------------------------------------------------
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


def _get_maya_main_window():
    """获取 Maya MainWindow 的 QWidget 包装对象。"""
    if omui is None or wrapInstance is None:
        return None

    try:
        ptr = omui.MQtUtil.mainWindow()
    except Exception:
        ptr = None

    if ptr is None:
        return None

    try:
        return wrapInstance(int(ptr), QWidget)
    except Exception:
        return None


def _remove_window(tool_key, window=None):
    """
    从窗口缓存中删除已经销毁的窗口。

    window 参数用于避免旧窗口延迟发出 destroyed 时，把后来新建的同名窗口
    一起从 _OPEN_WINDOWS 中误删。
    """
    current_window = _OPEN_WINDOWS.get(tool_key)

    if window is not None and current_window is not window:
        return

    _OPEN_WINDOWS.pop(tool_key, None)


def _window_identity_set():
    """返回 QApplication 当前所有有效顶层窗口的 id 集合。"""
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


def _is_candidate_window(widget, before_ids):
    """判断 widget 是否是 tool_function() 本次新建的顶层窗口。"""
    if not _is_valid_widget(widget):
        return False

    if id(widget) in before_ids:
        return False

    try:
        if not widget.isWindow():
            return False
    except Exception:
        return False

    # ToolTip 是 Qt 自己创建的临时顶层窗口，不能当作工具窗口接管。
    try:
        window_type = widget.windowType()
        if window_type == Qt.ToolTip:
            return False
    except Exception:
        pass

    return True


def _find_new_top_level_window(before_ids):
    """
    查找 tool_function() 执行后新出现的顶层 QWidget。

    用于兼容旧工具：
        def main():
            window = SomeUI()
            window.show()
            # 没有 return window

    这种代码以前 window_manager 得到的是 None，因此无法保存强引用。
    """
    app = QApplication.instance()
    if app is None:
        return None

    try:
        widgets = app.topLevelWidgets()
    except Exception:
        return None

    candidates = []

    for widget in widgets:
        if _is_candidate_window(widget, before_ids):
            candidates.append(widget)

    if not candidates:
        return None

    # 优先选择当前 activeWindow，因为通常它就是刚刚 show() 出来的工具。
    try:
        active_window = app.activeWindow()
    except Exception:
        active_window = None

    if active_window in candidates:
        return active_window

    # 其次选择当前可见的窗口。
    for widget in candidates:
        try:
            if widget.isVisible():
                return widget
        except Exception:
            pass

    return candidates[0]


def _extract_window(result, before_ids):
    """从工具返回值或新创建顶层窗口中取得需要管理的 QWidget。"""
    if _is_valid_widget(result):
        return result

    # 某些旧代码会返回 list / tuple，把窗口包在里面。
    if isinstance(result, (list, tuple)):
        for item in result:
            if _is_valid_widget(item):
                return item

    return _find_new_top_level_window(before_ids)


# -----------------------------------------------------------------------------
# Window flags
# -----------------------------------------------------------------------------
def _normal_window_flags(window):
    """
    返回适合 Maya 子工具的普通顶层窗口 flags。

    Qt.WindowType 使用同一组低位 bit 表示 Window / Dialog / Tool / Popup 等
    窗口类型。因此不能只写::

        window.windowFlags() | Qt.Window

    那样可能继续残留 Qt.Tool / Qt.Popup 的窗口类型行为。
    正确做法是先清除 WindowType_Mask，再明确设置 Qt.Window。
    """
    flags = window.windowFlags()

    try:
        flags = flags & ~Qt.WindowType_Mask
    except Exception:
        # 兼容极少数 Qt 绑定版本。
        for flag_name in [
            "Tool",
            "Popup",
            "SplashScreen",
            "Drawer",
            "Sheet",
        ]:
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

    # 清除容易造成 Maya 子工具体验异常的特殊 hints。
    for flag_name in [
        "WindowStaysOnTopHint",
        "WindowStaysOnBottomHint",
        "FramelessWindowHint",
        "BypassWindowManagerHint",
        "X11BypassWindowManagerHint",
    ]:
        try:
            flag_value = getattr(Qt, flag_name)
            flags = flags & ~flag_value
        except Exception:
            pass

    return flags


def _prepare_window(window):
    """
    把子工具规范成 Maya 拥有的普通 Qt.Window。

    这里故意不再使用 setParent(None)。

    parent=None 虽然可以把 Qt.Tool 转换成独立窗口，但当用户点击 Maya 主窗口时，
    独立窗口很容易掉到 Maya 后面，看起来仍然像“失焦后消失”。

    正确策略是：
        Maya MainWindow 作为 owner + Qt.Window 作为窗口类型。

    这样窗口仍属于 Maya，不会轻易跑到 Maya 后面，同时具备普通窗口的标题栏、
    最小化按钮和正常焦点行为。
    """
    if not _is_valid_widget(window):
        return

    try:
        window.setWindowModality(Qt.NonModal)
    except Exception:
        pass

    flags = _normal_window_flags(window)
    maya_main_window = _get_maya_main_window()

    if _is_valid_widget(maya_main_window) and window is not maya_main_window:
        try:
            window.setParent(maya_main_window, flags)
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

    # Window Manager 自己负责窗口生命周期。
    # 禁止“关闭即销毁”可以避免部分旧工具在 Maya 焦点切换、父窗口变化时被删除。
    try:
        window.setAttribute(Qt.WA_DeleteOnClose, False)
    except Exception:
        pass

    # 子工具关闭不应该影响 Maya QApplication。
    try:
        window.setAttribute(Qt.WA_QuitOnClose, False)
    except Exception:
        pass


def _show_and_activate(window):
    """显示窗口，并尽量恢复到可见、可交互状态。"""
    if not _is_valid_widget(window):
        return

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


# -----------------------------------------------------------------------------
# 对外接口
# -----------------------------------------------------------------------------
def show_tool(tool_key, tool_function):
    """
    显示一个工具窗口。

    流程：
        1. 已存在 -> 恢复已有窗口；
        2. 记录调用前的 QApplication 顶层窗口；
        3. 执行工具 main()；
        4. main() 返回 QWidget -> 直接接管；
        5. main() 返回 None -> 自动查找本次新建的顶层 QWidget；
        6. 统一设置 Maya owner / Qt.Window flags；
        7. 保存 Python 强引用。
    """
    old_window = _OPEN_WINDOWS.get(tool_key)

    if _is_valid_widget(old_window):
        _prepare_window(old_window)
        _show_and_activate(old_window)
        return old_window

    _OPEN_WINDOWS.pop(tool_key, None)

    before_ids = _window_identity_set()
    result = tool_function()
    window = _extract_window(result, before_ids)

    # 不是 PySide 窗口的工具，例如只执行 Maya cmds 的命令，保持原返回值。
    if not _is_valid_widget(window):
        return result

    _prepare_window(window)

    # 一定先保存强引用，再执行 show()。
    _OPEN_WINDOWS[tool_key] = window

    try:
        window.destroyed.connect(
            lambda *args, key=tool_key, obj=window: _remove_window(key, obj)
        )
    except Exception:
        pass

    _show_and_activate(window)

    return window


def close_tool(tool_key):
    """关闭指定工具窗口。"""
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
