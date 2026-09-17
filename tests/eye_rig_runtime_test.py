# coding=utf-8
u"""
Eye Rig Maya Runtime Test
=========================

这个测试不经过 UI，直接使用正式的 FaceModule + face_guide.ma 流程测试左眼或右眼。

测试顺序：
    import_guide()
        -> 直接导入整个 face_guide.ma

    build()
        -> 只执行指定侧 EyeModule.build_rig()

    connect()
        -> 只执行指定侧 EyeModule.connect_rig()

    delete()
        -> 只删除指定侧 Eye Rig

这样可以先把 Eye 的真实创建流程跑通，再继续测试整个 FaceModule。
"""

import maya.cmds as cmds

from muziToolset.systems.face.face_module import FaceModule


def get_eye(face, side="lf"):
    u"""从 FaceModule 中取得当前需要测试的左眼或右眼模块。"""

    if side == "lf":
        return face.lf_eye

    if side == "rt":
        return face.rt_eye

    raise ValueError(u"Eye Runtime Test 只支持 lf / rt，当前值：{}".format(side))


def import_guide():
    u"""导入整个 Face Guide Template，并返回 Guide Root。"""

    face = FaceModule()
    guide_root = face.import_guide()

    print(u"[Eye Test] import_guide PASS : {}".format(guide_root))

    return guide_root


def build(side="lf"):
    u"""
    只测试指定侧 Eye Rig 的创建阶段，不建立 Constraint。

    face_guide.ma 必须先导入场景。
    测试会创建 Face 总组，然后只执行当前侧 EyeModule.build_rig()，
    不会同时创建 Ear / Tongue 或另一侧 Eye，方便我们单独排查眼球绑定。
    """

    face = FaceModule()

    if not cmds.objExists(face.guide_root):
        face.import_guide()

    face.setup_hierarchy()

    eye = get_eye(face, side)
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
        face.jnt_master_grp,
        face.ctrl_master_grp,
    ]

    for node_name in expected_nodes:
        if not cmds.objExists(node_name):
            raise RuntimeError(u"Build 后缺少节点：{}".format(node_name))

    print(u"[Eye Test] build_rig PASS : {}".format(side))

    return expected_nodes


def connect(side="lf"):
    u"""测试 Aim -> Main -> Eye Joint 的绑定连接。"""

    face = FaceModule()
    eye = get_eye(face, side)
    result = eye.connect_rig()

    aim_constraint = result["aim"]
    orient_constraint = result["orient"]

    if not cmds.objExists(aim_constraint):
        raise RuntimeError(
            u"缺少 Eye Aim Constraint：{}".format(aim_constraint)
        )

    if cmds.nodeType(aim_constraint) != "aimConstraint":
        raise RuntimeError(
            u"Eye Aim 节点类型错误：{}".format(aim_constraint)
        )

    if not cmds.objExists(orient_constraint):
        raise RuntimeError(
            u"缺少 Eye Orient Constraint：{}".format(orient_constraint)
        )

    if cmds.nodeType(orient_constraint) != "orientConstraint":
        raise RuntimeError(
            u"Eye Orient 节点类型错误：{}".format(orient_constraint)
        )

    print(u"[Eye Test] connect_rig PASS : {}".format(side))
    print(result)

    return result


def delete(side="lf"):
    u"""
    删除指定侧 Eye Rig，并验证 Eye 模块组已经消失。

    Face 总组和 face_guide.ma 会继续保留，方便马上重新调整 Guide 并再次 Build。
    """

    face = FaceModule()
    eye = get_eye(face, side)
    deleted_nodes = eye.delete_rig()

    group_names = [
        "grp_{}_eye_jnt_001".format(side),
        "grp_{}_eye_ctrl_001".format(side),
    ]

    for group_name in group_names:
        if cmds.objExists(group_name):
            raise RuntimeError(u"Delete 后节点仍然存在：{}".format(group_name))

    print(u"[Eye Test] delete_rig PASS : {}".format(side))

    return deleted_nodes


def run(side="lf"):
    u"""按照正式模板流程执行 import -> build -> connect，并保留结果供 Maya 检查。"""

    import_guide()
    build(side)
    connect(side)

    print(u"[Eye Test] Runtime Flow PASS : {}".format(side))

    return True
