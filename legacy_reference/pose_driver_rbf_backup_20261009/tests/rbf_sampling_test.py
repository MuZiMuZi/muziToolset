# coding=utf-8
"""用隔离的命令替身验证自动采样恢复；真实 Maya 验证另有脚本。"""
import importlib
import math
import pathlib
import sys
import types
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]


class FakeCommands(object):
    def __init__(self, radians=False, failure=False):
        self.rotation = [0.1, 0.2, 0.3] if radians else [10.0, 20.0, 30.0]
        self.auto_key = True
        self.radians = radians
        self.failure = failure
        self.read_count = 0

    def objExists(self, plug):
        return True

    def getAttr(self, plug, **kwargs):
        if kwargs.get('type'):
            return 'doubleAngle'
        if kwargs.get('settable'):
            return True
        if plug.startswith('joint.'):
            self.read_count += 1
            if self.failure and self.read_count == 7:
                raise RuntimeError('模拟采样中断')
        return self.rotation['XYZ'.index(plug[-1])]

    def currentUnit(self, **kwargs):
        return 'rad' if self.radians else 'deg'

    def listConnections(self, *args, **kwargs):
        return []

    def transformLimits(self, *args, **kwargs):
        return [False, False]

    def setAttr(self, plug, value):
        self.rotation['XYZ'.index(plug[-1])] = value

    def autoKeyframe(self, **kwargs):
        if kwargs.get('query'):
            return self.auto_key
        self.auto_key = kwargs['state']


def load_sampling(commands):
    """提供 Maya 命令和项目 Core 边界，导入真实业务采样实现。"""
    root = types.ModuleType('rbf_test_package')
    root.__path__ = [str(ROOT)]
    maya = types.ModuleType('maya')
    maya.cmds = commands
    core = types.ModuleType('rbf_test_package.core')
    core.__path__ = []
    common = types.ModuleType('rbf_test_package.core.common')
    scene = types.ModuleType('rbf_test_package.core.common.scene_utils')
    scene.undo_chunk = lambda function: function
    scene.get_long_name = lambda node: node
    common.scene_utils = scene
    common.connection_utils = types.ModuleType('connection_utils')
    common.file_utils = types.ModuleType('file_utils')
    name = types.ModuleType('rbf_test_package.core.common.name_utils')
    name.Name = object
    modules = {'rbf_test_package': root, 'maya': maya, 'maya.cmds': commands,
               'rbf_test_package.core': core, 'rbf_test_package.core.common': common,
               'rbf_test_package.core.common.name_utils': name}
    with patch.dict(sys.modules, modules):
        for key in list(sys.modules):
            if key.startswith('rbf_test_package.systems'):
                del sys.modules[key]
        return importlib.import_module('rbf_test_package.systems.rbf.sampling')


class SamplingTest(unittest.TestCase):
    def test_auto_sample_restores(self):
        for radians in (False, True):
            commands = FakeCommands(radians=radians)
            sampling = load_sampling(commands)
            original = list(commands.rotation)
            model = sampling.RbfModel(['joint.rotateX', 'joint.rotateY', 'joint.rotateZ'])
            result = sampling.sample_controller(model, 'ctrl')
            self.assertEqual(len(result.poses), 11)
            self.assertEqual(model.poses, [])
            self.assertEqual(commands.rotation, original)
            self.assertTrue(commands.auto_key)
            expected = original[1] + (math.radians(-90) if radians else -90)
            expected = math.degrees(expected) if radians else expected
            self.assertAlmostEqual(result.poses[1]['values'][1], expected)

    def test_failure_restores(self):
        commands = FakeCommands(failure=True)
        sampling = load_sampling(commands)
        original = list(commands.rotation)
        model = sampling.RbfModel(['joint.rotateX', 'joint.rotateY', 'joint.rotateZ'])
        with self.assertRaisesRegex(RuntimeError, '模拟采样中断'):
            sampling.sample_controller(model, 'ctrl')
        self.assertEqual(commands.rotation, original)
        self.assertTrue(commands.auto_key)
        self.assertEqual(model.poses, [])


if __name__ == '__main__':
    unittest.main()
