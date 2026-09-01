# coding=utf-8
u"""
MuziTools Core
==============

正式 Maya 底层能力层。

Core 的定位
-----------
``core/`` 不是“所有代码都可以往里放”的公共目录，而是整个 MuziTools 的底层能力层。
一个模块对应一个清晰的 Maya / Python 领域，上层 Tool 和 System 通过组合 Core API 完成完整工作流。

依赖规则
--------
允许：
    core -> maya.cmds
    core -> maya.api.OpenMaya
    core -> Python 标准库
    core -> 其它明确的 core 模块

禁止：
    core -> app
    core -> ui
    core -> tools
    core -> systems
    core -> legacy_reference
    core -> PyMel

当前正式模块
------------
Animation：
    animation_utils.py
        AnimCurve 查询 / 清理、Transform Reset、动画数据收集、Animation JSON 导入导出。

Scene / File：
    scene_utils.py
        Undo、Node、Selection 查询、Object Set、Callback、Scene Open / Import / Reference。

    file_utils.py
        纯 Python Path、Directory、JSON、文件扫描；不负责 Maya Scene。

    export_utils.py
        显式对象列表的文件格式导出；当前包含 FBX Export。

Transform / Math / DG：
    transform_utils.py
        Transform / Joint 的 World Translation、Rotation、Matrix 和 Relative Move。

    math_utils.py
        与 Maya Scene 无关的纯 Python Point / Vector 数学。

    matrix_utils.py
        MMatrix 数据、矩阵计算、multMatrix / offsetParentMatrix 通用 Matrix Network。

    connection_utils.py
        DG Plug 输入 / 输出查询、单条连接 / 断开和显式 Plug Pair 批处理。

    constraint_utils.py
        Maya 原生 Parent / Point / Orient / Scale / Aim Constraint。

DAG / Attribute / Config / Naming：
    attr_utils.py
        单节点 Attribute 创建、状态、Value、Message 与 Transform Limits。
        通用 Plug Connection 统一由 connection_utils 负责；Channel Box UI 不属于 Core Attribute。

    config_utils.py
        通用 Network Config Node 生命周期、Message 引用和 Value 配置封装。
        Face / Body / Hand 等 System 应复用该模块，不重复实现 Config CRUD。

    hierarchy_utils.py
        DAG Parent / Child / Descendant、Ensure Group 和 Parent Group 插入。
        所有 Query 先解析唯一 DAG Long Path；正式 API 只使用模块函数，不保留无状态包装类。

    joint_utils.py
        单个 Maya Joint 的 Joint Orient、Radius、Local Axis、Scale Compensate、Orient 和 Label。
        通用 Transform / Hierarchy / Rename 能力不在 Joint 类重复包装。

    name_utils.py
        五段式 Rig 标准名称、解析、Mirror Name、Unique Index、Duplicate DAG Name。

    rename_utils.py
        DAG Short Name、Prefix / Suffix / Search Replace / Auto Number / Pattern Rename。

Geometry：
    curve_utils.py
        NURBS Curve Query、Arc Length Sample、Parameter Conversion、Curve Attachment。

    surface_utils.py
        NURBS Surface / Follicle。

    mesh_utils.py
        Mesh / Model 的轻量底层操作，包括模型 Transform 验证、复制和删除。

Deformer / Controller Shape：
    skin_utils.py
        SkinCluster、Influence、Weight Copy、XML / JSON Weight IO。

    blendshape_utils.py
        BlendShape Target、Alias、Corrective / Invert Shape。

    control_shape_utils.py
        Controller Curve Shape JSON、Shape CV、Color、Radius、Rotate / Scale / Mirror。

Scene Quality：
    model_check_utils.py
        Non-Manifold、Lamina、重名、History、Transform、Locked Normal 检查与安全修复。

    scene_clean_utils.py
        Empty Group、History、Freeze、Attribute、Pivot、Unknown Node 安全清理。

Utility：
    snap_utils.py
        Object / Component 平均位置与轻量 Rotation Snap。

Core API 原则
------------
有状态对象，例如 ``Joint(joint)``、``Attr(node)``：
    在 __init__() 建立并验证对象不变量，普通实例方法不重复做同一份节点校验。

无状态 Utils，例如 ``transform_utils.get_world_translation(node)``：
    每次收到外部 Maya Node / Plug 参数时进行必要校验。

通用操作只保留一个正式入口：
    Scene / Node       -> scene_utils
    File / Path        -> file_utils
    File Export        -> export_utils
    Transform 数值     -> transform_utils
    DAG Hierarchy      -> hierarchy_utils
    Attribute          -> attr_utils.Attr
    Plug Connection    -> connection_utils
    Rename             -> rename_utils
    Joint 专属属性     -> joint_utils.Joint
    Matrix 计算/网络   -> matrix_utils
    纯数学             -> math_utils

复杂 Face / Body / Controller Rig Graph 进入 ``systems/``，不能重新堆回 Core。

Import 原则
-----------
为了避免 ``import muziToolset.core`` 时一次性加载 Maya API、插件或较重模块，
本文件不主动 Import 所有子模块。
"""

from __future__ import print_function


__all__ = []
