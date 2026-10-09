# coding=utf-8
"""验证反算 Target 的事务恢复、真实索引与复制 Alias 整理。"""

import copy
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class FakeCommands(object):
    """提供可回滚场景状态，不模拟 Maya 的反算数学。"""

    def __init__(self):
        self.nodes = {'ctrl': 'transform', 'bs': 'blendShape',
                      'base': 'transform', 'baseShape': 'mesh',
                      'sculpt': 'transform', 'sculptShape': 'mesh'}
        self.parents = {'baseShape': 'base', 'sculptShape': 'sculpt'}
        self.values = {'bs.envelope': 0.35}
        for index, channel in enumerate(('tx', 'ty', 'tz', 'rx', 'ry', 'rz')):
            self.values['ctrl.' + channel] = index + 1.5
        self.aliases = {2: 'lf_smile_Copy', 9: 'middle'}
        self.selection = ['sculpt', 'base']
        self.connections = set()
        self.locked = set()
        self.failure = None
        self.topology_mismatch = False
        self.geometries = ['baseShape']
        self.undo_enabled = True
        self.before_chunk = None
        self.closed = 0
        self.undone = 0
        self.calls = []
        self.alias_write_count = 0

    def ls(self, node=None, **kwargs):
        if kwargs.get('selection'):
            return list(self.selection)
        return [node] if node in self.nodes else []

    def objExists(self, node):
        if node in self.nodes or node in self.values:
            return True
        if node.startswith('bs.'):
            return node[3:] in self.aliases.values()
        return False

    def nodeType(self, node):
        return self.nodes[node]

    def objectType(self, node, **kwargs):
        return self.nodes.get(node) in ('transform', 'joint')

    def listRelatives(self, node, **kwargs):
        if kwargs.get('parent'):
            return [self.parents[node]] if node in self.parents else []
        children = []
        for shape, parent in self.parents.items():
            if parent == node:
                children.append(shape)
        return children

    def polyEvaluate(self, node, **kwargs):
        return 4 if kwargs.get('vertex') or kwargs.get('edge') else 1

    def polyInfo(self, node, **kwargs):
        if self.topology_mismatch and node == 'sculptShape':
            return ['FACE 0: 0 2 1 3']
        return ['FACE 0: 0 1 2 3']

    def getAttr(self, plug, **kwargs):
        if kwargs.get('settable'):
            return plug not in self.locked
        if kwargs.get('multiIndices'):
            return [9, 2]
        return self.values[plug]

    def listConnections(self, plug, **kwargs):
        return ['driver.output'] if plug in self.connections else []

    def setAttr(self, plug, value):
        if self.failure == 'restore' and plug == 'ctrl.tx' and value == 1.5:
            raise RuntimeError('restore failed')
        self.values[plug] = value
        self.calls.append(('set', plug, value))

    def duplicate(self, node, **kwargs):
        if self.failure == 'duplicate':
            raise RuntimeError('duplicate failed')
        self.nodes['snapshot'] = 'transform'
        self.nodes['snapshotShape'] = 'mesh'
        self.parents['snapshotShape'] = 'snapshot'
        return ['snapshot']

    def invertShape(self, base, snapshot):
        self.calls.append(('invert', base, snapshot, self.values['bs.envelope'], self.values['ctrl.tx']))
        if self.failure == 'invert':
            raise RuntimeError('invert failed')
        self.nodes['inverted'] = 'transform'
        self.nodes['invertedShape'] = 'mesh'
        self.parents['invertedShape'] = 'inverted'
        return ['inverted']

    def blendShape(self, node, **kwargs):
        if kwargs.get('query'):
            return self.geometries
        self.calls.append(('add', kwargs['target'], self.values['ctrl.tx']))
        index = kwargs['target'][1]
        self.values['bs.weight[{}]'.format(index)] = 0
        self.aliases[index] = 'inverted'
        if self.failure == 'add':
            raise RuntimeError('add failed after partial write')

    def aliasAttr(self, name, plug=None, **kwargs):
        if kwargs.get('query'):
            result = []
            for index, alias in self.aliases.items():
                result.extend([alias, 'weight[{}]'.format(index)])
            return result
        self.alias_write_count += 1
        if self.failure == 'alias' and self.alias_write_count == 2:
            raise RuntimeError('alias failed')
        index = int(plug.split('[')[1].split(']')[0])
        self.aliases[index] = name

    def delete(self, node, **kwargs):
        if kwargs.get('constructionHistory'):
            self.calls.append(('bake', node))
            return
        self.nodes.pop(node, None)
        for shape, parent in list(self.parents.items()):
            if parent == node:
                self.nodes.pop(shape, None)
                self.parents.pop(shape)

    def select(self, selection=None, **kwargs):
        self.selection = [] if kwargs.get('clear') else list(selection)

    def undoInfo(self, **kwargs):
        if kwargs.get('query'):
            return self.undo_enabled
        if kwargs.get('openChunk'):
            self.before_chunk = copy.deepcopy((self.nodes, self.parents, self.values, self.aliases, self.selection))
        if kwargs.get('closeChunk'):
            self.closed += 1

    def undo(self):
        self.undone += 1
        self.nodes, self.parents, self.values, self.aliases, self.selection = copy.deepcopy(self.before_chunk)


def load_modules(commands):
    """载入真实 Core 函数，只有 Maya 命令和公共场景包装是测试桩。"""
    modules = {}
    for name in ('maya', 'maya.cmds', 'fixture', 'fixture.core',
                 'fixture.core.common', 'fixture.core.deformation'):
        modules[name] = types.ModuleType(name)
    modules['maya.cmds'] = commands
    modules['maya'].cmds = commands
    rename = types.ModuleType('fixture.core.common.rename_utils')
    rename.get_sanitized_short_name = lambda node: node.split('|')[-1]
    scene = types.ModuleType('fixture.core.common.scene_utils')
    scene.open_undo_chunk = lambda name: commands.undoInfo(openChunk=True, chunkName=name)
    scene.close_undo_chunk = lambda: commands.undoInfo(closeChunk=True)
    modules[rename.__name__] = rename
    modules[scene.__name__] = scene
    result = []
    with patch.dict(sys.modules, modules):
        for short_name in ('blendshape_utils', 'corrective_target', 'target_alias_utils'):
            name = 'fixture.core.deformation.' + short_name
            spec = importlib.util.spec_from_file_location(name, ROOT / 'core/deformation' / (short_name + '.py'))
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            result.append(module)
        for module in result:
            sys.modules.pop(module.__name__, None)
    return result


class CorrectiveTargetTests(unittest.TestCase):
    def setUp(self):
        self.commands = FakeCommands()
        self.bs, self.corrective, self.alias = load_modules(self.commands)
        self.initial = copy.deepcopy((self.commands.nodes, self.commands.values, self.commands.aliases, self.commands.selection))

    def add(self, name='smile_fix'):
        return self.corrective.add_inverted_target('ctrl', 'bs', 'sculpt', 'base', name)

    def test_success_restores_pose_envelope_selection_and_cleans_meshes(self):
        result = self.add()
        self.assertEqual(result, {'alias': 'smile_fix', 'index': 10, 'plug': 'bs.weight[10]'})
        self.assertEqual(self.commands.nodes, self.initial[0])
        for plug, value in self.initial[1].items():
            self.assertEqual(self.commands.values[plug], value)
        self.assertEqual(self.commands.values['bs.weight[10]'], 0)
        self.assertEqual(self.commands.selection, self.initial[3])
        self.assertIn(('invert', 'base', 'snapshot', 0, 1.5), self.commands.calls)
        self.assertIn(('add', ('base', 10, 'inverted', 1.0), 0), self.commands.calls)
        self.assertLess(self.commands.calls.index(('bake', 'inverted')), self.commands.calls.index(('set', 'ctrl.tx', 0)))
        self.assertEqual(self.commands.closed, 1)

    def test_failure_at_each_stage_rolls_back_only_current_operation(self):
        for stage in ('invert', 'add', 'restore'):
            with self.subTest(stage=stage):
                self.setUp()
                self.commands.failure = stage
                with self.assertRaises(RuntimeError):
                    self.add()
                self.assertEqual(self.commands.nodes, self.initial[0])
                self.assertEqual(self.commands.values, self.initial[1])
                self.assertEqual(self.commands.aliases, self.initial[2])
                self.assertEqual(self.commands.selection, self.initial[3])
                self.assertEqual(self.commands.undone, 1)
                self.assertEqual(self.commands.closed, 1)

    def test_duplicate_failure_never_undoes_previous_user_action(self):
        self.commands.failure = 'duplicate'
        with self.assertRaises(RuntimeError):
            self.add()
        self.assertEqual(self.commands.undone, 0)

    def test_locked_or_connected_channels_stop_before_mutation(self):
        for container in (self.commands.locked, self.commands.connections):
            container.add('ctrl.tx')
            with self.assertRaises(ValueError):
                self.add()
            self.assertIsNone(self.commands.before_chunk)
            container.clear()

    def test_topology_same_count_but_different_indices_is_rejected(self):
        self.commands.topology_mismatch = True
        with self.assertRaises(ValueError):
            self.add()
        self.assertIsNone(self.commands.before_chunk)

    def test_invalid_base_or_duplicate_alias_is_rejected(self):
        self.commands.geometries = ['sculptShape']
        with self.assertRaises(ValueError):
            self.add()
        self.commands.geometries = ['baseShape']
        with self.assertRaises(ValueError):
            self.add('middle')
        self.assertIsNone(self.commands.before_chunk)

    def test_empty_name_is_unique_and_zero_envelope_stays_zero(self):
        self.commands.aliases[9] = 'sculpt_invert'
        self.commands.values['bs.envelope'] = 0
        result = self.add('')
        self.assertEqual(result['alias'], 'sculpt_invert_001')
        self.assertEqual(self.commands.values['bs.envelope'], 0)

    def test_undo_disabled_is_rejected_before_mutation(self):
        self.commands.undo_enabled = False
        with self.assertRaises(RuntimeError):
            self.add()
        self.assertIsNone(self.commands.before_chunk)

    def test_alias_rename_uses_sparse_indices_and_only_outer_tokens(self):
        self.commands.aliases = {9: 'lf_smile_lf_Copier_Copy', 2: 'middle'}
        result = self.alias.rename_mirrored_targets('bs')
        self.assertEqual(result[0]['index'], 9)
        self.assertEqual(self.commands.aliases, {9: 'rt_smile_lf_Copier', 2: 'middle'})
        self.assertEqual(self.commands.selection, self.initial[3])

    def test_alias_conflict_is_atomic(self):
        self.commands.aliases = {2: 'lf_smile_Copy', 9: 'rt_smile'}
        with self.assertRaises(ValueError):
            self.alias.rename_mirrored_targets('bs')
        self.assertEqual(self.commands.alias_write_count, 0)

    def test_alias_failure_restores_prior_changes(self):
        self.commands.aliases = {2: 'lf_smile_Copy', 9: 'lf_frown_Copy'}
        original = dict(self.commands.aliases)
        self.commands.failure = 'alias'
        with self.assertRaises(RuntimeError):
            self.alias.rename_mirrored_targets('bs')
        self.assertEqual(self.commands.aliases, original)
        self.assertEqual(self.commands.closed, 1)


if __name__ == '__main__':
    unittest.main()
