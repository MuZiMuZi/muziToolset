# coding=utf-8
"""场景边界命令替身测试：所有权、编辑、映射和重建回滚；不替代 Maya DG。"""
import importlib
import sys
import unittest
from unittest.mock import patch
import types
from rbf_sampling_test import ROOT


class SceneCommands(object):
    def __init__(self):
        self.nodes = {}
        self.connections = {}
        self.parents = {}
        self.fail_target = None
        self.fail_locator = False
        self.fail_ownership = False
        self.createNode('joint', name='joint')
        self.createNode('joint', name='helper')
        for axis in 'XYZ':
            self.addAttr('joint', longName='rotate' + axis, attributeType='doubleAngle')
        for attribute, kind in (('rotateX', 'doubleAngle'), ('translateY', 'doubleLinear'), ('scaleZ', 'double')):
            self.addAttr('helper', longName=attribute, attributeType=kind)

    def createNode(self, kind, name, parent=None):
        if self.fail_locator and kind == 'locator':
            raise RuntimeError('模拟 Locator 创建失败')
        if name in self.nodes:
            raise RuntimeError('节点重名')
        self.nodes[name] = {'kind': kind, 'attrs': {}, 'types': {}, 'keys': []}
        self.addAttr(name, longName='message', attributeType='message')
        if parent:
            self.parents[name] = parent
        return name

    def objExists(self, plug):
        node, _, attr = plug.partition('.')
        return node in self.nodes and (not attr or attr.split('[')[0] in self.nodes[node]['types'])

    def addAttr(self, node, longName, attributeType=None, dataType=None, **kwargs):
        self.nodes[node]['attrs'][longName] = kwargs.get('defaultValue', 0)
        self.nodes[node]['types'][longName] = attributeType or dataType

    def setAttr(self, plug, *values, **kwargs):
        if not values:
            return
        node, attr = plug.split('.', 1)
        self.nodes[node]['attrs'][attr] = values[0] if len(values) == 1 else values

    def getAttr(self, plug, **kwargs):
        node, attr = plug.split('.', 1)
        if kwargs.get('type'):
            return self.nodes[node]['types'][attr]
        if kwargs.get('settable'):
            return plug not in self.connections
        if kwargs.get('multiIndices'):
            result = []
            for target in self.connections:
                if target.startswith(plug + '['):
                    result.append(int(target.split('[')[1].split(']')[0]))
            return result
        return self.nodes[node]['attrs'].get(attr, 0)

    def listConnections(self, plug, source=True, destination=False, plugs=False, **kwargs):
        result = []
        for target, origin in self.connections.items():
            match = target == plug or target.startswith(plug + '[')
            if source and match:
                result.append(origin if plugs else origin.split('.')[0])
            if destination and origin == plug:
                result.append(target if plugs else target.split('.')[0])
        return result

    def connectAttr(self, source, target, **kwargs):
        if self.fail_target == target and 'Stage_' in source:
            raise RuntimeError('模拟迁移连接失败')
        if self.fail_ownership and 'Stage_' in target and '.outputMappings[' in target:
            raise RuntimeError('模拟映射所有权迁移失败')
        self.connections[target] = source

    def disconnectAttr(self, source, target):
        if self.connections.get(target) == source:
            del self.connections[target]

    def isConnected(self, source, target):
        return self.connections.get(target) == source

    def attributeQuery(self, attribute, node, **kwargs):
        return attribute in self.nodes[node]['types']

    def objectType(self, node, **kwargs):
        return self.nodes[node]['kind'] in ('joint', 'transform')

    def xform(self, *args, **kwargs):
        return [0, 0, 0]

    def parent(self, node, parent, **kwargs):
        self.parents[node] = parent
        return [node]

    def expression(self, name, string, **kwargs):
        return self.createNode('expression', name=name)

    def aliasAttr(self, *args):
        pass

    def currentUnit(self, **kwargs):
        return 'deg'

    def setKeyframe(self, node, **kwargs):
        self.nodes[node]['keys'].append((kwargs['float'], kwargs['value']))

    def setInfinity(self, *args, **kwargs):
        pass

    def rename(self, node, new):
        self.nodes[new] = self.nodes.pop(node)
        for child, parent in list(self.parents.items()):
            if parent == node and child == node + 'Shape':
                self.rename(child, new + 'Shape')
        def renamed(plug):
            parts = plug.split('.', 1)
            if parts[0] == node:
                parts[0] = new
            return '.'.join(parts)
        updated = {}
        for target, source in self.connections.items():
            updated[renamed(target)] = renamed(source)
        self.connections = updated
        if node in self.parents:
            self.parents[new] = self.parents.pop(node)
        for child, parent in list(self.parents.items()):
            if parent == node:
                self.parents[child] = new
        return new

    def delete(self, node):
        for child, parent in list(self.parents.items()):
            if parent == node:
                self.delete(child)
        self.nodes.pop(node, None)
        self.parents.pop(node, None)
        for target, source in list(self.connections.items()):
            if target.split('.')[0] == node or source.split('.')[0] == node:
                del self.connections[target]


def load_scene(commands, test):
    root = types.ModuleType('rbf_test_package')
    root.__path__ = [str(ROOT)]
    maya = types.ModuleType('maya')
    maya.cmds = commands
    core = types.ModuleType('rbf_test_package.core')
    core.__path__ = []
    common = types.ModuleType('rbf_test_package.core.common')
    scene = types.ModuleType('scene_utils')
    scene.undo_chunk = lambda function: function
    scene.get_long_name = lambda node: node
    scene.create_node = lambda kind, name: commands.createNode(kind, name=name)
    scene.ensure_nodes_available = lambda names: None
    connection = types.ModuleType('connection_utils')
    def connect(source, target, force=False):
        if commands.isConnected(source, target):
            return True
        if commands.listConnections(target) and not force:
            return False
        commands.connectAttr(source, target)
        return True
    connection.connect_plugs = connect
    connection.disconnect_plugs = commands.disconnectAttr
    common.scene_utils = scene
    common.connection_utils = connection
    common.file_utils = types.ModuleType('file_utils')
    spec = importlib.util.spec_from_file_location('rbf_test_package.core.common.name_utils', ROOT / 'core/common/name_utils.py')
    name = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(name)
    modules = {'rbf_test_package': root, 'maya': maya, 'maya.cmds': commands,
               'rbf_test_package.core': core, 'rbf_test_package.core.common': common,
               'rbf_test_package.core.common.name_utils': name}
    patcher = patch.dict(sys.modules, modules)
    patcher.start()
    test.addCleanup(patcher.stop)
    for key in list(sys.modules):
        if key.startswith('rbf_test_package.systems'):
            del sys.modules[key]
    driver = importlib.import_module('rbf_test_package.systems.rbf.driver')
    locator = importlib.import_module('rbf_test_package.systems.rbf.pose_locator')
    output = importlib.import_module('rbf_test_package.systems.rbf.output_driver')
    return driver, locator, output


class SceneContractTest(unittest.TestCase):
    def setUp(self):
        self.cmds = SceneCommands()
        self.module, self.locator, self.mapping = load_scene(self.cmds, self)
        model = self.module.RbfModel(['joint.rotateX', 'joint.rotateY', 'joint.rotateZ'])
        model.add_pose('neutral', [0, 0, 0], neutral=True)
        model.add_pose('bend', [90, 0, 0])
        self.driver = self.module.RbfDriver(model)
        self.driver.build()

    def test_locator_edit_and_invalid_edit_preserves_model(self):
        locators = self.locator.get_pose_locators(self.driver)
        self.assertEqual(set(locators), {'neutral', 'bend'})
        self.locator.write_pose_locator(self.driver, 'bend', [45, 0, 0])
        candidate = self.locator.read_pose_locators(self.driver)
        self.assertEqual(candidate.poses[1]['values'], [45, 0, 0])
        self.assertEqual(self.driver.model.poses[1]['values'], [90, 0, 0])
        self.locator.write_pose_locator(self.driver, 'bend', [0, 0, 0])
        with self.assertRaises(ValueError):
            self.locator.read_pose_locators(self.driver)
        self.assertEqual(self.driver.model.poses[1]['values'], [90, 0, 0])

    def test_mapping_types_and_repeated_rebuild_cleanup(self):
        curves = []
        for destination, kind in (('helper.rotateX', 'animCurveUA'), ('helper.translateY', 'animCurveUL'), ('helper.scaleZ', 'animCurveUU')):
            curve = self.mapping.connect_mapped_output(self.driver, 'bend', destination, 30, 5)
            curves.append(curve)
            self.assertEqual(self.cmds.nodes[curve]['kind'], kind)
            self.assertEqual(self.cmds.nodes[curve]['keys'], [(0, 5), (1, 30)])
        for radius in (0.7, 1.2):
            candidate = self.module.RbfModel.from_dict(self.driver.model.to_dict())
            candidate.radius = radius
            self.driver.rebuild(candidate)
            self.assertEqual(set(self.mapping.get_output_mappings(self.driver.output)), set(curves))
            for curve in curves:
                self.assertTrue(self.cmds.isConnected(self.driver.get_output_plug('bend'), curve + '.input'))
        self.driver.delete()
        self.assertEqual(set(self.cmds.nodes), {'joint', 'helper'})

    def test_rebuild_failure_keeps_connections_and_owned_nodes(self):
        self.driver.connect_output('bend', 'helper.scaleZ')
        original = set(self.cmds.nodes)
        self.cmds.fail_target = 'helper.scaleZ'
        candidate = self.module.RbfModel.from_dict(self.driver.model.to_dict())
        candidate.radius = 0.5
        with self.assertRaisesRegex(RuntimeError, '迁移连接失败'):
            self.driver.rebuild(candidate)
        self.assertEqual(set(self.cmds.nodes), original)
        self.assertTrue(self.cmds.isConnected(self.driver.get_output_plug('bend'), 'helper.scaleZ'))

    def test_mapping_ownership_failure_rolls_back(self):
        curve = self.mapping.connect_mapped_output(self.driver, 'bend', 'helper.rotateX', 30)
        original = set(self.cmds.nodes)
        self.cmds.fail_ownership = True
        candidate = self.module.RbfModel.from_dict(self.driver.model.to_dict())
        candidate.radius = 0.5
        with self.assertRaisesRegex(RuntimeError, '所有权迁移失败'):
            self.driver.rebuild(candidate)
        self.assertEqual(set(self.cmds.nodes), original)
        self.assertEqual(self.mapping.get_output_mappings(self.driver.output), [curve])
        self.assertTrue(self.cmds.isConnected(self.driver.get_output_plug('bend'), curve + '.input'))

    def test_refuses_existing_target_and_connected_output_removal(self):
        self.driver.connect_output('bend', 'helper.scaleZ')
        with self.assertRaises(RuntimeError):
            self.mapping.connect_mapped_output(self.driver, 'bend', 'helper.scaleZ', 2)
        self.cmds.connections['helper.rotateX'] = 'external.output'
        with self.assertRaises(RuntimeError):
            self.driver.connect_output('bend', 'helper.rotateX')
        candidate = self.module.RbfModel.from_dict(self.driver.model.to_dict())
        candidate.remove_pose('bend')
        with self.assertRaises(ValueError):
            self.driver.rebuild(candidate)

    def test_locator_failure_cleans_candidate(self):
        original = set(self.cmds.nodes)
        self.cmds.fail_locator = True
        candidate = self.module.RbfModel.from_dict(self.driver.model.to_dict())
        candidate.part = 'wrist'
        with self.assertRaises(RuntimeError):
            self.module.RbfDriver(candidate).build()
        self.assertEqual(set(self.cmds.nodes), original)


if __name__ == '__main__':
    unittest.main()
