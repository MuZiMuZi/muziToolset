# coding=utf-8
u"""绑定库行为测试：不需要 Maya，覆盖配置、事务、冲突和现有接口调度。"""

import copy
import importlib
import json
import pathlib
import sys
import tempfile
import types
import unittest
from unittest import mock

repo_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root.parent))
from muziToolset.systems.rig import library_catalog as catalog
from muziToolset.systems.rig.library_service import RigLibraryService


class FakeCommands:
    u"""只模拟服务所需的场景存储与 Undo，不模拟 Maya 绑定计算。"""

    def __init__(self):
        self.nodes = {}
        self.stack = []
        self.snapshot = None
        self.undo_enabled = True
        self.namespace = ":"
        self.undo_count = 0
        self.selection = []

    def objExists(self, name):
        return name in self.nodes

    def nodeType(self, name):
        return self.nodes[name]["type"]

    def attributeQuery(self, attribute, node, exists=True):
        return attribute in self.nodes[node]["attrs"]

    def getAttr(self, plug):
        name, attribute = plug.split(".", 1)
        return self.nodes[name]["attrs"].get(attribute)

    def createNode(self, node_type, name, **kwargs):
        if name in self.nodes:
            raise RuntimeError("duplicate node")
        self.nodes[name] = {"type": node_type, "attrs": {}, "translation": [0.0, 0.0, 0.0]}
        return name

    def addAttr(self, name, longName, **kwargs):
        self.nodes[name]["attrs"][longName] = None

    def setAttr(self, plug, value, **kwargs):
        name, attribute = plug.split(".", 1)
        self.nodes[name]["attrs"][attribute] = value

    def namespaceInfo(self, **kwargs):
        return self.namespace

    def undoInfo(self, query=False, state=False, openChunk=False, closeChunk=False, **kwargs):
        if query:
            return self.undo_enabled
        if openChunk:
            self.snapshot = copy.deepcopy(self.nodes)
        if closeChunk:
            self.stack.append(self.snapshot)
            self.snapshot = None

    def undo(self):
        self.nodes = self.stack.pop()
        self.undo_count += 1

    def ls(self, name, **kwargs):
        return [name] if name in self.nodes else []

    def select(self, names, replace=True):
        self.selection = list(names)

    def xform(self, name, query=False, worldSpace=False, translation=None, **kwargs):
        if query:
            return list(self.nodes[name]["translation"])
        self.nodes[name]["translation"] = list(translation)


class ServiceFixture(RigLibraryService):
    u"""将绑定计算替换成输出桩，验证服务实际如何调度 Module。"""

    def __init__(self, commands):
        self.calls = []
        self.fail_kind = None
        self.display_calls = []
        super(ServiceFixture, self).__init__(commands)

    def _make_builder(self, record):
        owner = self
        class Builder:
            def build(self):
                owner.calls.append(record["kind"])
                for group, names in catalog.output_names(record).items():
                    for name in names:
                        owner.cmds.createNode("joint" if group == "joints" else "transform", name=name)
                if owner.fail_kind == record["kind"]:
                    raise RuntimeError("injected build failure")
        return Builder()

    def _apply_display(self, record, previous=None):
        self.display_calls.append((copy.deepcopy(record), previous))


class RigLibraryTests(unittest.TestCase):
    def setUp(self):
        self.commands = FakeCommands()
        self.service = ServiceFixture(self.commands)

    def prepare_face(self):
        self.service.add_template("face_starter")
        for record in self.service.document["modules"]:
            for name in catalog.guide_names(record):
                self.commands.createNode("transform", name=name)

    def test_open_is_read_only_and_templates_preserve_edits(self):
        self.assertEqual(self.commands.nodes, {})
        self.service.add_template("face_starter")
        first = self.service.document["modules"][0]
        self.service.update_module(first["id"], {"ctrl_size": 2.5})
        before = copy.deepcopy(self.service.document)
        self.service.add_template("face_starter")
        self.assertEqual(before, self.service.document)
        self.assertEqual(len(before["modules"]), 3)
        self.assertEqual(RigLibraryService(self.commands).document, before)

    def test_unknown_modules_never_fall_back_to_fk(self):
        with self.assertRaises(ValueError):
            self.service.add_module("eye")
        self.assertEqual(self.commands.nodes, {})

    def test_workflow_state_tracks_real_scene_progress(self):
        state = self.service.workflow_state()
        self.assertEqual(state["suggested"], 1)
        self.assertFalse(state["unlocked"][2])
        self.prepare_face()
        state = self.service.workflow_state()
        self.assertEqual(state["suggested"], 1)
        self.service.setup()
        state = self.service.workflow_state()
        self.assertTrue(state["completed"][1])
        self.assertTrue(state["completed"][2])
        self.assertEqual(state["suggested"], 3)
        self.service.build()
        state = self.service.workflow_state()
        self.assertTrue(state["completed"][3])
        self.assertTrue(state["unlocked"][4])
        self.assertEqual(state["suggested"], 4)
        self.assertEqual(set(state["unlocked"]), {1, 2, 3, 4})
        self.assertEqual(self.service.finalize(), 11)
        state = self.service.workflow_state()
        self.assertTrue(state["completed"][4])
        self.assertEqual(len(self.commands.selection), 11)

    def test_legacy_build_state_migrates_to_connected(self):
        document = catalog.new_document()
        record = catalog.new_module("ear")
        record["built"] = True
        del record["connected"]
        document["modules"].append(record)

        migrated = catalog.validate_document(document)

        self.assertTrue(migrated["modules"][0]["built"])
        self.assertTrue(migrated["modules"][0]["connected"])

    def test_duplicate_names_are_rejected_atomically(self):
        self.service.add_template("ear_pair")
        before = copy.deepcopy(self.commands.nodes)
        with self.assertRaises(ValueError):
            self.service.add_module("ear")
        self.assertEqual(self.commands.nodes, before)

    def test_non_finite_sizes_and_bad_side_are_rejected(self):
        self.service.add_module("ear")
        identity = self.service.document["modules"][0]["id"]
        for values in ({"ctrl_size": float("nan")}, {"ctrl_size": 0},
                       {"side": "md"}, {"ctrl_color": 32}):
            with self.assertRaises(ValueError):
                self.service.update_module(identity, values)
        self.assertEqual(self.service.document["modules"][0]["ctrl_size"], 1)

    def test_mirror_module_copies_settings_and_guide_positions(self):
        self.prepare_face()
        source = self.service.document["modules"][0]
        target = self.service.document["modules"][1]
        self.service.update_module(source["id"], {
            "ctrl_size": 2.5,
            "ctrl_axis": "Z+",
            "jnt_radius": 0.75,
            "show_axis": True,
        })
        source = self.service.document["modules"][0]
        source_guides = catalog.guide_names(source)
        target_guides = catalog.guide_names(target)
        positions = ([2.0, 3.0, 4.0], [3.0, 4.0, 5.0], [4.0, 5.0, 6.0])
        for index in range(len(source_guides)):
            self.commands.xform(source_guides[index], translation=positions[index])

        result = self.service.mirror_module(source["id"])

        target = self.service.document["modules"][1]
        self.assertEqual(result["guide_count"], 3)
        self.assertEqual(target["ctrl_size"], 2.5)
        self.assertEqual(target["ctrl_axis"], "Z+")
        self.assertEqual(target["jnt_radius"], 0.75)
        self.assertTrue(target["show_axis"])
        self.assertEqual(target["ctrl_color"], 13)
        for index in range(len(target_guides)):
            expected = [-positions[index][0], positions[index][1], positions[index][2]]
            self.assertEqual(self.commands.xform(target_guides[index], query=True), expected)

    def test_fk_requires_explicit_ordered_guides(self):
        self.service.add_module("fk_chain")
        self.assertTrue(self.service.validate())
        identity = self.service.document["modules"][0]["id"]
        self.commands.createNode("transform", name="end")
        self.commands.createNode("transform", name="start")
        self.service.update_module(identity, {"guides": ["end", "start"]})
        self.assertEqual(catalog.guide_names(self.service.document["modules"][0]), ["end", "start"])
        self.assertEqual(self.service.validate(), [])

    def test_missing_guide_blocks_before_any_build(self):
        self.service.add_template("face_starter")
        before = copy.deepcopy(self.commands.nodes)
        with self.assertRaises(RuntimeError):
            self.service.build()
        self.assertEqual(self.service.calls, [])
        self.assertEqual(self.commands.nodes, before)

    def test_existing_output_and_foreign_root_are_never_adopted(self):
        self.prepare_face()
        self.commands.createNode("joint", name="jnt_lf_ear_bind_001")
        before = copy.deepcopy(self.commands.nodes)
        with self.assertRaises(RuntimeError):
            self.service.build()
        self.assertEqual(self.commands.nodes, before)
        del self.commands.nodes["jnt_lf_ear_bind_001"]
        self.commands.createNode("transform", name=self.service.root)
        with self.assertRaises(RuntimeError):
            self.service.build()
        self.assertEqual(self.service.calls, [])

    def test_success_builds_only_pending_modules_and_restores(self):
        self.prepare_face()
        self.assertEqual(self.service.build(), 3)
        before = copy.deepcopy(self.commands.nodes)
        self.assertEqual(self.service.build(), 0)
        self.assertEqual(self.service.calls, ["ear", "ear", "tongue"])
        self.assertEqual(self.commands.nodes, before)
        reopened = ServiceFixture(self.commands)
        for record in reopened.document["modules"]:
            self.assertTrue(record["built"])
        self.assertEqual(reopened.validate(), [])

    def test_partial_failure_rolls_back_whole_transaction(self):
        self.prepare_face()
        before = copy.deepcopy(self.commands.nodes)
        document = copy.deepcopy(self.service.document)
        self.service.fail_kind = "tongue"
        with self.assertRaisesRegex(RuntimeError, "injected"):
            self.service.build()
        self.assertEqual(self.commands.nodes, before)
        self.assertEqual(self.service.document, document)
        self.assertEqual(self.commands.undo_count, 1)

    def test_built_identity_and_removal_are_locked(self):
        self.prepare_face()
        self.service.build()
        identity = self.service.document["modules"][0]["id"]
        with self.assertRaises(ValueError):
            self.service.update_module(identity, {"side": "rt"})
        with self.assertRaises(RuntimeError):
            self.service.remove_module(identity)

    def test_replaced_nodes_block_live_updates(self):
        self.prepare_face()
        self.service.build()
        identity = self.service.document["modules"][0]["id"]
        self.commands.nodes["ctrl_lf_ear_fk_001"]["attrs"].clear()
        with self.assertRaises(RuntimeError):
            self.service.update_module(identity, {"ctrl_size": 2.0})

    def test_undo_and_namespace_guards_do_not_mutate(self):
        self.commands.undo_enabled = False
        with self.assertRaises(RuntimeError):
            self.service.add_module("ear")
        self.commands.undo_enabled = True
        self.commands.namespace = ":character"
        with self.assertRaises(RuntimeError):
            self.service.add_module("ear")
        self.assertEqual(self.commands.nodes, {})

    def test_export_resets_build_status_and_import_conflict_is_atomic(self):
        self.prepare_face()
        self.service.build()
        with tempfile.TemporaryDirectory() as folder:
            path = str(pathlib.Path(folder) / "recipe.json")
            self.service.export_recipe(path)
            payload = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
            for record in payload["modules"]:
                self.assertFalse(record["built"])
            other = ServiceFixture(FakeCommands())
            other.import_recipe(path)
            self.assertEqual(len(other.document["modules"]), 3)
            before = copy.deepcopy(self.commands.nodes)
            with self.assertRaises(ValueError):
                self.service.import_recipe(path)
            self.assertEqual(self.commands.nodes, before)

    def test_live_size_uses_ratio_and_never_builds(self):
        self.prepare_face()
        self.service.build()
        previous = copy.deepcopy(self.service.document["modules"][0])
        previous["ctrl_size"] = 2.0
        updated = copy.deepcopy(previous)
        updated["ctrl_size"] = 3.0
        ctrl_module = types.ModuleType("muziToolset.core.rigging.ctrl_utils")
        jnt_module = types.ModuleType("muziToolset.core.rigging.jnt_utils")
        controller = mock.Mock()
        joint = mock.Mock()
        ctrl_module.Ctrl = mock.Mock(return_value=controller)
        jnt_module.Jnt = mock.Mock(return_value=joint)
        with mock.patch.dict(sys.modules, {ctrl_module.__name__: ctrl_module, jnt_module.__name__: jnt_module}):
            RigLibraryService._apply_display(self.service, updated, previous)
        self.assertEqual(controller.set_ctrl_size.call_count, 6)
        controller.set_ctrl_size.assert_called_with(1.5)
        controller.set_ctrl_axis.assert_not_called()
        controller.create_ctrl.assert_not_called()

    def test_factory_calls_current_public_builders(self):
        record = catalog.new_module("ear")
        builders = {}
        modules = {}
        for path, class_name in (
                ("muziToolset.systems.face.ear_module", "EarModule"),
                ("muziToolset.systems.face.tongue_module", "TongueModule"),
                ("muziToolset.systems.components.fk_chain", "FKChain")):
            module = types.ModuleType(path)
            factory = mock.Mock()
            setattr(module, class_name, factory)
            modules[path] = module
            builders[class_name] = factory
        with mock.patch.dict(sys.modules, modules):
            result = RigLibraryService._make_builder(self.service, record)
        builders["EarModule"].assert_called_once()
        builders["TongueModule"].assert_not_called()
        builders["FKChain"].assert_not_called()
        self.assertEqual(result.ctrl_size, 1.0)

    def test_locator_alignment_uses_shape_world_position(self):
        maya = types.ModuleType("maya")
        commands = types.ModuleType("maya.cmds")
        pymel = types.ModuleType("pymel")
        pm = types.ModuleType("pymel.core")
        commands.listRelatives = mock.Mock(return_value=["guideShape"])
        commands.getAttr = mock.Mock(return_value=[(7.0, 162.0, -3.0)])
        commands.xform = mock.Mock()
        pm.PyNode = lambda value: value
        pm.matchTransform = mock.Mock()
        with mock.patch.dict(sys.modules, {"maya": maya, "maya.cmds": commands, "pymel": pymel, "pymel.core": pm}):
            name = "muziToolset.core.common.transform_utils"
            sys.modules.pop(name, None)
            module = importlib.import_module(name)
            module.Transform("target").match_transform("guide")
            commands.getAttr.assert_called_once_with("guideShape.worldPosition[0]")
            commands.xform.assert_called_once_with("target", worldSpace=True, translation=(7.0, 162.0, -3.0))
            commands.xform.reset_mock()
            module.Transform("target").match_transform("guide", position=False)
            commands.xform.assert_not_called()
            sys.modules.pop(name, None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
