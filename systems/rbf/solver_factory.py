# coding=utf-8
"""按配置选择真正 RBF 或旧版 Smoothstep，调用方不重复判断。"""
from .solver import RbfSolver
from .smooth_solver import SmoothSolver


def create_solver(model):
    """返回具有 train、evaluate 接口的求解器。"""
    if model.solver_type == 'smoothstep':
        return SmoothSolver(model)
    return RbfSolver(model)
