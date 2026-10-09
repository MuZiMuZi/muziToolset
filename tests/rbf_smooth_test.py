# coding=utf-8
"""验证原 V6 方向隔离、端点保持及编译结果。"""
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from systems.rbf import RbfModel
from systems.rbf.smooth_solver import SmoothSolver, OUTPUTS
from rbf_expression_test import evaluate_compiled


class SmoothTest(unittest.TestCase):
    def test_v6_behavior(self):
        model = RbfModel(['joint.rx', 'joint.ry', 'joint.rz'], solver_type='smoothstep')
        model.add_pose('neutral', [0, 0, 0], neutral=True)
        for name in OUTPUTS:
            model.add_pose(name, [1, 1, 1])
        solver = SmoothSolver(model)
        solver.train()
        self.assertEqual(solver.evaluate([0, 0, 0]), [0] * 10)
        self.assertEqual(solver.evaluate([0, -90, 0]), [1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(solver.evaluate([90, -45, 45]), [0, 0, 0, 0, 1, 0, 0, 0, 1, 0])
        self.assertEqual(solver.evaluate([180, -180, 0]), [1, 0, 0, 0, 0, 0, 0, 0, 1, 0])
        for values in ([0, 0, 0], [35, -20, 25], [180, -180, 0], [-90, 30, -60]):
            first = solver.evaluate(values)
            second = evaluate_compiled(solver.compile('network'), values)
            for index in range(len(first)):
                self.assertAlmostEqual(first[index], second[index], places=12)


if __name__ == '__main__':
    unittest.main()
