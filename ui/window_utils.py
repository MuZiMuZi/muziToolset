# coding=utf-8
u"""
Window Utils
============

Maya 中独立 Tool 窗口的最小生命周期辅助模块。

模块职责
--------
本模块只解决一个非常具体的问题：

    ``window = tool_module.main()``

在 Maya Script Editor 中直接执行时，Tool 必须立即显示，并且不能因为 Python 局部引用结束而被垃圾回收。

公开方法
--------
show_window(window_key, window_factory)
    创建或恢复一个独立 Tool QWidget，保存强引用，显示、Raise、Activate，并返回 QWidget。

close_window(window_key)
    关闭并释放一个独立 Tool 窗口。

get_window(window_key)
    返回当前缓存且仍有效的 QWidget；不存在或已经被销毁时返回 None。

clear_invalid_windows()
    清理缓存中已经失效的 Qt 对象。

和 app.window_manager 的区别
----------------------------
``ui.window_utils``：
    服务于用户直接在 Maya Script Editor 调用某个 Tool 的 ``main()``。

``app.window_manager``：
    服务于 MuziTools 主工具箱，额外负责 Maya Main Window Parent、Window Flags、统一 Theme、
    跨 Tool 单实例缓存等应用级行为。

两者不会互相替代：Tool 的 ``main()`` 可以先通过本模块确保直接调用可见；主工具箱拿到 QWidget 后，
仍然由 ``app.window_manager`` 做最终应用级整理。

设计原则
--------
1. 不 import 任何具体 Tool，避免 UI 层形成反向依赖；
2. 不创建 QApplication，Maya 自己已经拥有 QApplication；
3. 不修改 Window Flags / Maya Parent，这些属于 app.window_manager；
4. 同一个 window_key 默认只保留一个有效实例；
5. 关闭后允许下一次 main() 创建新窗口；
6. PySide2 / PySide6 都支持。
"""

from __future__ import print_function

try:
    from PySide2.QtWidgets import QWidget
    from shiboken2 import isValid
except ImportError:
    from PySide6.QtWidgets import QWidget
    from shiboken6 import isValid


# =============================================================================
# Window Cache
# =============================================================================
#
# 这是模块级强引用缓存。
# 如果 QWidget 只保存在某个 main() 的局部变量中，函数结束后 Python 可能回收包装对象，
# Maya 中就会表现为“窗口没有显示”或“刚显示就消失”。
# =============================================================================
_windows = {}


def _is_valid_widget(window):
    """判断对象是否是仍然有效的 QWidget。"""
    if window is None:
        return False

    if not isinstance(window, QWidget):
        return False

    try:
        return bool(isValid(window))
    except Exception:
        return False


def clear_invalid_windows():
    u"""

        清理缓存里已经被 Qt / Maya 销毁的 QWidget。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    invalid_keys = []

    for window_key in _windows:
        window = _windows[window_key]

        if not _is_valid_widget(window):
            invalid_keys.append(window_key)

    for window_key in invalid_keys:
        _windows.pop(window_key, None)

    return len(invalid_keys)


def get_window(window_key):
    u"""

        返回当前有效窗口；不存在时返回 None。

        Args:
            window_key (object):
                当前方法执行 Maya / Rig 操作时使用的 `window_key` 数据。

        Returns:
            object | None:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    window = _windows.get(window_key)

    if not _is_valid_widget(window):
        _windows.pop(window_key, None)
        return None

    return window


def _show_and_activate(window):
    """显示、恢复并激活 QWidget。"""
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not _is_valid_widget(window):
        return None

    # -------------------------------------------------------------------------
    # 步骤 1：如果用户之前把窗口最小化，优先恢复正常状态。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 02：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        minimized = window.isMinimized()
    except Exception:
        minimized = False

    if minimized:
        try:
            window.showNormal()
        except Exception:
            window.show()
    else:
        window.show()

    # -------------------------------------------------------------------------
    # 步骤 2：Raise / Activate 让窗口从 Maya 后面回到用户当前视线。
    # -------------------------------------------------------------------------
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
    return window


def _connect_destroyed(window_key, window):
    """Qt 对象真正销毁后，从强引用缓存移除。"""

    def on_destroyed(*args):
        current = _windows.get(window_key)

        if current is window:
            _windows.pop(window_key, None)

    try:
        window.destroyed.connect(on_destroyed)
    except Exception:
        pass


def show_window(window_key, window_factory):
    u"""
    创建或恢复一个独立 Tool 窗口。

    Args:
        window_key (str):
            稳定的窗口唯一 Key，例如 ``tools.controller.control_shape_tool``。
        window_factory (callable):
            无参数调用后返回 QWidget 的 Factory，通常直接传 Tool Window Class。

    Returns:
        QWidget: 当前显示中的窗口。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
        TypeError:
        输入数据、场景状态或操作条件不满足要求时抛出。

    Example:
        def main():
                                                                        return window_utils.show_window(
                                                                            "tools.basic.rename_tool",
                                                                            RenameTool
                                                                        )
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not window_key:
        raise ValueError(u"window_key 不能为空。")

    if not callable(window_factory):
        raise TypeError(u"window_factory 必须是可调用对象。")

    # -------------------------------------------------------------------------
    # 步骤 1：先清理已经失效的缓存，避免拿到 Qt C++ 已销毁的 Python Wrapper。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 02：清理当前阶段不再需要的数据或场景状态
    # -------------------------------------------------------------------------
    clear_invalid_windows()

    # -------------------------------------------------------------------------
    # 步骤 2：已经有有效实例时直接恢复，而不是重复创建窗口。
    # -------------------------------------------------------------------------
    window = get_window(window_key)

    if window is not None:
        return _show_and_activate(window)

    # -------------------------------------------------------------------------
    # 步骤 3：创建新窗口，并验证 Factory 确实返回 QWidget。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    window = window_factory()

    if not _is_valid_widget(window):
        raise TypeError(
            u"window_factory 没有返回有效 QWidget：{}".format(
                window_key
            )
        )

    # 必须在 show() 之前保存强引用，避免极端情况下对象提前失效。
    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    _windows[window_key] = window
    _connect_destroyed(
        window_key,
        window
    )

    # -------------------------------------------------------------------------
    # 步骤 4：显示并返回窗口，让 Script Editor 和 app.window_manager 都可以继续持有它。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return _show_and_activate(window)


def close_window(window_key):
    u"""

        关闭并释放指定独立 Tool 窗口。

        Args:
            window_key (object):
                当前方法执行 Maya / Rig 操作时使用的 `window_key` 数据。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。

    """
    window = _windows.pop(window_key, None)

    if not _is_valid_widget(window):
        return False

    try:
        window.close()
    except Exception:
        pass

    try:
        window.deleteLater()
    except Exception:
        pass

    return True


__all__ = [
    "show_window",
    "close_window",
    "get_window",
    "clear_invalid_windows",
]
