# coding=utf-8
"""通用模板、训练失效与 V6 参数化回归；普通 Python 可运行。"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from systems.rbf import RbfModel, RbfSolver
from systems.rbf.presets import create_adv_model, create_joint_model
from systems.rbf.smooth_solver import SmoothSolver, OUTPUTS
from systems.rbf.expression import compile_expression
from rbf_expression_test import evaluate_compiled


class CoreLifecycleTest(unittest.TestCase):
    def test_stale_coefficients_and_failed_retrain(self):
        model = RbfModel(['joint.rotateX'])
        model.add_pose('neutral', [0], neutral=True)
        model.add_pose('bend', [90])
        solver = RbfSolver(model)
        solver.train()
        model.update_pose('bend', [45])
        with self.assertRaisesRegex(RuntimeError, '重新训练'):
            solver.evaluate([45])
        with self.assertRaises(RuntimeError):
            compile_expression(solver, 'network')
        solver.train()
        self.assertAlmostEqual(solver.evaluate([45])[0], 1)
        model.add_pose('duplicate', [45])
        with self.assertRaises(ValueError):
            solver.train()
        with self.assertRaises(RuntimeError):
            solver.evaluate([45])

    def test_pose_edit_is_atomic(self):
        model = RbfModel(['j.rx'])
        model.add_pose('neutral', [0], neutral=True)
        model.add_pose('bend', [90])
        original = model.to_dict()
        with self.assertRaises(ValueError):
            model.update_pose('bend', [float('nan')])
        self.assertEqual(model.to_dict(), original)
        with self.assertRaises(ValueError):
            model.remove_pose('neutral')
        model.remove_pose('bend')
        self.assertEqual(len(model.poses), 1)

    def test_presets_and_custom_joint(self):
        for part, joint in (('arm', 'Shoulder'), ('thigh', 'Hip'), ('wrist', 'Wrist')):
            model = create_adv_model(part, 'rt')
            self.assertEqual(model.inputs[0], joint + '_R.rotateX')
        model = create_joint_model('hero:ankle', part='ankle', swing_axes=('X', 'Z'), twist_axis='Y')
        self.assertEqual(model.inputs, ['hero:ankle.rotateX', 'hero:ankle.rotateY', 'hero:ankle.rotateZ'])
        self.assertEqual(model.smooth['axes'], [0, 2, 1])
        self.assertEqual(create_adv_model('wrist').smooth['angles'], [22.5, 22.5, 45.0])

    def test_v6_grid_with_axis_remap_and_nonzero_rest(self):
        for axes in ([1, 2, 0], [0, 2, 1], [2, 0, 1]):
            model = RbfModel(['j.rx', 'j.ry', 'j.rz'], solver_type='smoothstep',
                             smooth={'axes': axes, 'signs': [-1, 1], 'angles': [45, 45, 90]})
            rest = [10, 20, -30]
            model.add_pose('neutral', rest, neutral=True)
            for name in OUTPUTS:
                model.add_pose(name, rest)
            solver = SmoothSolver(model)
            solver.train()
            source = solver.compile('network')
            for first in range(-180, 181, 30):
                for second in range(-180, 181, 30):
                    values = list(rest)
                    values[axes[0]] += first
                    values[axes[1]] += second
                    values[axes[2]] += 120
                    result = solver.evaluate(values)
                    compiled = evaluate_compiled(source, values)
                    for index, value in enumerate(result):
                        self.assertGreaterEqual(value, 0)
                        self.assertLessEqual(value, 1)
                        self.assertAlmostEqual(value, compiled[index], places=12)
                    self.assertLessEqual(sum(result[:8]), 1 + 1e-12)
                    self.assertEqual(result[-2:], [1, 0])
                    if second == 0:
                        self.assertEqual(result[2:8], [0] * 6)
            model.smooth['angles'][0] = 60
            with self.assertRaises(RuntimeError):
                solver.compile('network')


if __name__ == '__main__':
    unittest.main()
