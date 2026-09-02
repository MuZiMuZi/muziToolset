# coding=utf-8
u"""
Teeth Build API
===============

Face Rig Step 03 中 Teeth Component 的稳定公共构建入口。

上层 UI / Tool 不直接依赖 TeethComponent 内部的分阶段调用顺序，
统一通过 build_teeth() 完成：

    Collect Inputs
        ↓
    Prepare Data
        ↓
    Create Joint
        ↓
    Create Controller
        ↓
    Create Connection
        ↓
    Finalize

这样以后 Teeth Component 内部增加新的构建阶段时，
只需要修改本模块，不需要让 UI 知道内部实现细节。
"""

from __future__ import print_function

from .teeth_component import TeethComponent


def build_teeth():
    u"""
    构建 Upper / Lower Teeth Rig。

    Returns:
        dict:
            component:
                TeethComponent 实例，供后续 Jaw / Finalize 阶段继续读取结果。

            upper_joint / lower_joint:
                Upper / Lower Teeth Bind Joint。

            upper_control / lower_control:
                Upper / Lower Teeth 动画控制器。

            upper_top_group / lower_top_group:
                Controller Hierarchy 顶层组。
                后续 Jaw Follow 应从这里接入，而不是修改 Teeth 内部 Matrix。

            upper_matrix / lower_matrix:
                Controller -> Joint 的 Matrix 驱动节点。

            upper_skin / lower_skin:
                Teeth Model 的刚性 SkinCluster。
                如果对应 Teeth Model 在 Setup 中为空，则返回 None。
    """
    component = TeethComponent()

    component.collect_inputs()
    component.prepare_data()
    component.create_joint()
    component.create_controller()
    component.create_connection()
    component.finalize_step()

    return {
        "component": component,
        "upper_joint": component.upper_teeth_joint,
        "lower_joint": component.lower_teeth_joint,
        "upper_control": component.upper_teeth_control,
        "lower_control": component.lower_teeth_control,
        "upper_top_group": component.upper_teeth_top_group,
        "lower_top_group": component.lower_teeth_top_group,
        "upper_matrix": component.upper_teeth_matrix_node,
        "lower_matrix": component.lower_teeth_matrix_node,
        "upper_skin": component.upper_teeth_skin_cluster,
        "lower_skin": component.lower_teeth_skin_cluster,
    }


__all__ = [
    "TeethComponent",
    "build_teeth",
]
