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

当前 Eye Joint 标准：
    Ball Guide -> jnt_<side>_eye_ball_001
    Iris Guide -> jnt_<side>_eye_iris_001

    Joint 层级：
        jnt_<side>_eye_ball_001
            jnt_<side>_eye_iris_001

Guide 规则：
    Locator Transform 就是绑定定位数据。
    Joint 创建时直接吸附 Locator Transform，不读取 Locator Shape 的额外位置偏移。
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

    本阶段主要检查：
        1. Ball / Iris 两根 Joint 是否创建。
        2. Ball Joint 是否直接吸附 Ball Locator。
        3. Iris Joint 是否直接吸附 Iris Locator。
        4. Iris Joint 是否正确成为 Ball Joint 的子关节。
        5. Main Controller 是否和 Ball Joint 共用同一个旋转中心。
    """

    face = FaceModule()

    # Guide Template 没有导入时，使用正式 FaceModule 流程导入。
    if not cmds.objExists(face.guide_root):
        face.import_guide()

    # 单独测试 Eye 时也需要先创建 Face Joint / Controller 总组。
    face.setup_hierarchy()

    eye = get_eye(face, side)
    eye.build_rig()

    # Build 完成后应该存在的关键节点。
    expected_nodes = [
        "jnt_{}_eye_ball_001".format(side),
        "jnt_{}_eye_iris_001".format(side),
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

    # -------------------------------------------------------------------------
    # Ball Joint 和 Main Controller 都从 Ball Locator 创建。
    # 因此它们的世界位置必须一致，保证眼球旋转中心完全相同。
    # -------------------------------------------------------------------------
    ball_jnt_position = cmds.xform(
        eye.ball_jnt_name,
        query=True,
        worldSpace=True,
        translation=True
    )

    main_ctrl_position = cmds.xform(
        eye.main_ctrl_name,
        query=True,
        worldSpace=True,
        translation=True
    )

    for index in range(3):
        position_difference = abs(
            ball_jnt_position[index] - main_ctrl_position[index]
        )

        if position_difference > 0.0001:
            raise RuntimeError(
                u"Main Controller 没有和 Ball Joint 对齐：{}".format(side)
            )

    # -------------------------------------------------------------------------
    # Joint 创建规则保持最简单的对应关系：
    #
    #     Ball Joint -> Ball Locator Transform
    #     Iris Joint -> Iris Locator Transform
    #
    # Locator 的 Transform 本身就是 Guide 数据，所以直接比较两者世界位置。
    # 不读取 Locator Shape.localPosition，也不做额外位置换算。
    # -------------------------------------------------------------------------
    guide_pairs = [
        (eye.ball_jnt_name, eye.guide_list[0]),
        (eye.iris_jnt_name, eye.guide_list[1]),
    ]

    for joint_name, guide_name in guide_pairs:
        joint_position = cmds.xform(
            joint_name,
            query=True,
            worldSpace=True,
            translation=True
        )

        guide_position = cmds.xform(
            guide_name,
            query=True,
            worldSpace=True,
            translation=True
        )

        for index in range(3):
            position_difference = abs(
                joint_position[index] - guide_position[index]
            )

            if position_difference > 0.0001:
                raise RuntimeError(
                    u"Joint 没有和 Locator 对齐：{} -> {}".format(
                        joint_name,
                        guide_name
                    )
                )

    # -------------------------------------------------------------------------
    # Iris Joint 必须位于 Ball Joint 下方。
    # Ball Joint 旋转时，Iris Joint 会通过 Joint Hierarchy 自然继承旋转。
    # -------------------------------------------------------------------------
    iris_parent = cmds.listRelatives(
        eye.iris_jnt_name,
        parent=True,
        type="joint"
    ) or []

    if not iris_parent:
        raise RuntimeError(
            u"Iris Joint 没有父 Joint：{}".format(eye.iris_jnt_name)
        )

    if iris_parent[0] != eye.ball_jnt_name:
        raise RuntimeError(
            u"Iris Joint 父级错误：{} -> {}".format(
                eye.iris_jnt_name,
                iris_parent[0]
            )
        )

    print(u"[Eye Test] build_rig PASS : {}".format(side))

    return expected_nodes


def connect(side="lf"):
    u"""
    测试 Aim -> Main -> Ball Joint 的绑定连接。

    Main Output 只约束 Ball Joint。
    Iris Joint 通过 Joint Hierarchy 继承 Ball Joint 的旋转，不创建额外 Constraint。
    """

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

    Face 总组和 face_guide.ma 会继续保留，方便调整 Guide 后立即重新 Build。
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
