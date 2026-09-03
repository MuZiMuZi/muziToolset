# coding=utf-8
u"""
Face Modules - Maya 2023 Runtime Smoke Test
===========================================

在真正 Autodesk Maya 2023 中逐模块验证新的 Face Rig Module 架构。

测试目标：
    1. 使用真实 FaceSetup 完成 Step 01；
    2. 使用正式 face_guide.ma 导入并完成 Step 02；
    3. 按真实依赖顺序执行每个 Face Module 的 create_build()；
    4. 每个模块独立报告 PASS / FAIL / SKIP；
    5. 一个模块失败时，只有依赖它的模块跳过，其余独立模块继续测试；
    6. 当前模板没有 Cheek Guide 时，CheekModule 的 skipped 属于合法结果；
    7. 全部测试放在独立 Namespace 中，结束后统一清理。

当前模块顺序：
    Brow
    Eye
    Eyelid      -> 依赖 Eye
    Nose
    Cheek       -> 当前 Guide 缺失时允许 SKIP
    Ear
    Jaw
    Teeth
    Tongue
    Lip
    Mouth       -> 依赖 Jaw + Lip

注意：
    本文件必须在 Maya 2023 / mayapy 中运行，普通 CPython 不能执行。
"""

from __future__ import print_function

import traceback

import maya.cmds as cmds

from ..systems import face as face_system
from .maya2023_smoke_test import create_namespace
from .maya2023_smoke_test import remove_namespace
from .maya2023_smoke_test import require_maya_2023


MODULE_CASES = [
    {
        "key": "brow",
        "label": "BrowModule",
        "module_class": face_system.BrowModule,
        "dependencies": [],
    },
    {
        "key": "eye",
        "label": "EyeModule",
        "module_class": face_system.EyeModule,
        "dependencies": [],
    },
    {
        "key": "eyelid",
        "label": "EyelidModule",
        "module_class": face_system.EyelidModule,
        "dependencies": ["eye"],
    },
    {
        "key": "nose",
        "label": "NoseModule",
        "module_class": face_system.NoseModule,
        "dependencies": [],
    },
    {
        "key": "cheek",
        "label": "CheekModule",
        "module_class": face_system.CheekModule,
        "dependencies": [],
    },
    {
        "key": "ear",
        "label": "EarModule",
        "module_class": face_system.EarModule,
        "dependencies": [],
    },
    {
        "key": "jaw",
        "label": "JawModule",
        "module_class": face_system.JawModule,
        "dependencies": [],
    },
    {
        "key": "teeth",
        "label": "TeethModule",
        "module_class": face_system.TeethModule,
        "dependencies": [],
    },
    {
        "key": "tongue",
        "label": "TongueModule",
        "module_class": face_system.TongueModule,
        "dependencies": [],
    },
    {
        "key": "lip",
        "label": "LipModule",
        "module_class": face_system.LipModule,
        "dependencies": [],
    },
    {
        "key": "mouth",
        "label": "MouthModule",
        "module_class": face_system.MouthModule,
        "dependencies": ["jaw", "lip"],
    },
]


DEFAULT_SHADING_GROUP = ":initialShadingGroup"


def _query_lock_state(node):
    u"""读取 Maya Node 的普通锁与未发布属性锁状态。"""
    node_lock_state = cmds.lockNode(
        node,
        query=True,
        lock=True
    )
    unpublished_lock_state = cmds.lockNode(
        node,
        query=True,
        lockUnpublished=True
    )

    return {
        "node": node,
        "locked": bool(node_lock_state[0]) if node_lock_state else False,
        "lock_unpublished": bool(unpublished_lock_state[0]) if unpublished_lock_state else False,
    }


def _get_container_chain(node):
    u"""返回包含指定 Node 的 Container 链，顺序为最外层到最内层。"""
    container_chain = []
    visited = set()

    try:
        current_container = cmds.container(
            query=True,
            findContainer=node
        )
    except Exception:
        current_container = ""

    while current_container:
        if current_container in visited:
            break

        visited.add(
            current_container
        )
        container_chain.append(
            current_container
        )

        try:
            parent_container = cmds.container(
                current_container,
                query=True,
                parentContainer=True
            )
        except Exception:
            parent_container = ""

        current_container = parent_container or ""

    container_chain.reverse()
    return container_chain


def prepare_default_shading_group():
    u"""
    临时解除默认 Shading Group 及其 Container 链的 unpublished lock。

    Returns:
        dict:
            initialShadingGroup 与 Container 链的原始锁状态。
    """
    state = {
        "exists": False,
        "node_state": None,
        "container_states": [],
    }

    if not cmds.objExists(DEFAULT_SHADING_GROUP):
        return state

    state["exists"] = True

    # -------------------------------------------------------------------------
    # Step 01：先记录 Container 链状态；外层 Container 必须最先解除锁定
    # -------------------------------------------------------------------------
    container_chain = _get_container_chain(
        DEFAULT_SHADING_GROUP
    )

    for container_node in container_chain:
        container_state = _query_lock_state(
            container_node
        )
        state["container_states"].append(
            container_state
        )

    state["node_state"] = _query_lock_state(
        DEFAULT_SHADING_GROUP
    )

    # -------------------------------------------------------------------------
    # Step 02：从最外层到最内层解除 Container 的普通锁与 unpublished lock
    # -------------------------------------------------------------------------
    for container_state in state["container_states"]:
        cmds.lockNode(
            container_state["node"],
            lock=False,
            lockUnpublished=False
        )

    # -------------------------------------------------------------------------
    # Step 03：最后解除 initialShadingGroup 自身 unpublished lock
    # 不再直接 setAttr(..., lock=False)，避免 locked-container unpublished 错误。
    # -------------------------------------------------------------------------
    cmds.lockNode(
        DEFAULT_SHADING_GROUP,
        lock=False,
        lockUnpublished=False
    )

    return state


def restore_default_shading_group(state):
    u"""
    恢复 Runtime Smoke 运行前的默认 Shading Group 与 Container 锁状态。

    Args:
        state (dict):
            prepare_default_shading_group() 保存的原始状态。

    Returns:
        bool:
            成功恢复或无需恢复时返回 True。
    """
    if not state:
        return True

    if not state.get("exists"):
        return True

    if not cmds.objExists(DEFAULT_SHADING_GROUP):
        return True

    # -------------------------------------------------------------------------
    # Step 01：Container 仍保持解锁时，先恢复 initialShadingGroup 自身状态
    # -------------------------------------------------------------------------
    node_state = state.get("node_state")

    if node_state:
        cmds.lockNode(
            DEFAULT_SHADING_GROUP,
            lock=node_state.get("locked", False),
            lockUnpublished=node_state.get("lock_unpublished", False)
        )

    # -------------------------------------------------------------------------
    # Step 02：从最内层到最外层恢复 Container，避免父 Container 提前锁死子级
    # -------------------------------------------------------------------------
    container_states = state.get(
        "container_states",
        []
    )

    container_index = len(container_states) - 1

    while container_index >= 0:
        container_state = container_states[container_index]
        container_node = container_state["node"]

        if cmds.objExists(container_node):
            cmds.lockNode(
                container_node,
                lock=container_state.get("locked", False),
                lockUnpublished=container_state.get("lock_unpublished", False)
            )

        container_index -= 1

    return True

def create_fixture_models():
    u"""
    创建 Face Setup Runtime Smoke 使用的简单测试模型。

    Returns:
        dict:
            Head / Eye / Teeth / Tongue 测试 Mesh Transform。
    """
    # -------------------------------------------------------------------------
    # Step 01：创建 Head 与左右 Eye Mesh，覆盖 Face Setup 的主要模型输入
    # -------------------------------------------------------------------------
    head_model = cmds.polySphere(
        name="model_md_head_face_modules_smoke_001",
        radius=2.0,
        subdivisionsX=12,
        subdivisionsY=8
    )[0]

    lf_eye_model = cmds.polySphere(
        name="model_lf_eye_face_modules_smoke_001",
        radius=0.35,
        subdivisionsX=8,
        subdivisionsY=6
    )[0]
    rt_eye_model = cmds.polySphere(
        name="model_rt_eye_face_modules_smoke_001",
        radius=0.35,
        subdivisionsX=8,
        subdivisionsY=6
    )[0]

    cmds.move(
        0.6,
        0.35,
        1.7,
        lf_eye_model,
        absolute=True,
        worldSpace=True
    )
    cmds.move(
        -0.6,
        0.35,
        1.7,
        rt_eye_model,
        absolute=True,
        worldSpace=True
    )

    # -------------------------------------------------------------------------
    # Step 02：创建 Upper / Lower Teeth Mesh，实际覆盖 TeethModule 的刚性 Skin
    # -------------------------------------------------------------------------
    upper_teeth_model = cmds.polyCube(
        name="model_md_upper_teeth_face_modules_smoke_001",
        width=1.0,
        height=0.18,
        depth=0.35
    )[0]
    lower_teeth_model = cmds.polyCube(
        name="model_md_lower_teeth_face_modules_smoke_001",
        width=1.0,
        height=0.18,
        depth=0.35
    )[0]

    cmds.move(
        0.0,
        0.15,
        1.65,
        upper_teeth_model,
        absolute=True,
        worldSpace=True
    )
    cmds.move(
        0.0,
        -0.15,
        1.65,
        lower_teeth_model,
        absolute=True,
        worldSpace=True
    )

    # -------------------------------------------------------------------------
    # Step 03：创建 Tongue Mesh，实际覆盖 TongueModule 的多 Joint SkinCluster
    # -------------------------------------------------------------------------
    tongue_model = cmds.polyCube(
        name="model_md_tongue_face_modules_smoke_001",
        width=0.7,
        height=0.12,
        depth=1.2,
        subdivisionsDepth=4
    )[0]
    cmds.move(
        0.0,
        -0.35,
        1.0,
        tongue_model,
        absolute=True,
        worldSpace=True
    )

    # -------------------------------------------------------------------------
    # Step 04：返回明确业务 Key，供 FaceSetup 直接使用
    # -------------------------------------------------------------------------
    return {
        "head_model": head_model,
        "lf_eye_model": lf_eye_model,
        "rt_eye_model": rt_eye_model,
        "upper_teeth_model": upper_teeth_model,
        "lower_teeth_model": lower_teeth_model,
        "tongue_model": tongue_model,
    }


def create_face_fixture():
    u"""
    创建完整 Step01 + Step02 Face Module Runtime Smoke Fixture。

    Returns:
        dict:
            Setup、Guide 与测试模型结果。
    """
    # -------------------------------------------------------------------------
    # Step 01：创建简单 Mesh，并用正式 FaceSetup 完成 Step 01
    # -------------------------------------------------------------------------
    model_dict = create_fixture_models()

    face_setup = face_system.FaceSetup(
        face_head_model=model_dict["head_model"],
        face_lf_eye_model=model_dict["lf_eye_model"],
        face_rt_eye_model=model_dict["rt_eye_model"],
        upper_teech_model=model_dict["upper_teeth_model"],
        lower_teech_model=model_dict["lower_teeth_model"],
        face_tongue_model=model_dict["tongue_model"],
        face_gum_model=None,
        mouth_jnt_number=32
    )
    face_setup.run_step()

    if not face_setup.is_step_completed(
            step_value=1
    ):
        raise RuntimeError(
            u"Face Module Smoke Fixture 的 Step 01 没有完成。"
        )

    # -------------------------------------------------------------------------
    # Step 02：导入正式 face_guide.ma，并用 FaceGuide 完成 Step 02
    # -------------------------------------------------------------------------
    face_guide = face_system.FaceGuide()
    guide_build_dict = face_guide.build_guide()
    face_guide.run_step()

    if not face_guide.is_step_completed(
            step_value=2
    ):
        raise RuntimeError(
            u"Face Module Smoke Fixture 的 Step 02 没有完成。"
        )

    # -------------------------------------------------------------------------
    # Step 03：确认真实 Guide Locator 已经可供后续 Module 查询
    # -------------------------------------------------------------------------
    guide_locators = face_guide.get_guide_locators()

    if not guide_locators:
        raise RuntimeError(
            u"Face Module Smoke Fixture 没有读取到任何 Guide Locator。"
        )

    # -------------------------------------------------------------------------
    # Step 04：返回 Fixture 数据，所有正式 Module 共享同一份 Setup / Guide
    # -------------------------------------------------------------------------
    return {
        "model_dict": model_dict,
        "face_setup": face_setup,
        "face_guide": face_guide,
        "guide_build_dict": guide_build_dict,
        "guide_locators": guide_locators,
    }


def create_dependency_skip_result(case_data, dependencies):
    u"""创建因为前置 Module 失败而产生的 SKIP 结果。"""
    dependency_text = ", ".join(
        dependencies
    )

    return {
        "key": case_data["key"],
        "name": case_data["label"],
        "state": "skipped",
        "passed": False,
        "skipped": True,
        "message": u"依赖 Module 未通过：{}".format(
            dependency_text
        ),
        "traceback": "",
        "module_dict": None,
    }


def run_module_case(case_data, module_state_dict):
    u"""
    执行一个正式 Face Module 的 create_build() Runtime Case。

    Args:
        case_data (dict):
            当前 Module 的 Key、Label、Class 和依赖定义。
        module_state_dict (dict):
            已执行模块的状态映射。

    Returns:
        dict:
            当前 Module 的 PASS / FAIL / SKIP 结果。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查显式依赖，只让真正依赖失败的后续 Module 跳过
    # -------------------------------------------------------------------------
    failed_dependencies = []

    for dependency_key in case_data["dependencies"]:
        dependency_state = module_state_dict.get(
            dependency_key
        )

        if dependency_state == "passed":
            continue

        failed_dependencies.append(
            dependency_key
        )

    if failed_dependencies:
        return create_dependency_skip_result(
            case_data,
            failed_dependencies
        )

    # -------------------------------------------------------------------------
    # Step 02：实例化正式 Module，并只通过统一 create_build() 入口执行
    # -------------------------------------------------------------------------
    try:
        face_module = case_data["module_class"]()
        face_module_dict = face_module.create_build()

        if not isinstance(face_module_dict, dict):
            raise RuntimeError(
                u"{} create_build() 没有返回 dict。".format(
                    case_data["label"]
                )
            )

        # ---------------------------------------------------------------------
        # Step 03：Cheek 等当前模板可选模块允许正式返回 skipped
        # ---------------------------------------------------------------------
        if face_module_dict.get("skipped"):
            return {
                "key": case_data["key"],
                "name": case_data["label"],
                "state": "skipped",
                "passed": False,
                "skipped": True,
                "message": face_module_dict.get(
                    "reason",
                    u"Module 主动跳过当前构建。"
                ),
                "traceback": "",
                "module_dict": face_module_dict,
            }

        if face_module_dict.get("built") is not True:
            raise RuntimeError(
                u"{} create_build() 没有返回 built=True。".format(
                    case_data["label"]
                )
            )

        # ---------------------------------------------------------------------
        # Step 04：构建成功时保存 Module Dict，方便后续调试具体输出
        # ---------------------------------------------------------------------
        return {
            "key": case_data["key"],
            "name": case_data["label"],
            "state": "passed",
            "passed": True,
            "skipped": False,
            "message": u"统一 create_build() 完整构建成功",
            "traceback": "",
            "module_dict": face_module_dict,
        }

    except Exception as error:
        # ---------------------------------------------------------------------
        # Step 05：保留完整 Traceback；后续独立 Module 仍然继续执行
        # ---------------------------------------------------------------------
        return {
            "key": case_data["key"],
            "name": case_data["label"],
            "state": "failed",
            "passed": False,
            "skipped": False,
            "message": str(error),
            "traceback": traceback.format_exc(),
            "module_dict": None,
        }


def print_case_result(case_result):
    u"""按统一格式打印一个 Face Module Runtime Case。"""
    state = case_result["state"]

    if state == "passed":
        prefix = "[PASS]"
    elif state == "skipped":
        prefix = "[SKIP]"
    else:
        prefix = "[FAIL]"

    print(
        u"{} {} | {}".format(
            prefix,
            case_result["name"],
            case_result["message"]
        )
    )

    if state == "failed":
        print(
            case_result["traceback"]
        )


def run():
    u"""
    运行新的 Face Modules Maya 2023 Runtime Smoke Test。

    Returns:
        dict:
            Maya 版本、Fixture、逐模块结果和 PASS / FAIL / SKIP 计数。
    """
    # -------------------------------------------------------------------------
    # Step 01：确认 Maya 版本，并创建隔离 Namespace
    # -------------------------------------------------------------------------
    maya_version = require_maya_2023()
    namespace = create_namespace()
    shading_group_state = prepare_default_shading_group()
    fixture_dict = None
    module_results = []
    module_state_dict = {}

    print("")
    print("=" * 78)
    print("Muzi Toolset - Face Modules Maya 2023 Runtime Smoke Test")
    print("Maya: {}".format(maya_version))
    print("=" * 78)

    try:
        # ---------------------------------------------------------------------
        # Step 02：先创建真实 Setup / Guide Fixture；Fixture 失败时不继续误报 Module
        # ---------------------------------------------------------------------
        try:
            fixture_dict = create_face_fixture()
            print(
                u"[PASS] Face Fixture | Step01 + Step02 + 正式 Guide Template 准备成功"
            )
        except Exception as error:
            fixture_result = {
                "key": "fixture",
                "name": "Face Fixture",
                "state": "failed",
                "passed": False,
                "skipped": False,
                "message": str(error),
                "traceback": traceback.format_exc(),
                "module_dict": None,
            }
            module_results.append(
                fixture_result
            )
            print_case_result(
                fixture_result
            )

        # ---------------------------------------------------------------------
        # Step 03：Fixture 正常时按依赖顺序逐个执行正式 Face Module
        # ---------------------------------------------------------------------
        if fixture_dict is not None:
            for case_data in MODULE_CASES:
                case_result = run_module_case(
                    case_data,
                    module_state_dict
                )
                module_results.append(
                    case_result
                )
                module_state_dict[case_data["key"]] = case_result["state"]
                print_case_result(
                    case_result
                )

    finally:
        # ---------------------------------------------------------------------
        # Step 04：无论成功失败都删除整个 Smoke Namespace，避免污染用户场景
        # ---------------------------------------------------------------------
        remove_namespace(
            namespace
        )
        restore_default_shading_group(
            shading_group_state
        )

    # -------------------------------------------------------------------------
    # Step 05：统计 PASS / FAIL / SKIP，并返回机器可读结果
    # -------------------------------------------------------------------------
    passed_count = 0
    failed_count = 0
    skipped_count = 0

    for module_result in module_results:
        if module_result["state"] == "passed":
            passed_count += 1
            continue

        if module_result["state"] == "skipped":
            skipped_count += 1
            continue

        failed_count += 1

    print("-" * 78)
    print(
        "Passed: {} | Failed: {} | Skipped: {}".format(
            passed_count,
            failed_count,
            skipped_count
        )
    )
    print("=" * 78)

    return {
        "maya_version": maya_version,
        "results": module_results,
        "passed": passed_count,
        "failed": failed_count,
        "skipped": skipped_count,
    }


if __name__ == "__main__":
    run()
