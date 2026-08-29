# coding=utf-8
from __future__ import print_function

import os
import shutil

ROOT = os.path.abspath(os.path.dirname(__file__))
MUZI_DIR = os.path.join(ROOT, "MuziTools")
RIGGING_TOOLBOX = os.path.join(MUZI_DIR, "rigging_toolbox.py")
WINDOW_MANAGER = os.path.join(MUZI_DIR, "window_manager.py")

WINDOW_MANAGER_CONTENT = '# coding=utf-8\nu"""\nMuziTools Window Manager\n========================\n\n统一管理从 Rigging Toolbox 打开的 PySide 窗口。\n"""\n\nfrom __future__ import print_function\n\ntry:\n    from PySide2.QtCore import Qt\n    from PySide2.QtWidgets import QWidget\n    try:\n        from shiboken2 import isValid\n    except ImportError:\n        isValid = None\nexcept ImportError:\n    from PySide6.QtCore import Qt\n    from PySide6.QtWidgets import QWidget\n    try:\n        from shiboken6 import isValid\n    except ImportError:\n        isValid = None\n\n\n_OPEN_WINDOWS = {}\n\n\ndef _is_valid_widget(widget):\n    if widget is None:\n        return False\n\n    if not isinstance(widget, QWidget):\n        return False\n\n    if isValid is None:\n        return True\n\n    try:\n        return bool(isValid(widget))\n    except Exception:\n        return False\n\n\ndef _remove_window(tool_key):\n    _OPEN_WINDOWS.pop(tool_key, None)\n\n\ndef _prepare_window(window):\n    try:\n        window.setWindowModality(Qt.NonModal)\n    except Exception:\n        pass\n\n    try:\n        flags = window.windowFlags()\n        flags = flags | Qt.Window\n        flags = flags | Qt.WindowMinimizeButtonHint\n        flags = flags | Qt.WindowCloseButtonHint\n        window.setWindowFlags(flags)\n    except Exception:\n        pass\n\n\ndef show_tool(tool_key, tool_function):\n    old_window = _OPEN_WINDOWS.get(tool_key)\n\n    if _is_valid_widget(old_window):\n        try:\n            if old_window.isMinimized():\n                old_window.showNormal()\n            else:\n                old_window.show()\n\n            old_window.raise_()\n            old_window.activateWindow()\n            return old_window\n\n        except Exception:\n            _OPEN_WINDOWS.pop(tool_key, None)\n\n    result = tool_function()\n\n    if not isinstance(result, QWidget):\n        return result\n\n    window = result\n\n    _prepare_window(window)\n\n    _OPEN_WINDOWS[tool_key] = window\n\n    try:\n        window.destroyed.connect(\n            lambda *args, key=tool_key: _remove_window(key)\n        )\n    except Exception:\n        pass\n\n    try:\n        window.show()\n        window.raise_()\n        window.activateWindow()\n    except Exception:\n        pass\n\n    return window\n\n\ndef close_tool(tool_key):\n    window = _OPEN_WINDOWS.get(tool_key)\n\n    if not _is_valid_widget(window):\n        _OPEN_WINDOWS.pop(tool_key, None)\n        return\n\n    try:\n        window.close()\n    finally:\n        _OPEN_WINDOWS.pop(tool_key, None)\n\n\ndef close_all_tools():\n    tool_keys = list(_OPEN_WINDOWS.keys())\n\n    for tool_key in tool_keys:\n        close_tool(tool_key)\n\n\ndef get_open_windows():\n    result = {}\n\n    for tool_key, window in _OPEN_WINDOWS.items():\n        if _is_valid_widget(window):\n            result[tool_key] = window\n\n    return result\n'


def log(message):
    print("[Window Fix] {}".format(message))


def backup_file(path):
    backup = path + ".before_window_fix.bak"

    if not os.path.exists(backup):
        shutil.copy2(path, backup)
        log("backup: {}".format(os.path.relpath(backup, ROOT)))


def write_utf8(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as file_obj:
        file_obj.write(content)

    log("write: {}".format(os.path.relpath(path, ROOT)))


def patch_rigging_toolbox():
    if not os.path.isfile(RIGGING_TOOLBOX):
        raise RuntimeError("MuziTools/rigging_toolbox.py not found")

    backup_file(RIGGING_TOOLBOX)

    with open(RIGGING_TOOLBOX, "r", encoding="utf-8") as file_obj:
        content = file_obj.read()

    import_line = "from .tools import get_tools_by_category"

    if "from . import window_manager" not in content:
        if import_line not in content:
            raise RuntimeError("get_tools_by_category import not found")

        content = content.replace(
            import_line,
            import_line + "\nfrom . import window_manager",
            1,
        )

    old_connect = "btn.clicked.connect(lambda *args, f=tool_func: f())"

    new_connect = (
        'tool_key = "{}/{}".format(category_name, tool_name)\n'
        '                btn.clicked.connect(\n'
        '                    lambda *args, key=tool_key, f=tool_func: '
        'window_manager.show_tool(key, f)\n'
        '                )'
    )

    if old_connect in content:
        content = content.replace(
            old_connect,
            new_connect,
            1,
        )
    elif "window_manager.show_tool" not in content:
        raise RuntimeError(
            "old button connection code not found; "
            "rigging_toolbox.py may have changed"
        )

    write_utf8(RIGGING_TOOLBOX, content)


def main():
    if not os.path.isdir(MUZI_DIR):
        raise RuntimeError(
            "Put this script in the muziToolset repository root."
        )

    write_utf8(
        WINDOW_MANAGER,
        WINDOW_MANAGER_CONTENT,
    )

    patch_rigging_toolbox()

    print("")
    print("=== Window lifetime fix complete ===")
    print("")
    print("Restart Maya 2023 and test:")
    print("    import muziToolset")
    print("    window = muziToolset.show()")


if __name__ == "__main__":
    main()
