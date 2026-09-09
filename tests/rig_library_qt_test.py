# coding=utf-8
u"""使用真实 Qt 控件检查绑定库交互；场景操作使用可撤销测试桩。"""

import os
import pathlib
import sys
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from muziToolset.systems.rig.ui.modular_rig_ui import ModularRigWindow
from muziToolset.systems.rig.ui.library_widgets import QtCore, QtWidgets, Qt
from muziToolset.tests.rig_library_test import ServiceFixture, FakeCommands
from muziToolset.systems.rig import library_catalog as catalog

application = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


class RigLibraryQtTests(unittest.TestCase):
    def setUp(self):
        self.service = ServiceFixture(FakeCommands())
        self.window = ModularRigWindow(service=self.service)
        self.window.show()
        application.processEvents()

    def tearDown(self):
        self.window.close()
        application.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)
        application.processEvents()

    def test_empty_window_template_and_search(self):
        self.assertFalse(self.window.build_button.isEnabled())
        self.window.add_selected_template()
        self.assertEqual(len(self.service.document["modules"]), 3)
        self.assertTrue(self.window.build_button.isEnabled())
        self.window.module_search.setText("tongue")
        self.assertTrue(self.window.module_list.item(0).isHidden())
        self.assertFalse(self.window.module_list.item(1).isHidden())
        self.window.tree_search.setText("tongue")
        root = self.window.module_tree.topLevelItem(0)
        self.assertTrue(root.child(0).isHidden())
        self.assertFalse(root.child(2).isHidden())

    def test_stage_actions_and_built_parameter_edit(self):
        self.window.add_selected_template()
        for record in self.service.document["modules"]:
            for name in catalog.guide_names(record):
                self.service.cmds.createNode("transform", name=name)
        self.service.setup()
        self.window.refresh_scene()
        self.window.set_step(3)
        self.window.run_step()
        self.assertEqual(self.window.current_step, 4)
        self.assertFalse(self.window.remove_button.isEnabled())
        self.assertFalse(self.window.side_combo.isEnabled())
        self.assertFalse(self.window.step_buttons[4].isEnabled())
        self.window.size_spin.setValue(2.3)
        self.assertEqual(self.service.document["modules"][0]["ctrl_size"], 2.3)
        self.assertEqual(len(self.service.calls), 3)

    def test_undo_refresh_reloads_config(self):
        self.window.add_selected_template()
        self.assertEqual(len(self.service.document["modules"]), 3)
        self.service.cmds.undo()
        self.window.refresh_scene()
        self.assertEqual(self.service.document["modules"], [])
        self.assertFalse(self.window.build_button.isEnabled())

    def test_compact_layout_never_overlaps_library_sections(self):
        self.window.add_selected_template()
        self.window.resize(1120, 740)
        application.processEvents()
        for step in self.window.step_buttons:
            self.assertEqual(step.height(), 78)
        self.assertGreater(self.window.library_scroll.verticalScrollBar().maximum(), 0)
        self.assertGreater(self.window.template_search.y(), self.window.module_list.geometry().bottom())
        self.assertGreater(self.window.build_button.width(), 200)
        self.assertTrue(self.window.windowFlags() & Qt.WindowMinimizeButtonHint)

    def test_inline_validation_preserves_records(self):
        self.window.add_selected_module()
        self.window.set_step(3)
        self.assertEqual(self.window.current_step, 1)
        self.window.run_step()
        self.assertEqual(self.service.calls, [])
        self.assertEqual(self.window.current_step, 2)
        self.window.set_step(3)
        self.assertIn(u"尚未解锁", self.window.status_label.text())
        self.assertEqual(len(self.service.document["modules"]), 1)

    def test_switching_steps_exposes_guide_drawer(self):
        self.window.add_selected_module()
        self.assertFalse(self.window.guide_section.button.isChecked())
        self.window.set_step(2)
        self.assertEqual(self.window.current_step, 1)
        self.service.setup()
        self.window.set_step(2)
        self.assertTrue(self.window.guide_section.button.isChecked())
        self.window.set_step(4)
        self.assertEqual(self.window.current_step, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
