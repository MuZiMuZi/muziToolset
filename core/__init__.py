# coding=utf-8
u"""
MuziTools Core
==============

正式 Maya 底层能力层。

Core 的定位
-----------
``core/`` 不是“所有代码都可以往里放”的公共目录，而是整个 MuziTools 的底层能力层。
一个模块通常对应一个清晰的 Maya / Python 领域，上层 Tool 和 System 通过组合 Core API 完成完整工作流。

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
        原 animation_io_utils.py 已合并到本模块。

Scene / File：
    scene_utils.py
        Undo、节点、Selection、Object Set、Callback、Scene Open / Import / Reference、FBX Export。
        原 scene_io_utils.py 已合并到本模块。

    file_utils.py
        纯 Python Path、Directory、JSON、文件扫描；不负责 Maya Scene。

Transform / DG：
    transform_utils.py
        World Position / Matrix / Distance / Relative Move。

    matrix_utils.py
        MMatrix、multMatrix、offsetParentMatrix Matrix Constraint。

    connection_utils.py
        DG Plug 查询、连接、断开、批量复制连接。

    constraint_utils.py
        Maya 原生 Parent / Point / Orient / Scale / Aim Constraint。

DAG / Attribute / Naming：
    attrUtils.py
        Attribute、Message、String Config、Transform Limits；旧文件名暂时保留用于兼容。

    hierarchyUtils.py
        DAG Parent、Extra Group、Child Query、基础 Group；旧文件名暂时保留用于兼容。

    jointUtils.py
        Joint、JointCurve、JointChain；Curve 查询已统一复用 curve_utils。

    nameUtils.py
        五段式 Rig 标准名称、解析、Mirror Name、Unique Index、Duplicate DAG Name。

    rename_utils.py
        面向批量操作的 Prefix / Suffix / Search Replace / Auto Number / Pattern Rename。

Geometry：
    curve_utils.py
        NURBS Curve Query、Arc Length Sample、Parameter Conversion、Curve Attachment。

    surface_utils.py
        NURBS Surface / Follicle。

    mesh_utils.py
        Mesh / Model 的轻量底层操作。

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

颗粒度原则
----------
当前 Core 采用“一个领域一个模块”，而不是：

    一个函数 -> 一个 py 文件

也不是重新回到：

    pipelineUtils.py -> 所有功能

例如：
    Animation 操作 + Animation JSON IO -> animation_utils.py
    Scene 基础 + Scene IO             -> scene_utils.py

但以下领域继续保持独立：
    Matrix != Constraint
    Connection != Constraint
    Curve != Surface
    Model Check != Scene Clean
    Name Semantic != Batch Rename

为什么部分文件仍然是 CamelCase
-------------------------------
``attrUtils.py / hierarchyUtils.py / jointUtils.py / nameUtils.py`` 是早期正式 API 的文件名，仓库中已有大量
Import 可能依赖它们。本轮先完成内部架构、注释和重复逻辑收口，不为了文件名统一制造破坏性迁移。
后续如需要统一 snake_case，应采用“新入口 + 兼容转发 + 分阶段删除”的迁移方式。

Import 原则
----------
为了避免 ``import muziToolset.core`` 时一次性加载 Maya API、插件或其它较重模块，
本文件不主动 Import 所有子模块。

推荐：

    from muziToolset.core import curve_utils
    from muziToolset.core import matrix_utils
    from muziToolset.core.attrUtils import Attr

旧 Pipeline
----------
旧 ``pipelineUtils.py`` 已完成职责迁移并删除。
Face / Controller / Body / Hair 等完整 Rig Workflow 必须进入 ``systems/``，不能重新堆回 Core。
"""

from __future__ import print_function


# 不主动 import 子模块，避免 package import 产生额外 Maya 副作用。
__all__ = []
