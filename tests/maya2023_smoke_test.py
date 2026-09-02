# coding=utf-8
u"""
Maya 2023 Runtime Smoke Test
============================

在真正 Autodesk Maya 2023 / mayapy 进程中运行的总 Smoke Runner。

验证：
    - Core 正式 API；
    - CtrlBase 标准控制器；
    - Face Setup / Guide Module 生命周期；
    - RigBase 直接实例属性；
    - Face Build Algorithm Smoke Test。
"""

from __future__ import print_function

import traceback
import uuid

import maya.cmds as cmds

from ..core import hierarchy_utils
from ..core import rename_utils
from ..core import scene_utils
from ..core import transform_utils
from ..systems import ctrl_base
from ..systems import face as face_system
from . import face_build_smoke_test


def create_namespace():
    u"""创建独立 Maya 2023 Smoke Namespace。"""
    token = uuid.uuid4().hex[:8]
    namespace = "muziMaya2023Smoke_{}".format(
        token
    )
    cmds.namespace(
        add=namespace
    )
    cmds.namespace(
        set=namespace
    )
    return namespace


def remove_namespace(namespace):
    u"""删除 Smoke Namespace。"""
    try:
        cmds.namespace(
            set=":"
        )
    except Exception:
        pass

    if not cmds.namespace(
            exists=namespace
    ):
        return

    try:
        cmds.namespace(
            removeNamespace=namespace,
            deleteNamespaceContent=True
        )
    except Exception as error:
        cmds.warning(
            u"无法删除 Maya 2023 Smoke Namespace {}：{}".format(
                namespace,
                error
            )
        )


def require_maya_2023():
    u"""确认当前运行环境为 Maya 2023。"""
    version = str(
        cmds.about(
            version=True
        )
    )

    if not version.startswith("2023"):
        raise RuntimeError(
            u"本 Smoke Runner 要求 Maya 2023，当前版本：{}".format(
                version
            )
        )

    return version


def test_core_contract(root_group):
    u"""验证 Scene / Hierarchy / Transform / Rename Core。"""
    parent_node = cmds.createNode(
        "transform",
        name="grp_md_core_parent_smoke_001",
        parent=root_group
    )
    child_node = cmds.createNode(
        "transform",
        name="grp_md_core_child_smoke_001"
    )

    scene_utils.validate_node(
        parent_node,
        label=u"Smoke Parent"
    )

    child_node = hierarchy_utils.parent(
        child_node,
        parent_node
    )

    queried_parent = hierarchy_utils.get_parent(
        child_node,
        full_path=True
    )

    if rename_utils.get_short_name(
            queried_parent
    ) != rename_utils.get_short_name(
            parent_node
    ):
        raise RuntimeError(
            u"Hierarchy Core Parent 查询结果错误。"
        )

    transform_utils.set_world_translation(
        child_node,
        [1.0, 2.0, 3.0]
    )
    position = transform_utils.get_world_translation(
        child_node
    )

    if len(position) != 3:
        raise RuntimeError(
            u"Transform Core World Translation 返回格式错误。"
        )

    return u"Scene / Hierarchy / Transform / Rename Core 正常"


def test_controller_contract(root_group):
    u"""验证 CtrlBase 标准控制器层级。"""
    target = cmds.createNode(
        "transform",
        name="jnt_lf_controller_target_smoke_001",
        parent=root_group
    )

    result = ctrl_base.create_ctrl(
        name="ctrl_lf_controller_smoke_001",
        shape="circle",
        radius=0.5,
        axis="Y+",
        target_node=target,
        color=6,
        create_sub_ctrl=False,
        add_to_set=True
    )

    required_keys = [
        "ctrl_node",
        "output_node",
        "top_grp",
        "grp_dict",
        "build_node_list",
    ]

    for key in required_keys:
        if key not in result:
            raise RuntimeError(
                u"CtrlBase Result 缺少 Key：{}".format(
                    key
                )
            )

    scene_utils.validate_node(
        result["ctrl_node"]
    )
    scene_utils.validate_node(
        result["output_node"]
    )
    scene_utils.validate_node(
        result["top_grp"]
    )

    expected_groups = [
        "zero",
        "driven",
        "space",
        "connect",
        "offset",
    ]

    for group_name in expected_groups:
        if group_name not in result["grp_dict"]:
            raise RuntimeError(
                u"CtrlBase 标准层级缺少：{}".format(
                    group_name
                )
            )

    return u"CtrlBase 标准层级创建正常"


def assert_rig_attributes(
        rig_object,
        side,
        part,
        index,
        label
):
    u"""验证一个 Rig Object 的 side / part / index 实例属性。"""
    if rig_object.side != side:
        raise RuntimeError(
            u"{}.side 错误：{}".format(
                label,
                rig_object.side
            )
        )

    if rig_object.part != part:
        raise RuntimeError(
            u"{}.part 错误：{}".format(
                label,
                rig_object.part
            )
        )

    if rig_object.index != index:
        raise RuntimeError(
            u"{}.index 错误：{}".format(
                label,
                rig_object.index
            )
        )


def test_face_step_contract(root_group):
    u"""验证 Face Workflow / Module 生命周期和 RigBase 属性。"""
    head_model = cmds.polySphere(
        name="model_md_head_smoke_001",
        radius=2.0
    )[0]
    head_model = hierarchy_utils.parent(
        head_model,
        root_group
    )

    face_setup = face_system.FaceSetup(
        face_head_model=head_model,
        mouth_jnt_number=32
    )

    assert_rig_attributes(
        face_setup,
        side="md",
        part="face",
        index=1,
        label=u"FaceSetup"
    )

    face_setup.run_step()

    if not face_setup.is_step_completed(
            step_value=1
    ):
        raise RuntimeError(
            u"FaceSetup.run_step() 没有完成 Step 01。"
        )

    if not callable(
            getattr(face_setup, "create_name", None)
    ):
        raise RuntimeError(
            u"FaceSetup 没有继承 RigBase Naming API。"
        )

    face_guide = face_system.FaceGuide()

    assert_rig_attributes(
        face_guide,
        side="md",
        part="face",
        index=1,
        label=u"FaceGuide"
    )

    if not callable(
            getattr(face_guide, "run_step", None)
    ):
        raise RuntimeError(
            u"FaceGuide 缺少统一 run_step()。"
        )

    if not callable(
            getattr(face_guide, "build_guide", None)
    ):
        raise RuntimeError(
            u"FaceGuide 缺少 Guide 编辑入口 build_guide()。"
        )

    teeth_module = face_system.TeethModule()

    assert_rig_attributes(
        teeth_module,
        side="md",
        part="teeth",
        index=1,
        label=u"TeethModule"
    )

    teeth_joint_name = teeth_module.create_name(
        node_type="jnt",
        part="upper_teeth",
        function="bind"
    )

    if teeth_joint_name != "jnt_md_upper_teeth_bind_001":
        raise RuntimeError(
            u"TeethModule Attribute Naming 错误：{}".format(
                teeth_joint_name
            )
        )

    if hasattr(face_setup, "build"):
        raise RuntimeError(
            u"FaceSetup 仍残留 build() Compatibility Wrapper。"
        )

    if hasattr(face_guide, "build") or hasattr(face_guide, "finalize"):
        raise RuntimeError(
            u"FaceGuide 仍残留 build/finalize Compatibility Wrapper。"
        )

    return u"Face Module Lifecycle 与 RigBase Direct Attributes 正常"


def run_case(results, name, test_function, root_group):
    u"""执行一个 Maya Smoke Case。"""
    try:
        message = test_function(
            root_group
        )
        results.append({
            "name": name,
            "passed": True,
            "message": message,
            "traceback": "",
        })
    except Exception as error:
        results.append({
            "name": name,
            "passed": False,
            "message": str(error),
            "traceback": traceback.format_exc(),
        })


def run():
    u"""运行 Maya 2023 Runtime Smoke Test。"""
    maya_version = require_maya_2023()
    namespace = create_namespace()
    results = []

    print("")
    print("=" * 78)
    print("Muzi Toolset - Maya 2023 Runtime Smoke Test")
    print("Maya: {}".format(maya_version))
    print("=" * 78)

    try:
        root_group = cmds.createNode(
            "transform",
            name="grp_md_maya2023_smoke_root_001"
        )

        run_case(
            results,
            "Core Contract",
            test_core_contract,
            root_group
        )
        run_case(
            results,
            "CtrlBase Contract",
            test_controller_contract,
            root_group
        )
        run_case(
            results,
            "Face Attribute / Step Contract",
            test_face_step_contract,
            root_group
        )
    finally:
        remove_namespace(
            namespace
        )

    face_build_result = face_build_smoke_test.run()

    passed_count = 0
    failed_count = 0

    for result in results:
        if result["passed"]:
            passed_count += 1
            print(
                u"[PASS] {} | {}".format(
                    result["name"],
                    result["message"]
                )
            )
        else:
            failed_count += 1
            print(
                u"[FAIL] {} | {}".format(
                    result["name"],
                    result["message"]
                )
            )
            print(
                result["traceback"]
            )

    failed_count += face_build_result["failed"]
    passed_count += face_build_result["passed"]

    print("-" * 78)
    print(
        "Passed: {} | Failed: {}".format(
            passed_count,
            failed_count
        )
    )
    print("=" * 78)

    return {
        "maya_version": maya_version,
        "results": results,
        "face_build": face_build_result,
        "passed": passed_count,
        "failed": failed_count,
    }


__all__ = [
    "run",
]
