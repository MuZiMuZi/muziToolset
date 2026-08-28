# coding=utf-8
from importlib import reload
from . import rigging_toolbox

reload(rigging_toolbox)
window = None


def main():
    global window
    try:
        if window is not None:
            window.close()
            window.deleteLater()
    except Exception:
        pass
    window = rigging_toolbox.main()
    return window


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback
        print('')
        print('!!! MuziTools merge failed !!!')
        traceback.print_exc()
        raise
