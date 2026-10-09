# coding=utf-8
"""比较编译表达式与独立求解器；不冒充真实 Maya 求值测试。"""
import math
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from systems.rbf import RbfModel, RbfSolver
from systems.rbf.expression import compile_expression


def evaluate_compiled(source, values):
    """执行表达式的数值语句子集，检查常量、索引与输出编译。"""
    environment = {'exp': math.exp, 'sin': math.sin, 'max': max,
                   'clamp': lambda low, high, value: max(low, min(high, value))}
    for index, value in enumerate(values):
        environment['input{}'.format(index)] = value
    outputs = {}
    for line in source.splitlines():
        line = line.replace('float ', '').replace('$', '').rstrip(';')
        line = re.sub(r'network\.input(\d+)', r'input\1', line)
        left, right = line.split(' = ')
        value = eval(right, {'__builtins__': {}}, environment)
        if left.startswith('network.weight'):
            outputs[int(left.split('weight')[1])] = value
        else:
            environment[left] = value
    return list(outputs.values())


class ExpressionTest(unittest.TestCase):
    def test_parity(self):
        for periodic in (False, True):
            for normalize in (False, True):
                model = RbfModel(['a.rx', 'a.ry'], scales=[50, 90], periods=[360, 360] if periodic else [0, 0], normalize=normalize)
                model.add_pose('neutral', [0, 0], neutral=True)
                model.add_pose('up', [90, 0])
                model.add_pose('front', [0, 90])
                solver = RbfSolver(model)
                solver.train()
                source = compile_expression(solver, 'network')
                for values in ([0, 0], [90, 0], [0, 90], [45, 30], [-179, 30], [270, 300]):
                    first = solver.evaluate(values)
                    second = evaluate_compiled(source, values)
                    for index in range(len(first)):
                        self.assertAlmostEqual(first[index], second[index], places=12)


if __name__ == '__main__':
    unittest.main()
