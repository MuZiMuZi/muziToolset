# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from contextlib import contextmanager
from importlib import reload


import maya.cmds as cmds

try:
    from ....core import controlUtils
except ImportError:
    raise ImportError(u"无法导入 controlUtils，请确保该工具通过 MuziTools 包运行")


def main():
    #获取选择的物体
    select_list = cmds.ls(sl = True)
    if select_list :
        #创建fk关节链条
        controlUtils.Control.create_fk_ctrl(select_list)
    else:
        raise ValueError(u'{} 请选择多个物体进行创建FK控制器')