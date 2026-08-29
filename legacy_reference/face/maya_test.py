import importlib

from muziToolset.face import face_guide,setup

importlib.reload(face_guide)

importlib.reload(setup)


def test_face_setup():
    print ("=" * 60)
    print (u"开始测试 FaceSetup")
    print ("=" * 60)

    # 测试模型名称
    face_head_model = "test_face_head_model"
    face_lf_eye_model = "test_face_lf_eye_model"
    face_rt_eye_model = "test_face_rt_eye_model"

    upper_teech_model = "test_upper_teech_model"
    lower_teech_model = "test_lower_teech_model"

    face_tongue_model = "test_face_tongue_model"
    face_gum_model = "test_face_gum_model"

    test_model_list = [
        face_head_model ,
        face_lf_eye_model ,
        face_rt_eye_model ,
        upper_teech_model ,
        lower_teech_model ,
        face_tongue_model ,
        face_gum_model
    ]

    # 删除旧模型
    for model in test_model_list :

        if cmds.objExists (model) :
            cmds.delete (model)

    # 创建测试模型
    cmds.polySphere (
        name = face_head_model ,
        radius = 5
    )

    cmds.polySphere (
        name = face_lf_eye_model ,
        radius = 0.8
    )

    cmds.polySphere (
        name = face_rt_eye_model ,
        radius = 0.8
    )

    cmds.polyCube (
        name = upper_teech_model
    )

    cmds.polyCube (
        name = lower_teech_model
    )

    cmds.polyCube (
        name = face_tongue_model
    )

    cmds.polyCube (
        name = face_gum_model
    )

    # 创建测试实例
    face_setup = FaceSetup (
        face_head_model = face_head_model ,
        face_lf_eye_model = face_lf_eye_model ,
        face_rt_eye_model = face_rt_eye_model ,
        upper_teech_model = upper_teech_model ,
        lower_teech_model = lower_teech_model ,
        face_tongue_model = face_tongue_model ,
        face_gum_model = face_gum_model ,
        mouth_jnt_number = 12
    )

    # 测试
    face_setup.check_model_exists ()

    print (u"FaceSetup 测试通过")

    face_setup.check_model_exists ()
    face_setup.create_hierarchy ()
    face_setup.parent_model ()
    face_setup.save_config ()


    guide = step2_face_guide.FaceGuide ()
    print (guide.face_head_model)
    print (guide.face_lf_eye_model)
    print (guide.mouth_jnt_number)
    print (guide.face_guide_grp)

