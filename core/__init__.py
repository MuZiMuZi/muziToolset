# coding=utf-8
u"""
Muzi Rigging Core
=================

正式 Maya 底层功能层。

规则：
    - Core 不依赖 app / ui / tools / systems；
    - 场景操作优先 maya.cmds；
    - 不新增 PyMel 依赖；
    - 不在 Core 中创建 PySide 工具窗口；
    - 历史实现位于 legacy_reference/core，不从正式包直接调用。

当前主要模块：
    attrUtils
    hierarchyUtils
    jointUtils
    nameUtils
    control_shape_utils
    mesh_utils
    rename_utils
    snap_utils
    skin_utils
    blendshape_utils
    scene_clean_utils
    model_check_utils

为了避免 import muzi_rigging.core 时产生额外 Maya 副作用，
本文件不主动 import 各个子模块。调用方按实际需要显式导入即可。
"""

from __future__ import print_function


__all__ = []
