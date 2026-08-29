# coding=utf-8
u"""
Step 01 - Face Setup
====================

负责：
    1. 指定头部模型
    2. 指定左右眼模型
    3. 指定上下牙模型
    4. 指定舌头模型
    5. 指定牙龈模型
    6. 设置嘴唇关节数量
    7. 更新 Face Rig 工作模型
    8. 更新 Config Node 配置

设计：
    Config Node 只创建一次。
    Step 01 可以重复执行。
    用户修改 Step 01 后，会把最新配置重新写入同一个 Config Node。
    Step 02 / Step 03 / Step 04 统一从 Config Node 获取最新数据。
"""

from imp import reload

import maya.cmds as cmds

from ..core import hierarchyUtils
from ..core import pipelineUtils
from ..core import nameUtils

from . import face_base

reload(hierarchyUtils)
reload(pipelineUtils)
reload(nameUtils)
reload(face_base)


class FaceSetup(face_base.FaceBase):
    u"""Face Rig Step 01。"""

    def __init__(
        self,
        face_head_model=None,
        face_lf_eye_model=None,
        face_rt_eye_model=None,
        upper_teech_model=None,
        lower_teech_model=None,
        face_tongue_model=None,
        face_gum_model=None,
        mouth_jnt_number=32
    ):

        # ------------------------------------------------------------
        # 初始化 Face Rig 公共配置
        # ------------------------------------------------------------

        super().__init__()

        # ------------------------------------------------------------
        # Step 01 模型配置
        # ------------------------------------------------------------

        self.face_head_model = face_head_model

        self.face_lf_eye_model = face_lf_eye_model

        self.face_rt_eye_model = face_rt_eye_model

        self.upper_teech_model = upper_teech_model

        self.lower_teech_model = lower_teech_model

        self.face_tongue_model = face_tongue_model

        self.face_gum_model = face_gum_model

        # ------------------------------------------------------------
        # 模型列表
        # ------------------------------------------------------------

        self.face_model_list = [
            self.face_head_model,
            self.face_lf_eye_model,
            self.face_rt_eye_model,
            self.upper_teech_model,
            self.lower_teech_model,
            self.face_tongue_model,
            self.face_gum_model
        ]

        # ------------------------------------------------------------
        # Step 01 参数
        # ------------------------------------------------------------

        self.mouth_jnt_number = mouth_jnt_number

        # ------------------------------------------------------------
        # Step 01 生成的工作模型
        # ------------------------------------------------------------

        self.face_head_tweak_model = None

        self.face_head_stretch_model = None

        self.face_head_deform_model = None

    # =========================================================================
    # Check
    # =========================================================================

    def check_model_exists(self):
        u"""检查 Step 01 指定的模型是否存在。

        头部模型是必须项。
        其它模型没有指定时允许跳过。

        Returns:
            bool: 检查通过返回 True。
        """

        # ------------------------------------------------------------
        # Head Model 必须存在
        # ------------------------------------------------------------

        if self.face_head_model is None or self.face_head_model == "":

            raise RuntimeError(
                u"Face Setup 必须指定头部模型。"
            )

        # ------------------------------------------------------------
        # 检查指定的模型
        # ------------------------------------------------------------

        for face_model in self.face_model_list:

            if face_model is None:
                continue

            if face_model == "":
                continue

            if not cmds.objExists(
                face_model
            ):

                raise RuntimeError(
                    u"给定名称的模型不存在于当前 Maya 场景中: {0}".format(
                        face_model
                    )
                )

        return True

    def check_mouth_jnt_number(self):
        u"""检查嘴唇关节数量。

        规则：
            1. 必须是整数。
            2. 最小为 4。
            3. 必须是 4 的倍数。
        """

        if self.mouth_jnt_number is None:

            raise RuntimeError(
                u"没有设置嘴唇关节数量。"
            )

        if not isinstance(
            self.mouth_jnt_number,
            int
        ):

            raise TypeError(
                u"嘴唇关节数量必须是整数。"
            )

        if self.mouth_jnt_number < 4:

            raise ValueError(
                u"嘴唇关节数量不能小于 4。"
            )

        if self.mouth_jnt_number % 4 != 0:

            raise ValueError(
                u"嘴唇关节数量必须是 4 的倍数，当前值为: {0}".format(
                    self.mouth_jnt_number
                )
            )

        return True

    # =========================================================================
    # Model
    # =========================================================================

    def parent_input_models(self):
        u"""把 Step 01 指定的模型整理到 Face Model Group。"""

        for face_model in self.face_model_list:

            if face_model is None:
                continue

            if face_model == "":
                continue

            hierarchyUtils.Hierarchy.parent(
                face_model,
                self.face_model_grp
            )

        return True

    def get_work_model_names(self):
        u"""生成 Step 01 三个头部工作模型名称。

        Returns:
            dict:
                tweak / stretch / deform 对应的模型名称。
        """

        face_head_tweak_name = nameUtils.Name.create_name(
            node_type="model",
            side=self.face_side,
            part="head",
            function="tweak",
            index=1
        )

        face_head_stretch_name = nameUtils.Name.create_name(
            node_type="model",
            side=self.face_side,
            part="head",
            function="stretch",
            index=1
        )

        face_head_deform_name = nameUtils.Name.create_name(
            node_type="model",
            side=self.face_side,
            part="head",
            function="deform",
            index=1
        )

        work_model_name_dict = {
            "tweak": face_head_tweak_name,
            "stretch": face_head_stretch_name,
            "deform": face_head_deform_name
        }

        return work_model_name_dict

    def delete_old_work_models(self, work_model_name_dict):
        u"""删除 Step 01 之前生成的旧工作模型。

        当前设计：
            Step 01 重新 Build 时，
            重新根据最新 head model 创建三个工作模型。

        注意：
            后续如果 Step 02 / 03 / 04 已经依赖这些工作模型，
            Step 01 重新 Build 后，后续步骤应该重新 Build。
        """

        for key in work_model_name_dict:

            model = work_model_name_dict.get(
                key
            )

            if not model:
                continue

            if not cmds.objExists(
                model
            ):
                continue

            cmds.delete(
                model
            )

        return True

    def create_work_models(self, work_model_name_dict):
        u"""根据最新 Head Model 创建三个工作模型。"""

        # ------------------------------------------------------------
        # Tweak
        # ------------------------------------------------------------

        face_head_tweak_name = work_model_name_dict.get(
            "tweak"
        )

        self.face_head_tweak_model = pipelineUtils.Pipeline.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_tweak_name,
            parent=self.face_tweak_grp
        )

        # ------------------------------------------------------------
        # Stretch
        # ------------------------------------------------------------

        face_head_stretch_name = work_model_name_dict.get(
            "stretch"
        )

        self.face_head_stretch_model = pipelineUtils.Pipeline.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_stretch_name,
            parent=self.face_stretch_grp
        )

        # ------------------------------------------------------------
        # Deform
        # ------------------------------------------------------------

        face_head_deform_name = work_model_name_dict.get(
            "deform"
        )

        self.face_head_deform_model = pipelineUtils.Pipeline.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_deform_name,
            parent=self.face_deform_grp
        )

        return True

    def update_work_models(self):
        u"""更新 Step 01 工作模型。

        流程：
            1. 整理输入模型。
            2. 生成固定工作模型名称。
            3. 删除旧工作模型。
            4. 根据最新 Head Model 重新创建工作模型。
        """

        self.parent_input_models()

        work_model_name_dict = self.get_work_model_names()

        self.delete_old_work_models(
            work_model_name_dict
        )

        self.create_work_models(
            work_model_name_dict
        )

        return True

    # =========================================================================
    # Config
    # =========================================================================

    def save_config(self):
        u"""把 Step 01 最新设置更新到 Config Node。

        Config Node：
            不存在 -> 第一次创建。
            已存在   -> 继续使用原节点。

        Message：
            新模型   -> 替换旧连接。
            空值     -> 清除旧连接。

        Value：
            属性不存在 -> 创建。
            属性已存在 -> 更新。
        """

        # ------------------------------------------------------------
        # Config Node 只确保存在，不重复创建
        # ------------------------------------------------------------

        self.ensure_config_node()

        # ------------------------------------------------------------
        # Config Attr
        # ------------------------------------------------------------

        config_attr = self.get_config_attr()

        # ------------------------------------------------------------
        # Maya 节点配置
        # ------------------------------------------------------------

        model_config_dict = {
            "face_head_model": self.face_head_model,
            "face_lf_eye_model": self.face_lf_eye_model,
            "face_rt_eye_model": self.face_rt_eye_model,
            "upper_teech_model": self.upper_teech_model,
            "lower_teech_model": self.lower_teech_model,
            "face_tongue_model": self.face_tongue_model,
            "face_gum_model": self.face_gum_model
        }

        config_attr.connect_messages(
            attrs_dict=model_config_dict,
            force=True,
            clear_empty=True
        )

        # ------------------------------------------------------------
        # 普通数值配置
        # ------------------------------------------------------------

        value_config_dict = {
            "mouth_jnt_number": self.mouth_jnt_number
        }

        value_type_dict = {
            "mouth_jnt_number": "long"
        }

        config_attr.set_attr_values(
            attrs_dict=value_config_dict,
            attr_types=value_type_dict,
            lock=False,
            hide=False
        )

        return True

    # =========================================================================
    # Build
    # =========================================================================

    def build(self):
        u"""执行 Step 01。

        该方法允许重复执行。

        用户返回 Step 01 修改设置之后再次 Build：
            1. 基础层级不会重复创建。
            2. 工作模型会根据最新 Head Model 更新。
            3. Config Node 不会重复创建。
            4. Config 属性会更新为最新设置。
        """

        self.check_model_exists()

        self.check_mouth_jnt_number()

        self.ensure_hierarchy()

        self.update_work_models()

        self.save_config()

        return True


# =============================================================================
# Maya Test
# =============================================================================

def maya_test_face_setup():
    u"""在 Maya 中测试 FaceSetup。"""

    print(
        "=" * 60
    )

    print(
        u"开始测试 FaceSetup"
    )

    print(
        "=" * 60
    )

    # -------------------------------------------------------------------------
    # 测试模型名称
    # -------------------------------------------------------------------------

    face_head_model = "test_face_head_model"

    face_lf_eye_model = "test_face_lf_eye_model"

    face_rt_eye_model = "test_face_rt_eye_model"

    upper_teech_model = "test_upper_teech_model"

    lower_teech_model = "test_lower_teech_model"

    face_tongue_model = "test_face_tongue_model"

    face_gum_model = "test_face_gum_model"

    test_model_list = [
        face_head_model,
        face_lf_eye_model,
        face_rt_eye_model,
        upper_teech_model,
        lower_teech_model,
        face_tongue_model,
        face_gum_model
    ]

    # -------------------------------------------------------------------------
    # 删除旧测试输入模型
    # -------------------------------------------------------------------------

    for model in test_model_list:

        if not cmds.objExists(
            model
        ):
            continue

        cmds.delete(
            model
        )

    # -------------------------------------------------------------------------
    # 创建测试模型
    # -------------------------------------------------------------------------

    cmds.polySphere(
        name=face_head_model,
        radius=5
    )

    cmds.polySphere(
        name=face_lf_eye_model,
        radius=0.8
    )

    cmds.polySphere(
        name=face_rt_eye_model,
        radius=0.8
    )

    cmds.polyCube(
        name=upper_teech_model
    )

    cmds.polyCube(
        name=lower_teech_model
    )

    cmds.polyCube(
        name=face_tongue_model
    )

    cmds.polyCube(
        name=face_gum_model
    )

    # -------------------------------------------------------------------------
    # 创建 Step 01
    # -------------------------------------------------------------------------

    face_setup_object = FaceSetup(
        face_head_model=face_head_model,
        face_lf_eye_model=face_lf_eye_model,
        face_rt_eye_model=face_rt_eye_model,
        upper_teech_model=upper_teech_model,
        lower_teech_model=lower_teech_model,
        face_tongue_model=face_tongue_model,
        face_gum_model=face_gum_model,
        mouth_jnt_number=32
    )

    # -------------------------------------------------------------------------
    # 完整 Build
    # -------------------------------------------------------------------------

    face_setup_object.build()

    print(
        u"FaceSetup Build 测试通过"
    )

    print(
        u"Config Node: {0}".format(
            face_setup_object.config_node
        )
    )

    print(
        u"Head Config: {0}".format(
            face_setup_object.get_config_message(
                "face_head_model"
            )
        )
    )

    print(
        u"Mouth Joint Number: {0}".format(
            face_setup_object.get_config_value(
                "mouth_jnt_number"
            )
        )
    )

    return face_setup_object
