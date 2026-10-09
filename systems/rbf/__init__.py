# coding=utf-8
"""通用 RBF 系统；数据和数学模块可在 Maya 外独立使用。"""
from .model import RbfModel
from .solver import RbfSolver

__all__ = ['RbfModel', 'RbfSolver']
