# coding=utf-8
u"""
MuziTools Core Package
======================

Core 只提供与具体 Rig 业务无关的 Maya / Python 通用基础能力。

模块职责：

    rename_utils.py
        Maya DAG Short Name、外部名称 Token、Rename 等通用节点改名操作。
        Rig Naming Convention 不属于 Core，统一由 systems.rig_base.RigBase 负责。

    attr_utils.py
        Attribute 创建、锁定、隐藏、读取和写入。

    hierarchy_utils.py
        DAG Parent / Child / Group 层级操作。

    joint_utils.py
        单个 Maya Joint 创建、属性和显示操作，以及全局 Joint Display Scale。

    joint_chain_utils.py
        多 Joint / Joint Chain、Maya Item -> Joint、Curve CV -> Joint 的参数化通用算法。
        不读取当前 Selection，不包含 Tool Warning / UI 语义。

    transform_utils.py
        Transform 校验、世界矩阵、位置和旋转操作。

    scene_utils.py
        Node 创建、校验、Scene Node Type 查询、Object Set、Scene Import、Undo Chunk 等场景能力。

    connection_utils.py
        DG Plug 查询、连接和断开。

    constraint_utils.py
        Maya Constraint 创建。

    matrix_utils.py
        Matrix 驱动和 offsetParentMatrix 等矩阵能力。

    curve_utils.py
        Curve 查询、采样、Attachment 和基础 Curve 创建。

    control_shape_utils.py
        Controller Shape 数据读写、缩放、旋转和颜色。

    math_utils.py
        与 Maya Scene 无关的 Point / Vector 基础数学。

    mesh_utils.py
        Mesh Model 校验、复制和删除。

    skin_utils.py
        SkinCluster 查询和 Skin 基础能力。

    config_utils.py
        Network Config Node 和 Message / Value 持久化。

设计边界：
    - Core 不知道 Face / Body / Teeth / Jaw 等业务概念；
    - Rig Name 由 systems.rig_base 负责；
    - Module Lifecycle 由 systems.module_base 负责；
    - Controller Workflow 由 systems.ctrl_base 负责；
    - Selection / Warning / PySide UI 语义优先留在 tools / ui；
    - 新功能先检查现有 Core 是否已经可以组合完成，避免重复实现。
"""

from __future__ import print_function


__all__ = []
