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
        lifecycle_methods = (
            "setup_window", "create_widgets", "create_layouts",
            "create_header_layout", "create_step_layout", "create_module_panel",
            "create_rig_structure_panel", "create_properties_panel",
            "create_bottom_layout", "create_connections", "apply_style",
            "load_data", "refresh_ui",
            "refresh_step_ui", "refresh_module_list", "refresh_rig_structure",
            "refresh_properties", "refresh_status", "set_current_step",
            "set_current_module", "validate_current_step", "build_current_step",
        )
        for method_name in lifecycle_methods:
            self.assertTrue(callable(getattr(self.window, method_name)))
        self.assertFalse(hasattr(self.window, "_create_layout"))
        self.assertFalse(hasattr(self.window, "_create_properties"))
        self.assertFalse(self.window.build_button.isEnabled())
        self.assertEqual(self.window.build_button.text(), u"下一步")
        self.assertTrue(self.window.basic_section.isVisible())
        self.assertFalse(self.window.guide_section.isVisible())
        self.assertFalse(self.window.control_section.isVisible())
        self.assertFalse(self.window.joint_section.isVisible())
        self.window.add_selected_template()
        self.assertEqual(self.window.current_module, self.window.current_id)
        self.assertEqual(len(self.service.document["modules"]), 3)
        self.assertTrue(self.window.build_button.isEnabled())
        self.window.module_search.setText("tongue")
        self.assertTrue(self.window.module_list.item(0).isHidden())
        self.assertFalse(self.window.module_list.item(1).isHidden())
        self.assertEqual(self.window.library_tabs.tabText(0), "MODULES  1 / 3")
        self.window.library_tabs.setCurrentIndex(1)
        self.window.template_search.setText("Ear Pair")
        self.assertEqual(self.window.library_tabs.tabText(1), "TEMPLATES  1 / 3")
        self.window.tree_search.setText("tongue")
        root = self.window.module_tree.topLevelItem(0)
        self.assertTrue(root.child(0).isHidden())
        self.assertFalse(root.child(2).isHidden())

    def test_loading_catalog_data_is_idempotent(self):
        self.window.load_data()
        self.window.load_data()

        self.assertEqual(self.window.module_list.count(), len(catalog.modules))
        self.assertEqual(self.window.template_list.count(), len(catalog.templates))
        self.assertEqual(self.window.side_combo.count(), 3)
        self.assertEqual(self.window.axis_combo.count(), len(catalog.axes))

    def test_stage_actions_and_built_parameter_edit(self):
        self.window.add_selected_template()
        for record in self.service.document["modules"]:
            for name in catalog.guide_names(record):
                self.service.cmds.createNode("transform", name=name)
        self.window.run_step()
        self.assertEqual(self.window.current_step, 2)
        self.assertFalse(self.window.step_buttons[2].isEnabled())
        self.window.run_step()
        self.assertEqual(self.window.current_step, 3)
        self.assertFalse(self.window.basic_section.isVisible())
        self.assertFalse(self.window.guide_section.isVisible())
        self.assertTrue(self.window.control_section.isVisible())
        self.assertTrue(self.window.joint_section.isVisible())
        self.assertTrue(self.window.control_section.isAncestorOf(self.window.control_check))
        self.window.run_step()
        self.assertEqual(self.window.current_step, 4)
        self.assertFalse(self.window.basic_section.isVisible())
        self.assertFalse(self.window.guide_section.isVisible())
        self.assertFalse(self.window.control_section.isVisible())
        self.assertFalse(self.window.joint_section.isVisible())
        self.assertEqual(len(self.window.step_buttons), 4)
        self.assertEqual([step.title for step in self.window.step_buttons],
                         ["Setup", "Guide", "Ctrl", "Final"])
        self.assertFalse(self.window.remove_button.isEnabled())
        self.assertFalse(self.window.side_combo.isEnabled())
        self.window.size_spin.setValue(2.3)
        self.assertEqual(self.service.document["modules"][0]["ctrl_size"], 2.3)
        self.assertEqual(len(self.service.calls), 3)
        self.window.run_step()
        self.assertEqual(len(self.service.cmds.selection), 11)
        self.assertIn("Final", self.window.status_label.text())

        self.window.set_step(2)
        self.assertEqual(self.window.build_button.text(), u"下一步")
        self.window.run_step()
        self.assertEqual(self.window.current_step, 3)
        current = self.window.current_record()
        self.assertTrue(current["built"])
        self.assertFalse(current["connected"])

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
        self.assertEqual(self.window.library_tabs.count(), 2)
        self.assertGreater(self.window.module_list.viewport().height(), 150)
        self.assertGreater(self.window.build_button.width(), 200)
        self.assertTrue(self.window.windowFlags() & Qt.WindowMinimizeButtonHint)

    def test_structure_add_button_opens_module_library(self):
        self.window.library_tabs.setCurrentIndex(1)
        self.window.open_module_library()
        self.assertEqual(self.window.library_tabs.currentIndex(), 0)
        self.assertTrue(self.window.module_search.hasFocus())

    def test_structure_only_lists_modules(self):
        self.window.add_selected_template()
        root = self.window.module_tree.topLevelItem(0)
        self.assertEqual(root.text(2), u"3 模块")
        self.assertEqual(self.window.module_tree.headerItem().text(0), u"模块")
        self.assertEqual(root.child(0).childCount(), 0)
        self.window.tree_search.setText(u"待构建")
        self.assertFalse(root.child(0).isHidden())
        self.assertNotIn(u"场景节点", self.window.structure_note.text())

    def test_structure_context_menu_mirrors_paired_module(self):
        self.window.add_selected_template()
        source = self.service.document["modules"][0]
        target = self.service.document["modules"][1]
        source_guides = catalog.guide_names(source)
        target_guides = catalog.guide_names(target)
        for index in range(len(source_guides)):
            self.service.cmds.createNode("transform", name=source_guides[index])
            self.service.cmds.createNode("transform", name=target_guides[index])
            self.service.cmds.xform(source_guides[index], translation=[index + 1.0, 2.0, 3.0])
        root = self.window.module_tree.topLevelItem(0)
        source_item = root.child(0)
        self.window.module_tree.setCurrentItem(source_item)
        self.assertEqual(self.window.module_tree.contextMenuPolicy(), Qt.CustomContextMenu)
        menu = self.window.create_structure_context_menu(source_item)
        self.assertEqual(len(menu.actions()), 1)
        self.assertTrue(menu.actions()[0].isEnabled())
        self.assertIn(u"右侧", menu.actions()[0].text())

        menu.actions()[0].trigger()
        application.processEvents()

        self.assertEqual(self.service.cmds.xform(target_guides[0], query=True), [-1.0, 2.0, 3.0])
        self.assertIn("RT", self.window.status_label.text())
        root = self.window.module_tree.topLevelItem(0)
        center_menu = self.window.create_structure_context_menu(root.child(2))
        self.assertFalse(center_menu.actions()[0].isEnabled())
        self.assertIn(u"中央模块", center_menu.actions()[0].text())
        self.assertIsNone(self.window.create_structure_context_menu(root))

    def test_inline_validation_preserves_records(self):
        self.window.add_selected_module()
        self.window.set_step(3)
        self.assertEqual(self.window.current_step, 1)
        self.window.run_step()
        self.assertEqual(self.service.calls, [])
        self.assertEqual(self.window.current_step, 2)
        self.window.set_step(3)
        self.assertIn(u"下一步", self.window.status_label.text())
        self.assertEqual(len(self.service.document["modules"]), 1)

    def test_switching_steps_exposes_guide_drawer(self):
        self.window.add_selected_module()
        self.assertFalse(self.window.guide_section.button.isChecked())
        self.window.set_step(2)
        self.assertEqual(self.window.current_step, 1)
        self.service.setup()
        self.window.set_step(2)
        self.assertEqual(self.window.current_step, 1)
        self.window.run_step()
        self.assertTrue(self.window.guide_section.isVisible())
        self.assertTrue(self.window.guide_section.button.isChecked())
        self.assertFalse(self.window.basic_section.isVisible())
        self.assertFalse(self.window.control_section.isVisible())
        self.assertFalse(self.window.joint_section.isVisible())
        self.window.set_step(4)
        self.assertEqual(self.window.current_step, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
