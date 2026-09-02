# coding=utf-8
u"""
Step 01 - Face Setup
====================

Module 生命周期：
    collect_inputs()
    prepare_data()
    process_data()
    finalize_step()

职责：
    1. 收集并检查 Head / Eye / Teeth / Tongue / Gum 输入；
    2. 检查嘴唇 Joint 数量；
    3. 准备 Face 基础层级和 Work Model 名称；
    4. 整理输入模型并创建 Tweak / Stretch / Deform Head；
    5. 保存 Step 01 Config；
    6. 完成 Step 01，并使后续旧 Step 状态失效；
    7. 把 Face Workflow 当前进度推进到 Step 02。

重要边界：
    - Rig Name 统一继承 FaceBase -> RigBase；
    - Short Name 统一由 core.rename_utils 处理；
    - Model 有效性统一由 core.mesh_utils 处理；
    - DAG Parent 统一由 core.hierarchy_utils 处理；
    - Config 的底层 Network / Message / Value 操作由 FaceBase -> core.config_utils 处理；
    - Module 生命周期入口统一由 systems.module_base.ModuleBase 提供；
    - FaceSetup 覆盖 process_data()，只保留 Step 01 自己的业务规则。
"""

from __future__ import print_function

from ....core import hierarchy_utils
from ....core import mesh_utils
from ....core import rename_utils
from .. import face_base


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
        u"""
        初始化 Step 01 输入。

        Args:
            face_head_model (str):
                当前检查、绑定、复制或变形使用的模型 / Mesh 节点。
            face_lf_eye_model (str):
                当前检查、绑定、复制或变形使用的模型 / Mesh 节点。
            face_rt_eye_model (str):
                当前检查、绑定、复制或变形使用的模型 / Mesh 节点。
            upper_teech_model (str):
                当前检查、绑定、复制或变形使用的模型 / Mesh 节点。
            lower_teech_model (str):
                当前检查、绑定、复制或变形使用的模型 / Mesh 节点。
            face_tongue_model (str):
                当前检查、绑定、复制或变形使用的模型 / Mesh 节点。
            face_gum_model (str):
                当前检查、绑定、复制或变形使用的模型 / Mesh 节点。
            mouth_jnt_number (int):
                嘴唇分布系统需要创建的 Joint 总数量。
        """
        # -------------------------------------------------------------------------
        # Step 01：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        super(FaceSetup, self).__init__()

        self.step_value = 1

        self.face_head_model = face_head_model
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.face_lf_eye_model = face_lf_eye_model
        self.face_rt_eye_model = face_rt_eye_model
        self.upper_teech_model = upper_teech_model
        self.lower_teech_model = lower_teech_model
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.face_tongue_model = face_tongue_model
        self.face_gum_model = face_gum_model
        self.mouth_jnt_number = mouth_jnt_number

        self.face_model_list = []
        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.work_model_name_dict = {}

        self.face_head_tweak_model = None
        self.face_head_stretch_model = None
        # -------------------------------------------------------------------------
        # Step 05：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.face_head_deform_model = None

    # =========================================================================
    # Module Lifecycle
    # =========================================================================

    def collect_inputs(self):
        u"""

                收集、规范化并检查 Step 01 输入。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.face_head_model = rename_utils.get_short_name(
            self.face_head_model
        )
        self.face_lf_eye_model = rename_utils.get_short_name(
            self.face_lf_eye_model
        )
        self.face_rt_eye_model = rename_utils.get_short_name(
            self.face_rt_eye_model
        )
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.upper_teech_model = rename_utils.get_short_name(
            self.upper_teech_model
        )
        self.lower_teech_model = rename_utils.get_short_name(
            self.lower_teech_model
        )
        self.face_tongue_model = rename_utils.get_short_name(
            self.face_tongue_model
        )
        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.face_gum_model = rename_utils.get_short_name(
            self.face_gum_model
        )

        self.face_model_list = [
            self.face_head_model,
            self.face_lf_eye_model,
            self.face_rt_eye_model,
            self.upper_teech_model,
            self.lower_teech_model,
            self.face_tongue_model,
            self.face_gum_model,
        ]

        if not self.face_head_model:
            raise RuntimeError(
                u"Face Setup 必须指定头部模型。"
            )

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        model_inputs = [
            (u"Head Model", self.face_head_model),
            (u"Left Eye Model", self.face_lf_eye_model),
            (u"Right Eye Model", self.face_rt_eye_model),
            (u"Upper Teeth Model", self.upper_teech_model),
            (u"Lower Teeth Model", self.lower_teech_model),
            (u"Tongue Model", self.face_tongue_model),
            (u"Gum Model", self.face_gum_model),
        ]

        for model_input in model_inputs:
            label = model_input[0]
            model = model_input[1]

            if not model:
                continue

            mesh_utils.validate_model_transform(
                model,
                label=label
            )

        self.check_mouth_jnt_number()
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def prepare_data(self):
        u"""

                准备 Step 01 执行环境和中间数据。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        self.ensure_hierarchy()
        self.work_model_name_dict = self.get_work_model_names()
        self.delete_old_work_models(
            self.work_model_name_dict
        )
        return True

    def process_data(self):
        u"""

                执行 Step 01 的核心场景处理。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        self.parent_input_models()
        self.create_work_models(
            self.work_model_name_dict
        )
        return True

    def finalize_step(self):
        u"""

                保存、检查并完成 Step 01。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        self.ensure_config_layout()
        self.save_config()
        self.validate_results()
        self.set_step_completed(
            completed=True
        )
        self.invalidate_later_steps()
        self.set_current_step_value(
            2
        )
        self.organize_config_attributes()
        return True

    # =========================================================================
    # Step 01 Business Validation
    # =========================================================================

    def check_mouth_jnt_number(self):
        u"""

                检查 Face Lip 系统要求的嘴唇 Joint 数量。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。
                    TypeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。
                    ValueError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """
        if self.mouth_jnt_number is None:
            raise RuntimeError(
                u"没有设置嘴唇 Joint 数量。"
            )

        if not isinstance(self.mouth_jnt_number, int):
            raise TypeError(
                u"嘴唇 Joint 数量必须是整数。"
            )

        if self.mouth_jnt_number < 4:
            raise ValueError(
                u"嘴唇 Joint 数量不能小于 4。"
            )

        if self.mouth_jnt_number % 4 != 0:
            raise ValueError(
                u"嘴唇 Joint 数量必须是 4 的倍数，当前值为: {}".format(
                    self.mouth_jnt_number
                )
            )

        return True

    # =========================================================================
    # Model
    # =========================================================================

    def parent_input_models(self):
        u"""

                把 Step 01 指定模型整理到 Face Model Group。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        for face_model in self.face_model_list:
            if not face_model:
                continue

            hierarchy_utils.parent(
                face_model,
                self.face_model_grp
            )

        return True

    def get_work_model_names(self):
        u"""

                生成三个 Head Work Model 的正式名称。

                Returns:
                    dict:
                        包含本次构建、查询或处理结果的结构化字典。

        """
        face_head_tweak_name = self.create_name(
            type="model",
            side=self.face_side,
            part="head",
            function="tweak",
            index=1
        )
        face_head_stretch_name = self.create_name(
            type="model",
            side=self.face_side,
            part="head",
            function="stretch",
            index=1
        )
        face_head_deform_name = self.create_name(
            type="model",
            side=self.face_side,
            part="head",
            function="deform",
            index=1
        )

        return {
            "tweak": face_head_tweak_name,
            "stretch": face_head_stretch_name,
            "deform": face_head_deform_name,
        }

    def delete_old_work_models(self, work_model_name_dict):
        u"""

                删除上一次 Step 01 创建的旧 Head Work Model。

                Args:
                    work_model_name_dict (dict):
                        Step 01 三个 Head Work Model（tweak / stretch / deform）的名称映射。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        for key in work_model_name_dict:
            model = work_model_name_dict.get(
                key
            )

            if not model:
                continue

            mesh_utils.delete_model(
                model,
                ignore_missing=True
            )

        return True

    def create_work_models(self, work_model_name_dict):
        u"""

                根据最新 Head Model 创建三个独立工作模型。

                Args:
                    work_model_name_dict (dict):
                        Step 01 三个 Head Work Model（tweak / stretch / deform）的名称映射。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        face_head_tweak_name = work_model_name_dict.get(
            "tweak"
        )
        face_head_stretch_name = work_model_name_dict.get(
            "stretch"
        )
        face_head_deform_name = work_model_name_dict.get(
            "deform"
        )

        self.face_head_tweak_model = mesh_utils.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_tweak_name,
            parent=self.face_tweak_grp
        )
        self.face_head_stretch_model = mesh_utils.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_stretch_name,
            parent=self.face_stretch_grp
        )
        self.face_head_deform_model = mesh_utils.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_deform_name,
            parent=self.face_deform_grp
        )

        return True

    def validate_results(self):
        u"""

                检查 Step 01 必须生成的三个 Head Work Model。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        result_models = [
            (u"Head Tweak Model", self.face_head_tweak_model),
            (u"Head Stretch Model", self.face_head_stretch_model),
            (u"Head Deform Model", self.face_head_deform_model),
        ]

        for result_model in result_models:
            label = result_model[0]
            model = result_model[1]

            mesh_utils.validate_model_transform(
                model,
                label=label
            )

        return True

    # =========================================================================
    # Config
    # =========================================================================

    def save_config(self):
        u"""

                把 Step 01 最新设置保存到 Face Config。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        model_config_dict = {
            "face_head_model": self.face_head_model,
            "face_lf_eye_model": self.face_lf_eye_model,
            "face_rt_eye_model": self.face_rt_eye_model,
            "upper_teech_model": self.upper_teech_model,
            "lower_teech_model": self.lower_teech_model,
            "face_tongue_model": self.face_tongue_model,
            "face_gum_model": self.face_gum_model,
        }

        self.set_config_messages(
            attrs_dict=model_config_dict,
            force=True,
            clear_empty=True
        )

        value_config_dict = {
            "mouth_jnt_number": self.mouth_jnt_number,
        }
        value_type_dict = {
            "mouth_jnt_number": "long",
        }

        self.set_config_values(
            attrs_dict=value_config_dict,
            attr_types=value_type_dict,
            lock=False,
            hide=False
        )

        return True


__all__ = [
    "FaceSetup",
]
