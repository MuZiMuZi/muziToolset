# coding=utf-8
u"""
Maya 2023 Functional Smoke Test
===============================

对 muziToolset 根包执行真实 Maya 功能测试。

与 maya_smoke_test.py 的区别：
    maya_smoke_test.py
        只验证 import、UI 构造、Window Manager 和资源。

    maya_functional_smoke_test.py
        会真实创建 Maya 临时节点并执行 Core / Tool / System 功能。

安全原则：
    1. 测试节点统一使用 __muzi_smoke_* 随机名称；
    2. 每个测试结束后立即删除自身临时节点；
    3. 运行结束后恢复用户原来的 Maya 选择；
    4. 不保存场景、不新建场景、不修改当前文件路径；
    5. Face Rig 使用固定全局名称，因此检测到已有 Face Rig 时直接 SKIP；
    6. 如果运行前不存在 ctrl_set，测试结束时会删除测试产生的空 ctrl_set。

Maya Script Editor：

    import muziToolset
    report = muziToolset.functional_smoke_test()

结果状态：
    PASS    功能执行并验证成功
    FAIL    功能执行失败或结果不符合预期
    SKIP    为保护当前场景主动跳过
"""

from __future__ import print_function

import importlib
import traceback
import uuid

import maya.cmds as cmds


package_name = __name__.split(".")[0]


class SmokeSkip(RuntimeError):
    """表示测试因为场景安全原因主动跳过。"""


# =============================================================================
# Common
# =============================================================================
def _import(relative_name):
    """导入 muziToolset 根包下的模块。"""
    full_name = "{}.{}".format(
        package_name,
        relative_name
    )
    return importlib.import_module(full_name)


def _new_token(label):
    """返回适合 Maya 节点名使用的唯一测试 token。"""
    unique_id = uuid.uuid4().hex[:8]
    clean_label = label.replace(" ", "_")
    clean_label = clean_label.replace("-", "_")
    return "muzi_smoke_{}_{}".format(
        clean_label,
        unique_id
    )


def _short_name(node):
    """返回 Maya DAG 短名称。"""
    return node.split("|")[-1]


def _assert_true(state, message):
    """统一测试断言。"""
    if not state:
        raise AssertionError(message)


def _almost_equal(value_a, value_b, tolerance=0.001):
    """浮点近似比较。"""
    return abs(float(value_a) - float(value_b)) <= tolerance


def _node_depth(node):
    """返回 DAG 深度，用于清理时先删除子节点。"""
    return node.count("|")


def _cleanup_nodes(nodes):
    """删除指定测试节点，忽略已经随父节点删除的节点。"""
    if not nodes:
        return

    if isinstance(nodes, str):
        nodes = [nodes]

    resolved_nodes = []

    for node in nodes:
        if not node:
            continue

        if not cmds.objExists(node):
            continue

        matches = cmds.ls(
            node,
            long=True
        )

        if matches is None:
            matches = []

        resolved = node

        if matches:
            resolved = matches[0]

        if resolved not in resolved_nodes:
            resolved_nodes.append(resolved)

    resolved_nodes = sorted(
        resolved_nodes,
        key=_node_depth,
        reverse=True
    )

    for node in resolved_nodes:
        if not cmds.objExists(node):
            continue

        try:
            cmds.delete(node)
        except Exception:
            pass


def _cleanup_token(token):
    """删除名称中包含测试 token 的全部 Maya 节点。"""
    pattern = "*{}*".format(token)
    nodes = cmds.ls(
        pattern,
        long=True
    )

    if nodes is None:
        nodes = []

    _cleanup_nodes(nodes)


def _delete_widget(widget):
    """释放 Functional Test 中创建的临时 QWidget。"""
    if widget is None:
        return

    try:
        widget.close()
    except Exception:
        pass

    try:
        widget.deleteLater()
    except Exception:
        pass


def _record(results, category, name, status, message):
    """记录单项结果。"""
    result = {
        "category": category,
        "name": name,
        "status": status,
        "message": message,
        "traceback": "",
    }
    results.append(result)
    return result


def _run_case(results, category, name, test_function):
    """运行一个 Functional Smoke Test Case。"""
    try:
        message = test_function()

        if not message:
            message = u"功能验证成功"

        return _record(
            results,
            category,
            name,
            "PASS",
            message
        )

    except SmokeSkip as error:
        return _record(
            results,
            category,
            name,
            "SKIP",
            str(error)
        )

    except Exception as error:
        result = _record(
            results,
            category,
            name,
            "FAIL",
            str(error)
        )
        result["traceback"] = traceback.format_exc()
        return result


# =============================================================================
# Basic
# =============================================================================
def _test_basic_attr():
    """验证 Attr Tool 的锁定 / 隐藏执行入口。"""
    token = _new_token("basic_attr")
    node = None
    widget = None

    try:
        attr_tool = _import("tools.basic.attr_tool")

        node = cmds.createNode(
            "transform",
            name="__{}_node".format(token)
        )
        cmds.select(
            node,
            replace=True
        )

        widget = attr_tool.AttrTool()
        widget.translation_locked_checkbox.setChecked(True)
        widget.translation_hidden_checkbox.setChecked(True)
        widget.clicked_attr_set_button()

        locked = cmds.getAttr(
            node + ".translateX",
            lock=True
        )
        keyable = cmds.getAttr(
            node + ".translateX",
            keyable=True
        )

        _assert_true(
            locked,
            u"Attr Tool 没有锁定 translateX。"
        )
        _assert_true(
            not keyable,
            u"Attr Tool 没有隐藏 translateX。"
        )

        return u"Transform 锁定 / 隐藏成功"

    finally:
        _delete_widget(widget)
        _cleanup_token(token)


def _test_basic_connections():
    """验证 Connections Tool 的 Translate 连接。"""
    token = _new_token("basic_connections")
    widget = None

    try:
        connections_tool = _import(
            "tools.basic.connections_tool"
        )

        driver = cmds.createNode(
            "transform",
            name="__{}_driver".format(token)
        )
        driven = cmds.createNode(
            "transform",
            name="__{}_driven".format(token)
        )

        widget = connections_tool.ConnectionsTool()
        widget.translate_checkbox.setChecked(True)

        cmds.select(
            [driver, driven],
            replace=True
        )
        widget.connect_default_attrs()

        connected = cmds.isConnected(
            driver + ".translate",
            driven + ".translate"
        )

        _assert_true(
            connected,
            u"Connections Tool 没有建立 Translate 连接。"
        )

        return u"Translate 连接成功"

    finally:
        _delete_widget(widget)
        _cleanup_token(token)


def _test_basic_constraint():
    """验证 Constraint Tool 的 Parent Constraint。"""
    token = _new_token("basic_constraint")
    widget = None

    try:
        constraint_tool = _import(
            "tools.basic.constraint_tool"
        )

        driver = cmds.createNode(
            "transform",
            name="__{}_driver".format(token)
        )
        driven = cmds.createNode(
            "transform",
            name="__{}_driven".format(token)
        )

        widget = constraint_tool.ConstraintTool()
        widget.maintain_offset_checkbox.setChecked(False)

        cmds.select(
            [driver, driven],
            replace=True
        )
        widget.clicked_parent_constraint_button()

        constraints = cmds.listConnections(
            driven,
            source=True,
            destination=False,
            type="parentConstraint"
        )

        if constraints is None:
            constraints = []

        _assert_true(
            bool(constraints),
            u"Constraint Tool 没有创建 Parent Constraint。"
        )

        return u"Parent Constraint 创建成功"

    finally:
        _delete_widget(widget)
        _cleanup_token(token)


def _test_basic_rename():
    """验证 Rename Tool 的添加前缀功能。"""
    token = _new_token("basic_rename")
    widget = None

    try:
        rename_tool = _import("tools.basic.rename_tool")

        node_a = cmds.createNode(
            "transform",
            name="__{}_a".format(token)
        )
        node_b = cmds.createNode(
            "transform",
            name="__{}_b".format(token)
        )

        cmds.select(
            [node_a, node_b],
            replace=True
        )

        widget = rename_tool.RenameTool()
        widget.prefix_line.setText("test_")
        widget.add_prefix()

        matches = cmds.ls(
            "test___{}_*".format(token),
            long=True
        )

        if matches is None:
            matches = []

        _assert_true(
            len(matches) == 2,
            u"Rename Tool 前缀结果数量不正确：{}".format(
                len(matches)
            )
        )

        return u"批量添加前缀成功"

    finally:
        _delete_widget(widget)
        _cleanup_token(token)


def _test_basic_snap():
    """验证 Quick Snap 命令型工具。"""
    token = _new_token("basic_snap")

    try:
        snap_tool = _import("tools.basic.snap_tool")

        reference_a = cmds.spaceLocator(
            name="__{}_a".format(token)
        )[0]
        reference_b = cmds.spaceLocator(
            name="__{}_b".format(token)
        )[0]
        target = cmds.spaceLocator(
            name="__{}_target".format(token)
        )[0]

        cmds.xform(
            reference_a,
            worldSpace=True,
            translation=(0.0, 0.0, 0.0)
        )
        cmds.xform(
            reference_b,
            worldSpace=True,
            translation=(2.0, 0.0, 0.0)
        )
        cmds.xform(
            target,
            worldSpace=True,
            translation=(10.0, 0.0, 0.0)
        )

        cmds.select(
            [reference_a, reference_b, target],
            replace=True
        )

        state = snap_tool.main()
        _assert_true(state, u"Quick Snap 返回失败状态。")

        position = cmds.xform(
            target,
            query=True,
            worldSpace=True,
            translation=True
        )

        _assert_true(
            _almost_equal(position[0], 1.0),
            u"Quick Snap X 位置错误：{}".format(position[0])
        )

        return u"平均位置吸附成功"

    finally:
        _cleanup_token(token)


# =============================================================================
# Joint
# =============================================================================
def _test_joint_tool_create():
    """验证 Joint Tool 按选择创建 Joint。"""
    token = _new_token("joint_tool")
    widget = None
    created_joints = []

    try:
        joint_tool = _import("tools.joint.joint_tool")

        locator = cmds.spaceLocator(
            name="__{}_locator".format(token)
        )[0]
        cmds.xform(
            locator,
            worldSpace=True,
            translation=(3.0, 4.0, 5.0)
        )

        old_joints = cmds.ls(
            type="joint",
            long=True
        )

        if old_joints is None:
            old_joints = []

        cmds.select(
            locator,
            replace=True
        )

        widget = joint_tool.JointTool()
        widget.create_snap_joints()

        new_joints = cmds.ls(
            type="joint",
            long=True
        )

        if new_joints is None:
            new_joints = []

        for joint in new_joints:
            if joint not in old_joints:
                created_joints.append(joint)

        _assert_true(
            len(created_joints) == 1,
            u"Joint Tool 创建 Joint 数量错误：{}".format(
                len(created_joints)
            )
        )

        joint_position = cmds.xform(
            created_joints[0],
            query=True,
            worldSpace=True,
            translation=True
        )

        _assert_true(
            _almost_equal(joint_position[0], 3.0)
            and _almost_equal(joint_position[1], 4.0)
            and _almost_equal(joint_position[2], 5.0),
            u"Joint Tool 创建位置不正确：{}".format(joint_position)
        )

        return u"按选择位置创建 Joint 成功"

    finally:
        _delete_widget(widget)
        _cleanup_nodes(created_joints)
        _cleanup_token(token)


def _test_joint_resample():
    """验证 Joint Resample 真实插入父子 Joint。"""
    token = _new_token("joint_resample")

    try:
        joint_resamp_tool = _import(
            "tools.joint.joint_resamp_tool"
        )

        cmds.select(clear=True)
        start_joint = cmds.joint(
            name="jnt_{}_start".format(token),
            position=(0.0, 0.0, 0.0)
        )
        end_joint = cmds.joint(
            name="jnt_{}_end".format(token),
            position=(0.0, 6.0, 0.0)
        )

        created_joints = joint_resamp_tool.resample_joint(
            start_joint=start_joint,
            end_joint=end_joint,
            joint_number=2
        )

        _assert_true(
            len(created_joints) == 2,
            u"Joint Resample 应创建 2 个 Joint，实际 {}。".format(
                len(created_joints)
            )
        )

        end_parent = cmds.listRelatives(
            end_joint,
            parent=True,
            fullPath=False
        )

        if end_parent is None:
            end_parent = []

        _assert_true(
            bool(end_parent),
            u"Joint Resample 后 End Joint 没有父节点。"
        )

        _assert_true(
            _short_name(end_parent[0]) == _short_name(created_joints[-1]),
            u"Joint Resample 父子层级错误。"
        )

        return u"直接父子 Joint 重采样成功"

    finally:
        _cleanup_token(token)


# =============================================================================
# Controller
# =============================================================================
def _test_controller_shape():
    """验证 Controller Shape JSON 可真实创建 NURBS Curve。"""
    token = _new_token("controller_shape")

    try:
        control_shape_utils = _import(
            "core.control_shape_utils"
        )

        transform = cmds.createNode(
            "transform",
            name="ctrl_{}_shape".format(token)
        )

        shape_data = control_shape_utils.load_shape_data("circle")
        control_shape_utils.apply_shape_data(
            transform,
            shape_data
        )

        shapes = cmds.listRelatives(
            transform,
            shapes=True,
            noIntermediate=True,
            type="nurbsCurve"
        )

        if shapes is None:
            shapes = []

        _assert_true(
            bool(shapes),
            u"circle Shape JSON 没有创建 NURBS Curve。"
        )

        return u"circle Shape JSON 创建成功"

    finally:
        _cleanup_token(token)


def _test_controller_create():
    """验证统一 Controller System 创建标准层级。"""
    token = _new_token("controller_create")

    try:
        controller_system = _import("systems.controller")

        target = cmds.createNode(
            "transform",
            name="target_{}".format(token)
        )
        cmds.xform(
            target,
            worldSpace=True,
            translation=(2.0, 3.0, 4.0)
        )

        result = controller_system.create_controller(
            name="ctrl_{}_main".format(token),
            shape="circle",
            radius=1.25,
            axis="Y+",
            target=target,
            color=17,
            create_sub_control=True,
            create_extra_groups=True,
            add_to_set=True
        )

        required_keys = [
            "control",
            "sub_control",
            "output",
            "top_group",
            "groups",
        ]

        for key in required_keys:
            _assert_true(
                key in result,
                u"Controller System 返回值缺少：{}".format(key)
            )

        _assert_true(
            cmds.objExists(result["control"]),
            u"Controller Transform 不存在。"
        )
        _assert_true(
            cmds.objExists(result["output"]),
            u"Controller Output 不存在。"
        )
        _assert_true(
            len(result["groups"]) == 5,
            u"标准 Controller Group 数量不是 5。"
        )

        return u"标准 Controller 层级创建成功"

    finally:
        _cleanup_token(token)


def _test_controller_fk():
    """验证 FK Creator 命令入口真实创建 FK 链。"""
    token = _new_token("controller_fk")

    try:
        create_fk_ctrl_tool = _import(
            "tools.controller.create_fk_ctrl_tool"
        )

        cmds.select(clear=True)
        joint_a = cmds.joint(
            name="jnt_{}_a".format(token),
            position=(0.0, 0.0, 0.0)
        )
        joint_b = cmds.joint(
            name="jnt_{}_b".format(token),
            position=(0.0, 3.0, 0.0)
        )
        joint_c = cmds.joint(
            name="jnt_{}_c".format(token),
            position=(0.0, 6.0, 0.0)
        )

        cmds.select(
            [joint_a, joint_b, joint_c],
            replace=True
        )

        controls = create_fk_ctrl_tool.main()

        _assert_true(
            len(controls) == 3,
            u"FK Creator 应创建 3 个控制器，实际 {}。".format(
                len(controls)
            )
        )

        for control in controls:
            _assert_true(
                cmds.objExists(control),
                u"FK Controller 不存在：{}".format(control)
            )

        return u"3 Joint FK Controller Chain 创建成功"

    finally:
        _cleanup_token(token)


# =============================================================================
# Rig
# =============================================================================
def _test_rig_ik():
    """验证 Rig Tool 基础 RP IK。"""
    token = _new_token("rig_ik")

    try:
        rig_tool = _import("tools.rig.rig_tool")

        cmds.select(clear=True)
        start_joint = cmds.joint(
            name="jnt_{}_start".format(token),
            position=(0.0, 0.0, 0.0)
        )
        middle_joint = cmds.joint(
            name="jnt_{}_middle".format(token),
            position=(3.0, 2.0, 0.0)
        )
        end_joint = cmds.joint(
            name="jnt_{}_end".format(token),
            position=(6.0, 0.0, 0.0)
        )

        result = rig_tool.create_ik_rig(
            start_joint,
            end_joint
        )

        _assert_true(
            cmds.objExists(result["ik_handle"]),
            u"RP IK Handle 没有创建。"
        )
        _assert_true(
            cmds.objExists(result["end_control"]),
            u"IK End Controller 没有创建。"
        )
        _assert_true(
            result["pole_control"]
            and cmds.objExists(result["pole_control"]),
            u"Pole Vector Controller 没有创建。"
        )

        return u"RP IK + End Ctrl + Pole Ctrl 创建成功"

    finally:
        _cleanup_token(token)


def _test_rig_skirt():
    """验证 Skirt Rig Setup + Build。"""
    token = _new_token("rig_skirt")

    try:
        skirt_system = _import("systems.body.skirt")

        builder = skirt_system.SkirtRigBuilder(
            name=token,
            horizontal_count=4,
            vertical_count=3
        )

        setup_result = builder.create_setup()
        _assert_true(
            cmds.objExists(setup_result["up_curve"]),
            u"Skirt Up Curve 没有创建。"
        )
        _assert_true(
            cmds.objExists(setup_result["down_curve"]),
            u"Skirt Down Curve 没有创建。"
        )

        result = builder.build()

        _assert_true(
            len(result["controls"]) == 12,
            u"Skirt Controller 数量错误：{}".format(
                len(result["controls"])
            )
        )
        _assert_true(
            len(result["joints"]) == 12,
            u"Skirt Joint 数量错误：{}".format(
                len(result["joints"])
            )
        )

        return u"4 × 3 Skirt Setup / Build 成功"

    finally:
        _cleanup_token(token)


# =============================================================================
# Face
# =============================================================================
def _test_face_setup():
    """验证 Face Rig Step 01；已有 Face Rig 时安全跳过。"""
    token = _new_token("face_setup")

    face_config = _import("systems.face.config")
    face_setup_module = _import("systems.face.face_setup")

    protected_nodes = [
        face_config.face_master_grp,
        face_config.config_node,
    ]

    for node in protected_nodes:
        if cmds.objExists(node):
            raise SmokeSkip(
                u"场景已存在正式 Face Rig 节点 {}，为保护现有数据跳过 Step 01。".format(
                    node
                )
            )

    try:
        head_model = cmds.polySphere(
            name="model_{}_head".format(token),
            constructionHistory=False
        )[0]

        face_setup = face_setup_module.FaceSetup(
            face_head_model=head_model,
            mouth_jnt_number=32
        )
        state = face_setup.build()

        _assert_true(state, u"Face Setup build() 返回失败。")
        _assert_true(
            cmds.objExists(face_setup.config_node),
            u"Face Config Network 没有创建。"
        )
        _assert_true(
            cmds.nodeType(face_setup.config_node) == "network",
            u"Face Config 节点类型不是 network。"
        )

        work_models = [
            face_setup.face_head_tweak_model,
            face_setup.face_head_stretch_model,
            face_setup.face_head_deform_model,
        ]

        for model in work_models:
            _assert_true(
                model and cmds.objExists(model),
                u"Face Setup 工作模型没有创建：{}".format(model)
            )

        return u"Face Step 01 层级 / 工作模型 / Config 创建成功"

    finally:
        cleanup_nodes = [
            face_config.face_master_grp,
            face_config.config_node,
        ]
        _cleanup_nodes(cleanup_nodes)
        _cleanup_token(token)


# =============================================================================
# Skin
# =============================================================================
def _test_skin_copy():
    """验证 SkinCluster 创建和 Skin Weight Copy。"""
    token = _new_token("skin_copy")

    try:
        skin_utils = _import("core.skin_utils")

        cmds.select(clear=True)
        joint_a = cmds.joint(
            name="jnt_{}_a".format(token),
            position=(-1.0, 0.0, 0.0)
        )
        cmds.select(clear=True)
        joint_b = cmds.joint(
            name="jnt_{}_b".format(token),
            position=(1.0, 0.0, 0.0)
        )

        source = cmds.polyPlane(
            name="mesh_{}_source".format(token),
            subdivisionsX=2,
            subdivisionsY=2,
            constructionHistory=False
        )[0]
        target = cmds.duplicate(
            source,
            name="mesh_{}_target".format(token),
            returnRootsOnly=True
        )[0]

        source_skin = cmds.skinCluster(
            [joint_a, joint_b],
            source,
            toSelectedBones=True,
            normalizeWeights=1,
            name="sc_{}_source".format(token)
        )[0]

        _assert_true(
            cmds.objExists(source_skin),
            u"Source SkinCluster 没有创建。"
        )

        results = skin_utils.copy_skin_weights(
            source=source,
            targets=[target]
        )

        _assert_true(
            len(results) == 1,
            u"Skin Copy 没有返回目标 SkinCluster。"
        )

        target_skin = skin_utils.find_skin_cluster(target)
        _assert_true(
            target_skin and cmds.objExists(target_skin),
            u"Target SkinCluster 没有创建。"
        )

        influences = skin_utils.get_influences(target_skin)
        _assert_true(
            len(influences) == 2,
            u"Target SkinCluster Influence 数量错误：{}".format(
                len(influences)
            )
        )

        return u"SkinCluster + Copy Skin Weights 成功"

    finally:
        _cleanup_token(token)


# =============================================================================
# BlendShape
# =============================================================================
def _test_blendshape_targets():
    """验证 BlendShape Target 添加和 Target 烘焙。"""
    token = _new_token("blendshape")

    try:
        blendshape_utils = _import(
            "core.blendshape_utils"
        )

        base = cmds.polyCube(
            name="mesh_{}_base".format(token),
            constructionHistory=False
        )[0]
        target_a = cmds.duplicate(
            base,
            name="mesh_{}_targetA".format(token),
            returnRootsOnly=True
        )[0]
        target_b = cmds.duplicate(
            base,
            name="mesh_{}_targetB".format(token),
            returnRootsOnly=True
        )[0]

        cmds.move(
            0.0,
            0.5,
            0.0,
            target_a + ".vtx[0]",
            relative=True,
            objectSpace=True
        )
        cmds.move(
            0.0,
            -0.5,
            0.0,
            target_b + ".vtx[1]",
            relative=True,
            objectSpace=True
        )

        blendshape_node = cmds.blendShape(
            target_a,
            base,
            name="bs_{}".format(token)
        )[0]

        add_result = blendshape_utils.add_or_replace_target(
            blendshape_node,
            target_b
        )

        _assert_true(
            add_result["alias"] == _short_name(target_b),
            u"BlendShape Target Alias 不正确。"
        )

        targets = blendshape_utils.get_targets(
            blendshape_node
        )
        _assert_true(
            len(targets) == 2,
            u"BlendShape Target 数量错误：{}".format(len(targets))
        )

        copies = blendshape_utils.duplicate_all_targets(
            blendshape_node
        )
        _assert_true(
            len(copies) == 2,
            u"BlendShape Target 烘焙数量错误：{}".format(len(copies))
        )

        return u"Target 添加 / 查询 / 烘焙成功"

    finally:
        _cleanup_token(token)


# =============================================================================
# Clean
# =============================================================================
def _test_model_checker():
    """验证 Model Checker 能识别未冻结 Transform。"""
    token = _new_token("model_checker")

    try:
        model_check_utils = _import(
            "core.model_check_utils"
        )

        mesh = cmds.polyCube(
            name="mesh_{}".format(token),
            constructionHistory=False
        )[0]
        cmds.setAttr(
            mesh + ".translateX",
            5.0
        )

        issues = model_check_utils.run_checks(
            nodes=[mesh],
            check_nonmanifold=False,
            check_lamina=False,
            check_duplicates=False,
            check_history=False,
            check_transform=True,
            check_normals=False
        )

        found_transform_issue = False

        for issue in issues:
            if issue.get("type") == u"Mesh Transform 未冻结":
                found_transform_issue = True
                break

        _assert_true(
            found_transform_issue,
            u"Model Checker 没有识别未冻结 Transform。"
        )

        return u"未冻结 Mesh Transform 检查成功"

    finally:
        _cleanup_token(token)


def _test_scene_cleaner():
    """验证 Scene Cleaner 安全删除测试空组。"""
    token = _new_token("scene_cleaner")

    try:
        scene_clean_utils = _import(
            "core.scene_clean_utils"
        )

        parent_group = cmds.createNode(
            "transform",
            name="grp_{}_parent".format(token)
        )
        child_group = cmds.createNode(
            "transform",
            name="grp_{}_child".format(token),
            parent=parent_group
        )

        result = scene_clean_utils.run_cleanup(
            nodes=[child_group],
            selected_only=True,
            delete_empty=True,
            delete_history_enabled=False,
            freeze_enabled=False,
            unlock_enabled=False,
            center_pivot_enabled=False,
            delete_unknown_enabled=False
        )

        _assert_true(
            result.get("empty_groups", 0) >= 1,
            u"Scene Cleaner 没有删除测试空组。"
        )
        _assert_true(
            not cmds.objExists(child_group),
            u"Scene Cleaner 执行后 Child Group 仍存在。"
        )

        return u"安全空组清理成功"

    finally:
        _cleanup_token(token)


# =============================================================================
# Report
# =============================================================================
def _print_report(report):
    """输出 Functional Smoke Test 报告。"""
    print("")
    print("=" * 78)
    print("Muzi Toolset - Maya Functional Smoke Test")
    print("=" * 78)

    for result in report["results"]:
        print(
            u"[{0}] {1} | {2} | {3}".format(
                result["status"],
                result["category"],
                result["name"],
                result["message"]
            )
        )

        if result["status"] == "FAIL":
            traceback_text = result.get(
                "traceback",
                ""
            )

            if traceback_text:
                print(traceback_text)

    print("-" * 78)
    print(
        u"Total: {0} | Passed: {1} | Failed: {2} | Skipped: {3}".format(
            report["total"],
            report["passed"],
            report["failed"],
            report["skipped"]
        )
    )
    print("=" * 78)


def _restore_selection(selection):
    """恢复测试前 Maya 选择。"""
    valid_nodes = []

    for node in selection:
        if cmds.objExists(node):
            valid_nodes.append(node)

    if valid_nodes:
        cmds.select(
            valid_nodes,
            replace=True
        )
    else:
        cmds.select(clear=True)


def run():
    """运行全部真实功能 Smoke Test。"""
    original_selection = cmds.ls(
        selection=True,
        long=True
    )

    if original_selection is None:
        original_selection = []

    control_set_existed = cmds.objExists("ctrl_set")
    results = []

    test_cases = [
        ("Basic", "Attr Tool", _test_basic_attr),
        ("Basic", "Connections Tool", _test_basic_connections),
        ("Basic", "Constraint Tool", _test_basic_constraint),
        ("Basic", "Rename Tool", _test_basic_rename),
        ("Basic", "Quick Snap", _test_basic_snap),
        ("Joint", "Joint Tool Create", _test_joint_tool_create),
        ("Joint", "Joint Resample", _test_joint_resample),
        ("Controller", "Control Shape", _test_controller_shape),
        ("Controller", "Controller System", _test_controller_create),
        ("Controller", "FK Creator", _test_controller_fk),
        ("Rig", "RP IK Rig", _test_rig_ik),
        ("Rig", "Skirt Rig", _test_rig_skirt),
        ("Face", "Face Setup Step 01", _test_face_setup),
        ("Skin", "Copy Skin Weights", _test_skin_copy),
        ("BlendShape", "Target Workflow", _test_blendshape_targets),
        ("Clean", "Model Checker", _test_model_checker),
        ("Clean", "Scene Cleaner", _test_scene_cleaner),
    ]

    try:
        for test_case in test_cases:
            category = test_case[0]
            name = test_case[1]
            test_function = test_case[2]

            _run_case(
                results,
                category,
                name,
                test_function
            )

    finally:
        # 清理任何异常中断后残留的 Smoke Test 节点。
        smoke_nodes = cmds.ls(
            "*muzi_smoke_*",
            long=True
        )

        if smoke_nodes is None:
            smoke_nodes = []

        _cleanup_nodes(smoke_nodes)

        # Controller / FK / Rig / Skirt 会使用统一 ctrl_set。
        # 只有测试前不存在时，才删除测试创建的空 Set。
        if not control_set_existed:
            if cmds.objExists("ctrl_set"):
                try:
                    set_members = cmds.sets(
                        "ctrl_set",
                        query=True
                    )

                    if not set_members:
                        cmds.delete("ctrl_set")
                except Exception:
                    pass

        _restore_selection(original_selection)

    passed_count = 0
    failed_count = 0
    skipped_count = 0
    failed_results = []

    for result in results:
        if result["status"] == "PASS":
            passed_count += 1
        elif result["status"] == "FAIL":
            failed_count += 1
            failed_results.append(result)
        elif result["status"] == "SKIP":
            skipped_count += 1

    report = {
        "total": len(results),
        "passed": passed_count,
        "failed": failed_count,
        "skipped": skipped_count,
        "results": results,
        "failed_results": failed_results,
    }

    _print_report(report)
    return report


__all__ = [
    "run",
]
