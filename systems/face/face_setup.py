# coding=utf-8
u"""
Step 01 - Face Setup
====================

Step 生命周期：
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
    6. 完成 Step 01，并使后续旧 Step 状态失效。

重要边界：
    - Short Name 统一由 core.rename_utils 处理；
    - Model 有效性统一由 core.mesh_utils 处理；
    - DAG Parent 统一由 core.hierarchy_utils 处理；
    - Config 的底层 Network / Message / Value 操作由 FaceBase -> core.config_utils 处理；
    - Step 生命周期入口统一由 systems.common.StepBase 提供；
    - FaceSetup 只保留 Step 01 自己的业务规则。
"""

from __future__ import print_function

from ...core import hierarchy_utils
from ...core import mesh_utils
from ...core import name_utils
from ...core import rename_utils
from . import face_base


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
        super(FaceSetup, self).__init__()

        self.step_value = 1

        # ------------------------------------------------------------
        # 原始输入。
        # 名称规范化和有效性检查统一放到 collect_inputs()。
        # ------------------------------------------------------------
        self.face_head_model = face_head_model
        self.face_lf_eye_model = face_lf_eye_model
        self.face_rt_eye_model = face_rt_eye_model
        self.upper_teech_model = upper_teech_model
        self.lower_teech_model = lower_teech_model
        self.face_tongue_model = face_tongue_model
        self.face_gum_model = face_gum_model
        self.mouth_jnt_number = mouth_jnt_number

        self.face_model_list = []
        self.work_model_name_dict = {}

        # ------------------------------------------------------------
        # Step 01 输出。
        # ------------------------------------------------------------
        self.face_head_tweak_model = None
        self.face_head_stretch_model = None
        self.face_head_deform_model = None

    # =========================================================================
    # Step Lifecycle
    # =========================================================================

    def collect_inputs(self):
        u"""
        收集、规范化并检查 Step 01 输入。

        Collect 阶段同时完成输入 Validation。
        只有本方法成功结束，后续 Prepare / Process 才允许继续。

        Returns:
            bool:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # 统一把所有模型输入转换成稳定的 DAG Short Name，避免 Reparent 后 Long Path 失效。
        self.face_head_model = rename_utils.get_short_name(
            self.face_head_model
        )
        self.face_lf_eye_model = rename_utils.get_short_name(
            self.face_lf_eye_model
        )
        self.face_rt_eye_model = rename_utils.get_short_name(
            self.face_rt_eye_model
        )
        self.upper_teech_model = rename_utils.get_short_name(
            self.upper_teech_model
        )
        self.lower_teech_model = rename_utils.get_short_name(
            self.lower_teech_model
        )
        self.face_tongue_model = rename_utils.get_short_name(
            self.face_tongue_model
        )
        self.face_gum_model = rename_utils.get_short_name(
            self.face_gum_model
        )

        # 汇总本 Step 使用的模型输入，供后续统一 Parent 和处理。
        self.face_model_list = [
            self.face_head_model,
            self.face_lf_eye_model,
            self.face_rt_eye_model,
            self.upper_teech_model,
            self.lower_teech_model,
            self.face_tongue_model,
            self.face_gum_model,
        ]

        # Head 是 Face Setup 的唯一必填模型，没有 Head 时直接阻止后续执行。
        if not self.face_head_model:
            raise RuntimeError(
                u"Face Setup 必须指定头部模型。"
            )

        model_inputs = [
            (u"Head Model", self.face_head_model),
            (u"Left Eye Model", self.face_lf_eye_model),
            (u"Right Eye Model", self.face_rt_eye_model),
            (u"Upper Teeth Model", self.upper_teech_model),
            (u"Lower Teeth Model", self.lower_teech_model),
            (u"Tongue Model", self.face_tongue_model),
            (u"Gum Model", self.face_gum_model),
        ]

        # 使用 Core 统一检查所有非空模型是否存在、名称唯一并且是 Transform。
        for model_input in model_inputs:
            label = model_input[0]
            model = model_input[1]

            if not model:
                continue

            mesh_utils.validate_model_transform(
                model,
                label=label
            )

        # 检查 Mouth Joint 数量是否满足 Face Lip 系统的业务规则。
        self.check_mouth_jnt_number()

        return True

    def prepare_data(self):
        u"""
        准备 Step 01 执行环境和中间数据。

        本阶段不创建最终 Work Model，只负责：
            1. 确保 Face Hierarchy；
            2. 生成 Work Model 名称；
            3. 清理上一次 Step 01 创建的旧 Work Model。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        # 确保 Face Rig 的基础层级已经创建完成，给后续模型整理提供目标 Group。
        self.ensure_hierarchy()

        # 生成本次 Step 01 需要使用的三个 Head Work Model 正式名称。
        self.work_model_name_dict = self.get_work_model_names()

        # 删除上一次 Step 01 生成的旧 Work Model，避免名称和旧数据冲突。
        self.delete_old_work_models(
            self.work_model_name_dict
        )

        return True

    def process_data(self):
        u"""
        执行 Step 01 的核心场景处理。

        负责整理输入模型层级，并创建三个 Head Work Model。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        # 把当前输入模型统一整理到 Face Model Group，建立稳定的模型层级。
        self.parent_input_models()

        # 根据最新 Head Model 创建 Tweak / Stretch / Deform 三个工作模型。
        self.create_work_models(
            self.work_model_name_dict
        )

        return True

    def finalize_step(self):
        u"""
        保存、检查并完成 Step 01。

        Finalize 成功后：
            1. 保存最新 Config；
            2. 验证三个 Work Model；
            3. Step 01 = Completed；
            4. Step 02～04 = Invalid。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        # 把本次 Step 01 的模型引用和参数写入统一 Face Config。
        self.save_config()

        # 检查三个 Head Work Model 是否都已正确生成并且仍然有效。
        self.validate_results()

        # 把当前 Step 标记为完成，允许 UI 进入后续 Step。
        self.set_step_completed(
            completed=True
        )

        # 当前 Step 被重新提交后，让所有后续旧结果失效，避免继续使用过期数据。
        self.invalidate_later_steps()

        return True

    def build(self):
        u"""
        兼容旧版 FaceSetup.build()。

        新代码统一使用 StepBase.run_step()。

        Returns:
            object:
                方法执行后的结果数据。
        """
        # 旧入口只转调统一 Step 生命周期，避免维护第二套执行流程。
        return self.run_step()

    # =========================================================================
    # Step 01 Business Validation
    # =========================================================================

    def check_mouth_jnt_number(self):
        u"""
        检查 Face Lip 系统要求的嘴唇 Joint 数量。

        Returns:
            bool:
                方法执行后的结果数据。

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
                方法执行后的结果数据。
        """
        # 逐个整理非空输入模型，避免可选模型为空时影响其它模型。
        for face_model in self.face_model_list:
            if not face_model:
                continue

            hierarchy_utils.Hierarchy.parent(
                face_model,
                self.face_model_grp
            )

        return True

    def get_work_model_names(self):
        u"""
        生成三个 Head Work Model 的正式名称。

        Returns:
            dict:
                方法执行后的结果数据。
        """
        # 生成 Head Tweak 工作模型名称。
        face_head_tweak_name = name_utils.Name.create_name(
            node_type="model",
            side=self.face_side,
            part="head",
            function="tweak",
            index=1
        )

        # 生成 Head Stretch 工作模型名称。
        face_head_stretch_name = name_utils.Name.create_name(
            node_type="model",
            side=self.face_side,
            part="head",
            function="stretch",
            index=1
        )

        # 生成 Head Deform 工作模型名称。
        face_head_deform_name = name_utils.Name.create_name(
            node_type="model",
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
                方法执行后的结果数据。
        """
        # 按正式名称逐个删除旧结果；不存在的模型由 Core 安全忽略。
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
                方法执行后的结果数据。
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

        # 创建 Tweak 工作模型，供后续局部微调和修型流程使用。
        self.face_head_tweak_model = mesh_utils.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_tweak_name,
            parent=self.face_tweak_grp
        )

        # 创建 Stretch 工作模型，供后续拉伸或体积相关处理使用。
        self.face_head_stretch_model = mesh_utils.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_stretch_name,
            parent=self.face_stretch_grp
        )

        # 创建 Deform 工作模型，作为后续正式变形系统的工作副本。
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
                方法执行后的结果数据。
        """
        result_models = [
            (u"Head Tweak Model", self.face_head_tweak_model),
            (u"Head Stretch Model", self.face_head_stretch_model),
            (u"Head Deform Model", self.face_head_deform_model),
        ]

        # 统一通过 Core 验证三个输出模型，确保 Finalize 不会保存损坏结果。
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
                方法执行后的结果数据。
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

        # 使用 Message 保存模型节点引用，保证 Maya Rename 后引用仍然有效。
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

        # 使用普通 Config Value 保存 Mouth Joint 数量，供后续 Lip Step 读取。
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
