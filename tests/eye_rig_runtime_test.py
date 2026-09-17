# coding=utf-8
u"""
Eye Rig Maya Runtime Test
=========================

不经过 Rig Library UI，只直接测试 EyeModule 的三个核心流程：

    build()
        -> EyeModule.build_rig()

    connect()
        -> EyeModule.connect_rig()

    delete()
        -> EyeModule.delete_rig()

使用前请先确保场景中已经存在对应侧的 Ball / Iris / Aim Guide。
"""

import maya.cmds as cmds

from muziToolset.systems.face.eye_module import EyeModule


def get_guides(side="lf"):
    u"""返回 Eye Module 测试使用的三个标准 Guide。"""

    guides = [
        "loc_{}_eye_ball_001".format(side),
        "loc_{}_eye_iris_001".format(side),
        "loc_{}_eye_aim_001".format(side),
    ]

    for guide_name in guides:
        if not cmds.objExists(guide_name):
            raise RuntimeError(
                u"找不到测试 Guide：{}".format(guide_name)
            )

    return guides


def build(side="lf"):
    u"""只测试 Eye Rig 的创建阶段，不建立 Constraint。"""

    eye = EyeModule(
        side=side,
        guide=get_guides(side)
    )

    eye.build_rig()

    expected_nodes = [
        "jnt_{}_eye_bind_001".format(side),
        "ctrl_{}_eye_main_001".format(side),
        "driven_{}_eye_main_001".format(side),
        "output_{}_eye_main_001".format(side),
        "ctrl_{}_eye_aim_001".format(side),
        "output_{}_eye_aim_001".format(side),
        "grp_{}_eye_jnt_001".format(side),
        "grp_{}_eye_ctrl_001".format(side),
    ]

    for node_name in expected_nodes:
        if not cmds.objExists(node_name):
            raise RuntimeError(
                u"Build 后缺少节点：{}".format(node_name)
            )

    print(u"[Eye Test] build_rig PASS : {}".format(side))

    return expected_nodes


def connect(side="lf"):
    u"""只测试已经 Build 完成的 Eye Rig 连接阶段。"""

    eye = EyeModule(side=side)
    result = eye.connect_rig()

    print(u"[Eye Test] connect_rig PASS : {}".format(side))
    print(result)

    return result


def delete(side="lf"):
    u"""删除当前侧 Eye Rig，并验证模块根组已经消失。"""

    eye = EyeModule(side=side)
    deleted_nodes = eye.delete_rig()

    group_names = [
        "grp_{}_eye_jnt_001".format(side),
        "grp_{}_eye_ctrl_001".format(side),
    ]

    for group_name in group_names:
        if cmds.objExists(group_name):
            raise RuntimeError(
                u"Delete 后节点仍然存在：{}".format(group_name)
            )

    print(u"[Eye Test] delete_rig PASS : {}".format(side))

    return deleted_nodes


def run(side="lf"):
    u"""按 build -> connect 顺序测试，并保留结果供 Maya 中检查。"""

    build(side)
    connect(side)

    print(u"[Eye Test] Runtime Flow PASS : {}".format(side))

    return True
