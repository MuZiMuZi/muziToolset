# coding=utf-8
"""使用真实 Qt 点击新增按钮，Maya 与 Core 场景操作使用测试桩。"""

import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PySide6.QtWidgets import QApplication


def prepare_maya():
    """为 UI 导入提供 Maya 测试桩，不连接真实 Maya。"""
    for name in ('maya', 'maya.cmds', 'maya.api', 'maya.api.OpenMaya', 'maya.mel', 'maya.OpenMayaUI'):
        module = types.ModuleType(name)
        module.__getattr__ = lambda key: MagicMock() if not key.startswith('__') else None
        sys.modules[name] = module
    for name in ('maya.cmds', 'maya.api', 'maya.api.OpenMaya', 'maya.mel', 'maya.OpenMayaUI'):
        parent, child = name.rsplit('.', 1)
        setattr(sys.modules[parent], child, sys.modules[name])
    commands = sys.modules['maya.cmds']
    commands.ls = MagicMock(return_value=['sculpt', 'base'])
    commands.objExists = MagicMock(return_value=True)
    commands.warning = MagicMock()
    return commands


class TargetUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])
        cls.commands = prepare_maya()
        from muziToolset.tools.blendshape import add_blendshape_tool
        cls.module = add_blendshape_tool

    def setUp(self):
        self.window = self.module.BlendShapeTargetTool()
        self.window.blendshape_line.setText('bs')
        self.window.controller_picker.line_edit.setText('ctrl')
        self.window.inverted_target_name.setText('smile_fix')
        self.commands.ls.return_value = ['sculpt', 'base']
        self.window.refresh_targets = MagicMock()

    def tearDown(self):
        self.window.close()

    def test_add_button_passes_selection_order_and_updates_status(self):
        with patch.object(self.module.corrective_target, 'add_inverted_target',
                          return_value={'index': 10, 'alias': 'smile_fix'}) as action:
            self.window.add_inverted_button.click()
        action.assert_called_once_with(controller='ctrl', blendshape_node='bs',
                                       corrective_mesh='sculpt', base_mesh='base',
                                       target_name='smile_fix')
        self.window.refresh_targets.assert_called_once_with()
        self.assertIn('smile_fix', self.window.status_label.text())
        self.assertIn('权重为 0', self.window.status_label.text())

    def test_wrong_selection_never_runs_core_action(self):
        self.commands.ls.return_value = ['sculpt']
        with patch.object(self.module.corrective_target, 'add_inverted_target') as action:
            self.window.add_inverted_button.click()
        action.assert_not_called()

    def test_rename_button_calls_core_and_refreshes(self):
        with patch.object(self.module.target_alias_utils, 'rename_mirrored_targets',
                          return_value=[{'index': 9}]) as action:
            self.window.rename_mirrored_button.click()
        action.assert_called_once_with('bs')
        self.window.refresh_targets.assert_called_once_with()
        self.assertIn('已重命名 1 个', self.window.status_label.text())


if __name__ == '__main__':
    unittest.main()
