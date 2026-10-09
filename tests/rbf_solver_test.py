# coding=utf-8
"""普通 Python RBF 数值回归；不导入 Maya。"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from systems.rbf import RbfModel, RbfSolver


class RbfSolverTest(unittest.TestCase):
    def make_model(self):
        model = RbfModel(['ctrl.rx', 'ctrl.ry'], scales=[90, 90], periods=[360, 360])
        model.add_pose('neutral', [0, 0], neutral=True)
        model.add_pose('up', [90, 0])
        model.add_pose('front', [0, 90])
        model.add_pose('diagonal', [90, 90])
        return model

    def test_interpolation(self):
        model = self.make_model()
        solver = RbfSolver(model)
        solver.train()
        for pose in model.poses:
            values = solver.evaluate(pose['values'])
            for index, name in enumerate(model.get_output_names()):
                expected = float(name == pose['name'])
                self.assertAlmostEqual(values[index], expected, places=9)

    def test_periodic_wrap(self):
        solver = RbfSolver(self.make_model())
        solver.train()
        first = solver.evaluate([179, 20])
        second = solver.evaluate([-181, 20])
        for index in range(len(first)):
            self.assertAlmostEqual(first[index], second[index], places=12)

    def test_duplicate(self):
        model = self.make_model()
        model.add_pose('duplicate', [360, 0])
        with self.assertRaises(ValueError):
            RbfSolver(model).train()

    def test_serialization_and_range(self):
        model = RbfModel.from_dict(self.make_model().to_dict())
        model.normalize = True
        solver = RbfSolver(model)
        solver.train()
        for x in range(-180, 181, 15):
            for y in range(-180, 181, 15):
                values = solver.evaluate([x, y])
                self.assertLessEqual(sum(values), 1.0 + 1e-10)
                for value in values:
                    self.assertGreaterEqual(value, 0)
                    self.assertLessEqual(value, 1)

    def test_invalid(self):
        for value in (0, -1, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                RbfModel(['a.rx'], scales=[value])


if __name__ == '__main__':
    unittest.main()
