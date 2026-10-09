# coding=utf-8
"""Gaussian RBF 插值训练与求值；不依赖 Maya、NumPy 或第三方插件。"""
import math


def squared_distance(first, second, scales, periods):
    """普通输入用欧氏距离；周期输入用圆上弦长，平滑跨越绕回点。"""
    result = 0.0
    for index, scale in enumerate(scales):
        delta = first[index] - second[index]
        period = periods[index]
        if period:
            delta = period / math.pi * math.sin(math.pi * delta / period)
        result += (delta / scale) ** 2
    return result


def solve_linear(matrix, targets):
    """部分主元 Gauss-Jordan；同时求解多个输出，病态矩阵明确报错。"""
    size = len(matrix)
    columns = len(targets[0])
    rows = []
    for index in range(size):
        rows.append(list(matrix[index]) + list(targets[index]))
    for pivot in range(size):
        best = pivot
        for index in range(pivot + 1, size):
            if abs(rows[index][pivot]) > abs(rows[best][pivot]):
                best = index
        if abs(rows[best][pivot]) < 1e-12:
            raise ValueError('RBF 矩阵病态，请增大正则项或调整半径、删除近似重复样本')
        rows[pivot], rows[best] = rows[best], rows[pivot]
        factor = rows[pivot][pivot]
        for column in range(pivot, size + columns):
            rows[pivot][column] /= factor
        for index in range(size):
            if index == pivot:
                continue
            factor = rows[index][pivot]
            for column in range(pivot, size + columns):
                rows[index][column] -= factor * rows[pivot][column]
    result = []
    for row in rows:
        result.append(row[size:])
    return result


class RbfSolver(object):
    """中立样本目标为零；每个修型样本目标为对应输出的 one-hot。"""

    def __init__(self, model):
        self.model = model
        self.coefficients = None

    def kernel(self, first, second):
        """Gaussian 核，半径作用于已按输入尺度归一化的距离。"""
        distance = squared_distance(first, second, self.model.scales, self.model.periods)
        return math.exp(-0.5 * distance / self.model.radius ** 2)

    def train(self):
        """训练全部输出；正则项非零时样本点不再严格 one-hot。"""
        self.model.validate()
        if len(self.model.poses) < 2:
            raise ValueError('至少采集中立和一个修型姿态')
        if len(self.model.poses) > 128:
            raise ValueError('当前场景表达式模式最多支持 128 个样本')
        matrix = []
        targets = []
        outputs = self.model.get_output_names()
        for index, pose in enumerate(self.model.poses):
            row = []
            for other_index, other in enumerate(self.model.poses):
                distance = squared_distance(pose['values'], other['values'], self.model.scales, self.model.periods)
                if other_index != index and distance < 1e-14:
                    raise ValueError('姿态重复：{} / {}'.format(pose['name'], other['name']))
                value = self.kernel(pose['values'], other['values'])
                if index == other_index:
                    value += self.model.regularization
                row.append(value)
            matrix.append(row)
            target = []
            for name in outputs:
                target.append(float(not pose['neutral'] and pose['name'] == name))
            targets.append(target)
        self.coefficients = solve_linear(matrix, targets)
        return self.coefficients

    def evaluate(self, values):
        """输出可选择夹到 0~1，再将大于 1 的总量归一化。"""
        self.model.validate_values(values)
        if self.coefficients is None:
            raise RuntimeError('请先训练 RBF')
        weights = [0.0] * len(self.model.get_output_names())
        for index, pose in enumerate(self.model.poses):
            basis = self.kernel(values, pose['values'])
            for column, coefficient in enumerate(self.coefficients[index]):
                weights[column] += basis * coefficient
        if self.model.clamp:
            for index, value in enumerate(weights):
                weights[index] = max(0.0, min(1.0, value))
        if self.model.normalize:
            total = sum(weights)
            if total > 1.0:
                for index in range(len(weights)):
                    weights[index] /= total
        return weights
