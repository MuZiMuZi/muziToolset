# coding=utf-8
"""按配置选择真正 RBF 或旧版 Smoothstep，调用方不重复判断。"""
from .solver import RbfSolver
from .smooth_solver import SmoothSolver


def create_solver(model):
    """返回具有 train、evaluate 接口的求解器。

    Args:
        model (RbfModel):
            已通过数据验证的姿态配置；场景接口构建前检查输入连接。

    Returns:
        RbfSolver | SmoothSolver: 根据 solver_type 选择的计算对象。
    """
    if model.solver_type == 'smoothstep':
        return SmoothSolver(model)
    return RbfSolver(model)
