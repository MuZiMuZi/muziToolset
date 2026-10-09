# coding=utf-8
"""真实 Qt 配置交互回归；Maya 查询为命令替身，场景求值另行验收。"""
import os
import pathlib
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
try:
    from PySide6 import QtWidgets
except ImportError:
    QtWidgets = None


@unittest.skipIf(QtWidgets is None, '未安装 PySide6，Qt 交互在专用 CI 执行')
class RbfUiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
        modules = {}
        for name in ('maya', 'maya.cmds', 'maya.mel', 'maya.api', 'maya.api.OpenMaya', 'maya.OpenMayaUI'):
            module = types.ModuleType(name)
            module.__getattr__ = lambda name: MagicMock() if not name.startswith('__') else None
            modules[name] = module
        for name in ('maya.cmds', 'maya.mel', 'maya.api', 'maya.api.OpenMaya', 'maya.OpenMayaUI'):
            parent, child = name.rsplit('.', 1)
            setattr(modules[parent], child, modules[name])
        cls.patcher = patch.dict(sys.modules, modules)
        cls.patcher.start()
        cls.addClassCleanup(cls.patcher.stop)
        cls.application = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        from muziToolset.tools.rig.rbf_corrective_tool import RbfCorrectiveTool
        cls.window_type = RbfCorrectiveTool

    def setUp(self):
        self.window = self.window_type()
        self.addCleanup(self.window.close)

    def test_smooth_preset_preserves_mode_and_wrist_thresholds(self):
        self.window.solver_type.setCurrentText('smoothstep')
        for part, angles in (('arm', [45, 45, 90]), ('thigh', [45, 45, 90]), ('wrist', [22.5, 22.5, 45])):
            self.window.part.setCurrentText(part)
            self.window.apply_preset()
            model = self.window.read_settings()
            self.assertEqual(model.solver_type, 'smoothstep')
            self.assertEqual(model.smooth['angles'], angles)

    def test_custom_joint_and_sample_removal(self):
        self.window.part.setCurrentText('ankle')
        self.window.inputs.setText('hero:ankle.rotateX,hero:ankle.rotateY,hero:ankle.rotateZ')
        self.window.apply_preset()
        self.assertEqual(self.window.read_settings().part, 'ankle')
        self.window.model.add_pose('neutral', [0, 0, 0], neutral=True)
        self.window.model.add_pose('bend', [30, 0, 0])
        self.window.show_poses()
        self.window.poses.setCurrentRow(0)
        with self.assertRaises(ValueError):
            self.window.remove_pose()
        self.window.poses.setCurrentRow(1)
        self.window.remove_pose()
        self.assertEqual(len(self.window.model.poses), 1)


if __name__ == '__main__':
    if QtWidgets is None:
        raise SystemExit('Qt 专项测试需要可加载的 PySide6 和 Linux 图形依赖')
    unittest.main()
