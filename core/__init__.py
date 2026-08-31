# coding=utf-8
u"""
Muzi Toolset Core
=================

PyMEL-first 架构中的通用算法层。

Core 不再包装 Maya 已经提供得很清楚的 Node 能力。
例如 Joint、Transform、Attribute、Parent、Connection 等基础操作，
正式代码优先直接使用 PyMEL PyNode / Attribute API。

只有当一段逻辑具有明确的项目语义、可复用算法或数据处理价值时，
才应该进入 core/，例如：

    - Rig Naming 规则；
    - Matrix / Math 算法；
    - Geometry 采样算法；
    - Rig 数据序列化；
    - 与具体 Face / Body Component 无关的通用计算。

依赖边界：

    core -> pymel.core
    core -> maya.api.OpenMaya
    core -> Python 标准库
    core -> 其它 core 模块

禁止：

    core -> systems
    core -> tools
    core -> legacy_reference

这里不保留旧接口兼容层。
"""

from __future__ import print_function

__all__ = []
