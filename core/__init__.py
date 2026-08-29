# coding=utf-8
u"""
Muzi Rigging Core
=================

正式 Maya 底层功能层。

规则：
    - Core 不依赖 app / ui / tools / systems；
    - 场景操作优先 maya.cmds，必要时使用 maya.api.OpenMaya；
    - 不新增 PyMel 依赖；
    - 不在 Core 中创建 PySide 工具窗口；
    - 历史实现位于 legacy_reference/core，不从正式包直接调用。

当前主要模块：

基础节点：
    attrUtils
    hierarchyUtils
    jointUtils
    nameUtils
    scene_utils
    transform_utils
    connection_utils
    matrix_utils

Rig / Scene：
    animation_utils
    constraint_utils
    curve_utils
    surface_utils
    snap_utils

文件 / Scene IO：
    file_utils
    scene_io_utils

Geometry / Deformer：
    mesh_utils
    skin_utils
    blendshape_utils
    control_shape_utils

工具支持：
    rename_utils
    scene_clean_utils
    model_check_utils

旧 pipelineUtils 的通用职责会逐步拆入以上模块；
Face、Controller、Hair 等完整 Rig Workflow 不允许重新塞回 Core。

为了避免 import muziToolset.core 时产生额外 Maya 副作用，
本文件不主动 import 各个子模块。调用方按实际需要显式导入即可。
"""

from __future__ import print_function


__all__ = []
