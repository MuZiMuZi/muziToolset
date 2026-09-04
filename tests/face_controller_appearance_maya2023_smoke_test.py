# coding=utf-8
u"""
Face Controller Appearance Maya 2023 Runtime Smoke Test
=======================================================

在真正 Autodesk Maya 2023 中验证 Step 03 Controller Appearance 的运行时契约。

测试流程：
    FaceSetup / FaceGuide Fixture
        -> FaceBuild.run_step()
            -> 记录 Controller / Output / Face Jnt / Shape 状态
                -> apply_controller_settings()
                    -> 保存 Controller Settings
                        -> 验证只有 Shape CV 尺寸和颜色发生变化

成功标准：
    1. Global Scale 能实时缩放全部 Face Controller Shape；
    2. Eye / Nose / Cheek / Jaw Module Size 能按模块单独叠加；
    3. cheekbone Controller 正确归属于 Cheek Size；
    4. LF / RT / MD 颜色能实时更新；
    5. Controller World Matrix 完全保持不变；
    6. Controller Transform Scale 始终保持 (1, 1, 1)；
    7. Representative Controller Output World Matrix 保持不变；
    8. Face Jnt Group 下全部 Jnt World Matrix 保持不变；
    9. Guide / Ctrl Alignment 在外观调整后仍然通过。
"""

from __future__ import print_function

import traceback

import maya.cmds as cmds

from ..core import control_shape_utils
from ..systems import ctrl_base
from ..systems import face as face_system
from ..systems.face import config
from ..systems.face import controller_appearance
from ..systems.face.guide.face_guide import FaceGuide
from .face_build_step_maya2023_smoke_test import _resolve_unique_node
from .face_build_step_maya2023_smoke_test import validate_guide_ctrl_alignment
from .face_modules_maya2023_smoke_test import create_fixture_models
from .face_modules_maya2023_smoke_test import prepare_default_shading_group
from .face_modules_maya2023_smoke_test import restore_default_shading_group
from .maya2023_smoke_test import create_namespace
from .maya2023_smoke_test import remove_namespace
from .maya2023_smoke_test import require_maya_2023


REPRESENTATIVE_CONTROLLERS = [
    {
        "name": "ctrl_lf_eye_main_001",
        "module": "eye",
        "side": "lf",
    },
    {
        "name": "ctrl_md_nose_center_bind_001",
        "module": "nose",
        "side": "md",
    },
    {
        "name": "ctrl_rt_cheekbone_bind_002",
        "module": "cheek",
        "side": "rt",
    },
    {
        "name": "ctrl_md_jaw_bind_001",
        "module": "jaw",
        "side": "md",
    },
]


MODULE_SCALE_MULTIPLIERS = {
    "eye": 1.15,
    "nose": 0.90,
    "cheek": 1.35,
    "jaw": 1.10,
}


GLOBAL_SCALE_MULTIPLIER = 1.20
MATRIX_TOLERANCE = 0.000001
RADIUS_TOLERANCE = 0.0001


def _set_smoke_namespace(namespace):
    u"""把 Maya 当前 Namespace 恢复为本次 Smoke 隔离空间。"""
    if not cmds.namespace(
            exists=namespace
    ):
        raise RuntimeError(
            u"Smoke Namespace 不存在：{}".format(
                namespace
            )
        )

    cmds.namespace(
        set=namespace
    )
    return cmds.namespaceInfo(
        currentNamespace=True,
        absoluteName=True
    )


def _bind_face_config(face_object, config_node):
    u"""把新的 Face Workflow 对象绑定到 Step 01 实际创建的 Config 节点。"""
    if not config_node:
        raise RuntimeError(
            u"Face Config 节点不能为空。"
        )

    if not cmds.objExists(
            config_node
    ):
        raise RuntimeError(
            u"Face Config 节点不存在：{}".format(
                config_node
            )
        )

    face_object.config_node = config_node
    face_object.config_data.node = config_node
    return config_node


def _create_namespace_safe_face_fixture(namespace):
    u"""
    创建独立 Namespace 下的完整 Step 01 + Step 02 Face Fixture。

    Face Setup / Guide 的正式业务代码仍保持不变。这里唯一额外做的事情是：
    每个 Workflow 对象都继续使用 Step 01 实际创建出来的 Config 节点，避免
    Maya 在某些命令执行后把 Current Namespace 切回 Root 时丢失 face_config。
    """
    # -------------------------------------------------------------------------
    # Step 01：创建测试模型并完成正式 Face Setup
    # -------------------------------------------------------------------------
    _set_smoke_namespace(
        namespace
    )
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
            u"Controller Appearance Fixture 的 Step 01 没有完成。"
        )

    actual_config_node = face_setup.config_node

    if not actual_config_node:
        raise RuntimeError(
            u"Face Setup 完成后没有返回实际 Config Node。"
        )

    if not cmds.objExists(
            actual_config_node
    ):
        raise RuntimeError(
            u"Face Setup 创建的 Config Node 不存在：{}".format(
                actual_config_node
            )
        )

    # -------------------------------------------------------------------------
    # Step 02：恢复 Smoke Namespace，并让 FaceGuide 继承同一个 Config 引用
    # -------------------------------------------------------------------------
    _set_smoke_namespace(
        namespace
    )
    face_guide = face_system.FaceGuide()
    _bind_face_config(
        face_guide,
        actual_config_node
    )
    guide_build_dict = face_guide.build_guide()

    # Guide Template Import 之后再次恢复 Current Namespace，避免后续短名解析漂移。
    _set_smoke_namespace(
        namespace
    )
    _bind_face_config(
        face_guide,
        actual_config_node
    )
    face_guide.run_step()

    if not face_guide.is_step_completed(
            step_value=2
    ):
        raise RuntimeError(
            u"Controller Appearance Fixture 的 Step 02 没有完成。"
        )

    guide_locators = face_guide.get_guide_locators()

    if not guide_locators:
        raise RuntimeError(
            u"Controller Appearance Fixture 没有读取到任何 Guide Locator。"
        )

    # 返回前把当前 Namespace 固定回本次 Smoke，供后续 FaceBuild / Module 使用。
    _set_smoke_namespace(
        namespace
    )

    return {
        "model_dict": model_dict,
        "face_setup": face_setup,
        "face_guide": face_guide,
        "config_node": actual_config_node,
        "guide_build_dict": guide_build_dict,
        "guide_locators": guide_locators,
    }


def _get_canonical_short_name(node):
    u"""返回去掉 DAG Path 和 Namespace 的短名称。"""
    short_name = str(node).rsplit(
        "|",
        1
    )[-1]
    return short_name.rsplit(
        ":",
        1
    )[-1]


def _get_world_matrix(node):
    u"""读取 Transform / Jnt 的 World Matrix。"""
    return cmds.xform(
        node,
        query=True,
        worldSpace=True,
        matrix=True
    )


def _get_transform_scale(node):
    u"""读取 Transform Scale XYZ。"""
    return [
        cmds.getAttr(node + ".scaleX"),
        cmds.getAttr(node + ".scaleY"),
        cmds.getAttr(node + ".scaleZ"),
    ]


def _assert_values_close(
        label,
        expected_values,
        actual_values,
        tolerance=MATRIX_TOLERANCE
):
    u"""逐元素比较两个数值序列。"""
    if len(expected_values) != len(actual_values):
        raise RuntimeError(
            u"{} 长度不一致：expected={} actual={}".format(
                label,
                len(expected_values),
                len(actual_values)
            )
        )

    index = 0

    while index < len(expected_values):
        expected_value = float(
            expected_values[index]
        )
        actual_value = float(
            actual_values[index]
        )
        delta = abs(
            expected_value - actual_value
        )

        if delta > tolerance:
            raise RuntimeError(
                u"{} 发生变化：index={} expected={} actual={} delta={}".format(
                    label,
                    index,
                    expected_value,
                    actual_value,
                    delta
                )
            )

        index += 1

    return True


def _get_setting(settings, attr_name):
    u"""按正式默认值读取 Controller Setting。"""
    default_value = config.face_controller_default_settings.get(
        attr_name
    )
    return settings.get(
        attr_name,
        default_value
    )


def _choose_new_color(old_color):
    u"""生成一个与旧值不同的合法 Maya Index Color。"""
    new_color = (
        int(old_color) + 7
    ) % 32

    if new_color == int(old_color):
        new_color = (
            int(old_color) + 1
        ) % 32

    return new_color


def _create_new_settings(previous_settings):
    u"""创建用于本次 Runtime Smoke 的确定性新外观参数。"""
    new_settings = dict(
        previous_settings
    )

    global_attr = config.face_controller_global_scale_attr
    old_global_scale = float(
        _get_setting(
            previous_settings,
            global_attr
        )
    )
    new_settings[global_attr] = (
        old_global_scale *
        GLOBAL_SCALE_MULTIPLIER
    )

    for module_name in MODULE_SCALE_MULTIPLIERS:
        module_attr = config.face_controller_size_attr_names.get(
            module_name
        )

        if not module_attr:
            raise RuntimeError(
                u"没有找到 {} Controller Size Attr。".format(
                    module_name
                )
            )

        old_module_scale = float(
            _get_setting(
                previous_settings,
                module_attr
            )
        )
        new_settings[module_attr] = (
            old_module_scale *
            MODULE_SCALE_MULTIPLIERS[module_name]
        )

    for side in config.face_controller_color_attr_names:
        color_attr = config.face_controller_color_attr_names[side]
        old_color = int(
            _get_setting(
                previous_settings,
                color_attr
            )
        )
        new_settings[color_attr] = _choose_new_color(
            old_color
        )

    return new_settings


def _get_effective_size(settings, module_name):
    u"""按 Config Schema 计算 Global Scale * Module Size。"""
    global_scale = float(
        _get_setting(
            settings,
            config.face_controller_global_scale_attr
        )
    )
    module_scale = 1.0
    module_attr = config.face_controller_size_attr_names.get(
        module_name
    )

    if module_attr:
        module_scale = float(
            _get_setting(
                settings,
                module_attr
            )
        )

    return global_scale * module_scale


def _get_expected_scale_ratio(
        previous_settings,
        new_settings,
        module_name
):
    u"""返回 Representative Controller 预期 Shape 缩放比例。"""
    old_effective_size = _get_effective_size(
        previous_settings,
        module_name
    )
    new_effective_size = _get_effective_size(
        new_settings,
        module_name
    )

    if old_effective_size <= 0.0:
        raise RuntimeError(
            u"旧 Controller Effective Size 必须大于 0：{}".format(
                module_name
            )
        )

    return new_effective_size / old_effective_size


def _snapshot_controller_states(ctrl_nodes):
    u"""记录全部 Face Controller 的 Transform / Shape 状态。"""
    states = {}

    for ctrl_node in ctrl_nodes:
        states[ctrl_node] = {
            "world_matrix": _get_world_matrix(
                ctrl_node
            ),
            "scale": _get_transform_scale(
                ctrl_node
            ),
            "shape_radius": control_shape_utils.get_shape_radius(
                ctrl_node
            ),
            "shape_data": control_shape_utils.get_shape_data(
                ctrl_node
            ),
            "shape_color": control_shape_utils.get_shape_color(
                ctrl_node,
                default=None
            ),
        }

    return states


def _get_face_jnt_nodes(face_jnt_grp):
    u"""只返回 Face Jnt Group 层级下的 Jnt Long Path。"""
    face_jnt_grp_node = _resolve_unique_node(
        face_jnt_grp
    )
    jnt_nodes = cmds.listRelatives(
        face_jnt_grp_node,
        allDescendents=True,
        type=__MUZI_MAYA_JNT_PROTECTED_00000__,
        fullPath=True
    ) or []
    jnt_nodes.sort()
    return jnt_nodes


def _snapshot_jnt_matrices(face_jnt_grp):
    u"""只记录 Face Jnt Group 下全部 Jnt World Matrix。"""
    jnt_nodes = _get_face_jnt_nodes(
        face_jnt_grp
    )
    jnt_matrices = {}

    for jnt_node in jnt_nodes:
        jnt_matrices[jnt_node] = _get_world_matrix(
            jnt_node
        )

    return jnt_matrices


def _resolve_output_node(ctrl_node):
    u"""通过 CtrlBase Naming API 解析 Controller 对应 Output。"""
    ctrl_short_name = _get_canonical_short_name(
        ctrl_node
    )
    hierarchy_names = ctrl_base.get_ctrl_hierarchy_names(
        ctrl_short_name,
        create_sub_ctrl=False
    )
    return _resolve_unique_node(
        hierarchy_names["output"]
    )


def _snapshot_representative_states():
    u"""记录 Representative Ctrl 的 Output / Radius / CV / Color。"""
    states = {}

    for representative in REPRESENTATIVE_CONTROLLERS:
        ctrl_node = _resolve_unique_node(
            representative["name"]
        )
        output_node = _resolve_output_node(
            ctrl_node
        )
        module_name = controller_appearance._get_ctrl_module(
            ctrl_node
        )
        side = controller_appearance._get_ctrl_side(
            ctrl_node
        )

        if module_name != representative["module"]:
            raise RuntimeError(
                u"Controller Module 解析错误：{} expected={} actual={}".format(
                    representative["name"],
                    representative["module"],
                    module_name
                )
            )

        if side != representative["side"]:
            raise RuntimeError(
                u"Controller Side 解析错误：{} expected={} actual={}".format(
                    representative["name"],
                    representative["side"],
                    side
                )
            )

        states[representative["name"]] = {
            "ctrl_node": ctrl_node,
            "output_node": output_node,
            "output_world_matrix": _get_world_matrix(
                output_node
            ),
            "shape_radius": control_shape_utils.get_shape_radius(
                ctrl_node
            ),
            "shape_data": control_shape_utils.get_shape_data(
                ctrl_node
            ),
            "shape_color": control_shape_utils.get_shape_color(
                ctrl_node,
                default=None
            ),
            "module": module_name,
            "side": side,
        }

    return states


def _validate_controller_transform_invariants(
        before_states,
        ctrl_nodes
):
    u"""确认 Appearance 更新没有修改 Controller Transform。"""
    for ctrl_node in ctrl_nodes:
        before_state = before_states[ctrl_node]
        after_world_matrix = _get_world_matrix(
            ctrl_node
        )
        after_scale = _get_transform_scale(
            ctrl_node
        )

        _assert_values_close(
            u"Controller World Matrix {}".format(ctrl_node),
            before_state["world_matrix"],
            after_world_matrix
        )
        _assert_values_close(
            u"Controller Scale {}".format(ctrl_node),
            [1.0, 1.0, 1.0],
            after_scale
        )

    return True


def _validate_jnt_invariants(
        face_jnt_grp,
        before_jnt_matrices
):
    u"""确认 Appearance 更新没有移动、增加或删除任何 Face Jnt。"""
    after_jnt_nodes = _get_face_jnt_nodes(
        face_jnt_grp
    )

    if len(after_jnt_nodes) != len(before_jnt_matrices):
        raise RuntimeError(
            u"Appearance 更新前后 Face Jnt 数量发生变化：before={} after={}".format(
                len(before_jnt_matrices),
                len(after_jnt_nodes)
            )
        )

    for jnt_node in before_jnt_matrices:
        if not cmds.objExists(jnt_node):
            raise RuntimeError(
                u"Appearance 更新后 Face Jnt 丢失：{}".format(
                    jnt_node
                )
            )

        _assert_values_close(
            u"Face Jnt World Matrix {}".format(jnt_node),
            before_jnt_matrices[jnt_node],
            _get_world_matrix(jnt_node)
        )

    return True


def _validate_representative_appearance(
        before_states,
        previous_settings,
        new_settings
):
    u"""验证 Representative Ctrl 的 Module Size、Color、Output 和 CV。"""
    validated_names = []

    for representative in REPRESENTATIVE_CONTROLLERS:
        ctrl_name = representative["name"]
        before_state = before_states[ctrl_name]
        ctrl_node = before_state["ctrl_node"]
        module_name = before_state["module"]
        side = before_state["side"]

        after_radius = control_shape_utils.get_shape_radius(
            ctrl_node
        )
        after_shape_data = control_shape_utils.get_shape_data(
            ctrl_node
        )
        after_color = control_shape_utils.get_shape_color(
            ctrl_node,
            default=None
        )
        after_output_matrix = _get_world_matrix(
            before_state["output_node"]
        )

        expected_ratio = _get_expected_scale_ratio(
            previous_settings,
            new_settings,
            module_name
        )
        expected_radius = (
            float(before_state["shape_radius"]) *
            expected_ratio
        )

        if abs(after_radius - expected_radius) > RADIUS_TOLERANCE:
            raise RuntimeError(
                u"Controller Shape Radius 错误：{} expected={} actual={} ratio={}".format(
                    ctrl_name,
                    expected_radius,
                    after_radius,
                    expected_ratio
                )
            )

        if before_state["shape_data"] == after_shape_data:
            raise RuntimeError(
                u"Controller Shape CV 没有发生预期变化：{}".format(
                    ctrl_name
                )
            )

        color_attr = config.face_controller_color_attr_names[side]
        expected_color = int(
            _get_setting(
                new_settings,
                color_attr
            )
        )

        if after_color != expected_color:
            raise RuntimeError(
                u"Controller Color 错误：{} expected={} actual={}".format(
                    ctrl_name,
                    expected_color,
                    after_color
                )
            )

        _assert_values_close(
            u"Controller Output World Matrix {}".format(ctrl_name),
            before_state["output_world_matrix"],
            after_output_matrix
        )

        validated_names.append(
            ctrl_name
        )

    return validated_names


def _validate_settings_persistence(face_guide, new_settings):
    u"""确认应用后的 Controller Settings 能正确持久化到 Face Config。"""
    face_guide.save_controller_settings(
        new_settings
    )
    loaded_settings = face_guide.load_controller_settings()

    check_attrs = [
        config.face_controller_global_scale_attr,
    ]

    for module_name in MODULE_SCALE_MULTIPLIERS:
        module_attr = config.face_controller_size_attr_names[module_name]
        check_attrs.append(
            module_attr
        )

    for side in config.face_controller_color_attr_names:
        color_attr = config.face_controller_color_attr_names[side]
        check_attrs.append(
            color_attr
        )

    for attr_name in check_attrs:
        expected_value = new_settings[attr_name]
        actual_value = loaded_settings[attr_name]

        if isinstance(expected_value, float):
            if abs(float(expected_value) - float(actual_value)) > 0.000001:
                raise RuntimeError(
                    u"Controller Setting 保存失败：{} expected={} actual={}".format(
                        attr_name,
                        expected_value,
                        actual_value
                    )
                )
        else:
            if expected_value != actual_value:
                raise RuntimeError(
                    u"Controller Setting 保存失败：{} expected={} actual={}".format(
                        attr_name,
                        expected_value,
                        actual_value
                    )
                )

    return True


def run():
    u"""在 Maya 2023 中执行完整 Controller Appearance Runtime Smoke。"""
    maya_version = require_maya_2023()
    namespace = create_namespace()
    shading_group_state = prepare_default_shading_group()

    print(
        "=" * 78
    )
    print(
        "Muzi Toolset - Face Controller Appearance Maya 2023 Runtime Smoke Test"
    )
    print(
        "Maya: {}".format(
            maya_version
        )
    )
    print(
        "=" * 78
    )

    try:
        # ---------------------------------------------------------------------
        # Step 01：创建完整 Face Fixture，并继承 Step 01 实际 Config Node
        # ---------------------------------------------------------------------
        fixture_dict = _create_namespace_safe_face_fixture(
            namespace
        )
        actual_config_node = fixture_dict["config_node"]

        _set_smoke_namespace(
            namespace
        )
        face_build = face_system.FaceBuild()
        _bind_face_config(
            face_build,
            actual_config_node
        )
        _bind_face_config(
            face_build.face_guide,
            actual_config_node
        )
        face_build.run_step()

        # FaceBuild 中的 Module 都依赖短名解析，构建完成后再次固定回测试 Namespace。
        _set_smoke_namespace(
            namespace
        )

        ctrl_nodes = controller_appearance._get_face_ctrl_nodes()

        if not ctrl_nodes:
            raise RuntimeError(
                u"FaceBuild 完成后没有找到 Face Controller。"
            )

        print(
            u"[PASS] Face Fixture | Step01 + Step02 Config / Namespace 准备成功"
        )
        print(
            u"[PASS] FaceBuild | Step 03 Controller 已创建"
        )

        # ---------------------------------------------------------------------
        # Step 02：记录 Appearance 更新前的不可变状态和 Shape 状态
        # ---------------------------------------------------------------------
        face_guide = FaceGuide()
        _bind_face_config(
            face_guide,
            actual_config_node
        )
        previous_settings = face_guide.load_controller_settings()
        new_settings = _create_new_settings(
            previous_settings
        )
        controller_states = _snapshot_controller_states(
            ctrl_nodes
        )
        jnt_matrices = _snapshot_jnt_matrices(
            face_build.face_jnt_grp
        )
        representative_states = _snapshot_representative_states()

        # ---------------------------------------------------------------------
        # Step 03：只通过正式 Appearance Application Layer 实时更新 Shape
        # ---------------------------------------------------------------------
        apply_result = controller_appearance.apply_controller_settings(
            previous_settings,
            new_settings
        )

        if apply_result["scaled_ctrl_count"] != len(ctrl_nodes):
            raise RuntimeError(
                u"Global Scale 应缩放全部 Face Ctrl：expected={} actual={}".format(
                    len(ctrl_nodes),
                    apply_result["scaled_ctrl_count"]
                )
            )

        print(
            u"[PASS] Appearance | Global / Module Size + Side Color 已应用"
        )

        # ---------------------------------------------------------------------
        # Step 04：验证 Transform / Output / Face Jnt 完全不受 Shape 编辑影响
        # ---------------------------------------------------------------------
        _validate_controller_transform_invariants(
            controller_states,
            ctrl_nodes
        )
        _validate_jnt_invariants(
            face_build.face_jnt_grp,
            jnt_matrices
        )
        representative_names = _validate_representative_appearance(
            representative_states,
            previous_settings,
            new_settings
        )
        alignment_pairs = validate_guide_ctrl_alignment()

        print(
            u"[PASS] Invariants | Ctrl Matrix / Scale / Output / Face Jnt 全部保持不变"
        )
        print(
            u"[PASS] Shape | Eye / Nose / CheekBone / Jaw CV 尺寸与颜色正确"
        )
        print(
            u"[PASS] Alignment | {} 个 Guide / Ctrl Pair 仍然对齐".format(
                len(alignment_pairs)
            )
        )

        # ---------------------------------------------------------------------
        # Step 05：验证 UI 回调后续使用的 Config 持久化路径
        # ---------------------------------------------------------------------
        _validate_settings_persistence(
            face_guide,
            new_settings
        )

        print(
            u"[PASS] Config | Controller Settings 保存 / 读取一致"
        )
        print(
            "-" * 78
        )
        print(
            u"Passed: 7 | Failed: 0"
        )
        print(
            "=" * 78
        )

        return {
            "maya_version": maya_version,
            "passed": True,
            "failed": 0,
            "summary": {
                "config_node": actual_config_node,
                "controller_count": len(ctrl_nodes),
                "jnt_count": len(jnt_matrices),
                "scaled_ctrl_count": apply_result["scaled_ctrl_count"],
                "colored_ctrl_count": apply_result["colored_ctrl_count"],
                "changed_ctrl_count": apply_result["changed_ctrl_count"],
                "representative_ctrls": representative_names,
                "guide_ctrl_alignment_count": len(alignment_pairs),
                "cheekbone_module": "cheek",
                "transform_scale_invariant": [1.0, 1.0, 1.0],
            },
            "traceback": "",
        }

    except Exception as error:
        error_traceback = traceback.format_exc()

        print(
            u"[FAIL] Controller Appearance | {}".format(
                error
            )
        )
        print(
            error_traceback
        )
        print(
            "-" * 78
        )
        print(
            u"Passed: 0 | Failed: 1"
        )
        print(
            "=" * 78
        )

        return {
            "maya_version": maya_version,
            "passed": False,
            "failed": 1,
            "summary": None,
            "traceback": error_traceback,
        }

    finally:
        remove_namespace(
            namespace
        )
        restore_default_shading_group(
            shading_group_state
        )


if __name__ == "__main__":
    run()
