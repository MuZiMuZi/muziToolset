# coding=utf-8
"""工具 UI 接入检查：发现、依赖完整性和控制器编排。"""

import ast
import importlib
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]


class ToolUiConnectionTest(unittest.TestCase):
    """在没有 Maya 的环境检查按钮对应的实际入口。"""

    def test_registry_and_entrypoints(self):
        """骨骼分类、执行模式和每一个 main 入口必须正确。"""
        spec = importlib.util.spec_from_file_location(
            'tool_registry', ROOT / 'tools/__init__.py')
        registry = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(registry)
        categories = registry.get_tools_by_category()
        self.assertIn('骨骼工具', categories)
        self.assertNotIn('jnt', categories)
        self.assertEqual(set(categories['骨骼工具']), {'jnt_tool', 'jnt_resamp_tool'})
        count = 0
        for tools in categories.values():
            for runner in tools.values():
                relative = runner.full_module_name.split('.')[1:]
                path = ROOT / 'tools' / Path(*relative).with_suffix('.py')
                tree = ast.parse(path.read_text(encoding='utf-8'))
                functions = set()
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef):
                        functions.add(node.name)
                self.assertIn('main', functions, str(path))
                count += 1
        self.assertEqual(count, 20)
        self.assertEqual(categories['基础工具']['snap_tool'].tool_mode, 'action')
        self.assertEqual(categories['控制器工具']['create_fk_ctrl_tool'].tool_mode, 'action')

    def test_runtime_dependencies(self):
        """每个相对导入及模块调用都必须能在当前工程找到。"""
        for folder in ('app', 'ui', 'tools', 'core', 'systems'):
            for path in (ROOT / folder).rglob('*.py'):
                tree = ast.parse(path.read_text(encoding='utf-8'))
                imports = {}
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.assertFalse(alias.name.startswith('pymel'), str(path))
                    if not isinstance(node, ast.ImportFrom):
                        continue
                    self.assertFalse((node.module or '').startswith('legacy_reference'), str(path))
                    if not node.level:
                        continue
                    base = path.parent
                    for unused in range(node.level - 1):
                        base = base.parent
                    if node.module:
                        base = base.joinpath(*node.module.split('.'))
                    for alias in node.names:
                        candidate = base / (alias.name + '.py')
                        if candidate.is_file():
                            imports[alias.asname or alias.name] = candidate
                        else:
                            self.assertTrue(base.with_suffix('.py').exists() or (base / '__init__.py').exists() or (base / alias.name / '__init__.py').exists(), '{}: {}'.format(path, alias.name))
                for node in ast.walk(tree):
                    if not isinstance(node, ast.Attribute) or not isinstance(node.value, ast.Name):
                        continue
                    dependency = imports.get(node.value.id)
                    if dependency is None:
                        continue
                    names = set()
                    for member in ast.parse(dependency.read_text(encoding='utf-8')).body:
                        if isinstance(member, (ast.FunctionDef, ast.ClassDef)):
                            names.add(member.name)
                        elif isinstance(member, ast.Assign):
                            for target in member.targets:
                                if isinstance(target, ast.Name):
                                    names.add(target.id)
                        elif isinstance(member, ast.ImportFrom):
                            for alias in member.names:
                                names.add(alias.asname or alias.name)
                    self.assertIn(node.attr, names, '{}: {}.{}'.format(path, node.value.id, node.attr))

    def load_builder(self):
        """隔离 Maya 后加载控制器编排，测试实际 FK 连接流程。"""
        modules = {}
        for name in ('maya', 'maya.cmds', 'testpkg', 'testpkg.core',
                     'testpkg.core.rigging', 'testpkg.core.rigging.ctrl_utils',
                     'testpkg.core.rigging.constraint_utils', 'testpkg.core.common',
                     'testpkg.core.common.hierarchy_utils', 'testpkg.core.common.scene_utils',
                     'testpkg.systems', 'testpkg.systems.components'):
            modules[name] = types.ModuleType(name)
        modules['testpkg.core.rigging.ctrl_utils'].Ctrl = MagicMock()
        name = 'testpkg.systems.components.controller_builder'
        spec = importlib.util.spec_from_file_location(
            name, ROOT / 'systems/components/controller_builder.py')
        builder = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, modules):
            spec.loader.exec_module(builder)
        builder.scene_utils = MagicMock()
        builder.constraint_utils = MagicMock()
        builder.cmds = MagicMock()
        builder.cmds.objExists.side_effect = lambda node: node.startswith('target')
        return builder

    def test_fk_parenting_constraints_and_undo(self):
        """FK 必须使用 Output 挂接和约束，并且异常时关闭 Undo Chunk。"""
        builder = self.load_builder()
        def create(**kwargs):
            return {'ctrl_node': kwargs['name'], 'output_node': kwargs['name'] + '_output'}
        with patch.object(builder, 'create_ctrl', side_effect=create) as create_mock:
            results = builder.create_fk_ctrl(['target1', 'target2'], ['ctrl1', 'ctrl2'])
        self.assertEqual(len(results), 2)
        self.assertIsNone(create_mock.call_args_list[0].kwargs['parent_node'])
        self.assertEqual(create_mock.call_args_list[1].kwargs['parent_node'], 'ctrl1_output')
        builder.constraint_utils.create_constraint.assert_any_call(
            driver_objects='ctrl1_output', driven_object='target1',
            constraint_type='parentConstraint', maintain_offset=True)
        builder.scene_utils.close_undo_chunk.assert_called_once_with()
        with patch.object(builder, 'create_ctrl', side_effect=RuntimeError('failed')):
            with self.assertRaises(RuntimeError):
                builder.create_fk_ctrl(['target1'], ['ctrl1'])
        self.assertEqual(builder.scene_utils.close_undo_chunk.call_count, 2)

    def test_fk_conflicts_rejected_before_scene_changes(self):
        """数量错误和重复名称不得触发任何构建。"""
        builder = self.load_builder()
        with patch.object(builder, 'create_ctrl') as create_mock:
            with self.assertRaises(ValueError):
                builder.create_fk_ctrl(['target1'], [])
            with self.assertRaises(ValueError):
                builder.create_fk_ctrl(['target1', 'target2'], ['same', 'same'])
            create_mock.assert_not_called()
            builder.scene_utils.open_undo_chunk.assert_not_called()


if __name__ == '__main__':
    unittest.main()
