# coding=utf-8
"""真实 Qt 窗口检查，Maya 查询使用测试桩，不验证场景算法。"""
import os
from pathlib import Path
import sys, types, importlib, traceback
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from unittest.mock import MagicMock
from PySide6.QtWidgets import QApplication, QWidget
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
def main():
    """验证所有 UI 入口，返回失败数量。"""
    for name in ('maya', 'maya.cmds', 'maya.mel', 'maya.api', 'maya.api.OpenMaya', 'maya.OpenMayaUI'):
        mod=types.ModuleType(name)
        mod.__getattr__ = lambda name: MagicMock() if not name.startswith('__') else None
        sys.modules[name]=mod
    for name in ('maya.cmds', 'maya.mel', 'maya.api', 'maya.api.OpenMaya', 'maya.OpenMayaUI'):
        parent, child = name.rsplit('.', 1)
        setattr(sys.modules[parent], child, sys.modules[name])
    cmds=sys.modules['maya.cmds']
    for name,value in {'ls':[], 'listRelatives':[], 'objExists':False, 'listConnections':[], 'listAttr':[], 'getAttr':0, 'attributeQuery':False, 'colorIndex':[0.5,0.5,0.5]}.items():
        setattr(cmds, name, MagicMock(return_value=value))
    omui=sys.modules['maya.OpenMayaUI'];omui.MQtUtil=MagicMock();omui.MQtUtil.mainWindow.return_value=None
    app=QApplication([])
    from muziToolset.tools import get_tools_by_category
    failures=[]; windows=[]
    for category,tools in get_tools_by_category().items():
        for name,runner in tools.items():
            if runner.tool_mode=='action':continue
            try:
                window=runner()
                assert isinstance(window,QWidget), type(window)
                assert runner() is window, 'not reused'
                assert window.isVisible(), 'not visible'
                windows.append(window)
                print('PASS',category,name)
            except Exception:
                failures.append(name);traceback.print_exc()
    from muziToolset.app import toolbox
    try:
        window=toolbox.main();assert window.isVisible();windows.append(window)
        print('PASS main toolbox')
    except Exception:
        failures.append('toolbox');traceback.print_exc()
    print('RESULT', len(windows), 'windows;', len(failures), 'failed', failures)
    for window in windows:window.close()
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
