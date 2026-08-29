# coding=utf-8
from ... import Connections_Tool_main as module

_window = None


def main():
    global _window
    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = module.Connections_Tool()

    if _window is not None:
        try:
            _window.show()
            _window.raise_()
            _window.activateWindow()
        except Exception:
            pass

    return _window
