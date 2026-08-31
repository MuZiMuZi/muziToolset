# coding=utf-8
u"""
Face Setup Maya Smoke Test
==========================

在 Maya 2023+ 中验证 Step 01 的真实 Scene 行为。

默认会新建空场景，请不要在需要保存的工作场景中直接运行。

运行：

    from muziToolset.tests.maya import face_setup_smoke
    face_setup_smoke.run()
"""

from __future__ import print_function

import pymel.core as pm

from muziToolset.systems.face import config
from muziToolset.systems.face.face_config import FaceConfig
from muziToolset.systems.face.setup import FaceSetup


def create_mesh(name, scale=1.0):
    model = pm.polySphere(
        name=name,
        radius=float(scale),
        constructionHistory=False
    )[0]
    return model


def create_source_models():
    return {
        "head_model": create_mesh("test_head_model", 5.0),
        "left_eye_model": create_mesh("test_left_eye_model", 1.0),
        "right_eye_model": create_mesh("test_right_eye_model", 1.0),
        "upper_teeth_model": create_mesh("test_upper_teeth_model", 1.5),
        "lower_teeth_model": create_mesh("test_lower_teeth_model", 1.5),
        "tongue_model": create_mesh("test_tongue_model", 1.0),
        "gum_model": create_mesh("test_gum_model", 1.5),
    }


def get_node_uuid(node):
    values = pm.ls(
        node,
        uuid=True
    )

    if not values:
        raise RuntimeError(
            u"无法读取 Node UUID：{}".format(node)
        )

    return values[0]


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def validate_setup_result(source_models, previous_work_uuids=None):
    face_config = FaceConfig()
    setup_data = face_config.load_setup()

    assert_true(
        face_config.exists(),
        u"Face Config 没有创建。"
    )

    for source_key in config.setup_source_node_attributes:
        assert_true(
            setup_data[source_key] == source_models[source_key],
            u"Source Model Config 不正确：{}".format(source_key)
        )
        assert_true(
            source_models[source_key].getParent() is None,
            u"Source Model 不应该被 Face Setup 改 Parent：{}".format(
                source_models[source_key]
            )
        )

    expected_work_parents = {
        "head_tweak_model": config.tweak_group_name,
        "head_stretch_model": config.stretch_group_name,
        "head_deform_model": config.deform_group_name,
    }

    work_uuids = {}

    for work_key in config.setup_work_node_attributes:
        work_model = setup_data[work_key]

        assert_true(
            work_model is not None,
            u"没有保存 Work Model：{}".format(work_key)
        )
        assert_true(
            pm.objExists(work_model),
            u"Work Model 不存在：{}".format(work_model)
        )
        assert_true(
            work_model.getParent() == pm.PyNode(expected_work_parents[work_key]),
            u"Work Model Parent 不正确：{}".format(work_model)
        )

        work_uuids[work_key] = get_node_uuid(work_model)

    if previous_work_uuids is not None:
        for work_key in work_uuids:
            assert_true(
                work_uuids[work_key] != previous_work_uuids[work_key],
                u"Setup 重建后 Work Model 没有被替换：{}".format(work_key)
            )

    assert_true(
        int(setup_data["mouth_joint_count"]) == 32,
        u"Mouth Joint Count 保存错误。"
    )
    assert_true(
        face_config.is_step_completed(1),
        u"Step 01 没有标记完成。"
    )
    assert_true(
        not face_config.is_step_completed(2),
        u"Step 02 应该处于未完成状态。"
    )
    assert_true(
        not face_config.is_step_completed(3),
        u"Step 03 应该处于未完成状态。"
    )
    assert_true(
        not face_config.is_step_completed(4),
        u"Step 04 应该处于未完成状态。"
    )
    assert_true(
        face_config.get_current_step() == 2,
        u"完成 Setup 后 Current Step 应该是 2。"
    )

    return work_uuids


def run(reset_scene=True):
    if reset_scene:
        pm.newFile(
            force=True
        )

    source_models = create_source_models()

    first_setup = FaceSetup(
        head_model=source_models["head_model"],
        left_eye_model=source_models["left_eye_model"],
        right_eye_model=source_models["right_eye_model"],
        upper_teeth_model=source_models["upper_teeth_model"],
        lower_teeth_model=source_models["lower_teeth_model"],
        tongue_model=source_models["tongue_model"],
        gum_model=source_models["gum_model"],
        mouth_joint_count=32
    )
    first_setup.run_step()

    first_work_uuids = validate_setup_result(
        source_models
    )

    second_setup = FaceSetup(
        head_model=source_models["head_model"],
        left_eye_model=source_models["left_eye_model"],
        right_eye_model=source_models["right_eye_model"],
        upper_teeth_model=source_models["upper_teeth_model"],
        lower_teeth_model=source_models["lower_teeth_model"],
        tongue_model=source_models["tongue_model"],
        gum_model=source_models["gum_model"],
        mouth_joint_count=32
    )
    second_setup.run_step()

    second_work_uuids = validate_setup_result(
        source_models,
        previous_work_uuids=first_work_uuids
    )

    result = {
        "source_models": source_models,
        "first_work_uuids": first_work_uuids,
        "second_work_uuids": second_work_uuids,
        "config": FaceConfig().node,
    }

    print(u"Face Setup Smoke Test Passed")
    return result


__all__ = [
    "run",
]
